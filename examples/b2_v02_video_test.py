import sys
import time
import cv2

from vision_pipeline.pipeline_controller import PipelineController


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 examples/b2_v02_video_test.py <video_path>")
        sys.exit(1)

    video_path = sys.argv[1]

    print("======================================================================")
    print("B2 v0.2 缓存逻辑 - 视频测试")
    print("======================================================================\n")

    print("📋 初始化 PipelineController...")
    controller = PipelineController()
    print("✅ PipelineController 初始化成功")
    print("✅ B2 v0.2 已启用\n")

    print(f"📹 使用视频文件: {video_path}\n")
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"❌ 无法打开视频: {video_path}")
        sys.exit(1)

    print("📋 开始处理帧...")
    print("   查找以下日志关键词:")
    print("   - [B2] world_signature=xxxx")
    print("   - [B2] future_cache=reused age=Xs")
    print("   - [B2] future_cache=expired recompute")
    print("   - [B2] future_cache=peek reused age=Xs")
    print("   - [B2] future_cache=peek miss")
    print("   - [B2] advisory suppressed (same as last, age=Xs)")
    print("   - [B2-v0.2][timestamp] PREWARN|DEESCALATE|WORLD_NOTE\n")
    print("----------------------------------------------------------------------")

    frame_count = 0
    t0 = time.time()

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        frame_count += 1

        # 走 pipeline（内部会跑 C1 / Nav / Modeling / B2）
        controller.process_frame(frame)

        if frame_count % 200 == 0:
            dt = time.time() - t0
            fps = frame_count / max(1e-6, dt)
            print(f"[进度] 已处理 {frame_count} 帧, FPS: {fps:.1f}")

    cap.release()
    dt = time.time() - t0
    fps = frame_count / max(1e-6, dt)

    print("----------------------------------------------------------------------\n")
    print("📋 处理完成:")
    print(f"   - 总帧数: {frame_count}")
    print(f"   - 总时间: {dt:.1f}s")
    print(f"   - 平均 FPS: {fps:.1f}\n")
    print("======================================================================")
    print("✅ 测试完成")
    print("======================================================================\n")
    print("📋 下一步:")
    print("   1) python3 examples/b2_v02_video_test.py <video> > b2_log.txt 2>&1")
    print("   2) python3 -m vision_pipeline.b2.b2_cache_observer b2_log.txt")


if __name__ == "__main__":
    main()
