# -*- coding: utf-8 -*-
"""P1 Model Test Lens Local Asset Import & Runner Bridge Planning — review v1."""

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
from capabilities.midplatform.model_test_lens.local_asset_import.local_asset_import_registry_v1 import (  # noqa: E402
    GOVERNANCE_CANONICAL_REFS,
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.midplatform.model_test_lens.local_asset_import.local_asset_import_types_v1 import (  # noqa: E402
    ADAPTER_REQUIRED_BEFORE_ENVELOPE_DISPLAY,
    ALL_GOVERNANCE_RULES,
    ASSET_TYPE_MODEL_MAP,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DATASET_DOWNLOAD_ALLOWED,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    EXTERNAL_URL_ALLOWED,
    FACT_WRITE_ALLOWED,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    IMAGE_IMPORT_ROUTE_STAGES,
    LIVE_CAMERA_ALLOWED,
    LOCAL_ASSETS_CANDIDATE_ONLY,
    LOCAL_ASSETS_NOT_FACT_SOURCE,
    LOCAL_ASSETS_NOT_RUNTIME_SOURCE,
    LOCAL_ASSET_IMPORT_ROOT_REL,
    LOCAL_ASSET_TYPES,
    LOCAL_STATIC_PAGE_ONLY,
    LUNA_CORE_PRINCIPLE,
    MICROPHONE_LIVE_CAPTURE_ALLOWED,
    MODEL_EXECUTION_ALLOWED,
    MODEL_TEST_LENS_LOCAL_ASSET_IMPORT_PLANNING,
    NEGATIVE_GUARDS,
    NEXT_PHASE_UI_PATCH,
    OUTPUT_ADAPTER_ALLOWED,
    PAGE_MAY_CREATE_JOB_REQUEST,
    PAGE_MAY_REGISTER_ASSETS,
    PAGE_MUST_NOT_EXECUTE_MODEL,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PLANNING_ONLY,
    PLANNING_PRINCIPLE_ZH,
    REAL_INFERENCE_ALLOWED,
    REGISTRY_MUTATION_ALLOWED,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    RUNNER_BRIDGE_PLANNING,
    RUNNER_BRIDGE_REQUIRES_OWNER_APPROVAL,
    RUNNER_BRIDGE_ROOT_REL,
    RUNTIME_ACTIVATION_ALLOWED,
    RUNTIME_EXECUTION_ALLOWED,
    SCHEMAS_LOCAL_ASSET_REL,
    SEMANTIC_LAYER_ALLOWED,
    SLAM_VIDEO_ROUTE_STAGES,
    SLAM_WITHOUT_GT_LIMITED_DIAGNOSTICS,
    SLAM_WITHOUT_GT_NO_ATE,
    SLAM_WITHOUT_GT_NO_GT_BENCHMARK_COMPARISON,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UI_PATCH_PLAN_ITEMS,
    ModelTestLensImportRouteRecord,
    ModelTestLensImportUiPatchPlanRecord,
    ModelTestLensLocalAssetImportPlanningProfile,
    NegativeLocalAssetImportPlanningGuard,
    P1MidplatformModelTestLensLocalAssetImportRunnerBridgePlanningDecision,
    NAVIGATION_ACTION_SPEECH_ALLOWED,
    to_dict,
)

_PKG = "capabilities/midplatform/model_test_lens"
STEP_FILES = (
    f"{_PKG}/local_asset_import/model_test_lens_local_asset_import_plan_v1.md",
    f"{_PKG}/local_asset_import/local_asset_import_types_v1.py",
    f"{_PKG}/local_asset_import/local_asset_import_registry_v1.py",
    f"{_PKG}/runner_bridge/model_test_lens_runner_bridge_plan_v1.md",
    f"{_PKG}/schemas/local_asset_import/local_test_asset_manifest_schema_v1.json",
    f"{_PKG}/schemas/local_asset_import/model_test_job_request_schema_v1.json",
    f"{_PKG}/schemas/local_asset_import/runner_bridge_request_schema_v1.json",
    f"{_PKG}/schemas/local_asset_import/asset_to_envelope_route_schema_v1.json",
    f"{_PKG}/review_model_test_lens_local_asset_import_runner_bridge_planning_v1.py",
)

SCHEMA_RELS = {
    "local_test_asset_manifest_schema_v1.json": "local_test_asset_manifest_schema_defined",
    "model_test_job_request_schema_v1.json": "model_test_job_request_schema_defined",
    "runner_bridge_request_schema_v1.json": "runner_bridge_request_schema_defined",
    "asset_to_envelope_route_schema_v1.json": "asset_to_envelope_route_schema_defined",
}

PROFILE_REF = "model_test_lens_local_asset_import_runner_bridge_planning_profile_v1"
DECISION_REF = "model_test_lens_local_asset_import_runner_bridge_planning_decision_v1"
REVIEW_FILENAME = "p1_midplatform_model_test_lens_local_asset_import_runner_bridge_planning_review_v1.json"
_BOARD_STANDIN_ROOT = _REPO_ROOT / "_tmp_eval_out" / "board_standin"


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
    / "p1_midplatform_model_test_lens_local_asset_import_runner_bridge_planning_v1_smoke_v0"
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


def _build_profile() -> Dict[str, Any]:
    return to_dict(
        ModelTestLensLocalAssetImportPlanningProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            planning_only=PLANNING_ONLY,
            model_test_lens_local_asset_import_planning=MODEL_TEST_LENS_LOCAL_ASSET_IMPORT_PLANNING,
            runner_bridge_planning=RUNNER_BRIDGE_PLANNING,
            local_static_page_only=LOCAL_STATIC_PAGE_ONLY,
            page_may_register_assets=PAGE_MAY_REGISTER_ASSETS,
            page_may_create_job_request=PAGE_MAY_CREATE_JOB_REQUEST,
            page_must_not_execute_model=PAGE_MUST_NOT_EXECUTE_MODEL,
            model_execution_allowed=MODEL_EXECUTION_ALLOWED,
            real_inference_allowed=REAL_INFERENCE_ALLOWED,
            runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
            output_adapter_allowed=OUTPUT_ADAPTER_ALLOWED,
            semantic_layer_allowed=SEMANTIC_LAYER_ALLOWED,
            fact_write_allowed=FACT_WRITE_ALLOWED,
            navigation_action_speech_allowed=NAVIGATION_ACTION_SPEECH_ALLOWED,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_model_test_lens_local_asset_import_runner_bridge_planning_v1(
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

    schema_flags: Dict[str, bool] = {}
    for fname, go_key in SCHEMA_RELS.items():
        ok = _resolve_file(f"{SCHEMAS_LOCAL_ASSET_REL}/{fname}") is not None
        schema_flags[go_key] = ok
        (passed_checks if ok else failed_checks).append(f"schema.{go_key}={'true' if ok else 'false'}")

    gov_refs_ok = all(_resolve_file(r) is not None for r in GOVERNANCE_CANONICAL_REFS)

    route_record = ModelTestLensImportRouteRecord(
        record_id="model_test_lens_import_route_record_v1",
        slam_video_import_route_defined=len(SLAM_VIDEO_ROUTE_STAGES) >= 8,
        image_import_route_defined=len(IMAGE_IMPORT_ROUTE_STAGES) >= 6,
        slam_route_stages=SLAM_VIDEO_ROUTE_STAGES,
        image_route_stages=IMAGE_IMPORT_ROUTE_STAGES,
        slam_without_gt_limited_diagnostics=SLAM_WITHOUT_GT_LIMITED_DIAGNOSTICS,
    )

    ui_patch = ModelTestLensImportUiPatchPlanRecord(
        record_id="model_test_lens_import_ui_patch_plan_v1",
        ui_patch_items=UI_PATCH_PLAN_ITEMS,
        planning_only_no_page_change_this_phase=True,
        retain_json_envelope_import=True,
        retain_mobile_sam_example=True,
        retain_slam_example=True,
        retain_insight_layer=True,
        retain_debug_mode=True,
    )

    invariant_state: Dict[str, bool] = {
        "page_must_not_execute_model": PAGE_MUST_NOT_EXECUTE_MODEL is True,
        "no_real_inference_on_page": REAL_INFERENCE_ALLOWED is False and MODEL_EXECUTION_ALLOWED is False,
        "no_slam_backend_on_page": MODEL_EXECUTION_ALLOWED is False,
        "no_live_camera_mic": LIVE_CAMERA_ALLOWED is False and MICROPHONE_LIVE_CAPTURE_ALLOWED is False,
        "no_external_url": EXTERNAL_URL_ALLOWED is False,
        "no_dataset_download": DATASET_DOWNLOAD_ALLOWED is False,
        "no_registry_mutation": REGISTRY_MUTATION_ALLOWED is False,
        "no_runtime_downstream": (
            RUNTIME_EXECUTION_ALLOWED is False
            and OUTPUT_ADAPTER_ALLOWED is False
            and SEMANTIC_LAYER_ALLOWED is False
            and FACT_WRITE_ALLOWED is False
            and NAVIGATION_ACTION_SPEECH_ALLOWED is False
        ),
        "local_assets_not_fact_or_runtime": (
            LOCAL_ASSETS_NOT_FACT_SOURCE is True and LOCAL_ASSETS_NOT_RUNTIME_SOURCE is True
        ),
        "slam_without_gt_no_ate": SLAM_WITHOUT_GT_NO_ATE is True,
        "runner_bridge_requires_owner_approval": RUNNER_BRIDGE_REQUIRES_OWNER_APPROVAL is True,
        "local_test_asset_manifest_schema_defined": schema_flags.get(
            "local_test_asset_manifest_schema_defined", False
        ),
        "model_test_job_request_schema_defined": schema_flags.get(
            "model_test_job_request_schema_defined", False
        ),
        "runner_bridge_request_schema_defined": schema_flags.get(
            "runner_bridge_request_schema_defined", False
        ),
        "test_board_record_required": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
        "test_artifact_protected": REQUIRED_TEST_BOARD_FIELDS_LOCAL.get("test_artifact_protected", False) is True,
    }

    negative_guards: List[NegativeLocalAssetImportPlanningGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeLocalAssetImportPlanningGuard(
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
        "model_test_lens_local_asset_import_runner_bridge_planning_profile_count_eq_1": True,
        **schema_flags,
        "slam_video_import_route_defined": route_record.slam_video_import_route_defined,
        "image_import_route_defined": route_record.image_import_route_defined,
        "page_may_register_assets": PAGE_MAY_REGISTER_ASSETS is True,
        "page_may_create_job_request": PAGE_MAY_CREATE_JOB_REQUEST is True,
        "page_must_not_execute_model": PAGE_MUST_NOT_EXECUTE_MODEL is True,
        "runner_bridge_requires_owner_approval": RUNNER_BRIDGE_REQUIRES_OWNER_APPROVAL is True,
        "adapter_required_before_envelope_display": ADAPTER_REQUIRED_BEFORE_ENVELOPE_DISPLAY is True,
        "local_assets_candidate_only": LOCAL_ASSETS_CANDIDATE_ONLY is True,
        "local_assets_not_fact_source": LOCAL_ASSETS_NOT_FACT_SOURCE is True,
        "local_assets_not_runtime_source": LOCAL_ASSETS_NOT_RUNTIME_SOURCE is True,
        "slam_without_gt_no_ate": SLAM_WITHOUT_GT_NO_ATE is True,
        "slam_without_gt_no_gt_benchmark_comparison": SLAM_WITHOUT_GT_NO_GT_BENCHMARK_COMPARISON is True,
        "model_execution_allowed_false": MODEL_EXECUTION_ALLOWED is False,
        "real_inference_allowed_false": REAL_INFERENCE_ALLOWED is False,
        "runtime_execution_allowed_false": RUNTIME_EXECUTION_ALLOWED is False,
        "output_adapter_allowed_false": OUTPUT_ADAPTER_ALLOWED is False,
        "semantic_layer_allowed_false": SEMANTIC_LAYER_ALLOWED is False,
        "fact_write_allowed_false": FACT_WRITE_ALLOWED is False,
        "navigation_action_speech_allowed_false": NAVIGATION_ACTION_SPEECH_ALLOWED is False,
        "registry_mutation_allowed_false": REGISTRY_MUTATION_ALLOWED is False,
        "external_url_allowed_false": EXTERNAL_URL_ALLOWED is False,
        "live_camera_allowed_false": LIVE_CAMERA_ALLOWED is False,
        "microphone_live_capture_allowed_false": MICROPHONE_LIVE_CAPTURE_ALLOWED is False,
        "planning_only": PLANNING_ONLY is True,
        "governance_standards_referenced": gov_refs_ok,
        "negative_guard_count_eq_16": negative_guard_count == 16,
        "negative_guard_passed_eq_16": negative_guard_passed == 16,
        **negative_guard_go,
        **{f"test_board.{k}": (v is True) for k, v in REQUIRED_TEST_BOARD_FIELDS_LOCAL.items()},
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
    }
    for key, ok in go_conditions.items():
        (passed_checks if ok else failed_checks).append(f"go.{key}={'true' if ok else 'false'}")

    blocker_count = len(failed_checks)
    final_decision = FINAL_DECISION_GO if blocker_count == 0 else FINAL_DECISION_BLOCKED

    test_board_total = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)
    decision = P1MidplatformModelTestLensLocalAssetImportRunnerBridgePlanningDecision(
        decision_ref=DECISION_REF,
        model_test_lens_local_asset_import_runner_bridge_planning_profile_count=1,
        local_test_asset_manifest_schema_defined=schema_flags.get("local_test_asset_manifest_schema_defined", False),
        model_test_job_request_schema_defined=schema_flags.get("model_test_job_request_schema_defined", False),
        runner_bridge_request_schema_defined=schema_flags.get("runner_bridge_request_schema_defined", False),
        asset_to_envelope_route_schema_defined=schema_flags.get("asset_to_envelope_route_schema_defined", False),
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    manifest_plan = {
        "schema_id": "local_test_asset_manifest_schema_v1",
        "schema_rel": f"{SCHEMAS_LOCAL_ASSET_REL}/local_test_asset_manifest_schema_v1.json",
        "asset_types": list(LOCAL_ASSET_TYPES),
        "asset_type_model_map": list(ASSET_TYPE_MODEL_MAP),
        "sha256_required": True,
        "candidate_only": True,
    }
    job_plan = {
        "schema_id": "model_test_job_request_schema_v1",
        "schema_rel": f"{SCHEMAS_LOCAL_ASSET_REL}/model_test_job_request_schema_v1.json",
        "requires_runner_execution": True,
        "requires_owner_approval": True,
    }
    bridge_plan = {
        "schema_id": "runner_bridge_request_schema_v1",
        "schema_rel": f"{SCHEMAS_LOCAL_ASSET_REL}/runner_bridge_request_schema_v1.json",
        "lens_may_not_execute_runner": True,
        "adapter_target_envelope": "model_test_result_envelope_v1",
    }
    slam_route_plan = {
        "route_id": "slam_video_import_route_v1",
        "stages": list(SLAM_VIDEO_ROUTE_STAGES),
        "without_gt_limited_diagnostics": list(SLAM_WITHOUT_GT_LIMITED_DIAGNOSTICS),
        "no_ate_without_gt": True,
        "no_gt_benchmark_comparison_without_gt": True,
    }
    image_route_plan = {
        "route_id": "image_import_route_v1",
        "stages": list(IMAGE_IMPORT_ROUTE_STAGES),
        "mobile_sam_via_segmentation_runner": True,
    }
    ui_patch_plan = asdict(ui_patch)

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Model Test Lens Local Asset Import & Runner Bridge Planning",
        "lifecycle_variant": "p1_midplatform_model_test_lens_local_asset_import_runner_bridge_planning",
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "planning_only": PLANNING_ONLY,
        "model_test_lens_local_asset_import_planning": MODEL_TEST_LENS_LOCAL_ASSET_IMPORT_PLANNING,
        "runner_bridge_planning": RUNNER_BRIDGE_PLANNING,
        "local_asset_import_root_rel": LOCAL_ASSET_IMPORT_ROOT_REL,
        "runner_bridge_root_rel": RUNNER_BRIDGE_ROOT_REL,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "model_test_lens_local_asset_import_runner_bridge_planning_profile": _build_profile(),
        "model_test_lens_local_asset_import_runner_bridge_planning_profile_count": 1,
        "model_test_lens_import_route_record": asdict(route_record),
        "model_test_lens_import_ui_patch_plan_record": ui_patch_plan,
        "stage_refs": stage_refs,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "final_decision": final_decision,
        "blocker_count": blocker_count,
        "recommended_next_phase": NEXT_PHASE_UI_PATCH,
        "conclusions": {
            "planning_status": "go" if blocker_count == 0 else "blocked",
            "transition_note": (
                "PLANNING ONLY. Page may register assets and create job requests; "
                "runner executes in separate phase; adapter required for envelope. "
                "Next: UI patch for import buttons without model execution."
            ),
        },
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
        "reviewed_at": _now(),
    }

    if write_file:
        review_path = out_root / REVIEW_FILENAME
        review_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(review_path)
        (out_root / "local_test_asset_manifest_schema_plan_v1.json").write_text(
            json.dumps(manifest_plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_root / "model_test_job_request_schema_plan_v1.json").write_text(
            json.dumps(job_plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_root / "runner_bridge_request_schema_plan_v1.json").write_text(
            json.dumps(bridge_plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_root / "slam_video_import_route_plan_v1.json").write_text(
            json.dumps(slam_route_plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_root / "image_import_route_plan_v1.json").write_text(
            json.dumps(image_route_plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_root / "model_test_lens_import_ui_patch_plan_v1.json").write_text(
            json.dumps(ui_patch_plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        result["output_root"] = str(out_root)

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
            "local_test_asset_manifest_record": {"record": manifest_plan},
            "model_test_job_request_record": {"record": job_plan},
            "runner_bridge_request_record": {"record": bridge_plan},
            "asset_import_route_record": {
                "record": {
                    "slam": slam_route_plan,
                    "image": image_route_plan,
                }
            },
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
            "page_must_not_execute_model": True,
            "candidate_output_only": True,
        }
        for rtype, payload in extra_payloads.items():
            out = {**common, **payload}
            (board_dir / f"{rtype}.json").write_text(
                json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
            )
        result["test_board_root"] = str(board_dir)

    return result


def main() -> int:
    result = review_model_test_lens_local_asset_import_runner_bridge_planning_v1()
    print(json.dumps(
        {
            "phase_id": result["phase_id"],
            "final_decision": result["final_decision"],
            "blocker_count": result["blocker_count"],
            "negative_guard_passed": result["negative_guard_passed"],
            "negative_guard_count": result["negative_guard_count"],
        },
        indent=2,
        ensure_ascii=False,
    ))
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
