# -*- coding: utf-8 -*-
"""P1 Model Test Lens Local Runner Bridge Service — planning review v1."""

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
from capabilities.midplatform.model_test_lens.local_runner_bridge.local_runner_bridge_registry_v1 import (  # noqa: E402
    GOVERNANCE_CANONICAL_REFS,
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.midplatform.model_test_lens.local_runner_bridge.local_runner_bridge_types_v1 import (  # noqa: E402
    ADAPTER_REQUIRED_BEFORE_UI_DISPLAY,
    ALL_GOVERNANCE_RULES,
    API_ENDPOINTS,
    ASSET_STORE_REL,
    CANDIDATE_ONLY_BOUNDARY_DEFINED,
    CAPABILITY_IDS,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DATASET_DOWNLOAD_ALLOWED,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    EXTERNAL_NETWORK_ALLOWED,
    FACT_WRITE_ALLOWED,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    JOB_LIFECYCLE_STATES,
    LIVE_CAMERA_ALLOWED,
    LIVE_MICROPHONE_ALLOWED,
    LOCALHOST_ONLY,
    LOCAL_RUNNER_BRIDGE_ROOT_REL,
    LOCAL_RUNNER_BRIDGE_SERVICE_PLANNING,
    LUNA_CORE_PRINCIPLE,
    MOBILESAM_IMAGE_RUNNER_ROUTE_STAGES,
    MODEL_TEST_LENS_BACKEND_BRIDGE,
    NAVIGATION_ACTION_SPEECH_ALLOWED,
    NEGATIVE_GUARDS,
    NEXT_PHASE_SKELETON_EXECUTION,
    NOT_COMMERCIAL_BACKEND,
    NOT_OUTPUT_ADAPTER,
    NOT_RUNTIME,
    PAGE_MAY_SUBMIT_LOCAL_JOB,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PLANNING_ONLY,
    PLANNING_PRINCIPLE_ZH,
    REGISTRY_MUTATION_ALLOWED,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    RUNNER_REGISTRY,
    SCHEMAS_LOCAL_RUNNER_BRIDGE_REL,
    SEMANTIC_LAYER_ALLOWED,
    SERVICE_BIND_ADDRESS,
    SERVICE_HOST,
    SERVICE_MAY_EXECUTE_MODEL_AFTER_APPROVAL,
    SERVICE_MUST_WRITE_TESTBOARD,
    SERVICE_PORT,
    SLAM_VIDEO_RUNNER_ROUTE_STAGES,
    SLAM_WITHOUT_GT_LIMITED_DIAGNOSTICS,
    SLAM_WITHOUT_GT_NO_ATE,
    SLAM_WITHOUT_GT_NO_GT_BENCHMARK_COMPARISON,
    TARGET_CHAIN_REF,
    TESTBOARD_REQUIRED_FOR_EACH_JOB,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UI_HOST,
    UI_INTEGRATION_PATCH_ITEMS,
    LocalRunnerBridgeApiPlanRecord,
    LocalRunnerBridgeServicePlanningProfile,
    LocalRunnerJobLifecycleRecord,
    LocalRunnerRegistryPlanRecord,
    MobileSamLocalImageRunnerRouteRecord,
    NegativeLocalRunnerBridgeServicePlanningGuard,
    P1MidplatformModelTestLensLocalRunnerBridgeServicePlanningDecision,
    SlamLocalVideoRunnerRouteRecord,
    to_dict,
)

_PKG = "capabilities/midplatform/model_test_lens"
STEP_FILES = (
    f"{_PKG}/local_runner_bridge/local_runner_bridge_service_plan_v1.md",
    f"{_PKG}/local_runner_bridge/local_runner_bridge_types_v1.py",
    f"{_PKG}/local_runner_bridge/local_runner_bridge_registry_v1.py",
    f"{_PKG}/local_runner_bridge/schemas/local_runner_bridge_api_schema_v1.json",
    f"{_PKG}/local_runner_bridge/schemas/local_runner_job_schema_v1.json",
    f"{_PKG}/local_runner_bridge/schemas/local_runner_status_schema_v1.json",
    f"{_PKG}/local_runner_bridge/schemas/local_runner_result_schema_v1.json",
    f"{_PKG}/review_model_test_lens_local_runner_bridge_service_planning_v1.py",
)

SCHEMA_RELS = {
    "local_runner_bridge_api_schema_v1.json": "api_schema_defined",
    "local_runner_job_schema_v1.json": "job_schema_defined",
    "local_runner_status_schema_v1.json": "status_schema_defined",
    "local_runner_result_schema_v1.json": "result_schema_defined",
}

PROFILE_REF = "local_runner_bridge_service_planning_profile_v1"
DECISION_REF = "local_runner_bridge_service_planning_decision_v1"
REVIEW_FILENAME = "p1_midplatform_model_test_lens_local_runner_bridge_service_planning_review_v1.json"
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
    / "p1_midplatform_model_test_lens_local_runner_bridge_service_planning_v1_smoke_v0"
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
        LocalRunnerBridgeServicePlanningProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            planning_only=PLANNING_ONLY,
            local_runner_bridge_service_planning=LOCAL_RUNNER_BRIDGE_SERVICE_PLANNING,
            localhost_only=LOCALHOST_ONLY,
            model_test_lens_backend_bridge=MODEL_TEST_LENS_BACKEND_BRIDGE,
            not_runtime=NOT_RUNTIME,
            not_output_adapter=NOT_OUTPUT_ADAPTER,
            not_commercial_backend=NOT_COMMERCIAL_BACKEND,
            page_may_submit_local_job=PAGE_MAY_SUBMIT_LOCAL_JOB,
            service_may_execute_model_after_approval=SERVICE_MAY_EXECUTE_MODEL_AFTER_APPROVAL,
            service_must_write_testboard=SERVICE_MUST_WRITE_TESTBOARD,
            adapter_required_before_ui_display=ADAPTER_REQUIRED_BEFORE_UI_DISPLAY,
            registry_mutation_allowed=REGISTRY_MUTATION_ALLOWED,
            semantic_layer_allowed=SEMANTIC_LAYER_ALLOWED,
            fact_write_allowed=FACT_WRITE_ALLOWED,
            navigation_action_speech_allowed=NAVIGATION_ACTION_SPEECH_ALLOWED,
            external_network_allowed=EXTERNAL_NETWORK_ALLOWED,
            live_camera_allowed=LIVE_CAMERA_ALLOWED,
            live_microphone_allowed=LIVE_MICROPHONE_ALLOWED,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_model_test_lens_local_runner_bridge_service_planning_v1(
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
    api_schema_defined = False
    for fname, go_key in SCHEMA_RELS.items():
        ok = _resolve_file(f"{SCHEMAS_LOCAL_RUNNER_BRIDGE_REL}/{fname}") is not None
        schema_flags[go_key] = ok
        if fname == "local_runner_bridge_api_schema_v1.json":
            api_schema_defined = ok
        (passed_checks if ok else failed_checks).append(f"schema.{go_key}={'true' if ok else 'false'}")

    gov_refs_ok = all(_resolve_file(r) is not None for r in GOVERNANCE_CANONICAL_REFS)

    api_plan_record = LocalRunnerBridgeApiPlanRecord(
        record_id="local_runner_bridge_api_plan_v1",
        service_host=SERVICE_HOST,
        service_bind_address=SERVICE_BIND_ADDRESS,
        service_port=SERVICE_PORT,
        ui_host=UI_HOST,
        endpoints=API_ENDPOINTS,
        localhost_only=LOCALHOST_ONLY,
        external_network_allowed=EXTERNAL_NETWORK_ALLOWED,
    )

    lifecycle_record = LocalRunnerJobLifecycleRecord(
        record_id="local_runner_job_lifecycle_v1",
        states=JOB_LIFECYCLE_STATES,
        required_fields_per_state=(
            "job_id", "status", "status_reason", "created_at", "updated_at",
            "phase_ref", "test_board_ref", "artifact_refs",
        ),
        lifecycle_defined=len(JOB_LIFECYCLE_STATES) >= 9,
    )

    registry_record = LocalRunnerRegistryPlanRecord(
        record_id="local_runner_registry_plan_v1",
        runners=RUNNER_REGISTRY,
        capability_ids=CAPABILITY_IDS,
        runner_registry_defined=len(RUNNER_REGISTRY) >= 5,
        v1_implementation_runners=("segmentation_mobile_sam_runner", "slam_video_runner"),
    )

    slam_route_record = SlamLocalVideoRunnerRouteRecord(
        record_id="slam_local_video_runner_route_v1",
        route_stages=SLAM_VIDEO_RUNNER_ROUTE_STAGES,
        without_gt_limited_diagnostics=SLAM_WITHOUT_GT_LIMITED_DIAGNOSTICS,
        no_ate_without_gt=SLAM_WITHOUT_GT_NO_ATE,
        no_gt_benchmark_comparison_without_gt=SLAM_WITHOUT_GT_NO_GT_BENCHMARK_COMPARISON,
    )

    mobilesam_route_record = MobileSamLocalImageRunnerRouteRecord(
        record_id="mobilesam_local_image_runner_route_v1",
        route_stages=MOBILESAM_IMAGE_RUNNER_ROUTE_STAGES,
        candidate_only=True,
        not_fact_not_runtime=True,
    )

    invariant_state: Dict[str, bool] = {
        "not_runtime": NOT_RUNTIME is True,
        "localhost_only": LOCALHOST_ONLY is True and SERVICE_BIND_ADDRESS == "127.0.0.1",
        "no_external_network": EXTERNAL_NETWORK_ALLOWED is False and DATASET_DOWNLOAD_ALLOWED is False,
        "no_live_camera_mic": LIVE_CAMERA_ALLOWED is False and LIVE_MICROPHONE_ALLOWED is False,
        "no_registry_mutation": REGISTRY_MUTATION_ALLOWED is False,
        "no_fact_semantic": FACT_WRITE_ALLOWED is False and SEMANTIC_LAYER_ALLOWED is False,
        "not_output_adapter_nav_speech": (
            NOT_OUTPUT_ADAPTER is True
            and NAVIGATION_ACTION_SPEECH_ALLOWED is False
        ),
        "testboard_required_for_each_job": TESTBOARD_REQUIRED_FOR_EACH_JOB is True and SERVICE_MUST_WRITE_TESTBOARD is True,
        "adapter_required_before_ui_display": ADAPTER_REQUIRED_BEFORE_UI_DISPLAY is True,
        "slam_without_gt_no_ate": SLAM_WITHOUT_GT_NO_ATE is True,
        "slam_without_gt_no_gt_benchmark": SLAM_WITHOUT_GT_NO_GT_BENCHMARK_COMPARISON is True,
        "job_lifecycle_defined": lifecycle_record.lifecycle_defined,
        "runner_registry_defined": registry_record.runner_registry_defined,
        "api_schema_defined": api_schema_defined,
        "candidate_only_boundary_defined": CANDIDATE_ONLY_BOUNDARY_DEFINED is True,
        "test_artifact_protected": REQUIRED_TEST_BOARD_FIELDS_LOCAL.get("test_artifact_protected", False) is True,
    }

    negative_guards: List[NegativeLocalRunnerBridgeServicePlanningGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeLocalRunnerBridgeServicePlanningGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    ui_patch_ok = (
        verify_flags.get("local_asset_import_ui_patch_go_verified") is True
        or verify_flags.get("local_asset_import_ui_patch_route_from_planning") is True
    )

    go_conditions: Dict[str, bool] = {
        "local_runner_bridge_service_planning_profile_count_eq_1": True,
        "localhost_only": LOCALHOST_ONLY is True,
        "not_runtime": NOT_RUNTIME is True,
        "not_output_adapter": NOT_OUTPUT_ADAPTER is True,
        "not_commercial_backend": NOT_COMMERCIAL_BACKEND is True,
        "api_schema_defined": api_schema_defined,
        "job_lifecycle_defined": lifecycle_record.lifecycle_defined,
        "runner_registry_defined": registry_record.runner_registry_defined,
        "adapter_required_before_ui_display": ADAPTER_REQUIRED_BEFORE_UI_DISPLAY is True,
        "testboard_required_for_each_job": TESTBOARD_REQUIRED_FOR_EACH_JOB is True,
        "candidate_only_boundary_defined": CANDIDATE_ONLY_BOUNDARY_DEFINED is True,
        "slam_without_gt_no_ate": SLAM_WITHOUT_GT_NO_ATE is True,
        "slam_without_gt_no_gt_benchmark_comparison": SLAM_WITHOUT_GT_NO_GT_BENCHMARK_COMPARISON is True,
        "ui_may_submit_local_job": PAGE_MAY_SUBMIT_LOCAL_JOB is True,
        "service_may_execute_model_after_approval": SERVICE_MAY_EXECUTE_MODEL_AFTER_APPROVAL is True,
        "registry_mutation_allowed_false": REGISTRY_MUTATION_ALLOWED is False,
        "semantic_layer_allowed_false": SEMANTIC_LAYER_ALLOWED is False,
        "fact_write_allowed_false": FACT_WRITE_ALLOWED is False,
        "navigation_action_speech_allowed_false": NAVIGATION_ACTION_SPEECH_ALLOWED is False,
        "external_network_allowed_false": EXTERNAL_NETWORK_ALLOWED is False,
        "live_camera_allowed_false": LIVE_CAMERA_ALLOWED is False,
        "live_microphone_allowed_false": LIVE_MICROPHONE_ALLOWED is False,
        "planning_only": PLANNING_ONLY is True,
        "governance_standards_referenced": gov_refs_ok,
        "ui_patch_upstream_ok": ui_patch_ok,
        "negative_guard_count_eq_16": negative_guard_count == 16,
        "negative_guard_passed_eq_16": negative_guard_passed == 16,
        **schema_flags,
        **negative_guard_go,
        **{f"test_board.{k}": (v is True) for k, v in REQUIRED_TEST_BOARD_FIELDS_LOCAL.items()},
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS if k != "local_asset_import_ui_patch_go_verified"},
        "local_asset_import_runner_bridge_planning_go_verified": (
            verify_flags.get("local_asset_import_runner_bridge_planning_go_verified") is True
        ),
    }
    if verify_flags.get("local_asset_import_ui_patch_go_verified") is True:
        go_conditions["local_asset_import_ui_patch_go_verified"] = True
    else:
        go_conditions["local_asset_import_ui_patch_route_from_planning"] = (
            verify_flags.get("local_asset_import_ui_patch_route_from_planning") is True
        )

    for key, ok in go_conditions.items():
        (passed_checks if ok else failed_checks).append(f"go.{key}={'true' if ok else 'false'}")

    blocker_count = len(failed_checks)
    final_decision = FINAL_DECISION_GO if blocker_count == 0 else FINAL_DECISION_BLOCKED

    test_board_total = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)
    decision = P1MidplatformModelTestLensLocalRunnerBridgeServicePlanningDecision(
        decision_ref=DECISION_REF,
        local_runner_bridge_service_planning_profile_count=1,
        api_schema_defined=api_schema_defined,
        job_lifecycle_defined=lifecycle_record.lifecycle_defined,
        runner_registry_defined=registry_record.runner_registry_defined,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    api_plan_payload = {
        **asdict(api_plan_record),
        "asset_store_rel": ASSET_STORE_REL,
        "endpoints_detail": [dict(e) for e in API_ENDPOINTS],
    }
    lifecycle_payload = asdict(lifecycle_record)
    registry_payload = asdict(registry_record)
    slam_route_payload = asdict(slam_route_record)
    mobilesam_route_payload = asdict(mobilesam_route_record)
    ui_integration_payload = {
        "ui_integration_patch_items": list(UI_INTEGRATION_PATCH_ITEMS),
        "boundary_copy_zh": [
            "本地 runner 在 localhost 执行",
            "这不是 runtime",
            "结果是 candidate-only",
            "不写 fact",
            "不进入 navigation/action/speech",
            "不进入 output adapter",
        ],
    }

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Model Test Lens Local Runner Bridge Service Planning",
        "lifecycle_variant": "p1_midplatform_model_test_lens_local_runner_bridge_service_planning",
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "planning_only": PLANNING_ONLY,
        "local_runner_bridge_service_planning": LOCAL_RUNNER_BRIDGE_SERVICE_PLANNING,
        "local_runner_bridge_root_rel": LOCAL_RUNNER_BRIDGE_ROOT_REL,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "local_runner_bridge_service_planning_profile": _build_profile(),
        "local_runner_bridge_service_planning_profile_count": 1,
        "local_runner_bridge_api_plan_record": api_plan_payload,
        "local_runner_job_lifecycle_record": lifecycle_payload,
        "local_runner_registry_plan_record": registry_payload,
        "slam_local_video_runner_route_record": slam_route_payload,
        "mobilesam_local_image_runner_route_record": mobilesam_route_payload,
        "ui_integration_plan": ui_integration_payload,
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
        "recommended_next_phase": NEXT_PHASE_SKELETON_EXECUTION,
        "conclusions": {
            "planning_status": "go" if blocker_count == 0 else "blocked",
            "transition_note": (
                "PLANNING ONLY. Local Runner Bridge Service at 127.0.0.1:8787; "
                "UI at localhost:8765 submits jobs; runner executes after approval; "
                "adapter required for envelope. Next: skeleton execution with "
                "MobileSAM + SLAM limited route."
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
        (out_root / "local_runner_bridge_api_plan_v1.json").write_text(
            json.dumps(api_plan_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_root / "local_runner_job_lifecycle_v1.json").write_text(
            json.dumps(lifecycle_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_root / "local_runner_registry_plan_v1.json").write_text(
            json.dumps(registry_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_root / "slam_local_video_runner_route_v1.json").write_text(
            json.dumps(slam_route_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_root / "mobilesam_local_image_runner_route_v1.json").write_text(
            json.dumps(mobilesam_route_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
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
            "local_runner_bridge_api_plan_record": {"record": api_plan_payload},
            "local_runner_job_lifecycle_record": {"record": lifecycle_payload},
            "local_runner_registry_plan_record": {"record": registry_payload},
            "slam_local_video_runner_route_record": {"record": slam_route_payload},
            "mobilesam_local_image_runner_route_record": {"record": mobilesam_route_payload},
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
            "localhost_only": True,
            "not_runtime": True,
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
    result = review_model_test_lens_local_runner_bridge_service_planning_v1()
    print(json.dumps(
        {
            "phase_id": result["phase_id"],
            "final_decision": result["final_decision"],
            "blocker_count": result["blocker_count"],
            "negative_guard_passed": result["negative_guard_passed"],
            "negative_guard_count": result["negative_guard_count"],
            "recommended_next_phase": result["recommended_next_phase"],
        },
        indent=2,
        ensure_ascii=False,
    ))
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
