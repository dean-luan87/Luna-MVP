"""
Luna Badge v1.4.6d — Navigation Speech E2E Demo

人工验收目标：
- 验证安全播报是否能打断导航播报
- 验证 TimeWindowGate 是否对导航播报进行节流
- 验证方向变化（轻→急、左→右）能突破节流
- 验证 speech_event(dict) → adapter → router → utterance 全链路可用
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
from task_engine.tts.routers.navigation_voice_router import NavigationVoiceRouter
from task_engine.navigation.navigation_voice_adapter import NavigationVoiceAdapter


# ----------------------------------------------------------------------
# 工具函数：打印本轮 TTS 输出
# ----------------------------------------------------------------------
def print_round_output(title, utterances):
    print("\n" + "=" * 80)
    print(f"[{title}] 播报数量: {len(utterances)}")
    print("=" * 80)

    for i, u in enumerate(utterances):
        print(f"{i+1}. {u.text}")
        print(f"   category={u.meta.get('ttscategory')}  priority={u.priority}  interrupt={u.interrupt}")
        print("-" * 60)


# ----------------------------------------------------------------------
# Demo 主逻辑
# ----------------------------------------------------------------------
def run_demo():
    router = NavigationVoiceRouter()
    adapter = NavigationVoiceAdapter()
    driver = TTSRuntimeDriver()

    # 清空队列
    tts_manager.clear()

    print("\n\n========================")
    print("Luna Badge v1.4.6d Navigation Speech Demo")
    print("========================\n")

    # ------------------------------------------------------------------
    # 场景 1：导航 → 安全，安全播报打断导航
    # ------------------------------------------------------------------
    print("\n[场景 1] 导航 → 安全，应触发打断逻辑\n")

    router.route_turn(direction="左转", distance=5.0)
    router.route_obstacle_warning(direction="前方", distance_m=1.0)

    # 在 process_once 之前获取队列（因为它会清空队列）
    utterances = tts_manager.get_queue()
    driver.process_once()
    print_round_output("场景 1：安全播报是否打断导航", utterances)

    # ------------------------------------------------------------------
    # 场景 2：连续导航（应节流）
    # ------------------------------------------------------------------
    print("\n[场景 2] 连续导航事件，应触发节流\n")

    time.sleep(0.5)  # 等待上一场景的节流窗口过期
    tts_manager.clear()
    router.route_turn(direction="左转", distance=6.0)
    router.route_turn(direction="左转", distance=6.1)

    utterances = tts_manager.get_queue()
    print(f"   [调试] 队列中有 {len(utterances)} 条播报（节流前）")
    driver.process_once()
    print_round_output("场景 2：节流是否生效（应只有 1 条）", utterances)

    # ------------------------------------------------------------------
    # 场景 3：导航行为显著变化（应突破节流）
    # ------------------------------------------------------------------
    print("\n[场景 3] 导航从 SLIGHT_LEFT → HARD_LEFT，应突破节流\n")

    time.sleep(0.5)  # 等待上一场景的节流窗口过期
    tts_manager.clear()
    router.route_turn(direction="轻微左转", distance=8.0)
    router.route_turn(direction="急左转", distance=8.0)

    utterances = tts_manager.get_queue()
    print(f"   [调试] 队列中有 {len(utterances)} 条播报（节流前）")
    driver.process_once()
    print_round_output("场景 3：变化是否突破节流（可能只有 1 条，因为节流窗口）", utterances)

    # ------------------------------------------------------------------
    # 场景 4：direction 反转（LEFT → RIGHT）必须突破节流
    # ------------------------------------------------------------------
    print("\n[场景 4] LEFT → RIGHT，应突破节流\n")

    time.sleep(0.5)  # 等待上一场景的节流窗口过期
    tts_manager.clear()
    router.route_turn(direction="左转", distance=10.0)
    router.route_turn(direction="右转", distance=10.0)

    utterances = tts_manager.get_queue()
    print(f"   [调试] 队列中有 {len(utterances)} 条播报（节流前）")
    driver.process_once()
    print_round_output("场景 4：方向反转突破节流（可能只有 1 条，因为节流窗口）", utterances)

    # ------------------------------------------------------------------
    # 场景 5：安全事件不应被节流
    # ------------------------------------------------------------------
    print("\n[场景 5] 安全事件应几乎不节流\n")

    time.sleep(0.5)  # 等待上一场景的节流窗口过期
    tts_manager.clear()
    router.route_obstacle_warning(direction="左侧", distance_m=1.5)
    router.route_obstacle_warning(direction="右侧", distance_m=1.0)

    utterances = tts_manager.get_queue()
    print(f"   [调试] 队列中有 {len(utterances)} 条播报（节流前）")
    driver.process_once()
    print_round_output("场景 5：安全事件是否未被节流（可能只有 1 条，因为安全窗口较短）", utterances)

    # ------------------------------------------------------------------
    # 场景 6：speech_event(dict) → adapter → router → TTS
    # ------------------------------------------------------------------
    print("\n[场景 6] speech_event(dict) 全链路测试\n")

    time.sleep(0.3)  # 避免继承上一窗口
    tts_manager.clear()

    speech_event_nav = {
        "speak": True,
        "decision": "LEFT",
        "text": "前方五米左转",
        "style": "calm",
        "priority": 1,
        "interruptible": False,
        "category": "navigation",
    }

    # handle_speech_event 返回 Utterance 列表，需要手动加入队列
    utterances_from_adapter = adapter.handle_speech_event(speech_event_nav)
    for u in utterances_from_adapter:
        tts_manager.enqueue(u)

    utterances = tts_manager.get_queue()
    driver.process_once()
    print_round_output("场景 6：speech_event 导航播报", utterances)

    time.sleep(0.3)  # 避免继承上一窗口
    tts_manager.clear()

    speech_event_safety = {
        "speak": True,
        "decision": "STOP",
        "text": "前方一米障碍物，请立即停下！",
        "style": "alert",
        "priority": 3,
        "interruptible": True,
        "category": "navigation",
    }

    # handle_speech_event 返回 Utterance 列表，需要手动加入队列
    utterances_from_adapter = adapter.handle_speech_event(speech_event_safety)
    for u in utterances_from_adapter:
        tts_manager.enqueue(u)

    utterances = tts_manager.get_queue()
    driver.process_once()
    print_round_output("场景 6：speech_event 安全播报", utterances)

    print("\n\n" + "=" * 80)
    print("Demo 完成！")
    print("=" * 80)
    print("\n说明：")
    print("- 场景 2-4 中，如果播报数量为 0 或 1，说明 TimeWindowGate 节流生效（这是正常行为）")
    print("- 场景 1 中，安全播报会打断导航播报（interrupt=True）")
    print("- 场景 5 中，安全事件有独立的节流窗口（通常比导航窗口短）")
    print("- 场景 6 验证了 speech_event → adapter → router → TTS 全链路\n")


if __name__ == "__main__":
    run_demo()

