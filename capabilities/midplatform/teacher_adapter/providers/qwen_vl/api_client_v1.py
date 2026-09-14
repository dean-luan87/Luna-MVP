# -*- coding: utf-8 -*-
"""Qwen-VL Teacher — API client v1 (DashScope multimodal, timeout/retry/error)."""

from __future__ import annotations

import base64
import json
import os
import time
import uuid
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from urllib import error, request

from capabilities.midplatform.teacher_adapter.providers.qwen_vl.qwen_vl_teacher_types_v1 import PROVIDER_ID

DEFAULT_MODEL = "qwen-vl-plus"
DEFAULT_TIMEOUT_S = 60
DEFAULT_RETRIES = 2
MULTIMODAL_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures" / "raw_responses"


def is_live_mode_enabled() -> bool:
    return os.getenv("LUNA_QWEN_VL_TEACHER_LIVE", "").strip().lower() in ("1", "true", "yes")


def resolve_api_key() -> Optional[str]:
    key = (os.getenv("DASHSCOPE_API_KEY") or os.getenv("LUNA_DASHSCOPE_API_KEY") or "").strip()
    return key or None


def resolve_model_id() -> str:
    return (os.getenv("LUNA_QWEN_VL_TEACHER_MODEL") or DEFAULT_MODEL).strip()


def _encode_image(image_path: str) -> Tuple[str, str]:
    path = Path(image_path)
    if not path.is_file():
        raise FileNotFoundError(f"image_not_found:{image_path}")
    data = path.read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    suffix = path.suffix.lower().lstrip(".") or "png"
    mime = "jpeg" if suffix in ("jpg", "jpeg") else suffix
    return f"data:image/{mime};base64,{b64}", str(path)


def _load_recorded_fixture(fixture_id: str) -> Dict[str, Any]:
    path = FIXTURES_DIR / f"{fixture_id}.json"
    if not path.is_file():
        raise FileNotFoundError(f"recorded_fixture_missing:{fixture_id}")
    return json.loads(path.read_text(encoding="utf-8"))


def _extract_http_error_body(exc: error.HTTPError) -> str:
    try:
        return exc.read().decode("utf-8", errors="replace")[:2000]
    except Exception:
        return str(exc)


def _post_json(url: str, payload: Dict[str, Any], headers: Dict[str, str], timeout_s: int) -> Dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=body, headers=headers, method="POST")
    with request.urlopen(req, timeout=timeout_s) as resp:
        return json.loads(resp.read().decode("utf-8"))


def call_qwen_vl_api(
    *,
    teacher_request: Dict[str, Any],
    recorded_fixture_id: Optional[str] = None,
    timeout_s: int = DEFAULT_TIMEOUT_S,
    max_retries: int = DEFAULT_RETRIES,
) -> Dict[str, Any]:
    """
    Call Qwen-VL API or replay recorded raw response.
    Returns envelope with raw_response separated from normalized evidence.
    """
    request_id = f"qwen_api_{uuid.uuid4().hex[:12]}"
    started = time.perf_counter()
    api_key = resolve_api_key()
    live = is_live_mode_enabled() and bool(api_key)
    image_path = teacher_request.get("image_path")

    if live and image_path and Path(image_path).is_file():
        image_data_url, _ = _encode_image(image_path)
        model = resolve_model_id()
        api_payload = {
            "model": model,
            "input": {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"image": image_data_url},
                            {"text": teacher_request.get("prompt_text", "")},
                        ],
                    }
                ]
            },
        }
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        last_err: Optional[str] = None
        raw: Dict[str, Any] = {}
        for attempt in range(max_retries + 1):
            try:
                raw = _post_json(MULTIMODAL_URL, api_payload, headers, timeout_s)
                last_err = None
                break
            except error.HTTPError as exc:
                last_err = _extract_http_error_body(exc)
                if exc.code in (429, 500, 502, 503, 504) and attempt < max_retries:
                    time.sleep(0.5 * (attempt + 1))
                    continue
                raw = {"error": last_err, "http_status": exc.code}
                break
            except (error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                last_err = str(exc)
                if attempt < max_retries:
                    time.sleep(0.5 * (attempt + 1))
                    continue
                raw = {"error": last_err}
                break
        latency_ms = round((time.perf_counter() - started) * 1000, 2)
        return {
            "provider_id": PROVIDER_ID,
            "request_id": request_id,
            "model_id": model,
            "live_call": True,
            "recorded_fixture_id": None,
            "raw_response": raw,
            "latency_ms": latency_ms,
            "usage": raw.get("usage") if isinstance(raw, dict) else None,
            "error": raw.get("error") if isinstance(raw, dict) else last_err,
            "candidate_only": True,
            "not_fact": True,
        }

    fixture_id = recorded_fixture_id or teacher_request.get("recorded_fixture_id") or "unknown_scene_hypothesis"
    recorded = _load_recorded_fixture(fixture_id)
    latency_ms = round((time.perf_counter() - started) * 1000, 2)
    return {
        "provider_id": PROVIDER_ID,
        "request_id": request_id,
        "model_id": recorded.get("model_id", resolve_model_id()),
        "live_call": False,
        "recorded_fixture_id": fixture_id,
        "raw_response": recorded.get("raw_response", recorded),
        "latency_ms": latency_ms,
        "usage": recorded.get("usage"),
        "error": None,
        "candidate_only": True,
        "not_fact": True,
    }
