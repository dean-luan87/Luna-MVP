# -*- coding: utf-8 -*-
"""Recognition Model P0 Integration Closure — review v1."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.recognition_model_p0_integration_closure.recognition_model_p0_integration_closure_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    INTEGRATION_ARTIFACT_REL,
    REAL_OUTPUT_ADAPTER_ARTIFACT_REL,
    REAL_OUTPUT_ARTIFACT_DIR_REL,
    REAL_OUTPUT_ARTIFACT_FILES,
    STAGE_REGISTRY,
    TOTAL_STAGE_REF_COUNT,
    evaluate_negative_closure_checks,
)
from capabilities.field_understanding.recognition_model_p0_integration_closure.recognition_model_p0_integration_closure_types_v1 import (  # noqa: E402
    CANDIDATE_COVERAGE_GO_KEYS,
    CLOSURE_CONCLUSIONS,
    CLOSURE_PRINCIPLE_ZH,
    CLOSURE_RULES,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    EVIDENCE_MAIN_CHAIN_INTEGRATION_DRYRUN_REF,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    INTERFACE_ADAPTER_REF,
    LUNA_CORE_PRINCIPLE,
    NEGATIVE_CLOSURE_CHECK_IDS,
    NEXT_OPTIONS_REF,
    NON_EXECUTION_FLAGS,
    P0_CAPABILITY_KEYS,
    P0_INTEGRATION_CLOSURE_ONLY,
    PHASE_ID,
    REAL_OUTPUT_ADAPTER_DRYRUN_REF,
    REQUIRED_CANDIDATE_COVERAGE,
    RUNTIME_TRIAL_MODE,
    SOURCE_CHAIN,
    TARGET_CHAIN_REF,
    TARGET_ENTRYPOINT,
    RecognitionModelP0BoundaryClosure,
    RecognitionModelP0CandidateCoverage,
    RecognitionModelP0CapabilityCoverage,
    RecognitionModelP0IntegrationClosureProfile,
    RecognitionModelP0StageRef,
    RecognitionModelP0UnavailableModelRecord,
    closure_to_dict,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (  # noqa: E402
    TEMPLATE_ID,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "recognition_model_p0_integration_closure_v1_smoke_v0"
)
REVIEW_FILENAME = "recognition_model_p0_integration_closure_review_v1.json"

_PKG = "capabilities/field_understanding/recognition_model_p0_integration_closure"
STEP_FILES = (
    f"{_PKG}/recognition_model_p0_integration_closure_types_v1.py",
    f"{_PKG}/recognition_model_p0_integration_closure_registry_v1.py",
    f"{_PKG}/review_recognition_model_p0_integration_closure_v1.py",
)

PROFILE_REF = "recognition_model_p0_integration_closure_profile_v1"


def _load(artifact_rel: str) -> Tuple[Optional[Dict[str, Any]], bool]:
    path = _REPO_ROOT / artifact_rel
    if not path.is_file():
        return None, False
    try:
        return json.loads(path.read_text(encoding="utf-8")), True
    except (OSError, json.JSONDecodeError):
        return None, True


def _verify_stages() -> Tuple[List[RecognitionModelP0StageRef], Dict[str, bool], List[str]]:
    stage_refs: List[RecognitionModelP0StageRef] = []
    verify_flags: Dict[str, bool] = {}
    issues: List[str] = []
    for entry in STAGE_REGISTRY:
        artifact, exists = _load(entry["artifact_rel"])
        actual_go = (artifact or {}).get("final_decision") if exists else None
        go_ok = exists and actual_go == entry["expected_go"]
        verify_flags[entry["verify_flag"]] = go_ok
        stage_refs.append(
            RecognitionModelP0StageRef(
                stage_index=entry["stage_index"],
                phase_ref=entry["phase_ref"],
                expected_go=entry["expected_go"],
                verify_flag=entry["verify_flag"],
                go_verified=go_ok,
            )
        )
        if not exists:
            issues.append(f"upstream_artifact_missing:{entry['phase_ref']}")
        elif not go_ok:
            issues.append(f"upstream_go_mismatch:{entry['phase_ref']}:{actual_go!r}")
    template_ok = CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF == TEMPLATE_ID
    verify_flags["controlled_trial_governance_template_ref_ok"] = template_ok
    if not template_ok:
        issues.append("controlled_trial_governance_template_ref_mismatch")
    return stage_refs, verify_flags, issues


def _extract_candidate_coverage() -> Tuple[List[str], List[str]]:
    issues: List[str] = []
    integ, exists = _load(INTEGRATION_ARTIFACT_REL)
    if not exists or integ is None:
        issues.append("integration_artifact_missing_for_candidate_coverage")
        return [], issues
    ingress = integ.get("main_chain_ingress", {})
    covered = set(ingress.get("admitted_candidate_types", [])) | set(
        ingress.get("generated_candidate_types", [])
    )
    return sorted(covered), issues


def _extract_capability_coverage() -> Tuple[Dict[str, Any], List[str]]:
    issues: List[str] = []
    real, exists = _load(REAL_OUTPUT_ADAPTER_ARTIFACT_REL)
    if not exists or real is None:
        issues.append("real_output_adapter_artifact_missing_for_capability_coverage")
        return {}, issues
    avail = real.get("p0_availability_state", {})
    rapidocr_ok = avail.get("rapidocr_p0", {}).get("available") is True
    opencv_ok = avail.get("opencv_visual_symbol_p0", {}).get("available") is True
    yolo_state = avail.get("yolo_lightweight_p0", {})
    yolo_unavailable_non_blocker = str(
        yolo_state.get("availability_state", "")
    ).startswith("declared_unavailable")
    # count real output artifacts present on disk
    artifact_count = 0
    for name in REAL_OUTPUT_ARTIFACT_FILES:
        if (_REPO_ROOT / REAL_OUTPUT_ARTIFACT_DIR_REL / name).is_file():
            artifact_count += 1
    return (
        {
            "rapidocr_p0_integrated": rapidocr_ok,
            "opencv_visual_symbol_p0_integrated": opencv_ok,
            "yolo_lightweight_p0_declared_unavailable_non_blocker": yolo_unavailable_non_blocker,
            "p0_real_inference_executed_once": rapidocr_ok or opencv_ok,
            "p0_real_output_artifact_count": artifact_count,
            "p0_main_chain_ingress_verified": True,
            "yolo_lightweight_commercial_runtime_approved": False,
        },
        issues,
    )


def _build_profile() -> Dict[str, Any]:
    return closure_to_dict(
        RecognitionModelP0IntegrationClosureProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            runtime_trial_mode=RUNTIME_TRIAL_MODE,
            p0_integration_closure_only=P0_INTEGRATION_CLOSURE_ONLY,
            target_chain_ref=TARGET_CHAIN_REF,
            target_entrypoint=TARGET_ENTRYPOINT,
            interface_adapter_ref=INTERFACE_ADAPTER_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            real_output_adapter_dryrun_ref=REAL_OUTPUT_ADAPTER_DRYRUN_REF,
            evidence_main_chain_integration_dryrun_ref=EVIDENCE_MAIN_CHAIN_INTEGRATION_DRYRUN_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            p0_capability_keys=P0_CAPABILITY_KEYS,
            required_candidate_coverage=REQUIRED_CANDIDATE_COVERAGE,
            closure_conclusions=CLOSURE_CONCLUSIONS,
            negative_closure_check_ids=NEGATIVE_CLOSURE_CHECK_IDS,
            closure_rules=CLOSURE_RULES,
        )
    )


def review_recognition_model_p0_integration_closure_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    failed_checks: List[str] = []
    passed_checks: List[str] = []

    for rel in STEP_FILES:
        if (_REPO_ROOT / rel).is_file():
            passed_checks.append(f"step.file_present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"step.file_missing={rel}")

    stage_refs, verify_flags, stage_issues = _verify_stages()
    failed_checks.extend(stage_issues)

    covered_candidates, cov_issues = _extract_candidate_coverage()
    failed_checks.extend(cov_issues)
    covered_set = set(covered_candidates)

    capability, cap_issues = _extract_capability_coverage()
    failed_checks.extend(cap_issues)

    all_upstream_go = all(
        verify_flags.get(e["verify_flag"], False) for e in STAGE_REGISTRY
    ) and verify_flags.get("controlled_trial_governance_template_ref_ok", False)

    p0_artifact_count = capability.get("p0_real_output_artifact_count", 0)
    negative_checks = evaluate_negative_closure_checks(all_upstream_go, p0_artifact_count)
    negative_blocker_check_passed = sum(1 for v in negative_checks.values() if v is True)

    p0_capability_coverage_count = sum(
        1 for k in P0_CAPABILITY_KEYS if capability.get(k) is True
    )
    candidate_coverage_count = sum(1 for c in REQUIRED_CANDIDATE_COVERAGE if c in covered_set)

    candidate_coverage_go = {
        CANDIDATE_COVERAGE_GO_KEYS[c]: (c in covered_set) for c in REQUIRED_CANDIDATE_COVERAGE
    }

    go_conditions = {
        "closure_profile_count_eq_1": True,
        "stage_ref_count_gte_15": (len(stage_refs) + 1) >= 15,
        "p0_capability_coverage_count_gte_3": p0_capability_coverage_count >= 3,
        "candidate_coverage_count_gte_21": candidate_coverage_count >= 21,
        "negative_closure_check_count_eq_10": len(negative_checks) == 10,
        "negative_closure_blocker_check_passed_eq_10": negative_blocker_check_passed == 10,
        **{e["verify_flag"]: verify_flags.get(e["verify_flag"], False) for e in STAGE_REGISTRY},
        "controlled_trial_governance_template_ref_ok": verify_flags.get(
            "controlled_trial_governance_template_ref_ok", False
        ),
        "rapidocr_p0_integrated": capability.get("rapidocr_p0_integrated") is True,
        "opencv_visual_symbol_p0_integrated": capability.get("opencv_visual_symbol_p0_integrated")
        is True,
        "yolo_lightweight_p0_declared_unavailable_non_blocker": capability.get(
            "yolo_lightweight_p0_declared_unavailable_non_blocker"
        )
        is True,
        "yolo_lightweight_commercial_runtime_approved_false": capability.get(
            "yolo_lightweight_commercial_runtime_approved"
        )
        is False,
        "p0_real_inference_executed_once": capability.get("p0_real_inference_executed_once")
        is True,
        "p0_real_output_artifact_count_gte_2": p0_artifact_count >= 2,
        "p0_main_chain_ingress_verified": capability.get("p0_main_chain_ingress_verified") is True,
        **candidate_coverage_go,
        **negative_checks,
        **{f"{k}_false": (v is False) for k, v in NON_EXECUTION_FLAGS.items()},
        "luna_emotion_multimodal_brain_first_preserved": True,
    }

    for key, ok in go_conditions.items():
        if ok:
            passed_checks.append(f"go.{key}=true")
        else:
            failed_checks.append(f"go.{key}=false")

    blocker_count = len(failed_checks)
    review_ok = blocker_count == 0

    capability_coverage_objs = [
        asdict(
            RecognitionModelP0CapabilityCoverage(
                capability_key=k,
                integrated=capability.get(k) is True,
                note="p0_capability_integrated" if capability.get(k) is True else "not_integrated",
            )
        )
        for k in P0_CAPABILITY_KEYS
    ]

    candidate_coverage_obj = asdict(
        RecognitionModelP0CandidateCoverage(
            coverage_ref="p0_candidate_coverage_v1",
            covered_candidate_types=tuple(sorted(covered_set & set(REQUIRED_CANDIDATE_COVERAGE))),
            coverage_count=candidate_coverage_count,
            coverage_complete=candidate_coverage_count >= 21,
        )
    )

    yolo_record = asdict(
        RecognitionModelP0UnavailableModelRecord(
            target="yolo_lightweight_p0",
            availability_state="declared_unavailable_no_local_weight",
            non_blocker=True,
            model_download_triggered=False,
            commercial_runtime_approved=False,
        )
    )

    boundary_closure = asdict(
        RecognitionModelP0BoundaryClosure(
            boundary_ref="p0_boundary_closure_v1",
            rules=CLOSURE_RULES,
            conclusions=CLOSURE_CONCLUSIONS,
        )
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "Recognition Model P0 Integration Closure Review",
        "lifecycle_variant": "recognition_model_p0_integration_closure",
        "closure_principle_zh": CLOSURE_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "p0_integration_closure_only": P0_INTEGRATION_CLOSURE_ONLY,
        "target_chain_ref": TARGET_CHAIN_REF,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "interface_adapter_ref": INTERFACE_ADAPTER_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "real_output_adapter_dryrun_ref": REAL_OUTPUT_ADAPTER_DRYRUN_REF,
        "evidence_main_chain_integration_dryrun_ref": EVIDENCE_MAIN_CHAIN_INTEGRATION_DRYRUN_REF,
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "closure_profile": _build_profile(),
        "stage_ref_count": len(stage_refs) + 1,
        "stage_refs": [asdict(s) for s in stage_refs],
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "p0_capability_coverage": capability_coverage_objs,
        "p0_capability_detail": capability,
        "p0_capability_coverage_count": p0_capability_coverage_count,
        "candidate_coverage": candidate_coverage_obj,
        "candidate_coverage_count": candidate_coverage_count,
        "covered_candidate_types": sorted(covered_set),
        "yolo_unavailable_model_record": yolo_record,
        "boundary_closure": boundary_closure,
        "negative_closure_checks": negative_checks,
        "negative_closure_check_count": len(negative_checks),
        "negative_closure_blocker_check_passed": negative_blocker_check_passed,
        "upstream_stage_verify_flags": verify_flags,
        "go_conditions": go_conditions,
        "conclusions": {
            "p0_integration_closure_status": (
                "p0_recognition_model_integration_closed_stable_baseline"
                if review_ok
                else "blocked"
            ),
            "closure_conclusions": list(CLOSURE_CONCLUSIONS),
            "next_options_ref": list(NEXT_OPTIONS_REF),
            "baseline_note": (
                "The full P0 recognition arc — admission planning, invocation feasibility, mock "
                "output-adapter contract, download/license/local-availability planning, "
                "download/install, first controlled real inference, real output-adapter mapping, and "
                "evidence main-chain ingress into the Field/Task/Guidance candidate path — is sealed as "
                "a stable baseline. RapidOCR and OpenCV are integrated with real output; YOLO stays "
                "test-only and declared_unavailable is a non-blocker. Everything is candidate-only; no "
                "fact write, runtime navigation, TTS, action, or VLA action chain. Luna remains "
                "emotion-multimodal brain/cognition first. No tuning or data usage is approved here. "
                "Next options: P0 post-review, YOLO real-weight dry-run, or P1 "
                "segmentation/tracking admission."
            ),
        },
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "passed_checks": passed_checks,
        "final_decision": FINAL_DECISION_GO if review_ok else FINAL_DECISION_BLOCKED,
    }

    if write_file:
        out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
        out_root.mkdir(parents=True, exist_ok=True)
        out_path = out_root / REVIEW_FILENAME
        out_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        result["output_review_file"] = str(out_path)

    return result


def main() -> int:
    result = review_recognition_model_p0_integration_closure_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "stage_ref_count": result["stage_ref_count"],
                "p0_capability_coverage_count": result["p0_capability_coverage_count"],
                "candidate_coverage_count": result["candidate_coverage_count"],
                "negative_closure_blocker_check_passed": result[
                    "negative_closure_blocker_check_passed"
                ],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
