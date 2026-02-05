#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语音底层测试脚本
测试 voice_av 模块的基础功能
"""

import sys
import os
import time

# 添加项目路径
_script_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.normpath(os.path.join(_script_dir, '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from modules.voice_av import Voice


def log(msg):
    print(f"[TEST-VOICE] {msg}")


def run_test():
    voice = Voice()
    log("Voice 初始化完成")

    # 1. 基础播报
    log("▶ 测试1：基础播报完整性测试")
    voice.speak_and_wait("测试一号，Luna 语音诊断，请确认语音完整播放。", timeout=12)
    log("✓ 测试1 完成")

    # 2. 长句完整性测试
    log("▶ 测试2：长句完整性测试")
    voice.speak_and_wait("这是第二句测试语音，用于验证长句子是否能够稳定完整播报。请认真确认。", timeout=15)
    log("✓ 测试2 完成")

    # 3. 打断测试
    log("▶ 测试3：播放中断测试（2秒后停止）")
    voice.speak("这一句语音会在中途被打断，用于验证 stop 方法是否生效。")
    time.sleep(2)
    voice.stop()
    log("✓ 测试3 完成")

    # 4. 恢复能力测试
    log("▶ 测试4：播报恢复能力测试")
    voice.speak_and_wait("刚才的语音已经被打断，现在开始测试恢复播放能力。", timeout=10)
    log("✓ 测试4 完成")

    # 5. 异步 + 覆盖测试
    log("▶ 测试5：覆盖播放测试")
    voice.speak("这是异步播放测试。")
    time.sleep(1)
    voice.speak("这一句应该成功覆盖上一句，而不出现叠音。")
    time.sleep(1)
    voice.speak("最后一句，用于验证覆盖机制表现正常。")
    time.sleep(5)
    log("✓ 测试5 完成")

    log("🎉 test_voice_av 全部测试完成，请确认听感表现是否正确。")


if __name__ == "__main__":
    run_test()













