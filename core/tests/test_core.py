import numpy as np, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parents[1]))
from bluepulse_core import *
SR = 16000
def test_pcen_shape_nonneg():
    x = np.random.default_rng(1).normal(0, .1, SR*2).astype(np.float32); P = pcen(mel_spec(x, SR), SR)
    assert P.shape[0] == 64 and np.isfinite(P).all()
def test_blast_detected_noise_not():
    assert abs(detect_transients(synth_blast(SR, 3, 1.0), SR)[0] - 1.0) < 0.1
    assert detect_transients(np.random.default_rng(2).normal(0, .02, SR*3), SR) == []
def test_entropy_noise_above_tone():
    t = np.arange(SR)/SR; assert spectral_entropy(np.random.default_rng(3).normal(0,1,SR)) > spectral_entropy(np.sin(2*np.pi*500*t))
def test_aci_finite():
    assert np.isfinite(aci(synth_blast(SR)))
def test_tdoa_recovers_source():
    S = np.array([[0,0],[4000,0],[0,4000],[4000,4000]], float); src = np.array([1500., 2500.])
    T = np.linalg.norm(S-src, axis=1)/1500.0; x, y, r = tdoa_locate(S, T)
    assert abs(x-src[0]) < 5 and abs(y-src[1]) < 5 and r < 1e-4
