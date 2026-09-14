# -*- coding: utf-8 -*-
"""Recognition Model Download And Install DryRun — cases v1.

Reads file-based P0 install plans, admits each plan (required fields present, no
prohibited execution flags), and plans the allowed non-destructive checks
(package / import / version / local-resource). A best-effort, side-effect-free
import probe (importlib.util.find_spec) records local availability for reporting
only — it never installs, downloads, runs inference or imports for execution.
"""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.recognition_model_download_and_install_dryrun.recognition_model_download_and_install_dryrun_types_v1 import (
    ALLOWED_CHECK_KINDS,
    PROHIBITED_REQUEST_FLAGS,
    REJECT_IF_MISSING_FIELDS,
    RecognitionModelImportVersionResult,
    RecognitionModelInstallCaseResult,
)

_SAMPLES_DIR = Path(__file__).resolve().parent / "samples"

INSTALL_PLAN_FILES: Dict[str, str] = {
    "rapidocr_p0": "sample_rapidocr_install_plan.json",
    "yolo_lightweight_p0": "sample_yolo_lightweight_install_plan.json",
    "opencv_visual_symbol_p0": "sample_opencv_visual_symbol_install_plan.json",
}

INVALID_PLAN_FILES: Dict[str, str] = {
    "invalid_missing_license_ref": "invalid_missing_license_ref_install_plan.json",
    "invalid_missing_download_source": "invalid_missing_download_source_install_plan.json",
    "invalid_commercial_runtime_for_agpl_yolo": "invalid_commercial_runtime_for_agpl_yolo.json",
    "invalid_real_inference_requested": "invalid_real_inference_requested_install_plan.json",
    "invalid_dataset_download_requested": "invalid_dataset_download_requested_install_plan.json",
    "invalid_adapter_dryrun_requested": "invalid_adapter_dryrun_requested_install_plan.json",
}

ALL_PLAN_FILES: Tuple[str, ...] = (
    tuple(INSTALL_PLAN_FILES.values()) + tuple(INVALID_PLAN_FILES.values())
)

POSITIVE_CASE_BY_TARGET: Dict[str, str] = {
    "rapidocr_p0": "rapidocr_download_install_check",
    "yolo_lightweight_p0": "yolo_lightweight_download_install_check",
    "opencv_visual_symbol_p0": "opencv_visual_symbol_install_check",
}


def read_local_plan(filename: str) -> Dict[str, Any]:
    return json.loads((_SAMPLES_DIR / filename).read_text(encoding="utf-8"))


def _missing_required_fields(plan: Dict[str, Any]) -> List[str]:
    missing: List[str] = []
    for f in REJECT_IF_MISSING_FIELDS:
        v = plan.get(f)
        if v is None or (isinstance(v, str) and not v.strip()):
            missing.append(f)
    return missing


def _prohibited_flags_present(plan: Dict[str, Any]) -> List[str]:
    present = [flag for flag in PROHIBITED_REQUEST_FLAGS if plan.get(flag) is True]
    if str(plan.get("allowed_use", "")).lower() == "commercial_runtime":
        present.append("commercial_runtime_requested")
    return present


def admit_install_plan(plan: Dict[str, Any]) -> Tuple[bool, List[str]]:
    reasons: List[str] = []
    for m in _missing_required_fields(plan):
        reasons.append(f"missing_required_field:{m}")
    for p in _prohibited_flags_present(plan):
        reasons.append(f"prohibited_request:{p}")
    return (len(reasons) == 0), reasons


def _safe_import_probe(module_name: str) -> RecognitionModelImportVersionResult:
    """Non-destructive availability probe. Never imports/executes; never raises."""
    available = False
    note = "module_not_locally_present_install_planned_for_install_dryrun"
    try:
        spec = importlib.util.find_spec(module_name) if module_name else None
        available = spec is not None
        if available:
            note = "module_spec_found_locally_no_execution_performed"
    except (ImportError, ValueError, ModuleNotFoundError):
        available = False
        note = "import_probe_safely_failed_treated_as_not_present"
    return RecognitionModelImportVersionResult(
        install_target="",
        expected_import_module=module_name,
        import_probe_kind="importlib.util.find_spec",
        import_available=available,
        note=note,
    )


def _planned_checks(plan: Dict[str, Any]) -> Tuple[str, ...]:
    checks = [
        "package_install_check",
        "model_download_check",
        "import_check",
        "version_check",
        "local_resource_check",
    ]
    if plan.get("model_weight_required") is False:
        checks.append("opencv_rule_runtime_check")
    else:
        checks.append("minimal_constructor_check")
    return tuple(c for c in checks if c in ALLOWED_CHECK_KINDS)


def _run_positive_install_case(install_target: str) -> RecognitionModelInstallCaseResult:
    plan = read_local_plan(INSTALL_PLAN_FILES[install_target])
    accepted, reasons = admit_install_plan(plan)
    probe = _safe_import_probe(str(plan.get("expected_import_module", "")))
    checks = _planned_checks(plan)
    # Case passes on admission + planned checks present + no real inference, regardless
    # of whether the package is already installed (install is the next concrete step).
    ok = accepted and len(checks) > 0
    notes = [
        f"license={plan.get('license_ref')}",
        f"commercial_use_status={plan.get('commercial_use_status')}",
        f"import_probe={probe.note}",
        "real_inference_not_executed",
    ]
    if install_target == "yolo_lightweight_p0":
        notes.append("commercial_runtime_approved=false_test_only")
    if install_target == "opencv_visual_symbol_p0":
        notes.append("no_model_weight_required")
    return RecognitionModelInstallCaseResult(
        case_id=POSITIVE_CASE_BY_TARGET[install_target],
        case_kind="positive",
        accepted=accepted,
        expected_result="accepted",
        passed=ok,
        install_target=install_target,
        model_id=str(plan.get("model_id", "")),
        planned_checks=checks,
        import_available=probe.import_available,
        real_inference_executed=False,
        reject_reasons=tuple(reasons),
        notes=tuple(notes),
    )


def _run_p0_matrix_case() -> RecognitionModelInstallCaseResult:
    covered: List[str] = []
    all_ok = True
    for target in INSTALL_PLAN_FILES:
        plan = read_local_plan(INSTALL_PLAN_FILES[target])
        accepted, _ = admit_install_plan(plan)
        all_ok = all_ok and accepted
        if accepted:
            covered.append(target)
    ok = all_ok and len(covered) == 3
    return RecognitionModelInstallCaseResult(
        case_id="p0_install_matrix_check",
        case_kind="positive",
        accepted=ok,
        expected_result="accepted",
        passed=ok,
        install_target="all_p0",
        planned_checks=tuple(covered),
        real_inference_executed=False,
        notes=(
            f"p0_coverage_count={len(covered)}",
            "rapidocr+yolo_lightweight+opencv_all_covered",
            "no_real_recognition",
        ),
    )


def run_positive_cases() -> List[RecognitionModelInstallCaseResult]:
    results = [
        _run_positive_install_case("rapidocr_p0"),
        _run_positive_install_case("yolo_lightweight_p0"),
        _run_positive_install_case("opencv_visual_symbol_p0"),
    ]
    results.append(_run_p0_matrix_case())
    return results


# --------------------------------------------------------------------------- #
# Negative cases: 6 from files + 2 from in-memory tampering.
# --------------------------------------------------------------------------- #
def _run_negative_file_case(case_id: str, filename: str) -> RecognitionModelInstallCaseResult:
    plan = read_local_plan(filename)
    accepted, reasons = admit_install_plan(plan)
    return RecognitionModelInstallCaseResult(
        case_id=case_id,
        case_kind="negative",
        accepted=accepted,
        expected_result="rejected",
        passed=accepted is False,
        install_target=str(plan.get("install_target", "")),
        model_id=str(plan.get("model_id", "")),
        reject_reasons=tuple(reasons),
    )


def _run_negative_tampered_case(
    case_id: str, base_target: str, mutate
) -> RecognitionModelInstallCaseResult:
    plan = copy.deepcopy(read_local_plan(INSTALL_PLAN_FILES[base_target]))
    mutate(plan)
    accepted, reasons = admit_install_plan(plan)
    return RecognitionModelInstallCaseResult(
        case_id=case_id,
        case_kind="negative",
        accepted=accepted,
        expected_result="rejected",
        passed=accepted is False,
        install_target=base_target,
        model_id=str(plan.get("model_id", "")),
        reject_reasons=tuple(reasons),
    )


def run_negative_cases() -> List[RecognitionModelInstallCaseResult]:
    results = [
        _run_negative_file_case(key, fname) for key, fname in INVALID_PLAN_FILES.items()
    ]
    results.append(
        _run_negative_tampered_case(
            "invalid_live_camera_sensor_requested", "rapidocr_p0",
            lambda p: (
                p.__setitem__("live_camera_requested", True),
                p.__setitem__("live_sensor_requested", True),
            ),
        )
    )
    results.append(
        _run_negative_tampered_case(
            "invalid_direct_action_speech_fact_write", "opencv_visual_symbol_p0",
            lambda p: (
                p.__setitem__("direct_action_requested", True),
                p.__setitem__("direct_speech_requested", True),
                p.__setitem__("fact_write_requested", True),
            ),
        )
    )
    return results
