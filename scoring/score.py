import math
import numpy as np   
from .config import ScoreConfig

def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))

def _band_score(x: float, lo: float, hi: float) -> float:
    if lo <= x <= hi:
        return 1.0
    w = hi - lo
    if x < lo:
        return _clamp01(1.0 - (lo - x) / w)
    return _clamp01(1.0 - (x - hi) / w)

def _lower_better(x: float, good: float, bad: float) -> float:
    if math.isnan(x) or math.isinf(x):
        return 0.0
    if x <= good:
        return 1.0
    if x >= bad:
        return 0.0
    return 1.0 - (x - good) / (bad - good)

def _higher_better(x: float, bad: float, good: float) -> float:
    if x <= bad:
        return 0.0
    if x >= good:
        return 1.0
    return (x - bad) / (good - bad)

def score_metrics(m: dict, cfg: ScoreConfig) -> dict:
    # 1) speed
    speed_s = _higher_better(m["hsi"], bad=60.0, good=160.0)

    # penalize if amplitude is tiny (just tapping) or huge (flinging)
    amp_s = _band_score(m["amp_x"], lo=40.0, hi=160.0)
    speed_s = 0.75 * speed_s + 0.25 * amp_s

    # 2) reversals/sec
    rev_s = _band_score(m["reversals_per_sec"], lo=1.5, hi=4.5)

    # 3) smoothness (log scaled)
    a95 = m["a95_abs_ax"]
    a95_log = np.log1p(a95)
    good = np.log1p(9000.0)
    bad = np.log1p(45000.0)
    smooth_s = _lower_better(a95_log, good=good, bad=bad)

    # 4) tightness
    tight_y = _lower_better(m["y_std"], good=10.0, bad=45.0)
    tight_x = _band_score(m["x_std"], lo=20.0, hi=120.0)
    tight_s = 0.6 * tight_y + 0.4 * tight_x

    # 5) rhythm
    rhythm_s = _lower_better(m["rhythm_cv"], good=0.30, bad=1.25)

    # error confidence 
    conf_s = _band_score(m["conf_good_frac"], lo=0.70, hi=1.00)

    # weighted total
    total = (
        cfg.w_speed * speed_s +
        cfg.w_reversals * rev_s +
        cfg.w_smoothness * smooth_s +
        cfg.w_tightness * tight_s +
        cfg.w_rhythm * rhythm_s
    )

    # small confidence influence (±1 max)
    total = total + (conf_s - 0.5) * 2.0
    total = max(0.0, min(100.0, total))

    return {
        "subscores": {
            "speed": round(cfg.w_speed * speed_s, 2),
            "reversals": round(cfg.w_reversals * rev_s, 2),
            "smoothness": round(float(cfg.w_smoothness * smooth_s), 2),
            "tightness": round(cfg.w_tightness * tight_s, 2),
            "rhythm": round(cfg.w_rhythm * rhythm_s, 2),
            "confidence_adj": round((conf_s - 0.5) * 2.0, 2),
        },
        "total": round(total, 2),
    }