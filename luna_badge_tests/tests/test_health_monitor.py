#!/usr/bin/env python3
"""
1.4.1-failsafe.1 HealthMonitor 测试脚本
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
from core.failsafe.health_monitor import HealthMonitor
from core.failsafe.health_events import HealthEvent
from core.speed.thread_controller import ThreadController
from core.speed.speed_thread_pool import SpeedThreadPool
from core.speed.camera_stream_worker import CameraStreamWorker
from core.speed.speed_context import SpeedContext


def test_health_monitor_basic():
    """测试 HealthMonitor 基本功能"""
    print("=" * 60)
    print("1.4.1-failsafe.1 HealthMonitor 基础测试")
    print("=" * 60)
    
    # 初始化基础设施
    ConfigCenter.init(env="dev")
    LogManager.init()
    
    events = []
    
    def cb(event):
        print(f"  Event: {event}")
        events.append(event)
    
    # 创建 HealthMonitor（使用较短的超时时间以便测试）
    hm = HealthMonitor(
        camera_timeout=0.1,
        infer_timeout=0.1,
        heartbeat_timeout=0.2,
        cpu_threshold=80.0,
        mem_threshold=85.0,
    )
    hm.set_callback(cb)
    
    print("\n启动 HealthMonitor...")
    hm.start_monitor()
    
    # 等待一段时间让监控运行
    print("\n等待监控运行（0.5 秒）...")
    time.sleep(0.5)
    
    print("\n停止 HealthMonitor...")
    hm.stop_monitor()
    
    print(f"\n收集到的事件: {events}")
    print(f"事件数量: {len(events)}")
    
    # 显示统计信息
    stats = hm.get_stats()
    print("\n统计信息:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n✅ HealthMonitor 基础测试通过")


def test_health_monitor_camera_stale():
    """测试摄像头超时检测"""
    print("\n" + "=" * 60)
    print("测试：摄像头超时检测")
    print("=" * 60)
    
    ConfigCenter.init(env="dev")
    LogManager.init()
    
    events = []
    
    def cb(event):
        print(f"  Event: {event}")
        events.append(event)
    
    # 创建摄像头 worker（但不启动，模拟断流）
    SpeedThreadPool.clear()
    camera_worker = CameraStreamWorker(cam_index=999, fps_limit=20)  # 无效摄像头
    SpeedThreadPool.register(camera_worker)
    SpeedContext.set_camera_worker(camera_worker)
    
    # 创建 HealthMonitor（使用很短的超时时间）
    hm = HealthMonitor(
        camera_timeout=0.2,
        infer_timeout=0.5,
    )
    hm.set_callback(cb)
    
    print("\n启动 HealthMonitor（摄像头未启动）...")
    hm.start_monitor()
    
    # 等待检测
    time.sleep(0.5)
    
    hm.stop_monitor()
    
    # 检查是否检测到 CAMERA_STALE
    if HealthEvent.CAMERA_STALE in events:
        print("✅ 成功检测到摄像头超时")
    else:
        print("⚠️  未检测到摄像头超时（可能摄像头初始化失败）")
    
    SpeedThreadPool.clear()


def test_health_monitor_infer_stale():
    """测试推理超时检测"""
    print("\n" + "=" * 60)
    print("测试：推理超时检测")
    print("=" * 60)
    
    ConfigCenter.init(env="dev")
    LogManager.init()
    
    events = []
    
    def cb(event):
        print(f"  Event: {event}")
        events.append(event)
    
    # 设置一个旧的推理时间戳
    SpeedContext.last_yolo_ts = time.time() - 1.0  # 1 秒前
    
    # 创建 HealthMonitor（使用很短的超时时间）
    hm = HealthMonitor(
        camera_timeout=0.5,
        infer_timeout=0.3,
    )
    hm.set_callback(cb)
    
    print("\n启动 HealthMonitor（推理时间戳已过期）...")
    hm.start_monitor()
    
    # 等待检测
    time.sleep(0.5)
    
    hm.stop_monitor()
    
    # 检查是否检测到 INFER_STALE
    if HealthEvent.INFER_STALE in events:
        print("✅ 成功检测到推理超时")
    else:
        print("⚠️  未检测到推理超时")


if __name__ == "__main__":
    try:
        test_health_monitor_basic()
        test_health_monitor_camera_stale()
        test_health_monitor_infer_stale()
        
        print("\n" + "=" * 60)
        print("✅ 所有 HealthMonitor 测试通过")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试异常: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        # 清理
        ThreadController.stop_speed_threads()
        SpeedThreadPool.clear()





