import pandas as pd

REQUIRED = ["frame", "time_s", "cx", "cy", "conf"]

def load_track_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns {missing}. Found: {list(df.columns)}")
    df = df.sort_values("frame").reset_index(drop=True)
    return df