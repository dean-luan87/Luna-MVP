# -*- coding: utf-8 -*-
"""Local Runner Bridge HTTP API handlers v1."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import parse_qs, urlparse

from capabilities.midplatform.model_test_lens.local_runner_bridge import local_runner_bridge_service_v1 as svc
from capabilities.midplatform.model_test_lens.local_runner_bridge.local_runner_bridge_storage_v1 import (
    artifact_roots,
    resolve_path,
)

_JOB_RUN_RE = re.compile(r"^/api/v1/jobs/([^/]+)/run$")
_JOB_STATUS_RE = re.compile(r"^/api/v1/jobs/([^/]+)/status$")
_JOB_RESULT_RE = re.compile(r"^/api/v1/jobs/([^/]+)/result$")
_LOCAL_FILE_PATH = "/api/v1/local-file"


_LOCAL_ORIGIN_RE = re.compile(r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$")


def cors_headers(origin: Optional[str]) -> Dict[str, str]:
    allowed = {"http://localhost:8765", "http://127.0.0.1:8765", "http://localhost:8787", "http://127.0.0.1:8787"}
    if origin and (origin in allowed or _LOCAL_ORIGIN_RE.match(origin)):
        return {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }
    return {}


def _path_allowed(path: Path) -> bool:
    resolved = path.resolve()
    for root in artifact_roots():
        try:
            resolved.relative_to(root.resolve())
            return True
        except ValueError:
            continue
    return False


def try_serve_local_file(path: str, origin: Optional[str] = None) -> Optional[Tuple[int, bytes, str, Dict[str, str]]]:
    """Read-only local artifact file for overlay display (localhost only)."""
    parsed = urlparse(path)
    if parsed.path != _LOCAL_FILE_PATH:
        return None
    qs = parse_qs(parsed.query)
    rel = (qs.get("rel") or [""])[0]
    if not rel:
        headers = {"Content-Type": "text/plain; charset=utf-8", **cors_headers(origin)}
        return 400, b"missing rel", "text/plain", headers

    candidates: List[Path] = []
    expanded = Path(rel).expanduser()
    candidates.append(expanded)
    if not expanded.is_file():
        candidates.append(resolve_path(rel))

    target: Optional[Path] = None
    for cand in candidates:
        if cand.is_file():
            target = cand.resolve()
            break
    headers = cors_headers(origin)
    if not target or not _path_allowed(target):
        return 404, b"file not found", "text/plain", {**headers, "Content-Type": "text/plain; charset=utf-8"}

    suffix = target.suffix.lower()
    if suffix == ".png":
        ctype = "image/png"
    elif suffix in (".jpg", ".jpeg"):
        ctype = "image/jpeg"
    elif suffix == ".webp":
        ctype = "image/webp"
    elif suffix == ".gif":
        ctype = "image/gif"
    else:
        ctype = "application/octet-stream"
    return 200, target.read_bytes(), ctype, {**headers, "Content-Type": ctype}


def handle_request(method: str, path: str, body: bytes, origin: Optional[str] = None) -> Tuple[int, Dict[str, Any], Dict[str, str]]:
    headers = {"Content-Type": "application/json; charset=utf-8", **cors_headers(origin)}
    if method == "OPTIONS":
        return 204, {}, headers

    parsed_path = urlparse(path).path
    payload: Dict[str, Any] = {}
    if body:
        try:
            payload = json.loads(body.decode("utf-8"))
        except json.JSONDecodeError:
            return 400, {"error": "invalid_json"}, headers

    if method == "GET" and parsed_path == "/api/v1/capabilities":
        return 200, svc.get_capabilities(), headers
    if method == "POST" and parsed_path == "/api/v1/assets/register":
        code, data = svc.register_asset(payload)
        return code, data, headers
    if method == "POST" and parsed_path == "/api/v1/jobs/create":
        code, data = svc.create_job(payload)
        return code, data, headers

    m = _JOB_RUN_RE.match(parsed_path)
    if method == "POST" and m:
        code, data = svc.run_job(m.group(1))
        return code, data, headers

    m = _JOB_STATUS_RE.match(parsed_path)
    if method == "GET" and m:
        code, data = svc.job_status(m.group(1))
        return code, data, headers

    m = _JOB_RESULT_RE.match(parsed_path)
    if method == "GET" and m:
        code, data = svc.job_result(m.group(1))
        return code, data, headers

    if method == "POST" and parsed_path == "/api/v1/controlled-execution/run":
        from capabilities.midplatform.model_test_lens.local_runner_bridge import (
            local_runner_bridge_controlled_execution_v1 as ctrl_exec,
        )
        code, data = ctrl_exec.run_controlled_execution_api(payload)
        return code, data, headers

    if method == "POST" and parsed_path == "/api/v1/controlled-execution/ocr/run":
        from capabilities.midplatform.model_test_lens.local_runner_bridge import (
            local_runner_bridge_controlled_ocr_execution_v1 as ctrl_ocr,
        )
        code, data = ctrl_ocr.run_controlled_ocr_execution_api(payload)
        return code, data, headers

    return 404, {"error": "not_found", "path": parsed_path}, headers
