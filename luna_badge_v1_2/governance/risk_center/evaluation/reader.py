from typing import Any, Dict, List


_FORBIDDEN_KEYS = {"decision", "selected_result", "reason", "action", "override"}


def assert_no_control_fields(data: Dict[str, Any]) -> None:
    for key in _FORBIDDEN_KEYS:
        assert key not in data, "[EVAL-INV] forbidden control field present"


def read_timeline_from_jsonl(path: str) -> List[Dict[str, Any]]:
    timeline = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = __import__("json").loads(line)
            except Exception:
                continue
            bc_snapshot = record.get("decision_trace", {}).get("bc_snapshot")
            if not bc_snapshot:
                continue
            assert_no_control_fields(bc_snapshot)
            debug_view = bc_snapshot.get("debug_view")
            if debug_view is None:
                continue
            timeline.append(debug_view)
    return timeline
