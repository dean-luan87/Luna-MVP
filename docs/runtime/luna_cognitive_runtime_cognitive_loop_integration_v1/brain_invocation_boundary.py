"""Brain invocation boundary returning a decision candidate placeholder only."""
from __future__ import annotations

from typing import Any, Mapping

from .attention_runtime_interface import AttentionRuntimeInterface
from .context_assembler import ContextPackage
from .decision_candidate_flow import DecisionCandidate, DecisionCandidateFlow


class BrainInvocationBoundary:
    """No reasoning engine is called in this phase."""

    def invoke(self, context: ContextPackage, attention_candidate: Mapping[str, Any]) -> DecisionCandidate:
        candidate = DecisionCandidateFlow.unresolved(context.context_id, context.unknowns)
        if candidate.metadata.get("action_command") or candidate.metadata.get("reality_mutation"):
            raise ValueError("brain response crossed the candidate boundary")
        return candidate
