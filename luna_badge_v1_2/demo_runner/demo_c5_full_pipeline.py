"""
C-5 完整链路 Demo

展示 C-1 → C-2 → C-3 → C-5 → C-4 完整表达链路
"""

import os
import sys
import time
import logging

# 设置日志格式
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from expression.contracts import create_navigation_contract, ACTION_TURN_LEFT, ACTION_TURN_RIGHT, ACTION_GO_STRAIGHT
from expression.embodiment import EmbodimentType, EmbodimentResolver
from expression.scene import SceneClassifier
from expression.calibration import ExpressionCalibrator
from expression.renderer import (
    ExpressionTemplate,
    TemplateRegistry,
    RendererPipeline,
    RenderProfile
)
from expression.profile import ExpressionProfile
from expression.scheduler.c5_types import VisionRhythmContext, ExpressionCandidate
from expression.scheduler.c5_scheduler import C5Scheduler


class C5FullPipelineDemo:
    """C-5 完整链路 Demo"""
    
    def __init__(self):
        """初始化 Demo"""
        # C-2: 身体形态和场景
        self.resolver = EmbodimentResolver(default_embodiment=EmbodimentType.BLIND_BADGE)
        self.classifier = SceneClassifier()
        self.calibrator = ExpressionCalibrator()
        
        # C-3: 渲染器
        self.registry = TemplateRegistry()
        self.registry.register(ExpressionTemplate(
            template_id="NAV_TURN_SIMPLE",
            supported_actions=["turn_left", "turn_right"],
            min_precision=1,
            max_precision=5,
            language="zh",
            pattern="{distance}{unit}后，{direction}转"
        ))
        self.registry.register(ExpressionTemplate(
            template_id="NAV_GO_STRAIGHT",
            supported_actions=["go_straight"],
            min_precision=1,
            max_precision=5,
            language="zh",
            pattern="继续直行{distance}{unit}"
        ))
        
        # C-5: 表达画像
        self.expression_profile = ExpressionProfile.vision_impaired_default()
        
        # C-3: 渲染管道（接入 C-5 画像）
        self.renderer = RendererPipeline(
            self.registry,
            expression_profile=self.expression_profile
        )
        
        # C-5: 调度器
        self.scheduler = C5Scheduler()
        
        # 当前视觉状态
        self.current_vision_state = "STABLE"
        self.current_speed = 0.5
    
    def create_vision_context(self, vision_state: str = None, speed: float = None) -> VisionRhythmContext:
        """创建视角节奏上下文"""
        return VisionRhythmContext(
            vision_state=vision_state or self.current_vision_state,
            speed_mps=speed or self.current_speed,
            last_vision_ts=time.time()
        )
    
    def emit_expression(self, expr: ExpressionCandidate, delay_ms: int):
        """输出表达式（模拟 TTS）"""
        if delay_ms > 0:
            time.sleep(delay_ms / 1000.0)
        
        # 从 contract_id 构造 ExpressionParams（简化版）
        # 实际应该从缓存或重新构造
        print(f"🎤 [TTS] {expr.contract_id} (延迟: {delay_ms}ms)")
    
    def run_scenario(self, name: str, contract_action: str, distance_m: float, 
                     vision_state: str = "STABLE", speed: float = 0.5, 
                     urgency: str = "normal", is_critical: bool = False):
        """运行一个场景"""
        print(f"\n{'='*60}")
        print(f"场景: {name}")
        print(f"{'='*60}")
        
        # C-1: 创建 Contract
        contract = create_navigation_contract(
            action=contract_action,
            distance_m=distance_m,
            confidence=0.9,
            direction=contract_action.split("_")[-1] if "_" in contract_action else None
        )
        print(f"  C-1 Contract: {contract.action}, {contract.distance_m}m, confidence={contract.confidence}")
        
        # C-2: 校准参数
        embodiment_ctx = self.resolver.resolve()
        scene_ctx = self.classifier.classify({
            "scene": "outdoor",
            "distance_m": distance_m
        })
        params = self.calibrator.calibrate(contract, embodiment_ctx, scene_ctx)
        print(f"  C-2 Params: {params.distance_value} {params.distance_unit}, {params.direction_reference}")
        
        # C-3: 渲染文本
        text = self.renderer._render_text(params, RenderProfile.default())
        print(f"  C-3 Text: {text}")
        
        # C-5: 创建表达式候选
        expr_candidate = ExpressionCandidate(
            contract_id=f"nav.{contract.action}",
            urgency=urgency,
            is_critical=is_critical,
            duplicate_key=f"nav_{contract.action}_{int(time.time())}"
        )
        
        # C-5: 创建视角上下文
        vision_ctx = self.create_vision_context(vision_state, speed)
        print(f"  C-5 Vision Context: state={vision_ctx.vision_state}, speed={vision_ctx.speed_mps:.2f} m/s")
        
        # C-5: 调度
        result = self.scheduler.schedule(expr_candidate, vision_ctx, self.emit_expression)
        print(f"  C-5 Schedule Result: {result}")
        
        return result
    
    def run_demo(self):
        """运行完整 Demo"""
        print("="*60)
        print("C-5 完整链路 Demo")
        print("="*60)
        print("\n展示 C-1 → C-2 → C-3 → C-5 完整表达链路")
        print("所有表达都遵循视角节奏\n")
        
        # 场景 1: 正常导航（STABLE + normal）
        self.run_scenario(
            "正常导航 - 左转",
            ACTION_TURN_LEFT,
            distance_m=5.0,
            vision_state="STABLE",
            speed=0.8,
            urgency="normal"
        )
        
        time.sleep(0.5)
        
        # 场景 2: 视觉转弯中（TURNING + normal）→ 应该被阻断
        self.run_scenario(
            "视觉转弯中 - 非关键表达",
            ACTION_TURN_RIGHT,
            distance_m=3.0,
            vision_state="TURNING",
            speed=0.6,
            urgency="normal",
            is_critical=False
        )
        
        time.sleep(0.5)
        
        # 场景 3: 视觉转弯中（TURNING + critical）→ 应该能输出
        self.run_scenario(
            "视觉转弯中 - 关键安全警告",
            ACTION_GO_STRAIGHT,
            distance_m=2.0,
            vision_state="TURNING",
            speed=0.6,
            urgency="high",
            is_critical=True
        )
        
        time.sleep(0.5)
        
        # 场景 4: 低速稳定（STABLE + low）→ 应该入队并延迟
        self.run_scenario(
            "低速稳定 - 低优先级提示",
            ACTION_GO_STRAIGHT,
            distance_m=10.0,
            vision_state="STABLE",
            speed=0.3,
            urgency="low"
        )
        
        # 处理队列
        print(f"\n  处理队列...")
        vision_ctx = self.create_vision_context("STABLE", 0.3)
        self.scheduler.process_queue(vision_ctx, self.emit_expression)
        
        time.sleep(0.5)
        
        # 场景 5: 视觉状态变化 → 队列清空
        print(f"\n{'='*60}")
        print("场景: 视觉状态变化 → 队列清空")
        print(f"{'='*60}")
        
        # 先入队一个低优先级
        expr1 = ExpressionCandidate(
            contract_id="nav.hint.low",
            urgency="low",
            is_critical=False
        )
        vision_ctx_stable = self.create_vision_context("STABLE", 0.5)
        result1 = self.scheduler.schedule(expr1, vision_ctx_stable, self.emit_expression)
        print(f"  STABLE 状态入队: {result1}, 队列大小: {self.scheduler.queue.size()}")
        
        # 视觉状态变化 → TURNING
        expr2 = ExpressionCandidate(
            contract_id="nav.turn.left",
            urgency="normal",
            is_critical=False
        )
        vision_ctx_turning = self.create_vision_context("TURNING", 0.8)
        result2 = self.scheduler.schedule(expr2, vision_ctx_turning, self.emit_expression)
        print(f"  TURNING 状态调度: {result2}, 队列大小: {self.scheduler.queue.size()}")
        
        assert self.scheduler.queue.is_empty(), "队列应该被清空"
        
        print("\n" + "="*60)
        print("✅ Demo 完成")
        print("="*60)
        print("\n关键观察点:")
        print("  1. 所有表达都遵循视角节奏")
        print("  2. TURNING 状态下非关键表达被阻断")
        print("  3. 关键表达可以覆盖 TURNING 限制")
        print("  4. 低优先级表达入队并延迟输出")
        print("  5. 视觉状态变化时队列自动清空")
        print("\n日志格式: [C5] action=... vision_state=... speed=... delay=... reason=...")


def main():
    """主函数"""
    demo = C5FullPipelineDemo()
    demo.run_demo()


if __name__ == "__main__":
    main()
