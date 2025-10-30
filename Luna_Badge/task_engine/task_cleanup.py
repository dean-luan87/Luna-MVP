#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Badge v1.4 - 任务清理器
超时/已完成任务自动释放
"""

import logging
import time
import os
import threading
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class TaskCleanup:
    """任务清理器"""
    
    def __init__(self, task_engine):
        """
        初始化任务清理器
        
        Args:
            task_engine: 任务引擎实例
        """
        self.task_engine = task_engine
        self.cleanup_queue: Dict[str, float] = {}  # graph_id -> cleanup_time
        self.cleanup_delay = 120  # 2分钟延迟
        self.timeout_threshold = 3600  # 60分钟超时
        self.log_retention_days = 30  # 日志保留30天
        self.log_directory = "data/task_logs"
        self.running = False
        self.cleanup_thread: Optional[threading.Thread] = None
        self.lock = threading.Lock()
        self.logger = logging.getLogger("TaskCleanup")
    
    def start(self):
        """启动清理线程"""
        if self.running:
            return
        
        self.running = True
        self.cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self.cleanup_thread.start()
        self.logger.info("🚀 任务清理器已启动")
    
    def stop(self):
        """停止清理线程"""
        self.running = False
        if self.cleanup_thread:
            self.cleanup_thread.join(timeout=1)
        self.logger.info("🛑 任务清理器已停止")
    
    def schedule_cleanup(self, graph_id: str, immediate: bool = False):
        """
        调度清理任务
        
        Args:
            graph_id: 任务ID
            immediate: 是否立即清理
        """
        cleanup_time = time.time() if immediate else time.time() + self.cleanup_delay
        
        with self.lock:
            self.cleanup_queue[graph_id] = cleanup_time
            status_text = "立即" if immediate else f"{self.cleanup_delay}秒后"
            self.logger.info(f"📅 调度清理: {graph_id} ({status_text})")
    
    def immediate_cleanup(self, graph_id: str):
        """立即清理任务"""
        self.schedule_cleanup(graph_id, immediate=True)
    
    def _cleanup_loop(self):
        """清理循环"""
        while self.running:
            try:
                current_time = time.time()
                to_cleanup = []
                
                # 检查需要清理的任务
                with self.lock:
                    for graph_id, cleanup_time in self.cleanup_queue.items():
                        if current_time >= cleanup_time:
                            to_cleanup.append(graph_id)
                
                # 执行清理
                for graph_id in to_cleanup:
                    self._perform_cleanup(graph_id)
                
                # 检查超时任务
                self._check_timeout_tasks()
                
                # 每日清理任务日志（每天执行一次）
                if int(current_time) % 86400 < 10:  # 每24小时检查一次
                    self._cleanup_old_logs()
                
                # 等待一段时间
                time.sleep(10)  # 每10秒检查一次
                
            except Exception as e:
                self.logger.error(f"❌ 清理循环异常: {e}")
                time.sleep(10)
    
    def _perform_cleanup(self, graph_id: str):
        """执行清理"""
        try:
            # 获取任务状态
            task_status = self.task_engine.get_task_status(graph_id)
            
            if task_status:
                # 从活动任务中移除
                if graph_id in self.task_engine.active_tasks:
                    del self.task_engine.active_tasks[graph_id]
                    self.logger.info(f"🗑️ 清理活动任务: {graph_id}")
                
                # 从已完成任务中移除
                if graph_id in self.task_engine.completed_tasks:
                    del self.task_engine.completed_tasks[graph_id]
                    self.logger.info(f"🗑️ 清理已完成任务: {graph_id}")
                
                # 从状态管理中移除
                self.task_engine.state_manager.remove_state(graph_id)
                
                # 从缓存管理器中移除
                self.task_engine.cache_manager.remove_task(graph_id)
                
                # 从插入任务队列中移除
                self.task_engine.inserted_queue.remove_inserted_task(graph_id)
            
            # 从清理队列中移除
            with self.lock:
                if graph_id in self.cleanup_queue:
                    del self.cleanup_queue[graph_id]
            
            self.logger.info(f"✅ 任务清理完成: {graph_id}")
            
        except Exception as e:
            self.logger.error(f"❌ 清理任务失败: {graph_id}: {e}")
    
    def _check_timeout_tasks(self):
        """检查超时任务"""
        current_time = time.time()
        
        for graph_id, task_graph in list(self.task_engine.active_tasks.items()):
            # 检查任务状态
            task_status = self.task_engine.get_task_status(graph_id)
            if not task_status:
                continue
            
            # 获取开始时间
            task_state = self.task_engine.state_manager.get_state(graph_id)
            if not task_state or not task_state.started_at:
                continue
            
            # 计算运行时间
            running_time = current_time - task_state.started_at
            
            # 检查是否超时
            if running_time > self.timeout_threshold:
                self.logger.warning(f"⏰ 任务超时: {graph_id} (运行{int(running_time)}秒)")
                
                # 取消任务并清理
                self.task_engine.cancel_task(graph_id)
                self.schedule_cleanup(graph_id, immediate=True)
    
    def _cleanup_old_logs(self):
        """清理旧的日志文件"""
        try:
            if not os.path.exists(self.log_directory):
                return
            
            current_time = time.time()
            retention_seconds = self.log_retention_days * 86400
            
            removed_count = 0
            for filename in os.listdir(self.log_directory):
                file_path = os.path.join(self.log_directory, filename)
                
                # 检查文件修改时间
                file_mtime = os.path.getmtime(file_path)
                if current_time - file_mtime > retention_seconds:
                    os.remove(file_path)
                    removed_count += 1
            
            if removed_count > 0:
                self.logger.info(f"🧹 清理了 {removed_count} 个过期日志文件（保留{self.log_retention_days}天）")
                
        except Exception as e:
            self.logger.error(f"❌ 清理日志失败: {e}")


if __name__ == "__main__":
    # 测试清理器
    print("🧹 TaskCleanup测试")
    print("=" * 60)
    
    # 注意：需要实际的task_engine实例
    print("⚠️ 清理器需要在TaskEngine实例化后测试")
    print("   请查看task_engine.py中的使用示例")
    
    print("\n📋 清理器功能:")
    print("   - 延迟清理: 任务完成后2分钟自动释放")
    print("   - 立即清理: 取消/失败的任务立即释放")
    print("   - 超时检查: 60分钟无进度的任务自动关闭")
    print("   - 后台运行: 每10秒检查一次需要清理的任务")
    
    print("\n🎉 TaskCleanup介绍完成！")
