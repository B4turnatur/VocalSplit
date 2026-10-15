# Entscheidungen

## 2026-10-15 – Technik-Stack
**Gewählt:** Python 3.12 (uv-venv `.venv`) + PyTorch **cu128** + `audio-separator` + Gradio-Weboberfläche – weil:
- RTX 50xx (Blackwell, sm_120) läuft nur mit PyTorch-Builds ab CUDA 12.8.
- `audio-separator` bündelt die aktuell besten Trennmodelle (BS-/Mel-RoFormer, Demucs v4, MDX-Net, VR) mit einer API und lädt sie automatisch.
- Gradio liefert eine moderne Oberfläche im Browser ohne eigenen Frontend-Code.
- Beschleunigung: FP16/BF16-Autocast nutzt die Tensor-Cores (5. Gen) der RTX 50xx.
**Alternativen:** Eigenes Qt/Electron-Frontend (viel mehr Code, kein Mehrwert); UVR5-GUI (fertig, aber kein eigenes Programm).
**VERWORFEN (Portable, 2026-10-15):** `.venv` einfach mitkopieren – venvs sind nicht verschiebbar (`pyvenv.cfg` zeigt mit absolutem Pfad auf das Basis-Python). PyInstaller/Nuitka – bei PyTorch+CUDA+Gradio fehleranfällig (versteckte Imports, DLLs) und kein Größenvorteil. **Gewählt:** Standalone-Python-Ordner + Pakete direkt hinein (`build_portable.bat`).
**VERWORFEN:** FP4 für Trennmodelle – die Modelle sind in FP32 trainiert, FP4-Quantisierung würde Qualität kosten, und PyTorch hat dafür keine einfache Inferenz-Unterstützung.
