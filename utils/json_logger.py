# -*- coding: utf-8 -*-
"""
JSON日志记录器模块
"""

import json
import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional

# 配置导入
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import LOG_CONFIG


class JSONLogger:
    """JSON格式日志记录器"""
    
    def __init__(self, log_dir: str = None):
        """
        初始化JSON日志记录器
        
        Args:
            log_dir: 日志目录路径，默认为配置中的路径
        """
        self.log_dir = log_dir or LOG_CONFIG['log_dir']
        self.logger = logging.getLogger('json_logger')
        self.logger.setLevel(logging.INFO)
        
        # 创建日志目录
        os.makedirs(self.log_dir, exist_ok=True)
        
        # 避免重复添加处理器
        if not self.logger.handlers:
            # 创建控制台处理器用于info/warning/error输出
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # 创建格式器
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            console_handler.setFormatter(formatter)
            
            self.logger.addHandler(console_handler)
    
    def _get_log_filename(self) -> str:
        """
        生成日志文件名
        
        Returns:
            格式为 log_YYYYMMDD_HHMMSS.json 的文件名
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"log_{timestamp}.json"
    
    def log(self, data: Dict[str, Any], filename: str = None) -> bool:
        """
        将数据保存为JSON文件
        
        Args:
            data: 要保存的字典数据
            filename: 指定的文件名，如果为None则自动生成
            
        Returns:
            是否保存成功
        """
        try:
            if filename is None:
                filename = self._get_log_filename()
            
            # 确保文件名以.json结尾
            if not filename.endswith('.json'):
                filename += '.json'
            
            filepath = os.path.join(self.log_dir, filename)
            
            # 添加时间戳到数据中
            log_data = {
                'timestamp': datetime.now().isoformat(),
                'data': data
            }
            
            # 保存JSON文件
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"JSON日志已保存: {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"保存JSON日志失败: {e}")
            return False
    
    def log_recognition_result(self, 
                             timestamp: str,
                             objects: list,
                             texts: list,
                             description: str,
                             audio_input: str = "",
                             processing_time: float = 0.0) -> bool:
        """
        记录识别结果到JSON日志
        
        Args:
            timestamp: 时间戳
            objects: 检测到的物体列表
            texts: 识别到的文字列表
            description: AI生成的描述
            audio_input: 语音输入
            processing_time: 处理时间
            
        Returns:
            是否保存成功
        """
        log_entry = {
            "timestamp": timestamp,
            "objects": objects,
            "texts": texts,
            "description": description,
            "audio_input": audio_input,
            "processing_time": processing_time,
            "status": "success"
        }
        
        return self.log(log_entry)
    
    def log_error(self, timestamp: str, error_message: str, error_type: str = "unknown") -> bool:
        """
        记录错误到JSON日志
        
        Args:
            timestamp: 时间戳
            error_message: 错误信息
            error_type: 错误类型
            
        Returns:
            是否保存成功
        """
        log_entry = {
            "timestamp": timestamp,
            "error_message": error_message,
            "error_type": error_type,
            "status": "error"
        }
        
        return self.log(log_entry)
    
    def info(self, message: str):
        """输出信息级别日志"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """输出警告级别日志"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """输出错误级别日志"""
        self.logger.error(message)
    
    def debug(self, message: str):
        """输出调试级别日志"""
        self.logger.debug(message)
    
    def get_log_files(self) -> list:
        """
        获取日志目录中的所有JSON文件
        
        Returns:
            JSON文件路径列表
        """
        try:
            json_files = []
            for filename in os.listdir(self.log_dir):
                if filename.endswith('.json'):
                    json_files.append(os.path.join(self.log_dir, filename))
            return sorted(json_files)
        except Exception as e:
            self.logger.error(f"获取日志文件列表失败: {e}")
            return []
    
    def cleanup_old_logs(self, keep_days: int = 7):
        """
        清理旧日志文件
        
        Args:
            keep_days: 保留天数
        """
        try:
            import time
            current_time = time.time()
            cutoff_time = current_time - (keep_days * 24 * 60 * 60)
            
            log_files = self.get_log_files()
            deleted_count = 0
            
            for filepath in log_files:
                if os.path.getmtime(filepath) < cutoff_time:
                    os.remove(filepath)
                    deleted_count += 1
            
            if deleted_count > 0:
                self.logger.info(f"清理了 {deleted_count} 个旧日志文件")
                
        except Exception as e:
            self.logger.error(f"清理旧日志失败: {e}")

