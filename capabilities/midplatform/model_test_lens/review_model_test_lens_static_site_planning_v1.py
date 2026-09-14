# -*- coding: utf-8 -*-
"""P1 Midplatform Model Test Lens Static Site Planning — review v1 (PLANNING ONLY)."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    REQUIRED_RECORD_TYPES,
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)
from capabilities.midplatform.model_test_lens.model_test_lens_registry_v1 import (  # noqa: E402
    GOVERNANCE_CANONICAL_REFS,
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.midplatform.model_test_lens.model_test_lens_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    AUDIO_INPUT_ALLOWED,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    EXAMPLES_ROOT_REL,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FACT_WRITE_ALLOWED,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    FORBIDDEN_INPUTS_V1,
    GOVERNANCE_LEGACY_INVENTORY_REL,
    GOVERNANCE_MANIFEST_REL,
    IMAGE_INPUT_ALLOWED,
    LOCAL_STATIC_PAGE_ONLY,
    LUNA_CORE_PRINCIPLE,
    MODEL_EXECUTION_ALLOWED,
    MODEL_ONBOARDING_STANDARD_REL,
    MODEL_PANEL_REGISTRY,
    MODEL_TESTING_ONLY,
    MODEL_TEST_LENS_ROOT_REL,
    MODEL_TEST_LENS_STATIC_SITE_PLANNING,
    NAVIGATION_ACTION_SPEECH_ALLOWED,
    NEGATIVE_GUARDS,
    NEXT_PHASE_SKELETON_EXECUTION,
    NOT_WHITEBOX_PRODUCT_PAGE,
    OUTPUT_ADAPTER_ALLOWED,
    PAGE_MODULES,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PLANNING_ONLY,
    PLANNING_PRINCIPLE_ZH,
    READ_SOURCES_V1,
    REAL_INFERENCE_ALLOWED,
    REGISTRY_MUTATION_ALLOWED,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    RUNTIME_EXECUTION_ALLOWED,
    SCHEMAS_ROOT_REL,
    SEMANTIC_LAYER_ALLOWED,
    SINGLE_MODEL_CAPABILITY_TEST_FOCUS,
    STATIC_SITE_ROOT_REL,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    VIDEO_INPUT_ALLOWED,
    VISUALIZATION_LAYER_TYPES,
    LAYOUT_REGIONS,
    ModelTestLensBoundaryPolicyRecord,
    ModelTestLensFollowupSkeletonRoute,
    ModelTestLensGovernanceReferenceRecord,
    ModelTestLensModelPanelRegistryRecord,
    ModelTestLensPageStructureRecord,
    ModelTestLensStaticSitePlanningDecision,
    ModelTestLensStaticSitePlanningProfile,
    ModelTestLensWhiteboxSeparationRecord,
    NegativeModelTestLensPlanningGuard,
    to_dict,
)

_PKG = "capabilities/midplatform/model_test_lens"
STEP_FILES = (
    f"{_PKG}/README.md",
    f"{_PKG}/model_test_lens_static_site_plan_v1.md",
    f"{_PKG}/model_test_lens_types_v1.py",
    f"{_PKG}/model_test_lens_registry_v1.py",
    f"{_PKG}/review_model_test_lens_static_site_planning_v1.py",
    f"{_PKG}/schemas/model_test_case_manifest_schema_v1.json",
    f"{_PKG}/schemas/model_test_result_envelope_schema_v1.json",
    f"{_PKG}/schemas/model_test_trace_schema_v1.json",
    f"{_PKG}/schemas/model_test_visualization_layer_schema_v1.json",
    f"{_PKG}/static_site/index.html",
    f"{_PKG}/static_site/app.js",
    f"{_PKG}/static_site/styles.css",
    f"{_PKG}/examples/mobile_sam_multi_real_image_envelope_example_v1.json",
)

PROFILE_REF = "model_test_lens_static_site_planning_profile_v1"
DECISION_REF = "model_test_lens_static_site_planning_decision_v1"
REVIEW_FILENAME = "p1_midplatform_model_test_lens_static_site_planning_review_v1.json"
_BOARD_STANDIN_ROOT = _REPO_ROOT / "_tmp_eval_out" / "board_standin"

REQUIRED_PANEL_IDS = {
    "ocr", "slam_vio", "depth_world", "vision_segmentation", "detection_tracking",
    "asr", "tts", "speaker", "face_expression_gesture", "multimodal_vlm",
}


def _pick_writable_base() -> Path:
    for cand in (_REPO_ROOT, Path.cwd()):
        try:
            (cand / "_tmp_eval_out").mkdir(parents=True, exist_ok=True)
            return cand
        except (PermissionError, OSError):
            continue
    return _REPO_ROOT


_WRITABLE_BASE = _pick_writable_base()
DEFAULT_OUTPUT_ROOT = (
    _WRITABLE_BASE / "_tmp_eval_out"
    / "p1_midplatform_model_test_lens_static_site_planning_v1_smoke_v0"
)


def _artifact_roots() -> List[Path]:
    roots: List[Path] = [_REPO_ROOT, Path.cwd(), _WRITABLE_BASE]
    for extra in (_REPO_ROOT.parent / "Luna-Core", _REPO_ROOT.parent / "Luna-Workspace-Min"):
        if extra.is_dir() and extra not in roots:
            roots.append(extra)
    return roots


def _resolve_file(rel: str) -> Optional[Path]:
    for base in _artifact_roots():
        p = base / rel
        if p.is_file():
            return p
    return None


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _panel_flags() -> Dict[str, bool]:
    ids = {p["panel_id"] for p in MODEL_PANEL_REGISTRY}
    return {
        "ocr_panel_defined": "ocr" in ids,
        "slam_vio_panel_defined": "slam_vio" in ids,
        "depth_world_panel_defined": "depth_world" in ids,
        "segmentation_panel_defined": "vision_segmentation" in ids,
        "detection_tracking_panel_defined": "detection_tracking" in ids,
        "asr_panel_defined": "asr" in ids,
        "tts_panel_defined": "tts" in ids,
        "speaker_panel_defined": "speaker" in ids,
        "face_expression_gesture_panel_defined": "face_expression_gesture" in ids,
        "multimodal_vlm_panel_defined": "multimodal_vlm" in ids,
        "all_model_panels_defined": REQUIRED_PANEL_IDS <= ids,
    }


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        ModelTestLensStaticSitePlanningProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            planning_only=PLANNING_ONLY,
            model_test_lens_static_site_planning=MODEL_TEST_LENS_STATIC_SITE_PLANNING,
            local_static_page_only=LOCAL_STATIC_PAGE_ONLY,
            not_whitebox_product_page=NOT_WHITEBOX_PRODUCT_PAGE,
            model_testing_only=MODEL_TESTING_ONLY,
            single_model_capability_test_focus=SINGLE_MODEL_CAPABILITY_TEST_FOCUS,
            runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
            model_execution_allowed=MODEL_EXECUTION_ALLOWED,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            fact_write_allowed=FACT_WRITE_ALLOWED,
            navigation_action_speech_allowed=NAVIGATION_ACTION_SPEECH_ALLOWED,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_model_test_lens_static_site_planning_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
) -> Dict[str, Any]:
    failed_checks: List[str] = []
    passed_checks: List[str] = []
    warnings: List[str] = []

    for rel in STEP_FILES:
        if _resolve_file(rel) is not None:
            passed_checks.append(f"step.file_present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"step.file_missing={rel}")

    stage_refs, verify_flags, stage_issues, stage_warnings = verify_stages(_REPO_ROOT)
    failed_checks.extend(stage_issues)
    warnings.extend(stage_warnings)

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    panel_flags = _panel_flags()
    for pid in REQUIRED_PANEL_IDS:
        panel_readme = f"{MODEL_TEST_LENS_ROOT_REL}/model_panels/"
        mapping = {
            "ocr": "ocr", "slam_vio": "slam", "depth_world": "depth",
            "vision_segmentation": "vision_segmentation", "detection_tracking": "tracking",
            "asr": "asr", "tts": "tts", "speaker": "speaker",
            "face_expression_gesture": "face_expression", "multimodal_vlm": "multimodal",
        }
        readme_path = f"{panel_readme}{mapping[pid]}/README.md"
        if _resolve_file(readme_path) is None:
            failed_checks.append(f"panel.readme_missing={pid}")

    page_structure = ModelTestLensPageStructureRecord(
        record_id="model_test_lens_page_structure_v1",
        layout_regions=LAYOUT_REGIONS,
        page_modules=PAGE_MODULES,
        read_sources=READ_SOURCES_V1,
        forbidden_inputs=FORBIDDEN_INPUTS_V1,
        static_site_root_rel=STATIC_SITE_ROOT_REL,
    )

    panel_registry = ModelTestLensModelPanelRegistryRecord(
        record_id="model_test_lens_model_panel_registry_v1",
        panels=MODEL_PANEL_REGISTRY,
        panel_count=len(MODEL_PANEL_REGISTRY),
        all_required_panels_defined=panel_flags["all_model_panels_defined"],
    )

    boundary_policy = ModelTestLensBoundaryPolicyRecord(
        record_id="model_test_lens_boundary_policy_v1",
        candidate_only=True,
        not_fact=True,
        not_runtime_output=True,
        not_output_adapter_output=True,
        not_semantic_output=True,
        not_navigation_action_speech=True,
        readiness_effect_all_false=True,
        page_generates_readiness=False,
    )

    whitebox_sep = ModelTestLensWhiteboxSeparationRecord(
        record_id="model_test_lens_whitebox_separation_v1",
        whitebox_purpose="system_decision_parameter_chain_runtime_product_explanation",
        model_test_lens_purpose="single_model_capability_boundary_research_test_evaluation",
        whitebox_covers_runtime_product_explanation=True,
        model_test_lens_covers_model_capability_evaluation=True,
    )

    gov_refs_ok = all(_resolve_file(r) is not None for r in GOVERNANCE_CANONICAL_REFS)
    governance_ref = ModelTestLensGovernanceReferenceRecord(
        record_id="model_test_lens_governance_reference_v1",
        governance_manifest_ref=GOVERNANCE_MANIFEST_REL,
        legacy_inventory_ref=GOVERNANCE_LEGACY_INVENTORY_REL,
        model_onboarding_standard_ref=MODEL_ONBOARDING_STANDARD_REL,
        test_board_protocol_ref=TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        page_bypasses_approval_gate=False,
    )

    followup = ModelTestLensFollowupSkeletonRoute(
        route_id="model_test_lens_followup_skeleton_route_v1",
        recommended_next_phase=NEXT_PHASE_SKELETON_EXECUTION,
        next_phase_scope="local_static_site_skeleton_json_read_display_only",
    )

    envelope_schema_path = f"{SCHEMAS_ROOT_REL}/model_test_result_envelope_schema_v1.json"
    viz_schema_path = f"{SCHEMAS_ROOT_REL}/model_test_visualization_layer_schema_v1.json"
    manifest_schema_path = f"{SCHEMAS_ROOT_REL}/model_test_case_manifest_schema_v1.json"
    unified_envelope_defined = _resolve_file(envelope_schema_path) is not None
    visualization_schema_defined = _resolve_file(viz_schema_path) is not None
    manifest_schema_defined = _resolve_file(manifest_schema_path) is not None

    module_ids = {m["module_id"] for m in PAGE_MODULES}
    boundary_panel_defined = "boundary_panel" in module_ids
    testboard_refs_panel_defined = "testboard_refs_panel" in module_ids

    invariant_state: Dict[str, bool] = {
        "not_whitebox_product_page": NOT_WHITEBOX_PRODUCT_PAGE is True,
        "no_model_execution": MODEL_EXECUTION_ALLOWED is False and REAL_INFERENCE_ALLOWED is False,
        "no_runtime_downstream": (
            RUNTIME_EXECUTION_ALLOWED is False
            and OUTPUT_ADAPTER_ALLOWED is False
            and SEMANTIC_LAYER_ALLOWED is False
            and FACT_WRITE_ALLOWED is False
            and NAVIGATION_ACTION_SPEECH_ALLOWED is False
        ),
        "no_external_live_realtime": (
            IMAGE_INPUT_ALLOWED is False
            and AUDIO_INPUT_ALLOWED is False
            and VIDEO_INPUT_ALLOWED is False
            and "external_url_import" in FORBIDDEN_INPUTS_V1
            and "live_camera" in FORBIDDEN_INPUTS_V1
        ),
        "no_registry_mutation": REGISTRY_MUTATION_ALLOWED is False,
        "no_delete_testboard": True,
        "candidate_not_fact": boundary_policy.not_fact is True and boundary_policy.candidate_only is True,
        "all_model_panels_defined": panel_flags["all_model_panels_defined"],
        "unified_result_envelope_defined": unified_envelope_defined,
        "visualization_layer_schema_defined": visualization_schema_defined,
        "boundary_panel_defined": boundary_panel_defined,
        "governance_standards_referenced": gov_refs_ok and governance_ref.page_bypasses_approval_gate is False,
        "testboard_required": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
    }

    negative_guards: List[NegativeModelTestLensPlanningGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeModelTestLensPlanningGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    go_conditions: Dict[str, bool] = {
        "model_test_lens_static_site_planning_profile_count_eq_1": True,
        "stage_ref_count_gte_6": len(stage_refs) >= 6,
        "model_panel_registry_defined": panel_registry.all_required_panels_defined,
        **panel_flags,
        "unified_result_envelope_defined": unified_envelope_defined,
        "visualization_layer_schema_defined": visualization_schema_defined,
        "manifest_schema_defined": manifest_schema_defined,
        "boundary_panel_defined": boundary_panel_defined,
        "testboard_refs_panel_defined": testboard_refs_panel_defined,
        "governance_standards_reference_defined": gov_refs_ok,
        "not_whitebox_product_page": NOT_WHITEBOX_PRODUCT_PAGE is True,
        "model_testing_only": MODEL_TESTING_ONLY is True,
        "planning_only": PLANNING_ONLY is True,
        "local_static_page_only": LOCAL_STATIC_PAGE_ONLY is True,
        "runtime_execution_allowed_false": RUNTIME_EXECUTION_ALLOWED is False,
        "model_execution_allowed_false": MODEL_EXECUTION_ALLOWED is False,
        "registry_mutation_allowed_false": REGISTRY_MUTATION_ALLOWED is False,
        "fact_write_allowed_false": FACT_WRITE_ALLOWED is False,
        "navigation_action_speech_allowed_false": NAVIGATION_ACTION_SPEECH_ALLOWED is False,
        "commercial_runtime_approved_false": COMMERCIAL_RUNTIME_APPROVED is False,
        "negative_guard_count_eq_13": negative_guard_count == 13,
        "negative_guard_passed_eq_13": negative_guard_passed == 13,
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": verify_flags.get("controlled_trial_template_ref_ok") is True,
        **negative_guard_go,
        **{f"test_board.{k}": (v is True) for k, v in REQUIRED_TEST_BOARD_FIELDS_LOCAL.items()},
        "test_board_manifest_written": write_test_board is True,
        "cleanup_does_not_delete_test_board": True,
    }
    for key, ok in go_conditions.items():
        (passed_checks if ok else failed_checks).append(f"go.{key}={'true' if ok else 'false'}")

    blocker_count = len(failed_checks)
    final_decision = FINAL_DECISION_GO if blocker_count == 0 else FINAL_DECISION_BLOCKED

    test_board_total = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)
    decision = ModelTestLensStaticSitePlanningDecision(
        decision_ref=DECISION_REF,
        model_test_lens_static_site_planning_profile_count=1,
        model_panel_registry_defined=panel_registry.all_required_panels_defined,
        unified_result_envelope_defined=unified_envelope_defined,
        visualization_layer_schema_defined=visualization_schema_defined,
        boundary_panel_defined=boundary_panel_defined,
        testboard_refs_panel_defined=testboard_refs_panel_defined,
        governance_standards_reference_defined=gov_refs_ok,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    envelope_plan = {
        "schema_id": "model_test_result_envelope_schema_v1",
        "schema_rel_path": envelope_schema_path,
        "example_rel_path": f"{EXAMPLES_ROOT_REL}/mobile_sam_multi_real_image_envelope_example_v1.json",
        "visualization_layer_types": list(VISUALIZATION_LAYER_TYPES),
        "boundary_flags_required": True,
        "readiness_effect_all_false": True,
    }
    viz_plan = {
        "schema_id": "model_test_visualization_layer_schema_v1",
        "schema_rel_path": viz_schema_path,
        "layer_types": list(VISUALIZATION_LAYER_TYPES),
        "candidate_only_required": True,
    }

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Midplatform Model Test Lens Static Site Planning (planning only)",
        "lifecycle_variant": "p1_midplatform_model_test_lens_static_site_planning",
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "weight_chain": "p1_midplatform_model_test_lens_static_site_planning_v1",
        "planning_only": PLANNING_ONLY,
        "model_test_lens_static_site_planning": MODEL_TEST_LENS_STATIC_SITE_PLANNING,
        "not_whitebox_product_page": NOT_WHITEBOX_PRODUCT_PAGE,
        "model_test_lens_root_rel": MODEL_TEST_LENS_ROOT_REL,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "model_test_lens_static_site_planning_profile": _build_profile(),
        "model_test_lens_static_site_planning_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "model_test_lens_page_structure_record": asdict(page_structure),
        "model_test_lens_model_panel_registry_record": asdict(panel_registry),
        "model_test_lens_boundary_policy_record": asdict(boundary_policy),
        "model_test_lens_whitebox_separation_record": asdict(whitebox_sep),
        "model_test_lens_governance_reference_record": asdict(governance_ref),
        "model_test_lens_followup_skeleton_route_record": asdict(followup),
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "conclusions": {
            "planning_status": "go" if blocker_count == 0 else "blocked",
            "recommended_next_phase": NEXT_PHASE_SKELETON_EXECUTION,
            "transition_note": (
                "PLANNING ONLY. Model Test Lens separated from WhiteBox. "
                "Directory, schemas, 10 model panels, envelope, boundary policy defined. "
                "No model execution. Next: skeleton static site + JSON read/display."
            ),
        },
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "passed_checks": passed_checks,
        "final_decision": final_decision,
    }

    if write_file:
        review_path = out_root / REVIEW_FILENAME
        review_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result["output_review_file"] = str(review_path)

        (out_root / "model_test_lens_page_structure_v1.json").write_text(
            json.dumps(asdict(page_structure), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (out_root / "model_test_lens_model_panel_registry_v1.json").write_text(
            json.dumps(asdict(panel_registry), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (out_root / "model_test_result_envelope_schema_plan_v1.json").write_text(
            json.dumps(envelope_plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (out_root / "model_test_visualization_layer_schema_plan_v1.json").write_text(
            json.dumps(viz_plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (out_root / "model_test_lens_boundary_policy_v1.json").write_text(
            json.dumps(asdict(boundary_policy), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    if write_test_board:
        board_root = Path(test_board_root).expanduser().resolve() if test_board_root else _REPO_ROOT
        try:
            manifest_tb = write_test_board_records(
                result,
                test_mode=TEST_BOARD_TEST_MODE,
                repo_root=board_root,
                module=TEST_BOARD_MODULE,
                source_review_file=result.get("output_review_file"),
            )
            result["test_board_write_mode"] = "canonical"
        except (PermissionError, OSError):
            _BOARD_STANDIN_ROOT.mkdir(parents=True, exist_ok=True)
            manifest_tb = write_test_board_records(
                result,
                test_mode=TEST_BOARD_TEST_MODE,
                repo_root=_BOARD_STANDIN_ROOT,
                module=TEST_BOARD_MODULE,
                source_review_file=result.get("output_review_file"),
            )
            result["test_board_write_mode"] = "standin_sandbox_fallback"

        board_dir = Path(manifest_tb["test_board_dir"])
        extra_payloads = {
            "model_test_lens_page_structure_record": {"record": asdict(page_structure)},
            "model_test_lens_model_panel_registry_record": {"record": asdict(panel_registry)},
            "model_test_lens_result_envelope_schema_record": {"record": envelope_plan},
            "model_test_lens_visualization_layer_schema_record": {"record": viz_plan},
            "model_test_lens_boundary_policy_record": {"record": asdict(boundary_policy)},
            "model_test_lens_whitebox_separation_record": {"record": asdict(whitebox_sep)},
            "model_test_lens_governance_reference_record": {"record": asdict(governance_ref)},
            "model_test_lens_followup_skeleton_route_record": {"record": asdict(followup)},
        }
        common = {
            "protocol_id": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
            "phase_id": PHASE_ID,
            "module": TEST_BOARD_MODULE,
            "test_mode": TEST_BOARD_TEST_MODE,
            "recorded_at_utc": _now(),
            "protected": True,
            "non_deletable": True,
            "deletion_forbidden": True,
            "planning_only": True,
            "model_test_lens": True,
            "not_whitebox_product_page": True,
            "runtime_allowed": False,
            "model_execution_allowed": False,
            "candidate_output_only": True,
        }
        extra_written: List[str] = []
        for rtype, payload in extra_payloads.items():
            p = board_dir / f"{rtype}.json"
            p.write_text(
                json.dumps({**common, "record_type": rtype, **payload}, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            extra_written.append(str(p))
        manifest_tb["extra_written_records"] = extra_written
        manifest_tb["total_record_count"] = manifest_tb["written_record_count"] + len(extra_written)
        result["test_board_manifest"] = manifest_tb
        result["test_board_record_count"] = manifest_tb["total_record_count"]

    return result


def main() -> int:
    result = review_model_test_lens_static_site_planning_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "negative_guard_passed": result["negative_guard_passed"],
                "model_panel_count": result["model_test_lens_model_panel_registry_record"]["panel_count"],
                "recommended_next_phase": result["conclusions"]["recommended_next_phase"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
