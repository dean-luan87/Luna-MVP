# -*- coding: utf-8 -*-
"""
v1.8.4: Risk 鲁棒性测试摘要生成器（Summary Generator）

目标：
为每个 Scenario 产出可回归、可对比、可解释的摘要结果，用于评审与后续模型接入前后的对照分析。

原则：
- 只读取 RiskDebugSnapshot
- 不反向影响 risk 计算
- Shadow Mode 下同样生效
- 不新增依赖，不影响 runtime 性能
"""

from __future__ import annotations
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from collections import Counter
import json
import os
import re
from datetime import datetime

from core.risk.risk_debug import RiskDebugSnapshot, RiskObjectSnapshot
from core.risk.robustness.fingerprint import (
    calculate_risk_params_fingerprint,
    get_build_info,
)


@dataclass
class ScenarioSummary:
    """场景摘要"""
    scenario: str
    frames: int
    risk_objects: int
    max_risk_level: float
    max_delta_risk: float
    trend_distribution: Dict[str, int]
    dynamic_active_ratio: float
    triggered: bool
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)


@dataclass
class RunSummary:
    """运行汇总"""
    summary_schema_version: str
    run_id: str
    build: Dict[str, str]
    risk_params_fingerprint: str
    seed: Optional[int]
    shadow_mode: bool
    scenarios: int
    total_frames: int
    any_triggered: bool
    global_max_risk_level: float
    global_max_delta_risk: float
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)


class SummaryGenerator:
    """
    摘要生成器
    
    从 RiskDebugSnapshot 列表中生成结构化摘要
    """
    
    @staticmethod
    def generate_scenario_summary(
        scenario_name: str,
        snapshots: List[RiskDebugSnapshot]
    ) -> ScenarioSummary:
        """
        生成场景摘要
        
        Args:
            scenario_name: 场景名称
            snapshots: 该场景期间收集的所有快照
        
        Returns:
            ScenarioSummary: 场景摘要
        """
        if not snapshots:
            return ScenarioSummary(
                scenario=scenario_name,
                frames=0,
                risk_objects=0,
                max_risk_level=0.0,
                max_delta_risk=0.0,
                trend_distribution={},
                dynamic_active_ratio=0.0,
                triggered=False
            )
        
        # 统计信息
        frames = len(snapshots)
        risk_objects_set = set()
        max_risk_level = 0.0
        max_delta_risk = 0.0
        trend_counter = Counter()
        dynamic_active_count = 0
        dynamic_total_count = 0
        triggered = False
        
        for snapshot in snapshots:
            # 检查是否触发
            if snapshot.advisory_triggered:
                triggered = True
            
            for obj in snapshot.objects:
                # 风险对象集合
                risk_objects_set.add(obj.risk_id)
                
                # 最大风险等级
                if obj.risk_level > max_risk_level:
                    max_risk_level = obj.risk_level
                
                # 最大 delta_risk
                if obj.delta_risk > max_delta_risk:
                    max_delta_risk = obj.delta_risk
                
                # 趋势分布
                trend_counter[obj.trend] += 1
                
                # 动态激活比例
                if obj.dynamic_active is not None:
                    dynamic_total_count += 1
                    if obj.dynamic_active:
                        dynamic_active_count += 1
        
        # 计算动态激活比例
        dynamic_active_ratio = (
            dynamic_active_count / dynamic_total_count
            if dynamic_total_count > 0
            else 0.0
        )
        
        return ScenarioSummary(
            scenario=scenario_name,
            frames=frames,
            risk_objects=len(risk_objects_set),
            max_risk_level=max_risk_level,
            max_delta_risk=max_delta_risk,
            trend_distribution=dict(trend_counter),
            dynamic_active_ratio=dynamic_active_ratio,
            triggered=triggered
        )
    
    @staticmethod
    def generate_run_summary(
        scenario_summaries: List[ScenarioSummary],
        run_id: Optional[str] = None,
        seed: Optional[int] = None,
        shadow_mode: bool = True
    ) -> RunSummary:
        """
        生成运行汇总
        
        Args:
            scenario_summaries: 所有场景摘要
            run_id: 运行 ID（如果为 None 则自动生成）
            seed: 随机种子
            shadow_mode: Shadow Mode 开关
        
        Returns:
            RunSummary: 运行汇总
        """
        if run_id is None:
            run_id = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        
        total_frames = sum(s.frames for s in scenario_summaries)
        any_triggered = any(s.triggered for s in scenario_summaries)
        global_max_risk_level = max(
            (s.max_risk_level for s in scenario_summaries),
            default=0.0
        )
        global_max_delta_risk = max(
            (s.max_delta_risk for s in scenario_summaries),
            default=0.0
        )
        
        # 获取构建信息
        build_info = get_build_info()
        
        # 计算风险参数指纹
        risk_params_fingerprint = calculate_risk_params_fingerprint()
        
        return RunSummary(
            summary_schema_version="1.0",
            run_id=run_id,
            build=build_info,
            risk_params_fingerprint=risk_params_fingerprint,
            seed=seed,
            shadow_mode=shadow_mode,
            scenarios=len(scenario_summaries),
            total_frames=total_frames,
            any_triggered=any_triggered,
            global_max_risk_level=global_max_risk_level,
            global_max_delta_risk=global_max_delta_risk
        )
    
    @staticmethod
    def _sanitize_filename(name: str) -> str:
        """
        将场景名称转换为安全的文件名
        
        Args:
            name: 场景名称
        
        Returns:
            str: 安全的文件名
        """
        # 替换特殊字符为下划线
        name = re.sub(r'[^\w\-_\.]', '_', name)
        # 移除连续的下划线
        name = re.sub(r'_+', '_', name)
        # 移除开头和结尾的下划线
        name = name.strip('_')
        return name
    
    @staticmethod
    def save_summary(
        summary: ScenarioSummary | RunSummary,
        output_dir: str,
        filename: str
    ) -> str:
        """
        保存摘要到文件
        
        Args:
            summary: 摘要对象
            output_dir: 输出目录
            filename: 文件名（如果包含特殊字符会自动清理）
        
        Returns:
            str: 保存的文件路径
        """
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 清理文件名
        safe_filename = SummaryGenerator._sanitize_filename(filename)
        
        # 生成文件路径
        filepath = os.path.join(output_dir, safe_filename)
        
        # 保存 JSON
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(summary.to_dict(), f, indent=2, ensure_ascii=False)
        
        return filepath

