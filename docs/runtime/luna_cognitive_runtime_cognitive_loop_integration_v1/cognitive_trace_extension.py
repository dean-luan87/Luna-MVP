"""Trace extension for cognitive-loop stages."""
from __future__ import annotations

from typing import Any, Mapping

from docs.runtime.luna_cognitive_runtime_foundation_impl_v1.trace_manager import TraceManager


class CognitiveTraceExtension:
    def __init__(self, trace: TraceManager) -> None:
        self.trace = trace

    def runtime_tick(self, tick: int) -> None:
        self.trace.record_tick({"stage": "runtime_tick", "tick": tick})

    def context_build(self, context_id: str) -> None:
        self.trace.record_tick({"stage": "context_build", "context_id": context_id})

    def attention_selection(self, context_id: str, selection: Mapping[str, Any]) -> None:
        self.trace.record_tick({"stage": "attention_selection", "context_id": context_id, "selection": dict(selection)})

    def brain_invocation(self, context_id: str) -> None:
        self.trace.record_tick({"stage": "brain_invocation", "context_id": context_id})

    def decision_candidate(self, candidate_id: str) -> None:
        self.trace.record_tick({"stage": "decision_candidate", "candidate_id": candidate_id})
