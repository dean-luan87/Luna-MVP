# -*- coding: utf-8 -*-
"""
Phase-Mainline-GuardedTrial-008 — OCR Stage-2 trial runner skeleton (skeleton only).

Hard scope:
- Default MUST NOT invoke any OCR provider.
- Default MUST NOT enable semantic interpretation.
- Default MUST NOT forward to MidPlatform.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, Optional

from capabilities.guarded_trial.ocr_stage2_trial_precheck_v0 import build_ocr_stage2_trial_id_v0


def build_ocr_stage2_trial_runner_plan_v0(
    *,
    trial_id: str,
    provider_execution_enabled: bool = False,
    semantic_interpretation_enabled: bool = False,
    midplatform_forward_enabled: bool = False,
) -> Dict[str, Any]:
    return {
        "runner_id": f"ocr_s2_runner_{uuid.uuid4().hex[:12]}",
        "trial_id": trial_id,
        "runner_mode": "skeleton_only",
        "provider_execution_enabled": bool(provider_execution_enabled),
        "semantic_interpretation_enabled": bool(semantic_interpretation_enabled),
        "midplatform_forward_enabled": bool(midplatform_forward_enabled),
        "request_trace_enabled": True,
        "abort_on_provider_error": True,
        "rollback_on_abort": True,
        "execution_result": "not_executed_skeleton_only",
    }


def run_ocr_stage2_trial_runner_skeleton_v0(*, trial_id: Optional[str] = None) -> Dict[str, Any]:
    tid = trial_id or build_ocr_stage2_trial_id_v0(prefix="ocr_s2_run")
    return build_ocr_stage2_trial_runner_plan_v0(
        trial_id=tid,
        provider_execution_enabled=False,
        semantic_interpretation_enabled=False,
        midplatform_forward_enabled=False,
    )

