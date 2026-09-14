# -*- coding: utf-8 -*-
"""
A 方案场景测试脚本 - 模拟实际使用场景

用法：
    cd luna_badge_v1_2
    python3 scripts/test_voice_av_scenarios.py

测试场景（共 3 组）：
1. 只播一次导航提示 - 测试导航逻辑是否只播一次
2. 连发两次需要打断的提示 - 测试打断功能在实际场景中的表现
3. 多轮识别+播报混合 - 测试实际使用场景
"""

import logging
import time
import sys
import os

# 添加项目根目录到路径
_script_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.normpath(os.path.join(_script_dir, '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from modules.voice_av import Voice


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger = logging.getLogger("voice_av_scenarios")

    voice = Voice()  # 默认 Ting-Ting 中文女声，语速 180

    logger.info("=" * 60)
    logger.info("A 方案场景测试开始")
    logger.info("Voice 状态: %r", voice.get_status())
    logger.info("=" * 60)
    print("\n" + "=" * 60)
    print("🎤 A 方案场景测试（共 3 组）")
    print("=" * 60 + "\n")

    # ============================================================
    # 场景 1：只播一次导航提示
    # ============================================================
    print("【场景 1/3】只播一次导航提示")
    print("=" * 60)
    print("目的：模拟导航到达场景，验证是否只播报一次")
    print("预期：只听到一次完整的'已到达示例地点附近。'")
    print("-" * 60)
    
    # 模拟导航控制器的逻辑：使用 _arrival_announced 标记
    arrival_announced = False
    last_broadcast_ts = 0.0
    broadcast_interval = 30.0
    
    print("模拟：连续 5 次触发'到达'播报（但应该只播放一次）")
    
    for i in range(5):
        now = time.time()
        print(f"  触发 #{i+1}: 距离 <= 0.5m，到达目标")
        
        # 模拟 navigation_controller 的逻辑
        if not arrival_announced:
            if now - last_broadcast_ts > broadcast_interval:
                print(f"    → 播报：已到达示例地点附近。")
                voice.speak("已到达示例地点附近。")
                last_broadcast_ts = now
                arrival_announced = True
            else:
                print(f"    → 跳过（冷却中，距离上次 {now - last_broadcast_ts:.1f} 秒）")
        else:
            print(f"    → 跳过（已播报过，_arrival_announced=True）")
        
        time.sleep(0.5)  # 快速连续触发
    
    print("\n等待 5 秒，观察是否只播放一次...")
    time.sleep(5)
    print("✅ 场景 1 完成\n")

    # ============================================================
    # 场景 2：连发两次需要打断的提示
    # ============================================================
    print("【场景 2/3】连发两次需要打断的提示")
    print("=" * 60)
    print("目的：测试紧急提示打断普通提示的功能")
    print("预期：前一条长提示被打断，只完整听到后面的紧急提示")
    print("-" * 60)
    
    # 先播放一条长提示
    long_message = "前方 10 米红绿灯，请减速慢行并留意右侧来车，注意观察交通信号灯变化，确保安全通过路口。"
    print(f"发送长提示: {long_message[:30]}...")
    voice.speak(long_message)
    
    # 等待 3 秒（让长提示播放一部分）
    print("等待 3 秒（让长提示播放一部分）...")
    time.sleep(3)
    
    # 发送紧急提示（应该打断上一条）
    urgent_message = "立即停车，前方有障碍物！"
    print(f"发送紧急提示: {urgent_message}")
    print("⚠️  紧急提示应该打断上一条长提示")
    voice.speak(urgent_message)
    
    print("\n等待 5 秒，观察是否只听到紧急提示...")
    time.sleep(5)
    print("✅ 场景 2 完成\n")

    # ============================================================
    # 场景 3：多轮识别+播报混合
    # ============================================================
    print("【场景 3/3】多轮识别+播报混合")
    print("=" * 60)
    print("目的：模拟实际使用场景，测试多轮播报是否正常")
    print("预期：所有播报都能完整播放，不截断、不叠音")
    print("-" * 60)
    
    # 模拟多轮场景播报
    scenarios = [
        ("场景 A", "检测到前方有行人，请注意避让。"),
        ("场景 B", "识别到文字：出口，距离 50 米。"),
        ("场景 C", "当前场景较为空旷，未检测到特殊物体或文字。"),
        ("场景 D", "检测到 3 个物体：椅子、桌子、电脑。"),
        ("场景 E", "识别到 2 个文字：入口、出口。"),
    ]
    
    for name, message in scenarios:
        print(f"\n{name}: {message}")
        # 使用 speak_and_wait() 确保每条播报完整播放
        # 设置超时时间为估算时间的 2 倍（安全余量）
        estimated_time = len(message) * 0.25  # 每字 0.25 秒
        timeout = max(5, estimated_time * 2)  # 至少 5 秒，估算时间的 2 倍
        print(f"  播放并等待完成（超时 {timeout:.1f} 秒，消息长度 {len(message)} 字）...")
        success = voice.speak_and_wait(message, timeout=timeout)
        if success:
            print(f"  ✅ {name} 播放完成")
        else:
            print(f"  ⚠️  {name} 播放超时或失败")
    
    print("\n✅ 场景 3 完成\n")

    # ============================================================
    # 总结
    # ============================================================
    print("=" * 60)
    print("📋 场景测试总结")
    print("=" * 60)
    print("请根据你实际听到的情况，回答以下问题：\n")
    print("【场景 1】只播一次导航提示：")
    print("  - 是否只听到一次'已到达示例地点附近'？ [是/否]")
    print("  - 是否有重复播报？ [有/无]\n")
    
    print("【场景 2】连发两次需要打断的提示：")
    print("  - 长提示是否被成功打断？ [是/否]")
    print("  - 是否只完整听到紧急提示？ [是/否]\n")
    
    print("【场景 3】多轮识别+播报混合：")
    print("  - 所有 5 条播报是否都完整播放？ [是/否]")
    print("  - 是否有播报被截断？ [有/无]")
    print("  - 是否有叠音现象？ [有/无]")
    print("  - 播报顺序是否正确？ [是/否]\n")
    
    print("其他问题：")
    print("- 整体体验如何？ [好/一般/差]")
    print("- 是否有其他异常？ [有/无，如有请描述]")
    print("=" * 60)
    
    logger.info("=" * 60)
    logger.info("A 方案场景测试结束")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()

