from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import logging
import threading
from pathlib import Path
from typing import Dict, Any, Optional
import sys

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ConfigManager:
    """設定ファイル管理クラス"""
    
    def __init__(self, config_file: str = 'config.json'):
        self.config_file = Path(config_file)
    
    def load_config(self) -> Dict[str, Any]:
        """設定ファイルを読み込む"""
        try:
            if not self.config_file.exists():
                logger.warning(f"設定ファイル {self.config_file} が見つかりません。デフォルト設定を返します。")
                return {"hotkeys": []}
                
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                logger.info(f"設定ファイル {self.config_file} を読み込みました")
                return config
                
        except json.JSONDecodeError as e:
            logger.error(f"設定ファイルのJSONが無効です: {e}")
            return {"hotkeys": []}
        except Exception as e:
            logger.error(f"設定ファイルの読み込み中にエラーが発生しました: {e}")
            return {"hotkeys": []}
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """設定ファイルを保存する"""
        try:
            # 設定の妥当性をチェック
            if not self.validate_config(config):
                logger.error("無効な設定データです")
                return False
                
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
                
            logger.info(f"設定ファイル {self.config_file} を保存しました")
            return True
            
        except Exception as e:
            logger.error(f"設定ファイルの保存中にエラーが発生しました: {e}")
            return False
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """設定データの妥当性をチェック"""
        if not isinstance(config, dict):
            return False
            
        if "hotkeys" not in config:
            return False
            
        if not isinstance(config["hotkeys"], list):
            return False
            
        for hotkey in config["hotkeys"]:
            if not isinstance(hotkey, dict):
                return False
            if "key" not in hotkey or "actions" not in hotkey:
                return False
            if not isinstance(hotkey["actions"], list):
                return False
                
        return True

class ConfigHandler(SimpleHTTPRequestHandler):
    """HTTP リクエストハンドラー"""
    
    def __init__(self, *args, **kwargs):
        self.config_manager = ConfigManager()
        super().__init__(*args, **kwargs)
    
    def log_message(self, format: str, *args) -> None:
        """HTTPリクエストのログをカスタマイズ"""
        logger.info(f"{self.address_string()} - {format % args}")
    
    def send_json_response(self, status_code: int, data: Dict[str, Any]) -> None:
        """JSON レスポンスを送信する"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        response_json = json.dumps(data, ensure_ascii=False)
        self.wfile.write(response_json.encode('utf-8'))
    
    def do_OPTIONS(self) -> None:
        """CORS プリフライトリクエストを処理"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self) -> None:
        """GET リクエストを処理"""
        if self.path == '/config.json':
            try:
                config = self.config_manager.load_config()
                self.send_json_response(200, config)
            except Exception as e:
                logger.error(f"設定取得エラー: {e}")
                self.send_json_response(500, {"error": "設定の取得に失敗しました"})
        else:
            super().do_GET()
    
    def do_POST(self) -> None:
        """POST リクエストを処理"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.send_json_response(400, {"error": "リクエストボディが空です"})
                return
                
            post_data = self.rfile.read(content_length)
            
            if self.path == '/save_config':
                self.handle_save_config(post_data)
            elif self.path == '/shutdown':
                self.handle_shutdown()
            else:
                self.send_json_response(404, {"error": "エンドポイントが見つかりません"})
                
        except Exception as e:
            logger.error(f"POST リクエスト処理エラー: {e}")
            self.send_json_response(500, {"error": "内部サーバーエラー"})
    
    def handle_save_config(self, post_data: bytes) -> None:
        """設定保存リクエストを処理"""
        try:
            config = json.loads(post_data.decode('utf-8'))
            
            if self.config_manager.save_config(config):
                self.send_json_response(200, {"message": "設定を保存しました"})
            else:
                self.send_json_response(400, {"error": "設定の保存に失敗しました"})
                
        except json.JSONDecodeError as e:
            logger.error(f"JSON デコードエラー: {e}")
            self.send_json_response(400, {"error": "無効なJSONデータです"})
        except Exception as e:
            logger.error(f"設定保存エラー: {e}")
            self.send_json_response(500, {"error": "設定の保存中にエラーが発生しました"})
    
    def handle_shutdown(self) -> None:
        """シャットダウンリクエストを処理"""
        try:
            self.send_json_response(200, {"message": "サーバーを終了します"})
            logger.info("シャットダウンリクエストを受信しました")
            
            # サーバーを別スレッドで安全に終了
            def shutdown_server():
                self.server.shutdown()
                
            threading.Thread(target=shutdown_server, daemon=True).start()
            
        except Exception as e:
            logger.error(f"シャットダウン処理エラー: {e}")
            self.send_json_response(500, {"error": "シャットダウン処理でエラーが発生しました"})

class ConfigServer:
    """設定サーバークラス"""
    
    def __init__(self, port: int = 8000, host: str = 'localhost'):
        self.port = port
        self.host = host
        self.httpd: Optional[HTTPServer] = None
    
    def start(self) -> None:
        """サーバーを開始"""
        try:
            server_address = (self.host, self.port)
            self.httpd = HTTPServer(server_address, ConfigHandler)
            
            logger.info(f'サーバーを起動しました - http://{self.host}:{self.port}')
            self.httpd.serve_forever()
            
        except KeyboardInterrupt:
            logger.info('キーボード割り込みでサーバーを終了します')
        except OSError as e:
            if e.errno == 48:  # Address already in use
                logger.error(f'ポート {self.port} は既に使用されています')
            else:
                logger.error(f'サーバー起動エラー: {e}')
        except Exception as e:
            logger.error(f'予期しないエラー: {e}')
        finally:
            if self.httpd:
                self.httpd.server_close()
                logger.info('サーバーを終了しました')

def main() -> None:
    """メイン関数"""
    port = 8000
    
    # コマンドライン引数からポート番号を取得
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            logger.error("無効なポート番号です。デフォルトポート 8000 を使用します。")
    
    server = ConfigServer(port=port)
    server.start()

if __name__ == '__main__':
    main() 