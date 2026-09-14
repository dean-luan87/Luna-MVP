#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务优化引擎
支持通过人工修正、AI学习，不断修正任务的最优解
"""

__version__ = "1.0.0"
__version_info__ = (1, 0, 0)

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class OptimizationSource(Enum):
    """优化来源枚举"""
    USER_FEEDBACK = "user_feedback"  # 用户反馈
    MANUAL = "manual"  # 人工修正
    AI_LEARNING = "ai_learning"  # AI学习
    SYSTEM_AUTO = "system_auto"  # 系统自动优化
    BACKEND_SYNC = "backend_sync"  # 后台同步


@dataclass
class TaskExecution:
    """任务执行记录"""
    task_id: str
    task_type: str  # 任务类型：navigation, search, etc.
    timestamp: str
    
    # 任务定义
    task_description: str
    original_plan: Dict[str, Any]  # 原始任务计划
    execution_steps: List[Dict[str, Any]]  # 执行步骤
    
    # 执行结果
    success: bool
    execution_time: float  # 执行时间（秒）
    user_satisfaction: Optional[float] = None  # 用户满意度（0-1）
    
    # 优化信息
    optimized_plan: Optional[Dict[str, Any]] = None  # 优化后的计划
    optimization_source: Optional[str] = None
    optimization_notes: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return asdict(self)


@dataclass
class TaskOptimization:
    """任务优化记录"""
    optimization_id: str
    task_id: str
    original_plan: Dict[str, Any]
    optimized_plan: Dict[str, Any]
    optimization_source: str
    timestamp: str
    
    # 优化理由
    reason: str
    improvements: List[str]  # 改进点
    expected_benefits: Dict[str, Any]  # 预期收益
    
    # 验证结果
    applied: bool = False
    verified: bool = False
    verification_result: Optional[Dict[str, Any]] = None
    
    # 统计信息
    application_count: int = 0  # 应用次数
    success_rate: float = 0.0  # 成功率


class TaskOptimizer:
    """任务优化引擎"""
    
    def __init__(self, data_dir: str = "data/tasks"):
        """初始化任务优化引擎
        
        Args:
            data_dir: 任务数据存储目录
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.tasks_file = self.data_dir / "task_executions.json"
        self.optimizations_file = self.data_dir / "task_optimizations.json"
        
        # 任务执行记录库
        self.task_executions: Dict[str, TaskExecution] = {}
        
        # 任务优化记录库
        self.task_optimizations: Dict[str, TaskOptimization] = {}
        
        # 优化模式库（任务类型 -> 最优方案）
        self.optimization_patterns: Dict[str, Dict[str, Any]] = {}
        
        # 加载已有记录
        self._load_data()
    
    def _load_data(self):
        """加载数据"""
        if self.tasks_file.exists():
            try:
                with open(self.tasks_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for task_id, task_data in data.items():
                        self.task_executions[task_id] = TaskExecution(**task_data)
                logger.info(f"✅ 已加载 {len(self.task_executions)} 条任务执行记录")
            except Exception as e:
                logger.error(f"❌ 加载任务记录失败: {e}")
        
        if self.optimizations_file.exists():
            try:
                with open(self.optimizations_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for opt_id, opt_data in data.items():
                        self.task_optimizations[opt_id] = TaskOptimization(**opt_data)
                    
                    # 从优化记录中提取优化模式
                    self._extract_optimization_patterns()
                logger.info(f"✅ 已加载 {len(self.task_optimizations)} 条优化记录")
            except Exception as e:
                logger.error(f"❌ 加载优化记录失败: {e}")
    
    def _save_data(self):
        """保存数据"""
        try:
            # 保存任务执行记录
            data = {tid: task.to_dict() for tid, task in self.task_executions.items()}
            with open(self.tasks_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            # 保存优化记录
            data = {oid: asdict(opt) for oid, opt in self.task_optimizations.items()}
            with open(self.optimizations_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"❌ 保存数据失败: {e}")
    
    def _extract_optimization_patterns(self):
        """从优化记录中提取优化模式"""
        for opt in self.task_optimizations.values():
            if opt.verified and opt.success_rate > 0.7:  # 只保留验证成功且成功率高的优化
                task_type = self.task_executions.get(opt.task_id, TaskExecution(
                    task_id=opt.task_id, task_type="unknown", timestamp="", 
                    task_description="", original_plan={}, execution_steps=[], success=False, execution_time=0.0
                )).task_type
                
                if task_type not in self.optimization_patterns:
                    self.optimization_patterns[task_type] = {}
                
                # 记录最优方案
                self.optimization_patterns[task_type][opt.optimization_id] = {
                    "plan": opt.optimized_plan,
                    "success_rate": opt.success_rate,
                    "improvements": opt.improvements
                }
    
    def record_task_execution(
        self,
        task_id: str,
        task_type: str,
        task_description: str,
        original_plan: Dict[str, Any],
        execution_steps: List[Dict[str, Any]],
        success: bool,
        execution_time: float,
        user_satisfaction: Optional[float] = None
    ) -> TaskExecution:
        """记录任务执行"""
        task_execution = TaskExecution(
            task_id=task_id,
            task_type=task_type,
            timestamp=datetime.now().isoformat(),
            task_description=task_description,
            original_plan=original_plan,
            execution_steps=execution_steps,
            success=success,
            execution_time=execution_time,
            user_satisfaction=user_satisfaction
        )
        
        self.task_executions[task_id] = task_execution
        self._save_data()
        
        logger.info(f"📝 记录任务执行: {task_id} ({task_type}) - {'成功' if success else '失败'}")
        
        return task_execution
    
    def optimize_task(
        self,
        task_id: str,
        optimized_plan: Dict[str, Any],
        optimization_source: OptimizationSource,
        reason: str,
        improvements: List[str],
        expected_benefits: Optional[Dict[str, Any]] = None,
        optimization_notes: Optional[str] = None
    ) -> str:
        """优化任务"""
        if task_id not in self.task_executions:
            logger.warning(f"⚠️ 任务记录不存在: {task_id}")
            return None
        
        task_execution = self.task_executions[task_id]
        
        optimization_id = f"opt_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(self.task_optimizations)}"
        
        optimization = TaskOptimization(
            optimization_id=optimization_id,
            task_id=task_id,
            original_plan=task_execution.original_plan,
            optimized_plan=optimized_plan,
            optimization_source=optimization_source.value,
            timestamp=datetime.now().isoformat(),
            reason=reason,
            improvements=improvements,
            expected_benefits=expected_benefits or {}
        )
        
        self.task_optimizations[optimization_id] = optimization
        
        # 更新任务执行记录
        task_execution.optimized_plan = optimized_plan
        task_execution.optimization_source = optimization_source.value
        task_execution.optimization_notes = optimization_notes
        
        self._save_data()
        
        logger.info(f"✅ 任务已优化: {task_id} (优化ID: {optimization_id}, 来源: {optimization_source.value})")
        
        return optimization_id
    
    def apply_optimization(
        self,
        task_type: str,
        task_description: str,
        task_plan: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], Optional[str]]:
        """应用优化方案到新任务"""
        # 查找相似任务的优化方案
        best_optimization = self._find_best_optimization(task_type, task_description, task_plan)
        
        if best_optimization:
            optimized_plan = self._adapt_optimization(best_optimization, task_plan)
            return optimized_plan, best_optimization.optimization_id
        
        return task_plan, None
    
    def _find_best_optimization(
        self,
        task_type: str,
        task_description: str,
        task_plan: Dict[str, Any]
    ) -> Optional[TaskOptimization]:
        """查找最佳优化方案"""
        # 查找相同类型的已验证优化
        candidates = [
            opt for opt in self.task_optimizations.values()
            if (opt.verified and 
                self.task_executions.get(opt.task_id, TaskExecution(
                    task_id="", task_type="unknown", timestamp="", task_description="",
                    original_plan={}, execution_steps=[], success=False, execution_time=0.0
                )).task_type == task_type and
                opt.success_rate > 0.7)
        ]
        
        if not candidates:
            return None
        
        # 选择成功率最高的优化方案
        best = max(candidates, key=lambda x: x.success_rate)
        return best
    
    def _adapt_optimization(
        self,
        optimization: TaskOptimization,
        current_plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """适配优化方案到当前任务"""
        # 简单的适配逻辑：合并优化方案的改进点
        optimized_plan = current_plan.copy()
        optimized_plan.update(optimization.optimized_plan)
        
        # 标记使用了优化
        optimized_plan['_optimization_applied'] = True
        optimized_plan['_optimization_id'] = optimization.optimization_id
        
        return optimized_plan
    
    def verify_optimization(
        self,
        optimization_id: str,
        task_id: Optional[str] = None,
        success: bool = True,
        performance_metrics: Optional[Dict[str, Any]] = None
    ) -> bool:
        """验证优化效果"""
        if optimization_id not in self.task_optimizations:
            logger.warning(f"⚠️ 优化记录不存在: {optimization_id}")
            return False
        
        optimization = self.task_optimizations[optimization_id]
        
        # 更新应用统计
        optimization.application_count += 1
        
        if success:
            # 更新成功率
            current_success = optimization.application_count * optimization.success_rate
            optimization.success_rate = (current_success + 1) / optimization.application_count
        else:
            # 降低成功率
            current_success = optimization.application_count * optimization.success_rate
            optimization.success_rate = current_success / optimization.application_count
        
        # 如果是首次验证，标记为已验证
        if not optimization.verified:
            optimization.verified = True
            optimization.verification_result = {
                "success": success,
                "metrics": performance_metrics or {},
                "timestamp": datetime.now().isoformat()
            }
        
        # 如果成功率足够高，更新优化模式
        if optimization.success_rate > 0.7:
            self._extract_optimization_patterns()
        
        self._save_data()
        
        logger.info(f"✅ 优化验证完成: {optimization_id} (成功率: {optimization.success_rate:.2%})")
        
        return True
    
    def learn_from_user_feedback(
        self,
        task_id: str,
        feedback: str,
        satisfaction: float,
        suggested_improvements: Optional[List[str]] = None
    ) -> Optional[str]:
        """从用户反馈中学习优化"""
        if task_id not in self.task_executions:
            return None
        
        task_execution = self.task_executions[task_id]
        
        # 如果满意度较低，尝试生成优化方案
        if satisfaction < 0.6 or suggested_improvements:
            # 分析反馈，提取改进点
            improvements = suggested_improvements or self._extract_improvements_from_feedback(feedback)
            
            if improvements:
                # 生成优化方案（这里需要调用AI分析）
                optimized_plan = self._generate_optimized_plan(task_execution, improvements)
                
                if optimized_plan:
                    return self.optimize_task(
                        task_id=task_id,
                        optimized_plan=optimized_plan,
                        optimization_source=OptimizationSource.USER_FEEDBACK,
                        reason=f"用户反馈：{feedback}",
                        improvements=improvements,
                        expected_benefits={"satisfaction": satisfaction + 0.2}
                    )
        
        # 更新任务执行的用户满意度
        task_execution.user_satisfaction = satisfaction
        
        self._save_data()
        
        return None
    
    def _extract_improvements_from_feedback(self, feedback: str) -> List[str]:
        """从反馈中提取改进点"""
        # 简单的关键词匹配（实际应该使用NLP）
        improvements = []
        
        if "慢" in feedback or "速度" in feedback:
            improvements.append("优化执行速度")
        if "路线" in feedback or "路径" in feedback:
            improvements.append("优化路径规划")
        if "不准确" in feedback or "错误" in feedback:
            improvements.append("提高准确性")
        if "复杂" in feedback or "繁琐" in feedback:
            improvements.append("简化操作流程")
        
        return improvements
    
    def _generate_optimized_plan(
        self,
        task_execution: TaskExecution,
        improvements: List[str]
    ) -> Optional[Dict[str, Any]]:
        """生成优化方案"""
        # 基于改进点调整计划
        optimized_plan = task_execution.original_plan.copy()
        
        for improvement in improvements:
            if "速度" in improvement:
                optimized_plan['priority'] = 'high'
                optimized_plan['timeout'] = optimized_plan.get('timeout', 30) * 0.8
            elif "路径" in improvement:
                optimized_plan['path_optimization'] = True
                optimized_plan['consider_alternatives'] = True
            elif "准确性" in improvement:
                optimized_plan['verify_accuracy'] = True
                optimized_plan['confidence_threshold'] = 0.9
            elif "简化" in improvement:
                optimized_plan['minimize_steps'] = True
        
        return optimized_plan
    
    def export_for_backend(self, optimization_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """导出优化数据供后台使用"""
        if optimization_ids is None:
            optimization_ids = list(self.task_optimizations.keys())
        
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "total_optimizations": len(optimization_ids),
            "optimizations": []
        }
        
        for opt_id in optimization_ids:
            if opt_id in self.task_optimizations:
                opt = self.task_optimizations[opt_id]
                task_exec = self.task_executions.get(opt.task_id)
                
                export_item = asdict(opt)
                if task_exec:
                    export_item['task_info'] = {
                        "task_type": task_exec.task_type,
                        "task_description": task_exec.task_description
                    }
                
                export_data["optimizations"].append(export_item)
        
        return export_data
    
    def get_optimization_statistics(self) -> Dict[str, Any]:
        """获取优化统计信息"""
        stats = {
            "total_tasks": len(self.task_executions),
            "total_optimizations": len(self.task_optimizations),
            "verified_optimizations": sum(1 for opt in self.task_optimizations.values() if opt.verified),
            "by_source": {},
            "average_success_rate": 0.0,
            "by_task_type": {}
        }
        
        total_success_rate = 0.0
        verified_count = 0
        
        for opt in self.task_optimizations.values():
            # 按来源统计
            source = opt.optimization_source
            stats["by_source"][source] = stats["by_source"].get(source, 0) + 1
            
            # 按任务类型统计
            task_type = self.task_executions.get(opt.task_id, TaskExecution(
                task_id="", task_type="unknown", timestamp="", task_description="",
                original_plan={}, execution_steps=[], success=False, execution_time=0.0
            )).task_type
            if task_type not in stats["by_task_type"]:
                stats["by_task_type"][task_type] = {"count": 0, "avg_success_rate": 0.0}
            stats["by_task_type"][task_type]["count"] += 1
            
            # 计算平均成功率
            if opt.verified:
                total_success_rate += opt.success_rate
                verified_count += 1
                stats["by_task_type"][task_type]["avg_success_rate"] = (
                    stats["by_task_type"][task_type]["avg_success_rate"] * 
                    (stats["by_task_type"][task_type]["count"] - 1) + opt.success_rate
                ) / stats["by_task_type"][task_type]["count"]
        
        if verified_count > 0:
            stats["average_success_rate"] = total_success_rate / verified_count
        
        return stats
