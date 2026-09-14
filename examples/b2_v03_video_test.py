# examples/b2_v03_video_test.py

import sys
import time
import cv2
from collections import deque

from vision_pipeline.b2.v03.b2_v03 import B2v03
from vision_pipeline.b2.v03.debug_snapshot import B2Snapshotter


def build_perception_from_frame(frame, frame_ts, frame_idx):
    """
    ⚠️ 这是【测试用 perception 构造器】
    真实系统中这些字段来自 CV / Tracker / Map / Event detector
    """

    # ===== 模拟一些可控变化（用于验证 B2 行为） =====
    perception = {
        # ---- PATH ----
        "path": {
            "surface": "concrete",
            "has_path": True,
        },

        # ---- ENV ----
        "env": {
            "scene": "road",
            "density": "low",
            "indoor": False,
        },

        # ---- PEOPLE ----
        "people": {
            "count": 0,
            "moving": False,
        },

        # ---- EVENT ----
        "events": [],
    }

    # ===== 人为制造变化区间（你后面可以删） =====

    # 120s～160s：路面变化
    if 120 < frame_ts < 160:
        perception["path"]["surface"] = "gravel"
        perception["path"]["has_path"] = True

    # 200s～260s：进入人群 / 集市类环境
    if 200 < frame_ts < 260:
        perception["env"]["scene"] = "market"
        perception["env"]["density"] = "high"
        perception["people"]["count"] = 15
        perception["people"]["moving"] = True

    # 300s～305s：突发事件
    if 300 < frame_ts < 305:
        perception["events"].append({
            "type": "construction",
            "severity": "high"
        })

    return perception


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 -m examples.b2_v03_video_test <video_path>")
        sys.exit(1)

    video_path = sys.argv[1]
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"[ERROR] Cannot open video: {video_path}")
        sys.exit(1)

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / max(fps, 1)
    
    # 帧缓冲区（约 1 秒历史，用于保存变化前的画面）
    frame_buffer = deque(maxlen=int(fps))
    
    # 截图工具
    snapshotter = B2Snapshotter()

    print("=" * 70)
    print("📋 B2 v0.3 VIDEO TEST")
    print(f"Video: {video_path}")
    print(f"FPS: {fps:.2f}, Frames: {total_frames}, Duration: {duration:.1f}s")
    print("=" * 70)
    print()

    # 初始化 B2 v0.3（视频模式，使用视频开始时间作为基准）
    # 注意：log_base_ts 会在第一次 tick 时设置为第一个 frame_ts
    b2 = B2v03(debug=True, log_mode="video", log_base_ts=None)

    start_wall = time.time()
    base_ts = time.time()
    frame_idx = 0
    first_frame_ts = None  # 用于设置日志基准时间

    # 统计信息
    stats = {
        "total_changes": 0,
        "world_shift": 0,
        "condition_change": 0,
        "interrupt": 0,
        "notice": 0,
    }

    print("📋 开始处理帧...")
    print("   查找以下日志关键词:")
    print("   - [B2-v0.3][TICK] - 每个 tick 的状态")
    print("   - [B2-v0.3][FACTOR] - 因子变化")
    print("   - [B2-v0.3][DECISION] - 关键决策")
    print("   - [B2-v0.3][INVALIDATE] - 世界重置")
    print()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # === 视频时间轴（秒）===
        video_ts = frame_idx / fps  # 视频内时间（用于 perception）
        frame_ts = base_ts + video_ts  # 绝对时间戳（用于 B2）
        
        # 设置日志基准时间（第一次 tick）
        if first_frame_ts is None:
            first_frame_ts = frame_ts
            b2.logger.base_ts = first_frame_ts

        # 保存帧到缓冲区（用于变化前截图）
        frame_buffer.append((video_ts, frame.copy()))

        perception = build_perception_from_frame(
            frame=frame,
            frame_ts=video_ts,  # 视频内时间
            frame_idx=frame_idx
        )

        # === 调用 B2 v0.3 tick ===
        world_change = b2.tick(
            frame_ts=frame_ts,
            perception=perception
        )

        # === 关键变化时保存截图 ===
        if world_change:
            decision = world_change.get("level", "")
            if decision in ("WORLD_SHIFT", "CONDITION_CHANGE", "INTERRUPT"):
                # BEFORE: 保存变化前的画面（缓冲区最早的一帧）
                if frame_buffer:
                    before_ts, before_frame = frame_buffer[0]
                    before_path = snapshotter.save(
                        before_frame,
                        before_ts,
                        f"BEFORE_{decision}"
                    )
                    print(f"[Snapshot] BEFORE: {before_path}")
                
                # AFTER: 保存变化后的画面（当前帧）
                after_path = snapshotter.save(
                    frame,
                    video_ts,
                    f"AFTER_{decision}"
                )
                print(f"[Snapshot] AFTER: {after_path}")

        # === 统计 ===
        if world_change:
            stats["total_changes"] += 1
            level = world_change.get("level", "UNKNOWN")
            if level == "WORLD_SHIFT":
                stats["world_shift"] += 1
            elif level == "CONDITION_CHANGE":
                stats["condition_change"] += 1
            elif level == "INTERRUPT":
                stats["interrupt"] += 1
            elif level == "NOTICE":
                stats["notice"] += 1

        frame_idx += 1

        # === 控制台进度 ===
        if frame_idx % 200 == 0:
            elapsed = time.time() - start_wall
            video_t = frame_idx / fps
            print(
                f"[进度] {frame_idx}/{total_frames} "
                f"video_ts={video_t:.1f}s "
                f"FPS(real)={frame_idx/max(elapsed,1e-3):.1f}"
            )

    cap.release()

    # === 保存健康日志 ===
    b2.health_logger.dump("b2_v03_health.json")

    print()
    print("=" * 70)
    print("✅ B2 v0.3 VIDEO TEST FINISHED")
    print(f"Total frames: {frame_idx}")
    print(f"Wall time: {time.time() - start_wall:.2f}s")
    print()
    print("📊 统计信息:")
    print(f"   总世界变化: {stats['total_changes']}")
    print(f"   - WORLD_SHIFT: {stats['world_shift']}")
    print(f"   - CONDITION_CHANGE: {stats['condition_change']}")
    print(f"   - INTERRUPT: {stats['interrupt']}")
    print(f"   - NOTICE: {stats['notice']}")
    print(f"   变化密度: {stats['total_changes'] / max(frame_idx, 1) * 100:.3f}% (每帧)")
    print("=" * 70)
    print()
    print("📋 下一步:")
    print("   1) 打开 b2_v03_health.json 查看所有世界变化事件")
    print("   2) 对照视频时间轴，验证 WORLD_SHIFT / INTERRUPT 是否出现在合理位置")
    print("   3) 检查空白区（长直路）是否保持安静")


if __name__ == "__main__":
    main()
