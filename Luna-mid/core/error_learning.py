#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
错误纠正学习引擎
记录犯错纠正的过程，分析犯错的原因，上传至后台，降低其他设备学习成本
"""

__version__ = "1.0.0"
__version_info__ = (1, 0, 0)

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class ErrorType(Enum):
    """错误类型枚举"""
    NAVIGATION = "navigation"  # 导航错误
    UNDERSTANDING = "understanding"  # 理解错误
    TASK_EXECUTION = "task_execution"  # 任务执行错误
    RESPONSE = "response"  # 响应错误
    VISUAL_RECOGNITION = "visual_recognition"  # 视觉识别错误
    OTHER = "other"  # 其他错误


class CorrectionSource(Enum):
    """纠正来源枚举"""
    USER = "user"  # 用户纠正
    SYSTEM = "system"  # 系统自动纠正
    MANUAL = "manual"  # 人工纠正


@dataclass
class ErrorRecord:
    """错误记录"""
    error_id: str
    error_type: str
    timestamp: str
    user_id: Optional[str]
    
    # 错误上下文
    context: Dict[str, Any]  # 错误发生时的上下文
    user_input: Optional[str]  # 用户输入
    system_response: Optional[str]  # 系统响应
    expected_response: Optional[str]  # 期望的响应
    
    # 错误分析
    error_reason: Optional[str]  # 错误原因分析
    error_details: Dict[str, Any]  # 错误详细信息
    
    # 纠正信息
    correction: Optional[Dict[str, Any]] = None  # 纠正方案
    correction_source: Optional[str] = None  # 纠正来源
    correction_timestamp: Optional[str] = None  # 纠正时间
    
    # 学习信息
    learned: bool = False  # 是否已学习
    applied_to_other_cases: int = 0  # 应用到其他案例的次数
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return asdict(self)


@dataclass
class ErrorAnalysis:
    """错误分析结果"""
    error_id: str
    root_cause: str  # 根本原因
    contributing_factors: List[str]  # 促成因素
    severity: str  # 严重程度：low, medium, high, critical
    frequency: int  # 发生频率
    impact: str  # 影响范围
    solution: str  # 解决方案
    prevention_measures: List[str]  # 预防措施


class ErrorLearningEngine:
    """错误纠正学习引擎"""
    
    def __init__(self, data_dir: str = "data/errors"):
        """初始化错误学习引擎
        
        Args:
            data_dir: 错误数据存储目录
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.errors_file = self.data_dir / "error_records.json"
        self.analysis_file = self.data_dir / "error_analysis.json"
        
        # 错误记录库
        self.error_records: Dict[str, ErrorRecord] = {}
        
        # 错误分析结果
        self.error_analysis: Dict[str, ErrorAnalysis] = {}
        
        # 加载已有记录
        self._load_errors()
    
    def _load_errors(self):
        """加载错误记录"""
        if self.errors_file.exists():
            try:
                with open(self.errors_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for error_id, error_data in data.items():
                        self.error_records[error_id] = ErrorRecord(**error_data)
                logger.info(f"✅ 已加载 {len(self.error_records)} 条错误记录")
            except Exception as e:
                logger.error(f"❌ 加载错误记录失败: {e}")
        
        if self.analysis_file.exists():
            try:
                with open(self.analysis_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for error_id, analysis_data in data.items():
                        self.error_analysis[error_id] = ErrorAnalysis(**analysis_data)
                logger.info(f"✅ 已加载 {len(self.error_analysis)} 条错误分析")
            except Exception as e:
                logger.error(f"❌ 加载错误分析失败: {e}")
    
    def _save_errors(self):
        """保存错误记录"""
        try:
            data = {eid: record.to_dict() for eid, record in self.error_records.items()}
            with open(self.errors_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"❌ 保存错误记录失败: {e}")
    
    def record_error(
        self,
        error_type: ErrorType,
        context: Dict[str, Any],
        user_input: Optional[str] = None,
        system_response: Optional[str] = None,
        expected_response: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> str:
        """记录错误
        
        Args:
            error_type: 错误类型
            context: 错误上下文
            user_input: 用户输入
            system_response: 系统响应
            expected_response: 期望响应
            user_id: 用户ID
            
        Returns:
            错误ID
        """
        error_id = f"error_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(self.error_records)}"
        
        error_record = ErrorRecord(
            error_id=error_id,
            error_type=error_type.value,
            timestamp=datetime.now().isoformat(),
            user_id=user_id,
            context=context,
            user_input=user_input,
            system_response=system_response,
            expected_response=expected_response,
            error_reason=None,
            error_details={}
        )
        
        self.error_records[error_id] = error_record
        self._save_errors()
        
        logger.info(f"📝 记录错误: {error_id} ({error_type.value})")
        
        return error_id
    
    def correct_error(
        self,
        error_id: str,
        correction: Dict[str, Any],
        correction_source: CorrectionSource,
        correction_notes: Optional[str] = None
    ) -> bool:
        """纠正错误
        
        Args:
            error_id: 错误ID
            correction: 纠正方案
            correction_source: 纠正来源
            correction_notes: 纠正说明
            
        Returns:
            是否成功
        """
        if error_id not in self.error_records:
            logger.warning(f"⚠️ 错误记录不存在: {error_id}")
            return False
        
        error_record = self.error_records[error_id]
        error_record.correction = correction
        error_record.correction_source = correction_source.value
        error_record.correction_timestamp = datetime.now().isoformat()
        
        if correction_notes:
            correction['notes'] = correction_notes
        
        self._save_errors()
        
        logger.info(f"✅ 错误已纠正: {error_id} (来源: {correction_source.value})")
        
        # 自动分析错误原因
        self.analyze_error(error_id)
        
        return True
    
    def analyze_error(self, error_id: str) -> Optional[ErrorAnalysis]:
        """分析错误原因
        
        Args:
            error_id: 错误ID
            
        Returns:
            错误分析结果
        """
        if error_id not in self.error_records:
            return None
        
        error_record = self.error_records[error_id]
        
        # 分析根本原因
        root_cause = self._identify_root_cause(error_record)
        
        # 识别促成因素
        contributing_factors = self._identify_contributing_factors(error_record)
        
        # 评估严重程度
        severity = self._assess_severity(error_record)
        
        # 计算发生频率（相同类型的错误）
        frequency = self._calculate_frequency(error_record.error_type)
        
        # 评估影响范围
        impact = self._assess_impact(error_record)
        
        # 生成解决方案
        solution = self._generate_solution(error_record)
        
        # 生成预防措施
        prevention_measures = self._generate_prevention_measures(error_record, root_cause)
        
        analysis = ErrorAnalysis(
            error_id=error_id,
            root_cause=root_cause,
            contributing_factors=contributing_factors,
            severity=severity,
            frequency=frequency,
            impact=impact,
            solution=solution,
            prevention_measures=prevention_measures
        )
        
        self.error_analysis[error_id] = analysis
        
        # 保存分析结果
        try:
            data = {aid: asdict(analysis) for aid, analysis in self.error_analysis.items()}
            with open(self.analysis_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"❌ 保存错误分析失败: {e}")
        
        logger.info(f"🔍 错误分析完成: {error_id}")
        
        return analysis
    
    def _identify_root_cause(self, error_record: ErrorRecord) -> str:
        """识别根本原因"""
        error_type = error_record.error_type
        context = error_record.context
        
        # 基于错误类型和上下文分析根本原因
        if error_type == ErrorType.NAVIGATION.value:
            if "location_accuracy" in context:
                return "位置精度不足导致导航偏差"
            elif "path_planning" in context:
                return "路径规划算法问题"
            else:
                return "导航系统判断错误"
        
        elif error_type == ErrorType.UNDERSTANDING.value:
            if "ambiguous_input" in context:
                return "用户输入歧义导致理解偏差"
            elif "context_missing" in context:
                return "上下文信息缺失"
            else:
                return "语义理解引擎错误"
        
        elif error_type == ErrorType.VISUAL_RECOGNITION.value:
            return "视觉识别模型无法识别未知物体或场景"
        
        else:
            return "系统逻辑错误或数据问题"
    
    def _identify_contributing_factors(self, error_record: ErrorRecord) -> List[str]:
        """识别促成因素"""
        factors = []
        context = error_record.context
        
        if "low_confidence" in context:
            factors.append("系统置信度较低")
        if "unfamiliar_scenario" in context:
            factors.append("不熟悉的场景")
        if "noise" in context:
            factors.append("环境噪音干扰")
        if "lighting" in context:
            factors.append("光照条件不佳")
        if "user_behavior_unusual" in context:
            factors.append("用户行为异常")
        
        return factors if factors else ["未知因素"]
    
    def _assess_severity(self, error_record: ErrorRecord) -> str:
        """评估严重程度"""
        error_type = error_record.error_type
        
        # 根据错误类型和上下文评估严重程度
        if error_type == ErrorType.NAVIGATION.value:
            if "safety" in error_record.context:
                return "critical"
            else:
                return "high"
        elif error_type == ErrorType.UNDERSTANDING.value:
            return "medium"
        else:
            return "low"
    
    def _calculate_frequency(self, error_type: str) -> int:
        """计算发生频率"""
        return sum(1 for record in self.error_records.values() 
                  if record.error_type == error_type)
    
    def _assess_impact(self, error_record: ErrorRecord) -> str:
        """评估影响范围"""
        if error_record.user_id:
            return f"影响用户: {error_record.user_id}"
        else:
            return "影响当前会话"
    
    def _generate_solution(self, error_record: ErrorRecord) -> str:
        """生成解决方案"""
        if error_record.correction:
            return error_record.correction.get('solution', '已纠正，待应用')
        else:
            return "待纠正"
    
    def _generate_prevention_measures(self, error_record: ErrorRecord, root_cause: str) -> List[str]:
        """生成预防措施"""
        measures = []
        
        if "精度" in root_cause:
            measures.append("提高位置定位精度")
            measures.append("增加路径验证机制")
        
        if "理解" in root_cause:
            measures.append("增强上下文理解能力")
            measures.append("添加歧义消解机制")
        
        if "识别" in root_cause:
            measures.append("扩展视觉识别模型训练数据")
            measures.append("建立未知物体联网查询机制")
        
        if not measures:
            measures.append("加强错误监控和预警")
            measures.append("定期分析错误模式")
        
        return measures
    
    def apply_correction_to_similar_cases(self, error_id: str) -> int:
        """将纠正方案应用到相似案例
        
        Args:
            error_id: 错误ID
            
        Returns:
            应用的案例数
        """
        if error_id not in self.error_records:
            return 0
        
        error_record = self.error_records[error_id]
        if not error_record.correction:
            return 0
        
        applied_count = 0
        error_type = error_record.error_type
        
        # 找到相同类型的未纠正错误
        for eid, record in self.error_records.items():
            if (eid != error_id and 
                record.error_type == error_type and 
                not record.correction):
                # 应用纠正方案
                record.correction = error_record.correction.copy()
                record.correction_source = "system_auto"
                record.correction_timestamp = datetime.now().isoformat()
                record.learned = True
                applied_count += 1
        
        if applied_count > 0:
            self._save_errors()
            error_record.applied_to_other_cases = applied_count
            logger.info(f"✅ 已将纠正方案应用到 {applied_count} 个相似案例")
        
        return applied_count
    
    def export_for_backend(self, error_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """导出错误数据供后台使用
        
        Args:
            error_ids: 要导出的错误ID列表，None表示导出所有
            
        Returns:
            导出的错误数据
        """
        if error_ids is None:
            error_ids = list(self.error_records.keys())
        
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "total_errors": len(error_ids),
            "errors": [],
            "analyses": []
        }
        
        for error_id in error_ids:
            if error_id in self.error_records:
                error_record = self.error_records[error_id]
                export_data["errors"].append(error_record.to_dict())
                
                if error_id in self.error_analysis:
                    analysis = self.error_analysis[error_id]
                    export_data["analyses"].append(asdict(analysis))
        
        return export_data
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """获取错误统计信息"""
        stats = {
            "total_errors": len(self.error_records),
            "by_type": {},
            "by_severity": {"low": 0, "medium": 0, "high": 0, "critical": 0},
            "corrected": 0,
            "uncorrected": 0,
            "learned": 0
        }
        
        for record in self.error_records.values():
            # 按类型统计
            error_type = record.error_type
            stats["by_type"][error_type] = stats["by_type"].get(error_type, 0) + 1
            
            # 纠正状态
            if record.correction:
                stats["corrected"] += 1
            else:
                stats["uncorrected"] += 1
            
            # 学习状态
            if record.learned:
                stats["learned"] += 1
            
            # 按严重程度统计
            if record.error_id in self.error_analysis:
                severity = self.error_analysis[record.error_id].severity
                stats["by_severity"][severity] += 1
        
        return stats
