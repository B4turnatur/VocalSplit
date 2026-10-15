@echo off
REM Start der portablen VocalSplit-Version (wird von build_portable.bat als start.bat kopiert)
cd /d "%~dp0"
set "PATH=%~dp0ffmpeg;%PATH%"
set PYTHONNOUSERSITE=1
set PYTHONUTF8=1
python\python.exe -s app.py
pause
