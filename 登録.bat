@echo off
REM �X�^�[�g���j���[�́u���ׂẴA�v���v�t�H���_�̃p�X���擾
set "STARTMENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs"
set "TARGET=%STARTMENU%\�L�[�{�[�h�}�N��"

REM �t�H���_�쐬
if not exist "%TARGET%" (
    mkdir "%TARGET%"
)

REM �V���[�g�J�b�g�쐬�isetting.bat�j
powershell -Command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%TARGET%\\�ݒ�A�v��.lnk');$s.TargetPath='%CD%\\setting.bat';$s.WorkingDirectory='%CD%';$s.Save()"

REM �V���[�g�J�b�g�쐬�irun.bat�j
powershell -Command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%TARGET%\\run.lnk');$s.TargetPath='%CD%\\run.bat';$s.WorkingDirectory='%CD%';$s.Save()"

echo �V���[�g�J�b�g�̍쐬���������܂����B
pause