# -*- coding: utf-8 -*-
"""
被动 ROI v0 轻量验证：只跑 _update_frame_context + A3 tick + trace，
不跑 YOLO/OCR，快速验证 roi_count 分布。
"""

import json
import os
import sys
import tempfile
from pathlib import Path

import cv2
import numpy as np

_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT))

from config import LOG_CONFIG  # noqa: E402
from main import LunaBadgeMVP  # noqa: E402


def make_test_video(path: str, num_frames: int = 90) -> None:
    """合成有 2 个运动区域的视频（大幅位移，确保 diff 区域 ≥1%）"""
    h, w = 240, 320
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(path, fourcc, 30.0, (w, h))
    for i in range(num_frames):
        frame = np.ones((h, w, 3), dtype=np.uint8) * 128
        # 块 1: 40x40，每帧跳 15 像素，产生足够大的 diff 区域
        y1, x1 = 20 + (i % 4) * 25, 30 + (i % 5) * 30
        cv2.rectangle(frame, (x1, y1), (x1 + 40, y1 + 40), (200, 200, 200), -1)
        # 块 2: 50x50
        y2, x2 = 120 + (i % 3) * 35, 180 + (i % 4) * 28
        cv2.rectangle(frame, (x2, y2), (x2 + 50, y2 + 50), (180, 180, 180), -1)
        out.write(frame)
    out.release()


def main():
    trace_path = Path(LOG_CONFIG["log_dir"]) / "a3_trace.jsonl"
    if trace_path.exists():
        trace_path.unlink()

    app = LunaBadgeMVP()
    app.a3_log_enabled = True

    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
        vid_path = f.name
    try:
        make_test_video(vid_path, num_frames=90)
        cap = cv2.VideoCapture(vid_path)
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

        frame_id = 0
        processed = 0
        while True:
            ret, frame = cap.read()
            if not ret or processed >= 100:
                break
            app.pipeline_controller._frame_id = frame_id
            app.pipeline_controller._update_frame_context(frame, ts=frame_id / max(1.0, fps))

            # 只跑 A3 tick + trace，不跑 pipeline
            import main as main_module
            main_module.last_frame_ts = 0
            now_ms = int(__import__("time").time() * 1000)
            app.a3_runtime.tick(app.runtime_ctx, now_ms=now_ms)
            from runtime.a3_logger import log_a3_timeseries
            log_a3_timeseries(
                app.a3_runtime.last_mode,
                app.a3_runtime.last_signals,
                frame_context=app.pipeline_controller.get_frame_context(),
                interval_sec=0.001,  # 几乎每帧都写
            )
            processed += 1
            frame_id += 1
        cap.release()
    finally:
        os.unlink(vid_path)

    # 分析 trace
    roi_counts = []
    by_quality = {}
    if trace_path.exists():
        with open(trace_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                obj = json.loads(line)
                rc = obj.get("a3", {}).get("inputs", {}).get("roi_count", 0)
                q = obj.get("view", {}).get("frame_quality", "INVALID")
                roi_counts.append(rc)
                by_quality.setdefault(q, []).append(rc)

    print("被动 ROI v0 跑完了，roi_count 分布是：")
    print(f"  样本数: {len(roi_counts)}")
    if roi_counts:
        print(f"  roi_count 均值: {np.mean(roi_counts):.2f}")
        print(f"  roi_count 最大: {max(roi_counts)}")
        print(f"  roi_count>0 占比: {100 * sum(1 for r in roi_counts if r > 0) / len(roi_counts):.1f}%")
        print(f"  按 frame_quality: {[(q, np.mean(v), len(v)) for q, v in by_quality.items()]}")


if __name__ == "__main__":
    main()
