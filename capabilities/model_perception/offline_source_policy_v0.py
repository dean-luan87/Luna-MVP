"""
Phase-EngineeringFlow-002

Offline perception source policy selection v0.

Hard boundaries:
- Offline evaluation only (OptionA + phone_local controlled capture).
- Never enables runtime default paths.
- Any mismatch/failure must fall back to baseline/mock.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple


SOURCE_POLICY_ID_V0 = "yolo_default_offline_perception_source_v0"


def _read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


@dataclass(frozen=True)
class ManifestReadinessV0:
    ok: bool
    status: str  # pass/fail/partial
    model_config_id: Optional[str]
    weights_source: Optional[str]
    weights_path: Optional[str]
    weights_sha256_expected: Optional[str]
    weights_sha256_actual: Optional[str]
    weights_file_size_bytes: Optional[int]
    reason: Optional[str]


def check_yolo_manifest_readiness_v0(*, repo_root: str, manifest_path: str) -> ManifestReadinessV0:
    """
    Minimal readiness check for offline policy selection.
    Does not import torch; only validates manifest + pinned weights file integrity.
    """
    if not manifest_path or not os.path.exists(manifest_path):
        return ManifestReadinessV0(
            ok=False,
            status="fail",
            model_config_id=None,
            weights_source=None,
            weights_path=None,
            weights_sha256_expected=None,
            weights_sha256_actual=None,
            weights_file_size_bytes=None,
            reason="manifest_missing",
        )
    try:
        m = _read_json(manifest_path)
    except Exception as e:  # noqa: BLE001
        return ManifestReadinessV0(
            ok=False,
            status="fail",
            model_config_id=None,
            weights_source=None,
            weights_path=None,
            weights_sha256_expected=None,
            weights_sha256_actual=None,
            weights_file_size_bytes=None,
            reason=f"manifest_unparseable:{type(e).__name__}:{e}",
        )

    weights_source = m.get("weights_source")
    weights_path = m.get("weights_path")
    exp_sha = m.get("weights_sha256")
    size = m.get("weights_file_size_bytes")
    model_config_id = m.get("model_config_id")
    verification_status = str(m.get("verification_status") or "partial")

    if weights_source != "pinned_local":
        return ManifestReadinessV0(
            ok=False,
            status="fail",
            model_config_id=str(model_config_id) if model_config_id else None,
            weights_source=str(weights_source) if weights_source is not None else None,
            weights_path=str(weights_path) if weights_path else None,
            weights_sha256_expected=str(exp_sha) if exp_sha else None,
            weights_sha256_actual=None,
            weights_file_size_bytes=int(size) if isinstance(size, int) else None,
            reason="weights_source_not_pinned_local",
        )

    if not isinstance(weights_path, str) or not weights_path:
        return ManifestReadinessV0(
            ok=False,
            status="fail",
            model_config_id=str(model_config_id) if model_config_id else None,
            weights_source="pinned_local",
            weights_path=None,
            weights_sha256_expected=str(exp_sha) if exp_sha else None,
            weights_sha256_actual=None,
            weights_file_size_bytes=int(size) if isinstance(size, int) else None,
            reason="weights_path_missing",
        )

    resolved = weights_path if os.path.isabs(weights_path) else os.path.join(repo_root, weights_path)
    if not os.path.exists(resolved):
        return ManifestReadinessV0(
            ok=False,
            status="fail",
            model_config_id=str(model_config_id) if model_config_id else None,
            weights_source="pinned_local",
            weights_path=weights_path,
            weights_sha256_expected=str(exp_sha) if exp_sha else None,
            weights_sha256_actual=None,
            weights_file_size_bytes=int(size) if isinstance(size, int) else None,
            reason="weights_path_not_found",
        )

    actual_sha = None
    try:
        actual_sha = _sha256_file(resolved)
    except Exception as e:  # noqa: BLE001
        return ManifestReadinessV0(
            ok=False,
            status="fail",
            model_config_id=str(model_config_id) if model_config_id else None,
            weights_source="pinned_local",
            weights_path=weights_path,
            weights_sha256_expected=str(exp_sha) if exp_sha else None,
            weights_sha256_actual=None,
            weights_file_size_bytes=int(size) if isinstance(size, int) else None,
            reason=f"weights_sha256_compute_failed:{type(e).__name__}:{e}",
        )

    if not exp_sha or str(exp_sha) != str(actual_sha):
        return ManifestReadinessV0(
            ok=False,
            status="fail",
            model_config_id=str(model_config_id) if model_config_id else None,
            weights_source="pinned_local",
            weights_path=weights_path,
            weights_sha256_expected=str(exp_sha) if exp_sha else None,
            weights_sha256_actual=str(actual_sha),
            weights_file_size_bytes=int(os.path.getsize(resolved)),
            reason="weights_sha256_mismatch",
        )

    # Require manifest verification status to be pass for policy selection.
    if verification_status != "pass":
        return ManifestReadinessV0(
            ok=False,
            status="fail",
            model_config_id=str(model_config_id) if model_config_id else None,
            weights_source="pinned_local",
            weights_path=weights_path,
            weights_sha256_expected=str(exp_sha),
            weights_sha256_actual=str(actual_sha),
            weights_file_size_bytes=int(os.path.getsize(resolved)),
            reason=f"manifest_verification_status_not_pass:{verification_status}",
        )

    return ManifestReadinessV0(
        ok=True,
        status="pass",
        model_config_id=str(model_config_id) if model_config_id else None,
        weights_source="pinned_local",
        weights_path=weights_path,
        weights_sha256_expected=str(exp_sha),
        weights_sha256_actual=str(actual_sha),
        weights_file_size_bytes=int(os.path.getsize(resolved)),
        reason=None,
    )


def select_offline_perception_source_v0(
    *,
    repo_root: str,
    source_policy_id: str,
    offline_evaluation: bool,
    option_scope: str,
    evidence_type: str,
    controlled_live_stream: bool,
    pending_real_sidewalk_run: bool,
    disable_yolo: bool,
    yolo_manifest_path: Optional[str],
) -> Dict[str, Any]:
    """
    Returns selection decision + audit.
    """
    if source_policy_id != SOURCE_POLICY_ID_V0:
        return {
            "source_policy_id": source_policy_id,
            "source_selected": "baseline_mock",
            "fallback_used": True,
            "fallback_reason": "unknown_source_policy_id",
            "manifest_readiness": None,
        }

    if offline_evaluation is not True:
        return {
            "source_policy_id": source_policy_id,
            "source_selected": "baseline_mock",
            "fallback_used": True,
            "fallback_reason": "offline_evaluation_not_true",
            "manifest_readiness": None,
        }
    if option_scope != "OptionA":
        return {
            "source_policy_id": source_policy_id,
            "source_selected": "baseline_mock",
            "fallback_used": True,
            "fallback_reason": "option_scope_not_option_a",
            "manifest_readiness": None,
        }
    if evidence_type != "phone_local_controlled_capture":
        return {
            "source_policy_id": source_policy_id,
            "source_selected": "baseline_mock",
            "fallback_used": True,
            "fallback_reason": "evidence_type_not_phone_local_controlled_capture",
            "manifest_readiness": None,
        }
    if controlled_live_stream is not False:
        return {
            "source_policy_id": source_policy_id,
            "source_selected": "baseline_mock",
            "fallback_used": True,
            "fallback_reason": "controlled_live_stream_not_false",
            "manifest_readiness": None,
        }
    if pending_real_sidewalk_run is not True:
        return {
            "source_policy_id": source_policy_id,
            "source_selected": "baseline_mock",
            "fallback_used": True,
            "fallback_reason": "pending_real_sidewalk_run_not_true",
            "manifest_readiness": None,
        }
    if disable_yolo is True:
        return {
            "source_policy_id": source_policy_id,
            "source_selected": "baseline_mock",
            "fallback_used": True,
            "fallback_reason": "disable_yolo_true",
            "manifest_readiness": None,
        }

    if not yolo_manifest_path:
        return {
            "source_policy_id": source_policy_id,
            "source_selected": "baseline_mock",
            "fallback_used": True,
            "fallback_reason": "yolo_manifest_path_missing",
            "manifest_readiness": None,
        }

    mr = check_yolo_manifest_readiness_v0(repo_root=repo_root, manifest_path=yolo_manifest_path)
    if not mr.ok:
        return {
            "source_policy_id": source_policy_id,
            "source_selected": "baseline_mock",
            "fallback_used": True,
            "fallback_reason": f"pinned_local_readiness_fail:{mr.reason}",
            "manifest_readiness": {
                "ok": mr.ok,
                "status": mr.status,
                "model_config_id": mr.model_config_id,
                "weights_source": mr.weights_source,
                "weights_path": mr.weights_path,
                "reason": mr.reason,
            },
        }

    return {
        "source_policy_id": source_policy_id,
        "source_selected": "yolo_shadow",
        "fallback_used": False,
        "fallback_reason": None,
        "manifest_readiness": {
            "ok": mr.ok,
            "status": mr.status,
            "model_config_id": mr.model_config_id,
            "weights_source": mr.weights_source,
            "weights_path": mr.weights_path,
            "weights_sha256": mr.weights_sha256_expected,
            "weights_file_size_bytes": mr.weights_file_size_bytes,
        },
    }

