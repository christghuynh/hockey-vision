from .config import ScoreConfig
from .io import load_track_csv
from .preprocess import preprocess
from .metrics import compute_metrics
from .score import score_metrics

def score_csv(path: str, cfg: ScoreConfig | None = None) -> dict:
    cfg = cfg or ScoreConfig()
    raw = load_track_csv(path)
    clean = preprocess(raw, cfg)
    metrics = compute_metrics(clean, cfg)
    score = score_metrics(metrics, cfg)

    return {
        "input_csv": path,
        "config": cfg.__dict__,
        "metrics": metrics,
        "score": score,
    }