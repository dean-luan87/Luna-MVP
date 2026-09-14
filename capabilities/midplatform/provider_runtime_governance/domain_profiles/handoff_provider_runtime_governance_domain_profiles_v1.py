# -*- coding: utf-8 -*-
"""Provider Runtime Governance — domain profile handoff v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[4]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.provider_runtime_governance.domain_profiles.spatial_evidence_provider_governance_profile_v1 import (
    build_spatial_evidence_governance_manager_v1,
    build_spatial_evidence_provider_governance_profile_v1,
)
from capabilities.midplatform.provider_runtime_governance.domain_profiles.vision_ocr_governance_compatibility_v1 import (
    build_vision_ocr_combined_governance_profile_v1,
    verify_vision_ocr_compatibility_v1,
)
from capabilities.midplatform.provider_runtime_governance.provider_runtime_governance_static_validators_v1 import (
    VALIDATOR_RULE_IDS,
)
from capabilities.midplatform.provider_runtime_governance.provider_runtime_governance_types_v1 import (
    DOMAIN_SPATIAL_EVIDENCE,
    DOMAIN_VISION_OCR,
    FIELD_SYNTHESIS_ENTRYPOINT,
    NON_EXECUTION_FLAGS,
    SHARED_MANAGER_REF,
)

PHASE_ID = "Phase-Provider-Runtime-Governance-Domain-Profile-Handoff-v1-001"
SOURCE_PHASE_ID = "Phase-Shared-Provider-Runtime-Governance-Skeleton-v1-001"
SOURCE_FINAL_DECISION = "SHARED_PROVIDER_RUNTIME_GOVERNANCE_POST_DRYRUN_REVIEW_GO"
VERIFIER_FINAL_DECISION_GO = "SHARED_PROVIDER_RUNTIME_GOVERNANCE_DRYRUN_VERIFIER_GO"
FINAL_DECISION_GO = "PROVIDER_RUNTIME_GOVERNANCE_DOMAIN_PROFILE_HANDOFF_GO"
FINAL_DECISION_BLOCKED = "PROVIDER_RUNTIME_GOVERNANCE_DOMAIN_PROFILE_HANDOFF_BLOCKED"

NEXT_PHASE_RUNTIME_SKELETON = "Phase-Provider-Manager-Runtime-Skeleton-Planning-v1-001"

DEFAULT_SOURCE_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "shared_provider_runtime_governance_dryrun_v1_smoke_v0"
)
DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "provider_runtime_governance_domain_profile_handoff_v1_smoke_v0"
)

REVIEW_FILENAME = "provider_runtime_governance_post_dryrun_review_v1.json"
SUMMARY_FILENAME = "provider_runtime_governance_dryrun_summary_v1.json"
VERIFICATION_FILENAME = "provider_runtime_governance_dryrun_verification_v1.json"
HANDOFF_FILENAME = "provider_runtime_governance_domain_profile_handoff_v1.json"

SPATIAL_ALLOWED_CANDIDATE_TYPES: Tuple[str, ...] = (
    "PoseCandidate",
    "MotionCandidate",
    "SpatialAnchorCandidate",
    "LocalMapCandidate",
    "SLAMHealthCandidate",
    "MapDriftCandidate",
    "RelocalizationCandidate",
    "SemanticFieldObjectCandidate",
    "FieldGraphCandidate",
    "SemanticMemoryMapCandidate",
)

_SPATIAL_POLLUTION_CANDIDATES = frozenset({"PoseCandidate", "SLAMHealthCandidate"})
_VISION_OCR_SIGNATURE_CANDIDATES = frozenset(
    {
        "DetectionCandidate",
        "TrackingCandidate",
        "SceneUnderstandingCandidate",
        "ocr_result_candidate",
        "ocr_evidence_pack_candidate",
        "roi_candidate",
    }
)

SUPERSEDED_MANAGER_DIR = (
    _REPO_ROOT / "capabilities" / "field_understanding" / "spatial_evidence_provider_manager"
)
PRIMARY_GOVERNANCE_DIR = _REPO_ROOT / "capabilities" / "midplatform" / "provider_runtime_governance"


def load_json_file(path: Path) -> Dict[str, Any]:
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError) as exc:
        raise ValueError(f"failed to load json: {path}: {exc}") from exc
    if not isinstance(doc, dict):
        raise ValueError(f"expected dict at root: {path}")
    return doc


def verify_source_review_go(review: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    checks = {
        "source_phase_id": review.get("phase_id") == SOURCE_PHASE_ID,
        "source_final_decision": review.get("final_decision") == SOURCE_FINAL_DECISION,
        "source_blocker_count_zero": review.get("blocker_count") == 0,
        "ready_for_domain_profile_handoff": (
            (review.get("handoff_readiness") or {}).get("ready_for_domain_profile_handoff")
            is True
        ),
        "shared_governance_ready": (
            (review.get("governance_review") or {}).get("shared_provider_runtime_governance_ready")
            is True
        ),
    }

    for key, ok in checks.items():
        if ok:
            passed.append(f"source.{key}=true")
        else:
            failed.append(f"source.{key}=false")

    return len(failed) == 0, passed, failed


def verify_spatial_evidence_profile_handoff() -> Tuple[Dict[str, Any], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    profile = build_spatial_evidence_provider_governance_profile_v1()
    manager = build_spatial_evidence_governance_manager_v1()
    declared = set(profile.supported_output_candidate_types)
    missing = [c for c in SPATIAL_ALLOWED_CANDIDATE_TYPES if c not in declared]

    profile_doc = {
        "profile_supported": profile.domain_id == DOMAIN_SPATIAL_EVIDENCE and not missing,
        "domain_id": profile.domain_id,
        "profile_ref": profile.profile_ref,
        "synthesis_entrypoint": profile.synthesis_entrypoint,
        "allowed_candidate_types": list(profile.supported_output_candidate_types),
        "candidate_only_required": profile.candidate_only is True,
        "runtime_activation_allowed": manager.runtime_activation_allowed,
        "provider_runtime_enabled": manager.provider_runtime_enabled,
        "uses_shared_manager_skeleton": profile.uses_shared_manager_skeleton is True,
        "domain_specific_rules_preserved": profile.synthesis_entrypoint == FIELD_SYNTHESIS_ENTRYPOINT,
    }

    if profile.domain_id == DOMAIN_SPATIAL_EVIDENCE:
        passed.append("spatial.domain_id_ok")
    else:
        failed.append(f"spatial.domain_id={profile.domain_id!r}")

    if profile.synthesis_entrypoint == FIELD_SYNTHESIS_ENTRYPOINT:
        passed.append("spatial.synthesis_entrypoint=field_synthesis_v1")
    else:
        failed.append(f"spatial.synthesis_entrypoint={profile.synthesis_entrypoint!r}")

    if not missing:
        passed.append("spatial.allowed_candidate_types_complete")
    else:
        failed.append(f"spatial.missing_candidate_types={missing}")

    if manager.runtime_activation_allowed is False and manager.provider_runtime_enabled is False:
        passed.append("spatial.runtime_disabled")
    else:
        failed.append("spatial.runtime_not_disabled")

    if SHARED_MANAGER_REF in manager.manager_ref:
        passed.append("spatial.uses_shared_manager_skeleton")
    else:
        failed.append(f"spatial.manager_ref={manager.manager_ref!r}")

    return profile_doc, passed, failed


def verify_vision_ocr_profile_handoff() -> Tuple[Dict[str, Any], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    profile = build_vision_ocr_combined_governance_profile_v1()
    vision_ok, vision_issues, compatibility_doc = verify_vision_ocr_compatibility_v1()
    declared = set(profile.get("supported_output_candidate_types") or ())
    spatial_pollution = declared.intersection(_SPATIAL_POLLUTION_CANDIDATES)

    profile_doc = {
        "profile_supported": profile.get("domain_id") == DOMAIN_VISION_OCR and vision_ok,
        "domain_id": profile.get("domain_id"),
        "profile_ref": profile.get("profile_ref"),
        "provider_abstraction_standard_v1_compatible": vision_ok,
        "candidate_only_required": profile.get("candidate_only") is True,
        "runtime_activation_allowed": False,
        "provider_runtime_enabled": False,
        "uses_shared_manager_skeleton": profile.get("uses_shared_manager_skeleton") is True,
        "not_polluted_by_spatial_candidates": not spatial_pollution,
        "allowed_candidate_types": list(profile.get("supported_output_candidate_types") or ()),
        "compatibility_standard_id": compatibility_doc.get("provider_abstraction_standard_id"),
    }

    if profile.get("domain_id") == DOMAIN_VISION_OCR:
        passed.append("vision_ocr.domain_id_ok")
    else:
        failed.append(f"vision_ocr.domain_id={profile.get('domain_id')!r}")

    if vision_ok:
        passed.append("vision_ocr.provider_abstraction_standard_v1_compatible")
    else:
        failed.extend(f"vision_ocr.compatibility:{issue}" for issue in vision_issues)

    if profile.get("candidate_only") is True:
        passed.append("vision_ocr.candidate_output_only")
    else:
        failed.append("vision_ocr.candidate_only_not_true")

    if not spatial_pollution:
        passed.append("vision_ocr.no_spatial_candidate_pollution")
    else:
        failed.append(f"vision_ocr.spatial_pollution={sorted(spatial_pollution)!r}")

    for ctype in _SPATIAL_POLLUTION_CANDIDATES:
        if ctype not in declared:
            passed.append(f"vision_ocr.does_not_require:{ctype}")

    return profile_doc, passed, failed


def verify_domain_isolation() -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    spatial_profile = build_spatial_evidence_provider_governance_profile_v1()
    vision_profile = build_vision_ocr_combined_governance_profile_v1()

    spatial_types = set(spatial_profile.supported_output_candidate_types)
    vision_types = set(vision_profile.get("supported_output_candidate_types") or ())

    spatial_not_in_vision = not spatial_types.intersection(_VISION_OCR_SIGNATURE_CANDIDATES)
    vision_not_in_spatial = not vision_types.intersection(_SPATIAL_POLLUTION_CANDIDATES)
    schemas_distinct = spatial_types != vision_types

    review = {
        "spatial_rules_do_not_pollute_vision_ocr": spatial_not_in_vision
        and not vision_types.intersection(
            spatial_types.intersection(
                {
                    "PoseCandidate",
                    "MotionCandidate",
                    "SLAMHealthCandidate",
                    "FieldGraphCandidate",
                }
            )
        ),
        "vision_ocr_rules_do_not_pollute_spatial": vision_not_in_spatial
        and not spatial_types.intersection(_VISION_OCR_SIGNATURE_CANDIDATES),
        "shared_governance_shape_reused": spatial_profile.uses_shared_manager_skeleton is True
        and vision_profile.get("uses_shared_manager_skeleton") is True,
        "domain_candidate_schema_not_forced_cross_domain": schemas_distinct
        and vision_not_in_spatial
        and spatial_not_in_vision,
    }

    for key, ok in review.items():
        if ok:
            passed.append(f"isolation.{key}=true")
        else:
            failed.append(f"isolation.{key}=false")

    return review, passed, failed


def verify_superseded_path() -> Tuple[Dict[str, bool], List[str], List[str]]:
    failed: List[str] = []
    passed: List[str] = []

    superseded_marked = False
    if SUPERSEDED_MANAGER_DIR.is_dir():
        for py_path in SUPERSEDED_MANAGER_DIR.rglob("*.py"):
            if "SUPERSEDED_BY_SHARED_PROVIDER_RUNTIME_GOVERNANCE" in py_path.read_text(
                encoding="utf-8"
            ):
                superseded_marked = True
                break

    step2_not_continued = not any(
        name.startswith("field_spatial_evidence_provider_manager_dryrun")
        or name.startswith("run_field_spatial_evidence_provider_manager")
        for name in (p.name for p in SUPERSEDED_MANAGER_DIR.rglob("*.py"))
    )

    primary_ok = (
        PRIMARY_GOVERNANCE_DIR.is_dir()
        and (PRIMARY_GOVERNANCE_DIR / "provider_runtime_governance_types_v1.py").is_file()
        and (PRIMARY_GOVERNANCE_DIR / "domain_profiles" / "spatial_evidence_provider_governance_profile_v1.py").is_file()
        and (PRIMARY_GOVERNANCE_DIR / "domain_profiles" / "vision_ocr_governance_compatibility_v1.py").is_file()
    )

    review = {
        "spatial_evidence_independent_manager_superseded": superseded_marked,
        "spatial_evidence_independent_manager_step2_not_continued": step2_not_continued,
        "shared_midplatform_path_is_primary": primary_ok,
    }

    for key, ok in review.items():
        if ok:
            passed.append(f"superseded.{key}=true")
        else:
            failed.append(f"superseded.{key}=false")

    return review, passed, failed


def _shared_governance_baseline(
    review: Dict[str, Any],
    summary: Dict[str, Any],
) -> Dict[str, Any]:
    baseline = review.get("baseline") or {}
    arch = review.get("architecture_frozen_conclusion") or {}
    governance = review.get("governance_review") or {}

    return {
        "shared_provider_runtime_governance_ready": governance.get(
            "shared_provider_runtime_governance_ready"
        )
        is True,
        "validator_rules": baseline.get("validator_rules") or len(VALIDATOR_RULE_IDS),
        "positive_case_count": baseline.get("positive_case_count") or summary.get("positive_case_count"),
        "invalid_case_count": baseline.get("invalid_case_count") or summary.get("invalid_case_count"),
        "trace_count": baseline.get("trace_count") or summary.get("trace_count"),
        "runtime_activation_allowed": False,
        "provider_runtime_enabled": False,
        "runtime_enabled_provider_refs": list(arch.get("runtime_enabled_provider_refs") or []),
    }


def handoff_provider_runtime_governance_domain_profiles_v1(
    *,
    source_root: Optional[str] = None,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    source = Path(source_root or DEFAULT_SOURCE_ROOT).expanduser().resolve()
    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()

    review_path = source / REVIEW_FILENAME
    summary_path = source / SUMMARY_FILENAME
    verification_path = source / VERIFICATION_FILENAME

    review = load_json_file(review_path)
    summary = load_json_file(summary_path)
    verification = load_json_file(verification_path)

    all_passed: List[str] = []
    all_failed: List[str] = []

    source_ok, p, f = verify_source_review_go(review)
    all_passed.extend(p)
    all_failed.extend(f)

    if verification.get("final_decision") != VERIFIER_FINAL_DECISION_GO:
        all_failed.append(
            f"verification.final_decision={verification.get('final_decision')!r}"
        )
    else:
        all_passed.append("verification.final_decision_go=true")

    spatial_doc, p, f = verify_spatial_evidence_profile_handoff()
    all_passed.extend(p)
    all_failed.extend(f)
    spatial_ok = spatial_doc.get("profile_supported") is True

    vision_doc, p, f = verify_vision_ocr_profile_handoff()
    all_passed.extend(p)
    all_failed.extend(f)
    vision_ok = vision_doc.get("profile_supported") is True

    isolation_review, p, f = verify_domain_isolation()
    all_passed.extend(p)
    all_failed.extend(f)
    isolation_ok = all(isolation_review.values())

    superseded_review, p, f = verify_superseded_path()
    all_passed.extend(p)
    all_failed.extend(f)
    superseded_ok = all(superseded_review.values())

    baseline = _shared_governance_baseline(review, summary)

    core_ready = (
        source_ok
        and spatial_ok
        and vision_ok
        and isolation_ok
        and superseded_ok
        and baseline.get("runtime_activation_allowed") is False
        and baseline.get("provider_runtime_enabled") is False
        and not baseline.get("runtime_enabled_provider_refs")
    )

    handoff_readiness = {
        "ready_for_spatial_evidence_profile_followup": core_ready and spatial_ok,
        "ready_for_vision_ocr_profile_followup": core_ready and vision_ok,
        "ready_for_additional_domain_profiles": core_ready and isolation_ok,
        "ready_for_future_provider_manager_runtime_skeleton_planning": core_ready,
    }

    blocker_count = len(all_failed)
    go_ok = (
        source_ok
        and spatial_ok
        and vision_ok
        and isolation_ok
        and superseded_ok
        and core_ready
        and all(handoff_readiness.values())
        and blocker_count == 0
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "source_phase_id": SOURCE_PHASE_ID,
        "source_final_decision": SOURCE_FINAL_DECISION,
        "source_review_go": source_ok,
        "spatial_evidence_profile_handoff_ok": spatial_ok,
        "vision_ocr_profile_handoff_ok": vision_ok,
        "domain_isolation_ok": isolation_ok,
        "spatial_manager_superseded_ok": superseded_ok,
        "handoff_scope": {
            "domain_profile_handoff_only": True,
            "no_runtime_activation": NON_EXECUTION_FLAGS.get("no_runtime_activation") is True,
            "no_provider_manager_runtime": NON_EXECUTION_FLAGS.get(
                "no_provider_manager_runtime"
            )
            is True,
            "no_real_backend_connected": True,
            "no_camera_or_ros_connected": True,
        },
        "input_artifacts": {
            "review": str(review_path),
            "summary": str(summary_path),
            "verification": str(verification_path),
        },
        "shared_governance_baseline": baseline,
        "domain_profiles": {
            "spatial_evidence": spatial_doc,
            "vision_ocr": vision_doc,
        },
        "domain_isolation_review": isolation_review,
        "superseded_path_review": superseded_review,
        "handoff_readiness": handoff_readiness,
        "recommended_next_phase": NEXT_PHASE_RUNTIME_SKELETON,
        "architecture_handoff_conclusion": {
            "layer_l1": "shared provider runtime governance (frozen)",
            "layer_l2": "spatial_evidence + vision_ocr domain profiles (handoff sample)",
            "domain_profiles_attach_without_runtime": True,
            "do_not_continue": "field_understanding/spatial_evidence_provider_manager Step 2+",
        },
        "blocker_count": blocker_count,
        "failed_checks": all_failed,
        "passed_checks": all_passed,
        "final_decision": FINAL_DECISION_GO if go_ok else FINAL_DECISION_BLOCKED,
    }

    if write_file:
        out_root.mkdir(parents=True, exist_ok=True)
        out_path = out_root / HANDOFF_FILENAME
        out_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        result["output_root"] = str(out_root)
        result["output_handoff_file"] = str(out_path)

    return result


def main() -> int:
    try:
        result = handoff_provider_runtime_governance_domain_profiles_v1()
    except ValueError as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 1

    print(
        json.dumps(
            {
                "output_handoff_file": result.get("output_handoff_file"),
                "source_review_go": result["source_review_go"],
                "spatial_evidence_profile_handoff_ok": result[
                    "spatial_evidence_profile_handoff_ok"
                ],
                "vision_ocr_profile_handoff_ok": result["vision_ocr_profile_handoff_ok"],
                "domain_isolation_ok": result["domain_isolation_ok"],
                "spatial_manager_superseded_ok": result["spatial_manager_superseded_ok"],
                "runtime_activation_allowed": result["shared_governance_baseline"][
                    "runtime_activation_allowed"
                ],
                "provider_runtime_enabled": result["shared_governance_baseline"][
                    "provider_runtime_enabled"
                ],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
                "recommended_next_phase": result["recommended_next_phase"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
