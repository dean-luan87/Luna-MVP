#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List


CLOSURE_ID = "luna.recent_integration_unified_record_closure_v1_001"
CHECKER_NAME = "check_recent_integration_unified_record_closure_v1"


def _is_workspace_root(candidate: Path) -> bool:
    return (
        (candidate / "AGENTS.md").exists()
        and (candidate / "capabilities").is_dir()
        and (candidate / "tools" / "evaluation" / "midplatform").is_dir()
    )


def _derive_workspace_root() -> Path:
    cwd = Path.cwd()
    if _is_workspace_root(cwd):
        return cwd.absolute()

    script_abs = Path(__file__).absolute()
    for candidate in (script_abs.parent, *script_abs.parents):
        if _is_workspace_root(candidate):
            return candidate.absolute()

    raise RuntimeError("Unable to determine workspace root")


WORKSPACE_ROOT = _derive_workspace_root()

CLOSURE_DOC_PATH = Path(
    "docs/architecture/closure/recent_integration_unified_record_closure_v1.md"
)
UNIFIED_VERIFIER_PATH = Path(
    "tools/evaluation/midplatform/verify_recent_integration_unified_final_v1.py"
)

MODEL_REPORT_PATH = Path(
    "_tmp_eval_out/model_manager_module_integration_v1_smoke_v0/model_manager_module_integration_v1.json"
)
PROVIDER_REGISTRY_PATH = Path(
    "capabilities/midplatform/model_manager/registry/provider_registry_v1.json"
)
MODEL_MANIFEST_PATH = Path(
    "capabilities/registry/manifests/model_manager_manifest_v1.json"
)
MODEL_BASELINE_PATH = Path(
    "capabilities/registry/baselines/model_manager_module_baseline_v1.json"
)

FIELD_REPORT_PATH = Path(
    "_tmp_eval_out/field_perception_visual_handoff_integration_v1_smoke_v0/field_perception_visual_handoff_integration_v1.json"
)
FIELD_MANIFEST_PATH = Path(
    "capabilities/registry/manifests/field_perception_orchestrator_manifest_v1.json"
)
FIELD_BASELINE_PATH = Path(
    "capabilities/registry/baselines/field_perception_orchestrator_module_baseline_v1.json"
)

SYSTEM_REPORT_PATH = Path(
    "_tmp_eval_out/system_integration_validation_v1_smoke_v0/system_integration_validation_v1.json"
)
SYSTEM_MANIFEST_PATH = Path(
    "capabilities/registry/manifests/system_integration_validation_manifest_v1.json"
)
SYSTEM_BASELINE_PATH = Path(
    "capabilities/registry/baselines/system_integration_validation_baseline_v1.json"
)

CAPABILITY_REGISTRY_PATH = Path(
    "capabilities/registry/luna_capability_registry_v1.json"
)
BASELINE_REGISTRY_PATH = Path(
    "capabilities/registry/luna_capability_module_baseline_registry_v1.json"
)

ALL_EVIDENCE_PATHS = [
    CLOSURE_DOC_PATH,
    UNIFIED_VERIFIER_PATH,
    MODEL_REPORT_PATH,
    PROVIDER_REGISTRY_PATH,
    MODEL_MANIFEST_PATH,
    MODEL_BASELINE_PATH,
    FIELD_REPORT_PATH,
    FIELD_MANIFEST_PATH,
    FIELD_BASELINE_PATH,
    SYSTEM_REPORT_PATH,
    SYSTEM_MANIFEST_PATH,
    SYSTEM_BASELINE_PATH,
    CAPABILITY_REGISTRY_PATH,
    BASELINE_REGISTRY_PATH,
]


def _abs(path: Path) -> Path:
    return (WORKSPACE_ROOT / path).absolute()


def _exists(path: Path) -> bool:
    return _abs(path).exists()


def _read_text(path: Path) -> str:
    return _abs(path).read_text(encoding="utf-8")


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(_read_text(path))


def _check(
    check_id: int, title: str, passed: bool, details: str = ""
) -> Dict[str, Any]:
    return {
        "check_id": check_id,
        "title": title,
        "passed": passed,
        "details": details,
    }


def _contains_all(text: str, items: List[str]) -> bool:
    return all(item in text for item in items)


def build_report() -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []

    closure_exists = _exists(CLOSURE_DOC_PATH)
    checks.append(_check(1, "closure document exists", closure_exists))

    closure_text = _read_text(CLOSURE_DOC_PATH) if closure_exists else ""

    covered_work_ok = _contains_all(
        closure_text,
        [
            "Model Manager Provider Registry Alignment",
            "Field Perception Visual Handoff",
            "System Integration Validation",
        ],
    )
    checks.append(_check(2, "three covered work items are present", covered_work_ok))

    missing_paths = [str(path) for path in ALL_EVIDENCE_PATHS if not _exists(path)]
    checks.append(
        _check(
            3,
            "all evidence paths exist",
            len(missing_paths) == 0,
            "missing=" + ",".join(missing_paths),
        )
    )

    model_report = _read_json(MODEL_REPORT_PATH)
    provider_registry = _read_json(PROVIDER_REGISTRY_PATH)
    field_report = _read_json(FIELD_REPORT_PATH)
    system_report = _read_json(SYSTEM_REPORT_PATH)
    system_manifest = _read_json(SYSTEM_MANIFEST_PATH)
    baseline_registry = _read_json(BASELINE_REGISTRY_PATH)

    model_core_ok = (
        bool(model_report.get("integration_pass") is True)
        and isinstance(model_report.get("failed_cases", []), list)
        and len(model_report.get("failed_cases", [])) == 0
        and bool(model_report.get("boundary_flags_ok") is True)
        and bool(
            model_report.get("deterministic_replay_ok") is True
            or model_report.get("deterministic_replay") is True
        )
    )
    checks.append(_check(4, "Model Manager key values match report", model_core_ok))

    provider_ids = {
        str(item.get("model_id", ""))
        for item in (provider_registry.get("providers") or [])
        if isinstance(item, dict)
    }
    checks.append(
        _check(
            5,
            "detection_v1 and slam_v1 exist in provider registry",
            "detection_v1" in provider_ids and "slam_v1" in provider_ids,
        )
    )

    field_1616_ok = (
        int(field_report.get("total_cases", -1)) == 16
        and int(field_report.get("passed_cases", -1)) == 16
        and isinstance(field_report.get("failed_cases"), list)
        and len(field_report.get("failed_cases") or []) == 0
    )
    checks.append(_check(6, "Field Perception 16/16", field_1616_ok))

    system_66_ok = (
        bool(system_report.get("integration_pass") is True)
        and int(system_report.get("scenario_count", -1)) == 6
        and isinstance(system_report.get("failed_cases"), list)
        and len(system_report.get("failed_cases") or []) == 0
    )
    checks.append(_check(7, "System Integration 6/6", system_66_ok))

    degraded_case = None
    for case in system_report.get("cases") or []:
        if isinstance(case, dict) and str(case.get("case_id", "")) == "degraded_budget":
            degraded_case = case
            break
    degraded_ok = (
        isinstance(degraded_case, dict)
        and str(degraded_case.get("field_perception_status", ""))
        == "degraded_resource_plan"
    )
    checks.append(_check(8, "degraded_budget contract value is correct", degraded_ok))

    all_trace_preserved = all(
        isinstance(case, dict) and bool(case.get("trace_replay_preserved") is True)
        for case in (system_report.get("cases") or [])
    )
    all_boundary_preserved = all(
        isinstance(case, dict) and bool(case.get("boundary_preserved") is True)
        for case in (system_report.get("cases") or [])
    )
    boundary_trace_replay_ok = (
        bool(model_report.get("boundary_flags_ok") is True)
        and bool(field_report.get("boundary_preserved") is True)
        and bool(field_report.get("deterministic_replay") is True)
        and bool(system_report.get("boundary_preserved") is True)
        and bool(system_report.get("deterministic_replay") is True)
        and bool(system_report.get("trace_replay_refs_preserved") is True)
        and all_trace_preserved
        and all_boundary_preserved
    )
    checks.append(
        _check(9, "boundary/trace/replay values are correct", boundary_trace_replay_ok)
    )

    checks.append(
        _check(
            10,
            "closure declares candidate-only",
            "candidate-only: true" in closure_text,
        )
    )
    checks.append(
        _check(
            11,
            "closure declares no real model execution",
            "no real model execution: true" in closure_text,
        )
    )
    checks.append(
        _check(
            12,
            "closure declares no real Field State write",
            "no real Field State write: true" in closure_text,
        )
    )
    checks.append(
        _check(
            13,
            "closure declares no runtime loop",
            "no runtime loop: true" in closure_text,
        )
    )

    unified_3535_ok = _contains_all(
        closure_text,
        [
            "passed_checks: 35",
            "failed_checks: 0",
            "blocker_count: 0",
            "boundary_preserved: true",
            "exit_code: 0",
            "decision: RECENT_INTEGRATION_UNIFIED_FINAL_VERIFIER_GO",
        ],
    )
    checks.append(_check(14, "closure records unified verifier 35/35", unified_3535_ok))

    allowed_candidates = {
        "READY_FOR_USER_TERMINAL_CLOSURE_VERIFICATION",
        "BLOCKED_BY_CLOSURE_RECORD_INCONSISTENCY",
    }
    closure_candidate_match = re.search(
        r"final_closure_candidate:\s*([A-Z_]+)",
        closure_text,
    )
    closure_candidate = (
        closure_candidate_match.group(1) if closure_candidate_match else ""
    )
    checks.append(
        _check(
            15,
            "closure final candidate is valid",
            closure_candidate in allowed_candidates,
            "value=" + closure_candidate,
        )
    )

    checker_source = _read_text(
        Path(
            "tools/evaluation/midplatform/check_recent_integration_unified_record_closure_v1.py"
        )
    )
    readonly_ok = not any(
        re.search(pattern, checker_source)
        for pattern in (
            r"\bsubprocess\b",
            r"\bos\.system\s*\(",
            r"\brun_.*integration.*\(",
            r"\bverify_recent_integration_unified_final_v1\s*\(",
        )
    )
    checks.append(
        _check(16, "checker is read-only and does not call any runner", readonly_ok)
    )

    baseline_entries = {
        str(item.get("capability_id", "")): item
        for item in (baseline_registry.get("entries") or [])
        if isinstance(item, dict)
    }
    baseline_flags_ok = True
    for cid in (
        "luna.model_manager",
        "luna.field_perception_orchestrator",
        "luna.system_integration_validation",
    ):
        entry = baseline_entries.get(cid)
        if not isinstance(entry, dict):
            baseline_flags_ok = False
            continue
        baseline_flags_ok = baseline_flags_ok and bool(
            entry.get("normal_runtime_load_allowed") is False
        )
        baseline_flags_ok = baseline_flags_ok and bool(
            entry.get("anomaly_diagnostic_load_allowed") is True
        )
    checks.append(
        _check(
            17,
            "baseline runtime load flags match closure boundary",
            baseline_flags_ok,
        )
    )

    manifest_boundary_ok = (
        json.dumps(system_manifest, ensure_ascii=False).lower().find("candidate-only")
        != -1
        and bool(
            system_manifest.get("ready_evidence", {}).get("no_real_model_execution")
            is True
        )
        and bool(
            system_manifest.get("ready_evidence", {}).get("no_real_field_state_write")
            is True
        )
    )
    checks.append(
        _check(
            18, "system manifest boundary declarations present", manifest_boundary_ok
        )
    )

    passed_checks = sum(1 for c in checks if c["passed"])
    failed_items = [
        {"check_id": c["check_id"], "title": c["title"], "details": c["details"]}
        for c in checks
        if not c["passed"]
    ]
    failed_checks = len(failed_items)
    blocker_count = failed_checks

    evidence_consistent = failed_checks == 0
    boundary_preserved = all(
        c["passed"]
        for c in checks
        if c["check_id"] in {4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18}
    )

    final_decision_candidate = (
        "READY_FOR_USER_TERMINAL_CLOSURE_VERIFICATION"
        if failed_checks == 0
        else "BLOCKED_BY_CLOSURE_RECORD_INCONSISTENCY"
    )

    return {
        "closure_id": CLOSURE_ID,
        "checker": CHECKER_NAME,
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
        "blocker_count": blocker_count,
        "failed_items": failed_items,
        "evidence_consistent": evidence_consistent,
        "boundary_preserved": boundary_preserved,
        "final_decision_candidate": final_decision_candidate,
        "checker_executed": True,
    }


def main() -> int:
    report = build_report()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
