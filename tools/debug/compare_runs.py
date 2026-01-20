import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.append(str(_ROOT))

from luna_badge_v1_2.governance.output_controller.debug_diff_schema import (
    SCHEMA_VERSION,
    REQUIRED_FIELDS,
    FORBIDDEN_FIELDS,
)


def load_snapshots(path: str) -> List[Dict[str, Any]]:
    snapshots = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            bc_snapshot = record.get("decision_trace", {}).get("bc_snapshot")
            if bc_snapshot:
                snapshots.append(bc_snapshot)
    return snapshots


def _extract_debug_view(snaps: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not snaps:
        return {}
    last = snaps[-1]
    return last.get("debug_view", {})


def _flatten_paths(data: Any, prefix: str = "") -> Dict[str, Any]:
    paths: Dict[str, Any] = {}
    if isinstance(data, dict):
        for key in sorted(data.keys()):
            next_prefix = f"{prefix}.{key}" if prefix else key
            paths.update(_flatten_paths(data[key], next_prefix))
    elif isinstance(data, list):
        for idx, value in enumerate(data):
            next_prefix = f"{prefix}[{idx}]"
            paths.update(_flatten_paths(value, next_prefix))
    else:
        paths[prefix] = data
    return paths


def build_diff_report(
    baseline_snapshots: List[Dict[str, Any]],
    candidate_snapshots: List[Dict[str, Any]],
    baseline_commit: str,
    candidate_commit: str,
) -> Dict[str, Any]:
    baseline_view = _extract_debug_view(baseline_snapshots)
    candidate_view = _extract_debug_view(candidate_snapshots)

    baseline_paths = _flatten_paths(baseline_view)
    candidate_paths = _flatten_paths(candidate_view)

    added_fields = sorted(set(candidate_paths.keys()) - set(baseline_paths.keys()))
    removed_fields = sorted(set(baseline_paths.keys()) - set(candidate_paths.keys()))

    changed_fields = []
    for key in sorted(set(baseline_paths.keys()) & set(candidate_paths.keys())):
        if baseline_paths[key] != candidate_paths[key]:
            changed_fields.append(
                {
                    "field": key,
                    "baseline": baseline_paths[key],
                    "candidate": candidate_paths[key],
                }
            )

    report = {
        "schema_version": SCHEMA_VERSION,
        "added_fields": added_fields,
        "removed_fields": removed_fields,
        "changed_fields": changed_fields,
        "meta": {
            "baseline_commit": baseline_commit,
            "candidate_commit": candidate_commit,
        },
    }
    return report


def summarize_authority_changes(snaps: List[Dict[str, Any]]) -> List[str]:
    changes = []
    last = None
    for snap in snaps:
        eff = snap.get("authority", {}).get("effective")
        if eff != last:
            changes.append(f"{last} -> {eff}")
            last = eff
    return changes


def summarize_risk_levels(snaps: List[Dict[str, Any]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for snap in snaps:
        level = snap.get("risk", {}).get("level", "NONE")
        counts[level] = counts.get(level, 0) + 1
    return counts


def summarize_distortion(snaps: List[Dict[str, Any]]) -> int:
    count = 0
    for snap in snaps:
        distorted = snap.get("distortion", {}).get("distorted", False)
        if distorted:
            count += 1
    return count


def _exit_code(report: Dict[str, Any]) -> int:
    if report.get("schema_version") != SCHEMA_VERSION:
        return 4
    removed_fields = report.get("removed_fields", [])
    if removed_fields:
        return 3
    added_fields = report.get("added_fields", [])
    if added_fields:
        return 2
    return 0


def _validate_report(report: Dict[str, Any]) -> None:
    missing = [field for field in REQUIRED_FIELDS if field not in report]
    assert not missing, "[DEBUGDIFF] missing required fields"
    assert FORBIDDEN_FIELDS.isdisjoint(report.keys()), "[DEBUGDIFF] forbidden fields present"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", required=True, help="jsonl file of baseline run")
    parser.add_argument("--candidate", required=True, help="jsonl file of candidate run")
    parser.add_argument("--out", required=True, help="output diff_report.json")
    parser.add_argument("--baseline-commit", default="", help="baseline commit sha")
    parser.add_argument("--candidate-commit", default="", help="candidate commit sha")
    args = parser.parse_args()

    snaps_a = load_snapshots(args.baseline)
    snaps_b = load_snapshots(args.candidate)
    if not snaps_a or not snaps_b:
        raise SystemExit(3)

    report = build_diff_report(snaps_a, snaps_b, args.baseline_commit, args.candidate_commit)
    _validate_report(report)
    with open(args.out, "w") as f:
        f.write(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    raise SystemExit(_exit_code(report))


if __name__ == "__main__":
    main()
