#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TTSGuard × 任务链 × 播报链联测
测试防抖机制与语音播报的协同工作
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

# 从 main.py 导入 TTSGuard（需要先导入 main 模块）
# 注意：这里需要导入 main 模块，但为了避免执行 main()，我们只导入类
import importlib.util
spec = importlib.util.spec_from_file_location("main_module", os.path.join(_project_root, "main.py"))
main_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main_module)

TTSGuard = main_module.TTSGuard
TTSGuardConfig = main_module.TTSGuardConfig

guard = TTSGuard()
voice = Voice()


def say(text):
    """模拟主程序调用 TTSManager → Voice.speak"""
    if guard.allow(text):
        print(f"[GUARD] 允许播报: {text}")
        voice.speak(text)
    else:
        print(f"[GUARD] 阻止重复播报: {text}")


def log(msg):
    print(f"[TEST-GUARD] {msg}")


def run_test():
    log("▶ 初始化 TTSGuard × Voice 联测")

    # 1. 第一次播报
    say("您已到达示例地点附近。")
    time.sleep(3)

    # 2. 重复播报（应阻止）
    say("您已到达示例地点附近。")
    time.sleep(1)

    # 3. 不同文案（应放行）
    say("前方 5 米有人群，请靠边行走。")
    time.sleep(4)

    # 4. 高频重复（模拟 bug 场景）
    for _ in range(3):
        say("前方 5 米有人群，请靠边行走。")
        time.sleep(0.5)

    time.sleep(3)

    # 5. 长句覆盖与打断测试
    say("这一段语音会被随后的一句覆盖，请注意听感效果。")
    time.sleep(1)
    say("覆盖成功，这一句应完整播放。")
    time.sleep(4)

    log("🎉 TTSGuard × Voice 播报链联测完成")


if __name__ == "__main__":
    run_test()













