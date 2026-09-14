# -*- coding: utf-8 -*-
"""
被动 ROI v0 验证：用合成视频跑 trace，验证 roi_count 分布。
"""

import os
import sys
import tempfile
from pathlib import Path

import cv2
import numpy as np

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.append(str(_ROOT))

from config import OUTPUT_CONFIG, PROCESSING_CONFIG, LOG_CONFIG  # noqa: E402
from core.audio_worker import stop_audio_worker  # noqa: E402
from main import LunaBadgeMVP  # noqa: E402
import main as main_module  # noqa: E402


def make_test_video(path: str, num_frames: int = 60, fps: float = 30.0) -> None:
    """合成有 2 个运动区域的视频（模拟行人/车辆）"""
    h, w = 240, 320
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(path, fourcc, fps, (w, h))
    for i in range(num_frames):
        frame = np.ones((h, w, 3), dtype=np.uint8) * 128
        # 区域 1：左上角移动块
        y1, x1 = 20 + (i % 10) * 2, 30 + (i % 8)
        cv2.rectangle(frame, (x1, y1), (x1 + 40, y1 + 40), (200, 200, 200), -1)
        # 区域 2：右下角移动块
        y2, x2 = 150 + (i % 12), 200 + (i % 6) * 3
        cv2.rectangle(frame, (x2, y2), (x2 + 50, y2 + 50), (180, 180, 180), -1)
        out.write(frame)
    out.release()


def run_and_analyze(video_path: str, max_frames: int = 50) -> dict:
    OUTPUT_CONFIG["play_audio"] = False
    OUTPUT_CONFIG["print_results"] = False
    OUTPUT_CONFIG["show_camera_feed"] = False
    PROCESSING_CONFIG["process_interval"] = 0.0

    trace_path = Path(LOG_CONFIG["log_dir"]) / "a3_trace.jsonl"
    if trace_path.exists():
        trace_path.unlink()

    app = LunaBadgeMVP()
    app.voice = None
    app.voice_recognition = None

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"无法打开视频: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    frame_id = 0
    processed = 0
    try:
        while True:
            ret, frame = cap.read()
            if not ret or (max_frames and processed >= max_frames):
                break
            app.pipeline_controller._frame_id = frame_id
            app.pipeline_controller._update_frame_context(frame, ts=frame_id / max(1.0, fps))
            frame_context = app.pipeline_controller.get_frame_context()
            main_module.last_frame_ts = 0
            app.process_frame(frame, context=frame_context)
            processed += 1
            frame_id += 1
    finally:
        cap.release()
        stop_audio_worker()

    # 分析 trace
    roi_counts = []
    roi_by_quality = {"GOOD": [], "DEGRADED": [], "INVALID": []}
    if trace_path.exists():
        import json
        with open(trace_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                obj = json.loads(line)
                rc = obj.get("a3", {}).get("inputs", {}).get("roi_count", 0)
                roi_counts.append(rc)
                q = obj.get("view", {}).get("frame_quality", "INVALID")
                roi_by_quality[q].append(rc)

    return {
        "processed": processed,
        "roi_counts": roi_counts,
        "roi_mean": np.mean(roi_counts) if roi_counts else 0,
        "roi_max": max(roi_counts) if roi_counts else 0,
        "roi_gt0_pct": 100 * sum(1 for r in roi_counts if r > 0) / len(roi_counts) if roi_counts else 0,
        "roi_by_quality": {k: (np.mean(v) if v else 0, len(v)) for k, v in roi_by_quality.items()},
    }


def main():
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
        vid_path = f.name
    try:
        make_test_video(vid_path, num_frames=180)  # 6 秒，确保多轮 trace 采样
        r = run_and_analyze(vid_path, max_frames=150)
        print("被动 ROI v0 跑完了，roi_count 分布是：")
        print(f"  样本数: {r['processed']}")
        print(f"  roi_count 均值: {r['roi_mean']:.2f}")
        print(f"  roi_count 最大: {r['roi_max']}")
        print(f"  roi_count>0 占比: {r['roi_gt0_pct']:.1f}%")
        print(f"  按 frame_quality: {r['roi_by_quality']}")
    finally:
        os.unlink(vid_path)


if __name__ == "__main__":
    main()
