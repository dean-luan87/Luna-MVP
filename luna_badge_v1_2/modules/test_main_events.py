#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主程序播报链模拟测试
模拟 main.py 中的实际播报场景
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
    print(f"[TEST-MAIN] {msg}")


voice = Voice()


def simulate_navigation_events():
    log("▶ 播报：系统启动")
    voice.speak("Luna 已启动。系统初始化完成。")
    time.sleep(4)

    log("▶ 播报：到达事件（第一次触发）")
    voice.speak("您已到达示例地点附近。")
    time.sleep(4)

    log("▶ 防抖验证：重复到达事件（应被覆盖）")
    voice.speak("您已到达示例地点附近。")
    time.sleep(1)
    voice.speak("您已到达示例地点附近。")
    time.sleep(2)

    log("▶ 中断场景验证")
    voice.speak("这一句将在两秒后被打断……")
    time.sleep(2)
    voice.stop()

    log("▶ 恢复能力验证")
    voice.speak("语音已恢复正常。")
    time.sleep(4)

    log("🎉 test_main_events 全部测试完成")


if __name__ == "__main__":
    simulate_navigation_events()













