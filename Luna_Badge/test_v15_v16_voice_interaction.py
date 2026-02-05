"""
Luna Badge v1.5/v1.6 - 完整语音交互测试
"""
import sys
import os
import asyncio

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.voice_verification_code import VoiceVerificationCodeHandler, handle_voice_verification_command
from core.voice_wifi_setup import VoiceWiFiSetup
from core.voice_wakeup_manager import VoiceWakeupManager, setup_wakeup_manager


def test_verification_code():
    """测试验证码语音交互"""
    print("\n" + "=" * 70)
    print("v1.5 测试：验证码语音输入与反馈")
    print("=" * 70)
    
    handler = VoiceVerificationCodeHandler()
    
    phone = "13800138000"
    
    # 1. 发送验证码
    print("\n1. 发送验证码...")
    result = handler.voice_send_verification_code(phone)
    print(f"结果: {result['message']}")
    
    # 2. 语音输入验证码（模拟）
    print("\n2. 语音输入验证码...")
    speech = "一二三四五六"  # 模拟用户说的验证码
    result = handler.voice_input_verification_code(phone, speech)
    print(f"输入: {speech} → {result.get('code', 'N/A')}")
    print(f"结果: {result['message']}")
    
    # 3. 再次发送验证码
    print("\n3. 再次发送验证码...")
    result = handler.voice_resend_verification_code(phone)
    print(f"结果: {result['message']}")


def test_wifi_setup():
    """测试WiFi语音配网"""
    print("\n" + "=" * 70)
    print("v1.5 测试：WiFi语音扫描和配网")
    print("=" * 70)
    
    wifi_setup = VoiceWiFiSetup()
    
    # 1. 扫描WiFi
    print("\n1. 扫描WiFi网络...")
    wifi_list = wifi_setup.voice_scan_wifi()
    print(f"找到 {len(wifi_list)} 个WiFi网络")
    
    # 2. 选择WiFi
    print("\n2. 选择WiFi...")
    selected = wifi_setup.voice_select_wifi("Home_WiFi", user_number=1)
    if selected:
        print(f"选择的WiFi: {selected['ssid']}")
    
    # 3. 输入密码并连接
    print("\n3. 输入密码并连接...")
    if selected:
        # 模拟语音输入的密码
        result = wifi_setup.voice_input_wifi_password(selected['ssid'], "12345678")
        print(f"结果: {result['message']}")


async def test_wakeup():
    """测试语音唤醒和待机"""
    print("\n" + "=" * 70)
    print("v1.6 测试：语音唤醒与待机管理")
    print("=" * 70)
    
    manager = setup_wakeup_manager()
    
    # 添加唤醒回调
    async def on_wakeup(wake_word: str):
        print(f"\n🎉 唤醒检测: {wake_word}")
        speak("你好，我在这里")
        manager.enter_idle_mode()
        await asyncio.sleep(2)
        manager.enter_sleep_mode()
    
    manager.add_wakeup_callback(on_wakeup)
    
    print("\n系统状态管理测试：")
    print("1. 当前状态:", manager.get_current_state())
    
    manager.enter_active_mode()
    print("2. 进入活跃状态:", manager.get_current_state())
    
    manager.enter_idle_mode()
    print("3. 进入空闲状态:", manager.get_current_state())
    
    manager.enter_sleep_mode()
    print("4. 进入待机状态:", manager.get_current_state())
    
    print("\n✓ 状态切换测试完成")


def main():
    """主测试函数"""
    print("=" * 70)
    print("Luna Badge v1.5/v1.6 语音交互增强功能测试")
    print("=" * 70)
    
    print("\n请选择测试内容：")
    print("1) v1.5: 验证码语音输入与反馈")
    print("2) v1.5: WiFi语音扫描和配网")
    print("3) v1.6: 语音唤醒与待机管理")
    print("4) 全部测试")
    
    choice = input("\n请输入选项（1-4）: ").strip()
    
    if choice == "1":
        test_verification_code()
    elif choice == "2":
        test_wifi_setup()
    elif choice == "3":
        asyncio.run(test_wakeup())
    elif choice == "4":
        test_verification_code()
        test_wifi_setup()
        asyncio.run(test_wakeup())
    else:
        print("无效选项")
    
    print("\n" + "=" * 70)
    print("测试完成")
    print("=" * 70)


if __name__ == "__main__":
    main()

