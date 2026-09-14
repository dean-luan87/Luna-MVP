import argparse
import json
import sys
import time
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.append(str(_ROOT))

from runtime.main_loop import MainLoop
from luna_badge_v1_2.governance.output_controller.controller import ModelOutputController


def _unwrap_fixture(fixture: dict) -> dict:
    snapshot = fixture["system_snapshot"]
    return {
        "ts": snapshot.get("ts", 0.0),
        "frame_id": snapshot.get("frame_id"),
        "context_mode": snapshot.get("context_mode"),
        "self": snapshot.get("self_state", {}),
        "objects": snapshot.get("perceived_objects", []),
        "restricted_zones": snapshot.get("environment", {}).get("restricted_zones", []),
        "perception_state": snapshot.get("system_facts", {}).get("perception_state"),
        "calibration_state": snapshot.get("system_facts", {}).get("calibration_state"),
        "hardware_state": snapshot.get("system_facts", {}).get("hardware_state"),
        "gate": snapshot.get("system_facts", {}).get("gate"),
        "control_distortion": snapshot.get("system_facts", {}).get("control_distortion", "FALSE"),
    }


def _run_empty_fixture(fixture: dict, out_path: Path) -> None:
    run_seconds = fixture.get("run_seconds", 60)
    loop = MainLoop(str(out_path))
    loop.run_for_seconds(run_seconds)


def _run_governance_fixtures(
    fixture_files: list,
    out_path: Path,
    include_debug_view: bool,
) -> None:
    with out_path.open("w", encoding="utf-8") as f:
        for fixture_path in fixture_files:
            with fixture_path.open("r", encoding="utf-8") as fh:
                fixture = json.load(fh)

            controller = ModelOutputController()
            result = controller.process(
                task_domain="NAVIGATION",
                model_outputs=fixture["model_outputs"]["candidate_actions"],
                system_snapshot=_unwrap_fixture(fixture),
            )
            bc_snapshot = result.get("decision_trace", {}).get("bc_snapshot", {})
            filtered_bc_snapshot = {
                "authority": bc_snapshot.get("authority"),
                "risk": bc_snapshot.get("risk"),
                "envelope": bc_snapshot.get("envelope"),
                "distortion": bc_snapshot.get("distortion"),
                "gate": bc_snapshot.get("gate"),
                "c_decision": bc_snapshot.get("c_decision"),
                "bc_action": bc_snapshot.get("bc_action"),
            }
            if include_debug_view:
                filtered_bc_snapshot["debug_view"] = bc_snapshot.get("debug_view")
            record = {
                "fixture_id": fixture.get("meta", {}).get("fixture_id"),
                "decision_trace": {"bc_snapshot": filtered_bc_snapshot},
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", required=True, help="fixtures directory or file")
    parser.add_argument("--out", required=True, help="output jsonl")
    parser.add_argument(
        "--enable-debug-view",
        action="store_true",
        help="include debug_view in bc_snapshot output",
    )
    args = parser.parse_args()

    fixtures_path = Path(args.fixtures)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if fixtures_path.is_file():
        fixture_files = [fixtures_path]
    else:
        fixture_files = sorted(fixtures_path.glob("*.json"))

    if not fixture_files:
        raise ValueError("no fixtures found")

    with fixture_files[0].open("r", encoding="utf-8") as fh:
        first_fixture = json.load(fh)

    if "run_seconds" in first_fixture and "system_snapshot" not in first_fixture:
        _run_empty_fixture(first_fixture, out_path)
        return

    _run_governance_fixtures(fixture_files, out_path, args.enable_debug_view)


if __name__ == "__main__":
    main()
