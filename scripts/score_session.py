import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scoring import ScoreConfig, score_csv


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "success": False,
            "error": "Usage: python score_session.py <track_csv> [output_json]"
        }))
        sys.exit(1)

    csv_path = Path(sys.argv[1])

    if not csv_path.exists():
        print(json.dumps({
            "success": False,
            "error": f"CSV not found: {csv_path}"
        }))
        sys.exit(1)

    if len(sys.argv) >= 3:
        out_json = Path(sys.argv[2])
    else:
        out_json = csv_path.with_name(csv_path.name.replace("_track.csv", "_score.json"))

    cfg = ScoreConfig()
    report = score_csv(str(csv_path), cfg)

    out_json.parent.mkdir(parents=True, exist_ok=True)
    with open(out_json, "w") as f:
        json.dump(report, f, indent=2)

    print(json.dumps(report))


if __name__ == "__main__":
    main()