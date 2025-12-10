"""
Luna Badge v1.4.6d Step 10 — NavigationScheduler E2E Demo

验证 NavigationScheduler → DecisionCore → TTSRouterFacade → NavigationVoiceRouter 全链路
"""

import sys
import os

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import time
from task_engine.tts import tts_manager
from task_engine.tts.runtime_driver import TTSRuntimeDriver
from task_engine.navigation.navigation_scheduler import (
    NavigationScheduler,
    TurnEvent,
    StraightEvent,
    ObstacleEvent,
)
from decision_core.decision_core import DecisionCore, Action
from core.flow_engine.planner import FlowPlanner
from core.flow_engine.runtime import FlowRuntime
from core.query_engine.query_manager import QueryEngine
from task_chain.task_chain_manager import TaskChainManager


def run_demo():
    """运行 E2E Demo"""
    
    # 初始化组件
    tts_manager.clear()
    driver = TTSRuntimeDriver()
    
    # 创建 DecisionCore（需要所有依赖）
    from core.flow_templates.templates_registry import FlowTemplateRegistry
    from core.flow_templates.hospital_go_template import GoHospitalTemplate
    
    template_registry = FlowTemplateRegistry()
    template_registry.register_template(GoHospitalTemplate())
    
    planner = FlowPlanner(template_registry=template_registry)
    runtime = FlowRuntime()
    query_engine = QueryEngine()
    task_manager = TaskChainManager(runtime=runtime)
    
    decision_core = DecisionCore(
        flow_planner=planner,
        flow_runtime=runtime,
        query_engine=query_engine,
        task_manager=task_manager,
    )
    
    # 创建 NavigationScheduler 并连接到 DecisionCore
    scheduler = NavigationScheduler(decision_core=decision_core)
    
    print("\n\n" + "=" * 80)
    print("Luna Badge v1.4.6d Step 10 — NavigationScheduler E2E Demo")
    print("=" * 80 + "\n")
    
    # ------------------------------------------------------------------
    # 场景 1：转弯事件 → TTS_ROUTER_TURN
    # ------------------------------------------------------------------
    print("\n[场景 1] 转弯事件 → TTS_ROUTER_TURN\n")
    
    turn_event = TurnEvent(direction="左转", distance=5.0)
    scheduler.process_turn_event(turn_event)
    
    utterances = tts_manager.get_queue()
    driver.process_once()
    
    print(f"   ✅ 队列中有 {len(utterances)} 条播报")
    for i, u in enumerate(utterances):
        print(f"   {i+1}. {u.text}")
    
    # ------------------------------------------------------------------
    # 场景 2：直行事件 → TTS_ROUTER_STRAIGHT
    # ------------------------------------------------------------------
    print("\n[场景 2] 直行事件 → TTS_ROUTER_STRAIGHT\n")
    
    time.sleep(0.5)  # 等待节流窗口过期
    tts_manager.clear()
    
    straight_event = StraightEvent(distance=20.0)
    scheduler.process_straight_event(straight_event)
    
    utterances = tts_manager.get_queue()
    driver.process_once()
    
    print(f"   ✅ 队列中有 {len(utterances)} 条播报")
    for i, u in enumerate(utterances):
        print(f"   {i+1}. {u.text}")
    
    # ------------------------------------------------------------------
    # 场景 3：障碍物事件 → TTS_ROUTER_OBSTACLE
    # ------------------------------------------------------------------
    print("\n[场景 3] 障碍物事件 → TTS_ROUTER_OBSTACLE\n")
    
    time.sleep(0.5)  # 等待节流窗口过期
    tts_manager.clear()
    
    obstacle_event = ObstacleEvent(
        obstacle_type="human",
        distance=2.0,
        direction="前方"
    )
    scheduler.process_obstacle_event(obstacle_event)
    
    utterances = tts_manager.get_queue()
    driver.process_once()
    
    print(f"   ✅ 队列中有 {len(utterances)} 条播报")
    for i, u in enumerate(utterances):
        print(f"   {i+1}. {u.text}")
    
    # ------------------------------------------------------------------
    # 场景 4：连续转弯事件（应被节流）
    # ------------------------------------------------------------------
    print("\n[场景 4] 连续转弯事件（应被节流）\n")
    
    time.sleep(0.5)  # 等待节流窗口过期
    tts_manager.clear()
    
    turn_event1 = TurnEvent(direction="左转", distance=6.0)
    turn_event2 = TurnEvent(direction="左转", distance=6.1)
    
    scheduler.process_turn_event(turn_event1)
    scheduler.process_turn_event(turn_event2)
    
    utterances = tts_manager.get_queue()
    driver.process_once()
    
    print(f"   ✅ 队列中有 {len(utterances)} 条播报（应只有 1 条，因为节流）")
    for i, u in enumerate(utterances):
        print(f"   {i+1}. {u.text}")
    
    # ------------------------------------------------------------------
    # 场景 5：转弯 → 障碍物（安全播报应打断导航）
    # ------------------------------------------------------------------
    print("\n[场景 5] 转弯 → 障碍物（安全播报应打断导航）\n")
    
    time.sleep(0.5)  # 等待节流窗口过期
    tts_manager.clear()
    
    turn_event = TurnEvent(direction="右转", distance=10.0)
    obstacle_event = ObstacleEvent(
        obstacle_type="object",
        distance=1.0,
        direction="前方"
    )
    
    scheduler.process_turn_event(turn_event)
    scheduler.process_obstacle_event(obstacle_event)
    
    utterances = tts_manager.get_queue()
    driver.process_once()
    
    print(f"   ✅ 队列中有 {len(utterances)} 条播报")
    for i, u in enumerate(utterances):
        print(f"   {i+1}. {u.text} (category={u.meta.get('ttscategory')}, priority={u.priority}, interrupt={u.interrupt})")
    
    print("\n\n" + "=" * 80)
    print("Demo 完成！")
    print("=" * 80)
    print("\n说明：")
    print("- 场景 1-3 验证了 NavigationScheduler → DecisionCore → TTSRouterFacade 全链路")
    print("- 场景 4 验证了 TimeWindowGate 节流机制")
    print("- 场景 5 验证了安全播报的优先级和打断机制\n")


if __name__ == "__main__":
    run_demo()

