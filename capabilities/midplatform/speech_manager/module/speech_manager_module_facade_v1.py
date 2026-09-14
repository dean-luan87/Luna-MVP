from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.speech_manager.module.speech_manager_content_governance_v1 import (
    build_speech_manager_content_candidate_v1,
)
from capabilities.midplatform.speech_manager.module.speech_manager_diagnostics_v1 import (
    build_speech_manager_diagnostics_v1,
)
from capabilities.midplatform.speech_manager.module.speech_manager_interruption_controller_v1 import (
    build_speech_manager_interruption_plan_v1,
)
from capabilities.midplatform.speech_manager.module.speech_manager_module_input_adapter_v1 import (
    adapt_speech_manager_input_v1,
)
from capabilities.midplatform.speech_manager.module.speech_manager_module_output_builder_v1 import (
    build_speech_manager_module_status_v1,
    build_speech_manager_result_summary_v1,
)
from capabilities.midplatform.speech_manager.module.speech_manager_priority_resolver_v1 import (
    build_speech_manager_priority_candidate_v1,
)
from capabilities.midplatform.speech_manager.module.speech_manager_provider_candidate_adapter_v1 import (
    build_speech_manager_provider_candidates_v1,
)
from capabilities.midplatform.speech_manager.module.speech_manager_request_governance_v1 import (
    run_speech_manager_request_governance_v1,
)
from capabilities.midplatform.speech_manager.module.speech_manager_trace_replay_v1 import (
    build_speech_manager_trace_replay_v1,
)


def run_speech_manager_module_v1(payload: Mapping[str, Any]) -> Dict[str, Any]:
    input_candidate = adapt_speech_manager_input_v1(payload)
    governance = run_speech_manager_request_governance_v1(input_candidate)
    priority_candidate = build_speech_manager_priority_candidate_v1(input_candidate)
    interruption_plan = build_speech_manager_interruption_plan_v1(
        input_candidate, priority_candidate
    )
    content_candidate = build_speech_manager_content_candidate_v1(input_candidate)
    provider_candidates = build_speech_manager_provider_candidates_v1(
        input_candidate, content_candidate, interruption_plan
    )
    trace_replay = build_speech_manager_trace_replay_v1(
        input_candidate,
        governance,
        content_candidate,
        interruption_plan,
        provider_candidates,
    )
    diagnostics = build_speech_manager_diagnostics_v1(
        input_candidate,
        governance,
        content_candidate,
        interruption_plan,
        provider_candidates,
        trace_replay,
    )
    module_status = build_speech_manager_module_status_v1(
        governance, provider_candidates, trace_replay
    )
    result_summary = build_speech_manager_result_summary_v1(
        request_id=str(input_candidate.get("request_id") or "speech_mgr_req_unknown"),
        module_status=module_status,
        content_candidate=content_candidate,
        interruption_plan=interruption_plan,
        provider_candidates=provider_candidates,
        trace_replay=trace_replay,
    )

    return {
        "module_status": module_status,
        "input_candidate": input_candidate,
        "governance": governance,
        "priority_candidate": priority_candidate,
        "interruption_plan": interruption_plan,
        "content_candidate": content_candidate,
        "provider_candidates": provider_candidates,
        "trace_replay": trace_replay,
        "diagnostics": diagnostics,
        "result_summary": result_summary,
        "trace_ref": trace_replay["trace_ref"],
        "replay_key": trace_replay["replay_key"],
        "candidate_only": True,
        "real_asr_invoked": False,
        "real_tts_invoked": False,
        "real_speech_gate_invoked": False,
        "real_vop_invoked": False,
        "boundary_preserved": True,
    }
