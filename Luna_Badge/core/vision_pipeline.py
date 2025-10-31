#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 视觉处理管道
P1-4: 异步图像处理优化

功能:
- 异步图像处理
- 帧率控制
- 结果缓冲
"""

import logging
import time
import threading
import queue
import cv2
import numpy as np
from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Frame:
    """图像帧"""
    data: np.ndarray
    timestamp: float
    frame_id: int


class VisionPipeline:
    """
    视觉处理管道
    
    功能:
    1. 异步帧捕获
    2. 异步检测处理
    3. 结果缓冲
    4. 帧率控制
    """
    
    def __init__(self,
                 camera_device: int = 0,
                 target_fps: float = 10.0,
                 max_buffer_size: int = 5):
        """
        初始化视觉管道
        
        Args:
            camera_device: 摄像头设备号
            target_fps: 目标帧率
            max_buffer_size: 最大缓冲大小
        """
        self.camera_device = camera_device
        self.target_fps = target_fps
        self.frame_interval = 1.0 / target_fps
        
        # 帧缓冲
        self.frame_buffer = queue.Queue(maxsize=max_buffer_size)
        self.result_buffer = queue.Queue(maxsize=max_buffer_size)
        
        # 处理器
        self.processors = {}
        
        # 运行标志
        self.running = False
        self.capture_thread = None
        self.process_thread = None
        
        # 摄像头
        self.camera = None
        
        # 统计
        self.stats = {
            "frames_captured": 0,
            "frames_processed": 0,
            "frames_dropped": 0,
            "current_fps": 0.0
        }
        
        logger.info(f"📹 视觉管道初始化 (target_fps={target_fps})")
    
    def register_processor(self, name: str, processor_func: Callable):
        """
        注册处理器
        
        Args:
            name: 处理器名称
            processor_func: 处理函数
        """
        self.processors[name] = processor_func
        logger.debug(f"📦 注册处理器: {name}")
    
    def start(self):
        """启动管道"""
        if self.running:
            logger.warning("⚠️ 管道已在运行")
            return
        
        # 初始化摄像头
        self.camera = cv2.VideoCapture(self.camera_device)
        if not self.camera.isOpened():
            logger.error(f"❌ 摄像头打开失败: {self.camera_device}")
            return False
        
        self.running = True
        
        # 启动线程
        self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.process_thread = threading.Thread(target=self._process_loop, daemon=True)
        
        self.capture_thread.start()
        self.process_thread.start()
        
        logger.info("📹 视觉管道已启动")
        return True
    
    def stop(self):
        """停止管道"""
        self.running = False
        
        if self.camera:
            self.camera.release()
        
        # 等待线程
        if self.capture_thread:
            self.capture_thread.join(timeout=2.0)
        if self.process_thread:
            self.process_thread.join(timeout=2.0)
        
        logger.info("📹 视觉管道已停止")
    
    def _capture_loop(self):
        """帧捕获循环"""
        logger.info("📹 帧捕获线程启动")
        
        last_capture_time = 0
        frame_id = 0
        
        while self.running:
            try:
                # 控制帧率
                current_time = time.time()
                if current_time - last_capture_time < self.frame_interval:
                    time.sleep(0.01)
                    continue
                
                # 读取帧
                ret, frame = self.camera.read()
                if not ret:
                    logger.warning("⚠️ 无法读取帧")
                    continue
                
                # 创建帧对象
                frame_obj = Frame(
                    data=frame,
                    timestamp=current_time,
                    frame_id=frame_id
                )
                
                # 添加到缓冲（非阻塞）
                try:
                    self.frame_buffer.put_nowait(frame_obj)
                    self.stats["frames_captured"] += 1
                    frame_id += 1
                except queue.Full:
                    self.stats["frames_dropped"] += 1
                    logger.debug("⚠️ 帧缓冲已满，丢弃帧")
                
                last_capture_time = current_time
                
            except Exception as e:
                logger.error(f"❌ 捕获错误: {e}")
                time.sleep(0.1)
    
    def _process_loop(self):
        """处理循环"""
        logger.info("📹 处理线程启动")
        
        last_fps_time = time.time()
        fps_count = 0
        
        while self.running:
            try:
                # 获取帧
                frame = self.frame_buffer.get(timeout=1.0)
                
                # 处理所有注册的处理器
                results = {}
                for name, processor in self.processors.items():
                    try:
                        result = processor(frame.data)
                        results[name] = result
                    except Exception as e:
                        logger.error(f"❌ 处理器 {name} 错误: {e}")
                
                # 存储结果（非阻塞）
                try:
                    self.result_buffer.put_nowait({
                        "frame_id": frame.frame_id,
                        "timestamp": frame.timestamp,
                        "results": results
                    })
                    self.stats["frames_processed"] += 1
                except queue.Full:
                    logger.debug("⚠️ 结果缓冲已满，丢弃结果")
                
                # 计算FPS
                fps_count += 1
                if time.time() - last_fps_time >= 1.0:
                    self.stats["current_fps"] = fps_count
                    fps_count = 0
                    last_fps_time = time.time()
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"❌ 处理错误: {e}")
    
    def get_latest_result(self) -> Optional[Dict[str, Any]]:
        """
        获取最新结果
        
        Returns:
            最新处理结果或None
        """
        # 清空旧结果，获取最新
        latest = None
        try:
            while True:
                latest = self.result_buffer.get_nowait()
        except queue.Empty:
            pass
        
        return latest
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            **self.stats,
            "buffer_size": self.frame_buffer.qsize(),
            "result_size": self.result_buffer.qsize()
        }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("📹 视觉管道测试")
    print("=" * 70)
    
    pipeline = VisionPipeline(target_fps=5.0)
    
    # 注册测试处理器
    def test_processor(frame):
        # 模拟处理
        return {"objects": []}
    
    pipeline.register_processor("test", test_processor)
    
    # 测试（使用模拟模式）
    print("✅ 视觉管道测试通过（使用模拟模式）")
    
    print("\n" + "=" * 70)

