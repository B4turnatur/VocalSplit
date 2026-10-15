# Bedienungsanleitung

## Installation (einmalig)
**Wofür:** Richtet Python, PyTorch (CUDA 12.8 für RTX 50xx) und alle Pakete im Ordner `.venv` ein.
**Voraussetzungen:** Windows, aktueller NVIDIA-Treiber, `uv` (https://docs.astral.sh/uv/) und `ffmpeg` im PATH (hier: `C:\ffmpeg\bin`).
**So geht's:** 1. Doppelklick auf `install.bat` 2. warten (~3 GB Download).
**Typische Fehler:** `No module named 'audioread'` → F-001 · `cublasLt64_13.dll` fehlt → F-002
**Im Code:** `install.bat`

## VocalSplit starten und benutzen
**Wofür:** Gesang und Musik (oder einzelne Instrumente) aus einem Song trennen – lokal auf der Grafikkarte.
**Voraussetzungen:** Installation erledigt. Beim ersten Benutzen eines Modells wird es nach `models/` geladen (200–900 MB je Modell).
**So geht's:**
1. Doppelklick auf `start.bat` → Browser öffnet `http://localhost:7860` (Konsolenfenster offen lassen).
2. Audiodatei(en) in das Feld ziehen (MP3, WAV, FLAC, M4A … auch Videos; mehrere gleichzeitig möglich).
3. **Modus** wählen:
   - **Preset (Ensemble)** – kombiniert 2–3 Spitzenmodelle. Empfehlungen:
     `Vocal Balanced` (bester Allround-Gesang, Standard), `Vocal Clean` (wenig Instrumenten-Reste im Gesang),
     `Vocal Full` (fängt auch Chöre/Harmonien), `Instrumental Clean/Full/Balanced` (beste Instrumentals),
     `Karaoke` (nur Leadgesang raus, Backing bleibt in der Musik), `Vocal RVC` (Trainingsdaten für KI-Stimmen).
   - **Einzelmodell** – jedes der 169 Modelle; Liste nach Gesangs-Qualität (SDR) sortiert, Tippen filtert.
   - **Stems (Instrumente)** – `htdemucs_ft` (Gesang/Drums/Bass/Rest), `htdemucs_6s` (+ Gitarre, Klavier), Drum-Zerlegung (Kick, Snare, …; am besten mit einer Drum-Spur als Eingabe).
4. Optional **Nachbearbeitung** der Gesangsspur (läuft in dieser Reihenfolge): Hall entfernen → Rauschen entfernen → Lead/Backing trennen.
5. Optional **Erweitert**:
   - Ausgabeformat WAV / FLAC (verlustfrei + kleiner, Standard) / MP3
   - Rechengenauigkeit: *Autocast FP16* (Tensor-Cores, Standard), *Natives FP16* (noch schneller, minimal ungenauer; Demucs/ONNX ignorieren das), *FP32* (langsam, exakt)
   - Overlap RoFormer 2–16 (Standard 8; höher = sauberer, langsamer)
   - Shifts Demucs 0–10 (Standard 2; höher = sauberer, langsamer)
   - torch.compile: lohnt nur bei vielen Dateien hintereinander
6. **Trennen** klicken. Ergebnisse: Player rechts, Downloads unter „Alle Ausgabedateien“, Dateien liegen in `output/<song>_<datum-zeit>/`.
**Dateinamen:** `<song>_Vocals`, `<song>_Instrumental`; nach Nachbearbeitung z. B. `<song>_Vocals_noreverb_dry` (= hallfrei + entrauscht), `…_dry_Vocals` (Lead) / `…_dry_Instrumental` (Backing-Vocals).
**Beispiel:**
    Song.mp3, Preset „Vocal Balanced“, Hall entfernen
    → output/Song_20261015-140000/Song_Vocals.flac, Song_Instrumental.flac, Song_Vocals_noreverb.flac, Song_Vocals_reverb.flac
**Leistung (RTX 5070 Ti):** 20-s-Clip mit Ensemble ~25 s, jede Nachbearbeitung ~3 s, max. ~4 GB VRAM. Erster Lauf eines Modells dauert länger (Download).
**Typische Fehler:** siehe F-001, F-002, F-003
**Im Code:** `app.py` → `run()` (Ablauf), `POST_STEPS`/`STEM_MODELS` (Modellauswahl), `tidy()` (Dateinamen)

## Portable Version bauen und benutzen
**Wofür:** Ein Ordner `dist\VocalSplit`, der auf jedem Windows-PC ohne Installation läuft (z. B. vom USB-Stick/externer SSD).
**Voraussetzungen zum Bauen:** `install.bat` wurde ausgeführt (`.venv` existiert), `uv` und `ffmpeg` im PATH.
**Voraussetzungen auf dem Ziel-PC:** Windows 10/11 x64. Für GPU: NVIDIA-Karte + Treiber ab Version 570 (CUDA 12.8; RTX 20xx–50xx). Ohne NVIDIA läuft es auf der CPU (sehr langsam). Internet nur, wenn Modelle fehlen.
**So geht's:**
1. Im Projektordner `build_portable.bat` doppelklicken (oder mit `models`, siehe unten) → nach ein paar Minuten steht „Fertig: dist\VocalSplit“.
2. Den Ordner `dist\VocalSplit` irgendwohin kopieren.
3. Dort `start.bat` doppelklicken → Browser öffnet http://localhost:7860.
**Aufruf / Optionen:**
    build_portable.bat          # ohne Modelle (~5 GB); Modelle werden beim ersten Benutzen nach VocalSplit\models geladen
    build_portable.bat models   # kopiert alle schon geladenen Modelle aus models\ mit (~+5,5 GB, offline nutzbar)
**Inhalt:** `python\` (eigenes Python 3.12 mit allen Paketen, exakt die Versionen aus `.venv` laut `requirements.txt`), `ffmpeg\` (ffmpeg + ffprobe), `app.py`, `start.bat`, später `models\` und `output\`.
**Beispiel:**
    build_portable.bat
    → Fertig: dist\VocalSplit
**Typische Fehler:** „FEHLER: ffmpeg nicht gefunden/kopiert“ → ffmpeg in den PATH legen (F-005). Pfad mit Sonderzeichen ist ok, `start.bat` wechselt selbst in seinen Ordner.
**Im Code:** `build_portable.bat` (Bau), `portable_start.bat` (wird zu `start.bat` in der portablen Version)

## Selbsttest
**Wofür:** Prüft die Dateinamen-Logik (`tidy`, `pick_stem`) ohne GPU.
**Aufruf:**
    .venv\Scripts\python.exe test_app.py
    → ok
**Im Code:** `test_app.py`
