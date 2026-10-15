"""VocalSplit – Gesang & Musik trennen, lokal auf der GPU (audio-separator + Gradio)."""
import logging
import re
import time
from datetime import datetime
from pathlib import Path

import gradio as gr
import torch
from audio_separator.separator import Separator

ROOT = Path(__file__).parent
MODELS_DIR = ROOT / "models"
OUTPUT_DIR = ROOT / "output"
AUDIO_SLOTS = 8  # so viele Player zeigt die Oberfläche maximal

# Nachbearbeitung der Gesangsspur: Name -> (Modell, Stem der weiterverwendet wird)
POST_STEPS = {
    "Hall entfernen (De-Reverb)": ("dereverb_mel_band_roformer_anvuew_sdr_19.1729.ckpt", "noreverb"),
    "Rauschen entfernen (Denoise)": ("denoise_mel_band_roformer_aufr33_sdr_27.9959.ckpt", "dry"),
    "Lead / Backing-Vocals trennen (Karaoke)": ("mel_band_roformer_karaoke_becruily.ckpt", "vocals"),
}
STEM_MODELS = {
    "4 Stems – Gesang, Drums, Bass, Rest (htdemucs_ft)": "htdemucs_ft.yaml",
    "6 Stems – + Gitarre, Klavier (htdemucs_6s)": "htdemucs_6s.yaml",
    "Drum-Zerlegung – Kick, Snare, Toms, HiHat … (MDX23C)": "MDX23C-DrumSep-aufr33-jarredou.ckpt",
}
PRECISIONS = ["Autocast FP16 (Tensor-Cores, empfohlen)", "Natives FP16 (schnellste)", "FP32 (exakt, langsam)"]

_info = Separator(info_only=True, log_level=logging.ERROR)
PRESETS = _info.list_ensemble_presets()
MODELS = _info.get_simplified_model_list(filter_sort_by="vocals") | _info.get_simplified_model_list()
MODEL_CHOICES = [(f"{v['Name']}  ·  {v['Type']}  ·  {', '.join(v['Stems'])}", f) for f, v in MODELS.items()]
PRESET_CHOICES = [(f"{p['name']}: {p['description']}", k) for k, p in PRESETS.items()]


def gpu_info():
    if not torch.cuda.is_available():
        return "⚠️ Keine CUDA-GPU gefunden – läuft auf der CPU (sehr langsam)."
    p = torch.cuda.get_device_properties(0)
    return f"🟢 {p.name} · {p.total_memory / 2**30:.0f} GB VRAM · sm_{p.major}{p.minor} · PyTorch {torch.__version__}"


def tidy(files, base):
    """Benennt Ausgaben in '<base>_<Stem>.ext' um (sonst wachsen die Namen pro Schritt über das Windows-Pfadlimit).
    Der Stem ist die letzte '(…)'-Gruppe im Namen, denn audio-separator schreibt '<eingabe>_(<Stem>)_<modell>'."""
    out = []
    for f in map(Path, files):
        stem = re.findall(r"\(([^()]+)\)", f.stem)[-1]
        out.append(str(f.replace(f.with_name(f"{base}_{stem}{f.suffix}"))))
    return out


def pick_stem(files, stem):
    """Ausgabedatei des Stems (nach tidy) – oder None."""
    return next((f for f in files if Path(f).stem.lower().endswith(f"_{stem.lower()}")), None)


def run(files, mode, preset, model, stem_model, post, fmt, precision, compile_, overlap, shifts, progress=gr.Progress()):
    if not files:
        raise gr.Error("Bitte erst eine oder mehrere Audiodateien hochladen.")
    models = {"Preset (Ensemble)": PRESETS.get(preset, {}).get("models"), "Einzelmodell": model,
              "Stems (Instrumente)": STEM_MODELS.get(stem_model)}[mode]
    if not models:
        raise gr.Error("Bitte ein Modell bzw. Preset auswählen.")

    log, results = [gpu_info()], []
    for i, src in enumerate(files):
        src = Path(src)
        out = OUTPUT_DIR / f"{src.stem}_{datetime.now():%Y%m%d-%H%M%S}"
        sep = Separator(
            model_file_dir=str(MODELS_DIR), output_dir=str(out), output_format=fmt, log_level=logging.WARNING,
            use_autocast=precision == PRECISIONS[0], use_native_fp16=precision == PRECISIONS[1],
            use_torch_compile=compile_,
            mdxc_params={"segment_size": 256, "override_model_segment_size": False, "batch_size": 1,
                         "overlap": int(overlap), "pitch_shift": 0},
            demucs_params={"segment_size": "Default", "shifts": int(shifts), "overlap": 0.25, "segments_enabled": True},
        )
        progress((i, len(files)), desc=f"{src.name}: Trennen (Modelle werden beim ersten Mal geladen) …")
        t = time.perf_counter()
        sep.load_model(models)
        outs = tidy([out / Path(f).name for f in sep.separate(str(src))], src.stem)
        log.append(f"✅ {src.name}: getrennt in {time.perf_counter() - t:.1f}s → {out}")

        vocals = pick_stem(outs, "vocals")
        for step in post or []:
            if not vocals:
                log.append(f"⚠️ {step}: keine Gesangsspur gefunden – übersprungen.")
                break
            step_model, keep = POST_STEPS[step]
            progress((i, len(files)), desc=f"{src.name}: {step} …")
            t = time.perf_counter()
            sep.load_model(step_model)
            step_outs = tidy([out / Path(f).name for f in sep.separate(vocals)], Path(vocals).stem)
            outs += step_outs
            vocals = pick_stem(step_outs, keep) or vocals
            log.append(f"✅ {step}: {time.perf_counter() - t:.1f}s")
        results += outs

    if torch.cuda.is_available():
        log.append(f"VRAM-Spitze: {torch.cuda.max_memory_allocated() / 2**30:.1f} GB")
    players = [gr.update(value=f, label=Path(f).stem, visible=True) for f in results[:AUDIO_SLOTS]]
    players += [gr.update(value=None, visible=False)] * (AUDIO_SLOTS - len(players))
    return [results, "\n".join(log), *players]


CSS = """
.gradio-container {max-width: 1200px !important; margin: auto}
#title h1 {font-size: 2.2rem; margin-bottom: 0; background: linear-gradient(90deg,#a78bfa,#22d3ee);
           -webkit-background-clip: text; -webkit-text-fill-color: transparent}
"""

with gr.Blocks(title="VocalSplit") as demo:
    gr.Markdown("# VocalSplit\nGesang und Musik trennen – lokal, mit den besten RoFormer-/Demucs-Modellen.",
                elem_id="title")
    gr.Markdown(gpu_info())
    with gr.Row():
        with gr.Column(scale=5):
            files = gr.File(label="Audiodateien (mehrere möglich)", file_count="multiple", type="filepath",
                            file_types=["audio", "video"])
            mode = gr.Radio(["Preset (Ensemble)", "Einzelmodell", "Stems (Instrumente)"],
                            value="Preset (Ensemble)", label="Modus")
            preset = gr.Dropdown(PRESET_CHOICES, value="vocal_balanced", label="Preset")
            model = gr.Dropdown(MODEL_CHOICES, value="bs_roformer_vocals_resurrection_unwa.ckpt",
                                label="Modell (sortiert nach Gesangs-SDR, tippen zum Suchen)", visible=False)
            stem_model = gr.Dropdown(list(STEM_MODELS), value=list(STEM_MODELS)[0], label="Stem-Modell",
                                     visible=False)
            post = gr.CheckboxGroup(list(POST_STEPS), label="Nachbearbeitung der Gesangsspur (nacheinander)")
            with gr.Accordion("Erweitert", open=False):
                with gr.Row():
                    fmt = gr.Radio(["WAV", "FLAC", "MP3"], value="FLAC", label="Ausgabeformat")
                    precision = gr.Radio(PRECISIONS, value=PRECISIONS[0], label="Rechengenauigkeit")
                with gr.Row():
                    overlap = gr.Slider(2, 16, value=8, step=1,
                                        label="Overlap RoFormer (höher = besser & langsamer)")
                    shifts = gr.Slider(0, 10, value=2, step=1, label="Shifts Demucs (höher = besser & langsamer)")
                compile_ = gr.Checkbox(label="torch.compile (schneller bei vielen Dateien, erster Lauf langsam)")
            go = gr.Button("Trennen", variant="primary", size="lg")
        with gr.Column(scale=6):
            players = [gr.Audio(visible=False, type="filepath", interactive=False) for _ in range(AUDIO_SLOTS)]
            out_files = gr.File(label="Alle Ausgabedateien", file_count="multiple")
            log = gr.Textbox(label="Protokoll", lines=6)

    mode.change(lambda m: [gr.update(visible=m == x) for x in ("Preset (Ensemble)", "Einzelmodell",
                                                                 "Stems (Instrumente)")],
                mode, [preset, model, stem_model])
    go.click(run, [files, mode, preset, model, stem_model, post, fmt, precision, compile_, overlap, shifts],
             [out_files, log, *players])

if __name__ == "__main__":
    demo.queue().launch(inbrowser=True, theme=gr.themes.Soft(primary_hue="violet", neutral_hue="slate"),
                        css=CSS, allowed_paths=[str(OUTPUT_DIR)])
