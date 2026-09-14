"""
Step 8: E2E（端到端）集成测试

模拟真实的导航 30 帧输入 → 导航语音节流 → 只输出合理次数的播报
用于验证整个 v1.4.6d 语音路由链条是否稳定。

测试覆盖：
1. 连续重复导航指令不会疯狂播报
2. 安全提示与导航提示节流独立
3. 节流后恢复逻辑生效
4. 任务链上下文不破坏导航语音行为
5. speech_event → voice_adapter → router → TTS 全链路可运行
"""

import sys
import os
import time
import pytest

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from task_engine.navigation.navigation_voice_adapter import NavigationVoiceAdapter
from task_engine.navigation.navigation_voice_router import NavigationVoiceRouter
from task_engine.tts.routers.time_window_gate import TimeWindowGate
from task_engine.tts import Utterance


# -----------------------------------------
# Step 1：Mock TTS Manager
# -----------------------------------------
class MockTTS:
    """模拟真实 TTS Manager 行为，并做记录"""

    def __init__(self):
        self.history = []
        self.queue = []

    def enqueue(self, utterance):
        """模拟 enqueue 行为"""
        text = utterance.text if hasattr(utterance, 'text') else str(utterance)
        self.history.append(text)
        self.queue.append(utterance)

    def speak(self, text=None, **kwargs):
        """模拟 speak 行为（向后兼容）"""
        self.history.append(text)

    def get_queue(self):
        """获取队列"""
        return self.queue

    def clear(self):
        """清空历史"""
        self.history = []
        self.queue = []


# -----------------------------------------
# Step 2：Mock NavigationEngine（模拟30帧输出）
# -----------------------------------------
class FakeNavigationEngine:
    """
    每一帧给出相同的导航指令：
    TURN_LEFT + 5m + 对应的播报文本
    """

    def __init__(self, decision_text="前方5米左转"):
        self.decision_text = decision_text
        self.frame_count = 0

    def process_frame(self, frame):
        """模拟处理一帧，返回导航结果"""
        self.frame_count += 1
        return {
            "nav_result": {"decision": "LEFT", "distance": 5},
            "speech_event": {
                "text": self.decision_text,
                "decision": "LEFT",
                "priority": 2,
                "category": "navigation",
            },
            "events": [],  # 结构化事件（可选）
        }

    def evaluate(self, scene_graph, movement_state):
        """兼容 NavigationEngineV13 接口"""
        return self.process_frame(None)


# -----------------------------------------
# Step 3：E2E 场景模拟
# -----------------------------------------
def test_e2e_navigation_voice_throttle_30_frames():
    """
    目标：模拟真实导航连续30帧输入
    验证：
        1. NavigationVoiceRouter节流生效（不会疯狂播报30次）
        2. 节流窗口后自动恢复
    """
    mock_tts = MockTTS()

    # 手动注入节流窗口（更严格易测试，窗口大于帧间隔）
    gate = TimeWindowGate(safety_window=0.5, navigation_window=0.5)

    # 使用 Navigation 层的 Router（与 NavigationTask 一致）
    from task_engine.navigation.navigation_voice_router import NavigationVoiceRouter
    from task_engine.tts import tts_manager
    
    # 临时替换全局 tts_manager 的 enqueue 方法
    original_enqueue = tts_manager.enqueue
    tts_manager.enqueue = mock_tts.enqueue
    
    try:
        router = NavigationVoiceRouter(time_window_gate=gate)  # 注入测试用的 gate
        router.reset()

        # 创建 NavigationVoiceAdapter
        adapter = NavigationVoiceAdapter()

        # 创建 Fake NavigationEngine
        fake_engine = FakeNavigationEngine("前方5米左转")

        # 执行 30 帧
        for i in range(30):
            result = fake_engine.process_frame({"frame_id": i})
            speech_event = result.get("speech_event")

            if speech_event:
                # 通过 adapter → router → TTS
                utterances = adapter.handle_speech_event(speech_event)
                router.route_and_speak(utterances)

            # 模拟摄像头帧率：100ms/帧
            time.sleep(0.1)
    finally:
        # 恢复原始 enqueue
        tts_manager.enqueue = original_enqueue

    # -----------------------------------------
    # 验证：节流后播报次数远小于30次
    # 30帧，每0.1秒一帧，窗口0.5秒，理论上最多 30 * 0.1 / 0.5 = 6次
    # 实际由于时间误差，可能略多，但应该远小于30
    # -----------------------------------------
    assert 2 <= len(mock_tts.history) <= 10, \
        f"节流异常，实际播报次数：{len(mock_tts.history)}（应为 2～10 次）"

    # 验证播报内容正确
    assert any("左转" in text for text in mock_tts.history), \
        "播报内容应包含'左转'"


def test_e2e_safety_navigation_independent_streams():
    """
    SAFETY 与 NAVIGATION 节流窗口互不影响。
    """
    mock_tts = MockTTS()
    gate = TimeWindowGate(safety_window=0.3, navigation_window=0.3)
    
    # 使用 TTS Routers 层的 Router（语义化接口）
    from task_engine.tts.routers.navigation_voice_router import NavigationVoiceRouter
    router = NavigationVoiceRouter(tts_manager_instance=mock_tts)
    router.gate = gate
    router.reset()

    # 模拟 NAVIGATION
    router.route_turn("左转", distance=5)
    # NAVIGATION 节流
    router.route_turn("左转", distance=5)

    # SAFETY 不受上一条 NAVIGATION 影响
    router.route_obstacle_warning(direction="前方", distance_m=10)

    assert len(mock_tts.history) == 2, \
        f"节流异常，NAV + SAFETY 应为 2 条，但得到 {len(mock_tts.history)}"

    # 验证内容
    assert any("左转" in text for text in mock_tts.history), \
        "应包含导航播报"
    assert any("障碍物" in text for text in mock_tts.history), \
        "应包含安全播报"


def test_e2e_recover_after_throttle():
    """
    节流后，时间窗口过期 → 播报必须恢复。
    """
    mock_tts = MockTTS()
    gate = TimeWindowGate(safety_window=0.1, navigation_window=0.1)
    
    # 使用 TTS Routers 层的 Router（语义化接口）
    from task_engine.tts.routers.navigation_voice_router import NavigationVoiceRouter
    router = NavigationVoiceRouter(tts_manager_instance=mock_tts)
    router.gate = gate
    router.reset()

    # 第一次：正常执行
    router.route_turn("左转", distance=5)
    assert len(mock_tts.history) == 1

    # 第二次：应被节流
    router.route_turn("左转", distance=5)
    assert len(mock_tts.history) == 1

    # 睡眠超过窗口
    time.sleep(0.12)
    router.route_turn("左转", distance=5)

    assert len(mock_tts.history) == 2, \
        f"节流恢复失败，应为2条，实际={len(mock_tts.history)}"


def test_e2e_full_chain_speech_event_to_tts():
    """
    测试完整链路：speech_event → adapter → router → TTS
    """
    mock_tts = MockTTS()
    gate = TimeWindowGate(safety_window=0.2, navigation_window=0.2)
    
    # 使用 Navigation 层的 Router（与 NavigationTask 一致）
    from task_engine.navigation.navigation_voice_router import NavigationVoiceRouter
    from task_engine.tts import tts_manager
    
    # 临时替换全局 tts_manager 的 enqueue 方法
    original_enqueue = tts_manager.enqueue
    tts_manager.enqueue = mock_tts.enqueue
    
    try:
        router = NavigationVoiceRouter(time_window_gate=gate)
        router.reset()

        adapter = NavigationVoiceAdapter()

        # 模拟多个 speech_event
        speech_events = [
            {"decision": "LEFT", "text": "前方5米左转", "category": "navigation"},
            {"decision": "STOP", "text": "前方有障碍物", "category": "safety"},
            {"decision": "RIGHT", "text": "前方3米右转", "category": "navigation"},
        ]

        for ev in speech_events:
            # speech_event → adapter → router → TTS
            utterances = adapter.handle_speech_event(ev)
            router.route_and_speak(utterances)
            time.sleep(0.05)  # 小延迟
    finally:
        # 恢复原始 enqueue
        tts_manager.enqueue = original_enqueue

    # 验证：由于节流，可能只有部分播报通过
    assert len(mock_tts.history) >= 1, \
        f"至少应有1条播报，实际={len(mock_tts.history)}"
    assert len(mock_tts.history) <= 3, \
        f"由于节流，最多3条播报，实际={len(mock_tts.history)}"


def test_e2e_mixed_safety_and_navigation_stream():
    """
    测试混合的安全和导航播报流，验证节流独立工作
    """
    mock_tts = MockTTS()
    gate = TimeWindowGate(safety_window=0.15, navigation_window=0.15)
    
    # 使用 TTS Routers 层的 Router（语义化接口）
    from task_engine.tts.routers.navigation_voice_router import NavigationVoiceRouter
    router = NavigationVoiceRouter(tts_manager_instance=mock_tts)
    router.gate = gate
    router.reset()

    # 交替播报安全和导航
    router.route_turn("左转", distance=5)      # NAV 1
    router.route_obstacle_warning(direction="前方")  # SAFETY 1
    router.route_turn("右转", distance=3)      # NAV 2（被节流）
    router.route_obstacle_warning(direction="左侧")  # SAFETY 2（被节流）

    # 应该只有前两条通过
    assert len(mock_tts.history) == 2, \
        f"混合流节流异常，应为2条，实际={len(mock_tts.history)}"

    # 等待窗口后
    time.sleep(0.16)
    router.route_turn("直行")                  # NAV 3（恢复）
    router.route_obstacle_warning()             # SAFETY 3（恢复）

    assert len(mock_tts.history) == 4, \
        f"等待窗口后应恢复，应为4条，实际={len(mock_tts.history)}"


def test_e2e_continuous_frames_with_recovery():
    """
    测试连续帧输入，验证节流和恢复的完整周期
    """
    mock_tts = MockTTS()
    gate = TimeWindowGate(safety_window=0.1, navigation_window=0.1)
    
    # 使用 Navigation 层的 Router（与 NavigationTask 一致）
    from task_engine.navigation.navigation_voice_router import NavigationVoiceRouter
    from task_engine.tts import tts_manager
    
    # 临时替换全局 tts_manager 的 enqueue 方法
    original_enqueue = tts_manager.enqueue
    tts_manager.enqueue = mock_tts.enqueue
    
    try:
        router = NavigationVoiceRouter(time_window_gate=gate)
        router.reset()

        adapter = NavigationVoiceAdapter()

        # 模拟连续 20 帧导航指令
        for i in range(20):
            speech_event = {
                "decision": "LEFT",
                "text": f"前方{i}米左转",
                "category": "navigation",
            }
            utterances = adapter.handle_speech_event(speech_event)
            router.route_and_speak(utterances)
            time.sleep(0.05)  # 50ms/帧
    finally:
        # 恢复原始 enqueue
        tts_manager.enqueue = original_enqueue

    # 验证：由于节流，播报次数应该远小于20
    # 窗口0.1秒，每帧0.05秒，理论上每2帧一次，20帧最多10次
    assert 2 <= len(mock_tts.history) <= 12, \
        f"连续帧节流异常，实际播报次数：{len(mock_tts.history)}（应为 2～12 次）"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

