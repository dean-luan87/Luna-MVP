import json
from typing import Any, Dict, List


_FORBIDDEN_KEYS = {"decision", "selected_result", "reason", "action", "override", "abilities"}


def _assert_readable_snapshot(bc_snapshot: Dict[str, Any]) -> None:
    for key in _FORBIDDEN_KEYS:
        assert key not in bc_snapshot, "[RA-VIEW] forbidden control field present"


def read_timeline(path: str) -> List[Dict[str, Any]]:
    timeline = []
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
            if not bc_snapshot:
                continue
            _assert_readable_snapshot(bc_snapshot)
            entry = {
                "ts": bc_snapshot.get("authority", {}).get("since", 0.0),
                "authority_raw": bc_snapshot.get("authority", {}).get("raw"),
                "authority_effective": bc_snapshot.get("authority", {}).get("effective"),
                "authority_blocked_by": bc_snapshot.get("authority", {}).get("blocked_by"),
                "risk_level": bc_snapshot.get("risk", {}).get("level"),
                "envelope_status": bc_snapshot.get("envelope", {}).get("status"),
                "risk_vo_level": bc_snapshot.get("risk", {}).get("vo", {}).get("level"),
                "gate": bc_snapshot.get("gate"),
                "distortion_distorted": bc_snapshot.get("distortion", {}).get("distorted", False),
                "distortion_codes": bc_snapshot.get("distortion", {}).get("codes", []),
                "c_decision": bc_snapshot.get("c_decision"),
                "bc_action": bc_snapshot.get("bc_action"),
            }
            timeline.append(entry)
    return timeline
