"""
队列封装
提供类型安全的队列接口
"""
from queue import Queue
from typing import Generic, TypeVar
import logging

# 使用标准 logging，避免循环依赖
logger = logging.getLogger(__name__)

T = TypeVar("T")


class BoundedQueue(Generic[T]):
    """
    有界队列封装
    
    提供类型安全的队列接口，支持泛型
    """
    
    def __init__(self, maxsize: int = 100):
        """
        初始化有界队列
        
        Args:
            maxsize: 队列最大容量
        """
        self._queue: Queue[T] = Queue(maxsize=maxsize)
        self._maxsize = maxsize
        logger.debug(f"BoundedQueue created with maxsize={maxsize}")

    def put(self, item: T, block: bool = True, timeout: float | None = None) -> None:
        """
        放入队列
        
        Args:
            item: 要放入的项目
            block: 是否阻塞等待
            timeout: 超时时间（秒）
        
        Raises:
            queue.Full: 队列已满且 block=False
        """
        self._queue.put(item, block=block, timeout=timeout)

    def get(self, block: bool = True, timeout: float | None = None) -> T:
        """
        从队列获取
        
        Args:
            block: 是否阻塞等待
            timeout: 超时时间（秒）
        
        Returns:
            队列中的项目
        
        Raises:
            queue.Empty: 队列为空且 block=False
        """
        return self._queue.get(block=block, timeout=timeout)

    def qsize(self) -> int:
        """
        获取队列当前大小
        
        Returns:
            队列中的项目数量
        """
        return self._queue.qsize()

    def empty(self) -> bool:
        """
        检查队列是否为空
        
        Returns:
            True 如果队列为空
        """
        return self._queue.empty()

    def full(self) -> bool:
        """
        检查队列是否已满
        
        Returns:
            True 如果队列已满
        """
        return self._queue.full()

    @property
    def maxsize(self) -> int:
        """获取队列最大容量"""
        return self._maxsize

