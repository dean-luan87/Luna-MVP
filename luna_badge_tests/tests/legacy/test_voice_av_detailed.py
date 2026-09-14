# -*- coding: utf-8 -*-
"""
A 方案详细测试脚本 - 带编号和测试说明

用法：
    cd luna_badge_v1_2
    python3 scripts/test_voice_av_detailed.py

测试内容（共 6 条语音）：
1. 基础播放测试
2. 完整性测试（长句子）
3. 打断功能测试（会被中途停止）
4. 打断后恢复测试
5. 快速连续播放测试（测试是否叠音）
6. 最终确认测试

每条语音播放时会显示编号和测试目的
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
    logger = logging.getLogger("voice_av_test")

    voice = Voice()  # 默认 Ting-Ting 中文女声，语速 180

    logger.info("=" * 60)
    logger.info("A 方案语音测试开始")
    logger.info("Voice 状态: %r", voice.get_status())
    logger.info("=" * 60)
    print("\n" + "=" * 60)
    print("🎤 A 方案语音测试（共 6 条语音）")
    print("=" * 60 + "\n")

    # ===== 测试 1：基础播放 =====
    print("【测试 1/6】基础播放测试")
    print("目的：验证语音模块能否正常播放短句子")
    print("预期：听到完整的'测试一号，基础播放功能正常。'")
    print("-" * 60)
    voice.speak("测试一号，基础播放功能正常。")
    time.sleep(4)
    print("✅ 测试 1 完成\n")

    # ===== 测试 2：完整性测试 =====
    print("【测试 2/6】完整性测试（长句子）")
    print("目的：验证长句子能否完整播放，不会被截断")
    print("预期：听到完整的'这是第二句测试语音，内容较长，用于验证语音播报的完整性。请确认是否能够完整听到整句话的全部内容。'")
    print("-" * 60)
    voice.speak("这是第二句测试语音，内容较长，用于验证语音播报的完整性。请确认是否能够完整听到整句话的全部内容。")
    time.sleep(12)  # 增加等待时间，确保长句子完整播放
    print("✅ 测试 2 完成\n")

    # ===== 测试 3：打断功能 =====
    print("【测试 3/6】打断功能测试")
    print("目的：验证 stop() 能否成功中断正在播放的语音")
    print("预期：听到'这一句语音会在中途被打断'后，语音被停止")
    print("-" * 60)
    voice.speak("这一句语音会在中途被打断，请注意，现在开始播放。")
    time.sleep(2)
    print("⏹️  正在调用 stop() 中断当前语音...")
    voice.stop()
    time.sleep(1)
    print("✅ 测试 3 完成（语音应已被打断）\n")

    # ===== 测试 4：打断后恢复 =====
    print("【测试 4/6】打断后恢复测试")
    print("目的：验证被打断后，能否继续正常播放新语音")
    print("预期：听到完整的'刚才的语音已经被打断。现在播放新的语音，说明停止功能可以正常工作。'")
    print("-" * 60)
    voice.speak("刚才的语音已经被打断。现在播放新的语音，说明停止功能可以正常工作。")
    time.sleep(8)  # 增加等待时间，确保完整播放
    print("✅ 测试 4 完成\n")

    # ===== 测试 5：快速连续播放 =====
    print("【测试 5/6】快速连续播放测试（防叠音）")
    print("目的：验证快速发送多条语音时，是否会出现叠音")
    print("预期：只听到最后一条'测试五号，这是最后一条语音。'，前面的应该被自动停止")
    print("-" * 60)
    print("发送：测试五号 A（应该被后续语音打断）")
    voice.speak("测试五号 A，这条语音应该被下一条打断。")
    time.sleep(0.5)
    print("发送：测试五号 B（应该被后续语音打断）")
    voice.speak("测试五号 B，这条语音也应该被下一条打断。")
    time.sleep(0.5)
    print("发送：测试五号 C（最终应该播放这条）")
    voice.speak("测试五号，这是最后一条语音。")
    time.sleep(4)
    print("✅ 测试 5 完成\n")

    # ===== 测试 6：最终确认 =====
    print("【测试 6/6】最终确认测试")
    print("目的：最终确认所有功能正常")
    print("预期：听到完整的'测试六号，所有测试已完成。如果以上六条语音都能正常播放，说明 A 方案工作正常。'")
    print("-" * 60)
    voice.speak("测试六号，所有测试已完成。如果以上六条语音都能正常播放，说明 A 方案工作正常。")
    time.sleep(10)  # 增加等待时间，确保长句子完整播放
    print("✅ 测试 6 完成\n")

    # ===== 总结 =====
    print("=" * 60)
    print("📋 测试总结")
    print("=" * 60)
    print("请根据你实际听到的情况，回答以下问题：\n")
    print("1. 测试 1（基础播放）：是否完整播放？ [是/否]")
    print("2. 测试 2（完整性）：长句子是否完整播放？ [是/否]")
    print("3. 测试 3（打断功能）：语音是否被成功打断？ [是/否]")
    print("4. 测试 4（恢复功能）：打断后是否正常播放？ [是/否]")
    print("5. 测试 5（防叠音）：是否只听到最后一条语音？ [是/否]")
    print("6. 测试 6（最终确认）：是否完整播放？ [是/否]")
    print("\n其他问题：")
    print("- 是否有卡顿或杂音？ [有/无]")
    print("- 是否有叠音现象？ [有/无]")
    print("- 整体体验如何？ [好/一般/差]")
    print("=" * 60)
    
    logger.info("=" * 60)
    logger.info("A 方案语音测试结束")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()

