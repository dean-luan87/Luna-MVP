# -*- coding: utf-8 -*-
"""
v1.8.4: Risk 鲁棒性测试框架（Robustness Test Harness）

目标：
在真实模型接入前，确认 risk 系统在"烂数据 + 极端行为"下不会乱说话。

架构定位：
【真实系统】
UserPositionProvider
RiskAdvisoryService
RiskDebugSnapshot
Decision / Speech

【鲁棒性验证层】 ← 本模块（只在测试/仿真用）
RobustnessHarness
 ├─ Position Noise Injector
 ├─ Scenario Script Runner
 ├─ Shadow Mode Gate
 └─ Snapshot Logger

原则：
- 不改 risk 核心
- 不改 decision
- 不改 speech
- 只"喂数据 + 看日志"
"""

from __future__ import annotations
from typing import List, Tuple, Optional, Callable, Dict, Any
from dataclasses import dataclass
import time
import datetime
import random

from core.risk.robustness.noise_position_provider import NoisePositionProvider
from core.risk.robustness.scenario_runner import Scenario, ScenarioLibrary
from core.risk.robustness.summary_generator import (
    SummaryGenerator,
    ScenarioSummary,
    RunSummary,
)
from core.risk.risk_debug import RiskDebugSnapshot

XY = Tuple[float, float]

# 默认随机种子（确保可复现）
DEFAULT_SEED = 123456


@dataclass
class TestScenario:
    """测试场景定义（兼容旧接口）"""
    name: str
    description: str
    position_generator: Callable[[], Optional[XY]]
    duration_seconds: float = 10.0
    expected_behavior: str = ""  # 期望行为描述


class RiskRobustnessTestHarness:
    """
    Risk 鲁棒性测试框架
    
    统一入口，支持噪声注入、极端场景、Shadow Mode
    
    原则：
    - 不改 risk 核心
    - 不改 decision
    - 不改 speech
    - 只"喂数据 + 看日志"
    """
    
    def __init__(
        self,
        risk_advisory_service,
        shadow_mode: bool = True,
        output_dir: str = "artifacts/risk_robustness",
        seed: Optional[int] = None
    ):
        """
        初始化测试框架
        
        Args:
            risk_advisory_service: RiskAdvisoryService 实例
            shadow_mode: Shadow Mode 开关（True = 只打日志，不播报）
            output_dir: 摘要输出目录（默认 artifacts/risk_robustness）
            seed: 随机种子（如果为 None 则使用默认值 DEFAULT_SEED）
        """
        self.risk_advisory_service = risk_advisory_service
        self.shadow_mode = shadow_mode
        self.output_dir = output_dir
        self.seed = seed if seed is not None else DEFAULT_SEED
        self.test_results: List[Dict[str, Any]] = []
        self.scenario_summaries: List[ScenarioSummary] = []
        
        # 显式设置随机种子（确保可复现）
        random.seed(self.seed)
        
        # 如果使用 numpy，也需要设置
        try:
            import numpy as np
            np.random.seed(self.seed)
        except ImportError:
            pass
    
    def run_scenario(
        self,
        scenario: TestScenario,
        sample_rate: float = 0.1,  # 每 0.1 秒采样一次
        verbose: bool = True
    ) -> Dict[str, Any]:
        """
        运行测试场景
        
        Args:
            scenario: 测试场景定义
            sample_rate: 采样率（秒）
            verbose: 是否输出详细信息
        
        Returns:
            Dict[str, Any]: 测试结果
        """
        if verbose:
            print(f"\n{'=' * 70}")
            print(f"🧪 运行场景: {scenario.name}")
            print(f"   描述: {scenario.description}")
            print(f"   期望行为: {scenario.expected_behavior}")
            print(f"{'=' * 70}\n")
        
        # 统计信息
        advisory_count = 0
        advisory_frames: List[int] = []
        delta_risk_spikes: List[float] = []
        trend_changes: List[str] = []
        last_trend = None
        
        # 收集所有快照（用于生成摘要）
        snapshots: List[RiskDebugSnapshot] = []
        
        start_time = time.time()
        frame_count = 0
        
        while time.time() - start_time < scenario.duration_seconds:
            # 生成位置
            user_xy = scenario.position_generator()
            if user_xy is None:
                break  # 场景结束信号（position_generator 返回 None 表示结束）
            
            ts = time.time()
            
            # 调用 risk_advisory_service.tick()
            advisory_text = self.risk_advisory_service.tick(user_xy, ts=ts)
            
            # Shadow Mode：拦截播报，只记录
            if self.shadow_mode and advisory_text:
                advisory_text = None  # 不触发播报，只记录
            
            # 获取调试快照
            snapshot = self.risk_advisory_service.get_last_debug_snapshot()
            
            # 收集快照（用于生成摘要）
            if snapshot:
                snapshots.append(snapshot)
            
            frame_count += 1
            
            # 统计
            if advisory_text:
                advisory_count += 1
                advisory_frames.append(frame_count)
            
            if snapshot:
                for obj in snapshot.objects:
                    # 检测 delta_risk 峰值
                    if obj.delta_risk > 0.1:
                        delta_risk_spikes.append(obj.delta_risk)
                    
                    # 检测 trend 变化
                    if obj.trend != last_trend:
                        trend_changes.append(f"{last_trend} → {obj.trend}")
                        last_trend = obj.trend
            
            time.sleep(sample_rate)
        
        # 生成测试结果
        result = {
            "scenario_name": scenario.name,
            "duration_seconds": time.time() - start_time,
            "frame_count": frame_count,
            "advisory_count": advisory_count,
            "advisory_frames": advisory_frames,
            "delta_risk_spikes": delta_risk_spikes,
            "trend_changes": trend_changes,
            "shadow_mode": self.shadow_mode,
        }
        
        self.test_results.append(result)
        
        # 生成场景摘要
        scenario_summary = SummaryGenerator.generate_scenario_summary(
            scenario_name=scenario.name,
            snapshots=snapshots
        )
        self.scenario_summaries.append(scenario_summary)
        
        # 保存场景摘要到文件
        filename = f"scenario_{scenario.name}.summary.json"
        filepath = SummaryGenerator.save_summary(
            summary=scenario_summary,
            output_dir=self.output_dir,
            filename=filename
        )
        
        if verbose:
            self._print_result(result)
            print(f"  📄 场景摘要已保存: {filepath}")
        
        return result
    
    def _print_result(self, result: Dict[str, Any]):
        """打印测试结果"""
        print(f"\n{'=' * 70}")
        print(f"📊 测试结果: {result['scenario_name']}")
        print(f"{'=' * 70}")
        print(f"  持续时间: {result['duration_seconds']:.1f} 秒")
        print(f"  总帧数: {result['frame_count']}")
        print(f"  触发 ADVISORY 次数: {result['advisory_count']}")
        if result['advisory_frames']:
            print(f"  触发帧: {result['advisory_frames']}")
        if result['delta_risk_spikes']:
            print(f"  ΔRisk 峰值: {max(result['delta_risk_spikes']):.3f}")
        if result['trend_changes']:
            print(f"  趋势变化次数: {len(result['trend_changes'])}")
        print(f"  Shadow Mode: {result['shadow_mode']}")
        print(f"{'=' * 70}\n")
    
    def run_all_scenarios(
        self,
        scenarios: List[TestScenario],
        verbose: bool = True
    ) -> Dict[str, Any]:
        """
        运行所有场景
        
        Args:
            scenarios: 场景列表
            verbose: 是否输出详细信息
        
        Returns:
            Dict[str, Any]: 汇总结果
        """
        if verbose:
            print("=" * 70)
            print("🚀 Risk 鲁棒性测试框架")
            print("=" * 70)
            print(f"Shadow Mode: {self.shadow_mode}")
            print(f"场景数量: {len(scenarios)}")
            print()
        
        for scenario in scenarios:
            self.run_scenario(scenario, verbose=verbose)
        
        # 汇总
        total_advisories = sum(r['advisory_count'] for r in self.test_results)
        total_frames = sum(r['frame_count'] for r in self.test_results)
        
        summary = {
            "total_scenarios": len(scenarios),
            "total_frames": total_frames,
            "total_advisories": total_advisories,
            "advisory_rate": total_advisories / total_frames if total_frames > 0 else 0.0,
            "results": self.test_results,
        }
        
        if verbose:
            print("=" * 70)
            print("📋 测试汇总")
            print("=" * 70)
            print(f"  总场景数: {summary['total_scenarios']}")
            print(f"  总帧数: {summary['total_frames']}")
            print(f"  总触发次数: {summary['total_advisories']}")
            print(f"  触发率: {summary['advisory_rate']:.2%}")
            print("=" * 70)
        
        # 生成运行汇总（传递 seed 和 shadow_mode）
        run_summary = SummaryGenerator.generate_run_summary(
            scenario_summaries=self.scenario_summaries,
            seed=self.seed,
            shadow_mode=self.shadow_mode
        )
        
        # 保存运行汇总到文件
        run_summary_filepath = SummaryGenerator.save_summary(
            summary=run_summary,
            output_dir=self.output_dir,
            filename="run_summary.json"
        )
        
        if verbose:
            print(f"\n📄 运行汇总已保存: {run_summary_filepath}")
        
        return summary
