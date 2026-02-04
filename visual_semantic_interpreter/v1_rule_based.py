from __future__ import annotations

from .interpreter import VisualSemanticInterpreter
from .types import VisualContext, InterpretationResult, SemanticInterpretation


class RuleBasedInterpreterV1(VisualSemanticInterpreter):
    def interpret(self, ctx: VisualContext) -> InterpretationResult:
        interpretations = []

        texts = [t.text.lower() for t in ctx.ocr_tokens]

        if any("exit" in t or "出口" in t for t in texts):
            interpretations.append(
                SemanticInterpretation(
                    meaning="可能是出口指示",
                    category="exit",
                    confidence=0.7,
                    evidence={
                        "ocr": "包含 exit / 出口 字样",
                        "roi": ctx.roi_kind,
                    },
                    ambiguity="可能是广告中的文字",
                )
            )

        if not interpretations:
            interpretations.append(
                SemanticInterpretation(
                    meaning="无法确定含义",
                    category="unknown",
                    confidence=0.2,
                    evidence={
                        "reason": "缺少稳定文字或结构线索",
                    },
                    ambiguity="需要更多视角或时间确认",
                )
            )

        return InterpretationResult(
            interpretations=interpretations,
            unresolved=len(interpretations) > 1,
        )
