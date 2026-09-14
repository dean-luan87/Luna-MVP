from __future__ import annotations

from typing import Any, Dict, Iterable, Mapping, Sequence, Tuple


def resolve_dependencies_v1(
    *,
    dependency_refs: Iterable[str],
    dependency_snapshot: Mapping[str, str],
) -> Dict[str, Any]:
    refs = tuple(str(x) for x in dependency_refs)
    statuses = {ref: str(dependency_snapshot.get(ref, "unknown")) for ref in refs}
    unresolved = tuple(
        ref for ref, status in statuses.items() if status not in {"completed", "ready"}
    )
    all_resolved = len(unresolved) == 0
    return {
        "dependency_refs": refs,
        "dependency_statuses": statuses,
        "waiting_dependency_refs": unresolved,
        "dependency_waiting": not all_resolved,
        "dependency_order": tuple(sorted(refs)),
    }


def enforce_waiting_dependency_rule_v1(
    *,
    current_status: str,
    waiting_dependency_refs: Sequence[str],
) -> Dict[str, Any]:
    waiting = tuple(str(x) for x in waiting_dependency_refs)
    should_wait = len(waiting) > 0
    if current_status == "waiting_dependency" and not should_wait:
        return {
            "next_status_hint": "ready",
            "rule_applied": "waiting_dependency_to_ready",
        }
    if should_wait and current_status in {"planned", "ready", "running_candidate"}:
        return {
            "next_status_hint": "waiting_dependency",
            "rule_applied": "force_waiting_dependency",
        }
    return {
        "next_status_hint": current_status,
        "rule_applied": "no_change",
    }
