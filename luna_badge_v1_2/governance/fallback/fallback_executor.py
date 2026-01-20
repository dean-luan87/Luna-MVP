"""
Fallback Executor

兜底执行器。

v1.5 设计原则：
- PlanB 不追求聪明，只追求不死
- PlanB 不做自动学习，只执行写好的策略
- FallbackExecutor 不判断该不该 fallback，只执行策略
- 返回"行动描述"而不是直接执行
"""

import os
import yaml
import time
from typing import Dict, Any, Optional, List
from pathlib import Path


class FallbackExecutor:
    """
    兜底执行器
    
    职责：
    - 根据 task_domain + reason + 当前上下文
    - 查找策略配置
    - 检查 attempts / cooldown
    - 匹配 trigger
    - 返回 action 指令（而不是直接执行）
    
    关键设计：
    - FallbackExecutor 不判断该不该 fallback，只做"既然要 fallback，我按策略执行下一步"
    - 返回"行动描述"，TaskChain 根据描述执行
    """
    
    def __init__(self, policy_path: Optional[str] = None, metrics_collector=None, trace_id=None):
        """
        初始化兜底执行器
        
        Args:
            policy_path: 策略配置文件路径（默认使用 fallback_policy.yaml）
            metrics_collector: 指标收集器（可选）
            trace_id: 跟踪 ID（可选）
        """
        if policy_path is None:
            # 默认使用同目录下的 fallback_policy.yaml
            current_dir = Path(__file__).parent
            policy_path = os.path.join(current_dir, "fallback_policy.yaml")
        
        self.policy_path = policy_path
        self.policy = self._load_policy(policy_path)
        
        # 运行时状态（用于追踪 attempts 和 cooldown）
        # key: task_domain, value: {"attempts": int, "last_attempt_ts": float}
        self._runtime_state: Dict[str, Dict[str, Any]] = {}
        
        # 指标收集
        self.metrics_collector = metrics_collector
        self.trace_id = trace_id
    
    def _load_policy(self, policy_path: str) -> Dict[str, Any]:
        """
        加载策略配置
        
        Args:
            policy_path: 策略文件路径
            
        Returns:
            策略配置字典
        """
        try:
            with open(policy_path, 'r', encoding='utf-8') as f:
                policy = yaml.safe_load(f)
            return policy.get("task_domains", {})
        except Exception as e:
            # 如果加载失败，返回空策略（系统将使用默认行为）
            return {"default": {"max_attempts": 2, "cooldown_ms": 2000, "rules": []}}
    
    def _get_domain_config(self, task_domain: str) -> Dict[str, Any]:
        """
        获取任务域的配置
        
        Args:
            task_domain: 任务领域
            
        Returns:
            任务域配置（如果不存在则返回 default）
        """
        if task_domain in self.policy:
            return self.policy[task_domain]
        return self.policy.get("default", {
            "max_attempts": 2,
            "cooldown_ms": 2000,
            "rules": []
        })
    
    def _check_cooldown(self, task_domain: str, cooldown_ms: int) -> bool:
        """
        检查是否在冷却时间内
        
        Args:
            task_domain: 任务领域
            cooldown_ms: 冷却时间（毫秒）
            
        Returns:
            True 表示在冷却期内，False 表示可以执行
        """
        if task_domain not in self._runtime_state:
            return False
        
        state = self._runtime_state[task_domain]
        last_attempt_ts = state.get("last_attempt_ts", 0)
        
        if last_attempt_ts == 0:
            return False
        
        elapsed_ms = (time.time() - last_attempt_ts) * 1000
        return elapsed_ms < cooldown_ms
    
    def _check_max_attempts(self, task_domain: str, max_attempts: int) -> bool:
        """
        检查是否达到最大尝试次数
        
        Args:
            task_domain: 任务领域
            max_attempts: 最大尝试次数
            
        Returns:
            True 表示已达到最大次数，False 表示还可以尝试
        """
        if task_domain not in self._runtime_state:
            return False
        
        attempts = self._runtime_state[task_domain].get("attempts", 0)
        return attempts >= max_attempts
    
    def _update_runtime_state(self, task_domain: str):
        """
        更新运行时状态（增加 attempts，更新 last_attempt_ts）
        
        Args:
            task_domain: 任务领域
        """
        if task_domain not in self._runtime_state:
            self._runtime_state[task_domain] = {"attempts": 0, "last_attempt_ts": 0}
        
        self._runtime_state[task_domain]["attempts"] += 1
        self._runtime_state[task_domain]["last_attempt_ts"] = time.time()
    
    def _match_trigger(self, reason: str, trigger: str) -> bool:
        """
        匹配触发原因
        
        Args:
            reason: 实际触发原因（来自 MOC）
            trigger: 策略中的 trigger
            
        Returns:
            True 表示匹配
        """
        # v1.5: 简单字符串匹配（可扩展为正则或模糊匹配）
        # 支持精确匹配和部分匹配
        if reason == trigger:
            return True
        
        # 支持部分匹配（如 "low_confidence" 匹配 "Conflicts detected and no primary/secondary model match. Conflicts: 1"）
        if trigger in reason.lower() or reason.lower() in trigger.lower():
            return True
        
        return False
    
    def _find_matching_rule(
        self, 
        domain_config: Dict[str, Any], 
        reason: str
    ) -> Optional[Dict[str, Any]]:
        """
        查找匹配的策略规则
        
        Args:
            domain_config: 任务域配置
            reason: 触发原因
            
        Returns:
            匹配的规则（如果找到），否则返回 None
        """
        rules = domain_config.get("rules", [])
        
        # 优先匹配精确的 trigger
        for rule in rules:
            if self._match_trigger(reason, rule.get("trigger", "")):
                return rule
        
        return None
    
    def execute(
        self, 
        task_domain: str, 
        reason: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        根据 task_domain + reason + 当前上下文
        返回下一步行动描述
        
        Args:
            task_domain: 任务领域（如 "navigation", "safety", "inquiry"）
            reason: 触发 fallback 的原因（来自 MOC 的 decision.reason）
            context: 上下文信息（可选，包含 attempt、previous_actions 等）
            
        Returns:
            行动描述：
            {
                "action": "switch_model" | "degrade_capability" | "cross_domain" | "abort",
                "target": str | None,
                "reason": str,
                "attempt": int,
                "plan": str,  # B1/B2/B3/abort
                "description": str,
                "cooldown_remaining_ms": int  # 如果处于冷却期
            }
        """
        if context is None:
            context = {}
        
        # 1. 获取任务域配置
        domain_config = self._get_domain_config(task_domain)
        max_attempts = domain_config.get("max_attempts", 2)
        cooldown_ms = domain_config.get("cooldown_ms", 2000)
        
        # 2. 初始化运行时状态（如果不存在）
        if task_domain not in self._runtime_state:
            self._runtime_state[task_domain] = {"attempts": 0, "last_attempt_ts": 0}
        
        # 3. 获取当前尝试次数（更新前）
        current_attempt = self._runtime_state[task_domain].get("attempts", 0)
        
        # 4. 检查是否达到最大尝试次数
        if current_attempt >= max_attempts:
            # 触发 exhausted，强制中止（不更新状态）
            return {
                "action": "abort",
                "target": None,
                "reason": "exhausted",
                "attempt": max_attempts,
                "plan": "abort",
                "description": f"达到最大尝试次数 ({max_attempts})，中止任务",
                "cooldown_remaining_ms": 0
            }
        
        # 5. 检查冷却时间（冷却期内不增加 attempt）
        if self._check_cooldown(task_domain, cooldown_ms):
            state = self._runtime_state[task_domain]
            last_attempt_ts = state.get("last_attempt_ts", 0)
            elapsed_ms = (time.time() - last_attempt_ts) * 1000
            remaining_ms = int(cooldown_ms - elapsed_ms)
            
            return {
                "action": "wait",
                "target": None,
                "reason": reason,
                "attempt": current_attempt,  # 冷却期内不增加 attempt
                "plan": "cooldown",
                "description": f"冷却期内，需等待 {remaining_ms}ms",
                "cooldown_remaining_ms": remaining_ms
            }
        
        # 6. 更新运行时状态（增加 attempts）
        self._update_runtime_state(task_domain)
        current_attempt = self._runtime_state[task_domain]["attempts"]
        
        # 5. 查找匹配的策略规则
        rule = self._find_matching_rule(domain_config, reason)
        
        if rule is None:
            # 没有匹配的规则，使用默认中止
            return {
                "action": "abort",
                "target": None,
                "reason": reason,
                "attempt": current_attempt,
                "plan": "abort",
                "description": f"未找到匹配的策略规则，中止任务",
                "cooldown_remaining_ms": 0
            }
        
        # 6. 返回行动描述
        action_result = {
            "action": rule.get("action", "abort"),
            "target": rule.get("target"),
            "reason": reason,
            "attempt": current_attempt,
            "plan": rule.get("plan", "unknown"),
            "description": rule.get("description", ""),
            "cooldown_remaining_ms": 0
        }
        
        # 7. 记录 fallback 事件（打点）
        if self.metrics_collector and self.trace_id:
            self.metrics_collector.trace(
                trace_id=self.trace_id,
                task_domain=task_domain,
                node_id="fallback",
                event="fallback",
                payload={
                    "trigger": reason,
                    "action": action_result["action"],
                    "attempt": current_attempt,
                    "max_attempts": max_attempts,
                    "plan": action_result["plan"]
                }
            )
        
        return action_result
    
    def reset(self, task_domain: Optional[str] = None):
        """
        重置运行时状态（用于测试或任务重启）
        
        Args:
            task_domain: 任务领域（如果为 None，重置所有）
        """
        if task_domain is None:
            self._runtime_state.clear()
        elif task_domain in self._runtime_state:
            del self._runtime_state[task_domain]





