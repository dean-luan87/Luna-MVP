"""
Arbiter: 多模型仲裁器（Patch-2 核心）

对模型结果进行后处理、排序、决策，并给出可解释的输出。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from .multi_model_engine import ModelSpec

from .vision_task_orchestrator import VisionTask


@dataclass
class ModelScore:
    """
    某个模型在一次推理中的得分情况。
    """
    model: str
    ok: bool
    raw_output: Any
    max_conf: float
    weight: float
    final_score: float
    error: Optional[str] = None
    reason: Optional[str] = None


@dataclass
class ArbiterDecision:
    """
    仲裁后的统一决策结果。
    """
    winner: Optional[str]
    winner_output: Any
    scores: List[ModelScore]
    error: Optional[str] = None


class Arbiter:
    """
    多模型仲裁器（Patch-2 核心）：

    对模型结果进行后处理、排序、决策，并给出可解释的输出。
    """

    def decide_detect(
        self,
        task: VisionTask,
        results: List[Tuple["ModelSpec", bool, Any, Optional[str]]],
    ) -> ArbiterDecision:
        """
        对 detect 任务进行仲裁决策。

        Args:
            task: VisionTask 实例
            results: 模型执行结果列表

        Returns:
            ArbiterDecision: 仲裁决策结果
        """
        model_scores: List[ModelScore] = []
        best_score = -1.0
        winner_spec: Optional[ModelSpec] = None
        winner_output: Any = None

        for spec, ok, value, err in results:
            if not ok:
                model_scores.append(
                    ModelScore(
                        model=spec.name,
                        ok=False,
                        raw_output=None,
                        max_conf=0.0,
                        weight=spec.weight or 1.0,
                        final_score=0.0,
                        error=err,
                        reason="model_failed",
                    )
                )
                continue

            dets = value or []
            if not isinstance(dets, list) or not dets:
                model_scores.append(
                    ModelScore(
                        model=spec.name,
                        ok=False,
                        raw_output=dets,
                        max_conf=0.0,
                        weight=spec.weight or 1.0,
                        final_score=0.0,
                        error="empty_detections",
                        reason="no_valid_output",
                    )
                )
                continue

            # 计算最大置信度
            max_conf = 0.0
            for d in dets:
                if isinstance(d, dict):
                    score = float(d.get("score", 0.0))
                    max_conf = max(max_conf, score)
                elif hasattr(d, "score"):
                    max_conf = max(max_conf, float(d.score))

            final_score = max_conf * (spec.weight or 1.0)

            model_scores.append(
                ModelScore(
                    model=spec.name,
                    ok=True,
                    raw_output=dets,
                    max_conf=max_conf,
                    weight=spec.weight or 1.0,
                    final_score=final_score,
                    reason="score_computed",
                )
            )

            if final_score > best_score:
                best_score = final_score
                winner_spec = spec
                winner_output = dets

        if winner_spec is None:
            return ArbiterDecision(
                winner=None,
                winner_output=None,
                scores=model_scores,
                error="all_models_failed_or_no_valid_output",
            )

        # 标记 winner
        for s in model_scores:
            if s.model == winner_spec.name:
                s.reason = "winner"

        return ArbiterDecision(
            winner=winner_spec.name,
            winner_output=winner_output,
            scores=model_scores,
            error=None,
        )

    # 对其他任务类型（ocr/classify）可扩展多种策略
    def decide_first_success(
        self,
        task: VisionTask,
        results: List[Tuple["ModelSpec", bool, Any, Optional[str]]],
    ) -> ArbiterDecision:
        """
        对 ocr/classify 任务进行 first-success 仲裁决策。

        Args:
            task: VisionTask 实例
            results: 模型执行结果列表

        Returns:
            ArbiterDecision: 仲裁决策结果
        """
        model_scores: List[ModelScore] = []
        errors = []

        for spec, ok, value, err in results:
            if ok:
                model_scores.append(
                    ModelScore(
                        model=spec.name,
                        ok=True,
                        raw_output=value,
                        max_conf=1.0,
                        weight=spec.weight or 1.0,
                        final_score=1.0,
                        reason="first_success",
                    )
                )
                return ArbiterDecision(
                    winner=spec.name,
                    winner_output=value,
                    scores=model_scores,
                )

            errors.append(f"{spec.name}: {err}")
            model_scores.append(
                ModelScore(
                    model=spec.name,
                    ok=False,
                    raw_output=None,
                    max_conf=0.0,
                    weight=spec.weight or 1.0,
                    final_score=0.0,
                    error=err,
                    reason="model_failed",
                )
            )

        return ArbiterDecision(
            winner=None,
            winner_output=None,
            scores=model_scores,
            error="; ".join(errors),
        )

