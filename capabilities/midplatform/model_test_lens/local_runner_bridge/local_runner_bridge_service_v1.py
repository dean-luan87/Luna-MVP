# -*- coding: utf-8 -*-
"""Local Runner Bridge Service orchestration v1."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.midplatform.model_test_lens.local_runner_bridge.adapters.mobilesam_runner_to_envelope_adapter_v1 import (
    build_mobilesam_envelope,
)
from capabilities.midplatform.model_test_lens.local_runner_bridge.adapters.slam_limited_runner_to_envelope_adapter_v1 import (
    build_slam_limited_envelope,
)
from capabilities.midplatform.model_test_lens.local_runner_bridge.local_runner_bridge_job_store_v1 import (
    load_job,
    new_asset_id,
    new_job_id,
    save_job,
    update_job_status,
)
from capabilities.midplatform.model_test_lens.local_runner_bridge.local_runner_bridge_skeleton_execution_types_v1 import (
    JOB_LIFECYCLE_STATES,
    PHASE_ID,
    RUNNER_REGISTRY,
    SERVICE_NAME,
    SERVICE_VERSION,
)
from capabilities.midplatform.model_test_lens.local_runner_bridge.local_runner_bridge_storage_v1 import (
    boundary_flags,
    copy_local_asset,
    eval_out_dir,
    job_output_dir,
    repo_root,
    resolve_path,
    sha256_file,
)
from capabilities.midplatform.model_test_lens.local_runner_bridge.runners.mobilesam_image_runner_v1 import (
    run_mobilesam_image_runner,
)
from capabilities.midplatform.model_test_lens.local_runner_bridge.runners.slam_video_limited_runner_v1 import (
    run_slam_video_limited_runner,
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _runner_type_for(category: str, model_id: str) -> str:
    if category == "segmentation" and "mobile_sam" in model_id:
        return "segmentation_mobile_sam"
    if category == "slam_vio":
        return "slam_video_limited"
    if category == "ocr":
        return "ocr_placeholder"
    if category == "tts":
        return "tts_placeholder"
    if category == "asr":
        return "asr_placeholder"
    return "unsupported"


def get_capabilities() -> Dict[str, Any]:
    return {
        "service_name": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "localhost_only": True,
        "available_runners": [
            "segmentation_mobile_sam",
            "slam_video_limited",
            "ocr_placeholder",
            "tts_placeholder",
            "asr_placeholder",
        ],
        "runner_registry": list(RUNNER_REGISTRY),
        "job_lifecycle_states": list(JOB_LIFECYCLE_STATES),
        "boundary_flags": {
            **boundary_flags(),
            "not_runtime": True,
            "not_output_adapter": True,
            "candidate_only": True,
        },
    }


def _manifest_rel(asset_id: str) -> str:
    return f"_tmp_eval_out/model_test_lens_local_runner_bridge_v1/assets/{asset_id}/manifest.json"


def register_asset(body: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
    asset_type = body.get("asset_type", "image")
    model_category = body.get("model_category", "segmentation")
    model_id = body.get("requested_model_id", "mobile_sam")
    local_path = body.get("local_path")
    browser_file_name = body.get("browser_file_name", "")

    if body.get("external_url_source"):
        return 400, {"error": "external_url_not_allowed"}

    asset_id = new_asset_id()
    stored_path = None
    copy_status = "no_copy"
    if local_path:
        src = Path(str(local_path)).expanduser()
        if not src.is_file():
            src = resolve_path(str(local_path))
        if src.is_file():
            stored_path, copy_status = copy_local_asset(src, asset_id)

    manifest = {
        "manifest_id": f"manifest_{asset_id}",
        "created_by": "local_runner_bridge_service_v1",
        "created_by_phase": PHASE_ID,
        "created_at": _now(),
        "asset_id": asset_id,
        "asset_type": asset_type,
        "local_file_name": browser_file_name or (stored_path.name if stored_path else ""),
        "local_path_or_browser_file_name": str(stored_path or local_path or browser_file_name),
        "local_path": str(stored_path or local_path or browser_file_name),
        "file_name": browser_file_name or (stored_path.name if stored_path else ""),
        "source_type": "user_supplied_local_asset",
        "scoped_for_model_test": True,
        "intended_test_type": model_category,
        "requested_model_id": model_id,
        "candidate_only": True,
        "fact_layer_source": False,
        "semantic_layer_source": False,
        "navigation_runtime_frame": False,
        "must_not_enter_fact_layer": True,
        "must_not_enter_runtime": True,
        "must_not_enter_output_adapter": True,
        "must_not_enter_semantic_layer": True,
        "must_not_trigger_navigation_action_speech": True,
        "copy_status": copy_status,
    }
    if stored_path and stored_path.is_file():
        manifest["file_size_bytes"] = stored_path.stat().st_size
        manifest["sha256_status"] = "service_computed"
        manifest["sha256"] = sha256_file(stored_path)
    else:
        manifest["sha256_status"] = "pending_runner_computation"

    manifest_ref = _manifest_rel(asset_id)
    manifest_path = repo_root() / manifest_ref
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return 200, {
        "asset_id": asset_id,
        "manifest_ref": manifest_ref,
        "asset_manifest": manifest,
        "status": "asset_registered",
        "candidate_only": True,
    }


def create_job(body: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
    manifest = body.get("asset_manifest") or body.get("asset_manifest_inline")
    if not manifest:
        return 400, {"error": "asset_manifest_required"}
    category = body.get("requested_model_category") or manifest.get("intended_test_type", "segmentation")
    model_id = body.get("requested_model_id") or manifest.get("requested_model_id", "mobile_sam")
    runner_type = _runner_type_for(category, model_id)
    job_id = new_job_id()
    job = {
        "job_id": job_id,
        "status": "ready_to_run",
        "status_reason": "local_test_approval_granted_for_skeleton",
        "created_at": _now(),
        "updated_at": _now(),
        "phase_ref": PHASE_ID,
        "asset_manifest": manifest,
        "asset_manifest_ref": body.get("asset_manifest_ref") or manifest.get("manifest_id"),
        "requested_model_category": category,
        "requested_model_id": model_id,
        "requested_test_profile": body.get("requested_test_profile", "default_candidate_test_profile_v1"),
        "runner_type": runner_type,
        "requires_test_board_record": True,
        "candidate_output_only": True,
        "local_test_approval_granted_for_skeleton": True,
        "not_runtime_approval": True,
        "not_output_adapter_approval": True,
        "not_fact_approval": True,
        "not_registry_mutation_approval": True,
        "test_board_ref": None,
        "envelope_ref": None,
        "result_artifact_refs": [],
    }
    save_job(job)
    return 200, {
        "job_id": job_id,
        "status": job["status"],
        "job_ref": job_id,
        "runner_type": runner_type,
        "requires_test_board_record": True,
        "candidate_output_only": True,
    }


def _write_job_testboard(job_id: str, payload: Dict[str, Any]) -> str:
    tb_dir = job_output_dir(job_id) / "test_board"
    tb_dir.mkdir(parents=True, exist_ok=True)
    ref = str(tb_dir / "job_test_board_record.json")
    record = {
        "protocol_id": "TestBoardProtectedArtifactRuleV1",
        "phase_id": PHASE_ID,
        "job_id": job_id,
        "recorded_at_utc": _now(),
        "protected": True,
        "non_deletable": True,
        "deletion_forbidden": True,
        "candidate_output_only": True,
        "not_runtime": True,
        **payload,
    }
    Path(ref).write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return ref


def run_job(job_id: str) -> Tuple[int, Dict[str, Any]]:
    job = load_job(job_id)
    if job is None:
        return 404, {"error": "job_not_found", "job_id": job_id}

    runner_type = job.get("runner_type")
    out_dir = job_output_dir(job_id)
    update_job_status(job_id, "running", f"runner_start:{runner_type}")

    manifest = job.get("asset_manifest") or {}
    local_path = manifest.get("local_path")
    image_path = Path(str(local_path)) if local_path else None
    if image_path and not image_path.is_file():
        image_path = resolve_path(str(local_path))

    runner_result: Dict[str, Any]
    if runner_type == "segmentation_mobile_sam":
        if not image_path or not image_path.is_file():
            runner_result = {
                "status": "failed_no_boundary_violation",
                "status_reason": "image_path_not_found",
                "no_boundary_violation": True,
                "failure_recorded": True,
            }
        else:
            runner_result = run_mobilesam_image_runner(
                image_path=image_path,
                output_dir=out_dir,
                job_id=job_id,
                file_name=str(manifest.get("file_name") or manifest.get("local_file_name") or ""),
            )
    elif runner_type == "slam_video_limited":
        runner_result = run_slam_video_limited_runner(
            asset_manifest=manifest,
            output_dir=out_dir,
            job_id=job_id,
        )
    else:
        return 400, {
            "error": "runner_not_executable_in_skeleton",
            "runner_type": runner_type,
            "status": "blocked",
        }

    update_job_status(job_id, "adapter_processing", "building_envelope")
    tb_ref = _write_job_testboard(job_id, {"runner_result_status": runner_result.get("status")})
    test_board_refs = [tb_ref]

    envelope: Optional[Dict[str, Any]] = None
    if runner_type == "segmentation_mobile_sam":
        envelope = build_mobilesam_envelope(job=job, runner_result=runner_result, test_board_refs=test_board_refs)
    elif runner_type == "slam_video_limited":
        envelope = build_slam_limited_envelope(job=job, runner_result=runner_result, test_board_refs=test_board_refs)

    envelope_ref = None
    if envelope:
        envelope_ref = str(out_dir / "envelope.json")
        Path(envelope_ref).write_text(json.dumps(envelope, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        runner_path = out_dir / "runner_result.json"
        runner_path.write_text(json.dumps(runner_result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    final_status = runner_result.get("status", "failed_no_boundary_violation")
    if final_status == "completed":
        pass
    elif final_status == "completed_limited":
        pass
    else:
        final_status = "failed_no_boundary_violation"

    job = update_job_status(
        job_id,
        final_status,
        runner_result.get("status_reason", ""),
        runner_result=runner_result,
        envelope=envelope,
        envelope_ref=envelope_ref,
        test_board_ref=tb_ref,
        test_board_refs=test_board_refs,
        result_artifact_refs=[envelope_ref, str(out_dir / "runner_result.json")] if envelope_ref else [],
    ) or job

    return 200, {
        "job_id": job_id,
        "status": final_status,
        "status_reason": runner_result.get("status_reason"),
        "runner_type": runner_type,
        "envelope_ref": envelope_ref,
        "test_board_ref": tb_ref,
        "candidate_output_only": True,
        "no_boundary_violation": runner_result.get("no_boundary_violation", True),
    }


def job_status(job_id: str) -> Tuple[int, Dict[str, Any]]:
    job = load_job(job_id)
    if job is None:
        return 404, {"error": "job_not_found"}
    return 200, {
        "job_id": job_id,
        "status": job.get("status"),
        "status_reason": job.get("status_reason"),
        "created_at": job.get("created_at"),
        "updated_at": job.get("updated_at"),
        "runner_type": job.get("runner_type"),
        "envelope_ref": job.get("envelope_ref"),
        "test_board_ref": job.get("test_board_ref"),
        "candidate_output_only": True,
    }


def job_result(job_id: str) -> Tuple[int, Dict[str, Any]]:
    job = load_job(job_id)
    if job is None:
        return 404, {"error": "job_not_found"}
    return 200, {
        "job_id": job_id,
        "status": job.get("status"),
        "envelope": job.get("envelope"),
        "envelope_ref": job.get("envelope_ref"),
        "result_artifact_refs": job.get("result_artifact_refs") or [],
        "test_board_refs": job.get("test_board_refs") or [],
        "candidate_output_only": True,
        "adapter_required_before_ui_display": True,
    }
