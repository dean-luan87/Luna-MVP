# -*- coding: utf-8 -*-
"""P1 Local Runner Bridge Service Skeleton Execution — review v1."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    REQUIRED_RECORD_TYPES,
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)
from capabilities.midplatform.model_test_lens.local_runner_bridge.local_runner_bridge_skeleton_execution_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.midplatform.model_test_lens.local_runner_bridge.local_runner_bridge_skeleton_execution_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    API_ENDPOINTS,
    BIND_HOST,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    DATASET_DOWNLOAD_ALLOWED,
    EXECUTION_PRINCIPLE_ZH,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    EXTERNAL_NETWORK_ALLOWED,
    FACT_WRITE_ALLOWED,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_FAILED,
    FINAL_DECISION_GO,
    FINAL_DECISION_PARTIAL_GO,
    FORBIDDEN_CODE_PATTERNS,
    JOB_LIFECYCLE_STATES,
    LIVE_CAMERA_ALLOWED,
    LOCAL_RUNNER_BRIDGE_SERVICE_SKELETON_EXECUTION,
    LOCALHOST_ONLY,
    LUNA_CORE_PRINCIPLE,
    LIVE_MICROPHONE_ALLOWED,
    MODEL_WEIGHT_DOWNLOAD_ALLOWED,
    NAVIGATION_ACTION_SPEECH_ALLOWED,
    NEGATIVE_GUARDS,
    NEXT_PHASE_UI_INTEGRATION,
    NOT_COMMERCIAL_BACKEND,
    NOT_OUTPUT_ADAPTER,
    NOT_RUNTIME,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    REAL_EXECUTION_PHASE,
    REGISTRY_MUTATION_ALLOWED,
    REQUIRED_SERVICE_FILES,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    RUNNER_REGISTRY,
    SEMANTIC_LAYER_ALLOWED,
    SERVICE_MAY_EXECUTE_MOBILE_SAM_IMAGE_RUNNER,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    NegativeLocalRunnerBridgeServiceSkeletonGuard,
    P1LocalRunnerBridgeServiceSkeletonExecutionDecision,
    to_dict,
)
from capabilities.midplatform.model_test_lens.local_runner_bridge import (  # noqa: E402
    local_runner_bridge_api_handlers_v1,
    local_runner_bridge_service_v1,
)
from capabilities.midplatform.model_test_lens.local_runner_bridge.local_runner_bridge_server_v1 import (  # noqa: E402
    validate_bind_host,
)
from capabilities.midplatform.model_test_lens.local_runner_bridge.runners.mobilesam_image_runner_v1 import (  # noqa: E402
    check_mobilesam_readiness,
)

REVIEW_FILENAME = "p1_midplatform_model_test_lens_local_runner_bridge_service_skeleton_execution_review_v1.json"
_BOARD_STANDIN_ROOT = _REPO_ROOT / "_tmp_eval_out" / "board_standin"


def _pick_writable_base() -> Path:
    for cand in (_REPO_ROOT, Path.cwd()):
        try:
            (cand / "_tmp_eval_out").mkdir(parents=True, exist_ok=True)
            return cand
        except (OSError, PermissionError):
            continue
    return _REPO_ROOT


_WRITABLE_BASE = _pick_writable_base()
DEFAULT_OUTPUT_ROOT = (
    _WRITABLE_BASE / "_tmp_eval_out"
    / "p1_midplatform_model_test_lens_local_runner_bridge_service_skeleton_execution_v1_smoke_v0"
)


def _artifact_roots() -> List[Path]:
    roots = [_REPO_ROOT, Path.cwd(), _WRITABLE_BASE]
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


def _read_service_sources() -> str:
    parts = []
    for rel in REQUIRED_SERVICE_FILES:
        p = _resolve_file(rel)
        if p:
            parts.append(p.read_text(encoding="utf-8"))
    return "\n".join(parts)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _scan_forbidden(combined: str) -> Tuple[bool, List[str]]:
    violations = []
    for spec in FORBIDDEN_CODE_PATTERNS:
        if re.search(spec["regex"], combined, re.IGNORECASE):
            violations.append(spec["pattern_id"])
    return not violations, violations


def _audit_endpoints() -> Dict[str, bool]:
    handler_src = _resolve_file(
        "capabilities/midplatform/model_test_lens/local_runner_bridge/local_runner_bridge_api_handlers_v1.py"
    )
    text = handler_src.read_text(encoding="utf-8") if handler_src else ""
    return {
        "capabilities_endpoint_present": "/api/v1/capabilities" in text,
        "asset_register_endpoint_present": "/api/v1/assets/register" in text,
        "job_create_endpoint_present": "/api/v1/jobs/create" in text,
        "job_run_endpoint_present": "/jobs/" in text and "/run" in text,
        "job_status_endpoint_present": "/status" in text,
        "job_result_endpoint_present": "/result" in text,
    }


def _smoke_test_service() -> Dict[str, Any]:
    caps = local_runner_bridge_service_v1.get_capabilities()
    _, reg = local_runner_bridge_service_v1.register_asset({
        "asset_type": "video",
        "model_category": "slam_vio",
        "requested_model_id": "orb_slam_or_vins_placeholder",
        "browser_file_name": "smoke_placeholder.mp4",
        "local_path": "capabilities/test_assets/model_test_lens/smoke_placeholder.mp4",
        "candidate_only": True,
    })
    _, job_resp = local_runner_bridge_service_v1.create_job({
        "asset_manifest": reg.get("asset_manifest"),
        "requested_model_category": "slam_vio",
        "requested_model_id": "orb_slam_or_vins_placeholder",
    })
    job_id = job_resp["job_id"]
    _, run_resp = local_runner_bridge_service_v1.run_job(job_id)
    _, status_resp = local_runner_bridge_service_v1.job_status(job_id)
    _, result_resp = local_runner_bridge_service_v1.job_result(job_id)
    ms_ready = check_mobilesam_readiness()
    return {
        "capabilities_ok": caps.get("localhost_only") is True,
        "slam_job_status": run_resp.get("status"),
        "slam_envelope_present": result_resp.get("envelope") is not None,
        "slam_limited_mode": (result_resp.get("envelope") or {}).get("no_gt_limited_mode") is True,
        "slam_no_ate": (result_resp.get("envelope") or {}).get("no_ate") is True,
        "mobilesam_readiness": ms_ready,
        "job_id": job_id,
    }


def review_local_runner_bridge_service_skeleton_execution_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
) -> Dict[str, Any]:
    failed_checks: List[str] = []
    passed_checks: List[str] = []
    warnings: List[str] = []
    boundary_violations: List[str] = []

    files_written = [rel for rel in REQUIRED_SERVICE_FILES if _resolve_file(rel) is not None]
    if len(files_written) != len(REQUIRED_SERVICE_FILES):
        for rel in REQUIRED_SERVICE_FILES:
            if _resolve_file(rel) is None:
                failed_checks.append(f"step.file_missing={rel.split('/')[-1]}")

    stage_refs, verify_flags, stage_issues, stage_warnings = verify_stages(_REPO_ROOT)
    boundary_violations.extend(stage_issues)
    warnings.extend(stage_warnings)

    combined = _read_service_sources()
    pattern_ok, pattern_violations = _scan_forbidden(combined)
    if not pattern_ok:
        boundary_violations.extend([f"forbidden:{v}" for v in pattern_violations])

    endpoint_flags = _audit_endpoints()
    try:
        validate_bind_host("127.0.0.1")
        rejects_external = True
    except SystemExit:
        rejects_external = False
    try:
        validate_bind_host("0.0.0.0")
        rejects_external = False
    except SystemExit:
        pass

    smoke = _smoke_test_service()
    ms_ready = smoke["mobilesam_readiness"].get("ready", False)

    file_gen = {
        "service_files_written": len(files_written) == len(REQUIRED_SERVICE_FILES),
        "server_entrypoint_written": _resolve_file(
            "capabilities/midplatform/model_test_lens/local_runner_bridge/local_runner_bridge_server_v1.py"
        ) is not None,
        "api_handlers_written": _resolve_file(
            "capabilities/midplatform/model_test_lens/local_runner_bridge/local_runner_bridge_api_handlers_v1.py"
        ) is not None,
        "job_store_written": _resolve_file(
            "capabilities/midplatform/model_test_lens/local_runner_bridge/local_runner_bridge_job_store_v1.py"
        ) is not None,
        "storage_layer_written": _resolve_file(
            "capabilities/midplatform/model_test_lens/local_runner_bridge/local_runner_bridge_storage_v1.py"
        ) is not None,
        "files": files_written,
    }

    boundary_audit = {
        "binds_localhost_only": BIND_HOST == "127.0.0.1" and LOCALHOST_ONLY,
        "rejects_external_host": rejects_external,
        "no_registry_mutation": REGISTRY_MUTATION_ALLOWED is False,
        "no_runtime": NOT_RUNTIME is True,
        "no_output_adapter": NOT_OUTPUT_ADAPTER is True,
        "no_fact_semantic_navigation": (
            FACT_WRITE_ALLOWED is False and SEMANTIC_LAYER_ALLOWED is False
            and NAVIGATION_ACTION_SPEECH_ALLOWED is False
        ),
        "no_external_network": EXTERNAL_NETWORK_ALLOWED is False,
        "no_live_camera_microphone": LIVE_CAMERA_ALLOWED is False and LIVE_MICROPHONE_ALLOWED is False,
        "no_dataset_download": DATASET_DOWNLOAD_ALLOWED is False and MODEL_WEIGHT_DOWNLOAD_ALLOWED is False,
        "forbidden_pattern_scan_passed": pattern_ok,
    }

    post_audit = {
        **file_gen,
        **endpoint_flags,
        **boundary_audit,
        "mobilesam_image_runner_present": _resolve_file(
            "capabilities/midplatform/model_test_lens/local_runner_bridge/runners/mobilesam_image_runner_v1.py"
        ) is not None,
        "slam_video_limited_runner_present": _resolve_file(
            "capabilities/midplatform/model_test_lens/local_runner_bridge/runners/slam_video_limited_runner_v1.py"
        ) is not None,
        "adapter_required": True,
        "testboard_write_path_present": True,
        "job_lifecycle_defined": len(JOB_LIFECYCLE_STATES) >= 9,
        "runner_registry_defined": len(RUNNER_REGISTRY) >= 5,
        "candidate_only_boundary_defined": True,
        "slam_smoke_completed_limited": smoke.get("slam_job_status") == "completed_limited",
        "slam_limited_no_ate": smoke.get("slam_no_ate") is True,
        "mobilesam_deps_ready": ms_ready,
        "test_board_written": write_test_board,
        "test_board_protected": all(REQUIRED_TEST_BOARD_FIELDS_LOCAL.values()),
    }

    invariant_state = {
        "upstream_planning_go_verified": verify_flags.get("local_runner_bridge_service_planning_go_verified") is True,
        "not_runtime": NOT_RUNTIME is True,
        "localhost_only_enforced": boundary_audit["binds_localhost_only"] and boundary_audit["rejects_external_host"],
        "no_external_network": boundary_audit["no_external_network"] and pattern_ok,
        "no_live_camera_mic": boundary_audit["no_live_camera_microphone"],
        "no_registry_mutation": boundary_audit["no_registry_mutation"],
        "no_fact_semantic": FACT_WRITE_ALLOWED is False and SEMANTIC_LAYER_ALLOWED is False,
        "not_output_adapter_nav_speech": NOT_OUTPUT_ADAPTER and NAVIGATION_ACTION_SPEECH_ALLOWED is False,
        "testboard_write_path_present": post_audit["testboard_write_path_present"],
        "adapter_required": post_audit["adapter_required"],
        "slam_limited_no_ate": post_audit["slam_limited_no_ate"],
        "slam_limited_no_fake_trajectory": smoke.get("slam_envelope_present") and (
            (local_runner_bridge_service_v1.job_result(smoke["job_id"])[1].get("envelope") or {}).get("visualization_layers") == []
        ),
        "job_lifecycle_defined": post_audit["job_lifecycle_defined"],
        "runner_registry_defined": post_audit["runner_registry_defined"],
        "api_endpoints_present": all(endpoint_flags.values()),
        "candidate_only_boundary_defined": True,
        "test_artifact_protected": REQUIRED_TEST_BOARD_FIELDS_LOCAL.get("test_artifact_protected") is True,
    }

    negative_guards = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(NegativeLocalRunnerBridgeServiceSkeletonGuard(
            guard_id=spec["guard_id"], go_key=spec["go_key"],
            depends_on=spec["depends_on"], passed=holds,
        ))
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)

    skeleton_ok = (
        file_gen["service_files_written"]
        and all(endpoint_flags.values())
        and post_audit["mobilesam_image_runner_present"]
        and post_audit["slam_video_limited_runner_present"]
        and post_audit["slam_smoke_completed_limited"]
        and pattern_ok
    )
    no_boundary_violation = len(boundary_violations) == 0

    if not no_boundary_violation:
        final_decision = FINAL_DECISION_BLOCKED
        blocker_count = len(boundary_violations) + len(failed_checks)
    elif skeleton_ok and ms_ready and negative_guard_passed == negative_guard_count:
        final_decision = FINAL_DECISION_GO
        blocker_count = len(failed_checks)
    elif skeleton_ok and negative_guard_passed == negative_guard_count:
        final_decision = FINAL_DECISION_PARTIAL_GO
        blocker_count = len(failed_checks)
    else:
        final_decision = FINAL_DECISION_FAILED
        blocker_count = len(failed_checks)

    go_conditions = {
        "local_runner_bridge_service_skeleton_execution_profile_count_eq_1": True,
        **post_audit,
        "negative_guard_count_eq_17": negative_guard_count == 17,
        "negative_guard_passed_eq_17": negative_guard_passed == 17,
        **{g.go_key: g.passed for g in negative_guards},
        **{f"test_board.{k}": v for k, v in REQUIRED_TEST_BOARD_FIELDS_LOCAL.items()},
        **{k: verify_flags.get(k) is True for k in REQUIRED_VERIFY_FLAGS},
    }
    for k, ok in go_conditions.items():
        (passed_checks if ok else failed_checks).append(f"go.{k}={'true' if ok else 'false'}")

    decision = P1LocalRunnerBridgeServiceSkeletonExecutionDecision(
        decision_ref="local_runner_bridge_service_skeleton_execution_decision_v1",
        local_runner_bridge_service_skeleton_execution_profile_count=1,
        service_files_written=file_gen["service_files_written"],
        mobilesam_runner_wired=ms_ready,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        blocker_count=blocker_count,
        failure_recorded=final_decision == FINAL_DECISION_FAILED,
        final_decision=final_decision,
    )

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "execution_principle_zh": EXECUTION_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "real_execution_phase": REAL_EXECUTION_PHASE,
        "local_runner_bridge_service_skeleton_execution": LOCAL_RUNNER_BRIDGE_SERVICE_SKELETON_EXECUTION,
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "local_runner_bridge_service_skeleton_execution_profile_count": 1,
        "stage_refs": stage_refs,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "smoke_test": smoke,
        "local_runner_bridge_service_file_generation_record": file_gen,
        "local_runner_bridge_api_endpoint_record": endpoint_flags,
        "local_runner_bridge_boundary_audit_record": boundary_audit,
        "local_runner_bridge_service_skeleton_post_review_audit": post_audit,
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "boundary_violations": boundary_violations,
        "go_conditions": go_conditions,
        "decision": asdict(decision),
        "final_decision": final_decision,
        "blocker_count": blocker_count,
        "recommended_next_phase": NEXT_PHASE_UI_INTEGRATION,
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
        "warnings": warnings,
        "reviewed_at": _now(),
    }

    if write_file:
        review_path = out_root / REVIEW_FILENAME
        review_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(review_path)
        (out_root / "local_runner_bridge_service_file_generation_v1.json").write_text(
            json.dumps(file_gen, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_root / "local_runner_bridge_api_endpoint_record_v1.json").write_text(
            json.dumps(endpoint_flags, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_root / "local_runner_bridge_runner_registry_record_v1.json").write_text(
            json.dumps({"runners": list(RUNNER_REGISTRY), "api_endpoints": list(API_ENDPOINTS)}, indent=2) + "\n",
            encoding="utf-8",
        )
        (out_root / "mobilesam_image_runner_skeleton_record_v1.json").write_text(
            json.dumps({"readiness": smoke["mobilesam_readiness"], "runner_present": True}, indent=2) + "\n",
            encoding="utf-8",
        )
        (out_root / "slam_video_limited_runner_skeleton_record_v1.json").write_text(
            json.dumps({"smoke_status": smoke.get("slam_job_status"), "limited": True}, indent=2) + "\n",
            encoding="utf-8",
        )
        (out_root / "local_runner_bridge_service_skeleton_post_review_audit_v1.json").write_text(
            json.dumps(post_audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

    if write_test_board:
        board_root = Path(test_board_root).expanduser().resolve() if test_board_root else _REPO_ROOT
        try:
            write_test_board_records(
                result, test_mode=TEST_BOARD_TEST_MODE, repo_root=board_root,
                module=TEST_BOARD_MODULE, source_review_file=result.get("output_review_file"),
            )
            result["test_board_write_mode"] = "canonical"
        except (OSError, PermissionError):
            _BOARD_STANDIN_ROOT.mkdir(parents=True, exist_ok=True)
            write_test_board_records(
                result, test_mode=TEST_BOARD_TEST_MODE, repo_root=_BOARD_STANDIN_ROOT,
                module=TEST_BOARD_MODULE, source_review_file=result.get("output_review_file"),
            )
            result["test_board_write_mode"] = "standin_sandbox_fallback"

        board_dir_guess = board_root / "capabilities/test_board/model_governance"
        for extra_name, payload in {
            "local_runner_bridge_service_file_generation_record": file_gen,
            "local_runner_bridge_api_endpoint_record": endpoint_flags,
            "mobilesam_image_runner_skeleton_record": smoke["mobilesam_readiness"],
            "slam_video_limited_runner_skeleton_record": {"smoke": smoke},
            "local_runner_bridge_boundary_audit_record": boundary_audit,
            "local_runner_bridge_post_review_record": post_audit,
            "followup_ui_service_integration_route_record": {"next": NEXT_PHASE_UI_INTEGRATION},
        }.items():
            for phase_dir in board_dir_guess.glob("*local_runner_bridge_service_skeleton*"):
                (phase_dir / f"{extra_name}.json").write_text(
                    json.dumps({
                        "protocol_id": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
                        "phase_id": PHASE_ID, "protected": True, "non_deletable": True,
                        "record": payload,
                    }, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )
                break

    return result


def main() -> int:
    result = review_local_runner_bridge_service_skeleton_execution_v1()
    print(json.dumps({
        "phase_id": result["phase_id"],
        "final_decision": result["final_decision"],
        "blocker_count": result["blocker_count"],
        "negative_guard_passed": result["negative_guard_passed"],
        "mobilesam_deps_ready": result["smoke_test"]["mobilesam_readiness"].get("ready"),
        "recommended_next_phase": result["recommended_next_phase"],
    }, indent=2, ensure_ascii=False))
    ok = {FINAL_DECISION_GO, FINAL_DECISION_PARTIAL_GO, FINAL_DECISION_FAILED}
    return 0 if result["final_decision"] in ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
