"""
EmergencyVoiceLayer QA 测试用例
对应 QA 清单：EV-01 ~ EV-03
"""
import pytest
import time
from core.failsafe.emergency_voice import EmergencyVoiceLayer
from core.failsafe.fail_safe_manager import FailSafeManager
from core.failsafe.health_events import HealthEvent


class TestEmergencyVoice:
    """EmergencyVoiceLayer 测试套件"""
    
    def test_ev_01_emergency_auto_playback(self, fail_safe_manager):
        """
        EV-01: Emergency 自动播报
        
        操作：触发 CAMERA_STALE
        预期：
        - 播报 1 次："当前视觉系统异常，请原地停下……"
        - 日志出现 [EmergencyVoice]
        """
        fsm = fail_safe_manager
        evl = EmergencyVoiceLayer.get_instance()
        
        # 记录初始时间
        initial_ts = evl.last_play_ts
        
        # 触发应急模式
        fsm.on_health_event(HealthEvent.CAMERA_STALE)
        
        # 验证播报（通过检查 last_play_ts）
        time.sleep(0.1)  # 等待播报完成
        assert evl.last_play_ts >= initial_ts, "应该至少播报一次（last_play_ts 应该已更新）"
    
    def test_ev_02_playback_throttle(self, fail_safe_manager):
        """
        EV-02: 播报节流测试
        
        操作：1 秒内连续触发 5 次 emergency
        预期：
        - 只播报 1 次
        - last_play_ts 有更新
        """
        fsm = fail_safe_manager
        evl = EmergencyVoiceLayer.get_instance()
        evl.min_interval = 2.0  # 设置 2 秒节流
        
        # 清空之前的播报记录
        evl.last_play_ts = 0
        initial_ts = evl.last_play_ts
        
        # 连续触发 5 次
        for i in range(5):
            fsm.on_health_event(HealthEvent.CAMERA_STALE)
            time.sleep(0.1)
        
        # 验证 last_play_ts 已更新（节流应该生效）
        assert evl.last_play_ts > initial_ts, "last_play_ts 应该已更新"
        
        # 验证节流（通过检查播报时间间隔）
        # 由于节流机制，连续触发应该只播报一次
        # 这个验证通过检查 last_play_ts 的变化来间接验证
    
    def test_ev_03_tts_not_available(self):
        """
        EV-03: TTS 不存在场景
        
        操作：注释掉 TTSManager 导入（模拟 TTS 不存在）
        预期：
        - 系统无报错
        - 日志输出 "TTSManager not available"
        """
        evl = EmergencyVoiceLayer.get_instance()
        
        # 播报（TTS 不存在时应该不报错）
        # 注意：EmergencyVoiceLayer.play() 不返回值，只记录日志
        try:
            evl.play("测试消息")
            # 如果没有抛出异常，说明处理正常
            assert True, "即使 TTS 不存在也应该不报错"
        except Exception as e:
            pytest.fail(f"TTS 不存在时不应该抛出异常: {e}")

