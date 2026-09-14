from __future__ import annotations

from .types import VisualContext, InterpretationResult


class VisualSemanticInterpreter:
    def interpret(self, ctx: VisualContext) -> InterpretationResult:
        raise NotImplementedError
