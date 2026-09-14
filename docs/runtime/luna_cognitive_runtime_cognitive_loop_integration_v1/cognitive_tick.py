"""One bounded Cognitive Tick layered above the Runtime Tick."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional

from docs.runtime.luna_cognitive_runtime_foundation_impl_v1.runtime_loop import CognitiveRuntime
from docs.runtime.luna_cognitive_runtime_foundation_impl_v1.runtime_types import RuntimeEvent

from .attention_runtime_interface import AttentionRuntimeInterface
from .brain_invocation_boundary import BrainInvocationBoundary
from .cognitive_trace_extension import CognitiveTraceExtension
from .context_assembler import ContextAssembler, ContextPackage
from .decision_candidate_flow import DecisionCandidate
from .state_update_boundary import StateUpdateBoundary
from .workspace_runtime_adapter import WorkspaceRuntimeAdapter


@dataclass(frozen=True)
class CognitiveTickResult:
    context: ContextPackage
    attention_candidate: Mapping[str, Any]
    decision_candidate: DecisionCandidate
    state_change: Any


class CognitiveTick:
    """Coordinates the context → workspace → attention → Brain boundary flow."""

    def __init__(self) -> None:
        self.context_assembler = ContextAssembler()
        self.workspace = WorkspaceRuntimeAdapter()
        self.attention = AttentionRuntimeInterface()
        self.brain = BrainInvocationBoundary()
        self.state_boundary = StateUpdateBoundary()

    def run(self, runtime: CognitiveRuntime, event: Optional[RuntimeEvent] = None) -> CognitiveTickResult:
        event_context = self._event_context(event)
        context = self.context_assembler.assemble(runtime.state.read(), event_context)
        workspace = self.workspace.activate(context)
        attention_candidate = self.attention.select(context, workspace)
        decision_candidate = self.brain.invoke(context, attention_candidate)
        state_change = self.state_boundary.apply_candidate(runtime.state, decision_candidate, context.context_id)
        trace = CognitiveTraceExtension(runtime.trace)
        trace.runtime_tick(runtime.tick_count)
        trace.context_build(context.context_id)
        trace.attention_selection(context.context_id, attention_candidate)
        trace.brain_invocation(context.context_id)
        trace.decision_candidate(decision_candidate.decision_candidate_id)
        runtime.trace.record_state_change(None, [state_change])
        return CognitiveTickResult(context, attention_candidate, decision_candidate, state_change)

    @staticmethod
    def _event_context(event: Optional[RuntimeEvent]) -> dict[str, Any]:
        if event is None:
            return {}
        return {"event_id": event.event_id, "event_type": event.event_type, **dict(event.payload)}
