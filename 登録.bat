@echo off
REM スタートメニューの「すべてのアプリ」フォルダのパスを取得
set "STARTMENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs"
set "TARGET=%STARTMENU%\キーボードマクロ"

REM フォルダ作成
if not exist "%TARGET%" (
    mkdir "%TARGET%"
)

REM ショートカット作成（setting.bat）
powershell -Command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%TARGET%\\設定アプリ.lnk');$s.TargetPath='%CD%\\setting.bat';$s.WorkingDirectory='%CD%';$s.Save()"

REM ショートカット作成（run.bat）
powershell -Command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%TARGET%\\run.lnk');$s.TargetPath='%CD%\\run.bat';$s.WorkingDirectory='%CD%';$s.Save()"

echo ショートカットの作成が完了しました。
pause