#!/usr/bin/env python3
"""
WorkerBase 单元测试
"""
import sys
import time
from pathlib import Path

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.config.config_center import ConfigCenter
from core.logging.log_manager import LogManager
from core.concurrency.worker_base import WorkerBase


class DummyWorker(WorkerBase):
    """测试用的 Dummy Worker"""
    
    def __init__(self, name: str = "DummyWorker", interval: float = 0.1):
        super().__init__(name=name, daemon=True, interval=interval)
        self.tick_count = 0
    
    def tick(self) -> None:
        """实现 tick 方法"""
        self.tick_count += 1
        if self.tick_count <= 3:
            logger = LogManager.get_logger(__name__)
            logger.debug(f"DummyWorker tick #{self.tick_count}")


def test_worker_base_start_stop():
    """测试 Worker 启动和停止"""
    try:
        # 初始化基础设施
        ConfigCenter.init(env="dev")
        LogManager.init()
        
        # 创建 Worker
        worker = DummyWorker(name="TestWorker", interval=0.1)
        
        # 测试启动
        assert not worker.is_running(), "Worker should not be running initially"
        worker.start()
        assert worker.is_running(), "Worker should be running after start()"
        
        # 等待几个 tick
        time.sleep(0.5)
        
        # 测试停止
        worker.stop(timeout=1.0)
        assert not worker.is_running(), "Worker should not be running after stop()"
        
        # 验证 tick 被调用
        assert worker.tick_count > 0, "Worker tick should have been called"
        
        print(f"✅ Worker 启动/停止测试通过 (tick_count={worker.tick_count})")
    except Exception as e:
        print(f"❌ Worker 测试失败: {e}")
        raise


def test_worker_base_daemon():
    """测试守护线程 Worker"""
    try:
        ConfigCenter.init(env="dev")
        LogManager.init()
        
        worker = DummyWorker(name="DaemonWorker", interval=0.1)
        worker.start()
        
        # 守护线程应该不会阻止程序退出
        # 这里只是验证可以正常启动
        time.sleep(0.2)
        worker.stop()
        
        print("✅ Worker 守护线程测试通过")
    except Exception as e:
        print(f"❌ Worker 守护线程测试失败: {e}")
        raise


if __name__ == "__main__":
    print("=" * 60)
    print("WorkerBase 单元测试")
    print("=" * 60)
    
    test_worker_base_start_stop()
    test_worker_base_daemon()
    
    print("=" * 60)
    print("测试完成")
    print("=" * 60)
















