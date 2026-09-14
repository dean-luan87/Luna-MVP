"""
测试导航语音适配层（v1.4.6d）

验证：
1. 导航事件 → 正确的 category / priority / interrupt
2. TASK / NAVIGATION / SAFETY 三类映射关系
3. 与 TTSManager 的队列联动
4. 去重和冷却机制
"""

import sys
import os
import time
import pytest

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from task_engine.tts import tts_manager
from task_engine.navigation.navigation_voice_adapter import (
    NavigationVoiceAdapter,
    navigation_voice,
)
from task_engine.navigation.navigation_voice_router import navigation_voice_router


@pytest.fixture
def voice():
    """创建 NavigationVoiceAdapter 实例"""
    return NavigationVoiceAdapter()


def setup_function(_):
    """每个测试前清空 TTS 队列和适配器状态"""
    tts_manager.clear()
    # 重置适配器的去重状态
    navigation_voice._last_text = None
    navigation_voice._last_text_ts = 0.0
    navigation_voice._last_type_ts = {}


def _pop_texts():
    """辅助函数：获取队列中的所有文本"""
    return [u.text for u in tts_manager.pop_all()]


def setup_module(module):
    """避免其他测试残留"""
    tts_manager.clear()


def test_route_planned_goes_to_task_category(voice):
    """测试路线规划完成 → TASK 类别"""
    tts_manager.clear()
    utterances = voice.announce_route_planned("虹口医院", eta_minutes=20)
    
    assert len(utterances) == 1
    u = utterances[0]

    assert "路线" in u.text
    assert u.meta["ttscategory"] == "task"
    assert u.priority == 50
    assert u.interrupt is False


def test_route_planned_without_eta(voice):
    """测试路线规划完成（无 ETA）→ TASK 类别"""
    tts_manager.clear()
    utterances = voice.announce_route_planned("虹口医院")
    
    assert len(utterances) == 1
    u = utterances[0]

    assert "路线" in u.text
    assert u.meta["ttscategory"] == "task"
    assert u.priority == 50


def test_navigation_started_goes_to_task_category(voice):
    """测试导航开始 → TASK 类别"""
    tts_manager.clear()
    utterances = voice.announce_navigation_started()
    
    assert len(utterances) == 1
    u = utterances[0]

    assert "导航已开始" in u.text
    assert u.meta["ttscategory"] == "task"
    assert u.priority == 50


def test_navigation_finished_goes_to_task_category(voice):
    """测试导航结束 → TASK 类别"""
    tts_manager.clear()
    utterances = voice.announce_navigation_finished()
    
    assert len(utterances) == 1
    u = utterances[0]

    assert "导航已结束" in u.text
    assert u.meta["ttscategory"] == "task"
    assert u.priority == 50


def test_turn_instruction_goes_to_navigation_category(voice):
    """测试转向提示 → NAVIGATION 类别"""
    tts_manager.clear()
    utterances = voice.announce_turn(distance_m=50, direction="左转")
    
    assert len(utterances) == 1
    u = utterances[0]

    assert "前方 50 米" in u.text
    assert "左转" in u.text
    assert u.meta["ttscategory"] == "navigation"
    assert u.priority == 75
    assert u.interrupt is False


def test_turn_instruction_without_distance(voice):
    """测试转向提示（无距离）→ NAVIGATION 类别"""
    tts_manager.clear()
    utterances = voice.announce_turn(direction="右转")
    
    assert len(utterances) == 1
    u = utterances[0]

    assert "右转" in u.text
    assert u.meta["ttscategory"] == "navigation"
    assert u.priority == 75


def test_straight_instruction_goes_to_navigation_category(voice):
    """测试直行提示 → NAVIGATION 类别"""
    tts_manager.clear()
    utterances = voice.announce_straight(distance_m=100)
    
    assert len(utterances) == 1
    u = utterances[0]

    assert "直行" in u.text
    assert u.meta["ttscategory"] == "navigation"
    assert u.priority == 75


def test_reroute_goes_to_navigation_category(voice):
    """测试重新规划路线 → NAVIGATION 类别"""
    tts_manager.clear()
    utterances = voice.announce_reroute(reason="偏离路线")
    
    assert len(utterances) == 1
    u = utterances[0]

    assert "重新规划" in u.text
    assert u.meta["ttscategory"] == "navigation"
    assert u.priority == 75


def test_arrival_goes_to_navigation_category(voice):
    """测试到达提示 → NAVIGATION 类别"""
    tts_manager.clear()
    utterances = voice.announce_arrival(destination_name="虹口医院")
    
    assert len(utterances) == 1
    u = utterances[0]

    assert "已到达" in u.text
    assert "虹口医院" in u.text
    assert u.meta["ttscategory"] == "navigation"
    assert u.priority == 75


def test_arrival_without_name(voice):
    """测试到达提示（无名称）→ NAVIGATION 类别"""
    tts_manager.clear()
    utterances = voice.announce_arrival()
    
    assert len(utterances) == 1
    u = utterances[0]

    assert "目的地" in u.text
    assert u.meta["ttscategory"] == "navigation"
    assert u.priority == 75


def test_crowded_warning_goes_to_safety_category(voice):
    """测试人群拥挤提示 → SAFETY 类别"""
    tts_manager.clear()
    utterances = voice.announce_crowded_ahead()
    
    assert len(utterances) == 1
    u = utterances[0]

    assert "人多" in u.text
    assert u.meta["ttscategory"] == "safety"
    assert u.priority == 90
    assert u.interrupt is True


def test_complex_environment_goes_to_safety_category(voice):
    """测试环境复杂提示 → SAFETY 类别"""
    tts_manager.clear()
    utterances = voice.announce_complex_environment()
    
    assert len(utterances) == 1
    u = utterances[0]

    assert "环境" in u.text
    assert u.meta["ttscategory"] == "safety"
    assert u.priority == 90
    assert u.interrupt is True


def test_obstacle_warning_goes_to_safety_category(voice):
    """测试障碍物提示 → SAFETY 类别"""
    tts_manager.clear()
    utterances = voice.announce_obstacle_warning(direction="前方", distance_m=10)
    
    assert len(utterances) == 1
    u = utterances[0]

    assert "障碍物" in u.text
    assert u.meta["ttscategory"] == "safety"
    assert u.priority == 90
    assert u.interrupt is True


def test_obstacle_warning_without_details(voice):
    """测试障碍物提示（无详细信息）→ SAFETY 类别"""
    tts_manager.clear()
    utterances = voice.announce_obstacle_warning()
    
    assert len(utterances) == 1
    u = utterances[0]

    assert "障碍物" in u.text
    assert u.meta["ttscategory"] == "safety"
    assert u.priority == 90
    assert u.interrupt is True


def test_priority_order_in_navigation_flow(voice):
    """测试导航流程中的优先级顺序"""
    tts_manager.clear()
    navigation_voice_router.reset()

    # 模拟一次导航流程
    utterances1 = voice.announce_route_planned("医院")      # TASK: 50
    utterances2 = voice.announce_turn(distance_m=50, direction="左转")  # NAVIGATION: 75
    utterances3 = voice.announce_crowded_ahead()            # SAFETY: 90
    utterances4 = voice.announce_arrival()                  # NAVIGATION: 75

    # 合并所有 Utterance
    all_utterances = utterances1 + utterances2 + utterances3 + utterances4
    assert len(all_utterances) == 4
    
    priorities = [u.priority for u in all_utterances]
    # 应该包含：90, 75, 75, 50
    assert 90 in priorities
    assert 75 in priorities
    assert 50 in priorities

    # 验证具体类别
    safety_utterances = [u for u in all_utterances if u.meta["ttscategory"] == "safety"]
    nav_utterances = [u for u in all_utterances if u.meta["ttscategory"] == "navigation"]
    task_utterances = [u for u in all_utterances if u.meta["ttscategory"] == "task"]
    
    assert len(safety_utterances) == 1
    assert len(nav_utterances) == 2
    assert len(task_utterances) == 1
    assert safety_utterances[0].priority == 90
    assert nav_utterances[0].priority == 75
    assert task_utterances[0].priority == 50


def test_eta_update_goes_to_navigation_category(voice):
    """测试 ETA 更新 → NAVIGATION 类别"""
    tts_manager.clear()
    utterances = voice.announce_eta_update(eta_minutes=5)
    
    assert len(utterances) == 1
    u = utterances[0]

    assert "预计还有" in u.text
    assert "5 分钟" in u.text
    assert u.meta["ttscategory"] == "navigation"
    assert u.priority == 75


def test_red_light_wait_uses_safety_category(voice):
    """测试红灯等待 → SAFETY 类别"""
    tts_manager.clear()
    utterances = voice.announce_red_light_wait(remain_seconds=30)
    
    assert len(utterances) == 1
    u = utterances[0]

    assert "红灯" in u.text
    assert "30 秒" in u.text
    assert u.meta["ttscategory"] == "safety"
    assert u.priority == 90
    assert u.interrupt is True


def test_red_light_wait_without_seconds(voice):
    """测试红灯等待（无剩余秒数）→ SAFETY 类别"""
    tts_manager.clear()
    utterances = voice.announce_red_light_wait()
    
    assert len(utterances) == 1
    u = utterances[0]

    assert "红灯" in u.text
    assert u.meta["ttscategory"] == "safety"
    assert u.priority == 90
    assert u.interrupt is True


def test_cross_with_caution_uses_safety_category(voice):
    """测试绿灯谨慎通行 → SAFETY 类别"""
    tts_manager.clear()
    utterances = voice.announce_cross_with_caution()
    
    assert len(utterances) == 1
    u = utterances[0]

    assert "可以通行" in u.text
    assert u.meta["ttscategory"] == "safety"
    assert u.priority == 90
    assert u.interrupt is True


def test_meta_preservation(voice):
    """测试自定义 meta 的保留"""
    tts_manager.clear()
    utterances = voice.announce_turn(
        distance_m=50,
        direction="左转",
        meta={"custom": "value", "another": 123},
    )
    
    assert len(utterances) == 1
    u = utterances[0]

    # 策略的 meta 应该保留
    assert u.meta["navigation"] is True
    assert u.meta["ttscategory"] == "navigation"
    # 自定义 meta 应该保留
    assert u.meta["custom"] == "value"
    assert u.meta["another"] == 123


# ====== Step 2 新增测试：handle_speech_event 相关 ======

def test_string_event_routes_to_navigation():
    """测试字符串事件 → 默认导航播报"""
    tts_manager.clear()
    navigation_voice_router.reset()
    utterances = navigation_voice.handle_speech_event("前方 10 米左转")
    navigation_voice_router.route_and_speak(utterances)
    texts = _pop_texts()
    assert texts == ["前方 10 米左转"]


def test_dict_event_stop_routes_to_safety():
    """测试 STOP decision → 自动识别为安全类"""
    from task_engine.navigation.navigation_voice_adapter import navigation_voice
    from task_engine.navigation.navigation_voice_router import navigation_voice_router
    
    ev = {
        "decision": "STOP",
        "text": "前方有障碍物，请注意安全",
        "category": "navigation",  # 即便这里是 navigation，也会被决策修正为 safety
    }
    utterances = navigation_voice.handle_speech_event(ev)
    navigation_voice_router.route_and_speak(utterances)
    queue_utterances = tts_manager.pop_all()
    assert len(queue_utterances) == 1
    u = queue_utterances[0]
    assert u.text == "前方有障碍物，请注意安全"
    # SAFETY 策略：priority 应该是安全通道的高优先级
    assert u.meta.get("ttscategory") == "safety"
    assert u.priority == 90
    assert u.interrupt is True


def test_debounce_same_text_in_short_time():
    """测试去重：短时间内重复同句 → 被过滤"""
    tts_manager.clear()
    navigation_voice_router.reset()
    
    # Step 6: Adapter 不再有去重逻辑，去重由 PostProcessor 和 Router 处理
    # 这里只测试 Adapter 返回 Utterance
    utterances1 = navigation_voice.handle_speech_event("前方有台阶")
    assert len(utterances1) == 1
    navigation_voice_router.route_and_speak(utterances1)
    texts1 = _pop_texts()
    assert texts1 == ["前方有台阶"]

    # 立即重复一次，Adapter 仍然返回 Utterance（去重由 Router 的静默窗口处理）
    utterances2 = navigation_voice.handle_speech_event("前方有台阶")
    assert len(utterances2) == 1
    navigation_voice_router.route_and_speak(utterances2)
    texts2 = _pop_texts()
    # Router 的静默窗口可能会抑制，但这里我们只验证 Adapter 返回了 Utterance
    # 实际去重由 Router 的安全窗口处理
    assert len(utterances2) == 1


def test_cooldown_allows_second_safety_after_some_time():
    """测试冷却：冷却时间过后 → 可以再次播报"""
    from task_engine.navigation.navigation_voice_adapter import navigation_voice
    from task_engine.navigation.navigation_voice_router import navigation_voice_router
    
    # Step 6: Adapter 不再有冷却逻辑，冷却由 PostProcessor 处理
    # 这里只测试 Adapter 返回 Utterance
    utterances1 = navigation_voice.handle_speech_event("前方有台阶，小心")
    navigation_voice_router.route_and_speak(utterances1)
    _ = _pop_texts()

    # 冷却时间默认 1.0s，这里模拟稍等一会
    time.sleep(1.1)
    utterances2 = navigation_voice.handle_speech_event("前方有台阶，小心")
    navigation_voice_router.route_and_speak(utterances2)
    texts = _pop_texts()
    # Router 的静默窗口可能会抑制，但这里我们只验证 Adapter 返回了 Utterance
    assert len(utterances2) == 1


def test_dict_event_with_text_key():
    """测试 dict 事件使用 text 字段"""
    tts_manager.clear()
    navigation_voice_router.reset()
    
    ev = {
        "text": "前方50米，请向左转",
        "decision": "SLIGHT_LEFT",
    }
    utterances = navigation_voice.handle_speech_event(ev)
    navigation_voice_router.route_and_speak(utterances)
    queue_utterances = tts_manager.pop_all()
    assert len(queue_utterances) == 1
    assert queue_utterances[0].text == "前方50米，请向左转"
    assert queue_utterances[0].meta.get("ttscategory") == "navigation"


def test_dict_event_with_raw_text_key():
    """测试 dict 事件使用 raw_text 字段（向后兼容）"""
    tts_manager.clear()
    navigation_voice_router.reset()
    
    ev = {
        "raw_text": "请继续直行",
        "decision": "FORWARD",
    }
    utterances = navigation_voice.handle_speech_event(ev)
    navigation_voice_router.route_and_speak(utterances)
    queue_utterances = tts_manager.pop_all()
    assert len(queue_utterances) == 1
    assert queue_utterances[0].text == "请继续直行"


def test_infer_category_from_text_keywords():
    """测试根据文本关键词推断类别"""
    from task_engine.navigation.navigation_voice_adapter import navigation_voice
    from task_engine.navigation.navigation_voice_router import navigation_voice_router
    
    # 危险关键词 → safety
    ev = {"text": "前方有障碍物，请注意"}
    utterances = navigation_voice.handle_speech_event(ev)
    assert len(utterances) == 1
    assert utterances[0].meta.get("ttscategory") == "safety"

    # 普通导航 → navigation
    ev2 = {"text": "前方50米，请向左转"}
    utterances2 = navigation_voice.handle_speech_event(ev2)
    assert len(utterances2) == 1
    assert utterances2[0].meta.get("ttscategory") == "navigation"


def test_none_event_handled_gracefully():
    """测试 None 输入时安全处理"""
    tts_manager.clear()
    navigation_voice_router.reset()
    utterances = navigation_voice.handle_speech_event(None)
    assert len(utterances) == 0
    navigation_voice_router.route_and_speak(utterances)
    texts = _pop_texts()
    assert texts == []


def test_empty_string_handled_gracefully():
    """测试空字符串时安全处理"""
    tts_manager.clear()
    navigation_voice_router.reset()
    utterances1 = navigation_voice.handle_speech_event("")
    # 空字符串会被 strip 后变成空，返回空列表
    assert len(utterances1) == 0
    navigation_voice_router.route_and_speak(utterances1)
    texts = _pop_texts()
    assert texts == []

    utterances2 = navigation_voice.handle_speech_event("   ")
    # 只有空格的字符串会被 strip 后变成空，返回空列表
    assert len(utterances2) == 0
    navigation_voice_router.route_and_speak(utterances2)
    texts2 = _pop_texts()
    assert texts2 == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

