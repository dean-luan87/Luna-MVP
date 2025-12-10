"""
Luna Badge v1.4.6d Step 11 — Safety Queue E2E Demo

验证安全播报高优先级队列（Preemptive Safety Queue）功能
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
    ObstacleEvent,
)
from decision_core.decision_core import DecisionCore, Action
from core.flow_templates.templates_registry import FlowTemplateRegistry
from core.flow_templates.hospital_go_template import GoHospitalTemplate
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
    print("Luna Badge v1.4.6d Step 11 — Safety Queue E2E Demo")
    print("=" * 80 + "\n")
    
    # ------------------------------------------------------------------
    # 场景 1：主队列有内容时，安全播报应抢占
    # ------------------------------------------------------------------
    print("\n[场景 1] 主队列有内容时，安全播报应抢占\n")
    
    # 先加入主队列
    tts_manager.speak("请直行", priority=50)
    tts_manager.speak("5米后左转", priority=50)
    
    # 然后加入安全队列（近距离障碍物）
    obstacle_event = ObstacleEvent(
        obstacle_type="human",
        distance=1.0,  # < 1.5m，触发安全播报
        direction="前方"
    )
    scheduler.process_obstacle_event(obstacle_event)
    
    # 获取队列快照
    main_queue = tts_manager.get_queue()
    safety_queue = tts_manager.get_safety_queue()
    
    print(f"   主队列: {len(main_queue)} 条")
    print(f"   安全队列: {len(safety_queue)} 条")
    
    # 处理播报
    utterances = tts_manager.pop_all()
    driver.process_once()
    
    print(f"\n   实际播报顺序（应优先安全播报）:")
    for i, u in enumerate(utterances):
        print(f"   {i+1}. {u.text} (priority={u.priority}, category={u.meta.get('ttscategory')})")
    
    assert len(safety_queue) > 0, "安全队列应该有内容"
    assert utterances[0].meta.get("ttscategory") == "SAFETY", "第一条应该是安全播报"
    
    # ------------------------------------------------------------------
    # 场景 2：安全播报限频（2秒内不重复）
    # ------------------------------------------------------------------
    print("\n[场景 2] 安全播报限频（2秒内不重复）\n")
    
    time.sleep(0.1)  # 短暂等待
    tts_manager.clear()
    
    # 连续两次相同安全播报
    from task_engine.tts import Utterance
    utter1 = Utterance(text="前方危险，请立即停下", priority=100)
    utter2 = Utterance(text="前方危险，请立即停下", priority=100)
    
    result1 = tts_manager.push_safety(utter1)
    result2 = tts_manager.push_safety(utter2)
    
    safety_queue = tts_manager.get_safety_queue()
    print(f"   第一次加入: {result1}")
    print(f"   第二次加入（2秒内）: {result2} (应返回 False)")
    print(f"   安全队列长度: {len(safety_queue)} (应为 1)")
    
    assert result1 is True, "第一次应该成功"
    assert result2 is False, "第二次应该被限频"
    assert len(safety_queue) == 1, "安全队列应该只有 1 条"
    
    # ------------------------------------------------------------------
    # 场景 3：2秒后可以重复安全播报
    # ------------------------------------------------------------------
    print("\n[场景 3] 2秒后可以重复安全播报\n")
    
    tts_manager.clear()
    
    # 第一次安全播报
    from task_engine.tts import Utterance
    utter1 = Utterance(text="前方危险，请立即停下", priority=100)
    result1 = tts_manager.push_safety(utter1)
    
    # 等待超过 2 秒
    time.sleep(2.1)
    
    # 第二次相同安全播报（2秒后）
    utter2 = Utterance(text="前方危险，请立即停下", priority=100)
    result2 = tts_manager.push_safety(utter2)
    
    safety_queue = tts_manager.get_safety_queue()
    print(f"   第一次加入: {result1}")
    print(f"   第二次加入（2秒后）: {result2} (应返回 True)")
    print(f"   安全队列长度: {len(safety_queue)} (应为 2)")
    
    assert result1 is True, "第一次应该成功"
    assert result2 is True, "2秒后应该可以重复"
    assert len(safety_queue) == 2, "安全队列应该有 2 条"
    
    # ------------------------------------------------------------------
    # 场景 4：安全播报跳过时间窗口限制
    # ------------------------------------------------------------------
    print("\n[场景 4] 安全播报跳过时间窗口限制\n")
    
    time.sleep(0.1)
    tts_manager.clear()
    
    # 先加入导航播报（会被节流）
    scheduler.process_turn_event(TurnEvent(direction="左转", distance=5.0))
    scheduler.process_turn_event(TurnEvent(direction="左转", distance=4.8))
    
    # 然后加入安全播报（应跳过节流）
    obstacle_event = ObstacleEvent(
        obstacle_type="object",
        distance=1.2,  # < 1.5m，触发安全播报
        direction="前方"
    )
    scheduler.process_obstacle_event(obstacle_event)
    
    main_queue = tts_manager.get_queue()
    safety_queue = tts_manager.get_safety_queue()
    
    print(f"   主队列: {len(main_queue)} 条（可能被节流）")
    print(f"   安全队列: {len(safety_queue)} 条（应跳过节流）")
    
    utterances = tts_manager.pop_all()
    driver.process_once()
    
    print(f"\n   实际播报顺序:")
    for i, u in enumerate(utterances):
        print(f"   {i+1}. {u.text} (category={u.meta.get('ttscategory')})")
    
    assert len(safety_queue) > 0, "安全队列应该有内容"
    
    # ------------------------------------------------------------------
    # 场景 5：DecisionCore 直接调用 TTS_ROUTER_SAFETY
    # ------------------------------------------------------------------
    print("\n[场景 5] DecisionCore 直接调用 TTS_ROUTER_SAFETY\n")
    
    time.sleep(0.1)
    tts_manager.clear()
    
    action = Action(
        type="TTS_ROUTER_SAFETY",
        payload={
            "text": "紧急：前方有危险，请立即停下！",
            "meta": {"source": "decision_core"}
        }
    )
    decision_core.handle_action(action)
    
    safety_queue = tts_manager.get_safety_queue()
    print(f"   安全队列: {len(safety_queue)} 条")
    
    utterances = tts_manager.pop_all()
    driver.process_once()
    
    print(f"\n   实际播报:")
    for i, u in enumerate(utterances):
        print(f"   {i+1}. {u.text}")
    
    assert len(safety_queue) > 0, "安全队列应该有内容"
    assert "危险" in utterances[0].text, "应包含危险提示"
    
    print("\n\n" + "=" * 80)
    print("Demo 完成！")
    print("=" * 80)
    print("\n说明：")
    print("- 场景 1 验证了安全播报抢占主队列")
    print("- 场景 2-3 验证了安全播报限频机制（2秒内不重复）")
    print("- 场景 4 验证了安全播报跳过时间窗口限制")
    print("- 场景 5 验证了 DecisionCore 直接调用安全播报\n")


if __name__ == "__main__":
    run_demo()

