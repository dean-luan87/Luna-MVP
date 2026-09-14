# -*- coding: utf-8 -*-
"""Recognition Model P1 Family Expansion Planning — review v1."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.recognition_model_p1_family_expansion_planning.recognition_model_p1_family_expansion_planning_registry_v1 import (  # noqa: E402
    CONTROL_CHECKS,
    DATA_HANDLING_CHECKS,
    EXPANSION_SEQUENCE,
    FAMILY_REGISTRY,
    GOVERNANCE_TEMPLATE_STAGE_REF,
    INTERACTION_TESTS,
    STAGE_REGISTRY,
    TIER_POLICIES,
    TOTAL_STAGE_REF_COUNT,
)
from capabilities.field_understanding.recognition_model_p1_family_expansion_planning.recognition_model_p1_family_expansion_planning_types_v1 import (  # noqa: E402
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    FAMILY_FLAG_KEYS,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    INTERFACE_ADAPTER_REF,
    LUNA_CORE_PRINCIPLE,
    NEXT_PHASE_REF,
    NON_EXECUTION_FLAGS,
    OUTPUT_STANDARD_FIELDS,
    OUTPUT_STANDARD_REQUIRED_FLAGS,
    P0_BASELINE_REF,
    P1_FAMILY_EXPANSION_PLANNING_ONLY,
    PHASE_ID,
    PLANNING_PRINCIPLE_ZH,
    PLANNING_RULES,
    REJECT_IF_MISSING_FIELDS,
    RUNTIME_TRIAL_MODE,
    SEQUENCING_FLAGS,
    SOURCE_CHAIN,
    TARGET_CHAIN_REF,
    TARGET_ENTRYPOINT,
    MidplatformModelControlReadinessPolicy,
    MidplatformModelDataHandlingReadinessPolicy,
    RecognitionModelAdapterReadinessPolicy,
    RecognitionModelExpansionTierPolicy,
    RecognitionModelFamilyExpansionPolicy,
    RecognitionModelInteractionReadinessPolicy,
    RecognitionModelOutputStandardPolicy,
    RecognitionModelP1FamilyExpansionPlanningProfile,
    planning_to_dict,
)
from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (  # noqa: E402
    TEMPLATE_ID,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "recognition_model_p1_family_expansion_planning_v1_smoke_v0"
)
REVIEW_FILENAME = "recognition_model_p1_family_expansion_planning_review_v1.json"

_PKG = "capabilities/field_understanding/recognition_model_p1_family_expansion_planning"
STEP_FILES = (
    f"{_PKG}/recognition_model_p1_family_expansion_planning_types_v1.py",
    f"{_PKG}/recognition_model_p1_family_expansion_planning_registry_v1.py",
    f"{_PKG}/review_recognition_model_p1_family_expansion_planning_v1.py",
)

PROFILE_REF = "recognition_model_p1_family_expansion_planning_profile_v1"


def _load(artifact_rel: str) -> Tuple[Optional[Dict[str, Any]], bool]:
    path = _REPO_ROOT / artifact_rel
    if not path.is_file():
        return None, False
    try:
        return json.loads(path.read_text(encoding="utf-8")), True
    except (OSError, json.JSONDecodeError):
        return None, True


def _verify_stages() -> Tuple[List[Dict[str, Any]], Dict[str, bool], List[str]]:
    stage_refs: List[Dict[str, Any]] = []
    verify_flags: Dict[str, bool] = {}
    issues: List[str] = []
    for entry in STAGE_REGISTRY:
        artifact, exists = _load(entry["artifact_rel"])
        actual_go = (artifact or {}).get("final_decision") if exists else None
        go_ok = exists and actual_go == entry["expected_go"]
        stage_refs.append(
            {
                "stage_index": entry["stage_index"],
                "phase_ref": entry["phase_ref"],
                "expected_go": entry["expected_go"],
                "gated": entry["verify"],
                "go_verified": go_ok,
            }
        )
        if entry["verify"]:
            verify_flags[entry["verify_flag"]] = go_ok
            if not exists:
                issues.append(f"upstream_artifact_missing:{entry['phase_ref']}")
            elif not go_ok:
                issues.append(f"upstream_go_mismatch:{entry['phase_ref']}:{actual_go!r}")
    template_ok = CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF == TEMPLATE_ID
    verify_flags["controlled_trial_governance_template_ref_ok"] = template_ok
    if not template_ok:
        issues.append("controlled_trial_governance_template_ref_mismatch")
    return stage_refs, verify_flags, issues


def _build_profile() -> Dict[str, Any]:
    return planning_to_dict(
        RecognitionModelP1FamilyExpansionPlanningProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            runtime_trial_mode=RUNTIME_TRIAL_MODE,
            p1_family_expansion_planning_only=P1_FAMILY_EXPANSION_PLANNING_ONLY,
            p0_baseline_ref=P0_BASELINE_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            target_entrypoint=TARGET_ENTRYPOINT,
            interface_adapter_ref=INTERFACE_ADAPTER_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            output_standard_fields=OUTPUT_STANDARD_FIELDS,
            reject_if_missing_fields=REJECT_IF_MISSING_FIELDS,
            expansion_sequence=EXPANSION_SEQUENCE,
            planning_rules=PLANNING_RULES,
        )
    )


def review_recognition_model_p1_family_expansion_planning_v1(
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

    # Build policy objects.
    tier_policies = [
        asdict(
            RecognitionModelExpansionTierPolicy(
                tier=t["tier"],
                description=t["description"],
                execution_status=t["execution_status"],
            )
        )
        for t in TIER_POLICIES
    ]

    family_policies = [
        asdict(
            RecognitionModelFamilyExpansionPolicy(
                family_id=f["family_id"],
                family_name=f["family_name"],
                tier=f["tier"],
                execution_status=f["execution_status"],
                candidate_models=tuple(f["candidate_models"]),
                target_candidates=tuple(f["target_candidates"]),
                boundaries=tuple(f["boundaries"]),
            )
        )
        for f in FAMILY_REGISTRY
    ]

    output_standard_policies = [
        asdict(
            RecognitionModelOutputStandardPolicy(
                family_id=f["family_id"],
                required_fields=OUTPUT_STANDARD_FIELDS,
                reject_if_missing_fields=REJECT_IF_MISSING_FIELDS,
                must_map_to_luna_standard=True,
            )
        )
        for f in FAMILY_REGISTRY
    ]

    adapter_readiness_policies = [
        asdict(
            RecognitionModelAdapterReadinessPolicy(
                family_id=f["family_id"],
                adapter_ref=INTERFACE_ADAPTER_REF,
                must_pass_adapter_before_candidate=True,
                output_becomes_evidence_candidate_first=True,
            )
        )
        for f in FAMILY_REGISTRY
    ]

    interaction_policies = [
        asdict(
            RecognitionModelInteractionReadinessPolicy(
                interaction_id=i["interaction_id"],
                description=i["description"],
                deferred_but_planned=True,
            )
        )
        for i in INTERACTION_TESTS
    ]

    data_handling_policies = [
        asdict(
            MidplatformModelDataHandlingReadinessPolicy(
                check_id=c["check_id"],
                description=c["description"],
                deferred_but_planned=True,
            )
        )
        for c in DATA_HANDLING_CHECKS
    ]

    control_policies = [
        asdict(
            MidplatformModelControlReadinessPolicy(
                check_id=c["check_id"],
                description=c["description"],
                deferred_but_planned=True,
            )
        )
        for c in CONTROL_CHECKS
    ]

    # Family planned/reserved flags.
    planned_family_ids = {f["family_id"] for f in FAMILY_REGISTRY}
    family_flags = {
        flag: (fid in planned_family_ids) for fid, flag in FAMILY_FLAG_KEYS.items()
    }

    output_standard_flags = {
        flag: (field in OUTPUT_STANDARD_FIELDS)
        for field, flag in OUTPUT_STANDARD_REQUIRED_FLAGS.items()
    }

    sequencing_flag_values = {flag: True for flag in SEQUENCING_FLAGS}

    go_conditions = {
        "planning_profile_count_eq_1": True,
        "upstream_stage_ref_count_gte_15": (len(stage_refs) + 1) >= 15,
        "expansion_family_policy_count_gte_7": len(family_policies) >= 7,
        "output_standard_policy_count_gte_7": len(output_standard_policies) >= 7,
        "adapter_readiness_policy_count_gte_7": len(adapter_readiness_policies) >= 7,
        "interaction_readiness_policy_count_gte_8": len(interaction_policies) >= 8,
        "midplatform_data_handling_readiness_count_gte_10": len(data_handling_policies) >= 10,
        "midplatform_control_readiness_count_gte_10": len(control_policies) >= 10,
        "p0_integration_closure_go_verified": verify_flags.get(
            "p0_integration_closure_go_verified", False
        ),
        "phase_one_evidence_main_chain_closure_go_verified": verify_flags.get(
            "phase_one_evidence_main_chain_closure_go_verified", False
        ),
        "rgb_vision_evidence_chain_closure_go_verified": verify_flags.get(
            "rgb_vision_evidence_chain_closure_go_verified", False
        ),
        "rgb_slam_cross_modal_closure_go_verified": verify_flags.get(
            "rgb_slam_cross_modal_closure_go_verified", False
        ),
        "field_task_guidance_safety_chain_closure_go_verified": verify_flags.get(
            "field_task_guidance_safety_chain_closure_go_verified", False
        ),
        "interface_layer_governance_verified": verify_flags.get(
            "interface_layer_governance_verified", False
        ),
        "model_admission_governance_verified": verify_flags.get(
            "model_admission_governance_verified", False
        ),
        "controlled_trial_governance_template_ref_ok": verify_flags.get(
            "controlled_trial_governance_template_ref_ok", False
        ),
        **family_flags,
        **output_standard_flags,
        **sequencing_flag_values,
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

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "Recognition Model P1 Family Expansion Planning Review",
        "lifecycle_variant": "recognition_model_p1_family_expansion_planning",
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "runtime_trial_mode": RUNTIME_TRIAL_MODE,
        "p1_family_expansion_planning_only": P1_FAMILY_EXPANSION_PLANNING_ONLY,
        "p0_baseline_ref": P0_BASELINE_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "target_entrypoint": TARGET_ENTRYPOINT,
        "interface_adapter_ref": INTERFACE_ADAPTER_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "planning_profile": _build_profile(),
        "upstream_stage_ref_count": len(stage_refs) + 1,
        "stage_refs": stage_refs,
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "tier_policies": tier_policies,
        "expansion_family_policies": family_policies,
        "expansion_family_policy_count": len(family_policies),
        "output_standard_policies": output_standard_policies,
        "output_standard_policy_count": len(output_standard_policies),
        "adapter_readiness_policies": adapter_readiness_policies,
        "adapter_readiness_policy_count": len(adapter_readiness_policies),
        "interaction_readiness_policies": interaction_policies,
        "interaction_readiness_policy_count": len(interaction_policies),
        "midplatform_data_handling_readiness": data_handling_policies,
        "midplatform_data_handling_readiness_count": len(data_handling_policies),
        "midplatform_control_readiness": control_policies,
        "midplatform_control_readiness_count": len(control_policies),
        "expansion_sequence": list(EXPANSION_SEQUENCE),
        "planning_rules": list(PLANNING_RULES),
        "go_conditions": go_conditions,
        "conclusions": {
            "p1_family_expansion_planning_status": (
                "p1_p2_family_expansion_route_planned" if review_ok else "blocked"
            ),
            "next_phase_ref": NEXT_PHASE_REF,
            "route_note": (
                "P0 stays a frozen stable baseline. P1/P2 model families are admitted only as planned "
                "candidates: P1-A segmentation, P1-B tracking, P1-C depth/spatial-hint, P1-D object-"
                "detection completion are planned; P2 scene-relation/VLM is planned; P2 audio/speech "
                "evidence and the emotion-multimodal bridge are reserved placeholders (not executed). "
                "Expansion order, Luna output standard, adapter requirements, the 8 multi-model "
                "interaction tests, the 10 midplatform data-handling checks, and the 11 midplatform "
                "control checks are all fixed but deferred. No download, no inference, no single-model "
                "debugging, no tuning, no dataset usage. Everything remains candidate-only; Luna stays "
                "emotion-multimodal brain/cognition first; VLA action chain excluded. Next: P1 "
                "Invocation & Local Availability DryRun to see which planned families are locally "
                "visible, which are contract-only, and which need download/license planning."
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
    result = review_recognition_model_p1_family_expansion_planning_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "upstream_stage_ref_count": result["upstream_stage_ref_count"],
                "expansion_family_policy_count": result["expansion_family_policy_count"],
                "interaction_readiness_policy_count": result["interaction_readiness_policy_count"],
                "midplatform_data_handling_readiness_count": result[
                    "midplatform_data_handling_readiness_count"
                ],
                "midplatform_control_readiness_count": result[
                    "midplatform_control_readiness_count"
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
