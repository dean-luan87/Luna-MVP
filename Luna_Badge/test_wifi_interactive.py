"""
Luna Badge v1.5 - WiFi语音配网交互式测试
"""
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.voice_wifi_setup import VoiceWiFiSetup
from core.tts_manager import speak


def test_interactive_wifi_setup():
    """测试交互式WiFi配网"""
    print("=" * 70)
    print("Luna Badge v1.5 - 交互式WiFi配网测试")
    print("=" * 70)
    
    wifi_setup = VoiceWiFiSetup()
    
    # 1. 扫描WiFi
    print("\n[1/4] 扫描WiFi网络...")
    speak("正在扫描WiFi网络")
    wifi_list = wifi_setup.voice_scan_wifi()
    
    if not wifi_list:
        print("未找到WiFi网络")
        return
    
    print(f"✓ 找到 {len(wifi_list)} 个WiFi网络")
    
    # 2. 用户选择WiFi
    print("\n[2/4] 请选择WiFi...")
    speak("请告诉我你想连接哪一个，可以说第几个或者WiFi名称")
    
    # 交互式输入（实际应该是语音识别）
    while True:
        user_input = input("你的选择 (数字/名称): ").strip()
        
        if not user_input:
            continue
        
        # 解析选择
        selected = wifi_setup._parse_user_selection(user_input)
        
        if selected:
            print(f"✓ 你选择了: {selected['ssid']}")
            speak(f"你选择了{selected['ssid']}")
            break
        else:
            print("✗ 未找到匹配的WiFi，请重新输入")
            speak("未找到，请重新选择")
    
    # 3. 输入密码
    print(f"\n[3/4] 请输入 {selected['ssid']} 的密码...")
    speak(f"请告诉我{selected['ssid']}的密码")
    
    password = input("WiFi密码: ").strip()
    
    # 4. 连接
    print(f"\n[4/4] 正在连接...")
    result = wifi_setup.voice_input_wifi_password(selected['ssid'], password)
    
    if result['success']:
        print("\n✓ WiFi配置成功！")
        speak("连接成功")
    else:
        print(f"\n✗ 连接失败: {result['message']}")
        speak("连接失败")


def test_fuzzy_search():
    """测试模糊搜索"""
    print("\n" + "=" * 70)
    print("模糊搜索测试")
    print("=" * 70)
    
    wifi_setup = VoiceWiFiSetup()
    wifi_setup.scanned_wifi_list = [
        {'ssid': 'Home_WiFi', 'signal_strength': -45},
        {'ssid': 'Office_Network', 'signal_strength': -68},
        {'ssid': 'Public_WiFi', 'signal_strength': -85},
        {'ssid': 'MyHome_2.4G', 'signal_strength': -52},
        {'ssid': 'Family_WiFi', 'signal_strength': -55}
    ]
    
    test_cases = [
        "Home",      # 部分匹配
        "WiFi",      # 多个匹配
        "Office",    # 完全匹配
        "家庭",       # 无匹配
        "1"          # 数字选择
    ]
    
    for keyword in test_cases:
        print(f"\n搜索: '{keyword}'")
        matches = wifi_setup._fuzzy_search_wifi(keyword)
        
        if matches:
            print(f"  找到 {len(matches)} 个匹配:")
            for wifi in matches:
                print(f"    - {wifi['ssid']}")
        else:
            print("  未找到匹配")


def main():
    """主函数"""
    print("请选择测试:")
    print("1) 交互式WiFi配网")
    print("2) 模糊搜索测试")
    print("3) 全部测试")
    
    choice = input("\n请输入选项 (1-3): ").strip()
    
    if choice == "1":
        test_interactive_wifi_setup()
    elif choice == "2":
        test_fuzzy_search()
    elif choice == "3":
        test_fuzzy_search()
        test_interactive_wifi_setup()
    else:
        print("无效选项")


if __name__ == "__main__":
    main()

