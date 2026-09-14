import argparse
import json
import sys
from pathlib import Path


def _load(path: str) -> dict:
    with open(path, "r") as f:
        return json.loads(f.read())


def _diff_metrics(base: dict, cand: dict) -> dict:
    diff = {}
    for key in sorted(set(base.keys()) | set(cand.keys())):
        if base.get(key) != cand.get(key):
            diff[key] = {"baseline": base.get(key), "candidate": cand.get(key)}
    return diff


def _event_counts(events: list) -> dict:
    counts = {}
    for event in events:
        etype = event.get("type")
        counts[etype] = counts.get(etype, 0) + 1
    return counts


def _hint_counts(summary: list) -> dict:
    counts = {}
    for item in summary:
        for hint in item.get("cause_hints", []):
            counts[hint] = counts.get(hint, 0) + 1
    return counts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", required=True, help="baseline ra_view.json")
    parser.add_argument("--candidate", required=True, help="candidate ra_view.json")
    parser.add_argument("--out", required=True, help="output ra_compare.json")
    args = parser.parse_args()

    baseline = _load(args.baseline)
    candidate = _load(args.candidate)

    report = {
        "schema_version": "ra_compare.v1",
        "metrics_delta": _diff_metrics(baseline.get("metrics", {}), candidate.get("metrics", {})),
        "events_delta": {
            "baseline": _event_counts(baseline.get("events", [])),
            "candidate": _event_counts(candidate.get("events", [])),
        },
        "behavior_profile_delta": {
            "baseline": baseline.get("behavior_profile", {}),
            "candidate": candidate.get("behavior_profile", {}),
        },
        "root_cause_hint_delta": {
            "baseline": _hint_counts(baseline.get("root_cause_summary", [])),
            "candidate": _hint_counts(candidate.get("root_cause_summary", [])),
        },
        "event_type_mix_delta": {
            "baseline": _event_counts(baseline.get("events", [])),
            "candidate": _event_counts(candidate.get("events", [])),
        },
    }

    with open(args.out, "w") as f:
        f.write(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
