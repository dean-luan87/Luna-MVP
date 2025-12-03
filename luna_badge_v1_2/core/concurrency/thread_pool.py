"""
线程池
提供统一的线程池管理，用于并发任务执行
"""
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Callable, Any, Optional
import logging

# 延迟导入，避免循环依赖
logger = logging.getLogger(__name__)


class ThreadPool:
    """
    线程池管理器（单例模式）
    
    提供统一的线程池，用于执行并发任务
    """
    
    _executor: Optional[ThreadPoolExecutor] = None
    _initialized = False

    @classmethod
    def init(cls) -> None:
        """初始化线程池"""
        if cls._initialized:
            logger.warning("ThreadPool already initialized, skipping")
            return

        # 延迟导入，避免循环依赖
        from core.config.config_center import ConfigCenter
        
        max_workers = ConfigCenter.get("concurrency.default_worker_threads", 4)
        cls._executor = ThreadPoolExecutor(max_workers=max_workers)
        cls._initialized = True
        logger.info(f"ThreadPool initialized with {max_workers} workers")

    @classmethod
    def submit(cls, fn: Callable[..., Any], *args, **kwargs) -> Future:
        """
        提交任务到线程池
        
        Args:
            fn: 要执行的函数
            *args: 位置参数
            **kwargs: 关键字参数
        
        Returns:
            Future 对象，可以用于获取结果或等待完成
        
        Examples:
            >>> future = ThreadPool.submit(my_function, arg1, arg2, key=value)
            >>> result = future.result()
        """
        if not cls._initialized:
            raise RuntimeError(
                "ThreadPool not initialized. Call ThreadPool.init() first."
            )
        
        if not cls._executor:
            raise RuntimeError("ThreadPool executor is None")
        
        return cls._executor.submit(fn, *args, **kwargs)

    @classmethod
    def shutdown(cls, wait: bool = True) -> None:
        """
        关闭线程池
        
        Args:
            wait: 是否等待所有任务完成
        """
        if not cls._executor:
            logger.warning("ThreadPool is not initialized")
            return

        cls._executor.shutdown(wait=wait)
        cls._executor = None
        cls._initialized = False
        logger.info("ThreadPool shut down")

    @classmethod
    def is_initialized(cls) -> bool:
        """检查线程池是否已初始化"""
        return cls._initialized

