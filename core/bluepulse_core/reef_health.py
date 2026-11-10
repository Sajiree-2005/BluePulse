"""Site-relative soundscape activity: robust per-hour baselines (median/MAD) and a transparent 0-100 score."""
import numpy as np
from collections import defaultdict

def fit_baseline(records):
    """records: iterable of (hour 0-23, value). Returns {hour: (median, mad)}."""
    by = defaultdict(list)
    for h, v in records: by[int(h)].append(float(v))
    return {h: (float(np.median(v)), float(np.median(np.abs(np.array(v) - np.median(v))))) for h, v in by.items()}

def zscore(value, baseline, hour):
    med, mad = baseline.get(int(hour), (value, 1.0))
    return float(0.6745 * (value - med) / (mad + 1e-9))

def activity_score(zs):
    """100 = typical for this site/hour. Drops in biological activity cost 3x more than rises. NOT a health diagnosis."""
    z = np.asarray(zs, float)
    return float(np.clip(100 - 12*np.mean(np.maximum(0, -z)) - 4*np.mean(np.maximum(0, z)), 0, 100))
