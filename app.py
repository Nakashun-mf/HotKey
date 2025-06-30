import keyboard
import pyautogui
import json
import logging
from typing import List, Dict, Any
from pathlib import Path

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('hotkey_app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class HotkeyManager:
    """ホットキー管理クラス"""
    
    def __init__(self, config_file: str = 'config.json'):
        self.config_file = Path(config_file)
        self.config: Dict[str, Any] = {}
        
    def load_config(self) -> Dict[str, Any]:
        """設定ファイルを読み込む"""
        try:
            if not self.config_file.exists():
                logger.warning(f"設定ファイル {self.config_file} が見つかりません。デフォルト設定を使用します。")
                return {"hotkeys": []}
                
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                logger.info(f"設定ファイル {self.config_file} を読み込みました")
                return config
                
        except json.JSONDecodeError as e:
            logger.error(f"設定ファイルの形式が正しくありません: {e}")
            return {"hotkeys": []}
        except Exception as e:
            logger.error(f"設定ファイルの読み込み中にエラーが発生しました: {e}")
            return {"hotkeys": []}
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """設定の妥当性をチェック"""
        if not isinstance(config, dict) or "hotkeys" not in config:
            logger.error("設定ファイルに 'hotkeys' キーが見つかりません")
            return False
            
        if not isinstance(config["hotkeys"], list):
            logger.error("'hotkeys' は配列である必要があります")
            return False
            
        for i, hotkey in enumerate(config["hotkeys"]):
            if not isinstance(hotkey, dict):
                logger.error(f"ホットキー設定 {i} は辞書である必要があります")
                return False
            if "key" not in hotkey or "actions" not in hotkey:
                logger.error(f"ホットキー設定 {i} に 'key' または 'actions' が見つかりません")
                return False
            if not isinstance(hotkey["actions"], list):
                logger.error(f"ホットキー設定 {i} の 'actions' は配列である必要があります")
                return False
                
        return True
    
    def perform_actions(self, actions: List[str]) -> None:
        """指定されたアクションのリストを順番に実行する"""
        try:
            for action in actions:
                logger.debug(f"アクション実行: {action}")
                
                if action == "right_click":
                    pyautogui.click(button='right')
                elif "+" in action:
                    # 複合キーの処理（例：ctrl+v）
                    keys = action.split("+")
                    pyautogui.hotkey(*keys)
                else:
                    pyautogui.press(action)
                    
                # アクション間の短い待機時間
                pyautogui.sleep(0.1)
                
        except Exception as e:
            logger.error(f"アクション実行中にエラーが発生しました: {e}")
    
    def register_hotkeys(self) -> None:
        """設定ファイルからホットキーを登録する"""
        self.config = self.load_config()
        
        if not self.validate_config(self.config):
            logger.error("設定ファイルの検証に失敗しました")
            return
            
        registered_count = 0
        for hotkey_config in self.config["hotkeys"]:
            try:
                key = hotkey_config["key"]
                actions = hotkey_config["actions"]
                
                keyboard.add_hotkey(
                    key, 
                    lambda a=actions: self.perform_actions(a)
                )
                logger.info(f"ホットキー '{key}' を登録しました")
                registered_count += 1
                
            except Exception as e:
                logger.error(f"ホットキー '{key}' の登録に失敗しました: {e}")
                
        logger.info(f"合計 {registered_count} 個のホットキーを登録しました")
    
    def start(self) -> None:
        """ホットキーマネージャーを開始する"""
        try:
            self.register_hotkeys()
            logger.info("ホットキーマネージャーを開始しました。終了するには Ctrl+C を押してください。")
            keyboard.wait()
        except KeyboardInterrupt:
            logger.info("ホットキーマネージャーを終了します")
        except Exception as e:
            logger.error(f"予期しないエラーが発生しました: {e}")

def main() -> None:
    """メイン関数"""
    manager = HotkeyManager()
    manager.start()

if __name__ == "__main__":
    main()