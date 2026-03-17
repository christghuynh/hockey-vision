import sys
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scoring import ScoreConfig, score_csv


def sanitize_for_json(obj):
    if isinstance(obj, dict):
        return {k: sanitize_for_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [sanitize_for_json(v) for v in obj]
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
    return obj


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
    report = sanitize_for_json(report)

    out_json.parent.mkdir(parents=True, exist_ok=True)
    with open(out_json, "w") as f:
        json.dump(report, f, indent=2)

    print(json.dumps(report))


if __name__ == "__main__":
    main()