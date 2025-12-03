"""
Health Events
1.4.1-failsafe.1: 健康事件类型定义
用于 HealthMonitor 和 FailSafeManager 之间的事件传递
"""


class HealthEvent:
    """
    健康事件类型定义
    
    事件说明：
    - CAMERA_DEAD: 摄像头完全失效（无法初始化）
    - INFER_DEAD: 推理线程完全失效（无法启动）
    - CAMERA_STALE: 摄像头帧更新超时（超过阈值时间无新帧）
    - INFER_STALE: 推理结果更新超时（超过阈值时间无新结果）
    - HIGH_CPU: CPU 使用率超过阈值
    - HIGH_MEM: 内存使用率超过阈值
    - THREAD_HANG: 线程心跳超时（可能卡死）
    """
    
    CAMERA_DEAD = "camera_dead"
    INFER_DEAD = "infer_dead"
    CAMERA_STALE = "camera_stale"
    INFER_STALE = "infer_stale"
    HIGH_CPU = "high_cpu"
    HIGH_MEM = "high_mem"
    THREAD_HANG = "thread_hang"
    
    @classmethod
    def all_events(cls) -> list[str]:
        """返回所有事件类型列表"""
        return [
            cls.CAMERA_DEAD,
            cls.INFER_DEAD,
            cls.CAMERA_STALE,
            cls.INFER_STALE,
            cls.HIGH_CPU,
            cls.HIGH_MEM,
            cls.THREAD_HANG,
        ]

