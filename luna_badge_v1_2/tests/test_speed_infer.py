#!/usr/bin/env python3
"""
1.4.1-speed.3 VisionInferWorker 自检脚本
按照任务说明创建的基础测试
"""
import sys
import time
from pathlib import Path

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.config.config_center import ConfigCenter
from core.logging.log_manager import LogManager
from core.speed.thread_controller import ThreadController
from core.speed.speed_thread_pool import SpeedThreadPool
from core.speed.camera_stream_worker import CameraStreamWorker
from core.speed.vision_infer_worker import VisionInferWorker
from core.speed.speed_context import SpeedContext


def main():
    """自检脚本主函数"""
    print("=" * 60)
    print("1.4.1-speed.3 VisionInferWorker 自检")
    print("=" * 60)
    
    # 初始化基础设施
    ConfigCenter.init(env="dev")
    LogManager.init()
    
    # 启动 camera worker
    print("\n启动 CameraStreamWorker...")
    camera_worker = CameraStreamWorker(cam_index=0, fps_limit=20)
    SpeedThreadPool.register(camera_worker)
    SpeedContext.set_camera_worker(camera_worker)
    
    # 加载 YOLO 模型
    print("\n加载 YOLO 模型...")
    try:
        from core.yolo_detector import YoloDetector
        model = YoloDetector()
        print("✅ YOLO 模型加载成功")
    except Exception as e:
        print(f"❌ YOLO 模型加载失败: {e}")
        print("⚠️  使用模拟模型进行测试")
        # 创建一个模拟模型用于测试
        class MockModel:
            def detect(self, frame):
                return {"boxes": [], "mock": True}
        model = MockModel()
    
    # 启动推理 worker
    print("\n启动 VisionInferWorker...")
    infer_worker = VisionInferWorker(model=model, infer_interval=0.1)
    SpeedThreadPool.register(infer_worker)
    
    ThreadController.start_speed_threads()
    
    # 等待初始化
    print("\n等待系统初始化...")
    time.sleep(2.0)
    
    # 测试读取推理结果
    print("\n测试读取推理结果（20 次，每次 0.2 秒）...")
    ok_count = 0
    total_count = 20
    
    for i in range(total_count):
        result = SpeedContext.current_yolo_result
        status = "OK" if result is not None else "None"
        if result is not None:
            ok_count += 1
        last_ts = SpeedContext.last_yolo_ts
        ts_str = f"{last_ts:.2f}" if last_ts > 0 else "N/A"
        print(f"  [{i+1}/{total_count}] YOLO Result: {status} (last_ts: {ts_str})")
        time.sleep(0.2)
    
    # 显示统计信息
    print("\n统计信息:")
    camera_stats = camera_worker.get_stats()
    infer_stats = infer_worker.get_stats()
    
    print("\nCameraStreamWorker:")
    for key, value in camera_stats.items():
        print(f"  {key}: {value}")
    
    print("\nVisionInferWorker:")
    for key, value in infer_stats.items():
        print(f"  {key}: {value}")
    
    # 计算成功率
    success_rate = (ok_count / total_count) * 100
    print(f"\n推理结果获取成功率: {success_rate:.1f}% ({ok_count}/{total_count})")
    
    if success_rate >= 50:  # 推理比摄像头帧率低，50% 即可
        print("✅ 测试通过：推理结果正常更新")
    else:
        print(f"⚠️  警告：推理结果更新不稳定（{success_rate:.1f}% < 50%）")
    
    print("\n停止所有 Worker...")
    ThreadController.stop_speed_threads()
    time.sleep(0.5)
    
    print("\n✅ 自检完成")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n收到中断信号，停止测试...")
        ThreadController.stop_speed_threads()
    except Exception as e:
        print(f"\n❌ 测试异常: {e}")
        import traceback
        traceback.print_exc()
        ThreadController.stop_speed_threads()
















