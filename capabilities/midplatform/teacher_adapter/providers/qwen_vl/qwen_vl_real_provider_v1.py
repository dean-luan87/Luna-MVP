# -*- coding: utf-8 -*-
"""Qwen-VL Real Provider — orchestrates API → parse → normalize pipeline."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from capabilities.midplatform.teacher_adapter.providers.qwen_vl.api_client_v1 import call_qwen_vl_api
from capabilities.midplatform.teacher_adapter.providers.qwen_vl.evidence_normalizer_v1 import (
    normalize_teacher_evidence,
)
from capabilities.midplatform.teacher_adapter.providers.qwen_vl.request_builder_v1 import (
    build_teacher_request,
)
from capabilities.midplatform.teacher_adapter.providers.qwen_vl.response_parser_v1 import (
    parse_raw_teacher_response,
)
from capabilities.midplatform.teacher_adapter.providers.qwen_vl.qwen_vl_teacher_types_v1 import (
    PROVIDER_ID,
    TEACHER_ROLE,
)


def resolve_image_path(
    *,
    job_envelope: Optional[Dict[str, Any]] = None,
    image_ref: Optional[str] = None,
) -> Optional[str]:
    """Resolve local image path from job envelope without exposing internal state."""
    if job_envelope:
        manifest = job_envelope.get("asset_manifest") or {}
        for key in ("local_path", "local_path_or_browser_file_name"):
            p = manifest.get(key)
            if p and Path(p).is_file():
                return str(Path(p))
        file_name = manifest.get("file_name") or manifest.get("local_file_name")
        asset_id = manifest.get("asset_id")
        if file_name:
            for base in (Path.cwd(), Path(__file__).resolve().parents[5]):
                candidates = [
                    base / "capabilities" / "test_assets" / "model_test_lens" / (asset_id or "") / file_name,
                    base / "capabilities" / "midplatform" / "model_test_lens" / "test_assets" / file_name,
                ]
                for c in candidates:
                    if c.is_file():
                        return str(c)
    if image_ref:
        p = Path(image_ref)
        if p.is_file():
            return str(p)
    return None


def invoke_qwen_vl_real_provider(
    *,
    situation_candidate: Dict[str, Any],
    plan_candidate: Optional[Dict[str, Any]] = None,
    job_envelope: Optional[Dict[str, Any]] = None,
    image_ref: Optional[str] = None,
    recorded_fixture_id: Optional[str] = None,
    task: str = "understand_environment",
) -> Dict[str, Any]:
    """
    Full real-provider pipeline:
    request_builder → api_client → response_parser → evidence_normalizer.
    Raw response is always returned separately from teacher_evidence_candidate.
    """
    image_path = resolve_image_path(job_envelope=job_envelope, image_ref=image_ref)
    teacher_request = build_teacher_request(
        situation_candidate=situation_candidate,
        plan_candidate=plan_candidate,
        image_ref=image_ref,
        image_path=image_path,
        task=task,
    )
    if recorded_fixture_id:
        teacher_request["recorded_fixture_id"] = recorded_fixture_id

    raw_envelope = call_qwen_vl_api(
        teacher_request=teacher_request,
        recorded_fixture_id=recorded_fixture_id,
    )
    parsed = parse_raw_teacher_response(raw_envelope)
    evidence = normalize_teacher_evidence(
        parsed_response=parsed,
        situation_candidate=situation_candidate,
        plan_candidate=plan_candidate,
        raw_envelope=raw_envelope,
    )

    return {
        "provider_id": PROVIDER_ID,
        "teacher_role": TEACHER_ROLE,
        "teacher_request": teacher_request,
        "raw_teacher_response": raw_envelope,
        "parsed_teacher_response": parsed,
        "teacher_evidence_candidate": evidence,
        "raw_separated_from_evidence": True,
        "live_call": raw_envelope.get("live_call"),
        "recorded_fixture_id": raw_envelope.get("recorded_fixture_id"),
        "latency_ms": raw_envelope.get("latency_ms"),
        "usage": raw_envelope.get("usage"),
        "candidate_only": True,
        "not_fact": True,
    }
