import tempfile
from pathlib import Path

from app import pick_stem, tidy

d = Path(tempfile.mkdtemp())
raw = ["Song (Live)_(Vocals)_bs_roformer.flac", "Song (Live)_(Instrumental)_bs_roformer.flac"]
for n in raw:
    (d / n).touch()
files = tidy([d / n for n in raw], "Song (Live)")
assert [Path(f).name for f in files] == ["Song (Live)_Vocals.flac", "Song (Live)_Instrumental.flac"]

files = ["a/s_Vocals_reverb.flac", "a/s_Vocals_noreverb.flac", "a/s_Vocals_noreverb_dry.flac", "a/s_Vocals_noreverb_no dry.flac"]
assert pick_stem(files, "noreverb") == files[1]
assert pick_stem(files, "dry") == files[2]
assert pick_stem(files, "drums") is None
print("ok")
