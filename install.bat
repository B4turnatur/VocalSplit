@echo off
REM Einmalige Installation (braucht uv: https://docs.astral.sh/uv/ und ffmpeg im PATH)
cd /d "%~dp0"
uv venv --python 3.12 .venv
uv pip install --python .venv\Scripts\python.exe torch torchaudio --index-url https://download.pytorch.org/whl/cu128
uv pip install --python .venv\Scripts\python.exe "audio-separator[gpu]" gradio audioread "onnxruntime-gpu<1.24"
pause
