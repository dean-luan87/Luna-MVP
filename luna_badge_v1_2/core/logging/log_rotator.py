"""
日志文件切割和轮转
支持按天切割、按大小切割、自动清理旧日志
"""
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional
import gzip
import shutil


class LogRotator:
    """日志轮转器"""
    
    def __init__(self, log_dir: Path, max_file_size_mb: int = 100, backup_count: int = 30):
        """
        初始化日志轮转器
        
        Args:
            log_dir: 日志目录
            max_file_size_mb: 单个日志文件最大大小（MB）
            backup_count: 保留的日志文件数量
        """
        self.log_dir = log_dir
        self.max_file_size_bytes = max_file_size_mb * 1024 * 1024
        self.backup_count = backup_count
    
    def should_rotate(self, file_path: Path) -> bool:
        """
        检查是否需要轮转
        
        Args:
            file_path: 日志文件路径
        
        Returns:
            bool: 是否需要轮转
        """
        if not file_path.exists():
            return False
        
        # 检查文件大小
        if file_path.stat().st_size > self.max_file_size_bytes:
            return True
        
        return False
    
    def rotate_file(self, file_path: Path) -> Path:
        """
        轮转日志文件
        
        Args:
            file_path: 当前日志文件路径
        
        Returns:
            Path: 新的日志文件路径
        """
        if not file_path.exists():
            return file_path
        
        # 生成带时间戳的备份文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = file_path.parent / f"{file_path.stem}_{timestamp}{file_path.suffix}"
        
        # 移动当前文件到备份
        shutil.move(str(file_path), str(backup_path))
        
        # 压缩旧日志（可选）
        if backup_path.suffix != '.gz':
            try:
                with open(backup_path, 'rb') as f_in:
                    with gzip.open(f"{backup_path}.gz", 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                backup_path.unlink()
                backup_path = Path(f"{backup_path}.gz")
            except Exception:
                pass  # 压缩失败，保留原文件
        
        return file_path
    
    def cleanup_old_logs(self, pattern: str = "*.log*"):
        """
        清理旧日志文件
        
        Args:
            pattern: 文件匹配模式
        """
        log_files = sorted(self.log_dir.glob(pattern), key=lambda p: p.stat().st_mtime)
        
        # 如果文件数量超过备份数量，删除最旧的
        if len(log_files) > self.backup_count:
            for old_file in log_files[:-self.backup_count]:
                try:
                    old_file.unlink()
                except Exception:
                    pass
    
    def get_daily_log_path(self, base_name: str) -> Path:
        """
        获取按天切割的日志文件路径
        
        Args:
            base_name: 日志文件基础名称
        
        Returns:
            Path: 日志文件路径
        """
        today = datetime.now().strftime("%Y%m%d")
        log_file = self.log_dir / f"{base_name}_{today}.log"
        return log_file

