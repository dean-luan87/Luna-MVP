# -*- coding: utf-8 -*-
"""Document Surface — Option B admission abort/rollback reviewer v1."""

from __future__ import annotations

from typing import Any, Dict, List


def review_abort_rollback(*, results: List[Dict[str, Any]]) -> Dict[str, Any]:
    blocked = [r for r in results if str(r.get("admission_status_candidate", "")).startswith("blocked")]
    per: List[Dict[str, Any]] = []
    for r in blocked:
        abort = r.get("abort_rollback") or {}
        ok = all([
            abort.get("abort_reason"),
            abort.get("next_action"),
            abort.get("forbidden_workaround"),
            abort.get("rollback_action"),
            abort.get("trace_retained") is True,
            abort.get("no_active_registry_update") is True,
            abort.get("no_runtime_activation") is True,
            abort.get("no_silent_fallback_to_option_a") is True,
            abort.get("no_fallback_to_ocr_vlm_layout") is True,
        ])
        per.append({
            "model_candidate_id": r.get("model_candidate_id"),
            "passed": ok,
            "abort_rollback": abort,
        })
    checks = {
        "blocked_count_6": len(blocked) == 6,
        "all_abort_complete": all(p.get("passed") for p in per),
        "no_active_registry_update": all((p.get("abort_rollback") or {}).get("no_active_registry_update") for p in per),
        "no_runtime_activation": all((p.get("abort_rollback") or {}).get("no_runtime_activation") for p in per),
        "no_silent_fallback": all((p.get("abort_rollback") or {}).get("no_silent_fallback_to_option_a") for p in per),
        "no_ocr_vlm_layout_fallback": all((p.get("abort_rollback") or {}).get("no_fallback_to_ocr_vlm_layout") for p in per),
        "trace_retained": all((p.get("abort_rollback") or {}).get("trace_retained") for p in per),
    }
    failed = [k for k, v in checks.items() if not v]
    return {
        "review_id": "option_b_abort_rollback_review",
        "passed": len(failed) == 0,
        "review_passed_count": sum(1 for v in checks.values() if v),
        "review_failed_count": len(failed),
        "checks": checks,
        "failed_checks": failed,
        "per_candidate": per,
        "candidate_only": True,
        "not_fact": True,
    }
