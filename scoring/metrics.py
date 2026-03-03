import numpy as np
import pandas as pd
from .config import ScoreConfig

def compute_metrics(df: pd.DataFrame, cfg: ScoreConfig) -> dict:
    x = df["cx_s"].to_numpy()
    y = df["cy_s"].to_numpy()
    t = df["time_s"].to_numpy()

    dt = np.diff(t)
    dx = np.diff(x)
    dy = np.diff(y)

    # guard
    if len(dt) < 5 or np.any(dt <= 0):
        raise ValueError("Bad or insufficient timestamps for derivatives.")

    # velocities (px/s)
    vx = dx / dt
    vy = dy / dt

    # accelerations (px/s^2)
    ax = np.diff(vx) / dt[1:]
    ay = np.diff(vy) / dt[1:]

    # jerks (px/s^3) - optional but useful
    jx = np.diff(ax) / dt[2:] if len(ax) > 2 else np.array([])
    jy = np.diff(ay) / dt[2:] if len(ay) > 2 else np.array([])

    total_time = t[-1] - t[0]

    # --- reversal detection on vx with deadband and minimum spacing ---
    vx_mid_t = t[1:]  # vx aligns with diff between frames
    vx_f = vx.copy()
    vx_f[np.abs(vx_f) < cfg.vx_deadband_px_s] = 0.0
    sgn = np.sign(vx_f)

    # indices where sign changes and both sides nonzero
    candidates = np.where((sgn[1:] * sgn[:-1]) < 0)[0] + 1  # index in vx array

    # enforce min separation in time
    rev_times = []
    last_t = -1e9
    for idx in candidates:
        ti = vx_mid_t[idx]
        if ti - last_t >= cfg.min_reversal_separation_s:
            rev_times.append(ti)
            last_t = ti

    rev_times = np.array(rev_times)
    reversals_per_sec = (len(rev_times) / total_time) if total_time > 0 else 0.0

    # rhythm consistency from reversal intervals
    if len(rev_times) >= 3:
        intervals = np.diff(rev_times)
        rhythm_cv = float(np.std(intervals) / (np.mean(intervals) + 1e-9))  # lower is better
        median_interval = float(np.median(intervals))
    else:
        rhythm_cv = float("inf")
        median_interval = float("nan")

    # tightness (control radius)
    x_std = float(np.std(x))
    y_std = float(np.std(y))

    # speed stats (focus on lateral)
    abs_vx = np.abs(vx)
    vmean = float(np.mean(abs_vx))
    v90 = float(np.percentile(abs_vx, 90))
    vmax = float(np.max(abs_vx))

    # ---- NEW: Amplitude + Hand Speed Index (stationary stickhandling) ----
    # Robust amplitude (ignores outliers)
    x_p5 = float(np.percentile(x, 5))
    x_p95 = float(np.percentile(x, 95))
    amp_x = (x_p95 - x_p5) / 2.0  # pixels

    # Hand Speed Index: amplitude * tempo
    hsi = amp_x * float(reversals_per_sec)

    # smoothness (lower is better): use mean abs accel + spike rate
    abs_ax = np.abs(ax)
    a_mean = float(np.mean(abs_ax))
    a95 = float(np.percentile(abs_ax, 95))

    # jerk summary (optional)
    j_mean = float(np.mean(np.abs(jx))) if len(jx) else float("nan")

    # confidence stability
    conf_mean = float(df["conf"].mean())
    conf_good_frac = float((df["conf"] >= 0.75).mean())

    return {
        "duration_s": float(total_time),

        "vmean_abs_vx": vmean,
        "v90_abs_vx": v90,
        "vmax_abs_vx": vmax,

        # tempo / rhythm
        "reversals_per_sec": float(reversals_per_sec),
        "rhythm_cv": float(rhythm_cv),
        "median_reversal_interval_s": float(median_interval),

        # speed metrics
        "amp_x": float(amp_x),
        "hsi": float(hsi),

        # control / smoothness
        "a_mean_abs_ax": a_mean,
        "a95_abs_ax": a95,
        "j_mean_abs_jx": j_mean,

        # tightness
        "x_std": x_std,
        "y_std": y_std,

        # model stability
        "conf_mean": conf_mean,
        "conf_good_frac": conf_good_frac,

        "n_points": int(len(df)),
    }