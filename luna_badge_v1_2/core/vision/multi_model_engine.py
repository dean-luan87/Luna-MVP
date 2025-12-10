"""
MultiModelEngine: 多模型并行推理引擎（Pro-2 核心）

职责：
- 按 task_type 查找模型组
- 并行执行
- 收集结果
- 按简单规则进行竞争/决策

注意：Patch-1 版本只做最小可用实现：
- detect: 选择 best_model = argmax(weight * best_conf)
- ocr/classify: 选第一个成功返回的模型
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

from .vision_task_orchestrator import VisionTask, VisionResult
from .arbiter import Arbiter
from .score_logger import ScoreLogger, ModelStats


@dataclass
class ModelSpec:
    """
    单个模型的描述信息。

    - name: 模型标识（如 'yolo11s'）
    - runner: 可调用对象：runner(task: VisionTask) -> Any
    - weight: 该模型在竞争决策中的权重
    - enabled: 是否启用
    """
    name: str
    runner: Callable[[VisionTask], Any]
    weight: float = 1.0
    enabled: bool = True
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModelHealth:
    """
    引擎内部使用的模型健康信息快照。
    """
    task_type: str
    model: str
    enabled: bool
    weight: float
    success_rate: float
    avg_conf: float
    total_calls: int


class MultiModelEngine:
    """
    多模型并行推理引擎（带仲裁 & 日志 & 健康统计）。

    Patch-3: 增加动态权重调整和自动禁用功能
    """

    def __init__(self, max_workers: int = 4):
        """
        Args:
            max_workers: 线程池最大工作线程数
        """
        self._registry: Dict[str, List[ModelSpec]] = {}
        self._executor = ThreadPoolExecutor(max_workers=max_workers)

        # Patch-2: 新增仲裁器与日志器
        self._arbiter = Arbiter()
        self._score_logger = ScoreLogger()

        # Patch-3: 动态权重调整参数（可后续从配置注入）
        self.min_calls_for_adjust = 20  # 至少多少次调用后才考虑调权重
        self.auto_disable_threshold = 0.1  # 成功率低于此值可自动禁用
        self.weight_adjust_alpha = 0.3  # 权重调整强度

    # ---------- 注册 / 查询 ----------

    def register_model(self, task_type: str, spec: ModelSpec) -> None:
        """
        注册模型到某个 task_type 下。

        Args:
            task_type: 任务类型（如 'detect', 'ocr', 'classify'）
            spec: 模型规格
        """
        self._registry.setdefault(task_type, []).append(spec)

    def list_models(self, task_type: str) -> List[ModelSpec]:
        """
        返回该 task_type 下所有启用的模型。

        Args:
            task_type: 任务类型

        Returns:
            List[ModelSpec]: 启用的模型列表
        """
        return [m for m in self._registry.get(task_type, []) if m.enabled]

    def has_models(self, task_type: str) -> bool:
        """
        检查是否有启用的模型。

        Args:
            task_type: 任务类型

        Returns:
            bool: 是否有启用的模型
        """
        return any(m.enabled for m in self._registry.get(task_type, []))

    # ---------- 对外主入口 ----------

    def run(self, task: VisionTask) -> VisionResult:
        """
        核心入口：并行跑所有可用模型，然后做决策。

        Args:
            task: VisionTask 实例

        Returns:
            VisionResult: 执行结果
        """
        task_type = task.task_type
        models = self.list_models(task_type)

        if not models:
            return VisionResult(
                ok=False,
                error=f"No models registered for task_type={task_type}",
                task_id=task.task_id,
            )

        # 提交任务
        futures: Dict[Any, ModelSpec] = {}
        for spec in models:
            future = self._executor.submit(self._safe_run, spec, task)
            futures[future] = spec

        # 收集结果
        results: List[Tuple[ModelSpec, bool, Any, Optional[str]]] = []
        for fut in as_completed(futures):
            spec = futures[fut]
            try:
                value = fut.result()
                results.append((spec, True, value, None))
            except Exception as e:  # 理论上不会到这儿（_safe_run 已 catch），双保险
                results.append((spec, False, None, str(e)))

        # Patch-2: 调用仲裁器进行决策
        if task_type == "detect":
            decision = self._arbiter.decide_detect(task, results)
        else:
            decision = self._arbiter.decide_first_success(task, results)

        # Patch-2: 记录日志
        self._score_logger.log(
            task_id=task.task_id or "",
            task_type=task.task_type,
            decision=decision,
        )

        # Patch-3: 动态调整（惰性策略：按调用次数阈值触发）
        self._maybe_adjust_weights(task_type)

        # Patch-2: 输出 VisionResult（包含详细的评分信息）
        if decision.winner is None:
            return VisionResult(
                ok=False,
                error=decision.error or "arbiter_no_winner",
                task_id=task.task_id,
            )

        # 构建结果，包含所有模型的评分信息
        result_dict: Dict[str, Any] = {
            "model": decision.winner,
            "output": decision.winner_output,
        }

        # 为了向后兼容，对于 detect 任务，同时保留 detections 字段
        if task_type == "detect" and isinstance(decision.winner_output, list):
            result_dict["detections"] = decision.winner_output

        # 添加评分信息（转换为字典以便序列化）
        if decision.scores:
            result_dict["scores"] = [
                {
                    "model": s.model,
                    "ok": s.ok,
                    "max_conf": s.max_conf,
                    "weight": s.weight,
                    "final_score": s.final_score,
                    "error": s.error,
                    "reason": s.reason,
                }
                for s in decision.scores
            ]

        return VisionResult(
            ok=True,
            result=result_dict,
            task_id=task.task_id,
        )

    # ---------- 内部工具 ----------

    @staticmethod
    def _safe_run(spec: ModelSpec, task: VisionTask) -> Any:
        """
        对 runner 的包装，避免单个模型抛异常导致全局崩溃。

        Args:
            spec: ModelSpec 实例
            task: VisionTask 实例

        Returns:
            Any: runner 的执行结果
        """
        try:
            return spec.runner(task)
        except Exception as e:
            # 这里捕获异常，返回错误信息，由调用方处理
            raise RuntimeError(f"{spec.name} failed: {str(e)}") from e

    def _decide_detect(
        self,
        task: VisionTask,
        results: List[Tuple[ModelSpec, bool, Any, Optional[str]]],
    ) -> VisionResult:
        """
        detect 任务的竞争决策：

        - 假设每个模型返回 detections: List[{"label": str, "score": float, ...}]
        - 我们用 max_score * weight 作为模型的评估值，选最大的那个

        Args:
            task: VisionTask 实例
            results: 模型执行结果列表

        Returns:
            VisionResult: 决策结果
        """
        best_spec: Optional[ModelSpec] = None
        best_value: Any = None
        best_score: float = -1.0
        errors: List[str] = []

        for spec, ok, value, err in results:
            if not ok:
                errors.append(f"{spec.name}: {err}")
                continue

            detections = value or []
            if not isinstance(detections, list) or not detections:
                errors.append(f"{spec.name}: empty or invalid detections")
                continue

            # 计算最大置信度
            max_conf = 0.0
            for det in detections:
                if isinstance(det, dict):
                    score = float(det.get("score", 0.0))
                    max_conf = max(max_conf, score)
                elif hasattr(det, "score"):
                    max_conf = max(max_conf, float(det.score))

            final_score = max_conf * float(spec.weight or 1.0)

            if final_score > best_score:
                best_score = final_score
                best_spec = spec
                best_value = detections

        if best_spec is None:
            # 所有模型都失败/无结果
            return VisionResult(
                ok=False,
                error="; ".join(errors) if errors else "All models failed",
                task_id=task.task_id,
            )

        return VisionResult(
            ok=True,
            result={
                "model": best_spec.name,
                "detections": best_value,
                "score": best_score,
                "errors": errors or [],
            },
            task_id=task.task_id,
        )

    # 旧版决策方法（保留作为备用，实际已由 Arbiter 接管）
    def _decide_first_success(
        self,
        task: VisionTask,
        results: List[Tuple[ModelSpec, bool, Any, Optional[str]]],
    ) -> VisionResult:
        """
        对于 ocr/classify 等任务的最小实现：

        - 返回第一个成功的模型输出
        - 后续可以扩展为 ensemble。

        Args:
            task: VisionTask 实例
            results: 模型执行结果列表

        Returns:
            VisionResult: 决策结果
        """
        errors: List[str] = []
        for spec, ok, value, err in results:
            if ok:
                return VisionResult(
                    ok=True,
                    result={"model": spec.name, "output": value},
                    task_id=task.task_id,
                )
            if err:
                errors.append(f"{spec.name}: {err}")

        return VisionResult(
            ok=False,
            error="; ".join(errors) if errors else "All models failed",
            task_id=task.task_id,
        )

    # ---------- 动态权重 & 自动禁用 ----------

    def _maybe_adjust_weights(self, task_type: str) -> None:
        """
        惰性执行：每次调用后检查是否满足条件，再决定是否刷新权重。

        条件：
        - 至少有一个模型 total_calls >= min_calls_for_adjust

        Args:
            task_type: 任务类型
        """
        models = self._registry.get(task_type, [])
        if not models:
            return

        # 检查是否有足够调用数据
        if not any(
            self._score_logger.get_stats(task_type, m.name).total_calls >= self.min_calls_for_adjust
            for m in models
        ):
            return

        self.recalculate_weights(task_type)

    def recalculate_weights(self, task_type: str) -> None:
        """
        使用 ScoreLogger 中的统计信息调整该 task_type 下的模型权重，并根据成功率决定是否禁用某些模型。

        策略（初版简单版）：
        - success_rate < auto_disable_threshold 且 total_calls >= min_calls_for_adjust → enabled=False
        - 对剩余 enabled 模型：
            weight_new = clamp(0.1, 3.0, weight_old * (1 + alpha * (success_rate - 0.5)))
        然后做归一化，让 sum(weights) ≈ 1.0（非必须，但有利于直觉）。

        Args:
            task_type: 任务类型
        """
        models = self._registry.get(task_type, [])
        if not models:
            return

        # 先调整 enabled / disabled
        for spec in models:
            stats: ModelStats = self._score_logger.get_stats(task_type, spec.name)

            if stats.total_calls < self.min_calls_for_adjust:
                continue

            if stats.success_rate < self.auto_disable_threshold:
                spec.enabled = False  # 自动禁用
            else:
                spec.enabled = True

        # 再调整权重
        total_weight = 0.0
        for spec in models:
            if not spec.enabled:
                continue

            stats = self._score_logger.get_stats(task_type, spec.name)

            if stats.total_calls < self.min_calls_for_adjust:
                # 数据太少，不调整
                total_weight += spec.weight
                continue

            delta = stats.success_rate - 0.5  # 以 0.5 为基准
            new_weight = spec.weight * (1.0 + self.weight_adjust_alpha * delta)

            # clamp
            new_weight = max(0.1, min(3.0, new_weight))
            spec.weight = new_weight
            total_weight += new_weight

        # 归一化（避免权重无限膨胀）
        if total_weight > 0:
            for spec in models:
                if spec.enabled:
                    spec.weight = spec.weight / total_weight

    # ---------- 对外健康快照接口（给上层用） ----------

    def get_model_health_snapshot(self) -> Dict[str, Any]:
        """
        返回结构：
        {
          "detect": {
             "yolo11n": {...},
             "yolo11s": {...}
          },
          "ocr": {
             "paddle": {...}
          }
        }

        Returns:
            Dict[str, Any]: 模型健康快照
        """
        raw_stats = self._score_logger.get_stats_snapshot()

        # 补充 enabled / weight 信息
        enriched: Dict[str, Any] = {}

        for task_type, models in raw_stats.items():
            task_block: Dict[str, Any] = {}
            reg_models = {m.name: m for m in self._registry.get(task_type, [])}

            for model_name, stat in models.items():
                spec = reg_models.get(model_name)
                if spec:
                    stat = dict(stat)
                    stat["enabled"] = spec.enabled
                    stat["weight"] = spec.weight
                task_block[model_name] = stat

            enriched[task_type] = task_block

        return enriched

