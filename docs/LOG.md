# Arbeitsprotokoll

## Session 2026-10-15 13:40
**Ausgangslage:** Neues Projekt, leerer Ordner (nur CLAUDE.md).
**Vorhaben:** Lokales Programm zum Trennen von Gesang und Musik mit den besten KI-Modellen, optimiert für RTX 5070 Ti, moderne Oberfläche.

### 13:55 – Umgebung installiert (Python 3.12, PyTorch cu128, audio-separator, Gradio)
**Warum:** RTX 5070 Ti (Blackwell, sm_120) braucht PyTorch mit CUDA 12.8.
**Gemacht:** uv-venv `.venv` mit Python 3.12, PyTorch 2.11.0+cu128, audio-separator 0.47.0 [gpu], Gradio 6.30.0. Danach `audioread` nachinstalliert (F-001) und onnxruntime-gpu auf 1.23.2 gesenkt (F-002).
**Befehle:**
    uv venv --python 3.12 .venv
    uv pip install --python .venv/Scripts/python.exe torch torchaudio --index-url https://download.pytorch.org/whl/cu128
    uv pip install --python .venv/Scripts/python.exe "audio-separator[gpu]" gradio
    uv pip install --python .venv/Scripts/python.exe audioread
    uv pip install --python .venv/Scripts/python.exe "onnxruntime-gpu<1.24"
**Ausgabe:** ✅ CUDA verfügbar, sm_120 in Arch-Liste, ONNX-Provider = CUDAExecutionProvider
**Ergebnis:** ✅

### 14:01 – App `app.py` (VocalSplit) gebaut und getestet
**Warum:** Nutzerwunsch: lokale Gesang/Musik-Trennung mit den besten Modellen, viele Funktionen, moderne Oberfläche.
**Gemacht:**
- Gradio-Oberfläche mit 3 Modi: Preset (Ensembles aus audio-separator, z. B. „Vocal Balanced“ = BS-RoFormer Resurrection + MelBand Big Beta6X), Einzelmodell (alle 169 Modelle, nach Gesangs-SDR sortiert, durchsuchbar), Stems (htdemucs_ft, htdemucs_6s, MDX23C-DrumSep).
- Nachbearbeitungskette der Gesangsspur: De-Reverb → Denoise → Karaoke (Lead/Backing).
- Erweitert: WAV/FLAC/MP3, Genauigkeit (Autocast FP16 / natives FP16 / FP32), torch.compile, Overlap, Shifts.
- Stapelverarbeitung, bis zu 8 Player, Download-Liste, Protokoll mit Zeiten + VRAM-Spitze.
- Ausgabenamen per `tidy()` gekürzt (F-003).
- `start.bat`, `install.bat`, `test_app.py`, `.claude/launch.json` angelegt.
**Dateien:** `app.py` (neu: `run()`, `tidy()`, `pick_stem()`, `gpu_info()`, UI), `test_app.py`, `start.bat`, `install.bat` (neu)
**Befehle:**
    .venv/Scripts/python.exe test_app.py
**Ausgabe:** ✅ `ok`
**Ergebnis:** ✅ funktioniert auf der GPU
**Getestet:** 20-s-Testsignal (synthetisch): Preset vocal_balanced + alle 3 Nachbearbeitungen → 24,6 s + je ~3 s (Modelle gecacht), VRAM-Spitze 4,1 GB. htdemucs_ft → 4 MP3-Stems in 10 s. ONNX-Modell UVR-MDX-NET-Inst_HQ_5 läuft. UI im Browser: Moduswechsel blendet richtige Felder ein.
**Offen:** Test mit echtem Song durch Nutzer. „Natives FP16“ wird bei Demucs, Autocast bei ONNX ignoriert (nur Warnung). Doku-Schreiben per Bash-Heredoc schlug fehl (F-004) → per Write-Tool erledigt.

### 14:30 – Portable Version gebaut und getestet
**Warum:** Nutzer möchte eine portable Version (ohne Installation auf anderen PCs lauffähig).
**Gemacht:**
- `build_portable.bat`: kopiert das Standalone-Python, auf dem `.venv` basiert (uv cpython-3.12.9, aus `pyvenv.cfg` → `home`), nach `dist\VocalSplit\python`; installiert per `uv pip freeze` exakt dieselben Pakete hinein (`--break-system-packages --link-mode=copy`, PyTorch-Index cu128, `--index-strategy unsafe-best-match`); kopiert ffmpeg/ffprobe, `app.py`, Starter. Option `models` kopiert den Modell-Cache mit.
- `portable_start.bat` → wird zu `start.bat`: setzt eigenes ffmpeg in den PATH, `PYTHONNOUSERSITE=1`, startet `python\python.exe -s app.py`.
- Erst ffmpeg nicht kopiert (F-005) → behoben, neu gebaut.
**Dateien:** `build_portable.bat` (neu), `portable_start.bat` (neu)
**Befehle:**
    build_portable.bat
**Ausgabe:** ✅ `Fertig: dist\VocalSplit` (~5 GB ohne Modelle)
**Ergebnis:** ✅
**Getestet:** Mit PATH nur auf `dist\VocalSplit\ffmpeg` + System32 (ohne .venv, ohne C:\ffmpeg): Einzelmodell bs_roformer_vocals_resurrection_unwa + De-Reverb → Modelle nach `dist\VocalSplit\models` geladen, Trennung auf GPU ok (sys.prefix = portable Python). UI-Server startet, HTTP 200 auf Port 7860 vom portablen python.exe.
**Offen:** Test auf einem zweiten PC. Die 2 im Test geladenen Modelle liegen jetzt in `dist\VocalSplit\models` (~1 GB).

### 14:45 – Öffentliches GitHub-Repo erstellt und hochgeladen
**Warum:** Nutzer möchte das Projekt auf GitHub (Wahl: öffentlich, Name VocalSplit).
**Gemacht:** Doku auf persönliche Daten geprüft (keine gefunden). `.gitignore` (`.venv/`, `models/`, `output/`, `dist/`, `__pycache__/`, `.gradio/`) und `README.md` angelegt; in CLAUDE.md §8 Sichtbarkeit auf öffentlich gesetzt. Git lokal mit GitHub-noreply-Adresse konfiguriert (private E-Mail bleibt raus). Keine Lizenz gesetzt (Nutzer-Entscheidung offen).
**Dateien:** `.gitignore`, `README.md` (neu), `CLAUDE.md` → §8 Sichtbarkeit
**Befehle:**
    git init -b main
    git config user.name "B4turnatur"
    git config user.email "<ID>+B4turnatur@users.noreply.github.com"
    git add -A && git commit
    gh repo create B4turnatur/VocalSplit --public --source . --remote origin --push
**Ausgabe:** ✅ https://github.com/B4turnatur/VocalSplit PUBLIC main
**Ergebnis:** ✅ Quellcode + Doku online; die portable Version (5 GB) ist nicht im Repo (zu groß für Git, Release-Limit 2 GB je Datei).
**Offen:** Lizenz wählen; ggf. Release mit portable Version (müsste in Teile < 2 GB gesplittet werden).

