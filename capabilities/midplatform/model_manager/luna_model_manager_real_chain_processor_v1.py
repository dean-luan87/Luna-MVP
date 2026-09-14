# -*- coding: utf-8 -*-
"""Luna Model Manager Real Chain — planning processor v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.collaboration.real_chain.real_chain_orchestrator_v1 import (
    run_detector_unavailable_degradation,
    run_normal_shopfront_chain,
    run_ocr_failure_chain,
    run_qwen_unsupported_claim_chain,
)
from capabilities.midplatform.model_manager.luna_model_manager_real_chain_types_v1 import (
    CHAIN_ID,
    POLICY_REF,
)


def run_real_chain_planning(*, scenario: str = "normal_shopfront") -> Dict[str, Any]:
    dispatch = {
        "normal_shopfront": run_normal_shopfront_chain,
        "ocr_failure": run_ocr_failure_chain,
        "qwen_unsupported": run_qwen_unsupported_claim_chain,
        "detector_unavailable": run_detector_unavailable_degradation,
    }
    fn = dispatch.get(scenario, run_normal_shopfront_chain)
    result = fn()
    result["chain_id"] = CHAIN_ID
    result["policy_ref"] = POLICY_REF
    result["planning_only"] = True
    return result


def run_real_chain_planning_summary() -> Dict[str, Any]:
    return {
        "phase_ref": "Phase-P1-Midplatform-Luna-Model-Manager-Real-Multi-Model-Chain-Integration-Planning-v1-001",
        "model_os_frozen": True,
        "single_chain": CHAIN_ID,
        "slots": ["text_detection", "text_recognition", "context_reasoning"],
        "providers": ["detection_v1", "ocr_v1", "qwen_vl"],
        "not_in_scope": ["internvl", "gemini", "sam_target_discovery"],
        "candidate_only": True,
        "not_fact": True,
    }
