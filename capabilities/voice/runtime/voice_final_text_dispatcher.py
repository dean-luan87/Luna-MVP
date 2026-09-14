# -*- coding: utf-8 -*-
"""
切段完成后的主分流入口（语音主线集成 v1）。

职责：在 VoiceInputEvent 已生成后，统一分流短链 / 长链 / reject；
短链止于 BridgeDecision；长链止于 run_long_input_task_planning_v1 → task_plan_v1。
"""

from __future__ import annotations

import os
import time
from dataclasses import replace
from typing import Any, Dict, List, Optional, Tuple

_CROSS_DOMAIN_ORCH_V1_ORDER: Tuple[str, ...] = (
    "risk_interrupt_v1",
    "sidewalk_nav_v1",
    "retail_find_item_v1",
)
_CROSS_DOMAIN_ORCH_V1_METADATA_KEYS: Tuple[str, ...] = _CROSS_DOMAIN_ORCH_V1_ORDER

from capabilities.voice.bridge.voice_input_to_bridge import voice_input_to_bridge_decision
from capabilities.voice.bridge.voice_long_input_task_planner import run_long_input_task_planning_v1
from capabilities.voice.config.voice_long_input_parse_config import get_default_voice_long_input_parse_config
from capabilities.voice.runtime.voice_final_text_dispatch_result import VoiceFinalTextDispatchResult
from capabilities.voice.runtime.voice_input_length_mode_classifier import classify_voice_input_length_mode
from capabilities.voice.runtime.voice_shortcut_registry import VoiceShortcutRegistry
from capabilities.voice.schemas.voice_input_event import VoiceInputEvent
from capabilities.voice.schemas.voice_input_rejection_result import VoiceInputRejectionResult
from capabilities.voice.schemas.voice_runtime_context import VoiceRuntimeContext
from capabilities.voice.schemas.speech_request import SpeechRequest
from capabilities.voice.observations.request_runtime_observation import RequestRuntimeObservation
from capabilities.voice.observations.output_decision_observation import OutputDecisionObservation
from capabilities.voice.observations.pilot_state_transition_observation import PilotStateTransitionObservation
from capabilities.voice.runtime.voice_navigation_handoff_v0 import (
    attempt_navigation_start_handoff_v0,
    consume_destination_bound_v0_in_handoff_v0,
)
from capabilities.voice.runtime.navigation_handoff_post_bound_execution_stub_v0 import (
    evaluate_navigation_handoff_post_bound_execution_stub_v0,
)
from capabilities.voice.runtime.voice_navigation_destination_eval_v0 import evaluate_destination_sufficiency_v0
from capabilities.voice.runtime.voice_navigation_destination_candidate_v0 import (
    capture_destination_candidate_v0,
)
from capabilities.voice.runtime.voice_navigation_destination_confirmation_fact_v0 import (
    evaluate_destination_confirmation_fact_check_v0,
)
from capabilities.voice.runtime.voice_navigation_destination_bound_check_v0 import (
    evaluate_destination_bound_check_v0,
)
from capabilities.voice.runtime.voice_navigation_destination_bound_upgrade_eval_v0 import (
    evaluate_destination_bound_upgrade_eval_v0,
)
from capabilities.voice.runtime.voice_navigation_destination_bound_materialization_eval_v0 import (
    evaluate_destination_bound_materialization_eval_v0,
)
from capabilities.voice.runtime.voice_navigation_destination_bound_v0 import (
    materialize_destination_bound_v0_if_allowed,
)
from capabilities.voice.runtime.voice_navigation_response_template_v0 import (
    NAVIGATION_MISSING_DESTINATION_CONFIRM_TEMPLATE_V0,
    should_trigger_navigation_missing_destination_confirm_v0,
)
from capabilities.voice.runtime.voice_response_submit_template_v0 import (
    ResponseTemplateIdV0,
    get_response_submit_template_spec_v0,
)
from capabilities.vision.runtime.vision_mid_platform_consume_stub_v0 import (
    consume_vision_consumable_slices_stub_v0,
)
from capabilities.vision.runtime.vision_mainline_minimal_wiring_v0 import (
    maybe_attach_vision_consumable_slices_v0_from_risk_summary_v1,
)
from capabilities.vision.runtime.vision_rerecognition_loop_v0 import (
    maybe_attach_vision_interpretation_candidates_v0_from_slices,
)
from capabilities.mid_platform.runtime.need_navigation_routing_v0 import (
    evaluate_need_navigation_routing_v0,
)
from capabilities.mid_platform.runtime.mid_platform_dispatch_consumption_stub_v0 import (
    consume_mid_platform_dispatch_consumption_stub_v0,
)
from capabilities.mid_platform.runtime.mid_platform_formal_decision_stub_v0 import (
    evaluate_mid_platform_formal_decision_stub_v0,
)
from capabilities.mid_platform.runtime.formal_decision_gate_inputs_v0 import (
    read_formal_decision_gate_inputs_v0,
)
from capabilities.mid_platform.runtime.formal_decision_handoff_gates_v0 import (
    build_formal_decision_handoff_gates_v0,
)
from capabilities.mid_platform.runtime.formal_decision_information_gates_v0 import (
    build_formal_decision_information_gates_v0,
)
from capabilities.mid_platform.runtime.navigation_real_execution_readiness_gate_inputs_v0 import (
    read_navigation_real_execution_readiness_gate_inputs_v0,
)
from capabilities.mid_platform.runtime.navigation_real_execution_readiness_gate_stub_v0 import (
    evaluate_navigation_real_execution_readiness_gate_stub_v0,
)
from capabilities.mid_platform.runtime.navigation_executor_takeover_stub_v0 import (
    evaluate_navigation_executor_takeover_stub_v0,
)
from capabilities.mid_platform.runtime.navigation_real_executor_input_object_v0 import (
    evaluate_navigation_real_executor_input_object_v0,
)
from capabilities.mid_platform.runtime.navigation_real_executor_status_placeholder_v0 import (
    evaluate_navigation_real_executor_status_placeholder_v0,
)
from capabilities.mid_platform.runtime.navigation_real_executor_status_object_v0 import (
    evaluate_navigation_real_executor_status_object_v0,
)
from capabilities.mid_platform.runtime.navigation_execution_monitoring_status_placeholder_v0 import (
    evaluate_navigation_execution_monitoring_status_placeholder_v0,
)
from capabilities.mid_platform.runtime.navigation_execution_monitoring_status_v0 import (
    evaluate_navigation_execution_monitoring_status_v0,
)
from capabilities.mid_platform.runtime.navigation_executor_takeover_wiring_v0 import (
    evaluate_navigation_executor_takeover_wiring_v0,
)
from capabilities.mid_platform.runtime.navigation_rollback_and_interruption_governance_entry_v0 import (
    evaluate_navigation_rollback_and_interruption_governance_entry_v0,
)
from capabilities.mid_platform.runtime.navigation_rollback_and_interruption_governance_decision_v0 import (
    evaluate_navigation_rollback_and_interruption_governance_decision_v0,
)
from capabilities.mid_platform.runtime.navigation_governance_action_boundary_v0 import (
    evaluate_navigation_governance_action_boundary_v0,
)
from capabilities.mid_platform.runtime.navigation_governance_action_approval_boundary_v0 import (
    evaluate_navigation_governance_action_approval_boundary_v0,
)
from capabilities.governance.runtime.navigation_governance_action_status_v0 import (
    evaluate_navigation_governance_action_status_v0,
)
from capabilities.governance.runtime.navigation_governance_action_executor_input_v0 import (
    evaluate_navigation_governance_action_executor_input_v0,
)
from capabilities.governance.runtime.navigation_governance_action_approval_status_v0 import (
    evaluate_navigation_governance_action_approval_status_v0,
)
from capabilities.mid_platform.runtime.navigation_governance_action_executor_readiness_gate_v0 import (
    evaluate_navigation_governance_action_executor_readiness_gate_v0,
)
from capabilities.mid_platform.runtime.navigation_governance_action_executor_wiring_v0 import (
    evaluate_navigation_governance_action_executor_wiring_v0,
)
from capabilities.governance.runtime.navigation_governance_action_release_control_input_v0 import (
    evaluate_navigation_governance_action_release_control_input_v0,
)
from capabilities.governance.runtime.navigation_governance_action_release_control_status_v0 import (
    evaluate_navigation_governance_action_release_control_status_v0,
)
from capabilities.mid_platform.runtime.navigation_governance_action_release_control_readiness_gate_v0 import (
    evaluate_navigation_governance_action_release_control_readiness_gate_v0,
)
from capabilities.mid_platform.runtime.navigation_governance_action_release_control_wiring_v0 import (
    evaluate_navigation_governance_action_release_control_wiring_v0,
)
from capabilities.governance.runtime.navigation_governance_action_release_control_result_v0 import (
    evaluate_navigation_governance_action_release_control_result_v0,
)
from capabilities.mid_platform.runtime.navigation_governance_action_release_control_executor_input_bridge_v0 import (
    evaluate_navigation_governance_action_release_control_executor_input_bridge_v0,
)
from capabilities.mid_platform.runtime.navigation_governance_action_release_control_live_release_gate_v0 import (
    evaluate_navigation_governance_action_release_control_live_release_gate_v0,
)
from capabilities.mid_platform.runtime.navigation_governance_action_release_control_side_effect_release_gate_v0 import (
    evaluate_navigation_governance_action_release_control_side_effect_release_gate_v0,
)
from capabilities.mid_platform.runtime.navigation_governance_action_release_control_first_live_enablement_approval_gate_v0 import (
    evaluate_navigation_governance_action_release_control_first_live_enablement_approval_gate_v0,
)
from capabilities.mid_platform.runtime.navigation_governance_action_release_control_first_live_launch_dry_run_v0 import (
    evaluate_navigation_governance_action_release_control_first_live_launch_dry_run_v0,
)
from capabilities.governance.runtime.navigation_governance_action_release_control_minimal_executor_v0 import (
    get_release_control_minimal_executor_identity,
)
from capabilities.governance.runtime.navigation_governance_action_release_control_guarded_live_stub_v0 import (
    accept_guarded_live_input,
    get_release_control_guarded_live_identity,
)
from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_enablement_dry_run_stub_v0 import (
    evaluate_enablement_dry_run_preconditions,
)
from capabilities.governance.runtime.navigation_governance_action_release_control_execution_state_v0 import (
    evaluate_navigation_governance_action_release_control_execution_state_v0,
)


def _env_truthy(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in ("1", "true", "yes")


def _maybe_consume_vision_slices_mid_platform_stub_v0(
    res: VoiceFinalTextDispatchResult,
    *,
    runtime_context: Optional[VoiceRuntimeContext],
) -> VoiceFinalTextDispatchResult:
    """
    Mid-platform consume stub v0 (read-only).

    Hard boundary:
    - Does NOT change dispatch/route/proposal.
    - Only attaches an observation to result.metadata when slices exist.
    """
    if runtime_context is None:
        return res
    try:
        md_rc = runtime_context.metadata or {}
        slices = md_rc.get("vision_consumable_slices_v0")
        candidates = md_rc.get("vision_interpretation_candidates_v0")
        applicable, obs = consume_vision_consumable_slices_stub_v0(slices=slices, candidates=candidates)
        if not applicable or not isinstance(obs, dict):
            return res
        md = dict(res.metadata or {})
        md["vision_mid_platform_consume_stub_v0"] = obs
        return replace(res, metadata=md)
    except Exception:
        return res


def _attach_need_navigation_routing_v0(
    res: VoiceFinalTextDispatchResult,
    *,
    event: VoiceInputEvent,
    bridge_decision: Any,
    runtime_context: Optional[VoiceRuntimeContext],
) -> VoiceFinalTextDispatchResult:
    """
    Need-Navigation Routing v0 (read-only suggestion).
    Always attaches a minimal suggestion payload for observability.
    """
    try:
        md_rc = (runtime_context.metadata or {}) if runtime_context is not None else {}
        payload = evaluate_need_navigation_routing_v0(
            proposal=getattr(bridge_decision, "proposal", None),
            route=getattr(bridge_decision, "route", None),
            raw_text=str(getattr(event, "raw_text", "") or ""),
            runtime_context_metadata=md_rc if isinstance(md_rc, dict) else {},
        )
        md = dict(res.metadata or {})
        md["need_navigation_routing_v0"] = payload
        return replace(res, metadata=md)
    except Exception:
        return res


def _maybe_consume_mid_platform_dispatch_consumption_stub_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Mid-platform dispatch consumption stub v0 (read-only).

    relevant-only:
    - If need_navigation_routing_v0 missing => do not write.
    """
    try:
        md0 = dict(res.metadata or {})
        n = md0.get("need_navigation_routing_v0")
        applicable, obs = consume_mid_platform_dispatch_consumption_stub_v0(need_navigation_routing_v0=n)
        if not applicable or not isinstance(obs, dict):
            return res
        md0["mid_platform_dispatch_consumption_stub_v0"] = obs
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_mid_platform_formal_decision_stub_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Mid-platform formal decision stub v0 (read-only).

    relevant-only:
    - requires need_navigation_routing_v0 to exist.
    """
    try:
        md0 = dict(res.metadata or {})
        applicable, payload = evaluate_mid_platform_formal_decision_stub_v0(
            need_navigation_routing_v0=md0.get("need_navigation_routing_v0"),
            mid_platform_dispatch_consumption_stub_v0=md0.get("mid_platform_dispatch_consumption_stub_v0"),
            destination_bound_v0=md0.get("destination_bound_v0"),
            navigation_handoff_consume_bound_v0=md0.get("navigation_handoff_consume_bound_v0"),
            navigation_handoff_post_bound_execution_stub_v0=md0.get("navigation_handoff_post_bound_execution_stub_v0"),
            formal_decision_gate_inputs_v0=md0.get("formal_decision_gate_inputs_v0"),
            formal_decision_handoff_gates_v0=md0.get("formal_decision_handoff_gates_v0"),
            formal_decision_information_gates_v0=md0.get("formal_decision_information_gates_v0"),
        )
        if not applicable or not isinstance(payload, dict):
            return res
        md0["mid_platform_formal_decision_stub_v0"] = payload
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_formal_decision_allow_progress_path_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Narrow allow-progress path observation (read-only).

    Only writes when formal decision stub outputs allow_progress.
    Does NOT trigger navigation execution; only records the intended downstream placeholder interface.
    """
    try:
        md0 = dict(res.metadata or {})
        fd = md0.get("mid_platform_formal_decision_stub_v0")
        if not isinstance(fd, dict):
            return res
        if str(fd.get("decision_scope") or "") != "mid_platform_formal_decision_stub_v0":
            return res
        if str(fd.get("decision_result") or "") != "allow_progress":
            return res
        md0["formal_decision_allow_progress_path_v0"] = {
            "allow_progress_path_present": True,
            "downstream_placeholder_interface": "navigation_handoff_post_bound_execution_stub_v0",
            "consume_mode": "read_only",
        }
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_mid_platform_formal_decision_gate_inputs_v0(
    res: VoiceFinalTextDispatchResult,
    *,
    runtime_context: Optional[VoiceRuntimeContext],
) -> VoiceFinalTextDispatchResult:
    """
    Formal decision gate inputs v0 (read-only observation).

    relevant-only:
    - writes only when at least one gate input exists (safety/task_validity).
    """
    if runtime_context is None:
        return res
    try:
        md_rc = runtime_context.metadata or {}
        applicable, payload = read_formal_decision_gate_inputs_v0(
            runtime_context_metadata=md_rc if isinstance(md_rc, dict) else {},
        )
        if not applicable or not isinstance(payload, dict):
            return res
        md0 = dict(res.metadata or {})
        md0["formal_decision_gate_inputs_v0"] = payload
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_formal_decision_handoff_gates_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Formal decision handoff gates v0 (read-only observation).

    relevant-only:
    - writes only when at least one handoff-chain input exists.
    """
    try:
        md0 = dict(res.metadata or {})
        applicable, payload = build_formal_decision_handoff_gates_v0(
            destination_bound_v0=md0.get("destination_bound_v0"),
            navigation_handoff_consume_bound_v0=md0.get("navigation_handoff_consume_bound_v0"),
            navigation_handoff_post_bound_execution_stub_v0=md0.get("navigation_handoff_post_bound_execution_stub_v0"),
        )
        if not applicable or not isinstance(payload, dict):
            return res
        md0["formal_decision_handoff_gates_v0"] = payload
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_formal_decision_information_gates_v0(
    res: VoiceFinalTextDispatchResult,
    *,
    task_action: str,
) -> VoiceFinalTextDispatchResult:
    """
    Formal decision information sufficiency gates v0 (read-only observation).

    relevant-only:
    - writes only when task context exists or candidate/hand-off inputs exist.
    """
    try:
        md0 = dict(res.metadata or {})
        applicable, payload = build_formal_decision_information_gates_v0(
            task_action=str(task_action or ""),
            destination_bound_v0=md0.get("destination_bound_v0"),
            navigation_handoff_consume_bound_v0=md0.get("navigation_handoff_consume_bound_v0"),
            navigation_handoff_post_bound_execution_stub_v0=md0.get("navigation_handoff_post_bound_execution_stub_v0"),
        )
        if not applicable or not isinstance(payload, dict):
            return res
        md0["formal_decision_information_gates_v0"] = payload
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_real_execution_readiness_gate_inputs_v0(
    res: VoiceFinalTextDispatchResult,
    *,
    runtime_context: Optional[VoiceRuntimeContext],
) -> VoiceFinalTextDispatchResult:
    """
    Navigation real execution readiness gate inputs v0 (read-only observation).

    relevant-only:
    - writes only when at least one readiness gate input object exists in runtime_context.metadata.
    """
    if runtime_context is None:
        return res
    try:
        md_rc = runtime_context.metadata or {}
        applicable, payload = read_navigation_real_execution_readiness_gate_inputs_v0(
            runtime_context_metadata=md_rc if isinstance(md_rc, dict) else {},
        )
        if not applicable or not isinstance(payload, dict):
            return res
        md0 = dict(res.metadata or {})
        md0["navigation_real_execution_readiness_gate_inputs_v0"] = payload
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_real_execution_readiness_gate_stub_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Navigation real execution readiness gate stub v0 (read-only).

    Input:
    - result.metadata["navigation_real_execution_readiness_gate_inputs_v0"]

    relevant-only:
    - If inputs missing => do not write.
    """
    try:
        md0 = dict(res.metadata or {})
        applicable, payload = evaluate_navigation_real_execution_readiness_gate_stub_v0(
            navigation_real_execution_readiness_gate_inputs_v0=md0.get("navigation_real_execution_readiness_gate_inputs_v0"),
        )
        if not applicable or not isinstance(payload, dict):
            return res
        md0["navigation_real_execution_readiness_gate_stub_v0"] = payload
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_executor_takeover_stub_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Navigation executor takeover stub v0 (read-only).

    Inputs (read-only):
    - mid_platform_formal_decision_stub_v0
    - formal_decision_allow_progress_path_v0
    - navigation_handoff_post_bound_execution_stub_v0 (or future consumption result key)
    - navigation_real_execution_readiness_gate_stub_v0

    relevant-only:
    - If none of the key inputs exist => do not write.
    """
    try:
        md0 = dict(res.metadata or {})
        applicable, payload = evaluate_navigation_executor_takeover_stub_v0(
            mid_platform_formal_decision_stub_v0=md0.get("mid_platform_formal_decision_stub_v0"),
            formal_decision_allow_progress_path_v0=md0.get("formal_decision_allow_progress_path_v0"),
            navigation_handoff_post_bound_execution_stub_v0=md0.get("navigation_handoff_post_bound_execution_stub_v0"),
            navigation_real_execution_readiness_gate_stub_v0=md0.get(
                "navigation_real_execution_readiness_gate_stub_v0"
            ),
            destination_bound_v0=md0.get("destination_bound_v0"),
            navigation_handoff_consume_bound_v0=md0.get("navigation_handoff_consume_bound_v0"),
            navigation_handoff_post_bound_execution_stub_consumption_v0=md0.get(
                "navigation_handoff_post_bound_execution_stub_consumption_v0"
            ),
        )
        if not applicable or not isinstance(payload, dict):
            return res
        md0["navigation_executor_takeover_stub_v0"] = payload
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_real_executor_input_object_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Navigation real executor input object v0 (implemented object; read-only).

    Writes:
    - result.metadata["navigation_real_executor_input_v0"]

    relevant-only:
    - Requires ALL upstream evidence to exist and match narrow conditions.
    """
    try:
        md0 = dict(res.metadata or {})
        applicable, payload = evaluate_navigation_real_executor_input_object_v0(
            mid_platform_formal_decision_stub_v0=md0.get("mid_platform_formal_decision_stub_v0"),
            formal_decision_allow_progress_path_v0=md0.get("formal_decision_allow_progress_path_v0"),
            navigation_real_execution_readiness_gate_stub_v0=md0.get(
                "navigation_real_execution_readiness_gate_stub_v0"
            ),
            navigation_executor_takeover_stub_v0=md0.get("navigation_executor_takeover_stub_v0"),
        )
        if not applicable or not isinstance(payload, dict):
            return res
        md0["navigation_real_executor_input_v0"] = payload
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_real_executor_status_object_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Navigation real executor status object v0 (implemented object; read-only).

    Writes:
    - result.metadata["navigation_real_executor_status_v0"]

    relevant-only:
    - Requires BOTH navigation_executor_takeover_stub_v0 and navigation_real_executor_input_v0.
    """
    try:
        md0 = dict(res.metadata or {})
        applicable, payload = evaluate_navigation_real_executor_status_object_v0(
            navigation_executor_takeover_stub_v0=md0.get("navigation_executor_takeover_stub_v0"),
            navigation_real_executor_input_v0=md0.get("navigation_real_executor_input_v0"),
            navigation_real_execution_readiness_gate_stub_v0=md0.get(
                "navigation_real_execution_readiness_gate_stub_v0"
            ),
        )
        if not applicable or not isinstance(payload, dict):
            return res
        md0["navigation_real_executor_status_v0"] = payload
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_execution_monitoring_status_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Navigation execution monitoring status v0 (implemented object; minimal monitoring loop).

    Writes:
    - result.metadata["navigation_execution_monitoring_status_v0"]

    relevant-only:
    - Requires BOTH navigation_executor_takeover_stub_v0 and navigation_real_executor_status_v0.
    """
    try:
        md0 = dict(res.metadata or {})
        applicable, payload = evaluate_navigation_execution_monitoring_status_v0(
            navigation_real_executor_status_v0=md0.get("navigation_real_executor_status_v0"),
            navigation_executor_takeover_stub_v0=md0.get("navigation_executor_takeover_stub_v0"),
            navigation_real_executor_input_v0=md0.get("navigation_real_executor_input_v0"),
        )
        if not applicable or not isinstance(payload, dict):
            return res
        md0["navigation_execution_monitoring_status_v0"] = payload
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_executor_takeover_wiring_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Navigation executor takeover wiring v0 (minimal implementation; non-action).

    Writes:
    - result.metadata["navigation_executor_takeover_wiring_v0"]

    relevant-only:
    - If none of the key upstream evidence exists => do not write.
    """
    try:
        md0 = dict(res.metadata or {})
        applicable, payload = evaluate_navigation_executor_takeover_wiring_v0(
            mid_platform_formal_decision_stub_v0=md0.get("mid_platform_formal_decision_stub_v0"),
            formal_decision_allow_progress_path_v0=md0.get("formal_decision_allow_progress_path_v0"),
            navigation_handoff_post_bound_execution_stub_v0=md0.get("navigation_handoff_post_bound_execution_stub_v0"),
            navigation_handoff_post_bound_execution_stub_consumption_v0=md0.get(
                "navigation_handoff_post_bound_execution_stub_consumption_v0"
            ),
            navigation_real_execution_readiness_gate_stub_v0=md0.get("navigation_real_execution_readiness_gate_stub_v0"),
            navigation_executor_takeover_stub_v0=md0.get("navigation_executor_takeover_stub_v0"),
            navigation_real_executor_input_v0=md0.get("navigation_real_executor_input_v0"),
            navigation_real_executor_status_v0=md0.get("navigation_real_executor_status_v0"),
            navigation_execution_monitoring_status_v0=md0.get("navigation_execution_monitoring_status_v0"),
        )
        if not applicable or not isinstance(payload, dict):
            return res

        md0["navigation_executor_takeover_wiring_v0"] = payload

        # Optional: call executor skeleton wiring interface (still non-action).
        try:
            from capabilities.navigation.runtime.navigation_real_executor_v0 import (  # noqa: E402
                wire_executor_takeover,
            )

            st = str(payload.get("wiring_status") or "")
            if st in ("wired_ready_to_takeover", "wired_inactive"):
                _ = wire_executor_takeover(
                    wiring_status=st,
                    wiring_reason=str(payload.get("reason") or ""),
                )
        except Exception:
            pass

        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_rollback_and_interruption_governance_entry_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Navigation rollback/interruption governance entry v0 (minimal implementation; non-action).

    Writes:
    - result.metadata["navigation_rollback_and_interruption_governance_entry_v0"]

    Policy:
    - If both standardized objects exist (executor status + monitoring status) => write tri-state result.
    - If neither exists => relevant-only (do not write).
    """
    try:
        md0 = dict(res.metadata or {})
        applicable, payload = evaluate_navigation_rollback_and_interruption_governance_entry_v0(
            navigation_real_executor_status_v0=md0.get("navigation_real_executor_status_v0"),
            navigation_execution_monitoring_status_v0=md0.get("navigation_execution_monitoring_status_v0"),
            navigation_executor_takeover_wiring_v0=md0.get("navigation_executor_takeover_wiring_v0"),
        )
        if not applicable or not isinstance(payload, dict):
            return res
        md0["navigation_rollback_and_interruption_governance_entry_v0"] = payload
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_rollback_and_interruption_governance_decision_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Navigation rollback/interruption governance decision v0 (minimal implementation; non-action).

    Writes:
    - result.metadata["navigation_rollback_and_interruption_governance_decision_v0"]

    Policy:
    - Requires governance entry object present and status == governance_entry_open.
    - If entry missing or not open => relevant-only (do not write).
    """
    try:
        md0 = dict(res.metadata or {})
        applicable, payload = evaluate_navigation_rollback_and_interruption_governance_decision_v0(
            navigation_rollback_and_interruption_governance_entry_v0=md0.get(
                "navigation_rollback_and_interruption_governance_entry_v0"
            ),
            navigation_real_executor_status_v0=md0.get("navigation_real_executor_status_v0"),
            navigation_execution_monitoring_status_v0=md0.get("navigation_execution_monitoring_status_v0"),
            navigation_executor_takeover_wiring_v0=md0.get("navigation_executor_takeover_wiring_v0"),
        )
        if not applicable or not isinstance(payload, dict):
            return res
        md0["navigation_rollback_and_interruption_governance_decision_v0"] = payload
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_boundary_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Navigation governance action boundary v0 (minimal implementation; non-action).

    Writes:
    - result.metadata["navigation_governance_action_boundary_v0"]

    Policy:
    - Requires governance decision object present and valid.
    - If decision missing => relevant-only (do not write).
    """
    try:
        md0 = dict(res.metadata or {})
        applicable, payload = evaluate_navigation_governance_action_boundary_v0(
            navigation_rollback_and_interruption_governance_decision_v0=md0.get(
                "navigation_rollback_and_interruption_governance_decision_v0"
            ),
            navigation_rollback_and_interruption_governance_entry_v0=md0.get(
                "navigation_rollback_and_interruption_governance_entry_v0"
            ),
            navigation_real_executor_status_v0=md0.get("navigation_real_executor_status_v0"),
            navigation_execution_monitoring_status_v0=md0.get("navigation_execution_monitoring_status_v0"),
        )
        if not applicable or not isinstance(payload, dict):
            return res
        md0["navigation_governance_action_boundary_v0"] = payload
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_approval_boundary_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Navigation governance action approval boundary v0 (minimal implementation; non-action).

    Writes:
    - result.metadata["navigation_governance_action_approval_boundary_v0"]

    Policy:
    - Requires valid navigation_governance_action_boundary_v0.
    - If missing => relevant-only (do not write).

    Optional: executor skeleton recognition (still non-action).
    """
    try:
        md0 = dict(res.metadata or {})
        applicable, payload = evaluate_navigation_governance_action_approval_boundary_v0(
            navigation_governance_action_boundary_v0=md0.get("navigation_governance_action_boundary_v0"),
            navigation_rollback_and_interruption_governance_decision_v0=md0.get(
                "navigation_rollback_and_interruption_governance_decision_v0"
            ),
            navigation_rollback_and_interruption_governance_entry_v0=md0.get(
                "navigation_rollback_and_interruption_governance_entry_v0"
            ),
            navigation_real_executor_status_v0=md0.get("navigation_real_executor_status_v0"),
            navigation_execution_monitoring_status_v0=md0.get("navigation_execution_monitoring_status_v0"),
        )
        if not applicable or not isinstance(payload, dict):
            return res
        md0["navigation_governance_action_approval_boundary_v0"] = payload
        try:
            from capabilities.governance.runtime.navigation_governance_action_executor_v0 import (  # noqa: E402
                accept_governance_action_approval_boundary,
            )

            _ = accept_governance_action_approval_boundary(
                navigation_governance_action_approval_boundary_v0=payload,
            )
        except Exception:
            pass
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_approval_status_object_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Navigation governance action approval status object v0 (implemented object; read-only; non-action).

    Writes:
    - result.metadata["navigation_governance_action_approval_status_v0"]

    Policy:
    - Requires valid navigation_governance_action_approval_boundary_v0.
    - If missing => relevant-only (do not write).
    """
    try:
        md0 = dict(res.metadata or {})
        applicable, payload = evaluate_navigation_governance_action_approval_status_v0(
            navigation_governance_action_approval_boundary_v0=md0.get(
                "navigation_governance_action_approval_boundary_v0"
            ),
            navigation_governance_action_boundary_v0=md0.get("navigation_governance_action_boundary_v0"),
            navigation_governance_action_executor_input_v0=md0.get(
                "navigation_governance_action_executor_input_v0"
            ),
        )
        if not applicable or not isinstance(payload, dict):
            return res
        md0["navigation_governance_action_approval_status_v0"] = payload
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_executor_input_object_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Navigation governance action executor input object v0 (implemented object; read-only; non-action).

    Writes:
    - result.metadata["navigation_governance_action_executor_input_v0"]

    Policy:
    - Requires valid approval boundary object + governance action executor skeleton identity.
    - If prerequisites missing => relevant-only (do not write).

    Optional: call executor skeleton recognition interface (still non-action).
    """
    try:
        md0 = dict(res.metadata or {})
        applicable, payload = evaluate_navigation_governance_action_executor_input_v0(
            navigation_governance_action_approval_boundary_v0=md0.get(
                "navigation_governance_action_approval_boundary_v0"
            ),
            navigation_governance_action_boundary_v0=md0.get("navigation_governance_action_boundary_v0"),
            navigation_rollback_and_interruption_governance_decision_v0=md0.get(
                "navigation_rollback_and_interruption_governance_decision_v0"
            ),
        )
        if not applicable or not isinstance(payload, dict):
            return res
        md0["navigation_governance_action_executor_input_v0"] = payload
        try:
            from capabilities.governance.runtime.navigation_governance_action_executor_v0 import (  # noqa: E402
                accept_governance_action_executor_input_object,
            )

            _ = accept_governance_action_executor_input_object(
                navigation_governance_action_executor_input_v0=payload,
            )
        except Exception:
            pass
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_status_object_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Navigation governance action status object v0 (implemented object; read-only; non-action).

    Writes:
    - result.metadata["navigation_governance_action_status_v0"]

    Policy:
    - Requires valid navigation_governance_action_boundary_v0 + governance action executor skeleton identity.
    - If prerequisites missing => relevant-only (do not write).

    Optional: call executor skeleton recognition interface (still non-action).
    """
    try:
        md0 = dict(res.metadata or {})
        applicable, payload = evaluate_navigation_governance_action_status_v0(
            navigation_governance_action_boundary_v0=md0.get("navigation_governance_action_boundary_v0"),
            navigation_rollback_and_interruption_governance_decision_v0=md0.get(
                "navigation_rollback_and_interruption_governance_decision_v0"
            ),
        )
        if not applicable or not isinstance(payload, dict):
            return res
        md0["navigation_governance_action_status_v0"] = payload
        try:
            from capabilities.governance.runtime.navigation_governance_action_executor_v0 import (  # noqa: E402
                accept_governance_action_status_object,
            )

            _ = accept_governance_action_status_object(
                navigation_governance_action_status_v0=payload,
            )
        except Exception:
            pass
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_executor_readiness_gate_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Navigation governance action executor readiness gate v0 (minimal implementation; non-action).

    Writes:
    - result.metadata["navigation_governance_action_executor_readiness_gate_v0"]

    Policy (minimal):
    - relevant-only: requires valid implemented executor input object; otherwise do not write.
    - Consumes only standardized objects already attached in metadata.
    """
    try:
        md0 = dict(res.metadata or {})
        applicable, payload = evaluate_navigation_governance_action_executor_readiness_gate_v0(
            navigation_governance_action_executor_input_v0=md0.get(
                "navigation_governance_action_executor_input_v0"
            ),
            navigation_governance_action_status_v0=md0.get("navigation_governance_action_status_v0"),
            navigation_governance_action_approval_status_v0=md0.get(
                "navigation_governance_action_approval_status_v0"
            ),
            navigation_governance_action_approval_boundary_v0=md0.get(
                "navigation_governance_action_approval_boundary_v0"
            ),
        )
        if not applicable or not isinstance(payload, dict):
            return res
        md0["navigation_governance_action_executor_readiness_gate_v0"] = payload
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_executor_wiring_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Navigation governance action executor wiring v0 (minimal implementation; non-action).

    Writes:
    - result.metadata["navigation_governance_action_executor_wiring_v0"]

    Policy:
    - relevant-only when neither executor input nor readiness gate present.
    - Optional: executor skeleton wiring recognition (still non-action).
    """
    try:
        md0 = dict(res.metadata or {})
        applicable, payload = evaluate_navigation_governance_action_executor_wiring_v0(
            navigation_governance_action_executor_input_v0=md0.get(
                "navigation_governance_action_executor_input_v0"
            ),
            navigation_governance_action_status_v0=md0.get("navigation_governance_action_status_v0"),
            navigation_governance_action_approval_status_v0=md0.get(
                "navigation_governance_action_approval_status_v0"
            ),
            navigation_governance_action_executor_readiness_gate_v0=md0.get(
                "navigation_governance_action_executor_readiness_gate_v0"
            ),
            navigation_governance_action_approval_boundary_v0=md0.get(
                "navigation_governance_action_approval_boundary_v0"
            ),
        )
        if not applicable or not isinstance(payload, dict):
            return res
        md0["navigation_governance_action_executor_wiring_v0"] = payload
        try:
            from capabilities.governance.runtime.navigation_governance_action_executor_v0 import (  # noqa: E402
                wire_governance_action_executor,
            )

            _ = wire_governance_action_executor(
                navigation_governance_action_executor_wiring_v0=payload,
            )
        except Exception:
            pass
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_release_control_input_object_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Release control input contract object v0 (implemented object; read-only; non-action).

    Writes:
    - result.metadata["navigation_governance_action_release_control_input_v0"]

    Policy:
    - relevant-only: requires implemented executor input + readiness gate + wiring.
    - Requires approved_action_type == release_control.
    """
    try:
        md0 = dict(res.metadata or {})
        applicable, payload = evaluate_navigation_governance_action_release_control_input_v0(
            navigation_governance_action_executor_input_v0=md0.get(
                "navigation_governance_action_executor_input_v0"
            ),
            navigation_governance_action_executor_readiness_gate_v0=md0.get(
                "navigation_governance_action_executor_readiness_gate_v0"
            ),
            navigation_governance_action_executor_wiring_v0=md0.get(
                "navigation_governance_action_executor_wiring_v0"
            ),
            navigation_governance_action_approval_status_v0=md0.get(
                "navigation_governance_action_approval_status_v0"
            ),
            navigation_governance_action_status_v0=md0.get("navigation_governance_action_status_v0"),
        )
        if not applicable or not isinstance(payload, dict):
            return res
        md0["navigation_governance_action_release_control_input_v0"] = payload
        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_v0 import (  # noqa: E402
                accept_release_control_input_object,
            )

            _ = accept_release_control_input_object(
                navigation_governance_action_release_control_input_v0=payload,
            )
        except Exception:
            pass
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_release_control_status_object_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Release control status object v0 (implemented object; read-only; non-action).

    Writes:
    - result.metadata["navigation_governance_action_release_control_status_v0"]

    Policy:
    - relevant-only: requires release_control input placeholder + wiring.
    - Optional: reads governance action status + readiness gate for consistency observation only.
    """
    try:
        md0 = dict(res.metadata or {})
        applicable, payload = evaluate_navigation_governance_action_release_control_status_v0(
            navigation_governance_action_release_control_input_v0=md0.get(
                "navigation_governance_action_release_control_input_v0"
            ),
            navigation_governance_action_executor_wiring_v0=md0.get(
                "navigation_governance_action_executor_wiring_v0"
            ),
            navigation_governance_action_status_v0=md0.get("navigation_governance_action_status_v0"),
            navigation_governance_action_executor_readiness_gate_v0=md0.get(
                "navigation_governance_action_executor_readiness_gate_v0"
            ),
        )
        if not applicable or not isinstance(payload, dict):
            return res
        md0["navigation_governance_action_release_control_status_v0"] = payload
        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_v0 import (  # noqa: E402
                accept_release_control_status_object,
            )

            _ = accept_release_control_status_object(
                navigation_governance_action_release_control_status_v0=payload,
            )
        except Exception:
            pass
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_release_control_readiness_gate_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Release control readiness gate v0 (minimal implementation; non-action).

    Writes:
    - result.metadata["navigation_governance_action_release_control_readiness_gate_v0"]

    Policy:
    - relevant-only: requires valid implemented release_control input object; otherwise do not write.
    """
    try:
        md0 = dict(res.metadata or {})
        applicable, payload = evaluate_navigation_governance_action_release_control_readiness_gate_v0(
            navigation_governance_action_release_control_input_v0=md0.get(
                "navigation_governance_action_release_control_input_v0"
            ),
            navigation_governance_action_release_control_status_v0=md0.get(
                "navigation_governance_action_release_control_status_v0"
            ),
            navigation_governance_action_executor_wiring_v0=md0.get(
                "navigation_governance_action_executor_wiring_v0"
            ),
            navigation_governance_action_executor_readiness_gate_v0=md0.get(
                "navigation_governance_action_executor_readiness_gate_v0"
            ),
            navigation_governance_action_approval_status_v0=md0.get(
                "navigation_governance_action_approval_status_v0"
            ),
        )
        if not applicable or not isinstance(payload, dict):
            return res
        md0["navigation_governance_action_release_control_readiness_gate_v0"] = payload
        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_v0 import (  # noqa: E402
                accept_release_control_readiness_gate,
            )

            _ = accept_release_control_readiness_gate(
                navigation_governance_action_release_control_readiness_gate_v0=payload
            )
        except Exception:
            pass
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_release_control_wiring_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Release control wiring v0 (minimal implementation; non-action).

    Writes:
    - result.metadata["navigation_governance_action_release_control_wiring_v0"]

    Policy:
    - relevant-only when neither input object nor readiness gate present.
    - Optional: call release_control skeleton wiring recognition interface (still non-action).
    """
    try:
        md0 = dict(res.metadata or {})
        applicable, payload = evaluate_navigation_governance_action_release_control_wiring_v0(
            navigation_governance_action_release_control_input_v0=md0.get(
                "navigation_governance_action_release_control_input_v0"
            ),
            navigation_governance_action_release_control_status_v0=md0.get(
                "navigation_governance_action_release_control_status_v0"
            ),
            navigation_governance_action_release_control_readiness_gate_v0=md0.get(
                "navigation_governance_action_release_control_readiness_gate_v0"
            ),
            navigation_governance_action_executor_wiring_v0=md0.get(
                "navigation_governance_action_executor_wiring_v0"
            ),
            navigation_governance_action_approval_status_v0=md0.get(
                "navigation_governance_action_approval_status_v0"
            ),
        )
        if not applicable or not isinstance(payload, dict):
            return res
        md0["navigation_governance_action_release_control_wiring_v0"] = payload
        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_v0 import (  # noqa: E402
                wire_release_control,
            )

            _ = wire_release_control(
                navigation_governance_action_release_control_wiring_v0=payload
            )
        except Exception:
            pass
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_release_control_execution_state_object_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Release control execution state object v0 (implemented object; non-action).

    Writes:
    - result.metadata["navigation_governance_action_release_control_execution_state_v0"]

    Policy:
    - relevant-only: requires release_control status object + release_control wiring object.
    - Optional: reads release_control result + readiness for consistency observation only.
    """
    try:
        md0 = dict(res.metadata or {})
        applicable, payload = evaluate_navigation_governance_action_release_control_execution_state_v0(
            navigation_governance_action_release_control_status_v0=md0.get(
                "navigation_governance_action_release_control_status_v0"
            ),
            navigation_governance_action_release_control_wiring_v0=md0.get(
                "navigation_governance_action_release_control_wiring_v0"
            ),
            navigation_governance_action_release_control_result_v0=md0.get(
                "navigation_governance_action_release_control_result_v0"
            ),
            navigation_governance_action_release_control_readiness_gate_v0=md0.get(
                "navigation_governance_action_release_control_readiness_gate_v0"
            ),
        )
        if not applicable or not isinstance(payload, dict):
            return res
        md0["navigation_governance_action_release_control_execution_state_v0"] = payload
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_release_control_result_object_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Release control result object v0 (implemented object; non-action).

    Writes:
    - result.metadata["navigation_governance_action_release_control_result_v0"]

    Policy:
    - relevant-only: requires release_control status object + release_control wiring object.
    - Optional: reads release_control input + readiness for consistency observation only.
    """
    try:
        md0 = dict(res.metadata or {})
        applicable, payload = evaluate_navigation_governance_action_release_control_result_v0(
            navigation_governance_action_release_control_status_v0=md0.get(
                "navigation_governance_action_release_control_status_v0"
            ),
            navigation_governance_action_release_control_wiring_v0=md0.get(
                "navigation_governance_action_release_control_wiring_v0"
            ),
            navigation_governance_action_release_control_input_v0=md0.get(
                "navigation_governance_action_release_control_input_v0"
            ),
            navigation_governance_action_release_control_readiness_gate_v0=md0.get(
                "navigation_governance_action_release_control_readiness_gate_v0"
            ),
        )
        if not applicable or not isinstance(payload, dict):
            return res
        md0["navigation_governance_action_release_control_result_v0"] = payload
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_release_control_executor_input_bridge_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Release control executor input bridge v0 (minimal implementation; non-action).

    Writes:
    - result.metadata["navigation_governance_action_release_control_executor_input_bridge_v0"]

    Policy:
    - relevant-only: when absolutely no core sources exist, do not write.
    - otherwise, write attempted object with bridge_status in {ready, not_ready, blocked}.
    """
    try:
        md0 = dict(res.metadata or {})
        applicable, payload = evaluate_navigation_governance_action_release_control_executor_input_bridge_v0(
            navigation_governance_action_release_control_input_v0=md0.get(
                "navigation_governance_action_release_control_input_v0"
            ),
            navigation_governance_action_release_control_execution_state_v0=md0.get(
                "navigation_governance_action_release_control_execution_state_v0"
            ),
            navigation_governance_action_release_control_result_v0=md0.get(
                "navigation_governance_action_release_control_result_v0"
            ),
            navigation_governance_action_release_control_readiness_gate_v0=md0.get(
                "navigation_governance_action_release_control_readiness_gate_v0"
            ),
            navigation_governance_action_release_control_wiring_v0=md0.get(
                "navigation_governance_action_release_control_wiring_v0"
            ),
            release_control_minimal_executor_identity=md0.get(
                "navigation_governance_action_release_control_minimal_executor_identity_v0"
            ),
            navigation_governance_action_approval_status_v0=md0.get(
                "navigation_governance_action_approval_status_v0"
            ),
            navigation_governance_action_executor_wiring_v0=md0.get(
                "navigation_governance_action_executor_wiring_v0"
            ),
        )
        if not applicable or not isinstance(payload, dict):
            return res
        md0["navigation_governance_action_release_control_executor_input_bridge_v0"] = payload
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_release_control_live_release_gate_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Release control live release gate v0 (minimal implementation; non-action).

    Writes:
    - result.metadata["navigation_governance_action_release_control_live_release_gate_v0"]
    """
    try:
        md0 = dict(res.metadata or {})
        applicable, payload = evaluate_navigation_governance_action_release_control_live_release_gate_v0(
            navigation_governance_action_release_control_executor_input_bridge_v0=md0.get(
                "navigation_governance_action_release_control_executor_input_bridge_v0"
            ),
            navigation_governance_action_release_control_guarded_live_stub_v0=md0.get(
                "navigation_governance_action_release_control_guarded_live_stub_v0"
            ),
            navigation_governance_action_release_control_execution_state_v0=md0.get(
                "navigation_governance_action_release_control_execution_state_v0"
            ),
            navigation_governance_action_release_control_result_v0=md0.get(
                "navigation_governance_action_release_control_result_v0"
            ),
            navigation_governance_action_release_control_guarded_live_identity_v0=md0.get(
                "navigation_governance_action_release_control_guarded_live_identity_v0"
            ),
            navigation_governance_action_release_control_minimal_executor_identity_v0=md0.get(
                "navigation_governance_action_release_control_minimal_executor_identity_v0"
            ),
            navigation_governance_action_release_control_readiness_gate_v0=md0.get(
                "navigation_governance_action_release_control_readiness_gate_v0"
            ),
            navigation_governance_action_release_control_wiring_v0=md0.get(
                "navigation_governance_action_release_control_wiring_v0"
            ),
        )
        if not applicable or not isinstance(payload, dict):
            return res
        md0["navigation_governance_action_release_control_live_release_gate_v0"] = payload
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_release_control_side_effect_release_gate_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Release control side-effect release gate v0 (minimal implementation; non-action).

    Writes:
    - result.metadata["navigation_governance_action_release_control_side_effect_release_gate_v0"]
    """
    try:
        md0 = dict(res.metadata or {})
        applicable, payload = evaluate_navigation_governance_action_release_control_side_effect_release_gate_v0(
            navigation_governance_action_release_control_live_release_gate_v0=md0.get(
                "navigation_governance_action_release_control_live_release_gate_v0"
            ),
            navigation_governance_action_release_control_guarded_live_stub_v0=md0.get(
                "navigation_governance_action_release_control_guarded_live_stub_v0"
            ),
            navigation_governance_action_release_control_execution_state_v0=md0.get(
                "navigation_governance_action_release_control_execution_state_v0"
            ),
            navigation_governance_action_release_control_result_v0=md0.get(
                "navigation_governance_action_release_control_result_v0"
            ),
            navigation_governance_action_release_control_guarded_live_identity_v0=md0.get(
                "navigation_governance_action_release_control_guarded_live_identity_v0"
            ),
            navigation_governance_action_release_control_minimal_executor_identity_v0=md0.get(
                "navigation_governance_action_release_control_minimal_executor_identity_v0"
            ),
            navigation_governance_action_release_control_executor_input_bridge_v0=md0.get(
                "navigation_governance_action_release_control_executor_input_bridge_v0"
            ),
            navigation_governance_action_release_control_readiness_gate_v0=md0.get(
                "navigation_governance_action_release_control_readiness_gate_v0"
            ),
            navigation_governance_action_release_control_wiring_v0=md0.get(
                "navigation_governance_action_release_control_wiring_v0"
            ),
        )
        if not applicable or not isinstance(payload, dict):
            return res
        md0["navigation_governance_action_release_control_side_effect_release_gate_v0"] = payload
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_release_control_first_live_enablement_dry_run_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Release control first live enablement dry-run result v0 (stub evaluation; non-action).

    Writes:
    - result.metadata["navigation_governance_action_release_control_first_live_enablement_dry_run_v0"]

    Policy:
    - relevant-only: if none of the core upstream objects exist, do not write.
    """
    try:
        md0 = dict(res.metadata or {})
        lg = md0.get("navigation_governance_action_release_control_live_release_gate_v0")
        sg = md0.get("navigation_governance_action_release_control_side_effect_release_gate_v0")
        gs = md0.get("navigation_governance_action_release_control_guarded_live_stub_v0")
        xs = md0.get("navigation_governance_action_release_control_execution_state_v0")
        rs = md0.get("navigation_governance_action_release_control_result_v0")

        any_core_present = any(isinstance(x, dict) for x in [lg, sg, gs, xs, rs])
        if not any_core_present:
            return res

        payload = evaluate_enablement_dry_run_preconditions(
            live_release_gate_v0=lg,
            side_effect_release_gate_v0=sg,
            guarded_live_stub_v0=gs,
            execution_state_v0=xs,
            result_v0=rs,
            approval_signal=md0.get(
                "navigation_governance_action_release_control_first_live_enablement_approval_signal_v0"
            ),
        )
        if not isinstance(payload, dict):
            return res
        md0["navigation_governance_action_release_control_first_live_enablement_dry_run_v0"] = payload
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_release_control_first_live_enablement_approval_gate_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Release control first live enablement approval gate v0 (minimal implementation; non-action).

    Writes:
    - result.metadata["navigation_governance_action_release_control_first_live_enablement_approval_gate_v0"]
    """
    try:
        md0 = dict(res.metadata or {})
        applicable, payload = (
            evaluate_navigation_governance_action_release_control_first_live_enablement_approval_gate_v0(
                navigation_governance_action_release_control_first_live_enablement_dry_run_v0=md0.get(
                    "navigation_governance_action_release_control_first_live_enablement_dry_run_v0"
                ),
                navigation_governance_action_release_control_live_release_gate_v0=md0.get(
                    "navigation_governance_action_release_control_live_release_gate_v0"
                ),
                navigation_governance_action_release_control_side_effect_release_gate_v0=md0.get(
                    "navigation_governance_action_release_control_side_effect_release_gate_v0"
                ),
                navigation_governance_action_release_control_guarded_live_stub_v0=md0.get(
                    "navigation_governance_action_release_control_guarded_live_stub_v0"
                ),
                navigation_governance_action_release_control_execution_state_v0=md0.get(
                    "navigation_governance_action_release_control_execution_state_v0"
                ),
                navigation_governance_action_release_control_result_v0=md0.get(
                    "navigation_governance_action_release_control_result_v0"
                ),
                navigation_governance_action_release_control_guarded_live_identity_v0=md0.get(
                    "navigation_governance_action_release_control_guarded_live_identity_v0"
                ),
                navigation_governance_action_release_control_minimal_executor_identity_v0=md0.get(
                    "navigation_governance_action_release_control_minimal_executor_identity_v0"
                ),
                release_control_first_live_enablement_approval_signal_v0=md0.get(
                    "navigation_governance_action_release_control_first_live_enablement_approval_signal_v0"
                ),
            )
        )
        if not applicable or not isinstance(payload, dict):
            return res
        md0["navigation_governance_action_release_control_first_live_enablement_approval_gate_v0"] = payload
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_release_control_first_live_launch_dry_run_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Release control first live launch dry-run v0 (minimal implementation; non-action).

    Writes:
    - result.metadata["navigation_governance_action_release_control_first_live_launch_dry_run_v0"]
    """
    try:
        md0 = dict(res.metadata or {})
        applicable, payload = (
            evaluate_navigation_governance_action_release_control_first_live_launch_dry_run_v0(
                navigation_governance_action_release_control_first_live_enablement_approval_gate_v0=md0.get(
                    "navigation_governance_action_release_control_first_live_enablement_approval_gate_v0"
                ),
                navigation_governance_action_release_control_live_release_gate_v0=md0.get(
                    "navigation_governance_action_release_control_live_release_gate_v0"
                ),
                navigation_governance_action_release_control_side_effect_release_gate_v0=md0.get(
                    "navigation_governance_action_release_control_side_effect_release_gate_v0"
                ),
                navigation_governance_action_release_control_guarded_live_stub_v0=md0.get(
                    "navigation_governance_action_release_control_guarded_live_stub_v0"
                ),
                navigation_governance_action_release_control_execution_state_v0=md0.get(
                    "navigation_governance_action_release_control_execution_state_v0"
                ),
                navigation_governance_action_release_control_result_v0=md0.get(
                    "navigation_governance_action_release_control_result_v0"
                ),
                navigation_governance_action_release_control_guarded_live_identity_v0=md0.get(
                    "navigation_governance_action_release_control_guarded_live_identity_v0"
                ),
                navigation_governance_action_release_control_minimal_executor_identity_v0=md0.get(
                    "navigation_governance_action_release_control_minimal_executor_identity_v0"
                ),
            )
        )
        if not applicable or not isinstance(payload, dict):
            return res
        md0["navigation_governance_action_release_control_first_live_launch_dry_run_v0"] = payload
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_wiring_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Release control first live guarded implementation wiring v0 (non-effect wiring; non-action).

    Writes:
    - result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_wiring_v0"]

    Policy:
    - relevant-only: if none of the core upstream objects exist, do not write.
    - otherwise, write attempted object with wiring_status in {wired_ready, wired_not_ready, wired_blocked}.
    - Optional: call guarded implementation skeleton wiring recognition interface (still non-action).
    """
    try:
        md0 = dict(res.metadata or {})

        # Required standardized inputs (read-only)
        ag = md0.get("navigation_governance_action_release_control_first_live_enablement_approval_gate_v0")
        ld = md0.get("navigation_governance_action_release_control_first_live_launch_dry_run_v0")
        lg = md0.get("navigation_governance_action_release_control_live_release_gate_v0")
        sg = md0.get("navigation_governance_action_release_control_side_effect_release_gate_v0")
        xs = md0.get("navigation_governance_action_release_control_execution_state_v0")
        rs = md0.get("navigation_governance_action_release_control_result_v0")

        # Skeleton identity (fixed; read-only)
        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_skeleton_v0 import (  # noqa: E402
                get_release_control_first_live_guarded_implementation_skeleton_identity,
            )

            sk = get_release_control_first_live_guarded_implementation_skeleton_identity()
        except Exception:
            sk = None

        from capabilities.mid_platform.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_wiring_v0 import (  # noqa: E402
            evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_wiring_v0,
        )

        applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_wiring_v0(
            navigation_governance_action_release_control_first_live_enablement_approval_gate_v0=ag,
            navigation_governance_action_release_control_first_live_launch_dry_run_v0=ld,
            navigation_governance_action_release_control_live_release_gate_v0=lg,
            navigation_governance_action_release_control_side_effect_release_gate_v0=sg,
            release_control_first_live_guarded_implementation_skeleton_identity_v0=sk,
            navigation_governance_action_release_control_execution_state_v0=xs,
            navigation_governance_action_release_control_result_v0=rs,
        )
        if not applicable or not isinstance(payload, dict):
            return res

        md0["navigation_governance_action_release_control_first_live_guarded_implementation_wiring_v0"] = payload

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_skeleton_v0 import (  # noqa: E402
                accept_first_live_guarded_implementation_wiring,
            )

            _ = accept_first_live_guarded_implementation_wiring(
                navigation_governance_action_release_control_first_live_guarded_implementation_wiring_v0=payload
            )
        except Exception:
            pass

        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_non_effect_execution_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Release control first live guarded implementation minimal non-effect execution v0 (non-action).

    Writes:
    - result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_non_effect_execution_v0"]

    Policy:
    - relevant-only: if none of the core upstream objects exist, do not write.
    - otherwise, write attempted object with execution_status in {executed, not_ready, blocked}.
    - Optional: call guarded implementation skeleton execution recognition interface (still non-action).
    """
    try:
        md0 = dict(res.metadata or {})

        w = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_wiring_v0"
        )
        xs = md0.get("navigation_governance_action_release_control_execution_state_v0")
        rs = md0.get("navigation_governance_action_release_control_result_v0")

        any_core_present = any(isinstance(x, dict) for x in [w, xs, rs])
        if not any_core_present:
            return res

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_skeleton_v0 import (  # noqa: E402
                get_release_control_first_live_guarded_implementation_skeleton_identity,
            )

            sk = get_release_control_first_live_guarded_implementation_skeleton_identity()
        except Exception:
            sk = None

        from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_non_effect_execution_v0 import (  # noqa: E402
            evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_non_effect_execution_v0,
        )

        applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_non_effect_execution_v0(
            navigation_governance_action_release_control_first_live_guarded_implementation_wiring_v0=w,
            release_control_first_live_guarded_implementation_skeleton_identity_v0=sk,
            navigation_governance_action_release_control_execution_state_v0=xs,
            navigation_governance_action_release_control_result_v0=rs,
        )
        if not applicable or not isinstance(payload, dict):
            return res

        md0[
            "navigation_governance_action_release_control_first_live_guarded_implementation_non_effect_execution_v0"
        ] = payload

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_skeleton_v0 import (  # noqa: E402
                accept_first_live_guarded_implementation_non_effect_execution,
            )

            _ = accept_first_live_guarded_implementation_non_effect_execution(
                navigation_governance_action_release_control_first_live_guarded_implementation_non_effect_execution_v0=payload
            )
        except Exception:
            pass

        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Release control first live guarded implementation dry-effect simulation v0 (non-action).

    Writes:
    - result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0"]

    Policy:
    - relevant-only: if none of the core upstream objects exist, do not write.
    - otherwise, write attempted object with simulation_status in {simulated, not_ready, blocked}.
    - Optional: call guarded implementation skeleton simulation recognition interface (still non-action).
    """
    try:
        md0 = dict(res.metadata or {})

        ex = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_non_effect_execution_v0"
        )
        xs = md0.get("navigation_governance_action_release_control_execution_state_v0")
        rs = md0.get("navigation_governance_action_release_control_result_v0")

        any_core_present = any(isinstance(x, dict) for x in [ex, xs, rs])
        if not any_core_present:
            return res

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_skeleton_v0 import (  # noqa: E402
                get_release_control_first_live_guarded_implementation_skeleton_identity,
            )

            sk = get_release_control_first_live_guarded_implementation_skeleton_identity()
        except Exception:
            sk = None

        from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0 import (  # noqa: E402
            evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0,
        )

        applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0(
            navigation_governance_action_release_control_first_live_guarded_implementation_non_effect_execution_v0=ex,
            release_control_first_live_guarded_implementation_skeleton_identity_v0=sk,
            navigation_governance_action_release_control_execution_state_v0=xs,
            navigation_governance_action_release_control_result_v0=rs,
        )
        if not applicable or not isinstance(payload, dict):
            return res

        md0[
            "navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0"
        ] = payload

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_skeleton_v0 import (  # noqa: E402
                accept_first_live_guarded_implementation_dry_effect_simulation,
            )

            _ = accept_first_live_guarded_implementation_dry_effect_simulation(
                navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0=payload
            )
        except Exception:
            pass

        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Release control first live guarded implementation minimal real-effect wiring v0 (non-effect wiring; non-action).

    Writes:
    - result.metadata["navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0"]

    Policy:
    - relevant-only: if none of the core upstream metadata dicts exist, do not write.
    - otherwise, write attempted object with wiring_status in
      {first_live_minimal_real_effect_wired_ready, first_live_minimal_real_effect_wired_not_ready,
       first_live_minimal_real_effect_wired_blocked}.
    - Optional: call minimal real-effect stub wiring recognition interface (still non-action).
    """
    try:
        md0 = dict(res.metadata or {})

        ag = md0.get("navigation_governance_action_release_control_first_live_enablement_approval_gate_v0")
        ld = md0.get("navigation_governance_action_release_control_first_live_launch_dry_run_v0")
        lg = md0.get("navigation_governance_action_release_control_live_release_gate_v0")
        sg = md0.get("navigation_governance_action_release_control_side_effect_release_gate_v0")
        ds = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0"
        )
        xs = md0.get("navigation_governance_action_release_control_execution_state_v0")
        rs = md0.get("navigation_governance_action_release_control_result_v0")

        any_core_present = any(isinstance(x, dict) for x in [ag, ld, lg, sg, ds, xs, rs])
        if not any_core_present:
            return res

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_stub_v0 import (  # noqa: E402
                get_release_control_first_live_guarded_implementation_minimal_real_effect_stub_identity,
            )

            stub = get_release_control_first_live_guarded_implementation_minimal_real_effect_stub_identity()
        except Exception:
            stub = None

        from capabilities.mid_platform.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0 import (  # noqa: E402
            evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0,
        )

        applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0(
            navigation_governance_action_release_control_first_live_enablement_approval_gate_v0=ag,
            navigation_governance_action_release_control_first_live_launch_dry_run_v0=ld,
            navigation_governance_action_release_control_live_release_gate_v0=lg,
            navigation_governance_action_release_control_side_effect_release_gate_v0=sg,
            navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0=ds,
            release_control_first_live_guarded_implementation_minimal_real_effect_stub_identity_v0=stub,
            navigation_governance_action_release_control_execution_state_v0=xs,
            navigation_governance_action_release_control_result_v0=rs,
        )
        if not applicable or not isinstance(payload, dict):
            return res

        md0[
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0"
        ] = payload

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_stub_v0 import (  # noqa: E402
                accept_first_live_minimal_real_effect_wiring,
            )

            _ = accept_first_live_minimal_real_effect_wiring(
                navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0=payload
            )
        except Exception:
            pass

        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_dry_run_execution_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Release control first live guarded implementation minimal real-effect dry-run execution v0 (non-action).

    Writes:
    - result.metadata[
        "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_dry_run_execution_v0"
      ]

    Policy:
    - relevant-only: if none of minimal_real_effect_wiring_v0 / execution_state_v0 / result_v0 exist, do not write.
    - otherwise write attempted object with execution_status in dry_run_executed | not_ready | blocked.
    - Runs stub placeholder chain only when wiring_status == wired_ready (evaluator-enforced).
    """
    try:
        md0 = dict(res.metadata or {})

        mw = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0"
        )
        xs = md0.get("navigation_governance_action_release_control_execution_state_v0")
        rs = md0.get("navigation_governance_action_release_control_result_v0")

        any_core_present = any(isinstance(x, dict) for x in [mw, xs, rs])
        if not any_core_present:
            return res

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_stub_v0 import (  # noqa: E402
                get_release_control_first_live_guarded_implementation_minimal_real_effect_stub_identity,
            )

            stub = get_release_control_first_live_guarded_implementation_minimal_real_effect_stub_identity()
        except Exception:
            stub = None

        from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_dry_run_execution_v0 import (  # noqa: E402
            evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_dry_run_execution_v0,
        )

        applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_dry_run_execution_v0(
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0=mw,
            release_control_first_live_guarded_implementation_minimal_real_effect_stub_identity_v0=stub,
            navigation_governance_action_release_control_execution_state_v0=xs,
            navigation_governance_action_release_control_result_v0=rs,
        )
        if not applicable or not isinstance(payload, dict):
            return res

        md0[
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_dry_run_execution_v0"
        ] = payload

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_stub_v0 import (  # noqa: E402
                accept_first_live_minimal_real_effect_dry_run_execution,
            )

            _ = accept_first_live_minimal_real_effect_dry_run_execution(
                navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_dry_run_execution_v0=payload
            )
        except Exception:
            pass

        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Release control first live guarded implementation minimal real-effect implementation wiring v0 (non-effect wiring; non-action).

    Writes:
    - result.metadata[
        "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_v0"
      ]

    Policy:
    - relevant-only: if none of the core upstream metadata dicts exist, do not write.
    - otherwise, write attempted object with wiring_status in
      {first_live_minimal_real_effect_implementation_wired_ready,
       first_live_minimal_real_effect_implementation_wired_not_ready,
       first_live_minimal_real_effect_implementation_wired_blocked}.
    - Optional: call implementation skeleton wiring recognition interface (still non-action).
    """
    try:
        md0 = dict(res.metadata or {})

        ag = md0.get("navigation_governance_action_release_control_first_live_enablement_approval_gate_v0")
        ld = md0.get("navigation_governance_action_release_control_first_live_launch_dry_run_v0")
        lg = md0.get("navigation_governance_action_release_control_live_release_gate_v0")
        sg = md0.get("navigation_governance_action_release_control_side_effect_release_gate_v0")
        ds = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0"
        )
        dr = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_dry_run_execution_v0"
        )
        xs = md0.get("navigation_governance_action_release_control_execution_state_v0")
        rs = md0.get("navigation_governance_action_release_control_result_v0")

        any_core_present = any(isinstance(x, dict) for x in [ag, ld, lg, sg, ds, dr, xs, rs])
        if not any_core_present:
            return res

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_v0 import (  # noqa: E402
                get_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity,
            )

            sk = (
                get_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity()
            )
        except Exception:
            sk = None

        from capabilities.mid_platform.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_v0 import (  # noqa: E402
            evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_v0,
        )

        applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_v0(
            navigation_governance_action_release_control_first_live_enablement_approval_gate_v0=ag,
            navigation_governance_action_release_control_first_live_launch_dry_run_v0=ld,
            navigation_governance_action_release_control_live_release_gate_v0=lg,
            navigation_governance_action_release_control_side_effect_release_gate_v0=sg,
            navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0=ds,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_dry_run_execution_v0=dr,
            release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity_v0=sk,
            navigation_governance_action_release_control_execution_state_v0=xs,
            navigation_governance_action_release_control_result_v0=rs,
        )
        if not applicable or not isinstance(payload, dict):
            return res

        md0[
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_v0"
        ] = payload

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_v0 import (  # noqa: E402
                accept_first_live_minimal_real_effect_implementation_wiring,
            )

            _ = accept_first_live_minimal_real_effect_implementation_wiring(
                minimal_real_effect_implementation_wiring_v0=payload
            )
        except Exception:
            pass

        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Release control first live guarded implementation minimal real-effect live implementation wiring v0
    (non-effect wiring; non-action).

    Writes:
    - result.metadata[
        "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0"
      ]

    Policy:
    - relevant-only: if none of the core upstream metadata dicts exist, do not write.
    - otherwise, write attempted object with wiring_status in
      {first_live_minimal_real_effect_live_wired_ready,
       first_live_minimal_real_effect_live_wired_not_ready,
       first_live_minimal_real_effect_live_wired_blocked}.
    - Optional: call live implementation skeleton wiring recognition interface (still non-action).
    """
    try:
        md0 = dict(res.metadata or {})

        adm = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0"
        )
        lgate = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0"
        )
        pc = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0"
        )
        cg = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_v0"
        )
        cdr = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_dry_run_v0"
        )
        ag = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_gate_v0"
        )
        adr = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_dry_run_v0"
        )
        xs = md0.get("navigation_governance_action_release_control_execution_state_v0")
        rs = md0.get("navigation_governance_action_release_control_result_v0")

        any_core_present = any(
            isinstance(x, dict) for x in [adm, lgate, pc, cg, cdr, ag, adr, xs, rs]
        )
        if not any_core_present:
            return res

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_v0 import (  # noqa: E402
                get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_identity,
            )

            sk = (
                get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_identity()
            )
        except Exception:
            sk = None

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_stub_v0 import (  # noqa: E402
                get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_stub_identity,
            )

            stub = (
                get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_stub_identity()
            )
        except Exception:
            stub = None

        from capabilities.mid_platform.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0 import (  # noqa: E402
            evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0,
        )

        applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0(
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0=adm,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0=lgate,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0=pc,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_v0=cg,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_dry_run_v0=cdr,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_gate_v0=ag,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_dry_run_v0=adr,
            release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_identity_v0=sk,
            release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_stub_identity_v0=stub,
            navigation_governance_action_release_control_execution_state_v0=xs,
            navigation_governance_action_release_control_result_v0=rs,
            side_effects_released=md0.get("side_effects_released"),
        )
        if not applicable or not isinstance(payload, dict):
            return res

        md0[
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0"
        ] = payload

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_v0 import (  # noqa: E402
                accept_first_live_minimal_real_effect_live_implementation_wiring,
            )

            _ = accept_first_live_minimal_real_effect_live_implementation_wiring(
                navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0=payload
            )
        except Exception:
            pass

        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Release control first live guarded implementation minimal real-effect live implementation dry-run execution v0 (non-action).

    Writes:
    - result.metadata[
        "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_v0"
      ]

    Policy:
    - relevant-only: if none of live_implementation_wiring_v0 / execution_state_v0 / result_v0 exist, do not write.
    - otherwise write attempted object with execution_status in executed | not_ready | blocked.
    - Runs stub placeholder chain only when wiring_status == wired_ready (evaluator-enforced).
    """
    try:
        md0 = dict(res.metadata or {})

        lw = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0"
        )
        xs = md0.get("navigation_governance_action_release_control_execution_state_v0")
        rs = md0.get("navigation_governance_action_release_control_result_v0")

        any_core_present = any(isinstance(x, dict) for x in [lw, xs, rs])
        if not any_core_present:
            return res

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_v0 import (  # noqa: E402
                get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_identity,
            )

            sk = (
                get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_identity()
            )
        except Exception:
            sk = None

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_stub_v0 import (  # noqa: E402
                get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_stub_identity,
            )

            stub = (
                get_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_stub_identity()
            )
        except Exception:
            stub = None

        from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_v0 import (  # noqa: E402
            evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_v0,
        )

        applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_v0(
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0=lw,
            release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_identity_v0=sk,
            release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_stub_identity_v0=stub,
            navigation_governance_action_release_control_execution_state_v0=xs,
            navigation_governance_action_release_control_result_v0=rs,
        )
        if not applicable or not isinstance(payload, dict):
            return res

        md0[
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_v0"
        ] = payload

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_skeleton_v0 import (  # noqa: E402
                accept_first_live_minimal_real_effect_live_implementation_dry_run_execution,
            )

            _ = accept_first_live_minimal_real_effect_live_implementation_dry_run_execution(
                navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_v0=payload
            )
        except Exception:
            pass

        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Release control first live guarded implementation minimal real-effect live implementation shadow v0
    (observe-only; no real writes).

    Writes:
    - result.metadata[
        "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_v0"
      ]

    Policy:
    - relevant-only: if none of the core objects exist, do not write.
    - otherwise write attempted object with shadow_status in
      {shadow_executed, shadow_not_ready, shadow_blocked}.
    - default-off: without explicit shadow_enable_signal_v0 -> shadow_not_ready.
    """
    try:
        md0 = dict(res.metadata or {})

        go_no_go = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_real_write_go_no_go_gate_v0"
        )
        cpd = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_code_path_dry_run_v0"
        )
        sig = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_enable_signal_v0"
        )
        xs = md0.get("navigation_governance_action_release_control_execution_state_v0")
        rs = md0.get("navigation_governance_action_release_control_result_v0")
        ex = md0.get("exception_or_failure_path_v0")
        ser = md0.get("side_effects_released")

        any_core_present = any(isinstance(x, dict) for x in [go_no_go, cpd, sig, xs, rs, ex])
        if not any_core_present and ser is None:
            return res

        from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_v0 import (  # noqa: E402
            evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_v0,
        )

        applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_v0(
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_real_write_go_no_go_gate_v0=go_no_go,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_code_path_dry_run_v0=cpd,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_enable_signal_v0=sig,
            navigation_governance_action_release_control_execution_state_v0=xs,
            navigation_governance_action_release_control_result_v0=rs,
            exception_or_failure_path_v0=ex,
            side_effects_released=ser,
        )
        if not applicable or not isinstance(payload, dict):
            return res

        md0[
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_v0"
        ] = payload

        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Release control first live guarded implementation minimal real-effect live implementation controlled trial shadow trial v0
    (observe-only; no real enablement).

    Writes:
    - result.metadata[
        "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_v0"
      ]

    Policy:
    - relevant-only: if none of the core objects exist, do not write.
    - otherwise write attempted object with shadow_trial_status in
      {shadow_trial_executed, shadow_trial_not_ready, shadow_trial_blocked}.
    - default-off: without explicit shadow_trial_enable_signal_v0 -> shadow_trial_not_ready.
    """
    try:
        md0 = dict(res.metadata or {})

        ct_go = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_go_no_go_gate_v0"
        )
        ct_dry = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_enablement_dry_run_v0"
        )
        ct_ready = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_first_minimal_real_enablement_v0"
        )
        sig = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_trial_enable_signal_v0"
        )
        xs = md0.get("navigation_governance_action_release_control_execution_state_v0")
        rs = md0.get("navigation_governance_action_release_control_result_v0")
        ex = md0.get("exception_or_failure_path_v0")
        ser = md0.get("side_effects_released")

        any_core_present = any(isinstance(x, dict) for x in [ct_go, ct_dry, ct_ready, sig, xs, rs, ex])
        if not any_core_present and ser is None:
            return res

        from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_v0 import (  # noqa: E402
            evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_v0,
        )

        applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_v0(
            controlled_trial_go_no_go_gate_v0=ct_go,
            controlled_trial_enablement_dry_run_v0=ct_dry,
            controlled_trial_first_minimal_real_enablement_v0=ct_ready,
            shadow_trial_enable_signal_v0=sig,
            execution_state_v0=xs,
            result_v0=rs,
            exception_or_failure_path_v0=ex,
            side_effects_released=ser,
        )
        if not applicable or not isinstance(payload, dict):
            return res

        md0[
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_v0"
        ] = payload

        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Release control first live guarded implementation minimal real-effect implementation dry-run execution v0 (non-action).

    Writes:
    - result.metadata[
        "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0"
      ]

    Policy:
    - relevant-only: if none of implementation_wiring_v0 / execution_state_v0 / result_v0 exist, do not write.
    - otherwise write attempted object with execution_status in executed | not_ready | blocked.
    - Runs skeleton placeholder chain only when implementation wiring_status == wired_ready (evaluator-enforced).
    """
    try:
        md0 = dict(res.metadata or {})

        iw = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_v0"
        )
        xs = md0.get("navigation_governance_action_release_control_execution_state_v0")
        rs = md0.get("navigation_governance_action_release_control_result_v0")

        any_core_present = any(isinstance(x, dict) for x in [iw, xs, rs])
        if not any_core_present:
            return res

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_v0 import (  # noqa: E402
                get_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity,
            )

            sk = (
                get_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity()
            )
        except Exception:
            sk = None

        from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0 import (  # noqa: E402
            evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0,
        )

        applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0(
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_v0=iw,
            release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity_v0=sk,
            navigation_governance_action_release_control_execution_state_v0=xs,
            navigation_governance_action_release_control_result_v0=rs,
        )
        if not applicable or not isinstance(payload, dict):
            return res

        md0[
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0"
        ] = payload

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_v0 import (  # noqa: E402
                accept_first_live_minimal_real_effect_implementation_dry_run_execution,
            )

            _ = accept_first_live_minimal_real_effect_implementation_dry_run_execution(
                minimal_real_effect_implementation_dry_run_execution_v0=payload
            )
        except Exception:
            pass

        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Release control first live guarded implementation minimal real-effect admission gate v0 (non-effect; non-action).

    Writes:
    - result.metadata[
        "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0"
      ]

    Policy:
    - relevant-only: if none of the core upstream metadata dicts exist, do not write.
    - otherwise, write attempted object with admission_status in
      {first_live_minimal_real_effect_admitted, first_live_minimal_real_effect_not_admitted,
       first_live_minimal_real_effect_blocked}.
    - Optional: call implementation skeleton admission gate recognition interface (still non-action).
    """
    try:
        md0 = dict(res.metadata or {})

        ag = md0.get("navigation_governance_action_release_control_first_live_enablement_approval_gate_v0")
        ld = md0.get("navigation_governance_action_release_control_first_live_launch_dry_run_v0")
        lg = md0.get("navigation_governance_action_release_control_live_release_gate_v0")
        sg = md0.get("navigation_governance_action_release_control_side_effect_release_gate_v0")
        ds = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0"
        )
        mw = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0"
        )
        idr = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0"
        )
        xs = md0.get("navigation_governance_action_release_control_execution_state_v0")
        rs = md0.get("navigation_governance_action_release_control_result_v0")
        sig = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_signal_v0"
        )
        ser = md0.get("side_effects_released")

        any_core_present = any(isinstance(x, dict) for x in [ag, ld, lg, sg, ds, mw, idr, xs, rs])
        if not any_core_present and sig is None and ser is None:
            return res

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_v0 import (  # noqa: E402
                get_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity,
            )

            sk = (
                get_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity()
            )
        except Exception:
            sk = None

        from capabilities.mid_platform.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0 import (  # noqa: E402
            evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0,
        )

        applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0(
            navigation_governance_action_release_control_first_live_enablement_approval_gate_v0=ag,
            navigation_governance_action_release_control_first_live_launch_dry_run_v0=ld,
            navigation_governance_action_release_control_live_release_gate_v0=lg,
            navigation_governance_action_release_control_side_effect_release_gate_v0=sg,
            navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0=ds,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0=mw,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0=idr,
            release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity_v0=sk,
            navigation_governance_action_release_control_execution_state_v0=xs,
            navigation_governance_action_release_control_result_v0=rs,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_signal_v0=sig,
            side_effects_released=ser,
        )
        if not applicable or not isinstance(payload, dict):
            return res

        md0[
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0"
        ] = payload

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_v0 import (  # noqa: E402
                accept_first_live_minimal_real_effect_admission_gate,
            )

            _ = accept_first_live_minimal_real_effect_admission_gate(
                minimal_real_effect_admission_gate_v0=payload
            )
        except Exception:
            pass

        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_dry_run_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Release control first live guarded implementation minimal real-effect guarded launch dry-run v0 (non-effect; non-action).

    Writes:
    - result.metadata[
        "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_dry_run_v0"
      ]

    Policy:
    - relevant-only: if none of the core upstream metadata dicts exist, do not write.
    - otherwise, write attempted object with launch_status in
      {first_live_minimal_real_effect_launch_ready,
       first_live_minimal_real_effect_launch_not_ready,
       first_live_minimal_real_effect_launch_blocked}.
    - Optional: call implementation skeleton recognition interface (still non-action).
    """
    try:
        md0 = dict(res.metadata or {})

        adm = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0"
        )
        ag = md0.get("navigation_governance_action_release_control_first_live_enablement_approval_gate_v0")
        ld = md0.get("navigation_governance_action_release_control_first_live_launch_dry_run_v0")
        lg = md0.get("navigation_governance_action_release_control_live_release_gate_v0")
        sg = md0.get("navigation_governance_action_release_control_side_effect_release_gate_v0")
        ds = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0"
        )
        idr = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0"
        )
        xs = md0.get("navigation_governance_action_release_control_execution_state_v0")
        rs = md0.get("navigation_governance_action_release_control_result_v0")
        ser = md0.get("side_effects_released")

        any_core_present = any(isinstance(x, dict) for x in [adm, ag, ld, lg, sg, ds, idr, xs, rs])
        if not any_core_present and ser is None:
            return res

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_v0 import (  # noqa: E402
                get_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity,
            )

            sk = (
                get_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity()
            )
        except Exception:
            sk = None

        from capabilities.mid_platform.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_dry_run_v0 import (  # noqa: E402
            evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_dry_run_v0,
        )

        applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_dry_run_v0(
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0=adm,
            navigation_governance_action_release_control_first_live_enablement_approval_gate_v0=ag,
            navigation_governance_action_release_control_first_live_launch_dry_run_v0=ld,
            navigation_governance_action_release_control_live_release_gate_v0=lg,
            navigation_governance_action_release_control_side_effect_release_gate_v0=sg,
            navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0=ds,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0=idr,
            release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity_v0=sk,
            navigation_governance_action_release_control_execution_state_v0=xs,
            navigation_governance_action_release_control_result_v0=rs,
            side_effects_released=ser,
        )
        if not applicable or not isinstance(payload, dict):
            return res

        md0[
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_dry_run_v0"
        ] = payload

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_v0 import (  # noqa: E402
                accept_first_live_minimal_real_effect_guarded_launch_dry_run,
            )

            _ = accept_first_live_minimal_real_effect_guarded_launch_dry_run(
                minimal_real_effect_guarded_launch_dry_run_v0=payload
            )
        except Exception:
            pass

        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Release control first live guarded implementation minimal real-effect guarded launch gate v0 (non-effect; non-action).

    Writes:
    - result.metadata[
        "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0"
      ]

    Policy:
    - relevant-only: if none of the core upstream metadata dicts exist, do not write.
    - otherwise, write attempted object with launch_admission_status in
      {first_live_minimal_real_effect_launch_admitted,
       first_live_minimal_real_effect_launch_not_admitted,
       first_live_minimal_real_effect_launch_blocked}.
    - Optional: call implementation skeleton recognition interface (still non-action).
    """
    try:
        md0 = dict(res.metadata or {})

        adm = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0"
        )
        ldr = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_dry_run_v0"
        )
        ag = md0.get("navigation_governance_action_release_control_first_live_enablement_approval_gate_v0")
        ld = md0.get("navigation_governance_action_release_control_first_live_launch_dry_run_v0")
        lg = md0.get("navigation_governance_action_release_control_live_release_gate_v0")
        sg = md0.get("navigation_governance_action_release_control_side_effect_release_gate_v0")
        ds = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0"
        )
        idr = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0"
        )
        xs = md0.get("navigation_governance_action_release_control_execution_state_v0")
        rs = md0.get("navigation_governance_action_release_control_result_v0")
        sig = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_signal_v0"
        )
        ser = md0.get("side_effects_released")

        any_core_present = any(
            isinstance(x, dict) for x in [adm, ldr, ag, ld, lg, sg, ds, idr, xs, rs]
        )
        if not any_core_present and sig is None and ser is None:
            return res

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_v0 import (  # noqa: E402
                get_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity,
            )

            sk = (
                get_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity()
            )
        except Exception:
            sk = None

        from capabilities.mid_platform.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0 import (  # noqa: E402
            evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0,
        )

        applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0(
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0=adm,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_dry_run_v0=ldr,
            navigation_governance_action_release_control_first_live_enablement_approval_gate_v0=ag,
            navigation_governance_action_release_control_first_live_launch_dry_run_v0=ld,
            navigation_governance_action_release_control_live_release_gate_v0=lg,
            navigation_governance_action_release_control_side_effect_release_gate_v0=sg,
            navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0=ds,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0=idr,
            release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity_v0=sk,
            navigation_governance_action_release_control_execution_state_v0=xs,
            navigation_governance_action_release_control_result_v0=rs,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_signal_v0=sig,
            side_effects_released=ser,
        )
        if not applicable or not isinstance(payload, dict):
            return res

        md0[
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0"
        ] = payload

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_v0 import (  # noqa: E402
                accept_first_live_minimal_real_effect_guarded_launch_gate,
            )

            _ = accept_first_live_minimal_real_effect_guarded_launch_gate(
                minimal_real_effect_guarded_launch_gate_v0=payload
            )
        except Exception:
            pass

        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Release control first live guarded implementation minimal real-effect pre-commit dry-run v0 (non-effect; non-action).

    Writes:
    - result.metadata[
        "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0"
      ]

    Policy:
    - relevant-only: if none of the core upstream metadata dicts exist, do not write.
    - otherwise, write attempted object with pre_commit_status in
      {first_live_minimal_real_effect_pre_commit_ready,
       first_live_minimal_real_effect_pre_commit_not_ready,
       first_live_minimal_real_effect_pre_commit_blocked}.
    - Optional: call implementation skeleton recognition interface (still non-action).
    """
    try:
        md0 = dict(res.metadata or {})

        adm = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0"
        )
        lgate = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0"
        )
        ag = md0.get("navigation_governance_action_release_control_first_live_enablement_approval_gate_v0")
        ld = md0.get("navigation_governance_action_release_control_first_live_launch_dry_run_v0")
        live = md0.get("navigation_governance_action_release_control_live_release_gate_v0")
        seg = md0.get("navigation_governance_action_release_control_side_effect_release_gate_v0")
        ds = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0"
        )
        idr = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0"
        )
        xs = md0.get("navigation_governance_action_release_control_execution_state_v0")
        rs = md0.get("navigation_governance_action_release_control_result_v0")
        ser = md0.get("side_effects_released")

        any_core_present = any(
            isinstance(x, dict) for x in [adm, lgate, ag, ld, live, seg, ds, idr, xs, rs]
        )
        if not any_core_present and ser is None:
            return res

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_v0 import (  # noqa: E402
                get_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity,
            )

            sk = (
                get_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity()
            )
        except Exception:
            sk = None

        from capabilities.mid_platform.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0 import (  # noqa: E402
            evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0,
        )

        applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0(
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0=adm,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0=lgate,
            navigation_governance_action_release_control_first_live_enablement_approval_gate_v0=ag,
            navigation_governance_action_release_control_first_live_launch_dry_run_v0=ld,
            navigation_governance_action_release_control_live_release_gate_v0=live,
            navigation_governance_action_release_control_side_effect_release_gate_v0=seg,
            navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0=ds,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0=idr,
            release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity_v0=sk,
            navigation_governance_action_release_control_execution_state_v0=xs,
            navigation_governance_action_release_control_result_v0=rs,
            side_effects_released=ser,
        )
        if not applicable or not isinstance(payload, dict):
            return res

        md0[
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0"
        ] = payload

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_v0 import (  # noqa: E402
                accept_first_live_minimal_real_effect_pre_commit_dry_run,
            )

            _ = accept_first_live_minimal_real_effect_pre_commit_dry_run(
                minimal_real_effect_pre_commit_dry_run_v0=payload
            )
        except Exception:
            pass

        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Release control first live guarded implementation minimal real-effect commit gate v0 (non-effect; non-action).

    Writes:
    - result.metadata[
        "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_v0"
      ]

    Policy:
    - relevant-only: if none of the core upstream metadata dicts exist, do not write.
    - otherwise, write attempted object with commit_admission_status in
      {first_live_minimal_real_effect_commit_admitted,
       first_live_minimal_real_effect_commit_not_admitted,
       first_live_minimal_real_effect_commit_blocked}.
    - Optional: call implementation skeleton recognition interface (still non-action).
    """
    try:
        md0 = dict(res.metadata or {})

        adm = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0"
        )
        lgate = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0"
        )
        pc = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0"
        )
        ag = md0.get("navigation_governance_action_release_control_first_live_enablement_approval_gate_v0")
        ld = md0.get("navigation_governance_action_release_control_first_live_launch_dry_run_v0")
        live = md0.get("navigation_governance_action_release_control_live_release_gate_v0")
        seg = md0.get("navigation_governance_action_release_control_side_effect_release_gate_v0")
        ds = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0"
        )
        idr = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0"
        )
        xs = md0.get("navigation_governance_action_release_control_execution_state_v0")
        rs = md0.get("navigation_governance_action_release_control_result_v0")
        sig = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_signal_v0"
        )
        ser = md0.get("side_effects_released")

        any_core_present = any(
            isinstance(x, dict) for x in [adm, lgate, pc, ag, ld, live, seg, ds, idr, xs, rs]
        )
        if not any_core_present and sig is None and ser is None:
            return res

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_v0 import (  # noqa: E402
                get_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity,
            )

            sk = (
                get_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity()
            )
        except Exception:
            sk = None

        from capabilities.mid_platform.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_v0 import (  # noqa: E402
            evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_v0,
        )

        applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_v0(
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0=adm,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0=lgate,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0=pc,
            navigation_governance_action_release_control_first_live_enablement_approval_gate_v0=ag,
            navigation_governance_action_release_control_first_live_launch_dry_run_v0=ld,
            navigation_governance_action_release_control_live_release_gate_v0=live,
            navigation_governance_action_release_control_side_effect_release_gate_v0=seg,
            navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0=ds,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0=idr,
            release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity_v0=sk,
            navigation_governance_action_release_control_execution_state_v0=xs,
            navigation_governance_action_release_control_result_v0=rs,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_signal_v0=sig,
            side_effects_released=ser,
        )
        if not applicable or not isinstance(payload, dict):
            return res

        md0[
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_v0"
        ] = payload

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_v0 import (  # noqa: E402
                accept_first_live_minimal_real_effect_commit_gate,
            )

            _ = accept_first_live_minimal_real_effect_commit_gate(minimal_real_effect_commit_gate_v0=payload)
        except Exception:
            pass

        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_dry_run_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Release control first live guarded implementation minimal real-effect commit dry-run v0 (non-effect; non-action).

    Writes:
    - result.metadata[
        "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_dry_run_v0"
      ]

    Policy:
    - relevant-only: if none of the core upstream metadata dicts exist, do not write.
    - otherwise, write attempted object with commit_dry_run_status in
      {first_live_minimal_real_effect_commit_ready,
       first_live_minimal_real_effect_commit_not_ready,
       first_live_minimal_real_effect_commit_blocked}.
    - Optional: call implementation skeleton recognition interface (still non-action).
    """
    try:
        md0 = dict(res.metadata or {})

        cg = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_v0"
        )
        adm = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0"
        )
        lgate = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0"
        )
        pc = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0"
        )
        ag = md0.get("navigation_governance_action_release_control_first_live_enablement_approval_gate_v0")
        ld = md0.get("navigation_governance_action_release_control_first_live_launch_dry_run_v0")
        live = md0.get("navigation_governance_action_release_control_live_release_gate_v0")
        seg = md0.get("navigation_governance_action_release_control_side_effect_release_gate_v0")
        ds = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0"
        )
        idr = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0"
        )
        xs = md0.get("navigation_governance_action_release_control_execution_state_v0")
        rs = md0.get("navigation_governance_action_release_control_result_v0")
        ser = md0.get("side_effects_released")

        any_core_present = any(
            isinstance(x, dict) for x in [cg, adm, lgate, pc, ag, ld, live, seg, ds, idr, xs, rs]
        )
        if not any_core_present and ser is None:
            return res

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_v0 import (  # noqa: E402
                get_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity,
            )

            sk = (
                get_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity()
            )
        except Exception:
            sk = None

        from capabilities.mid_platform.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_dry_run_v0 import (  # noqa: E402
            evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_dry_run_v0,
        )

        applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_dry_run_v0(
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_v0=cg,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0=adm,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0=lgate,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0=pc,
            navigation_governance_action_release_control_first_live_enablement_approval_gate_v0=ag,
            navigation_governance_action_release_control_first_live_launch_dry_run_v0=ld,
            navigation_governance_action_release_control_live_release_gate_v0=live,
            navigation_governance_action_release_control_side_effect_release_gate_v0=seg,
            navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0=ds,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0=idr,
            release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity_v0=sk,
            navigation_governance_action_release_control_execution_state_v0=xs,
            navigation_governance_action_release_control_result_v0=rs,
            side_effects_released=ser,
        )
        if not applicable or not isinstance(payload, dict):
            return res

        md0[
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_dry_run_v0"
        ] = payload

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_v0 import (  # noqa: E402
                accept_first_live_minimal_real_effect_commit_dry_run,
            )

            _ = accept_first_live_minimal_real_effect_commit_dry_run(
                minimal_real_effect_commit_dry_run_v0=payload
            )
        except Exception:
            pass

        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_gate_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Release control first live guarded implementation minimal real-effect activation gate v0 (non-effect; non-action).

    Writes:
    - result.metadata[
        "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_gate_v0"
      ]

    Policy:
    - relevant-only: if none of the core upstream metadata dicts exist, do not write.
    - otherwise, write attempted object with activation_admission_status in
      {first_live_minimal_real_effect_activation_admitted,
       first_live_minimal_real_effect_activation_not_admitted,
       first_live_minimal_real_effect_activation_blocked}.
    - Optional: call implementation skeleton recognition interface (still non-action).
    """
    try:
        md0 = dict(res.metadata or {})

        adm = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0"
        )
        lgate = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0"
        )
        pc = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0"
        )
        cg = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_v0"
        )
        cdr = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_dry_run_v0"
        )
        ag = md0.get("navigation_governance_action_release_control_first_live_enablement_approval_gate_v0")
        ld = md0.get("navigation_governance_action_release_control_first_live_launch_dry_run_v0")
        live = md0.get("navigation_governance_action_release_control_live_release_gate_v0")
        seg = md0.get("navigation_governance_action_release_control_side_effect_release_gate_v0")
        ds = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0"
        )
        idr = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0"
        )
        xs = md0.get("navigation_governance_action_release_control_execution_state_v0")
        rs = md0.get("navigation_governance_action_release_control_result_v0")
        sig = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_signal_v0"
        )
        ser = md0.get("side_effects_released")

        any_core_present = any(
            isinstance(x, dict)
            for x in [adm, lgate, pc, cg, cdr, ag, ld, live, seg, ds, idr, xs, rs]
        )
        if not any_core_present and sig is None and ser is None:
            return res

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_v0 import (  # noqa: E402
                get_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity,
            )

            sk = (
                get_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity()
            )
        except Exception:
            sk = None

        from capabilities.mid_platform.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_gate_v0 import (  # noqa: E402
            evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_gate_v0,
        )

        applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_gate_v0(
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0=adm,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0=lgate,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0=pc,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_v0=cg,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_dry_run_v0=cdr,
            navigation_governance_action_release_control_first_live_enablement_approval_gate_v0=ag,
            navigation_governance_action_release_control_first_live_launch_dry_run_v0=ld,
            navigation_governance_action_release_control_live_release_gate_v0=live,
            navigation_governance_action_release_control_side_effect_release_gate_v0=seg,
            navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0=ds,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0=idr,
            release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity_v0=sk,
            navigation_governance_action_release_control_execution_state_v0=xs,
            navigation_governance_action_release_control_result_v0=rs,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_signal_v0=sig,
            side_effects_released=ser,
        )
        if not applicable or not isinstance(payload, dict):
            return res

        md0[
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_gate_v0"
        ] = payload

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_v0 import (  # noqa: E402
                accept_first_live_minimal_real_effect_activation_gate,
            )

            _ = accept_first_live_minimal_real_effect_activation_gate(
                minimal_real_effect_activation_gate_v0=payload
            )
        except Exception:
            pass

        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_dry_run_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Release control first live guarded implementation minimal real-effect activation dry-run v0 (non-effect; non-action).

    Writes:
    - result.metadata[
        "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_dry_run_v0"
      ]

    Policy:
    - relevant-only: if none of the core upstream metadata dicts exist, do not write.
    - otherwise, write attempted object with activation_dry_run_status in
      {first_live_minimal_real_effect_activation_ready,
       first_live_minimal_real_effect_activation_not_ready,
       first_live_minimal_real_effect_activation_blocked}.
    - Optional: call implementation skeleton recognition interface (still non-action).
    """
    try:
        md0 = dict(res.metadata or {})

        adm = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0"
        )
        lgate = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0"
        )
        pc = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0"
        )
        cg = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_v0"
        )
        cdr = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_dry_run_v0"
        )
        agate = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_gate_v0"
        )
        ag = md0.get("navigation_governance_action_release_control_first_live_enablement_approval_gate_v0")
        ld = md0.get("navigation_governance_action_release_control_first_live_launch_dry_run_v0")
        live = md0.get("navigation_governance_action_release_control_live_release_gate_v0")
        seg = md0.get("navigation_governance_action_release_control_side_effect_release_gate_v0")
        ds = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0"
        )
        idr = md0.get(
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0"
        )
        xs = md0.get("navigation_governance_action_release_control_execution_state_v0")
        rs = md0.get("navigation_governance_action_release_control_result_v0")
        ser = md0.get("side_effects_released")

        any_core_present = any(
            isinstance(x, dict)
            for x in [adm, lgate, pc, cg, cdr, agate, ag, ld, live, seg, ds, idr, xs, rs]
        )
        if not any_core_present and ser is None:
            return res

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_v0 import (  # noqa: E402
                get_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity,
            )

            sk = (
                get_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity()
            )
        except Exception:
            sk = None

        from capabilities.mid_platform.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_dry_run_v0 import (  # noqa: E402
            evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_dry_run_v0,
        )

        applicable, payload = evaluate_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_dry_run_v0(
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0=adm,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0=lgate,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0=pc,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_v0=cg,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_dry_run_v0=cdr,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_gate_v0=agate,
            navigation_governance_action_release_control_first_live_enablement_approval_gate_v0=ag,
            navigation_governance_action_release_control_first_live_launch_dry_run_v0=ld,
            navigation_governance_action_release_control_live_release_gate_v0=live,
            navigation_governance_action_release_control_side_effect_release_gate_v0=seg,
            navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0=ds,
            navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0=idr,
            release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_identity_v0=sk,
            navigation_governance_action_release_control_execution_state_v0=xs,
            navigation_governance_action_release_control_result_v0=rs,
            side_effects_released=ser,
        )
        if not applicable or not isinstance(payload, dict):
            return res

        md0[
            "navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_dry_run_v0"
        ] = payload

        try:
            from capabilities.governance.runtime.navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_skeleton_v0 import (  # noqa: E402
                accept_first_live_minimal_real_effect_activation_dry_run,
            )

            _ = accept_first_live_minimal_real_effect_activation_dry_run(
                minimal_real_effect_activation_dry_run_v0=payload
            )
        except Exception:
            pass

        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_release_control_minimal_executor_identity_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Release control minimal executor identity v0 (read-only; non-action).

    Writes:
    - result.metadata["navigation_governance_action_release_control_minimal_executor_identity_v0"]
    """
    try:
        md0 = dict(res.metadata or {})
        ident = get_release_control_minimal_executor_identity()
        if not isinstance(ident, dict):
            return res
        md0["navigation_governance_action_release_control_minimal_executor_identity_v0"] = ident
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_attach_navigation_governance_action_release_control_guarded_live_stub_v0(
    res: VoiceFinalTextDispatchResult,
) -> VoiceFinalTextDispatchResult:
    """
    Release control guarded live stub v0 (read-only; non-action).

    Writes:
    - result.metadata["navigation_governance_action_release_control_guarded_live_identity_v0"]
    - result.metadata["navigation_governance_action_release_control_guarded_live_stub_v0"]
    """
    try:
        md0 = dict(res.metadata or {})
        ident = get_release_control_guarded_live_identity()
        if isinstance(ident, dict):
            md0["navigation_governance_action_release_control_guarded_live_identity_v0"] = ident

        stub_state = accept_guarded_live_input(
            executor_input_bridge_v0=md0.get(
                "navigation_governance_action_release_control_executor_input_bridge_v0"
            )
        )
        if isinstance(stub_state, dict):
            md0["navigation_governance_action_release_control_guarded_live_stub_v0"] = stub_state
        return replace(res, metadata=md0)
    except Exception:
        return res


def _maybe_submit_response_template_v0(
    res: VoiceFinalTextDispatchResult,
    template_id: ResponseTemplateIdV0,
    *,
    event: VoiceInputEvent,
) -> VoiceFinalTextDispatchResult:
    """
    Response Submit Template Interface v0 (response-only submit).

    Hard boundary:
    - Does NOT change dispatch/route/proposal.
    - Does NOT start navigation.
    - Only submits a fixed response when trigger conditions are met.
    """
    if not _env_truthy("LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1"):
        return res

    if template_id == "navigation_missing_destination_confirm_v0":
        if not should_trigger_navigation_missing_destination_confirm_v0(res):
            return res
    else:
        # This minimal workspace only wires the navigation template in this change.
        return res

    spec = get_response_submit_template_spec_v0(
        template_id,
        continue_request_info_confirm_text="",
        navigation_missing_destination_confirm_text=NAVIGATION_MISSING_DESTINATION_CONFIRM_TEMPLATE_V0,
    )
    if spec is None or not str(spec.text or "").strip():
        return res

    rid = str(getattr(res, "request_id", "") or getattr(event, "request_id", "") or getattr(event, "event_id", "") or "")
    if not rid.strip():
        return res

    # Always attach a minimal observation envelope for downstream visibility.
    md0 = dict(res.metadata or {})
    md0["response_submit_template_v0"] = {
        "response_submitted": False,
        "response_type": str(spec.response_type),
        "template_id": str(spec.template_id),
        "submit_kind": "response_only",
    }
    res = replace(res, metadata=md0)

    try:
        from capabilities.voice.output.voice_output_plane_v1 import (  # noqa: E402
            get_voice_output_plane_v1,
        )

        plane = get_voice_output_plane_v1()
        req = SpeechRequest(
            request_id=rid,
            source_module=str(spec.source_module or "voice_response_submit_template_v0"),
            output_category="prompt",
            text_candidate=str(spec.text),
            metadata={
                "submit_v1": True,
                "response_submit_template_v0": True,
                "template_id": str(spec.template_id),
                "submit_kind": "response_only",
            },
        )
        sub_ok, _sub_reason = plane.submit(req)
        if not sub_ok:
            return res
    except Exception:
        return res

    md = dict(res.metadata or {})
    payload = md.get("response_submit_template_v0")
    if isinstance(payload, dict):
        payload2 = dict(payload)
        payload2["response_submitted"] = True
        md["response_submit_template_v0"] = payload2
    else:
        md["response_submit_template_v0"] = {
            "response_submitted": True,
            "response_type": str(spec.response_type),
            "template_id": str(spec.template_id),
            "submit_kind": "response_only",
        }
    return replace(res, metadata=md)


def _sidewalk_env_summary_stabilizer_enabled_v1() -> bool:
    """
    默认开启：对 runtime_context.metadata[\"sidewalk_env_summary_v1\"] 先做稳定化再交给旁路。
    设为 0/false/no 可秒退为「直接使用上游原始 dict」。
    """
    v = os.getenv("LUNA_ENABLE_SIDEWALK_ENV_SUMMARY_STABILIZER_V1", "1").strip().lower()
    if v in ("0", "false", "no"):
        return False
    return True


def _retail_env_summary_stabilizer_enabled_v1() -> bool:
    """
    默认开启：对 runtime_context.metadata["retail_env_summary_v1"] 先做稳定化再交给旁路。
    设为 0/false/no 可秒退为「直接使用上游原始 dict」。
    """
    v = os.getenv("LUNA_ENABLE_RETAIL_ENV_SUMMARY_STABILIZER_V1", "1").strip().lower()
    if v in ("0", "false", "no"):
        return False
    return True


def _maybe_stabilize_runtime_context_sidewalk_env_v1(
    event: VoiceInputEvent,
    runtime_context: VoiceRuntimeContext,
) -> VoiceRuntimeContext:
    """
    若存在原始 sidewalk 环境 dict（且尚未带 V1 schema），则 build 后写回 metadata。
    与 risk_summary_v1 无耦合；失败时保持原 context。
    """
    if not _sidewalk_env_summary_stabilizer_enabled_v1():
        return runtime_context
    try:
        md = dict(runtime_context.metadata or {})
        raw = md.get("sidewalk_env_summary_v1")
        if not isinstance(raw, dict):
            return runtime_context
        if str(raw.get("summary_schema_version") or "").startswith("sidewalk_env_summary_v1/"):
            return runtime_context

        from capabilities.cross_domain.context.sidewalk_env_summary_v1 import (  # noqa: E402
            build_sidewalk_env_summary_v1,
        )

        now = float(event.timestamp) if getattr(event, "timestamp", None) not in (None, 0.0) else time.time()
        evt_src = raw.get("event_timestamp")
        if evt_src is not None:
            try:
                event_timestamp = float(evt_src)
            except (TypeError, ValueError):
                event_timestamp = now
        else:
            event_timestamp = now

        built = build_sidewalk_env_summary_v1(
            scene_candidate=str(raw.get("scene_candidate") or "unknown"),
            path_confidence=float(raw.get("path_confidence") or 0.0),
            is_outdoor=bool(raw.get("is_outdoor") or False),
            event_timestamp=event_timestamp,
            now=now,
        )
        md["sidewalk_env_summary_v1"] = built
        return replace(runtime_context, metadata=md)
    except Exception:
        return runtime_context


def _maybe_stabilize_runtime_context_retail_env_v1(
    event: VoiceInputEvent,
    runtime_context: VoiceRuntimeContext,
) -> VoiceRuntimeContext:
    """
    若存在原始 retail 环境 dict（且尚未带 V1 schema），则 build 后写回 metadata。
    与 risk_summary_v1 / find_item_intent_summary_v1 零耦合；失败时保持原 context。
    """
    if not _retail_env_summary_stabilizer_enabled_v1():
        return runtime_context
    try:
        md = dict(runtime_context.metadata or {})
        raw = md.get("retail_env_summary_v1")
        if not isinstance(raw, dict):
            return runtime_context
        if str(raw.get("summary_schema_version") or "").startswith("retail_env_summary_v1/"):
            return runtime_context

        from capabilities.cross_domain.context.retail_env_summary_v1 import (  # noqa: E402
            build_retail_env_summary_v1,
        )

        now = float(event.timestamp) if getattr(event, "timestamp", None) not in (None, 0.0) else time.time()
        evt_src = raw.get("event_timestamp")
        if evt_src is not None:
            try:
                event_timestamp = float(evt_src)
            except (TypeError, ValueError):
                event_timestamp = now
        else:
            event_timestamp = now

        built = build_retail_env_summary_v1(
            scene_type=str(raw.get("scene_type") or ""),
            scene_type_candidate=str(raw.get("scene_type_candidate") or ""),
            retail_context_confidence=float(raw.get("retail_context_confidence") or 0.0),
            shelf_visible=bool(raw.get("shelf_visible") or False),
            gating_passed=(raw.get("gating_passed") if isinstance(raw.get("gating_passed"), bool) else None),
            event_timestamp=event_timestamp,
            now=now,
        )
        md["retail_env_summary_v1"] = built
        return replace(runtime_context, metadata=md)
    except Exception:
        return runtime_context


def _unified_env_shadow_enabled_v1() -> bool:
    """
    unified env shadow：默认关闭；显式 LUNA_ENABLE_UNIFIED_ENV_SHADOW_V1=1/true/yes 才计算并写入
    metadata[\"unified_env_summary_shadow_v1\"]。不参与任何旁路或稳定化决策。
    """
    v = os.getenv("LUNA_ENABLE_UNIFIED_ENV_SHADOW_V1", "").strip().lower()
    return v in ("1", "true", "yes")


def _unified_shadow_raw_inputs_v1(
    md: Dict[str, Any],
    *,
    event: VoiceInputEvent,
) -> Tuple[str, float, float, float]:
    """
    只读从 metadata 推导 build_unified_env_summary_v1 的最小输入。
    优先级：明确 retail 场景 → sidewalk → 其余 retail dict → 缺省 unknown。
    """
    now = float(event.timestamp) if getattr(event, "timestamp", None) not in (None, 0.0) else time.time()
    sw = md.get("sidewalk_env_summary_v1")
    rt = md.get("retail_env_summary_v1")
    sw = sw if isinstance(sw, dict) else None
    rt = rt if isinstance(rt, dict) else None

    def _ts(d: Optional[Dict[str, Any]]) -> float:
        if not d:
            return now
        v = d.get("event_timestamp")
        if v is None:
            return now
        try:
            return float(v)
        except (TypeError, ValueError):
            return now

    rt_scene = ""
    if rt:
        rt_scene = str(rt.get("scene_type_candidate") or rt.get("scene_type") or "").strip().lower()
    retail_like = rt_scene in ("retail_shelf", "retail_aisle") or (
        bool(rt_scene) and rt_scene.startswith("retail_")
    )

    if rt and retail_like:
        cand = str(rt.get("scene_type_candidate") or rt.get("scene_type") or "unknown").strip() or "unknown"
        return cand, float(rt.get("retail_context_confidence") or 0.0), _ts(rt), now

    if sw:
        cand = str(sw.get("scene_candidate") or "unknown").strip() or "unknown"
        return cand, float(sw.get("path_confidence") or 0.0), _ts(sw), now

    if rt:
        cand = str(rt.get("scene_type_candidate") or rt.get("scene_type") or "unknown").strip() or "unknown"
        return cand, float(rt.get("retail_context_confidence") or 0.0), _ts(rt), now

    return "unknown", 0.0, now, now


def _maybe_attach_unified_env_shadow_v1(
    event: VoiceInputEvent,
    runtime_context: VoiceRuntimeContext,
) -> VoiceRuntimeContext:
    """
    在 sidewalk / retail 稳定化之后调用：只读计算 unified env，写入 unified_env_summary_shadow_v1。
    不回写 sidewalk_env_summary_v1 / retail_env_summary_v1 / risk / intent / OCR。
    """
    if not _unified_env_shadow_enabled_v1():
        return runtime_context
    try:
        md = dict(runtime_context.metadata or {})
        cand, conf, evt_ts, now = _unified_shadow_raw_inputs_v1(md, event=event)
        # family_hint：仅用于让 family 更保守地服从“命中垂直源”的域约束，避免跨域字符串污染硬定类
        hint = None
        if isinstance(md.get("retail_env_summary_v1"), dict):
            rt = md.get("retail_env_summary_v1") or {}
            rt_scene = str((rt or {}).get("scene_type_candidate") or (rt or {}).get("scene_type") or "").strip().lower()
            if rt_scene in ("retail_shelf", "retail_aisle") or (bool(rt_scene) and rt_scene.startswith("retail_")):
                hint = "retail"
        if hint is None and isinstance(md.get("sidewalk_env_summary_v1"), dict):
            hint = "walkway"

        from capabilities.cross_domain.context.unified_env_summary_v1 import (  # noqa: E402
            build_unified_env_summary_v1,
        )

        shadow = build_unified_env_summary_v1(
            raw_scene_candidate=cand,
            raw_environment_confidence=conf,
            event_timestamp=evt_ts,
            now=now,
            source="unified_env_shadow_v1",
            raw_family_hint=hint,
        )
        md["unified_env_summary_shadow_v1"] = shadow
        return replace(runtime_context, metadata=md)
    except Exception:
        return runtime_context


def _unified_env_min_wiring_enabled_v1() -> bool:
    """
    unified env 最小接线实验：默认关闭；显式 LUNA_ENABLE_UNIFIED_ENV_MIN_WIRING_V1=1/true/yes
    才写入 metadata["unified_env_fill_shadow_v1"]（只读补缺 + 独立留痕，不驱动任何决策）。
    """
    v = os.getenv("LUNA_ENABLE_UNIFIED_ENV_MIN_WIRING_V1", "").strip().lower()
    return v in ("1", "true", "yes")


def _maybe_attach_unified_env_fill_shadow_v1(
    *,
    event: VoiceInputEvent,
    runtime_context: VoiceRuntimeContext,
) -> VoiceRuntimeContext:
    """
    最小接线实验（V1）：
    - 只读 unified shadow 与垂直 summary
    - 只补白名单字段到独立键 unified_env_fill_shadow_v1（不回写垂直 summary）
    - family/candidate 不一致则直接阻断（更保守）
    """
    if not _unified_env_min_wiring_enabled_v1():
        return runtime_context
    try:
        md_src = dict(runtime_context.metadata or {})

        # 目标垂直源选择：与 shadow 输入优先级保持一致
        sw = md_src.get("sidewalk_env_summary_v1") if isinstance(md_src.get("sidewalk_env_summary_v1"), dict) else None
        rt = md_src.get("retail_env_summary_v1") if isinstance(md_src.get("retail_env_summary_v1"), dict) else None
        target_key = None
        vertical_candidate = "unknown"
        expected_family = "unknown"

        rt_scene = ""
        if rt:
            rt_scene = str(rt.get("scene_type_candidate") or rt.get("scene_type") or "").strip().lower()
        retail_like = rt_scene in ("retail_shelf", "retail_aisle") or (bool(rt_scene) and rt_scene.startswith("retail_"))
        if rt and retail_like:
            target_key = "retail_env_summary_v1"
            vertical_candidate = str(rt.get("scene_type_candidate") or rt.get("scene_type") or "unknown").strip() or "unknown"
            expected_family = "retail"
        elif sw:
            target_key = "sidewalk_env_summary_v1"
            vertical_candidate = str(sw.get("scene_candidate") or "unknown").strip() or "unknown"
            # 期望家族：保守推导（仅对 walkway marker 判定为 walkway，否则 unknown）
            vc = (vertical_candidate or "").strip().lower()
            markers = ("outdoor_walkway", "walkway", "sidewalk", "pedestrian", "path_outdoor")
            expected_family = "walkway" if (any(m in vc for m in markers) or vc == "outdoor") else "unknown"
        elif rt:
            target_key = "retail_env_summary_v1"
            vertical_candidate = str(rt.get("scene_type_candidate") or rt.get("scene_type") or "unknown").strip() or "unknown"
            expected_family = "unknown"

        blocked: List[str] = []
        if not target_key:
            blocked.append("target_summary_missing")

        uni = md_src.get("unified_env_summary_shadow_v1")
        if not isinstance(uni, dict) or not uni:
            blocked.append("missing_unified_shadow")
            uni = {}

        u_family = str(uni.get("scene_family") or "unknown").strip().lower() or "unknown"
        u_candidate = str(uni.get("scene_candidate") or "unknown").strip() or "unknown"

        # 更保守：family/candidate 任一不一致直接阻断
        if target_key and u_family != expected_family:
            blocked.append("family_candidate_mismatch")
        if target_key and (u_candidate or "").strip().lower() != (vertical_candidate or "").strip().lower():
            blocked.append("family_candidate_mismatch")

        allow_fields = ("summary_freshness", "ttl_ms", "confidence_weight", "age_ms", "inference_notes")
        filled_fields: List[str] = []
        filled: Dict[str, Any] = {}

        if not blocked and target_key:
            tgt = md_src.get(target_key)
            if not isinstance(tgt, dict):
                blocked.append("target_summary_missing")
            else:
                for k in allow_fields:
                    if k in tgt and tgt.get(k) is not None:
                        blocked.append(f"target_has_value:{k}")
                        continue
                    if k not in uni:
                        blocked.append(f"unified_missing:{k}")
                        continue
                    filled_fields.append(k)
                    filled[k] = uni.get(k)

        fill_applied = bool(filled_fields) and not any(r.startswith("family_candidate_mismatch") for r in blocked)
        payload = {
            "fill_applied": bool(fill_applied),
            "target_summary_key": str(target_key or ""),
            "filled_fields": list(filled_fields),
            "fill_source": "unified_env_summary_shadow_v1",
            "fill_blocked_reason": list(dict.fromkeys(blocked)),  # stable de-dup, keep order
            "related_unified_schema_version": str(uni.get("summary_schema_version") or ""),
            # 附带对照信息（不参与消费）：便于离线复盘
            "vertical_expected_family": str(expected_family),
            "unified_family": str(u_family),
            "vertical_candidate": str(vertical_candidate),
            "unified_candidate": str(u_candidate),
            "filled": dict(filled),
        }

        md2 = dict(md_src)
        md2["unified_env_fill_shadow_v1"] = payload
        return replace(runtime_context, metadata=md2)
    except Exception:
        return runtime_context


def _unified_env_shadow_snapshot_enabled_v1() -> bool:
    """
    unified env shadow snapshot：默认关闭；显式 LUNA_ENABLE_UNIFIED_ENV_SHADOW_SNAPSHOT_V1=1/true/yes
    才会写入独立 JSONL 观测事件。失败吞掉，不影响主链。
    """
    v = os.getenv("LUNA_ENABLE_UNIFIED_ENV_SHADOW_SNAPSHOT_V1", "").strip().lower()
    return v in ("1", "true", "yes")


def _emit_unified_env_shadow_snapshot_jsonl_v1(payload: Dict[str, Any]) -> None:
    try:
        import json
        from pathlib import Path

        pth = os.getenv(
            "LUNA_UNIFIED_ENV_SHADOW_SNAPSHOT_V1_JSONL",
            "logs/unified_env_shadow_snapshot_v1.jsonl",
        )
        Path(pth).parent.mkdir(parents=True, exist_ok=True)
        with Path(pth).open("a", encoding="utf-8") as f:
            f.write(json.dumps({"type": "unified_env_shadow_snapshot", "data": payload}, ensure_ascii=False) + "\n")
    except Exception:
        return


def _maybe_emit_unified_env_shadow_snapshot_v1(
    *,
    event: VoiceInputEvent,
    runtime_context: VoiceRuntimeContext,
) -> None:
    """
    仅观测落盘：在 unified shadow 已写入（或可由当前 metadata 计算）后，
    写一条 analyzer 可消费的最小 snapshot JSONL。

    - 不回写任何 summary key
    - 不参与任何决策
    - 失败吞掉
    """
    if not _unified_env_shadow_snapshot_enabled_v1():
        return
    try:
        md_src = runtime_context.metadata or {}
        md: Dict[str, Any] = {}

        # 白名单：只保留分析所需的最小三键（存在且为 dict 时）
        for k in ("sidewalk_env_summary_v1", "retail_env_summary_v1", "unified_env_summary_shadow_v1"):
            v = md_src.get(k)
            if isinstance(v, dict):
                md[k] = v

        # 若 runtime_context 尚未携带 shadow key，但 snapshot 开关开启，允许在 payload 内补齐一份 shadow
        if "unified_env_summary_shadow_v1" not in md:
            try:
                from capabilities.cross_domain.context.unified_env_summary_v1 import (  # noqa: E402
                    build_unified_env_summary_v1,
                )

                cand, conf, evt_ts, now = _unified_shadow_raw_inputs_v1(dict(md_src), event=event)
                hint = None
                if isinstance(md_src.get("retail_env_summary_v1"), dict):
                    rt = md_src.get("retail_env_summary_v1") or {}
                    rt_scene = str((rt or {}).get("scene_type_candidate") or (rt or {}).get("scene_type") or "").strip().lower()
                    if rt_scene in ("retail_shelf", "retail_aisle") or (bool(rt_scene) and rt_scene.startswith("retail_")):
                        hint = "retail"
                if hint is None and isinstance(md_src.get("sidewalk_env_summary_v1"), dict):
                    hint = "walkway"
                md["unified_env_summary_shadow_v1"] = build_unified_env_summary_v1(
                    raw_scene_candidate=cand,
                    raw_environment_confidence=conf,
                    event_timestamp=evt_ts,
                    now=now,
                    source="unified_env_shadow_snapshot_v1",
                    raw_family_hint=hint,
                )
            except Exception:
                pass

        ev_ts = float(event.timestamp) if getattr(event, "timestamp", None) not in (None, 0.0) else time.time()
        rid = str(event.request_id or event.event_id or "")
        payload = {
            "timestamp": time.time(),
            "event_timestamp": ev_ts,
            "related_request_id": rid,
            "source": "voice_final_text_dispatcher_v1",
            "metadata": md,
        }
        _emit_unified_env_shadow_snapshot_jsonl_v1(payload)
    except Exception:
        return


def _emit_trace_envelope_v1(typ: str, data: dict) -> None:
    try:
        import json
        from pathlib import Path

        pth = os.getenv("LUNA_REAL_OUTPUT_SUBMIT_V1_TRACE_JSONL", "logs/real_output_submit_v1.jsonl")
        Path(pth).parent.mkdir(parents=True, exist_ok=True)
        with Path(pth).open("a", encoding="utf-8") as f:
            f.write(json.dumps({"type": typ, "data": data}, ensure_ascii=False) + "\n")
    except Exception:
        return


def _emit_pilot_state_transition_v1(
    *,
    transition: str,
    reason: str,
    related_request_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> None:
    try:
        from dataclasses import asdict

        obs = PilotStateTransitionObservation(
            timestamp=time.time(),
            transition=str(transition),
            reason=str(reason),
            related_request_id=str(related_request_id) if related_request_id else None,
            metadata=dict(metadata or {}),
        )
        _emit_trace_envelope_v1("pilot_state_transition", asdict(obs))
    except Exception:
        return


_LAST_PILOT_SWITCH_SNAPSHOT_V1: Optional[Dict[str, bool]] = None


def _maybe_emit_operator_toggle_transitions_v1() -> None:
    """
    V1：由于回退/退出通常由开关触发（运维动作），缺少集中治理入口时，
    这里采用“在主线每轮执行时检测开关变化并发出状态切换观测”的最小做法。

    说明：
    - 这是观测层补齐，不改变任何业务行为。
    - 仅在开关从 on->off 时发出一次 transition。
    """
    global _LAST_PILOT_SWITCH_SNAPSHOT_V1

    snap = {
        "risk_on": _env_truthy("LUNA_ENABLE_RISK_INTERRUPT_V1"),
        "level2a_on": _env_truthy("LUNA_ENABLE_RISK_INTERRUPT_V1_LEVEL2_PILOT"),
        "level2b_on": _env_truthy("LUNA_ENABLE_RISK_INTERRUPT_V1_CANCEL_REPLACE_PILOT"),
        "submit_on": _env_truthy("LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1"),
    }
    prev = _LAST_PILOT_SWITCH_SNAPSHOT_V1
    _LAST_PILOT_SWITCH_SNAPSHOT_V1 = snap
    if not prev:
        return

    md = {"switch_snapshot_prev": prev, "switch_snapshot_now": snap}

    # Level2B -> Level2A：关掉 cancel+replace 试点但 Level2A 仍开
    if prev.get("level2b_on") and (not snap.get("level2b_on")) and snap.get("level2a_on"):
        _emit_pilot_state_transition_v1(transition="level2b_to_level2a", reason="operator_toggle", metadata=md)

    # Level2A -> Level1：关掉 Level2A 试点，但 risk 仍开（回到白盒/Level1 口径）
    if prev.get("level2a_on") and (not snap.get("level2a_on")) and snap.get("risk_on"):
        _emit_pilot_state_transition_v1(transition="level2a_to_level1", reason="operator_toggle", metadata=md)

    # Any -> Level0：关掉 risk 或 submit（按当前工程口径，这两种都会让试点链路失效）
    if (prev.get("risk_on") and (not snap.get("risk_on"))) or (prev.get("submit_on") and (not snap.get("submit_on"))):
        _emit_pilot_state_transition_v1(transition="any_to_level0", reason="operator_toggle", metadata=md)


def _risk_level_from_attached_sources_v1(res: VoiceFinalTextDispatchResult) -> str:
    """
    V1 极小实现：仅从 res.metadata 中读取 risk_summary_v1（若上游已附加）。
    不读取旁路白盒，避免用白盒冒充真状态。
    """
    md = res.metadata or {}
    rs = md.get("risk_summary_v1")
    if isinstance(rs, dict):
        return str(rs.get("risk_level") or "")
    return ""


def _maybe_submit_real_output_v1(
    res: VoiceFinalTextDispatchResult,
    *,
    event: VoiceInputEvent,
    runtime_context: Optional[VoiceRuntimeContext] = None,
    session_state_anchor: Any = None,
) -> None:
    """
    最小 submit 闭环（V1）：
    - 默认关闭
    - 仅允许“原主链稳定输出”的提示/确认类短文本（当前仅覆盖 rejected_input / session_wake）
    - 不修改 res，不接 speaking/runtime
    """
    if not _env_truthy("LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1"):
        return

    _maybe_emit_operator_toggle_transitions_v1()

    text_candidate = ""
    output_category = "prompt"
    source_module = "voice_mainline_v1"

    # 1) rejected_input：直接使用 rejection reason 作为提示文本（短文本、可枚举）
    if res.rejected_input and res.rejection_result is not None:
        text_candidate = str(res.rejection_result.reason or "").strip()
        output_category = "prompt"
    # 2) short_controlled_input + session_wake：最小确认提示
    elif (
        res.short_controlled_input
        and res.bridge_decision is not None
        and str(getattr(getattr(res.bridge_decision, "route", None), "value", getattr(res.bridge_decision, "route", "")))
        == "session_wake"
    ):
        text_candidate = "我在。"
        output_category = "prompt"

    text_candidate = (text_candidate or "").strip()
    if not text_candidate:
        return

    # Minimal No Fabrication guard for placeholder/unknown outputs (V1 verification).
    low = text_candidate.lower()
    if any(tok in low for tok in ("unknown", "todo", "placeholder", "n/a", "none")):
        text_candidate = "这个我现在不能确定。"

    # 最小长度限制（避免长文本误入）
    if len(text_candidate) > 80:
        text_candidate = text_candidate[:80]

    # risk_interrupt_v1 Level 2 pilot（极小试点）：仅允许 high/critical 抢占低价值 prompt/confirmation（提交前替换）
    pilot_on = _env_truthy("LUNA_ENABLE_RISK_INTERRUPT_V1_LEVEL2_PILOT")
    cancel_replace_on = _env_truthy("LUNA_ENABLE_RISK_INTERRUPT_V1_CANCEL_REPLACE_PILOT")
    try:
        from capabilities.cross_domain.risk_interrupt_v1 import (  # noqa: E402
            risk_interrupt_enabled,
            risk_interrupt_whitebox_only,
        )

        risk_on = bool(risk_interrupt_enabled())
        risk_wb_only = bool(risk_interrupt_whitebox_only())
    except Exception:
        risk_on = False
        risk_wb_only = True

    if pilot_on and risk_on and (not risk_wb_only) and output_category in ("prompt", "confirmation"):
        rs = _risk_summary_v1_for_orchestrator_observation(event=event, runtime_context=runtime_context)
        lv = str(rs.get("risk_level") or "").strip().lower()
        if lv in ("high", "critical"):
            original = text_candidate
            text_candidate = "注意安全，前方有风险，请先停一下。"
            try:
                import uuid
                from dataclasses import asdict

                od = OutputDecisionObservation(
                    observation_id=f"od_{uuid.uuid4().hex[:12]}",
                    timestamp=time.time(),
                    request_id=str(res.request_id or ""),
                    accepted=True,
                    reason="risk_interrupt_v1_level2_pilot_preempt_before_submit",
                    cooldown_key=None,
                    metadata={
                        "pilot": True,
                        "risk_level": lv,
                        "preempted_output_category": output_category,
                        "original_text_len": len(original),
                    },
                )
                _emit_trace_envelope_v1("output_decision", asdict(od))
            except Exception:
                pass

    # cancel+replace 受限试点（仅取消待执行 request）：不替换当前试点，不扩边界
    # 条件：开关开启 + risk high/critical + prompt/confirmation + risk enabled + NOT whitebox_only
    cancel_replace_fallback_reason = ""
    cancel_replace_chain_closed = False
    replacement_request_id: Optional[str] = None
    cancel_replace_risk_level: str = ""
    cancel_replace_target_output_category: str = ""
    if cancel_replace_on and risk_on and (not risk_wb_only) and output_category in ("prompt", "confirmation"):
        rs2 = _risk_summary_v1_for_orchestrator_observation(event=event, runtime_context=runtime_context)
        lv2 = str(rs2.get("risk_level") or "").strip().lower()
        cancel_replace_risk_level = lv2
        cancel_replace_target_output_category = str(output_category or "")
        if lv2 in ("high", "critical"):
            try:
                # 仅允许取消“待执行/未 started”的 request（明确禁止取消已 started playback）
                from capabilities.voice.output.audio_worker_v1 import get_audio_worker_v1  # noqa: E402
                from capabilities.voice.output.playback_plane_v1 import get_playback_plane_v1  # noqa: E402

                worker = get_audio_worker_v1()
                st = worker.snapshot_state()
                # 优先取消 queued_request_id；若无 queued 且 current 未 started，则允许取消 current（仍属于“进入执行层但未 started”）
                target_rid = st.get("queued_request_id") or ""
                if not target_rid:
                    if st.get("current_request_id") and (st.get("current_started") is False):
                        target_rid = str(st.get("current_request_id") or "")

                if not target_rid:
                    cancel_replace_fallback_reason = "no_pending_request"
                else:
                    # 强制禁止：若 target 恰好是 current_started=True 的情况
                    if st.get("current_request_id") == target_rid and st.get("current_started") is True:
                        cancel_replace_fallback_reason = "started_playback_forbidden"
                    else:
                        plane2 = get_playback_plane_v1()
                        ok_cancel, cancel_reason = plane2.cancel(
                            request_id=str(target_rid),
                            reason="risk_interrupt_cancel_replace_pilot",
                        )
                        if not ok_cancel:
                            cancel_replace_fallback_reason = f"cancel_failed:{cancel_reason}"
                        else:
                            # 等待执行层确认 cancelled（极小时间窗；不闭合则回退到 preempt-before-submit）
                            t0 = time.time()
                            timeout_ms = int(os.getenv("LUNA_RISK_INTERRUPT_CANCEL_REPLACE_WAIT_MS", "120") or "120")
                            confirmed = False
                            while (time.time() - t0) * 1000.0 <= timeout_ms:
                                try:
                                    import json
                                    from pathlib import Path

                                    pth = os.getenv("LUNA_REAL_OUTPUT_SUBMIT_V1_TRACE_JSONL", "logs/real_output_submit_v1.jsonl")
                                    if Path(pth).exists():
                                        for ln in Path(pth).read_text(encoding="utf-8").splitlines()[-200:]:
                                            try:
                                                row = json.loads(ln)
                                            except Exception:
                                                continue
                                            if row.get("type") != "playback_runtime":
                                                continue
                                            d = row.get("data") if isinstance(row.get("data"), dict) else {}
                                            if d.get("request_id") != str(target_rid):
                                                continue
                                            if d.get("event") == "playback_cancelled":
                                                confirmed = True
                                                break
                                except Exception:
                                    pass
                                if confirmed:
                                    break
                                time.sleep(0.01)

                            if not confirmed:
                                cancel_replace_fallback_reason = "cancel_terminal_not_observed"
                            else:
                                cancel_replace_chain_closed = True
                                # cancel 成功后才允许 replace submit：提交新的风险提示 request
                                import uuid

                                replacement_request_id = f"{res.request_id}_risk_{uuid.uuid4().hex[:8]}"
                                # 直接替换本次将提交的 request（本次 request_id 改为 replacement_request_id）
                                # 注意：不改变 submit 候选范围（仍为 prompt），仅替换 request_id 与文本
                                text_candidate = "注意安全，前方有风险，请先停一下。"
            except Exception as e:
                cancel_replace_fallback_reason = f"exception:{type(e).__name__}"

    # 若 Level2B attempt 发生但链不闭合，则显式记录一次 “Level2B -> Level2A” 的回退状态切换事实
    if cancel_replace_on and risk_on and (not risk_wb_only):
        if (not cancel_replace_chain_closed) and str(cancel_replace_fallback_reason or "").strip():
            _emit_pilot_state_transition_v1(
                transition="level2b_to_level2a",
                reason="observation_chain_broken" if cancel_replace_fallback_reason == "cancel_terminal_not_observed" else "guardrail_violation",
                related_request_id=str(res.request_id or "") or None,
                metadata={"failure_reason": str(cancel_replace_fallback_reason)},
            )

    try:
        from capabilities.voice.output.voice_output_plane_v1 import (  # noqa: E402
            get_voice_output_plane_v1,
        )

        plane = get_voice_output_plane_v1()
        # request_created：SpeechRequest 已构造（但尚未提交）
        # 该事件不代表 submit 发生；submit 真锚点在 VoiceOutputPlane.submit 内发出 request_submitted。
        req = SpeechRequest(
            request_id=str(replacement_request_id or res.request_id or ""),
            source_module=source_module,
            output_category=output_category,
            text_candidate=text_candidate,
            metadata={
                "submit_v1": True,
                "risk_interrupt_v1_level2_pilot": bool(pilot_on),
                "risk_interrupt_v1_cancel_replace_pilot": bool(cancel_replace_on),
            },
        )
        try:
            from dataclasses import asdict
            ts = time.time()
            rr_created = RequestRuntimeObservation(
                request_id=req.request_id,
                timestamp=ts,
                event="request_created",
                status="ok",
                reason="speech_request_constructed",
                metadata={"source_module": source_module, "output_category": output_category},
            )
            _emit_trace_envelope_v1("request_runtime", asdict(rr_created))
        except Exception:
            pass

        # 观测：是否走了 cancel+replace，是否回退到 preempt
        try:
            import uuid
            from dataclasses import asdict

            od2 = OutputDecisionObservation(
                observation_id=f"od_{uuid.uuid4().hex[:12]}",
                timestamp=time.time(),
                request_id=str(res.request_id or ""),
                accepted=True,
                reason="risk_interrupt_v1_cancel_replace_pilot_evaluated",
                cooldown_key=None,
                metadata={
                    "cancel_replace_on": bool(cancel_replace_on),
                    "cancel_replace_chain_closed": bool(cancel_replace_chain_closed),
                    "fallback_to_preempt_before_submit": bool(bool(cancel_replace_fallback_reason) and not cancel_replace_chain_closed),
                    "failure_reason": str(cancel_replace_fallback_reason or ""),
                    "replacement_request_id": str(replacement_request_id or ""),
                    "risk_level": str(cancel_replace_risk_level or ""),
                    "target_output_category": str(cancel_replace_target_output_category or ""),
                },
            )
            _emit_trace_envelope_v1("output_decision", asdict(od2))
        except Exception:
            pass
        sub_ok, _sub_reason = plane.submit(req)
        if session_state_anchor is not None and bool(sub_ok):
            try:
                session_state_anchor.record_successful_output(
                    spoken_text=text_candidate, request_id=str(req.request_id or "")
                )
            except Exception:
                pass
    except Exception:
        # 默认安全：submit 出错不影响主链结果
        return


def _risk_summary_v1_for_orchestrator_observation(
    *,
    event: VoiceInputEvent,
    runtime_context: Optional[VoiceRuntimeContext] = None,
) -> Dict[str, Any]:
    src: Dict[str, Any] = {}
    if runtime_context is not None and isinstance(getattr(runtime_context, "metadata", None), dict):
        rs = (runtime_context.metadata or {}).get("risk_summary_v1")
        if isinstance(rs, dict):
            src = rs
    if not src and isinstance(getattr(event, "metadata", None), dict):
        rs2 = (event.metadata or {}).get("risk_summary_v1")
        if isinstance(rs2, dict):
            src = rs2
    return src


def _risk_preempt_active_v1(risk_summary: Dict[str, Any]) -> bool:
    if not risk_summary:
        return False
    if bool(risk_summary.get("risk_interrupt_preempt")):
        return True
    lv = str(risk_summary.get("risk_level") or "").strip().lower()
    return lv in ("high", "critical")


def _collect_cross_domain_capability_switch_state_v1() -> Tuple[List[str], bool]:
    """
    返回 (enabled_capabilities 按固定顺序, whitebox_only_mode：三模块均可导入且 *_whitebox_only 均为 True)。
    """
    enabled: List[str] = []
    wb_ok_count = 0
    wb_all_true = True
    try:
        from capabilities.cross_domain.risk_interrupt_v1 import (  # noqa: E402
            risk_interrupt_enabled,
            risk_interrupt_whitebox_only,
        )

        if risk_interrupt_enabled():
            enabled.append("risk_interrupt_v1")
        wb_ok_count += 1
        wb_all_true = wb_all_true and bool(risk_interrupt_whitebox_only())
    except Exception:
        wb_all_true = False

    try:
        from capabilities.cross_domain.sidewalk_nav_v1.evaluate import (  # noqa: E402
            sidewalk_nav_enabled,
            sidewalk_nav_whitebox_only,
        )

        if sidewalk_nav_enabled():
            enabled.append("sidewalk_nav_v1")
        wb_ok_count += 1
        wb_all_true = wb_all_true and bool(sidewalk_nav_whitebox_only())
    except Exception:
        wb_all_true = False

    try:
        from capabilities.cross_domain.retail_find_item_v1.evaluate import (  # noqa: E402
            retail_find_item_enabled,
            retail_find_item_whitebox_only,
        )

        if retail_find_item_enabled():
            enabled.append("retail_find_item_v1")
        wb_ok_count += 1
        wb_all_true = wb_all_true and bool(retail_find_item_whitebox_only())
    except Exception:
        wb_all_true = False

    whitebox_only_mode = wb_ok_count == 3 and wb_all_true
    return enabled, whitebox_only_mode


def _attach_cross_domain_orchestrator_v1_summary(
    res: VoiceFinalTextDispatchResult,
    *,
    event: VoiceInputEvent,
    runtime_context: Optional[VoiceRuntimeContext] = None,
) -> VoiceFinalTextDispatchResult:
    """
    编排层统一白盒摘要：不复制三条旁路全量字段，不改旁路内部结构。
    全关（无任何旁路开关启用）时不写入 cross_domain_orchestrator_v1。
    """
    enabled_capabilities, whitebox_only_mode = _collect_cross_domain_capability_switch_state_v1()
    if not enabled_capabilities:
        return res

    md = dict(res.metadata or {})
    executed_capabilities = [k for k in _CROSS_DOMAIN_ORCH_V1_METADATA_KEYS if k in md]
    suppressed_capabilities: List[str] = []
    sw = md.get("sidewalk_nav_v1")
    if isinstance(sw, dict) and sw.get("output_suppressed_by_risk") is True:
        suppressed_capabilities.append("sidewalk_nav_v1")
    rt = md.get("retail_find_item_v1")
    if isinstance(rt, dict) and rt.get("output_suppressed_by_risk") is True:
        suppressed_capabilities.append("retail_find_item_v1")

    risk_summary = _risk_summary_v1_for_orchestrator_observation(
        event=event, runtime_context=runtime_context
    )
    risk_preempt_active = _risk_preempt_active_v1(risk_summary)

    metadata_keys_attached = [k for k in _CROSS_DOMAIN_ORCH_V1_METADATA_KEYS if k in md]

    ts_ms = getattr(event, "timestamp", None)
    try:
        event_timestamp = float(ts_ms) * 1000.0 if ts_ms is not None else time.time() * 1000.0
    except (TypeError, ValueError):
        event_timestamp = time.time() * 1000.0

    summary: Dict[str, Any] = {
        "enabled_capabilities": list(enabled_capabilities),
        "executed_capabilities": executed_capabilities,
        "suppressed_capabilities": suppressed_capabilities,
        "risk_preempt_active": risk_preempt_active,
        "whitebox_only_mode": whitebox_only_mode,
        "metadata_keys_attached": metadata_keys_attached,
        "orchestration_order": list(_CROSS_DOMAIN_ORCH_V1_ORDER),
        "event_timestamp": event_timestamp,
        "near_real_output_candidate_any": False,
    }
    md["cross_domain_orchestrator_v1"] = summary
    return replace(res, metadata=md)


def _run_cross_domain_orchestrator_v1(
    res: VoiceFinalTextDispatchResult,
    *,
    event: VoiceInputEvent,
    runtime_context: Optional[VoiceRuntimeContext] = None,
) -> VoiceFinalTextDispatchResult:
    """
    统一主线旁路编排入口（V1，最小）。

    目标（写死）：
    - 只做 Level 1 / whitebox-only 编排（不做 Level 2、不做 speaking/runtime 接管）
    - 顺序固定：risk_interrupt_v1 → sidewalk_nav_v1 → retail_find_item_v1
    - 统一传递 runtime_context
    - 统一合并 metadata（仍保持三个并列 key）

    回退边界：
    - 如需紧急回退，可设置 LUNA_DISABLE_CROSS_DOMAIN_ORCHESTRATOR_V1=1，恢复为“分散 helper 串联”逻辑。
    """
    if _env_truthy("LUNA_DISABLE_CROSS_DOMAIN_ORCHESTRATOR_V1"):
        # legacy path: keep prior behavior (explicit chaining)
        out = _maybe_attach_risk_interrupt_v1_whitebox(res, event=event, runtime_context=runtime_context)
        out = _maybe_attach_sidewalk_nav_v1_whitebox(out, event=event, runtime_context=runtime_context)
        out = _maybe_attach_retail_find_item_v1_whitebox(out, event=event, runtime_context=runtime_context)
        return _attach_cross_domain_orchestrator_v1_summary(
            out, event=event, runtime_context=runtime_context
        )

    out = _maybe_attach_risk_interrupt_v1_whitebox(res, event=event, runtime_context=runtime_context)
    out = _maybe_attach_sidewalk_nav_v1_whitebox(out, event=event, runtime_context=runtime_context)
    out = _maybe_attach_retail_find_item_v1_whitebox(out, event=event, runtime_context=runtime_context)
    return _attach_cross_domain_orchestrator_v1_summary(out, event=event, runtime_context=runtime_context)

def _maybe_attach_risk_interrupt_v1_whitebox(
    res: VoiceFinalTextDispatchResult,
    *,
    event: VoiceInputEvent,
    runtime_context: Optional[VoiceRuntimeContext] = None,
) -> VoiceFinalTextDispatchResult:
    """
    风险打断 V1 深接入（阶段 1）：只做 Level 1 / whitebox-only 的真实主线挂载。

    约束：
    - 仅当 LUNA_ENABLE_RISK_INTERRUPT_V1=1 且 LUNA_RISK_INTERRUPT_WHITEBOX_ONLY=1 时生效
    - 不改变 dispatch_type / notes / 任何输出文本；只并入 metadata["risk_interrupt_v1"]
    - 不执行真实抢占（即使用户把 WHITEBOX_ONLY 关掉，也不在本阶段启用）
    """
    try:
        from capabilities.cross_domain.risk_interrupt_v1 import (  # noqa: E402
            OutputStateSnapshot,
            RiskInterruptEventV1,
            TaskChainStateSnapshot,
            handle_risk_interrupt_v1,
            risk_interrupt_enabled,
            risk_interrupt_whitebox_only,
        )
    except Exception:
        return res

    if not risk_interrupt_enabled():
        return res
    if not risk_interrupt_whitebox_only():
        # 深联调阶段 1：写死只允许 whitebox-only
        return res

    # speaking 的真实运行态在本 repo 的 Stage-1 dispatcher 中不可得；
    # 深联调阶段 1 以“本轮将要下发的候选输出”作为可观测替代，并写入白盒 original_output。
    speaking_observable = False
    output_category = str((res.metadata or {}).get("output_category") or res.dispatch_type or "unknown")
    output_digest = str((res.metadata or {}).get("output_digest") or "")

    # 风险事件来源（阶段 1.5）：优先读 runtime_context.metadata["risk_summary_v1"]，缺失时回退到 event.metadata 占位。
    # 不做多来源融合，只做单一路径优先级切换。
    src: Dict[str, Any] = {}
    if runtime_context is not None and isinstance(getattr(runtime_context, "metadata", None), dict):
        rs = runtime_context.metadata.get("risk_summary_v1")
        if isinstance(rs, dict):
            src = rs

    fallback_evm = event.metadata or {}
    risk_level = str(src.get("risk_level") or fallback_evm.get("risk_level") or fallback_evm.get("risk_level_hint") or "unknown")
    risk_type = str(src.get("risk_type") or fallback_evm.get("risk_type") or "unknown")
    direction_hint = str(src.get("direction_hint") or fallback_evm.get("direction_hint") or "unknown")
    distance_band = str(src.get("distance_band") or fallback_evm.get("distance_band") or "unknown")
    confidence = float(src.get("confidence") if src.get("confidence") is not None else (fallback_evm.get("risk_confidence") or 0.0))

    ts_ms = None
    if src.get("timestamp_ms") is not None:
        try:
            ts_ms = int(src.get("timestamp_ms"))
        except Exception:
            ts_ms = None
    if ts_ms is None and getattr(event, "timestamp", None) is not None:
        try:
            ts_ms = int(float(event.timestamp) * 1000.0)
        except Exception:
            ts_ms = None

    decision = handle_risk_interrupt_v1(
        event=RiskInterruptEventV1.new(
            risk_type=risk_type,
            risk_level=risk_level,
            direction_hint=direction_hint,
            distance_band=distance_band,
            confidence=confidence,
            timestamp_ms=ts_ms,
        ),
        current_output=OutputStateSnapshot(
            speaking=speaking_observable,
            output_category=output_category,
            output_digest=output_digest,
        ),
        task_state=TaskChainStateSnapshot(
            task_chain_id=str(event.session_id or event.request_id or ""),
            task_status="running",
        ),
    )

    wb = decision.metadata.get("risk_interrupt_v1", {})
    if not isinstance(wb, dict) or not wb:
        return res

    meta2 = dict(res.metadata or {})
    meta2["risk_interrupt_v1"] = wb
    return replace(res, metadata=meta2)

def _maybe_attach_sidewalk_nav_v1_whitebox(
    res: VoiceFinalTextDispatchResult,
    *,
    event: VoiceInputEvent,
    runtime_context: Optional[VoiceRuntimeContext] = None,
) -> VoiceFinalTextDispatchResult:
    """
    人行道导航 V1 深接入（阶段 1）：只做 whitebox-only 的真实主线挂载。

    约束：
    - 仅当 LUNA_ENABLE_SIDEWALK_NAV_V1=1 且 LUNA_SIDEWALK_NAV_WHITEBOX_ONLY=1 时生效
    - 不进入真实输出候选：强制不外显（final_spoken_output 置空）
    - 风险链优先：若 risk_level 为 high/critical 或 risk_interrupt_preempt=true，则压制标记必须成立
    - 不改变 dispatch_type / notes / 任何输出文本；只并入 metadata["sidewalk_nav_v1"]
    """
    try:
        from capabilities.cross_domain.sidewalk_nav_v1 import (  # noqa: E402
            RiskSummaryInput,
            SidewalkEnvironmentInput,
            evaluate_sidewalk_nav_v1,
            sidewalk_nav_enabled,
            sidewalk_nav_whitebox_only,
        )
    except Exception:
        return res

    if not sidewalk_nav_enabled():
        return res
    if not sidewalk_nav_whitebox_only():
        # 深联调阶段 1：写死只允许 whitebox-only
        return res

    # 1) 环境摘要：优先从 runtime_context 注入；缺失则用安全的 unknown 占位（仍可留白盒）。
    env_src: Dict[str, Any] = {}
    if runtime_context is not None and isinstance(getattr(runtime_context, "metadata", None), dict):
        se = runtime_context.metadata.get("sidewalk_env_summary_v1")
        if isinstance(se, dict):
            env_src = se

    env = SidewalkEnvironmentInput(
        scene_candidate=str(env_src.get("scene_candidate") or "unknown"),
        path_confidence=float(env_src.get("path_confidence") or 0.0),
        is_outdoor=bool(env_src.get("is_outdoor") or False),
    )

    # 2) 风险摘要：复用 risk_interrupt 已对齐的 runtime_context.metadata["risk_summary_v1"]（若无则回退 unknown/low）。
    risk_src: Dict[str, Any] = {}
    if runtime_context is not None and isinstance(getattr(runtime_context, "metadata", None), dict):
        rs = runtime_context.metadata.get("risk_summary_v1")
        if isinstance(rs, dict):
            risk_src = rs
    fallback_evm = event.metadata or {}
    risk_level = str(risk_src.get("risk_level") or fallback_evm.get("risk_level") or "low")
    risk_type = str(risk_src.get("risk_type") or fallback_evm.get("risk_type") or "")
    safe_direction_hint = str(risk_src.get("safe_direction_hint") or "")
    risk_interrupt_preempt = bool(risk_src.get("risk_interrupt_preempt") or risk_src.get("risk_interrupt_preempt", False))

    # 高风险也视为压制信号（写死口径）
    lv = (risk_level or "").strip().lower()
    suppressed = bool(risk_interrupt_preempt or (lv in ("high", "critical")))

    # 3) 调用旁路，生成白盒；深接入阶段强制不外显（即使未来误配 WHITEBOX_ONLY=0，也不推候选）
    r = evaluate_sidewalk_nav_v1(
        environment=env,
        risk=RiskSummaryInput(
            risk_level=risk_level,
            risk_type=risk_type,
            safe_direction_hint=safe_direction_hint,
        ),
        timestamp_ms=int(float(event.timestamp) * 1000.0) if getattr(event, "timestamp", None) is not None else None,
        risk_interrupt_preempt=bool(suppressed),
    )

    wb = r.metadata.get("sidewalk_nav_v1") if isinstance(r.metadata, dict) else None
    if not isinstance(wb, dict) or not wb:
        return res

    # 写死 whitebox-only 深接入：不外显
    wb2 = dict(wb)
    wb2["final_spoken_output"] = ""
    wb2["whitebox_only"] = True
    if suppressed:
        wb2["output_suppressed_by_risk"] = True

    meta2 = dict(res.metadata or {})
    meta2["sidewalk_nav_v1"] = wb2
    return replace(res, metadata=meta2)

def _maybe_attach_retail_find_item_v1_whitebox(
    res: VoiceFinalTextDispatchResult,
    *,
    event: VoiceInputEvent,
    runtime_context: Optional[VoiceRuntimeContext] = None,
) -> VoiceFinalTextDispatchResult:
    """
    retail_find_item_v1 深接入（阶段 1）：只做 whitebox-only 的真实主线挂载。

    约束：
    - 仅当 LUNA_ENABLE_RETAIL_FIND_ITEM_V1=1 且 LUNA_RETAIL_FIND_ITEM_WHITEBOX_ONLY=1 时生效
    - 不进入真实输出候选：强制不外显（final_spoken_output 置空）
    - 安全链优先：若 risk_level 为 high/critical 或 risk_interrupt_preempt=true，则压制标记必须成立
    - 不改变 dispatch_type / notes / 任何输出文本；只并入 metadata["retail_find_item_v1"]
    """
    try:
        from capabilities.cross_domain.retail_find_item_v1 import (  # noqa: E402
            FindItemIntentInput,
            OcrSummaryInput,
            RetailEnvironmentInput,
            RiskSummaryInput,
            evaluate_retail_find_item_v1,
            retail_find_item_enabled,
            retail_find_item_whitebox_only,
        )
    except Exception:
        return res

    if not retail_find_item_enabled():
        return res
    if not retail_find_item_whitebox_only():
        # 深联调阶段 1：写死只允许 whitebox-only
        return res

    md = runtime_context.metadata if (runtime_context is not None and isinstance(getattr(runtime_context, "metadata", None), dict)) else {}

    # 1) retail 环境摘要（context）
    env_src: Dict[str, Any] = {}
    re = md.get("retail_env_summary_v1")
    if isinstance(re, dict):
        env_src = re

    scene_type_candidate = str(env_src.get("scene_type_candidate") or env_src.get("scene_type") or "unknown")
    retail_conf = float(env_src.get("retail_context_confidence") or 0.0)
    shelf_visible = bool(env_src.get("shelf_visible") or False)
    gating_passed_ctx = env_src.get("gating_passed")
    gating_passed = gating_passed_ctx if isinstance(gating_passed_ctx, bool) else None

    env = RetailEnvironmentInput(
        scene_type=scene_type_candidate,
        retail_context_confidence=retail_conf,
        shelf_visible=shelf_visible,
        gating_passed=gating_passed,
    )

    # 2) 找货意图摘要（context）
    intent_src: Dict[str, Any] = {}
    fi = md.get("find_item_intent_summary_v1")
    if isinstance(fi, dict):
        intent_src = fi

    intent = FindItemIntentInput(
        active=bool(intent_src.get("active") or False),
        query=str(intent_src.get("query") or ""),
        user_requested_reading=bool(intent_src.get("user_requested_reading") or False),
        need_text_to_progress=bool(intent_src.get("need_text_to_progress") or False),
        ocr_budget_ok=bool(intent_src.get("ocr_budget_ok") if intent_src.get("ocr_budget_ok") is not None else True),
    )

    # 3) 风险摘要（context 优先；缺失则回退到 event.metadata 占位；不做多来源融合）
    risk_src: Dict[str, Any] = {}
    rs = md.get("risk_summary_v1")
    if isinstance(rs, dict):
        risk_src = rs
    fallback_evm = event.metadata or {}
    risk_level = str(risk_src.get("risk_level") or fallback_evm.get("risk_level") or "low")
    risk_type = str(risk_src.get("risk_type") or fallback_evm.get("risk_type") or "")
    risk_interrupt_preempt = bool(risk_src.get("risk_interrupt_preempt") or False)
    lv = (risk_level or "").strip().lower()
    suppressed = bool(risk_interrupt_preempt or (lv in ("high", "critical")))

    # 4) OCR 摘要（深接入阶段不做真实执行；若上层注入摘要则透传，否则为空占位）
    ocr_src = md.get("ocr_summary_v1")
    ocr_summary = OcrSummaryInput()
    if isinstance(ocr_src, dict):
        ocr_summary = OcrSummaryInput(
            text_digest=str(ocr_src.get("text_digest") or ""),
            confidence=float(ocr_src.get("confidence") or 0.0),
            roi_hint=str(ocr_src.get("roi_hint") or ""),
        )

    r = evaluate_retail_find_item_v1(
        environment=env,
        intent=intent,
        ocr_summary=ocr_summary,
        risk=RiskSummaryInput(
            risk_level=risk_level,
            risk_type=risk_type,
            risk_interrupt_preempt=bool(suppressed),
        ),
        timestamp_ms=int(float(event.timestamp) * 1000.0) if getattr(event, "timestamp", None) is not None else None,
    )

    wb = r.metadata.get("retail_find_item_v1") if isinstance(r.metadata, dict) else None
    if not isinstance(wb, dict) or not wb:
        return res

    # 写死 whitebox-only 深接入：不外显
    wb2 = dict(wb)
    wb2["final_spoken_output"] = ""
    wb2["whitebox_only"] = True
    if suppressed:
        wb2["output_suppressed_by_risk"] = True

    meta2 = dict(res.metadata or {})
    meta2["retail_find_item_v1"] = wb2
    return replace(res, metadata=meta2)


def dispatch_voice_final_text(
    event: VoiceInputEvent,
    *,
    pending_confirmation_context: bool = False,
    pending_confirmation_id: Optional[str] = None,
    registry: Optional[VoiceShortcutRegistry] = None,
    runtime_context: Optional[VoiceRuntimeContext] = None,
    session_state_anchor: Any = None,
) -> VoiceFinalTextDispatchResult:
    """
    对 process_final_text 产出的 VoiceInputEvent 做分流。

    - short_controlled_input：voice_input_to_bridge_decision（占位 Core，不执行）
    - long_task_planning_input：run_long_input_task_planning_v1，不接执行 / V2 / Final
    - rejected_input：结构化 reject，不进入上述两链
    """
    reg = registry or VoiceShortcutRegistry()
    rid = event.request_id or event.event_id
    sid = event.session_id

    if runtime_context is not None:
        runtime_context = _maybe_stabilize_runtime_context_sidewalk_env_v1(event, runtime_context)
        runtime_context = _maybe_stabilize_runtime_context_retail_env_v1(event, runtime_context)
        runtime_context = _maybe_attach_unified_env_shadow_v1(event, runtime_context)
        _maybe_emit_unified_env_shadow_snapshot_v1(event=event, runtime_context=runtime_context)
        runtime_context = _maybe_attach_unified_env_fill_shadow_v1(event=event, runtime_context=runtime_context)
        # P1-3 minimal wiring: summary -> one consumable slice -> mid-platform observe.
        runtime_context = maybe_attach_vision_consumable_slices_v0_from_risk_summary_v1(runtime_context=runtime_context)
        # P2-3 minimal loop wiring: slice -> needs_rerecognition_candidate -> mid-platform observe.
        runtime_context = maybe_attach_vision_interpretation_candidates_v0_from_slices(runtime_context=runtime_context)

    lm = classify_voice_input_length_mode(
        event,
        pending_confirmation_context=pending_confirmation_context,
        registry=reg,
    )

    meta_obs = {
        "length_mode_reason_code": lm.reason_code,
        "length_mode_notes": lm.notes,
    }

    if lm.mode == "rejected_input":
        if event.router_decision == "reject":
            rej = VoiceInputRejectionResult(
                request_id=rid,
                reason=str((event.metadata or {}).get("reject_reason") or "rejected"),
                router_stage="voice_input",
                raw_text=event.raw_text,
                normalized_text=event.normalized_text,
                is_task_mode=event.is_task_mode,
                source_type=event.source_type,
                reason_code=str((event.metadata or {}).get("reason_code") or ""),
            )
            notes = f"router_reject:{rej.reason_code}; {lm.notes}"
        else:
            rej = VoiceInputRejectionResult(
                request_id=rid,
                reason="final_text_dispatch_reject",
                router_stage="voice_final_text_dispatcher",
                raw_text=event.raw_text,
                normalized_text=event.normalized_text,
                is_task_mode=event.is_task_mode,
                source_type=event.source_type,
                reason_code=lm.reason_code,
            )
            notes = f"dispatcher_reject:{lm.reason_code}; {lm.notes}"

        out = VoiceFinalTextDispatchResult(
            request_id=rid,
            session_id=sid,
            dispatch_type="rejected_input",
            rejected_input=True,
            voice_input_event=event,
            rejection_result=rej,
            dispatch_reason_code=lm.reason_code,
            notes=notes,
            metadata=meta_obs,
        )
        out = _attach_need_navigation_routing_v0(out, event=event, bridge_decision=None, runtime_context=runtime_context)
        out = _maybe_consume_mid_platform_dispatch_consumption_stub_v0(out)
        out = _maybe_attach_mid_platform_formal_decision_stub_v0(out)
        out = _maybe_attach_formal_decision_allow_progress_path_v0(out)
        out = _maybe_attach_mid_platform_formal_decision_gate_inputs_v0(out, runtime_context=runtime_context)
        out = _maybe_attach_formal_decision_handoff_gates_v0(out)
        out = _maybe_attach_formal_decision_information_gates_v0(out, task_action="")
        out = _maybe_attach_navigation_real_execution_readiness_gate_inputs_v0(out, runtime_context=runtime_context)
        out = _maybe_attach_navigation_real_execution_readiness_gate_stub_v0(out)
        out = _maybe_attach_navigation_executor_takeover_stub_v0(out)
        out = _maybe_attach_navigation_real_executor_input_object_v0(out)
        out = _maybe_attach_navigation_real_executor_status_object_v0(out)
        out = _maybe_attach_navigation_execution_monitoring_status_v0(out)
        out = _maybe_attach_navigation_executor_takeover_wiring_v0(out)
        out = _maybe_attach_navigation_rollback_and_interruption_governance_entry_v0(out)
        out = _maybe_attach_navigation_rollback_and_interruption_governance_decision_v0(out)
        out = _maybe_attach_navigation_governance_action_boundary_v0(out)
        out = _maybe_attach_navigation_governance_action_approval_boundary_v0(out)
        out = _maybe_attach_navigation_governance_action_approval_status_object_v0(out)
        out = _maybe_attach_navigation_governance_action_executor_input_object_v0(out)
        out = _maybe_attach_navigation_governance_action_status_object_v0(out)
        out = _maybe_attach_navigation_governance_action_executor_readiness_gate_v0(out)
        out = _maybe_attach_navigation_governance_action_executor_wiring_v0(out)
        out = _maybe_attach_navigation_governance_action_release_control_input_object_v0(out)
        out = _maybe_attach_navigation_governance_action_release_control_status_object_v0(out)
        out = _maybe_attach_navigation_governance_action_release_control_readiness_gate_v0(out)
        out = _maybe_attach_navigation_governance_action_release_control_wiring_v0(out)
        out = _maybe_attach_navigation_governance_action_release_control_execution_state_object_v0(out)
        out = _maybe_attach_navigation_governance_action_release_control_result_object_v0(out)
        out = _maybe_attach_navigation_governance_action_release_control_minimal_executor_identity_v0(out)
        out = _maybe_attach_navigation_governance_action_release_control_executor_input_bridge_v0(out)
        out = _maybe_attach_navigation_governance_action_release_control_guarded_live_stub_v0(out)
        out = _maybe_attach_navigation_governance_action_release_control_live_release_gate_v0(out)
        out = _maybe_attach_navigation_governance_action_release_control_side_effect_release_gate_v0(out)
        out = _maybe_attach_navigation_governance_action_release_control_first_live_enablement_dry_run_v0(out)
        out = _maybe_attach_navigation_governance_action_release_control_first_live_enablement_approval_gate_v0(out)
        out = _maybe_attach_navigation_governance_action_release_control_first_live_launch_dry_run_v0(out)
        out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_wiring_v0(
            out
        )
        out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_non_effect_execution_v0(
            out
        )
        out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0(
            out
        )
        out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0(
            out
        )
        out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_dry_run_execution_v0(
            out
        )
        out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_v0(
            out
        )
        out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0(
            out
        )
        out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0(
            out
        )
        out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_dry_run_v0(
            out
        )
        out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0(
            out
        )
        out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0(
            out
        )
        out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_gate_v0(
            out
        )
        out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_commit_dry_run_v0(
            out
        )
        out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_gate_v0(
            out
        )
        out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_activation_dry_run_v0(
            out
        )
        out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_wiring_v0(
            out
        )
        out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_dry_run_execution_v0(
            out
        )
        out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_shadow_v0(
            out
        )
        out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_live_implementation_controlled_trial_shadow_v0(
            out
        )
        out = _maybe_consume_vision_slices_mid_platform_stub_v0(out, runtime_context=runtime_context)
        out2 = _run_cross_domain_orchestrator_v1(out, event=event, runtime_context=runtime_context)
        _maybe_submit_real_output_v1(
            out2, event=event, runtime_context=runtime_context, session_state_anchor=session_state_anchor
        )
        return out2

    if lm.mode == "short_controlled_input":
        bd = voice_input_to_bridge_decision(
            event,
            registry=reg,
            pending_confirmation_id=pending_confirmation_id,
        )
        nav_handoff = None
        try:
            nav_handoff = attempt_navigation_start_handoff_v0(bd)
        except Exception:
            nav_handoff = None
        dest_eval = None
        try:
            _applicable, dest_eval = evaluate_destination_sufficiency_v0(getattr(bd, "proposal", None))
        except Exception:
            dest_eval = None
        out = VoiceFinalTextDispatchResult(
            request_id=rid,
            session_id=sid,
            dispatch_type="short_controlled_input",
            short_controlled_input=True,
            voice_input_event=event,
            bridge_decision=bd,
            dispatch_reason_code=lm.reason_code,
            notes=lm.notes,
            metadata={
                **meta_obs,
                "bridge_reason": bd.reason,
                **({"navigation_handoff_v0": nav_handoff} if isinstance(nav_handoff, dict) else {}),
                **({"destination_sufficiency_eval_v0": dest_eval} if isinstance(dest_eval, dict) else {}),
            },
        )
        out = _attach_need_navigation_routing_v0(out, event=event, bridge_decision=bd, runtime_context=runtime_context)
        out = _maybe_consume_mid_platform_dispatch_consumption_stub_v0(out)
        out = _maybe_attach_mid_platform_formal_decision_stub_v0(out)
        out = _maybe_attach_formal_decision_allow_progress_path_v0(out)
        out = _maybe_attach_mid_platform_formal_decision_gate_inputs_v0(out, runtime_context=runtime_context)
        out = _maybe_attach_formal_decision_handoff_gates_v0(out)
        out = _maybe_attach_formal_decision_information_gates_v0(
            out, task_action=str(getattr(getattr(bd, "proposal", None), "task_action", "") or "")
        )
        out = _maybe_attach_navigation_real_execution_readiness_gate_inputs_v0(out, runtime_context=runtime_context)
        out = _maybe_attach_navigation_real_execution_readiness_gate_stub_v0(out)
        out = _maybe_attach_navigation_executor_takeover_stub_v0(out)
        out = _maybe_attach_navigation_real_executor_input_object_v0(out)
        out = _maybe_attach_navigation_real_executor_status_object_v0(out)
        out = _maybe_attach_navigation_execution_monitoring_status_v0(out)
        out = _maybe_attach_navigation_executor_takeover_wiring_v0(out)
        out = _maybe_attach_navigation_rollback_and_interruption_governance_entry_v0(out)
        out = _maybe_attach_navigation_rollback_and_interruption_governance_decision_v0(out)
        out = _maybe_attach_navigation_governance_action_boundary_v0(out)
        out = _maybe_attach_navigation_governance_action_approval_boundary_v0(out)
        out = _maybe_attach_navigation_governance_action_approval_status_object_v0(out)
        out = _maybe_attach_navigation_governance_action_executor_input_object_v0(out)
        out = _maybe_attach_navigation_governance_action_status_object_v0(out)
        out = _maybe_attach_navigation_governance_action_executor_readiness_gate_v0(out)
        out = _maybe_attach_navigation_governance_action_executor_wiring_v0(out)
        out = _maybe_attach_navigation_governance_action_release_control_input_object_v0(out)
        out = _maybe_attach_navigation_governance_action_release_control_status_object_v0(out)
        out = _maybe_attach_navigation_governance_action_release_control_readiness_gate_v0(out)
        out = _maybe_attach_navigation_governance_action_release_control_wiring_v0(out)
        out = _maybe_attach_navigation_governance_action_release_control_execution_state_object_v0(out)
        out = _maybe_attach_navigation_governance_action_release_control_result_object_v0(out)
        out = _maybe_attach_navigation_governance_action_release_control_minimal_executor_identity_v0(out)
        out = _maybe_attach_navigation_governance_action_release_control_executor_input_bridge_v0(out)
        out = _maybe_attach_navigation_governance_action_release_control_guarded_live_stub_v0(out)
        out = _maybe_attach_navigation_governance_action_release_control_live_release_gate_v0(out)
        out = _maybe_attach_navigation_governance_action_release_control_side_effect_release_gate_v0(out)
        out = _maybe_attach_navigation_governance_action_release_control_first_live_enablement_dry_run_v0(out)
        out = _maybe_attach_navigation_governance_action_release_control_first_live_enablement_approval_gate_v0(out)
        out = _maybe_attach_navigation_governance_action_release_control_first_live_launch_dry_run_v0(out)
        out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_wiring_v0(
            out
        )
        out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_non_effect_execution_v0(
            out
        )
        out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0(
            out
        )
        out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0(
            out
        )
        out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_dry_run_execution_v0(
            out
        )
        out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_v0(
            out
        )
        out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0(
            out
        )
        out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0(
            out
        )
        out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_dry_run_v0(
            out
        )
        out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0(
            out
        )
        out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0(
            out
        )
        out = _maybe_consume_vision_slices_mid_platform_stub_v0(out, runtime_context=runtime_context)
        cand = None
        try:
            cand = capture_destination_candidate_v0(event=event, navigation_context_result=out)
        except Exception:
            cand = None
        if isinstance(cand, dict):
            md2 = dict(out.metadata or {})
            md2["destination_candidate_v0"] = cand
            out = replace(out, metadata=md2)
        cchk = None
        try:
            _app_c, cchk = evaluate_destination_confirmation_fact_check_v0(res=out, event=event)
        except Exception:
            cchk = None
        if isinstance(cchk, dict):
            mdx = dict(out.metadata or {})
            mdx["destination_confirmation_fact_v0"] = cchk
            out = replace(out, metadata=mdx)
        bchk = None
        try:
            _app, bchk = evaluate_destination_bound_check_v0(res=out, event=event)
        except Exception:
            bchk = None
        if isinstance(bchk, dict):
            md3 = dict(out.metadata or {})
            md3["destination_bound_check_v0"] = bchk
            out = replace(out, metadata=md3)
        uev = None
        try:
            _app_u, uev = evaluate_destination_bound_upgrade_eval_v0(res=out, event=event)
        except Exception:
            uev = None
        if isinstance(uev, dict):
            md4 = dict(out.metadata or {})
            md4["destination_bound_upgrade_eval_v0"] = uev
            out = replace(out, metadata=md4)
        mev = None
        try:
            _app_m, mev = evaluate_destination_bound_materialization_eval_v0(res=out, event=event)
        except Exception:
            mev = None
        if isinstance(mev, dict):
            md5 = dict(out.metadata or {})
            md5["destination_bound_materialization_eval_v0"] = mev
            out = replace(out, metadata=md5)
        bnd = None
        try:
            _written, bnd = materialize_destination_bound_v0_if_allowed(res=out)
        except Exception:
            bnd = None
        if isinstance(bnd, dict):
            md6 = dict(out.metadata or {})
            md6["destination_bound_v0"] = bnd
            out = replace(out, metadata=md6)
        hcb = None
        try:
            hcb = consume_destination_bound_v0_in_handoff_v0(
                bd, destination_bound_v0=(out.metadata or {}).get("destination_bound_v0")  # type: ignore[union-attr]
            )
        except Exception:
            hcb = None
        if isinstance(hcb, dict):
            md7 = dict(out.metadata or {})
            md7["navigation_handoff_consume_bound_v0"] = hcb
            out = replace(out, metadata=md7)
        p4_stub = None
        try:
            _app_p4, p4_stub = evaluate_navigation_handoff_post_bound_execution_stub_v0(
                destination_bound_v0=(out.metadata or {}).get("destination_bound_v0"),  # type: ignore[union-attr]
                navigation_handoff_consume_bound_v0=(out.metadata or {}).get("navigation_handoff_consume_bound_v0"),  # type: ignore[union-attr]
            )
        except Exception:
            p4_stub = None
        if isinstance(p4_stub, dict):
            mdp4 = dict(out.metadata or {})
            mdp4["navigation_handoff_post_bound_execution_stub_v0"] = p4_stub
            out = replace(out, metadata=mdp4)
        out2 = _run_cross_domain_orchestrator_v1(out, event=event, runtime_context=runtime_context)
        out2 = _maybe_submit_response_template_v0(
            out2,
            template_id="navigation_missing_destination_confirm_v0",
            event=event,
        )
        _maybe_submit_real_output_v1(
            out2, event=event, runtime_context=runtime_context, session_state_anchor=session_state_anchor
        )
        return out2

    # long_task_planning_input
    text_for_plan = (event.wake_word_stripped or event.normalized_text or "").strip()
    parse_cfg_base = get_default_voice_long_input_parse_config()
    timeout_override_ms = int(os.getenv("LUNA_QWEN_MODEL_TIMEOUT_MS", str(parse_cfg_base.model_timeout_ms)) or parse_cfg_base.model_timeout_ms)
    parse_cfg = parse_cfg_base
    long_provider = None

    routing_obs: Dict[str, Any] = {
        "prefilter_routing_enabled": False,
        "prefilter_routing_suggestion": "",
        "prefilter_simple_or_complex": "",
        "prefilter_cleaned_text_len": None,
        "selected_provider_model_id": "",
        "backup_provider_used": False,
        "provider_switch_reason": "",
        "route_match_expected": None,
        "prefilter_notes": "",
        # M3.5.6b：最小观测补证（默认关闭；仅在专项开关下填充）
        "raw_model_payload_present": None,
        "raw_json_present": None,
        "raw_json_top_level_keys": None,
        "model_chain_detection_reason": "",
        "model_chain_detection_failed_reason": "",
    }
    audit_debug_on = _env_truthy("LUNA_VOICE_ENABLE_MODEL_CHAIN_AUDIT_DEBUG")

    if _env_truthy("LUNA_VOICE_ENABLE_PREFILTER_ROUTING"):
        from capabilities.voice.bridge.voice_long_input_prefilter_v0 import prefilter_long_voice_text_v0
        from capabilities.voice.providers.qwen_long_voice_primary_backup_provider import (
            BACKUP_MODEL_ID,
            PRIMARY_MODEL_ID,
            create_qwen_long_voice_single_model_provider_from_env,
        )

        pf = prefilter_long_voice_text_v0(text_for_plan, session_hint=event.context_resume_hint or "")
        text_for_plan = pf.cleaned_text
        routing_obs["prefilter_routing_enabled"] = True
        routing_obs["prefilter_routing_suggestion"] = pf.routing_suggestion
        routing_obs["prefilter_simple_or_complex"] = pf.simple_or_complex
        routing_obs["prefilter_cleaned_text_len"] = len(pf.cleaned_text or "")
        routing_obs["prefilter_notes"] = pf.notes

        if pf.routing_suggestion == "route_to_rule_or_reject":
            parse_cfg = replace(
                parse_cfg_base,
                parse_mode="rule_only",
                enable_model_adapter=False,
            )
            long_provider = None
            routing_obs["selected_provider_model_id"] = "rule_chain_only"
        else:
            model_id = PRIMARY_MODEL_ID if pf.routing_suggestion == "route_to_plus" else BACKUP_MODEL_ID
            long_provider = create_qwen_long_voice_single_model_provider_from_env(
                model_id=model_id,
                timeout_ms=timeout_override_ms,
            )
            if long_provider is not None:
                parse_cfg = replace(
                    parse_cfg_base,
                    parse_mode="model_preferred_with_rule_fallback",
                    enable_model_adapter=True,
                    model_timeout_ms=timeout_override_ms,
                )
                routing_obs["selected_provider_model_id"] = model_id
            else:
                parse_cfg = replace(
                    parse_cfg_base,
                    parse_mode="rule_only",
                    enable_model_adapter=False,
                )
                routing_obs["selected_provider_model_id"] = "rule_chain_only_unconfigured_qwen_external"
    else:
        routing_obs["prefilter_routing_suggestion"] = "disabled"
        routing_obs["prefilter_notes"] = "prefilter routing off; env default provider selection"
        if _env_truthy("LUNA_QWEN_USE_PRIMARY_BACKUP"):
            from capabilities.voice.providers.qwen_long_voice_primary_backup_provider import (
                create_qwen_long_voice_task_parse_provider_bundle_from_env,
            )

            long_provider = create_qwen_long_voice_task_parse_provider_bundle_from_env(
                timeout_ms=timeout_override_ms,
            )
            if long_provider is not None:
                parse_cfg = replace(
                    parse_cfg_base,
                    parse_mode="model_preferred_with_rule_fallback",
                    enable_model_adapter=True,
                    model_timeout_ms=timeout_override_ms,
                )
                routing_obs["selected_provider_model_id"] = "qwen_primary_backup_bundle"
            else:
                routing_obs["selected_provider_model_id"] = "bundle_unavailable_fallback_rule"
        else:
            routing_obs["selected_provider_model_id"] = "legacy_default_no_bundle"

    long_res = run_long_input_task_planning_v1(
        text_for_plan,
        request_id=rid,
        session_hint=event.context_resume_hint or "",
        parse_config=parse_cfg,
        model_provider=long_provider,
    )

    # provider 观测：主备 bundle 会在调用后写入诊断字段；单模型 provider 默认保持 False/空串。
    if long_provider is not None:
        sel = getattr(long_provider, "selected_provider_model_id", "") or ""
        if sel:
            routing_obs["selected_provider_model_id"] = sel
        routing_obs["backup_provider_used"] = bool(getattr(long_provider, "backup_provider_used", False))
        routing_obs["provider_switch_reason"] = str(getattr(long_provider, "provider_switch_reason", "") or "")
        if audit_debug_on:
            routing_obs["raw_model_payload_present"] = getattr(long_provider, "audit_raw_model_payload_present", None)
            routing_obs["raw_json_present"] = getattr(long_provider, "audit_raw_json_present", None)
            routing_obs["raw_json_top_level_keys"] = getattr(long_provider, "audit_raw_json_top_level_keys", None)
            routing_obs["model_chain_detection_reason"] = str(
                getattr(long_provider, "audit_model_chain_detection_reason", "") or ""
            )
            routing_obs["model_chain_detection_failed_reason"] = str(
                getattr(long_provider, "audit_model_chain_detection_failed_reason", "") or ""
            )

    if audit_debug_on:
        # 与“used_model_chain 判定”一致的可观察证据：notes 是否以 model_chain 前缀开头（不改判定逻辑，只写观测）
        ln = str(getattr(long_res, "notes", "") or "")
        if ln.startswith("model_chain"):
            routing_obs["model_chain_detection_reason"] = (
                routing_obs["model_chain_detection_reason"] or "long_res.notes_prefix=model_chain"
            )
        else:
            routing_obs["model_chain_detection_failed_reason"] = (
                routing_obs["model_chain_detection_failed_reason"] or f"long_res.notes_prefix_not_model_chain:{ln[:48]}"
            )
    out = VoiceFinalTextDispatchResult(
        request_id=rid,
        session_id=sid,
        dispatch_type="long_task_planning_input",
        long_task_planning_input=True,
        voice_input_event=event,
        long_input_parse_result=long_res,
        dispatch_reason_code=lm.reason_code,
        notes=f"{lm.notes}; long_notes={long_res.notes}",
        metadata={**meta_obs, **routing_obs, "long_input_notes": long_res.notes},
    )
    out = _attach_need_navigation_routing_v0(out, event=event, bridge_decision=None, runtime_context=runtime_context)
    out = _maybe_consume_mid_platform_dispatch_consumption_stub_v0(out)
    out = _maybe_attach_mid_platform_formal_decision_stub_v0(out)
    out = _maybe_attach_formal_decision_allow_progress_path_v0(out)
    out = _maybe_attach_mid_platform_formal_decision_gate_inputs_v0(out, runtime_context=runtime_context)
    out = _maybe_attach_formal_decision_handoff_gates_v0(out)
    out = _maybe_attach_formal_decision_information_gates_v0(out, task_action="")
    out = _maybe_attach_navigation_real_execution_readiness_gate_inputs_v0(out, runtime_context=runtime_context)
    out = _maybe_attach_navigation_real_execution_readiness_gate_stub_v0(out)
    out = _maybe_attach_navigation_executor_takeover_stub_v0(out)
    out = _maybe_attach_navigation_real_executor_input_object_v0(out)
    out = _maybe_attach_navigation_real_executor_status_object_v0(out)
    out = _maybe_attach_navigation_execution_monitoring_status_v0(out)
    out = _maybe_attach_navigation_executor_takeover_wiring_v0(out)
    out = _maybe_attach_navigation_rollback_and_interruption_governance_entry_v0(out)
    out = _maybe_attach_navigation_rollback_and_interruption_governance_decision_v0(out)
    out = _maybe_attach_navigation_governance_action_boundary_v0(out)
    out = _maybe_attach_navigation_governance_action_approval_boundary_v0(out)
    out = _maybe_attach_navigation_governance_action_approval_status_object_v0(out)
    out = _maybe_attach_navigation_governance_action_executor_input_object_v0(out)
    out = _maybe_attach_navigation_governance_action_status_object_v0(out)
    out = _maybe_attach_navigation_governance_action_executor_readiness_gate_v0(out)
    out = _maybe_attach_navigation_governance_action_executor_wiring_v0(out)
    out = _maybe_attach_navigation_governance_action_release_control_input_object_v0(out)
    out = _maybe_attach_navigation_governance_action_release_control_status_object_v0(out)
    out = _maybe_attach_navigation_governance_action_release_control_readiness_gate_v0(out)
    out = _maybe_attach_navigation_governance_action_release_control_wiring_v0(out)
    out = _maybe_attach_navigation_governance_action_release_control_execution_state_object_v0(out)
    out = _maybe_attach_navigation_governance_action_release_control_result_object_v0(out)
    out = _maybe_attach_navigation_governance_action_release_control_minimal_executor_identity_v0(out)
    out = _maybe_attach_navigation_governance_action_release_control_executor_input_bridge_v0(out)
    out = _maybe_attach_navigation_governance_action_release_control_guarded_live_stub_v0(out)
    out = _maybe_attach_navigation_governance_action_release_control_live_release_gate_v0(out)
    out = _maybe_attach_navigation_governance_action_release_control_side_effect_release_gate_v0(out)
    out = _maybe_attach_navigation_governance_action_release_control_first_live_enablement_dry_run_v0(out)
    out = _maybe_attach_navigation_governance_action_release_control_first_live_enablement_approval_gate_v0(out)
    out = _maybe_attach_navigation_governance_action_release_control_first_live_launch_dry_run_v0(out)
    out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_wiring_v0(out)
    out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_non_effect_execution_v0(
        out
    )
    out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_dry_effect_simulation_v0(
        out
    )
    out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_wiring_v0(
        out
    )
    out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_dry_run_execution_v0(
        out
    )
    out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_wiring_v0(
        out
    )
    out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_implementation_dry_run_execution_v0(
        out
    )
    out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_admission_gate_v0(
        out
    )
    out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_dry_run_v0(
        out
    )
    out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_guarded_launch_gate_v0(
        out
    )
    out = _maybe_attach_navigation_governance_action_release_control_first_live_guarded_implementation_minimal_real_effect_pre_commit_dry_run_v0(
        out
    )
    out = _maybe_consume_vision_slices_mid_platform_stub_v0(out, runtime_context=runtime_context)
    out2 = _run_cross_domain_orchestrator_v1(out, event=event, runtime_context=runtime_context)
    _maybe_submit_real_output_v1(
        out2, event=event, runtime_context=runtime_context, session_state_anchor=session_state_anchor
    )
    return out2
