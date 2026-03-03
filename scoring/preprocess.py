import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
from .config import ScoreConfig

def _interp_small_gaps(series: pd.Series, max_gap: int) -> pd.Series:
    # interpolate linearly, but only for small NaN runs
    s = series.copy()
    is_nan = s.isna().values
    if not is_nan.any():
        return s

    idx = np.arange(len(s))
    # fill all by interpolation first
    s = s.interpolate(limit_direction="both")

    # now revert long gaps back to NaN
    run_start = None
    for i, nan in enumerate(is_nan.tolist() + [False]):
        if nan and run_start is None:
            run_start = i
        if (not nan) and run_start is not None:
            run_len = i - run_start
            if run_len > max_gap:
                s.iloc[run_start:i] = np.nan
            run_start = None

    return s

def preprocess(df: pd.DataFrame, cfg: ScoreConfig) -> pd.DataFrame:
    out = df.copy()

    # mark low confidence as missing
    low = out["conf"] < cfg.min_conf
    out.loc[low, ["cx", "cy"]] = np.nan

    # interpolate small gaps only
    out["cx"] = _interp_small_gaps(out["cx"], cfg.max_gap_frames_to_interp)
    out["cy"] = _interp_small_gaps(out["cy"], cfg.max_gap_frames_to_interp)

    # drop remaining NaNs (long gaps) for scoring
    out = out.dropna(subset=["cx", "cy"]).reset_index(drop=True)

    # smoothing
    w = cfg.sg_window
    if w % 2 == 0:
        w += 1
    if len(out) >= w:
        out["cx_s"] = savgol_filter(out["cx"].to_numpy(), w, cfg.sg_poly)
        out["cy_s"] = savgol_filter(out["cy"].to_numpy(), w, cfg.sg_poly)
    else:
        out["cx_s"] = out["cx"]
        out["cy_s"] = out["cy"]

    return out