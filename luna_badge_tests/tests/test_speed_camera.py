#!/usr/bin/env python3
"""
1.4.1-speed.2 CameraStreamWorker 自检脚本
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
from core.speed.speed_context import SpeedContext


def main():
    """自检脚本主函数"""
    print("=" * 60)
    print("1.4.1-speed.2 CameraStreamWorker 自检")
    print("=" * 60)
    
    # 初始化基础设施
    ConfigCenter.init(env="dev")
    LogManager.init()
    
    # 创建并注册 CameraStreamWorker
    camera_worker = CameraStreamWorker(cam_index=0, fps_limit=20)
    SpeedThreadPool.register(camera_worker)
    SpeedContext.set_camera_worker(camera_worker)
    
    print("\n启动 CameraStreamWorker...")
    ThreadController.start_speed_threads()
    
    # 等待摄像头初始化
    time.sleep(1.0)
    
    # 测试读取帧
    print("\n测试读取帧（20 次，每次 0.1 秒）...")
    ok_count = 0
    total_count = 20
    
    for i in range(total_count):
        frame = camera_worker.buffer.read_latest()
        status = "OK" if frame is not None else "None"
        if frame is not None:
            ok_count += 1
        print(f"  [{i+1}/{total_count}] Frame: {status} (shape: {frame.shape if frame is not None else 'N/A'})")
        time.sleep(0.1)
    
    # 测试通过 SpeedContext 获取帧
    print("\n测试通过 SpeedContext 获取帧...")
    frame = SpeedContext.get_latest_frame()
    print(f"  SpeedContext.get_latest_frame(): {'OK' if frame is not None else 'None'}")
    
    # 显示统计信息
    print("\n统计信息:")
    stats = camera_worker.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # 计算成功率
    success_rate = (ok_count / total_count) * 100
    print(f"\n帧获取成功率: {success_rate:.1f}% ({ok_count}/{total_count})")
    
    if success_rate >= 80:
        print("✅ 测试通过：帧率稳定（>= 80%）")
    else:
        print(f"⚠️  警告：帧率不稳定（{success_rate:.1f}% < 80%）")
    
    print("\n停止 CameraStreamWorker...")
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





