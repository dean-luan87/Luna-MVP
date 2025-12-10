"""
线程健康检查工具
用于验证线程状态、检测死锁等
"""
import threading
import time
from typing import List, Dict, Any

from core.speed.speed_thread_pool import SpeedThreadPool


class ThreadChecker:
    """线程健康检查器"""
    
    @staticmethod
    def check_all_workers() -> Dict[str, Any]:
        """
        检查所有 Worker 的健康状态
        
        Returns:
            包含每个 Worker 状态的字典
        """
        stats = {}
        
        for worker in SpeedThreadPool.workers:
            worker_stats = {
                "name": worker.name,
                "is_alive": worker.is_alive() if hasattr(worker, 'is_alive') else False,
                "daemon": worker.daemon if hasattr(worker, 'daemon') else False,
            }
            
            # 检查心跳
            if hasattr(worker, 'last_heartbeat'):
                worker_stats["last_heartbeat"] = worker.last_heartbeat
                worker_stats["heartbeat_age"] = time.time() - worker.last_heartbeat
            
            stats[worker.name] = worker_stats
        
        return stats
    
    @staticmethod
    def check_thread_count() -> Dict[str, int]:
        """
        检查线程数量
        
        Returns:
            包含线程统计信息的字典
        """
        active_threads = threading.active_count()
        daemon_threads = sum(1 for t in threading.enumerate() if t.daemon)
        
        return {
            "total": active_threads,
            "daemon": daemon_threads,
            "non_daemon": active_threads - daemon_threads,
        }
    
    @staticmethod
    def detect_hanging_threads(timeout: float = 2.0) -> List[str]:
        """
        检测可能挂起的线程
        
        Args:
            timeout: 心跳超时时间（秒）
        
        Returns:
            可能挂起的线程名称列表
        """
        hanging = []
        
        for worker in SpeedThreadPool.workers:
            if hasattr(worker, 'last_heartbeat') and worker.last_heartbeat > 0:
                age = time.time() - worker.last_heartbeat
                if age > timeout:
                    hanging.append(worker.name)
        
        return hanging





