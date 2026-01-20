"""
AskResultBinder: 负责将 AskChainRuntime 收集到的 slot answers
根据 task_meta["ask_bindings"] 的映射规则
自动写入到 task_context 的目标位置。
"""

from typing import Dict, Any


class AskResultBinder:
    """
    负责将 AskChainRuntime 收集到的 slot answers
    根据 task_meta["ask_bindings"] 的映射规则
    自动写入到 task_context 的目标位置。
    """

    @staticmethod
    def bind(
        answers: Dict[str, Any],
        task_meta: Dict[str, Any],
        task_context: Dict[str, Any],
    ) -> None:
        """
        将 answers 根据 bindings 配置写入 task_context。

        Args:
            answers: AskIntegrationResult.answers 字典（slot → value）
            task_meta: 当前任务的 metadata，可能包含 ask_bindings
            task_context: TaskChainManager 内部维护的 context dict
        """

        # --- 1. 原始 answers 始终写入 ask_result，用于 trace/debug ---
        bucket = task_context.setdefault("ask_result", {})
        bucket.update(answers)

        # --- 2. 读取映射配置 ---
        bindings = task_meta.get("ask_bindings") or {}
        if not bindings:
            # 没有绑定配置，不做任何映射，保持 ask_result 原样
            return

        # --- 3. 目前版本仅支持绑定到 params ---
        params_bucket = task_context.setdefault("params", {})

        for slot_name, cfg in bindings.items():
            if slot_name not in answers:
                # slot 未回答，跳过
                continue

            value = answers[slot_name]
            target = cfg.get("target", "params")
            target_name = cfg.get("name", slot_name)

            if target == "params":
                params_bucket[target_name] = value
            else:
                # 未来扩展更多 target
                continue












