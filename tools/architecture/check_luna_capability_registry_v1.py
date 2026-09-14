from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Set


REGISTRY_PATH = Path("capabilities/registry/luna_capability_registry_v1.json")
LIFECYCLE_PATH = Path(
    "capabilities/registry/luna_capability_lifecycle_registry_v1.json"
)
BASELINE_REGISTRY_PATH = Path(
    "capabilities/registry/luna_capability_module_baseline_registry_v1.json"
)


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _result(name: str, passed: bool, details: str) -> Dict[str, Any]:
    return {"check": name, "passed": passed, "details": details}


def _path_exists(rel_path: str | None) -> bool:
    if not rel_path:
        return False
    return Path(rel_path).exists()


def main() -> int:
    checks: List[Dict[str, Any]] = []

    # 1) registry json readable
    try:
        registry = _load_json(REGISTRY_PATH)
        lifecycle = _load_json(LIFECYCLE_PATH)
        baseline_registry = _load_json(BASELINE_REGISTRY_PATH)
        checks.append(_result("registry_json_readable", True, str(REGISTRY_PATH)))
    except Exception as e:  # pragma: no cover
        checks.append(_result("registry_json_readable", False, f"load_failed:{e}"))
        print(
            json.dumps(
                {"checks": checks, "passed": 0, "failed": len(checks)},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1

    capabilities = registry.get("capabilities", [])
    baseline_entries = baseline_registry.get("entries", [])
    baseline_by_capability = {
        str(item.get("capability_id", "")): item
        for item in baseline_entries
        if isinstance(item, dict)
    }
    lifecycle_statuses: Set[str] = {
        row.get("status_id")
        for row in lifecycle.get("statuses", [])
        if isinstance(row, dict)
    }

    # 2) capability_id unique
    ids = [c.get("capability_id") for c in capabilities]
    unique_ok = len(ids) == len(set(ids))
    checks.append(
        _result(
            "capability_id_unique",
            unique_ok,
            "duplicate_ids_found" if not unique_ok else f"count={len(ids)}",
        )
    )

    # 3) lifecycle status legal
    bad_status = [
        c.get("capability_id")
        for c in capabilities
        if c.get("lifecycle_status") not in lifecycle_statuses
    ]
    checks.append(
        _result(
            "lifecycle_status_legal",
            not bad_status,
            "ok" if not bad_status else f"invalid={bad_status}",
        )
    )

    # 4) manifest path exists (for declared manifest path)
    missing_manifest = [
        c.get("capability_id")
        for c in capabilities
        if c.get("manifest_path") is not None
        and not _path_exists(c.get("manifest_path"))
    ]
    checks.append(
        _result(
            "manifest_path_exists",
            not missing_manifest,
            "ok" if not missing_manifest else f"missing={missing_manifest}",
        )
    )

    # 5) functional module ready has ready evidence
    missing_ready_evidence = [
        c.get("capability_id")
        for c in capabilities
        if c.get("lifecycle_status") == "functional_module_ready"
        and not c.get("ready_evidence")
    ]
    checks.append(
        _result(
            "functional_ready_has_evidence",
            not missing_ready_evidence,
            "ok" if not missing_ready_evidence else f"missing={missing_ready_evidence}",
        )
    )

    # 5b) functional module ready modules must have baseline entry
    functional_ready_ids = [
        str(c.get("capability_id", ""))
        for c in capabilities
        if c.get("lifecycle_status") == "functional_module_ready"
    ]
    missing_baseline_entry = [
        cid for cid in functional_ready_ids if cid not in baseline_by_capability
    ]
    checks.append(
        _result(
            "functional_ready_has_baseline_entry",
            not missing_baseline_entry,
            "ok" if not missing_baseline_entry else f"missing={missing_baseline_entry}",
        )
    )

    # 5c) baseline path exists and JSON is valid
    missing_baseline_path = []
    invalid_baseline_json = []
    baseline_capability_mismatch = []
    invalid_runtime_load_flags = []
    for cid in functional_ready_ids:
        entry = baseline_by_capability.get(cid)
        if not isinstance(entry, dict):
            continue
        baseline_path = entry.get("baseline_path")
        if not _path_exists(baseline_path):
            missing_baseline_path.append(cid)
            continue
        try:
            baseline_payload = _load_json(Path(str(baseline_path)))
        except Exception:
            invalid_baseline_json.append(cid)
            continue
        if str(baseline_payload.get("capability_id", "")) != cid:
            baseline_capability_mismatch.append(cid)
        if (
            entry.get("normal_runtime_load_allowed") is not False
            or entry.get("anomaly_diagnostic_load_allowed") is not True
        ):
            invalid_runtime_load_flags.append(cid)

    checks.append(
        _result(
            "baseline_path_exists",
            not missing_baseline_path,
            "ok" if not missing_baseline_path else f"missing={missing_baseline_path}",
        )
    )
    checks.append(
        _result(
            "baseline_json_valid",
            not invalid_baseline_json,
            "ok" if not invalid_baseline_json else f"invalid={invalid_baseline_json}",
        )
    )
    checks.append(
        _result(
            "baseline_capability_id_match",
            not baseline_capability_mismatch,
            "ok"
            if not baseline_capability_mismatch
            else f"mismatch={baseline_capability_mismatch}",
        )
    )
    checks.append(
        _result(
            "baseline_runtime_load_flags",
            not invalid_runtime_load_flags,
            "ok"
            if not invalid_runtime_load_flags
            else f"invalid={invalid_runtime_load_flags}",
        )
    )

    # 6) field state reducer implementation path exists
    fsr = next(
        (
            c
            for c in capabilities
            if c.get("capability_id") == "luna.field_state_reducer"
        ),
        None,
    )
    fsr_impl_ok = bool(fsr and _path_exists(fsr.get("implementation_path")))
    checks.append(
        _result(
            "field_state_reducer_implementation_exists",
            fsr_impl_ok,
            "ok" if fsr_impl_ok else "missing_field_state_reducer_implementation",
        )
    )

    # 7) field state reducer integration runner exists
    fsr_runner = None
    if fsr and isinstance(fsr.get("integration_runner"), dict):
        fsr_runner = fsr["integration_runner"].get("path")
    fsr_runner_ok = _path_exists(fsr_runner)
    checks.append(
        _result(
            "field_state_reducer_runner_exists",
            fsr_runner_ok,
            "ok" if fsr_runner_ok else "missing_field_state_reducer_runner",
        )
    )

    # 8) no internal components registered as top-level capability modules
    forbidden_tokens = {
        "policy_evaluation",
        "policy_selection",
        "state_reduction",
        "trace_builder",
        "replay_builder",
    }
    bad_top_level = []
    for c in capabilities:
        cid = str(c.get("capability_id", ""))
        cname = str(c.get("capability_name", ""))
        token_hit = [t for t in forbidden_tokens if t in cid or t in cname.lower()]
        if token_hit:
            bad_top_level.append({"capability_id": cid, "tokens": token_hit})
    checks.append(
        _result(
            "no_internal_component_as_top_level",
            not bad_top_level,
            "ok" if not bad_top_level else f"invalid={bad_top_level}",
        )
    )

    passed = sum(1 for c in checks if c["passed"])
    failed = len(checks) - passed
    report = {
        "registry": str(REGISTRY_PATH),
        "checks": checks,
        "passed": passed,
        "failed": failed,
        "final_decision": "pass" if failed == 0 else "fail",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
