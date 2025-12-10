"""
Luna Badge v1.4.6d Step 12 — PriorityScheduler Demo

验证优先级调度器（PriorityScheduler）功能
"""

import sys
import os

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from task_engine.tts import tts_manager, Utterance
from task_engine.tts.runtime_driver import TTSRuntimeDriver
from task_engine.tts.priority_bands import PriorityBand
from task_engine.tts.tts_policy import TTSCategory, make_utterance


def run_demo():
    """运行 Step 12 Demo"""
    
    # 初始化组件
    tts_manager.clear()
    driver = TTSRuntimeDriver()
    
    print("\n\n" + "=" * 80)
    print("Luna Badge v1.4.6d Step 12 — PriorityScheduler Demo")
    print("=" * 80 + "\n")
    
    # ------------------------------------------------------------------
    # 场景 1：验证 PriorityBand 映射
    # ------------------------------------------------------------------
    print("\n[场景 1] 验证 PriorityBand 映射\n")
    
    test_cases = [
        (100, PriorityBand.P0_SAFETY),
        (90, PriorityBand.P0_SAFETY),
        (85, PriorityBand.P1_NAV),
        (75, PriorityBand.P1_NAV),
        (50, PriorityBand.P2_TASK),
        (40, PriorityBand.P2_TASK),
        (25, PriorityBand.P3_CHAT),
        (0, PriorityBand.P3_CHAT),
    ]
    
    for priority, expected_band in test_cases:
        band = PriorityBand.from_priority(priority)
        status = "✅" if band == expected_band else "❌"
        print(f"   {status} priority={priority:3d} → {band.name} (期望: {expected_band.name})")
        assert band == expected_band, f"Priority {priority} should map to {expected_band.name}"
    
    # ------------------------------------------------------------------
    # 场景 2：安全队列优先于主队列
    # ------------------------------------------------------------------
    print("\n[场景 2] 安全队列优先于主队列\n")
    
    tts_manager.clear()
    
    # 先加入主队列（高优先级导航）
    nav_utter = make_utterance("前方5米左转", TTSCategory.NAVIGATION)
    tts_manager.enqueue(nav_utter)
    
    # 然后加入安全队列
    safety_utter = make_utterance("前方危险，请立即停下", TTSCategory.SAFETY)
    tts_manager.push_safety(safety_utter)
    
    # 使用 pop_next() 获取下一条
    first = tts_manager.pop_next()
    print(f"   第一条播报: {first.text} (band={PriorityBand.from_priority(first.priority).name})")
    assert first.text == "前方危险，请立即停下", "安全播报应该优先"
    
    second = tts_manager.pop_next()
    print(f"   第二条播报: {second.text} (band={PriorityBand.from_priority(second.priority).name})")
    assert second.text == "前方5米左转", "导航播报应该在安全播报之后"
    
    # ------------------------------------------------------------------
    # 场景 3：主队列内按 Band 排序（P1 > P2 > P3）
    # ------------------------------------------------------------------
    print("\n[场景 3] 主队列内按 Band 排序（P1 > P2 > P3）\n")
    
    tts_manager.clear()
    
    # 加入不同 band 的播报（乱序）
    chat_utter = make_utterance("今天天气不错", TTSCategory.CHAT)  # P3
    task_utter = make_utterance("任务已完成", TTSCategory.TASK)     # P2
    nav_utter = make_utterance("前方10米直行", TTSCategory.NAVIGATION)  # P1
    
    tts_manager.enqueue(chat_utter)
    tts_manager.enqueue(task_utter)
    tts_manager.enqueue(nav_utter)
    
    # 应该按 P1 > P2 > P3 顺序输出
    first = tts_manager.pop_next()
    print(f"   第一条: {first.text} (band={PriorityBand.from_priority(first.priority).name})")
    assert first.text == "前方10米直行", "P1 导航应该最先"
    
    second = tts_manager.pop_next()
    print(f"   第二条: {second.text} (band={PriorityBand.from_priority(second.priority).name})")
    assert second.text == "任务已完成", "P2 任务应该在 P1 之后"
    
    third = tts_manager.pop_next()
    print(f"   第三条: {third.text} (band={PriorityBand.from_priority(third.priority).name})")
    assert third.text == "今天天气不错", "P3 闲聊应该在最后"
    
    # ------------------------------------------------------------------
    # 场景 4：同 Band 内按 Priority 排序
    # ------------------------------------------------------------------
    print("\n[场景 4] 同 Band 内按 Priority 排序\n")
    
    tts_manager.clear()
    
    # 同是 P1 (NAV)，但 priority 不同
    nav_low = Utterance(text="导航低优先级", priority=70, level="info")
    nav_high = Utterance(text="导航高优先级", priority=85, level="info")
    
    tts_manager.enqueue(nav_low)
    tts_manager.enqueue(nav_high)
    
    first = tts_manager.pop_next()
    print(f"   第一条: {first.text} (priority={first.priority})")
    assert first.text == "导航高优先级", "高 priority 应该先出"
    
    second = tts_manager.pop_next()
    print(f"   第二条: {second.text} (priority={second.priority})")
    assert second.text == "导航低优先级", "低 priority 应该后出"
    
    # ------------------------------------------------------------------
    # 场景 5：TTSRuntimeDriver 使用 pop_next() 逐条播报
    # ------------------------------------------------------------------
    print("\n[场景 5] TTSRuntimeDriver 使用 pop_next() 逐条播报\n")
    
    tts_manager.clear()
    
    # 加入多条播报
    tts_manager.enqueue(make_utterance("闲聊1", TTSCategory.CHAT))
    tts_manager.enqueue(make_utterance("任务1", TTSCategory.TASK))
    tts_manager.enqueue(make_utterance("导航1", TTSCategory.NAVIGATION))
    tts_manager.push_safety(make_utterance("安全1", TTSCategory.SAFETY))
    
    print("   播报顺序（应优先安全，然后按 P1 > P2 > P3）:")
    for i in range(4):
        driver.process_once()
        if not tts_manager.get_queue() and not tts_manager.get_safety_queue():
            break
    
    print("\n\n" + "=" * 80)
    print("Demo 完成！")
    print("=" * 80)
    print("\n说明：")
    print("- 场景 1 验证了 PriorityBand 映射规则")
    print("- 场景 2 验证了安全队列优先于主队列")
    print("- 场景 3 验证了主队列内按 Band 排序（P1 > P2 > P3）")
    print("- 场景 4 验证了同 Band 内按 Priority 排序")
    print("- 场景 5 验证了 TTSRuntimeDriver 使用 pop_next() 逐条播报\n")


if __name__ == "__main__":
    run_demo()

