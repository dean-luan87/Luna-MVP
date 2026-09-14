#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any, Dict, List, Tuple


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

    raise RuntimeError(
        "Unable to determine workspace root from cwd or non-resolved script parents"
    )


WORKSPACE_ROOT = _derive_workspace_root()

REGISTRY_PATH = Path("capabilities/registry/luna_capability_registry_v1.json")
DEPENDENCY_MAP_PATH = Path(
    "capabilities/registry/luna_capability_dependency_map_v1.json"
)
BASELINE_REGISTRY_PATH = Path(
    "capabilities/registry/luna_capability_module_baseline_registry_v1.json"
)

SYSTEM_MANIFEST_PATH = Path(
    "capabilities/registry/manifests/system_integration_validation_manifest_v1.json"
)
SYSTEM_BASELINE_PATH = Path(
    "capabilities/registry/baselines/system_integration_validation_baseline_v1.json"
)
SYSTEM_RUNNER_PATH = Path(
    "tools/evaluation/midplatform/run_system_integration_validation_v1.py"
)
SYSTEM_REPORT_PATH = Path(
    "_tmp_eval_out/system_integration_validation_v1_smoke_v0/system_integration_validation_v1.json"
)

FIELD_MANIFEST_PATH = Path(
    "capabilities/registry/manifests/field_perception_orchestrator_manifest_v1.json"
)
FIELD_BASELINE_PATH = Path(
    "capabilities/registry/baselines/field_perception_orchestrator_module_baseline_v1.json"
)
FIELD_RUNNER_PATH = Path(
    "tools/evaluation/midplatform/run_field_perception_visual_handoff_integration_v1.py"
)
FIELD_REPORT_PATH = Path(
    "_tmp_eval_out/field_perception_visual_handoff_integration_v1_smoke_v0/field_perception_visual_handoff_integration_v1.json"
)

MODEL_MANIFEST_PATH = Path(
    "capabilities/registry/manifests/model_manager_manifest_v1.json"
)
MODEL_BASELINE_PATH = Path(
    "capabilities/registry/baselines/model_manager_module_baseline_v1.json"
)
MODEL_RUNNER_PATH = Path(
    "tools/evaluation/midplatform/run_model_manager_module_integration_v1.py"
)
MODEL_REPORT_PATH = Path(
    "_tmp_eval_out/model_manager_module_integration_v1_smoke_v0/model_manager_module_integration_v1.json"
)
PROVIDER_REGISTRY_PATH = Path(
    "capabilities/midplatform/model_manager/registry/provider_registry_v1.json"
)

VERIFIER_NAME = "verify_recent_integration_unified_final_v1"
MODULE_NAME = "luna.recent_integration_unified_final_verifier"


def _abs(path: Path) -> Path:
    return (WORKSPACE_ROOT / path).absolute()


def _exists(path: Path) -> bool:
    return _abs(path).exists()


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(_abs(path).read_text(encoding="utf-8"))


def _stringify(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False)


def _flatten_values(payload: Any) -> List[Any]:
    values: List[Any] = []
    if isinstance(payload, dict):
        for key, value in payload.items():
            values.append(key)
            values.extend(_flatten_values(value))
        return values
    if isinstance(payload, list):
        for item in payload:
            values.extend(_flatten_values(item))
        return values
    values.append(payload)
    return values


def _manifest_explicit_flag(
    payload: Dict[str, Any], keys: Tuple[str, ...], phrases: Tuple[str, ...]
) -> bool:
    flat = _flatten_values(payload)
    lowered = [_stringify(v).lower() for v in flat]

    for k in keys:
        if any(s == k.lower() for s in lowered):
            return True
    for phrase in phrases:
        if any(phrase.lower() in s for s in lowered):
            return True
    return False


def _check_result(
    check_id: int, title: str, passed: bool, details: str
) -> Dict[str, Any]:
    return {
        "check_id": check_id,
        "title": title,
        "passed": passed,
        "details": details,
    }


def build_report() -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []

    registry = _read_json(REGISTRY_PATH)
    dependency_map = _read_json(DEPENDENCY_MAP_PATH)
    baseline_registry = _read_json(BASELINE_REGISTRY_PATH)

    system_manifest = _read_json(SYSTEM_MANIFEST_PATH)
    system_baseline = _read_json(SYSTEM_BASELINE_PATH)
    system_report = _read_json(SYSTEM_REPORT_PATH)

    field_manifest = _read_json(FIELD_MANIFEST_PATH)
    field_baseline = _read_json(FIELD_BASELINE_PATH)
    field_report = _read_json(FIELD_REPORT_PATH)

    model_manifest = _read_json(MODEL_MANIFEST_PATH)
    model_baseline = _read_json(MODEL_BASELINE_PATH)
    model_report = _read_json(MODEL_REPORT_PATH)
    provider_registry = _read_json(PROVIDER_REGISTRY_PATH)

    capabilities = registry.get("capabilities") or []
    capability_ids = {
        str(item.get("capability_id", ""))
        for item in capabilities
        if isinstance(item, dict)
    }

    target_capabilities = {
        "luna.model_manager",
        "luna.field_perception_orchestrator",
        "luna.system_integration_validation",
    }

    baseline_entries = {
        str(item.get("capability_id", "")): item
        for item in (baseline_registry.get("entries") or [])
        if isinstance(item, dict)
    }

    # A. Registry 与 Promotion
    c1 = target_capabilities.issubset(capability_ids)
    checks.append(
        _check_result(
            1,
            "Registry has required capability records",
            c1,
            "found=" + ",".join(sorted(target_capabilities & capability_ids)),
        )
    )

    manifest_paths_ok = all(
        _exists(p)
        for p in (MODEL_MANIFEST_PATH, FIELD_MANIFEST_PATH, SYSTEM_MANIFEST_PATH)
    )
    manifest_json_ok = all(
        isinstance(m, dict) for m in (model_manifest, field_manifest, system_manifest)
    )
    checks.append(
        _check_result(
            2,
            "Manifest paths exist and JSON readable",
            manifest_paths_ok and manifest_json_ok,
            "paths_ok=" + str(manifest_paths_ok) + ";json_ok=" + str(manifest_json_ok),
        )
    )

    baseline_paths_ok = all(
        _exists(p)
        for p in (MODEL_BASELINE_PATH, FIELD_BASELINE_PATH, SYSTEM_BASELINE_PATH)
    )
    baseline_json_ok = all(
        isinstance(b, dict) for b in (model_baseline, field_baseline, system_baseline)
    )
    checks.append(
        _check_result(
            3,
            "Baseline paths exist and JSON readable",
            baseline_paths_ok and baseline_json_ok,
            "paths_ok=" + str(baseline_paths_ok) + ";json_ok=" + str(baseline_json_ok),
        )
    )

    c4 = True
    c5 = True
    c6 = True
    for cid in target_capabilities:
        entry = baseline_entries.get(cid)
        if not isinstance(entry, dict):
            c4 = False
            c5 = False
            c6 = False
            continue
        c4 = c4 and bool(entry.get("calibration_enabled") is True)
        c5 = c5 and bool(entry.get("normal_runtime_load_allowed") is False)
        c6 = c6 and bool(entry.get("anomaly_diagnostic_load_allowed") is True)

    checks.append(
        _check_result(
            4, "Baseline registry calibration_enabled=true", c4, "target=3 capabilities"
        )
    )
    checks.append(
        _check_result(
            5,
            "Baseline registry normal_runtime_load_allowed=false",
            c5,
            "target=3 capabilities",
        )
    )
    checks.append(
        _check_result(
            6,
            "Baseline registry anomaly_diagnostic_load_allowed=true",
            c6,
            "target=3 capabilities",
        )
    )

    # B. Model Manager
    providers = provider_registry.get("providers") or []
    provider_ids = {
        str(item.get("model_id", "")) for item in providers if isinstance(item, dict)
    }
    checks.append(
        _check_result(
            7, "Provider registry has detection_v1", "detection_v1" in provider_ids, ""
        )
    )
    checks.append(
        _check_result(8, "Provider registry has slam_v1", "slam_v1" in provider_ids, "")
    )

    model_integration_pass = bool(model_report.get("integration_pass") is True)
    checks.append(
        _check_result(
            9,
            "Model Manager latest report integration_pass=true",
            model_integration_pass,
            "",
        )
    )

    model_failed_cases = model_report.get("failed_cases")
    if model_failed_cases is None:
        model_failed_cases = []
    checks.append(
        _check_result(
            10,
            "Model Manager latest report failed_cases=[]",
            isinstance(model_failed_cases, list) and len(model_failed_cases) == 0,
            "failed_cases=" + _stringify(model_failed_cases),
        )
    )

    checks.append(
        _check_result(
            11,
            "Model Manager boundary_flags_ok=true",
            bool(model_report.get("boundary_flags_ok") is True),
            "",
        )
    )

    model_deterministic_ok = bool(
        model_report.get("deterministic_replay") is True
        or model_report.get("deterministic_replay_ok") is True
    )
    checks.append(
        _check_result(
            12, "Model Manager deterministic_replay=true", model_deterministic_ok, ""
        )
    )

    model_report_abs = _abs(MODEL_REPORT_PATH)
    workspace_root_abs = WORKSPACE_ROOT.absolute()
    model_report_under_workspace = (
        model_report_abs == workspace_root_abs
        or workspace_root_abs in model_report_abs.parents
    )
    checks.append(
        _check_result(
            13,
            "Model Manager runner output path under Luna-Workspace-Min",
            model_report_under_workspace,
            str(model_report_abs),
        )
    )

    # C. Field Perception Visual Handoff
    checks.append(
        _check_result(
            14,
            "Field Perception total_cases=16",
            int(field_report.get("total_cases", -1)) == 16,
            "total_cases=" + str(field_report.get("total_cases")),
        )
    )
    checks.append(
        _check_result(
            15,
            "Field Perception passed_cases=16",
            int(field_report.get("passed_cases", -1)) == 16,
            "passed_cases=" + str(field_report.get("passed_cases")),
        )
    )
    checks.append(
        _check_result(
            16,
            "Field Perception failed_cases=[]",
            isinstance(field_report.get("failed_cases"), list)
            and len(field_report.get("failed_cases") or []) == 0,
            "failed_cases=" + _stringify(field_report.get("failed_cases")),
        )
    )
    checks.append(
        _check_result(
            17,
            "Field Perception boundary_preserved=true",
            bool(field_report.get("boundary_preserved") is True),
            "",
        )
    )
    checks.append(
        _check_result(
            18,
            "Field Perception deterministic_replay=true",
            bool(field_report.get("deterministic_replay") is True),
            "",
        )
    )
    checks.append(
        _check_result(
            19,
            "Field Perception unhandled_exceptions=0",
            int(field_report.get("unhandled_exceptions", -1)) == 0,
            "unhandled_exceptions=" + str(field_report.get("unhandled_exceptions")),
        )
    )

    # D. System Integration
    checks.append(
        _check_result(
            20,
            "System Integration integration_pass=true",
            bool(system_report.get("integration_pass") is True),
            "",
        )
    )
    checks.append(
        _check_result(
            21,
            "System Integration scenario_count=6",
            int(system_report.get("scenario_count", -1)) == 6,
            "scenario_count=" + str(system_report.get("scenario_count")),
        )
    )
    checks.append(
        _check_result(
            22,
            "System Integration failed_cases=[]",
            isinstance(system_report.get("failed_cases"), list)
            and len(system_report.get("failed_cases") or []) == 0,
            "failed_cases=" + _stringify(system_report.get("failed_cases")),
        )
    )
    checks.append(
        _check_result(
            23,
            "System Integration boundary_preserved=true",
            bool(system_report.get("boundary_preserved") is True),
            "",
        )
    )
    checks.append(
        _check_result(
            24,
            "System Integration deterministic_replay=true",
            bool(system_report.get("deterministic_replay") is True),
            "",
        )
    )
    checks.append(
        _check_result(
            25,
            "System Integration unhandled_exceptions=0",
            int(system_report.get("unhandled_exceptions", -1)) == 0,
            "unhandled_exceptions=" + str(system_report.get("unhandled_exceptions")),
        )
    )

    cases = system_report.get("cases") or []
    degraded_case = None
    for case in cases:
        if isinstance(case, dict) and str(case.get("case_id", "")) == "degraded_budget":
            degraded_case = case
            break

    degraded_ok = (
        isinstance(degraded_case, dict)
        and str(degraded_case.get("field_perception_status", ""))
        == "degraded_resource_plan"
    )
    checks.append(
        _check_result(
            26,
            "System Integration degraded_budget field_perception_status=degraded_resource_plan",
            degraded_ok,
            "actual="
            + str(
                degraded_case.get("field_perception_status")
                if isinstance(degraded_case, dict)
                else None
            ),
        )
    )

    all_trace_replay_preserved = all(
        isinstance(case, dict) and bool(case.get("trace_replay_preserved") is True)
        for case in cases
    )
    checks.append(
        _check_result(
            27,
            "System Integration all scenarios trace_replay_preserved=true",
            all_trace_replay_preserved,
            "case_count=" + str(len(cases)),
        )
    )

    all_boundary_preserved = all(
        isinstance(case, dict) and bool(case.get("boundary_preserved") is True)
        for case in cases
    )
    checks.append(
        _check_result(
            28,
            "System Integration all scenarios boundary_preserved=true",
            all_boundary_preserved,
            "case_count=" + str(len(cases)),
        )
    )

    # E. 治理边界
    checks.append(
        _check_result(
            29,
            "System manifest explicitly states candidate-only",
            _manifest_explicit_flag(
                system_manifest,
                keys=("candidate_only", "candidate_only_processing"),
                phrases=("candidate-only",),
            ),
            "",
        )
    )
    checks.append(
        _check_result(
            30,
            "System manifest explicitly states no real model execution",
            _manifest_explicit_flag(
                system_manifest,
                keys=("no_real_model_execution",),
                phrases=("no real model execution",),
            ),
            "",
        )
    )
    checks.append(
        _check_result(
            31,
            "System manifest explicitly states no real Field State write",
            _manifest_explicit_flag(
                system_manifest,
                keys=("no_real_field_state_write", "no_field_state_write_execution"),
                phrases=("no real field state write",),
            ),
            "",
        )
    )
    checks.append(
        _check_result(
            32,
            "System manifest explicitly states no runtime loop",
            _manifest_explicit_flag(
                system_manifest,
                keys=("no_runtime_loop",),
                phrases=("no runtime loop", "no runtime loop activation"),
            ),
            "",
        )
    )

    system_baseline_entry = baseline_entries.get("luna.system_integration_validation")
    c33 = isinstance(system_baseline_entry, dict) and bool(
        system_baseline_entry.get("normal_runtime_load_allowed") is False
    )
    checks.append(
        _check_result(33, "System baseline disallows normal runtime load", c33, "")
    )

    verifier_source = _abs(
        Path(
            "tools/evaluation/midplatform/verify_recent_integration_unified_final_v1.py"
        )
    ).read_text(encoding="utf-8")
    readonly_block_patterns = (
        r"\bsubprocess\b",
        r"\bos\.system\s*\(",
        r"\brun_system_integration_validation_v1\s*\(",
        r"\brun_model_manager_module_integration_v1\s*\(",
        r"\brun_field_perception_visual_handoff_integration_v1\s*\(",
    )
    c34 = not any(
        re.search(pattern, verifier_source) for pattern in readonly_block_patterns
    )
    checks.append(
        _check_result(
            34,
            "Verifier is read-only and does not call any integration runner",
            c34,
            "",
        )
    )

    real_model_import_or_call_patterns = (
        r"\bimport\s+torch\b",
        r"\bfrom\s+torch\s+import\b",
        r"\bimport\s+transformers\b",
        r"\bfrom\s+transformers\s+import\b",
        r"\bqwen\b\s*\(",
        r"\bgemini\b\s*\(",
        r"\bmodel_inference\b\s*\(",
        r"\bprovider_call\b\s*\(",
    )
    c35 = not any(
        re.search(pattern, verifier_source)
        for pattern in real_model_import_or_call_patterns
    )
    checks.append(
        _check_result(
            35,
            "Verifier does not import or call any real model execution entry",
            c35,
            "",
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

    boundary_preserved = all(
        c["passed"]
        for c in checks
        if c["check_id"] in {17, 23, 28, 29, 30, 31, 32, 33, 34, 35}
    )

    final_decision_candidate = (
        "READY_FOR_USER_TERMINAL_VERIFICATION"
        if failed_checks == 0
        else "BLOCKED_BY_VERIFIER_PREPARATION"
    )

    report = {
        "module": MODULE_NAME,
        "verifier": VERIFIER_NAME,
        "checked_scope": {
            "registry": [
                str(REGISTRY_PATH),
                str(DEPENDENCY_MAP_PATH),
                str(BASELINE_REGISTRY_PATH),
            ],
            "system_integration": [
                str(SYSTEM_MANIFEST_PATH),
                str(SYSTEM_BASELINE_PATH),
                str(SYSTEM_RUNNER_PATH),
                str(SYSTEM_REPORT_PATH),
            ],
            "field_perception": [
                str(FIELD_MANIFEST_PATH),
                str(FIELD_BASELINE_PATH),
                str(FIELD_RUNNER_PATH),
                str(FIELD_REPORT_PATH),
            ],
            "model_manager": [
                str(MODEL_MANIFEST_PATH),
                str(MODEL_BASELINE_PATH),
                str(MODEL_RUNNER_PATH),
                str(MODEL_REPORT_PATH),
                str(PROVIDER_REGISTRY_PATH),
            ],
        },
        "checks": checks,
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
        "blocker_count": blocker_count,
        "failed_items": failed_items,
        "boundary_preserved": boundary_preserved,
        "evidence_refs": [
            str(MODEL_REPORT_PATH),
            str(FIELD_REPORT_PATH),
            str(SYSTEM_REPORT_PATH),
            str(PROVIDER_REGISTRY_PATH),
        ],
        "final_decision_candidate": final_decision_candidate,
        "verifier_executed": False,
    }
    return report


def main() -> int:
    report = build_report()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
