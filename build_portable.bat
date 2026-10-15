@echo off
REM Baut die portable Version nach dist\VocalSplit (Ordner kopieren -> start.bat doppelklicken, keine Installation noetig).
REM Aufruf:  build_portable.bat          ohne Modelle (werden beim ersten Benutzen geladen)
REM          build_portable.bat models   inkl. der schon geladenen Modelle aus models\ (offline nutzbar)
REM Voraussetzung: install.bat wurde ausgefuehrt (.venv existiert), uv und ffmpeg im PATH.
setlocal
cd /d "%~dp0"
set "D=dist\VocalSplit"
if exist "%D%" rmdir /s /q "%D%"
mkdir "%D%\ffmpeg" || exit /b 1

REM 1) Standalone-Python, auf dem die .venv basiert, komplett kopieren
for /f "tokens=2 delims==" %%h in ('findstr /b "home" .venv\pyvenv.cfg') do set "PYHOME=%%h"
set "PYHOME=%PYHOME:~1%"
robocopy "%PYHOME%" "%D%\python" /e /nfl /ndl /njh /njs /np >nul
if not exist "%D%\python\python.exe" (echo FEHLER: Python nicht kopiert aus "%PYHOME%" & exit /b 1)

REM 2) Exakt dieselben Paketversionen wie in .venv hineininstallieren (Kopien statt Hardlinks)
uv pip freeze --python .venv\Scripts\python.exe > "%D%\requirements.txt"
uv pip install --python "%D%\python\python.exe" --break-system-packages --link-mode=copy ^
  --extra-index-url https://download.pytorch.org/whl/cu128 --index-strategy unsafe-best-match ^
  -r "%D%\requirements.txt" || exit /b 1

REM 3) ffmpeg + App + Starter
REM (Schleifenvariable G, weil f/d/p in %%~dp... selbst Modifier sind)
for /f "delims=" %%G in ('where ffmpeg') do (copy /y "%%~dpGffmpeg.exe" "%D%\ffmpeg\" >nul & copy /y "%%~dpGffprobe.exe" "%D%\ffmpeg\" >nul)
if not exist "%D%\ffmpeg\ffmpeg.exe" (echo FEHLER: ffmpeg nicht gefunden/kopiert & exit /b 1)
copy /y app.py "%D%\" >nul
copy /y portable_start.bat "%D%\start.bat" >nul

REM 4) Optional Modelle
if /i "%~1"=="models" robocopy models "%D%\models" /e /nfl /ndl /njh /njs /np >nul

echo Fertig: %D%
