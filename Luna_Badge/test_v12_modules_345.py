"""
Luna Badge v1.2 - 模块3、4、5完整测试脚本
"""
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.luna_usage_guide import LunaUsageGuide, run_interactive_guide
from core.hardware_identity_logger import HardwareIdentityLogger, demo_hardware_logger
from core.network_connection_strategy import NetworkConnectionStrategy, demo_network_strategy


def main():
    """主测试函数"""
    print("=" * 70)
    print("Luna Badge v1.2 - 模块3、4、5测试")
    print("=" * 70)
    
    print("\n请选择要测试的模块：")
    print("1) 模块3：Luna产品语音引导系统")
    print("2) 模块4：硬件编码记录机制")
    print("3) 模块5：联网机制设计")
    print("4) 全部测试")
    print("0) 退出")
    
    while True:
        choice = input("\n请输入选项（0-4）: ").strip()
        
        if choice == "0":
            print("退出测试")
            break
        elif choice == "1":
            test_module3()
        elif choice == "2":
            test_module4()
        elif choice == "3":
            test_module5()
        elif choice == "4":
            test_all_modules()
        else:
            print("无效选项，请重新输入")


def test_module3():
    """测试模块3：Luna产品语音引导系统"""
    print("\n" + "=" * 70)
    print("模块3：Luna产品语音引导系统")
    print("=" * 70)
    
    guide = LunaUsageGuide()
    
    # 测试各种引导
    triggers = ["intro", "how_to_navigate", "how_to_remind", "help"]
    
    for trigger in triggers:
        print(f"\n--- {trigger} ---")
        guides = guide.luna_usage_guide(trigger)
        for line in guides:
            print(f"Luna: {line}")
    
    # 交互式测试
    print("\n是否进入交互式测试？(y/n)")
    if input().strip().lower() == 'y':
        run_interactive_guide()


def test_module4():
    """测试模块4：硬件编码记录机制"""
    demo_hardware_logger()


def test_module5():
    """测试模块5：联网机制设计"""
    print("\n" + "=" * 70)
    print("模块5：联网机制设计")
    print("=" * 70)
    
    demo_network_strategy()


def test_all_modules():
    """测试所有模块"""
    print("\n开始全部模块测试...\n")
    
    test_module3()
    input("\n按Enter继续测试模块4...")
    
    test_module4()
    input("\n按Enter继续测试模块5...")
    
    test_module5()
    
    print("\n" + "=" * 70)
    print("全部模块测试完成！")
    print("=" * 70)


if __name__ == "__main__":
    main()

