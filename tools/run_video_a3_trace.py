# -*- coding: utf-8 -*-
"""
使用本地视频跑主流程，生成 A3 trace。
只读执行，不改业务逻辑。
"""

import argparse
import os
import sys
import time
from pathlib import Path

import cv2

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.append(str(_ROOT))

from config import OUTPUT_CONFIG, PROCESSING_CONFIG  # noqa: E402
from core.audio_worker import stop_audio_worker  # noqa: E402
from main import LunaBadgeMVP  # noqa: E402
import main as main_module  # noqa: E402


def run_video(
    video_path: str,
    max_frames: int = None,
    frame_step: int = 1,
    simulate_active: bool = False,
    force_engaged: bool = False,
    force_engaged_test_l2: bool = False,
    output_path: str = None,
) -> None:
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"视频不存在: {video_path}")

    trace_path = _ROOT / "logs" / "a3_trace.jsonl"
    trace_path.parent.mkdir(parents=True, exist_ok=True)
    if trace_path.exists():
        trace_path.unlink()

    # 主线 A：模拟 ACTIVE 任务态（用于验证 eligible 分布）
    if simulate_active:
        os.environ["A3_HAS_GOAL"] = "1"
        print("⚠️ 模拟 ACTIVE 任务态 (A3_HAS_GOAL=1)")

    if force_engaged:
        print("⚠️ 强制 engagement=L1，仲裁与 P 层将执行并写入 trace")
    if force_engaged_test_l2:
        print("⚠️ 强制 L2 执行测试：允许真实 SAY，验证 P1–P5→Q/R/S 闭环")

    OUTPUT_CONFIG["play_audio"] = force_engaged_test_l2
    OUTPUT_CONFIG["print_results"] = False
    OUTPUT_CONFIG["show_camera_feed"] = False
    PROCESSING_CONFIG["process_interval"] = 0.0

    # L2 执行测试需同时走 SPEAK 分支（占位/门禁），故自动带上 force_engaged_test
    app = LunaBadgeMVP(force_engaged_test=force_engaged or force_engaged_test_l2, force_engaged_test_l2=force_engaged_test_l2)
    if not force_engaged_test_l2:
        app.voice = None
        app.voice_recognition = None

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"无法打开视频: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"视频: {video_path}")
    print(f"fps={fps:.2f}, total_frames={total_frames}, step={frame_step}")

    BASE_MS = 1700000000000
    FRAME_MS = 33

    frame_id = 0
    processed = 0
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_id % frame_step != 0:
                frame_id += 1
                continue
            if max_frames is not None and processed >= max_frames:
                break

            app.pipeline_controller._frame_id = frame_id
            app.pipeline_controller._update_frame_context(frame, ts=frame_id / max(1.0, fps))
            frame_context = app.pipeline_controller.get_frame_context()
            if frame_context is None:
                frame_context = {}
            now_ms = BASE_MS + frame_id * FRAME_MS
            frame_context["now_ms"] = now_ms

            # 用视频时间驱动采样，保证两遍跑同一视频时 seq/采样数一致（确定性）
            app.current_ts = frame_id / max(1.0, fps)
            app.process_frame(frame, context=frame_context)

            processed += 1
            frame_id += 1
            # 主循环节流：避免毫秒级自旋，使 A1/ENGAGED 时间累计基于感知 tick 而非 CPU 时间
            time.sleep(0.03)  # 约 30 FPS 上限
    finally:
        cap.release()
        stop_audio_worker()

    if output_path:
        import shutil
        out = Path(output_path).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(trace_path, out)
        print(f"处理完成: processed={processed}, trace={trace_path} -> 已复制到 {out}")
    else:
        print(f"处理完成: processed={processed}, trace={trace_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True, help="视频路径")
    parser.add_argument("--max-frames", type=int, default=None, help="限制处理帧数")
    parser.add_argument("--frame-step", type=int, default=1, help="每隔 N 帧处理一次")
    parser.add_argument(
        "--simulate-active",
        action="store_true",
        help="模拟 ACTIVE 任务态，验证 eligible 分布",
    )
    parser.add_argument(
        "--force-engaged",
        action="store_true",
        help="强制 engagement=L1、eligibility=allowed，使仲裁与 P 层执行并写入 trace",
    )
    parser.add_argument(
        "--force-engaged-test-l2",
        action="store_true",
        help="执行链路测试：强制 L2 并允许真实 SAY，验证 P1–P5→Q/R/S 闭环",
    )
    parser.add_argument("--output", default=None, help="trace 输出路径（默认写 logs/a3_trace.jsonl）")
    args = parser.parse_args()
    run_video(
        args.video,
        max_frames=args.max_frames,
        frame_step=args.frame_step,
        simulate_active=args.simulate_active,
        force_engaged=args.force_engaged,
        force_engaged_test_l2=getattr(args, "force_engaged_test_l2", False),
        output_path=args.output,
    )


if __name__ == "__main__":
    main()
