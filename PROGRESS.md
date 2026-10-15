# Projekt: VocalSplit (BackgroundMusic remover)

## Ziel
Lokales Programm, das Gesang und Musik (und Instrumente) mit den besten KI-Modellen trennt – optimiert für RTX 5070 Ti, moderne Weboberfläche.

## Aktueller Stand
- `app.py` fertig: Gradio-UI, 3 Modi (Ensemble-Presets, 169 Einzelmodelle, Demucs-Stems), Nachbearbeitungskette (De-Reverb, Denoise, Karaoke), Batch, WAV/FLAC/MP3, FP16-Autocast auf Tensor-Cores
- Auf der GPU getestet (synthetisches Testsignal), alle Modi laufen
- Portable Version: `build_portable.bat` → `dist\VocalSplit` (eigenes Python + ffmpeg, ohne Installation), isoliert getestet
- **Benutzbare Version liegt auf dem Desktop: `Desktop\VocalSplit\start.bat`** (portable + alle bisher geladenen Modelle, ~12 GB)
- Projektordner aufgeräumt: `.venv`, `models`, `dist`, `output` gelöscht → zum Weiterentwickeln erst `install.bat` ausführen
- Öffentlich auf GitHub: https://github.com/B4turnatur/VocalSplit (ohne .venv/models/dist)

## Nächste Schritte
1. Nutzer testet mit echten Songs, Feedback einarbeiten
2. Portable Version auf einem zweiten PC ausprobieren

## Offene Fehler (Details in docs/FEHLER.md)
- keine

## Wichtige Dateien
- `app.py` – ganze App (UI + Ablauf)
- `start.bat` / `install.bat` – starten / einmalig installieren
- `test_app.py` – Selbsttest Dateinamen-Logik
- `build_portable.bat` / `portable_start.bat` – portable Version bauen / deren Starter
- `models/` – heruntergeladene Modelle (Cache) · `output/` – Ergebnisse

## Testen
- `.venv\Scripts\python.exe test_app.py` → `ok`
- `start.bat` → Browser auf http://localhost:7860, Song hochladen, Trennen

## Changelog (neueste oben, max. 15 Zeilen – Details in docs/LOG.md)
- 2026-10-15 – Portable Version auf Desktop, Projektordner aufgeräumt – siehe LOG.md
- 2026-10-15 – MIT-Lizenz – LICENSE, README.md – siehe LOG.md
- 2026-10-15 – GitHub-Repo B4turnatur/VocalSplit (öffentlich) – .gitignore, README.md – siehe LOG.md
- 2026-10-15 – Portable Version – build_portable.bat, portable_start.bat – siehe LOG.md
- 2026-10-15 – App gebaut + auf GPU getestet – app.py, test_app.py, start.bat, install.bat – siehe LOG.md
