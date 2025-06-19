import keyboard
import pydirectinput as pdi
import json
import sys
import time
import logging

# ログ設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# PyDirectInputの設定
pdi.PAUSE = 0.1  # 各操作間の待機時間
pdi.FAILSAFE = True  # 安全機能を有効

def perform_actions(actions):
    """指定されたアクションのリストを順番に実行する関数（PyDirectInput版）"""
    try:
        for action in actions:
            logger.info(f"実行中のアクション: {action}")
            
            if action == "right_click":
                pdi.rightClick()
            elif "+" in action:
                # 複合キーの処理（例：ctrl+v）
                keys = action.split("+")
                # キーの正規化
                normalized_keys = [key.strip().lower() for key in keys]
                pdi.hotkey(*normalized_keys)
            else:
                # 単一キーの処理
                pdi.press(action.strip().lower())
            
            # アクション間の短い待機
            time.sleep(0.05)
            
    except Exception as e:
        logger.error(f"アクション実行エラー: {e}")
        raise

def load_config():
    """設定ファイルを読み込む関数"""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            logger.info("設定ファイルを正常に読み込みました")
            return config
    except FileNotFoundError:
        logger.warning("設定ファイルが見つかりません。デフォルト設定を使用します。")
        return {"hotkeys": []}
    except json.JSONDecodeError as e:
        logger.error(f"設定ファイルの形式が不正です: {e}")
        return {"hotkeys": []}
    except Exception as e:
        logger.error(f"設定ファイル読み込みエラー: {e}")
        return {"hotkeys": []}

def validate_config(config):
    """設定の妥当性をチェックする関数"""
    if not isinstance(config, dict):
        return False
    
    if "hotkeys" not in config:
        return False
    
    if not isinstance(config["hotkeys"], list):
        return False
    
    for hotkey_config in config["hotkeys"]:
        if not isinstance(hotkey_config, dict):
            return False
        if "key" not in hotkey_config or "actions" not in hotkey_config:
            return False
        if not isinstance(hotkey_config["actions"], list):
            return False
    
    return True

def register_hotkeys():
    """設定ファイルからホットキーを登録する関数"""
    config = load_config()
    
    if not validate_config(config):
        logger.error("設定ファイルの内容が不正です")
        return False
    
    registered_count = 0
    
    for hotkey_config in config["hotkeys"]:
        try:
            key = hotkey_config["key"].strip().lower()
            actions = hotkey_config["actions"]
            
            # ホットキーを登録（エラーハンドリング付き）
            keyboard.add_hotkey(key, lambda a=actions: perform_actions(a))
            logger.info(f"ホットキー '{key}' を登録しました")
            registered_count += 1
            
        except Exception as e:
            logger.error(f"ホットキー登録エラー ({key}): {e}")
            continue
    
    logger.info(f"合計 {registered_count} 個のホットキーを登録しました")
    return registered_count > 0

def check_system_compatibility():
    """システム互換性をチェックする関数（PyDirectInput版）"""
    try:
        # キーボードライブラリのテスト
        keyboard.is_pressed('shift')
        logger.info("keyboardライブラリ: OK")
    except Exception as e:
        logger.error(f"keyboardライブラリエラー: {e}")
        return False
    
    try:
        # PyDirectInputのテスト
        pdi.size()
        logger.info("PyDirectInputライブラリ: OK")
    except Exception as e:
        logger.error(f"PyDirectInputライブラリエラー: {e}")
        return False
    
    return True

if __name__ == "__main__":
    try:
        logger.info("HotKeyプログラム（PyDirectInput版）を開始します...")
        logger.info("このバージョンはより高い互換性とゲーム対応を提供します")
        
        # システム互換性チェック
        if not check_system_compatibility():
            logger.error("システム互換性チェックに失敗しました")
            sys.exit(1)
        
        # ホットキー登録
        if not register_hotkeys():
            logger.error("ホットキーの登録に失敗しました")
            sys.exit(1)
        
        logger.info("プログラムが正常に開始されました。終了するには Ctrl+C を押してください。")
        
        # メインループ
        keyboard.wait()
        
    except KeyboardInterrupt:
        logger.info("プログラムを終了します...")
    except Exception as e:
        logger.error(f"予期しないエラーが発生しました: {e}")
        sys.exit(1)