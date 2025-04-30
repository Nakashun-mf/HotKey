import keyboard
import pyautogui
import json

def perform_actions(actions):
    """指定されたアクションのリストを順番に実行する関数"""
    for action in actions:
        if action == "right_click":
            pyautogui.click(button='right')
        else:
            pyautogui.press(action)

def load_config():
    """設定ファイルを読み込む関数"""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("設定ファイルが見つかりません。")
        return {"hotkeys": []}

def register_hotkeys():
    """設定ファイルからホットキーを登録する関数"""
    config = load_config()
    for hotkey_config in config["hotkeys"]:
        key = hotkey_config["key"]
        actions = hotkey_config["actions"]
        keyboard.add_hotkey(key, lambda a=actions: perform_actions(a))
        print(f"ホットキー {key} を登録しました")

if __name__ == "__main__":
    register_hotkeys()
    print("プログラムを開始しました。終了するには Ctrl+C を押してください。")
    keyboard.wait()