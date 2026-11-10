"""numpy/scipy-only signal tools shared by training, edge and backend (no torch, no librosa)."""
import numpy as np
from scipy.signal import lfilter, lfilter_zi
from scipy.optimize import least_squares

def stft_power(x, n_fft=512, hop=160):
    w = np.hanning(n_fft); n = 1 + max(0, (len(x) - n_fft) // hop)
    fr = np.stack([x[i*hop:i*hop+n_fft] * w for i in range(n)])
    return (np.abs(np.fft.rfft(fr, axis=1)) ** 2).T  # (freq, time)

def mel_filterbank(sr, n_fft=512, n_mels=64, fmin=20.0, fmax=None):
    fmax = fmax or sr / 2; m = lambda f: 2595*np.log10(1+f/700); inv = lambda v: 700*(10**(v/2595)-1)
    pts = inv(np.linspace(m(fmin), m(fmax), n_mels+2)); bins = np.floor((n_fft+1)*pts/sr).astype(int)
    fb = np.zeros((n_mels, n_fft//2+1))
    for i in range(n_mels):
        a, b, c = bins[i], bins[i+1], bins[i+2]
        for k in range(a, b): fb[i, k] = (k-a)/max(1, b-a)
        for k in range(b, c): fb[i, k] = (c-k)/max(1, c-b)
    return fb

def mel_spec(x, sr, n_fft=512, hop=160, n_mels=64):
    return mel_filterbank(sr, n_fft, n_mels) @ stft_power(x, n_fft, hop)

def pcen(S, sr, hop=160, gain=0.98, bias=2.0, power=0.5, time_const=0.4, eps=1e-6):
    """Per-channel energy normalisation: IIR smoother + adaptive gain + root compression."""
    s = 1 - np.exp(-hop / (sr * time_const)); M = lfilter([s], [1, s-1], S, axis=1, zi=None)
    return (S / (eps + M) ** gain + bias) ** power - bias ** power

def detect_transients(x, sr, win_ms=10, ratio=8.0, refractory_s=1.0):
    """Tier-0 detector: short-time energy vs slow background. Returns event onset times (s)."""
    n = max(1, int(sr*win_ms/1000)); e = np.convolve(x**2, np.ones(n)/n, mode="same")[::n]
    zi = lfilter_zi([0.01], [1, -0.99]) * np.median(e); bg, _ = lfilter([0.01], [1, -0.99], e, zi=zi); hits, last = [], -1e9
    for i in range(len(e)):
        t = i*n/sr
        if e[i] > ratio*(bg[i]+1e-12) and e[i] > 1e-6 and t-last > refractory_s: hits.append(t); last = t
    return hits

def spectral_entropy(x, n_fft=512):
    p = stft_power(x, n_fft).mean(axis=1); p = p/(p.sum()+1e-12)
    return float(-(p*np.log2(p+1e-12)).sum()/np.log2(len(p)))

def aci(x, n_fft=512, hop=160):
    S = np.sqrt(stft_power(x, n_fft, hop)); d = np.abs(np.diff(S, axis=1)).sum(axis=1)
    return float((d/(S.sum(axis=1)+1e-12)).sum())

def synth_blast(sr=16000, dur=3.0, onset=1.0, rng=None, bubble_hz=9.0, snr_db=15):
    """Synthetic blast for augmentation: shock pulse + decaying bubble oscillation on ambient noise."""
    rng = rng or np.random.default_rng(0); n = int(sr*dur); t = np.arange(n)/sr
    noise = rng.normal(0, 0.02, n); y = np.zeros(n); k = int(onset*sr); tt = t[:n-k]
    y[k:] = (np.exp(-tt/0.03)*rng.normal(0,1,n-k) + 0.6*np.exp(-tt/0.5)*np.sin(2*np.pi*bubble_hz*tt)*np.sin(2*np.pi*80*tt))
    y *= 0.02*10**(snr_db/20)/(np.abs(y).max()+1e-12)*3
    return (noise+y).astype(np.float32)

def tdoa_locate(sensors, times, c=1500.0):
    """sensors: (N,2) metres, times: (N,) arrival seconds, N>=3. Returns (x,y, rms_residual_s)."""
    S = np.asarray(sensors, float); T = np.asarray(times, float)
    def res(p): d = np.linalg.norm(S-p[:2], axis=1)/c; return (d-d[0])-(T-T[0]) + 0*p[2]
    x0 = np.r_[S.mean(axis=0), 0.0]; r = least_squares(lambda p: res(p), x0)
    return float(r.x[0]), float(r.x[1]), float(np.sqrt(np.mean(r.fun**2)))
