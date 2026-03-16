import sys
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SCRIPTS = ROOT / "scripts"
OUTPUTS = ROOT / "outputs"


def run_script(script, args):
    command = [sys.executable, str(script)] + args

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        cwd=ROOT
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return result.stdout.strip()


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "error": "No video path provided"}))
        sys.exit(1)

    video_path = sys.argv[1]
    video_name = Path(video_path).stem

    prediction_video = OUTPUTS / f"{video_name}_pred.mp4"
    csv_path = OUTPUTS / f"{video_name}_track.csv"
    score_json = OUTPUTS / f"{video_name}_score.json"

    try:
        # run YOLO inference
        run_script(
            SCRIPTS / "run_inference.py",
            [
                video_path,
                str(prediction_video)
            ]
        )

        # export puck trajectory CSV
        run_script(
            SCRIPTS / "export_track_csv.py",
            [
                str(prediction_video),
                str(csv_path)
            ]
        )

        # score the session
        score_output = run_script(
            SCRIPTS / "score_session.py",
            [
                str(csv_path),
                str(score_json)
            ]
        )

        score = json.loads(score_output)

        final = {
            "success": True,
            "session_id": video_name,
            "score": score["score"],
            "report": score,
            "artifacts": {
                "prediction_video": f"/outputs/{video_name}_pred.mp4",
                "track_csv": f"/outputs/{video_name}_track.csv",
                "score_json": f"/outputs/{video_name}_score.json"
            }
        }

        print(json.dumps(final))

    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": str(e)
        }))
        sys.exit(1)


if __name__ == "__main__":
    main()