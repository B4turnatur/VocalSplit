# Fehler-Datenbank

## F-001 – audio-separator startet nicht: „No module named 'audioread'“
**Status:** 🟢 gelöst
**Wann/Wo:** 2026-10-15 · Import `audio_separator.separator` · Windows 11 · audio-separator 0.47.0
**Fehlermeldung:**
    File "...\audio_separator\separator\uvr_lib_v5\spec_utils.py", line 1, in <module>
        import audioread
    ModuleNotFoundError: No module named 'audioread'
**Nachstellen:** 1. `uv pip install "audio-separator[gpu]"` 2. `from audio_separator.separator import Separator`
**Ursache:** Abhängigkeit fehlt in den Paket-Metadaten von audio-separator 0.47.0.
**Versuche:**
1. `uv pip install audioread` → ✅
**Lösung:** `audioread` mitinstallieren (steht jetzt in `install.bat`).
**Vorbeugen:** Bei Neuinstallation immer `install.bat` benutzen.

## F-002 – ONNX-Modelle laufen nicht auf der GPU: „cublasLt64_13.dll“ fehlt
**Status:** 🟢 gelöst
**Wann/Wo:** 2026-10-15 · Separator-Start · Windows 11 · onnxruntime-gpu 1.31.0, PyTorch 2.11.0+cu128
**Fehlermeldung:**
    WARNING: The installed PyTorch 2.11.0+cu128 uses CUDA 12.x, but onnxruntime-gpu is built with CUDA 13.x. Please install PyTorch for CUDA 13.x to be compatible.
    Failed to load cublasLt64_13.dll: Could not find module 'cublasLt64_13.dll' (or one of its dependencies). Try using the full path with constructor syntax.
    Failed to load cublas64_13.dll: ... (gekürzt)
    Failed to load cudart64_13.dll: ... (gekürzt)
**Nachstellen:** 1. audio-separator[gpu] installiert neuestes onnxruntime-gpu (1.31, CUDA 13) 2. App starten.
**Ursache:** onnxruntime-gpu 1.31 ist für CUDA 13 gebaut, PyTorch cu128 bringt CUDA-12-DLLs mit. Betrifft nur .onnx-Modelle (MDX-Net); RoFormer/Demucs (PyTorch) liefen trotzdem auf der GPU.
**Versuche:**
1. `uv pip install "onnxruntime-gpu<1.24"` → ✅ 1.23.2, Provider = CUDAExecutionProvider, keine Warnung
**Lösung:** onnxruntime-gpu auf <1.24 pinnen (in `install.bat`).
**Vorbeugen:** Erst bei Umstieg auf PyTorch für CUDA 13 den Pin entfernen.

## F-003 – Ausgabedateinamen werden bei Nachbearbeitung extrem lang (Windows-Pfadlimit)
**Status:** 🟢 gelöst
**Wann/Wo:** 2026-10-15 · `app.py` → `run()` · Windows 11
**Fehlermeldung:** keine – Name z. B. `test_(Vocals)_custom_ensemble_vocals_resur_big_beta6x_(noreverb)_dereverb_mel_band_roformer_anvuew_sdr_19_(dry)_denoise_..._(Vocals)_mel_band_roformer_karaoke_becruily.flac` (~280 Zeichen Pfad, über MAX_PATH 260)
**Nachstellen:** Preset + alle 3 Nachbearbeitungen wählen.
**Ursache:** audio-separator hängt pro Schritt `_(<Stem>)_<modell>` an den Eingabenamen.
**Versuche:**
1. `tidy()` benennt nach jedem Schritt in `<eingabe>_<Stem>.ext` um (Stem = letzte `(…)`-Gruppe) → ✅
**Lösung:** `app.py` → `tidy()`; `pick_stem()` sucht jetzt nach Endung `_<stem>`.
**Vorbeugen:** Abgedeckt durch `test_app.py`.

## F-004 – Mehrzeiliges Bash-Skript mit Heredocs bricht ab: „unexpected EOF while looking for matching `''“
**Status:** 🟡 Workaround
**Wann/Wo:** 2026-10-15 · Claude-Bash-Tool (Git Bash) beim Schreiben der Doku
**Fehlermeldung:**
    /usr/bin/bash: -c: line 87: unexpected EOF while looking for matching `''
**Nachstellen:** Mehrere `cat >> datei <<'EOF'`-Blöcke mit Backticks/Anführungszeichen plus Python-Heredoc in einem Aufruf.
**Ursache:** unklar, Vermutung: Quoting-Problem beim Weiterreichen des langen Befehls. Es wurde nichts geschrieben.
**Lösung:** Doku-Dateien mit den Write/Edit-Werkzeugen schreiben statt per Shell.
**Vorbeugen:** Keine langen Heredoc-Ketten für Doku verwenden.

## F-005 – Portable Version: ffmpeg wird nicht mitkopiert → „[WinError 2] Das System kann die angegebene Datei nicht finden“
**Status:** 🟢 gelöst
**Wann/Wo:** 2026-10-15 · `build_portable.bat` Schritt 3 · Windows 11
**Fehlermeldung:**
    File "...\dist\VocalSplit\python\Lib\site-packages\audio_separator\separator\separator.py", line 405, in check_ffmpeg_installed
        ffmpeg_version_output = subprocess.check_output(["ffmpeg", "-version"], text=True)
    ... (gekürzt)
    FileNotFoundError: [WinError 2] Das System kann die angegebene Datei nicht finden
**Nachstellen:** portable Version starten auf einem PC ohne ffmpeg im PATH; Ordner `dist\VocalSplit\ffmpeg` war leer.
**Ursache:** In `for /f ... %%f ... "%%~dpfffmpeg.exe"` liest cmd `f` als Modifier (`~dpfff…`), der Pfad stimmt dann nicht. Copy schlug still fehl.
**Versuche:**
1. Schleifenvariable auf `%%G` geändert + Prüfung `if not exist ffmpeg.exe → FEHLER` → ✅
**Lösung:** `build_portable.bat` → Variable `%%G`, Abbruch mit Meldung wenn ffmpeg fehlt.
**Vorbeugen:** In Batch nie d/p/f/n/x/s/a/t/z als `for`-Variable nehmen, wenn `%%~…`-Modifier benutzt werden.
