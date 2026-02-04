#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ACTIVE × 视频 最小验证脚本

目标：在真实视频下强制 ACTIVE，使系统进入 ENGAGED，产生 arbitration → K → L，
不改默认配置、不绕 eligibility/rhythm/PAL，跑完即清理。

用法:
  python3 tools/run_active_video_test.py --video test_video_complex_6m42s.mp4 --seconds 120
"""

import argparse
import os
import sys
import time

# 项目根目录
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

from intervention.task_state_override import TaskStateOverride


def parse_args():
    p = argparse.ArgumentParser("ACTIVE × Video minimal test")
    p.add_argument("--video", required=True, help="video file path")
    p.add_argument("--seconds", type=int, default=120, help="run duration")
    p.add_argument("--no-camera", action="store_true", help="不显示摄像头窗口")
    return p.parse_args()


def main():
    args = parse_args()
    video_path = args.video
    if not os.path.isabs(video_path) and not os.path.isfile(video_path):
        video_path = os.path.join(_root, video_path)
    if not os.path.isfile(video_path):
        print(f"[ACTIVE TEST] 视频文件不存在: {video_path}")
        sys.exit(1)

    # 1. 强制 ACTIVE（仅本次 run 生效）
    TaskStateOverride.set_active(
        task_type="NAVIGATION",
        source="TEST_ACTIVE_VIDEO",
    )
    print("[ACTIVE TEST] task_state forced to ACTIVE")

    # 2. 启动主程序（视频 + 限时）
    from main import LunaBadgeMVP

    app = LunaBadgeMVP(video_path=video_path)
    app.run(show_camera=not args.no_camera, max_seconds=float(args.seconds))

    # 3. 清理 override
    TaskStateOverride.clear()
    print("[ACTIVE TEST] finished, task_state restored")


if __name__ == "__main__":
    main()
