# HotKey ライブラリ更新ガイド

## 📝 更新内容

このプロジェクトは最新のライブラリに対応し、安定性と互換性を向上させました。

### ✅ 主な改善点

1. **ライブラリの明確化**: `requirements.txt`に不足していた`keyboard`と`pyautogui`を追加
2. **エラーハンドリングの強化**: 予期しないエラーに対する適切な処理を追加
3. **ログ機能の追加**: 動作状況の可視化とデバッグの改善
4. **設定検証機能**: 設定ファイルの妥当性チェック
5. **代替ライブラリオプション**: より安定した`pydirectinput-rgx`の選択肢

## 🚀 使用方法

### オプション1: 従来ライブラリ（推奨）

```bash
# 依存関係のインストール
pip install -r requirements.txt

# プログラムの実行
python app.py
```

### オプション2: 高互換性ライブラリ

ゲームや DirectX アプリケーションでより良い動作が期待できます：

```bash
# 代替ライブラリのインストール
pip install -r requirements-alternative.txt

# 代替版プログラムの実行
python app_alternative.py
```

## 📋 ライブラリ情報

### 従来版 (requirements.txt)
- `keyboard==0.13.5` - キーボードイベント処理
- `pyautogui==0.9.54` - GUI自動化
- `fastapi==0.104.1` - Web API
- `uvicorn==0.24.0` - ASGI サーバー

### 高互換性版 (requirements-alternative.txt)
- `keyboard==0.13.5` - キーボードイベント処理
- `pydirectinput-rgx==2.1.2` - DirectInput対応の改良版GUI自動化
- `fastapi==0.104.1` - Web API
- `uvicorn==0.24.0` - ASGI サーバー

## 🔧 新機能

### 1. ログ出力
プログラムの動作状況が詳細に表示されます：
```
2025-01-19 14:30:15,123 - INFO - HotKeyプログラムを開始します...
2025-01-19 14:30:15,124 - INFO - keyboardライブラリ: OK
2025-01-19 14:30:15,125 - INFO - PyAutoGUIライブラリ: OK
2025-01-19 14:30:15,126 - INFO - ホットキー 'f2' を登録しました
```

### 2. エラーハンドリング
- 設定ファイルの形式エラー検出
- ライブラリの互換性チェック
- ホットキー登録エラーの個別処理

### 3. 安全機能
- `FAILSAFE`: マウスを画面左上角に移動すると緊急停止
- `PAUSE`: 操作間の適切な待機時間設定

## 🛠️ トラブルシューティング

### Linux環境での権限エラー
```bash
# root権限で実行
sudo python app.py
```

### ライブラリインストールエラー
```bash
# システムパッケージを破壊せずにインストール
pip install --user -r requirements.txt
```

### DirectXゲームで動作しない場合
代替版を使用してください：
```bash
python app_alternative.py
```

## 📄 設定ファイル例

`config.json`:
```json
{
    "hotkeys": [
        {
            "key": "f2",
            "actions": ["right_click", "up", "up", "enter"]
        },
        {
            "key": "f3", 
            "actions": ["ctrl+v", "down"]
        }
    ]
}
```

## 🔍 互換性テスト

プログラム起動時に以下のテストが自動実行されます：
- キーボードライブラリの動作確認
- GUI自動化ライブラリの動作確認
- 設定ファイルの妥当性チェック

## 📞 サポート

問題が発生した場合は、ログ出力を確認して具体的なエラーメッセージを参照してください。