# VocalSplit

Gesang, Musik und einzelne Instrumente aus Songs trennen – lokal auf der eigenen NVIDIA-GPU, mit den aktuell besten Open-Source-Modellen (BS-/Mel-RoFormer, Demucs v4). Optimiert für RTX 50xx (Blackwell, CUDA 12.8), läuft auch auf älteren RTX-Karten.

Basiert auf [python-audio-separator](https://github.com/nomadkaraoke/python-audio-separator) und [Gradio](https://gradio.app).

## Funktionen
- **Ensemble-Presets** – 2–3 Spitzenmodelle kombiniert: Vocal Balanced / Clean / Full, Instrumental Clean / Full / Balanced, Karaoke, Vocal RVC
- **169 Einzelmodelle** – nach Gesangs-Qualität (SDR) sortiert und durchsuchbar
- **Stems** – Gesang/Drums/Bass/Rest (htdemucs_ft), + Gitarre/Klavier (htdemucs_6s), Drum-Zerlegung (Kick, Snare, …)
- **Nachbearbeitung der Gesangsspur** – Hall entfernen → Rauschen entfernen → Lead/Backing-Vocals trennen
- Mehrere Dateien auf einmal, Ausgabe WAV / FLAC / MP3, Player direkt in der Oberfläche
- FP16 auf den Tensor-Cores, optional torch.compile

## Installation (Windows)
Voraussetzungen: aktueller NVIDIA-Treiber (ab 570), [uv](https://docs.astral.sh/uv/), [ffmpeg](https://ffmpeg.org) im PATH.

```bat
install.bat
start.bat
```
Der Browser öffnet http://localhost:7860. Modelle werden beim ersten Benutzen nach `models/` geladen (200–900 MB je Modell).

## Portable Version
```bat
build_portable.bat          :: ohne Modelle
build_portable.bat models   :: inkl. bereits geladener Modelle (offline nutzbar)
```
Ergebnis: `dist\VocalSplit` – Ordner auf einen anderen PC kopieren, `start.bat` doppelklicken, fertig.

## Doku
- [docs/ANLEITUNG.md](docs/ANLEITUNG.md) – Bedienung aller Funktionen
- [docs/FEHLER.md](docs/FEHLER.md) – bekannte Fehler und Lösungen
- [docs/ENTSCHEIDUNGEN.md](docs/ENTSCHEIDUNGEN.md) – Technik-Entscheidungen

## Lizenz
Code: [MIT](LICENSE). Die Modelle haben eigene Lizenzen ihrer jeweiligen Autoren.
