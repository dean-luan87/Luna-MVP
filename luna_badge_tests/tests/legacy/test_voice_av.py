# -*- coding: utf-8 -*-
"""
A 方案语音诊断脚本

用法：
    cd luna_badge_v1_2
    python3 scripts/test_voice_av.py

预期效果：
1. 听到四段不同中文播报
2. 第三段会被中途打断
3. 不叠音、不卡顿，能完整播完
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

    logger.info("Voice 状态: %r", voice.get_status())

    logger.info("播放 1：测试一号")
    voice.speak("测试一号，Luna 语音诊断。")
    # 等待第一段播放完成（估算时间：约3-4秒）
    time.sleep(5)

    logger.info("播放 2：测试二号（完整性）")
    voice.speak("这是第二句测试语音，请确认是否能够完整听到。")
    # 等待第二段播放完成（估算时间：约4-5秒）
    time.sleep(6)

    logger.info("播放 3：测试打断能力")
    voice.speak("这一句语音会在中途被打断，请注意，现在开始播放。")
    # 只等待2秒就打断
    time.sleep(2)
    logger.info("调用 stop() 中断当前语音")
    voice.stop()
    time.sleep(1)

    logger.info("播放 4：确认打断后仍可继续正常播报")
    voice.speak("刚才的语音已经被打断。说明停止功能可以正常工作。测试结束。")
    # 等待第四段播放完成（估算时间：约5-6秒）
    time.sleep(7)

    logger.info("全部测试结束。")


if __name__ == "__main__":
    main()

