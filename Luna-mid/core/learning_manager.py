#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学习系统统一管理器
整合所有学习引擎，提供统一的学习能力接口
"""

__version__ = "1.0.0"
__version_info__ = (1, 0, 0)

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from .error_learning import ErrorLearningEngine, ErrorType, CorrectionSource
from .task_optimizer import TaskOptimizer, OptimizationSource
from .user_habit_analyzer import UserHabitAnalyzer
from .visual_learning import VisualLearningEngine, RecognitionSource, ObjectCategory

logger = logging.getLogger(__name__)


class LearningSystemManager:
    """学习系统统一管理器"""
    
    def __init__(self, data_dir: Optional[Path] = None):
        """
        初始化学习系统管理器
        
        Args:
            data_dir: 数据存储根目录，默认为 ./data
        """
        if data_dir is None:
            data_dir = Path(__file__).parent.parent.parent / "data"
        self.data_dir = Path(data_dir)
        
        # 初始化各个学习引擎
        self.error_engine = ErrorLearningEngine(
            data_dir=self.data_dir / "error_learning"
        )
        self.task_optimizer = TaskOptimizer(
            data_dir=self.data_dir / "task_optimization"
        )
        self.habit_analyzer = UserHabitAnalyzer(
            data_dir=self.data_dir / "user_habits"
        )
        self.visual_engine = VisualLearningEngine(
            data_dir=self.data_dir / "visual_learning"
        )
        
        logger.info("学习系统管理器初始化完成")
    
    # ==================== 错误学习接口 ====================
    
    def record_error(
        self,
        error_type: str,
        context: Dict[str, Any],
        user_input: Optional[str] = None,
        system_response: Optional[str] = None,
        expected_response: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        记录错误
        
        Args:
            error_type: 错误类型
            context: 错误上下文
            user_input: 用户输入
            system_response: 系统响应
            expected_response: 期望响应
            **kwargs: 其他参数
            
        Returns:
            错误ID
        """
        return self.error_engine.record_error(
            error_type=ErrorType(error_type) if isinstance(error_type, str) else error_type,
            context=context,
            user_input=user_input,
            system_response=system_response,
            expected_response=expected_response,
            **kwargs
        )
    
    def record_correction(
        self,
        error_id: str,
        correction_source: str,
        correction: str,
        **kwargs
    ) -> bool:
        """
        记录纠正
        
        Args:
            error_id: 错误ID
            correction_source: 纠正来源
            correction: 纠正内容
            **kwargs: 其他参数
            
        Returns:
            是否成功
        """
        source = CorrectionSource(correction_source) if isinstance(correction_source, str) else correction_source
        return self.error_engine.correct_error(
            error_id=error_id,
            correction_source=source,
            correction=correction,
            **kwargs
        )
    
    def get_error_analysis(self, error_id: str) -> Optional[Dict[str, Any]]:
        """
        获取错误分析
        
        Args:
            error_id: 错误ID
            
        Returns:
            错误分析结果
        """
        analysis = self.error_engine.analyze_error(error_id)
        if analysis:
            return analysis.to_dict()
        return None
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """
        获取错误统计信息
        
        Returns:
            统计信息
        """
        return self.error_engine.get_statistics()
    
    # ==================== 任务优化接口 ====================
    
    def record_task_execution(
        self,
        task_type: str,
        task_description: str,
        original_plan: Dict[str, Any],
        execution_steps: List[Dict[str, Any]],
        success: bool,
        execution_time: float,
        user_satisfaction: Optional[float] = None,
        **kwargs
    ) -> str:
        """
        记录任务执行
        
        Args:
            task_type: 任务类型
            task_description: 任务描述
            original_plan: 原始计划
            execution_steps: 执行步骤
            success: 是否成功
            execution_time: 执行时间（秒）
            user_satisfaction: 用户满意度（0-1）
            **kwargs: 其他参数
            
        Returns:
            任务ID
        """
        import uuid
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
        execution = self.task_optimizer.record_task_execution(
            task_id=task_id,
            task_type=task_type,
            task_description=task_description,
            original_plan=original_plan,
            execution_steps=execution_steps,
            success=success,
            execution_time=execution_time,
            user_satisfaction=user_satisfaction
        )
        return task_id
    
    def optimize_task(
        self,
        task_id: str,
        optimized_plan: Dict[str, Any],
        optimization_source: str,
        optimization_notes: Optional[str] = None,
        **kwargs
    ) -> bool:
        """
        优化任务
        
        Args:
            task_id: 任务ID
            optimized_plan: 优化后的计划
            optimization_source: 优化来源
            optimization_notes: 优化说明
            **kwargs: 其他参数
            
        Returns:
            是否成功
        """
        source = OptimizationSource(optimization_source) if isinstance(optimization_source, str) else optimization_source
        return self.task_optimizer.optimize_task(
            task_id=task_id,
            optimized_plan=optimized_plan,
            optimization_source=source,
            optimization_notes=optimization_notes,
            **kwargs
        )
    
    def get_optimized_plan(
        self,
        task_type: str,
        task_description: str
    ) -> Optional[Dict[str, Any]]:
        """
        获取优化后的任务计划
        
        Args:
            task_type: 任务类型
            task_description: 任务描述
            
        Returns:
            优化后的计划，如果不存在返回None
        """
        return self.task_optimizer.get_optimized_plan(
            task_type=task_type,
            task_description=task_description
        )
    
    def get_task_statistics(self) -> Dict[str, Any]:
        """
        获取任务统计信息
        
        Returns:
            统计信息
        """
        return self.task_optimizer.get_statistics()
    
    # ==================== 用户习惯分析接口 ====================
    
    def record_walking_session(
        self,
        user_id: str,
        start_location: Dict[str, Any],
        end_location: Dict[str, Any],
        route: List[Dict[str, Any]],
        duration: float,
        distance: float,
        weather: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        记录行走会话
        
        Args:
            user_id: 用户ID
            start_location: 起始位置
            end_location: 结束位置
            route: 路径点列表
            duration: 持续时间（秒）
            distance: 距离（米）
            weather: 天气
            **kwargs: 其他参数
            
        Returns:
            会话ID
        """
        return self.habit_analyzer.record_walking_session(
            user_id=user_id,
            start_location=start_location,
            end_location=end_location,
            route=route,
            duration=duration,
            distance=distance,
            weather=weather,
            **kwargs
        )
    
    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        获取用户画像
        
        Args:
            user_id: 用户ID
            
        Returns:
            用户画像，如果不存在返回None
        """
        profile = self.habit_analyzer.get_user_profile(user_id)
        if profile:
            return profile.to_dict()
        return None
    
    def estimate_walking_time(
        self,
        user_id: str,
        distance: float,
        time_of_day: Optional[str] = None
    ) -> float:
        """
        估算行走时间
        
        Args:
            user_id: 用户ID
            distance: 距离（米）
            time_of_day: 时间段
            
        Returns:
            估算时间（秒）
        """
        return self.habit_analyzer.estimate_walking_time(
            user_id=user_id,
            distance=distance,
            time_of_day=time_of_day
        )
    
    def get_user_statistics(self, user_id: str) -> Dict[str, Any]:
        """
        获取用户统计信息
        
        Args:
            user_id: 用户ID
            
        Returns:
            统计信息
        """
        return self.habit_analyzer.get_statistics(user_id)
    
    # ==================== 视觉学习接口 ====================
    
    def record_visual_recognition(
        self,
        category: str,
        name: Optional[str],
        confidence: float,
        bbox: Dict[str, float],
        features: Dict[str, Any],
        source: str = "camera",
        location: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> str:
        """
        记录视觉识别结果
        
        Args:
            category: 物体类别
            name: 物体名称
            confidence: 置信度
            bbox: 边界框
            features: 特征描述
            source: 识别来源
            location: 位置信息
            **kwargs: 其他参数
            
        Returns:
            物体ID
        """
        return self.visual_engine.record_recognition(
            category=category,
            name=name,
            confidence=confidence,
            bbox=bbox,
            features=features,
            source=source,
            location=location,
            **kwargs
        )
    
    def get_visual_knowledge(
        self,
        object_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        获取视觉知识库
        
        Args:
            object_id: 物体ID，如果提供则返回单个知识，否则返回所有
            
        Returns:
            知识字典
        """
        knowledge = self.visual_engine.get_knowledge(object_id)
        return {
            obj_id: k.to_dict()
            for obj_id, k in knowledge.items()
        }
    
    def correct_visual_recognition(
        self,
        object_id: str,
        correct_category: Optional[str] = None,
        correct_name: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> bool:
        """
        纠正视觉识别结果
        
        Args:
            object_id: 物体ID
            correct_category: 正确的类别
            correct_name: 正确的名称
            user_id: 用户ID
            
        Returns:
            是否成功
        """
        return self.visual_engine.correct_recognition(
            object_id=object_id,
            correct_category=correct_category,
            correct_name=correct_name,
            user_id=user_id
        )
    
    def get_visual_statistics(self) -> Dict[str, Any]:
        """
        获取视觉学习统计信息
        
        Returns:
            统计信息
        """
        return self.visual_engine.get_statistics()
    
    # ==================== 统一接口 ====================
    
    def get_all_statistics(self) -> Dict[str, Any]:
        """
        获取所有学习系统的统计信息
        
        Returns:
            统计信息字典
        """
        return {
            "error_learning": self.get_error_statistics(),
            "task_optimization": self.get_task_statistics(),
            "visual_learning": self.get_visual_statistics(),
            "timestamp": datetime.now().isoformat()
        }
    
    def export_all_data(self, output_dir: Path) -> bool:
        """
        导出所有数据
        
        Args:
            output_dir: 输出目录
            
        Returns:
            是否成功
        """
        try:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # 导出错误学习数据
            error_file = output_dir / "error_learning.json"
            self.error_engine.export_data(error_file)
            
            # 导出任务优化数据
            task_file = output_dir / "task_optimization.json"
            self.task_optimizer.export_data(task_file)
            
            # 导出视觉学习数据
            visual_file = output_dir / "visual_learning.json"
            self.visual_engine.export_data(visual_file)
            
            # 导出汇总统计
            summary_file = output_dir / "summary.json"
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(self.get_all_statistics(), f, ensure_ascii=False, indent=2)
            
            logger.info(f"已导出所有数据到 {output_dir}")
            return True
        except Exception as e:
            logger.error(f"导出数据失败: {e}")
            return False
    
    def sync_from_backend(self, backend_data: Dict[str, Any]) -> bool:
        """
        从后台同步数据
        
        Args:
            backend_data: 后台数据字典，包含各个学习系统的数据
            
        Returns:
            是否成功
        """
        try:
            # 同步错误学习数据
            if "error_learning" in backend_data:
                errors = backend_data["error_learning"]
                for error_data in errors:
                    self.error_engine.record_error(**error_data)
            
            # 同步任务优化数据
            if "task_optimization" in backend_data:
                tasks = backend_data["task_optimization"]
                for task_data in tasks:
                    # 确保有task_id
                    if "task_id" not in task_data:
                        import uuid
                        task_data["task_id"] = f"task_{uuid.uuid4().hex[:8]}"
                    self.task_optimizer.record_task_execution(**task_data)
            
            # 同步视觉学习数据
            if "visual_learning" in backend_data:
                visual_data = backend_data["visual_learning"]
                for obj_data in visual_data:
                    self.visual_engine.record_recognition(**obj_data)
            
            logger.info("从后台同步数据成功")
            return True
        except Exception as e:
            logger.error(f"从后台同步数据失败: {e}")
            return False
    
    def prepare_backend_sync(self) -> Dict[str, Any]:
        """
        准备同步到后台的数据
        
        Returns:
            准备同步的数据字典
        """
        try:
            # 获取错误学习数据（最近100条）
            error_records = self.error_engine.get_recent_errors(limit=100)
            
            # 获取任务执行数据（最近100条）
            task_executions = list(self.task_optimizer.task_executions.values())[-100:]
            
            # 获取视觉识别数据（最近100条）
            visual_objects = self.visual_engine._objects[-100:] if len(self.visual_engine._objects) > 100 else self.visual_engine._objects
            
            return {
                "error_learning": [e.to_dict() for e in error_records],
                "task_optimization": [t.to_dict() for t in task_executions],
                "visual_learning": [o.to_dict() for o in visual_objects],
                "sync_time": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"准备同步数据失败: {e}")
            return {}

