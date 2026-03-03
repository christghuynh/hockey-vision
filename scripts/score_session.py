import sys
import json
from pathlib import Path

from scoring import ScoreConfig, score_csv

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m scripts.score_session outputs/<name>_track.csv")
        sys.exit(1)

    csv_path = Path(sys.argv[1])

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    cfg = ScoreConfig()
    report = score_csv(str(csv_path), cfg)

    print("\nPUCKHANDLING SCORE REPORT")
    print("Total:", report["score"]["total"])
    print("Breakdown:", report["score"]["subscores"])

    # save score report as JSON
    out_json = csv_path.with_name(csv_path.name.replace("_track.csv", "_score.json"))
    with open(out_json, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\nSaved -> {out_json}")

if __name__ == "__main__":
    main()