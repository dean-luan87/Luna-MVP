"""
Luna Badge v1.5/v1.6 - 非交互式自动测试
"""
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def test_verification_code():
    """测试验证码功能"""
    print("\n" + "=" * 70)
    print("测试1: 验证码语音输入与反馈")
    print("=" * 70)
    
    try:
        from core.voice_verification_code import VoiceVerificationCodeHandler
        
        handler = VoiceVerificationCodeHandler()
        phone = "13800138000"
        
        # 发送验证码
        print("\n1. 发送验证码...")
        result = handler.voice_send_verification_code(phone)
        print(f"   ✓ {result['message']}")
        
        # 转换中文数字
        print("\n2. 测试中文数字转换...")
        test_cases = ["一二三四五六", "123456", "一 二 三 四 五 六"]
        for test in test_cases:
            code = handler._convert_chinese_numbers_to_digits(test)
            print(f"   '{test}' → '{code}'")
        
        print("\n   ✅ 验证码模块测试通过")
        
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        import traceback
        traceback.print_exc()


def test_wifi_setup():
    """测试WiFi配网"""
    print("\n" + "=" * 70)
    print("测试2: WiFi语音扫描和配网")
    print("=" * 70)
    
    try:
        from core.voice_wifi_setup import VoiceWiFiSetup
        
        wifi_setup = VoiceWiFiSetup()
        
        # 扫描WiFi
        print("\n1. 扫描WiFi网络...")
        wifi_list = wifi_setup.voice_scan_wifi()
        print(f"   ✓ 找到 {len(wifi_list)} 个WiFi网络")
        
        if wifi_list:
            print(f"   ✓ 第1个WiFi: {wifi_list[0]['ssid']}")
        
        # 信号强度转换
        print("\n2. 测试信号强度转换...")
        test_signals = [-45, -60, -70, -80, -85]
        for signal in test_signals:
            text = wifi_setup._signal_to_text(signal)
            print(f"   {signal} dBm → '{text}'")
        
        print("\n   ✅ WiFi模块测试通过")
        
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        import traceback
        traceback.print_exc()


def test_wakeup_manager():
    """测试唤醒管理"""
    print("\n" + "=" * 70)
    print("测试3: 语音唤醒与待机管理")
    print("=" * 70)
    
    try:
        from core.voice_wakeup_manager import VoiceWakeupManager, SystemState
        
        manager = VoiceWakeupManager()
        
        # 测试状态切换
        print("\n1. 测试状态切换...")
        
        current = manager.get_current_state()
        print(f"   初始状态: {current}")
        
        manager.enter_active_mode()
        print(f"   活跃状态: {manager.get_current_state()}")
        
        manager.enter_idle_mode()
        print(f"   空闲状态: {manager.get_current_state()}")
        
        manager.enter_sleep_mode()
        print(f"   待机状态: {manager.get_current_state()}")
        
        print("\n2. 测试状态检查...")
        manager.enter_active_mode()
        is_ready = manager.is_ready()
        print(f"   系统准备就绪: {is_ready}")
        
        print("\n   ✅ 唤醒管理模块测试通过")
        
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        import traceback
        traceback.print_exc()


def main():
    """主函数"""
    print("=" * 70)
    print("Luna Badge v1.5/v1.6 语音交互功能测试")
    print("=" * 70)
    
    # 运行所有测试
    test_verification_code()
    test_wifi_setup()
    test_wakeup_manager()
    
    print("\n" + "=" * 70)
    print("✅ 所有测试完成")
    print("=" * 70)


if __name__ == "__main__":
    main()

