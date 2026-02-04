"""
EmergencyVoiceLayer / TTS 行为测试：
- 对应 QA 清单中的 EV-01 / EV-02 / EV-03
- 通过 monkeypatch TTSManager.speak 捕获调用次数，验证节流逻辑
"""
import time
import pytest

from core.failsafe.emergency_voice import EmergencyVoiceLayer


class FakeTTSManager:
    """模拟 TTSManager，用于捕获调用"""
    calls = []

    @classmethod
    def speak(cls, text: str):
        cls.calls.append(text)


@pytest.fixture(autouse=True)
def patch_tts_manager(monkeypatch):
    """将 EmergencyVoiceLayer 内部引用替换为 FakeTTSManager"""
    import core.failsafe.emergency_voice as ev_module
    monkeypatch.setattr(ev_module, "TTSManager", FakeTTSManager)
    monkeypatch.setattr(ev_module, "TTS_AVAILABLE", True)
    FakeTTSManager.calls = []
    yield
    FakeTTSManager.calls = []


def test_emergency_voice_single_play():
    """
    测试单次播报
    
    对应 QA 清单：EV-01
    """
    ev = EmergencyVoiceLayer.get_instance()
    ev.min_interval = 2  # 缩短节流间隔，便于测试
    ev.last_play_ts = 0

    ev.play("测试播报")
    
    assert len(FakeTTSManager.calls) == 1, "Should call TTS once"


def test_emergency_voice_throttle():
    """
    测试节流机制
    
    对应 QA 清单：EV-02
    """
    ev = EmergencyVoiceLayer.get_instance()
    ev.min_interval = 2
    ev.last_play_ts = 0
    FakeTTSManager.calls = []

    ev.play("第一次")
    ev.play("第二次（短间隔）")
    
    assert len(FakeTTSManager.calls) == 1, "Within min_interval, should only play once"

    time.sleep(2.1)
    ev.play("第三次（超过间隔）")
    
    assert len(FakeTTSManager.calls) == 2, "After interval, play again"


def test_emergency_voice_no_tts_manager(monkeypatch):
    """
    验证 TTSManager 不存在时不抛异常
    
    对应 QA 清单：EV-03
    """
    import core.failsafe.emergency_voice as ev_module
    monkeypatch.setattr(ev_module, "TTSManager", None)
    monkeypatch.setattr(ev_module, "TTS_AVAILABLE", False)

    ev = EmergencyVoiceLayer.get_instance()
    ev.min_interval = 1
    ev.last_play_ts = 0

    # 不应抛异常
    try:
        ev.play("无 TTS 场景")
        assert True, "Should not throw exception when TTSManager is None"
    except Exception as e:
        pytest.fail(f"Should not throw exception when TTSManager is None: {e}")
















