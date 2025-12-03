"""
提供测试环境所需的模拟函数，用于注入故障。

这些 mock 不会破坏现有模块，只是替换 worker 的时间戳或内部变量。
"""
import time
import threading
import os


def freeze_camera_stream(worker):
    """模拟 CameraWorker 死亡：停止 frame 更新"""
    worker._test_freeze = True


def unfreeze_camera_stream(worker):
    """恢复 CameraWorker"""
    worker._test_freeze = False


def freeze_infer_stream(worker):
    """模拟推理线程停止"""
    worker._test_freeze = True


def unfreeze_infer_stream(worker):
    """恢复推理线程"""
    worker._test_freeze = False


def simulate_high_cpu(duration=3):
    """制造 CPU 占用 100%"""
    start = time.time()
    while time.time() - start < duration:
        _ = sum([i*i for i in range(2000)])


def simulate_high_mem():
    """简单分配大数组模拟内存压力"""
    try:
        a = [0] * (5_000_000)
    except:
        pass


def block_thread(seconds=3):
    """阻塞线程模拟死锁"""
    time.sleep(seconds)


import random
from core.failsafe.health_events import HealthEvent


def random_health_event():
    """
    随机生成一个 HealthEvent，用于压力测试
    
    Returns:
        随机的 HealthEvent 类型
    """
    candidates = [
        HealthEvent.CAMERA_STALE,
        HealthEvent.INFER_STALE,
        HealthEvent.THREAD_HANG,
        HealthEvent.HIGH_CPU,
        HealthEvent.HIGH_MEM,
    ]
    return random.choice(candidates)


def inject_random_events(failsafe_manager, count=50, interval=0.1):
    """
    在一段时间内持续注入随机 HealthEvent
    
    Args:
        failsafe_manager: FailSafeManager 实例
        count: 注入事件数量
        interval: 事件间隔（秒）
    """
    for _ in range(count):
        ev = random_health_event()
        failsafe_manager.on_health_event(ev)
        time.sleep(interval)

