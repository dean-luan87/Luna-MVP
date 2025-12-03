"""
日志写入器
支持同步和异步写入
"""
import threading
import queue
from pathlib import Path
from typing import Optional
from datetime import datetime
from .log_rotator import LogRotator
from .log_config import LogConfig


class LogWriter:
    """日志写入器"""
    
    def __init__(self, name: str, test_mode: bool = False):
        """
        初始化日志写入器
        
        Args:
            name: 日志名称（模块名）
            test_mode: 是否为测试模式
        """
        self.name = name
        self.test_mode = test_mode
        self.config = LogConfig()
        self.rotator = LogRotator(
            self.config.get_log_dir(test_mode),
            self.config.get("max_file_size_mb", 100),
            self.config.get("backup_count", 30)
        )
        
        # 异步写入队列
        self.write_queue: Optional[queue.Queue] = None
        self.write_thread: Optional[threading.Thread] = None
        
        if self.config.is_async():
            self._start_async_writer()
    
    def _start_async_writer(self):
        """启动异步写入线程"""
        self.write_queue = queue.Queue(maxsize=1000)
        self.write_thread = threading.Thread(target=self._async_write_worker, daemon=True)
        self.write_thread.start()
    
    def _async_write_worker(self):
        """异步写入工作线程"""
        while True:
            try:
                log_entry = self.write_queue.get(timeout=1.0)
                if log_entry is None:  # 退出信号
                    break
                self._write_sync(log_entry)
                self.write_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Log writer error: {e}")
    
    def _get_log_file_path(self) -> Path:
        """获取日志文件路径"""
        if self.config.should_rotate_daily():
            return self.rotator.get_daily_log_path(self.name)
        else:
            return self.rotator.log_dir / f"{self.name}.log"
    
    def _write_sync(self, log_entry: str):
        """同步写入日志"""
        log_file = self._get_log_file_path()
        
        # 检查是否需要轮转
        if self.rotator.should_rotate(log_file):
            self.rotator.rotate_file(log_file)
            log_file = self._get_log_file_path()
        
        # 写入日志
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry + '\n')
        except Exception as e:
            print(f"Failed to write log: {e}")
    
    def write(self, log_entry: str):
        """写入日志（同步或异步）"""
        if not self.config.is_enabled():
            return
        
        if self.config.is_async() and self.write_queue:
            try:
                self.write_queue.put_nowait(log_entry)
            except queue.Full:
                # 队列满时，降级为同步写入
                self._write_sync(log_entry)
        else:
            self._write_sync(log_entry)
    
    def flush(self):
        """刷新日志缓冲区"""
        if self.write_queue:
            self.write_queue.join()
    
    def close(self):
        """关闭日志写入器"""
        if self.write_queue:
            self.write_queue.put(None)  # 发送退出信号
            if self.write_thread:
                self.write_thread.join(timeout=2.0)
        
        # 清理旧日志
        self.rotator.cleanup_old_logs()

