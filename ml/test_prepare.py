import sys, pathlib, tempfile, os
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import numpy as np, soundfile as sf
from prepare_clips import clips
def test_resample_and_clip():
    d = tempfile.mkdtemp(); p = os.path.join(d, "a.wav"); sf.write(p, (np.random.default_rng(0).normal(0, .1, 22050 * 7)).astype("float32"), 22050)
    cs = list(clips(p)); assert len(cs) == 2 and all(len(c) == 48000 for c in cs)       # 7 s -> two 3 s clips at 16 kHz
def test_silence_skipped():
    d = tempfile.mkdtemp(); p = os.path.join(d, "s.wav"); sf.write(p, np.zeros(16000 * 4, "float32"), 16000); assert list(clips(p)) == []
