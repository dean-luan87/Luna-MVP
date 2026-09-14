# -*- coding: utf-8 -*-
"""
Reasoning Console API M0（最小 HTTP API）

接口：
- GET /api/reasoning/snapshots?view=all|blocked|issue|with_feedback
- GET /api/reasoning/snapshots/{id}
- GET /api/reasoning/snapshots/{id}/whitebox/{module}
- GET /api/reasoning/issues
"""

from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import parse_qs, urlparse

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.append(str(_ROOT))

from tools.reasoning_console_aggregator import (  # noqa: E402
    ReasoningConsoleSnapshot,
    load_snapshots_from_jsonl,
    resolve_default_jsonl_path,
)


def _json_bytes(obj: Any) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, default=str) + "\n").encode("utf-8")


def _pick_whitebox(snap: ReasoningConsoleSnapshot, module: str) -> Optional[Dict[str, Any]]:
    m = (module or "").strip().lower()
    if m in ("grid_search", "grid", "grid_search_whitebox_trace"):
        return snap.grid_search_whitebox_trace
    if m in ("recheck", "recheck_whitebox_trace"):
        return snap.recheck_whitebox_trace
    if m in ("action_hint", "action_hint_whitebox_trace"):
        return snap.action_hint_whitebox_trace
    if m in ("confirmation", "confirmation_whitebox_trace"):
        return snap.confirmation_whitebox_trace
    if m in ("evidence_hypothesis", "evidence_hypothesis_whitebox_trace"):
        return snap.evidence_hypothesis_whitebox_trace
    if m in ("experience_governance", "experience_governance_whitebox_trace"):
        return snap.experience_governance_whitebox_trace
    return None


def _apply_filters(snaps: List[ReasoningConsoleSnapshot], qs: Dict[str, List[str]]) -> List[ReasoningConsoleSnapshot]:
    view = (qs.get("view", ["all"])[0] or "all").strip().lower()
    if view == "blocked":
        return [s for s in snaps if s.blocked]
    if view == "issue":
        return [s for s in snaps if s.possible_issue_type]
    if view == "with_feedback":
        return [s for s in snaps if s.confirmation_input_raw_text]
    return snaps


class ReasoningConsoleAPIHandler(BaseHTTPRequestHandler):
    def _send(self, code: int, obj: Any) -> None:
        body = _json_bytes(obj)
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path or "/"
        qs = parse_qs(parsed.query or "")

        jsonl_path = resolve_default_jsonl_path()
        if not jsonl_path:
            self._send(404, {"error": "jsonl_not_found"})
            return

        snaps = load_snapshots_from_jsonl(jsonl_path)

        if path == "/api/reasoning/snapshots":
            snaps2 = _apply_filters(snaps, qs)
            items = []
            for s in snaps2[-200:]:
                items.append(
                    {
                        "id": s.snapshot_id,
                        "ts": s.ts,
                        "seq": s.seq,
                        "goal": s.current_goal,
                        "flow": s.current_flow_type,
                        "terminal_status": s.terminal_status,
                        "blocked": s.blocked,
                        "integration_summary": s.integration_summary,
                        "possible_issue_type": s.possible_issue_type,
                    }
                )
            self._send(200, {"jsonl_path": jsonl_path, "items": items})
            return

        if path.startswith("/api/reasoning/snapshots/") and "/whitebox/" not in path:
            snap_id = path.split("/")[-1]
            s = next((x for x in snaps if x.snapshot_id == snap_id), None)
            if not s:
                self._send(404, {"error": "snapshot_not_found", "id": snap_id})
                return
            self._send(200, s.to_dict())
            return

        if "/api/reasoning/snapshots/" in path and "/whitebox/" in path:
            parts = path.split("/")
            try:
                snap_id = parts[4]
                module = parts[6]
            except Exception:
                self._send(400, {"error": "bad_path"})
                return
            s = next((x for x in snaps if x.snapshot_id == snap_id), None)
            if not s:
                self._send(404, {"error": "snapshot_not_found", "id": snap_id})
                return
            wb = _pick_whitebox(s, module)
            if wb is None:
                self._send(404, {"error": "whitebox_not_found", "module": module})
                return
            self._send(200, {"id": snap_id, "module": module, "whitebox": wb})
            return

        if path == "/api/reasoning/issues":
            snaps2 = _apply_filters(snaps, qs)
            items = []
            for s in snaps2:
                if not s.possible_issue_type:
                    continue
                items.append(
                    {
                        "id": s.snapshot_id,
                        "ts": s.ts,
                        "seq": s.seq,
                        "issue_type": s.possible_issue_type,
                        "issue_reason": s.possible_issue_reason,
                        "suggested_debug_module": s.suggested_debug_module,
                        "flow": s.current_flow_type,
                        "goal": s.current_goal,
                        "blocked": s.blocked,
                    }
                )
            self._send(200, {"jsonl_path": jsonl_path, "items": items[-200:]})
            return

        self._send(404, {"error": "not_found", "path": path})

    def log_message(self, fmt, *args):  # noqa: A003
        return

