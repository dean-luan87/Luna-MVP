# -*- coding: utf-8 -*-
"""Document Surface — rollback policy preflight v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

ROLLBACK_KEYS = (
    "do_not_modify_runtime_registry",
    "do_not_activate_runtime",
    "do_not_expand_input_directory",
    "do_not_enable_ocr_vlm_fallback",
    "preserve_failure_trace",
)


def _load_rollback_policy(repo_root: Path) -> Dict[str, Any]:
    path = repo_root / "capabilities/midplatform/model_manager/runtime/document_surface/controlled_execution_planning/document_surface_rollback_policy_v1.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def run_rollback_policy_preflight(*, repo_root: Path) -> Dict[str, Any]:
    policy = _load_rollback_policy(repo_root)
    on_fail = policy.get("on_controlled_execution_failure") or {}
    handoff = on_fail.get("handoff_to") or []

    checks = {k: on_fail.get(k) is True for k in ROLLBACK_KEYS}
    handoff_ok = any(h in handoff for h in ("dependency_admission_review", "implementation_planning_review", "controlled_execution_planning"))

    return {
        "check_id": "rollback_policy_preflight_v1",
        "rollback_checks": checks,
        "handoff_targets": handoff,
        "handoff_ok": handoff_ok,
        "passed": all(checks.values()) and handoff_ok,
        "candidate_only": True,
        "not_fact": True,
    }
