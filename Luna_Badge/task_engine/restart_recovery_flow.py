#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Luna Badge v1.4 - 重启恢复引导模块
系统异常重启后自动执行，检测恢复点并通过语音引导用户选择是否恢复任务
"""

import logging
import time
import os
import json
from typing import Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class RestartContext:
    """重启上下文"""
    task_id: str
    last_node_id: str
    timestamp: str
    reason: str
    valid: bool = True
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


class RestartRecoveryFlow:
    """重启恢复引导模块"""
    
    def __init__(self, state_manager=None, cache_manager=None, 
                 failsafe_trigger=None, storage_dir: str = "data"):
        """
        初始化恢复引导模块
        
        Args:
            state_manager: 状态管理器
            cache_manager: 缓存管理器
            failsafe_trigger: 故障安全触发器
            storage_dir: 存储目录
        """
        self.state_manager = state_manager
        self.cache_manager = cache_manager
        self.failsafe_trigger = failsafe_trigger
        self.storage_dir = storage_dir
        self.logger = logging.getLogger("RestartRecoveryFlow")
        
        # 恢复上下文文件
        self.context_file = os.path.join(storage_dir, "restart_context.json")
        self.recovery_log_file = os.path.join(storage_dir, "recovery_logs.json")
        
        # 确保目录存在
        os.makedirs(storage_dir, exist_ok=True)
        
        self.logger.info("🔄 RestartRecoveryFlow 初始化完成")
    
    def check_restart_context(self) -> bool:
        """
        判断是否存在恢复上下文
        
        Returns:
            bool: 是否存在有效恢复上下文
        """
        # 检查文件是否存在
        if not os.path.exists(self.context_file):
            self.logger.info("📋 没有恢复上下文文件")
            return False
        
        try:
            with open(self.context_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 检查是否有效
            if data.get("valid", False):
                self.logger.info(f"✅ 发现有效恢复上下文: {data.get('task_id')}")
                return True
            else:
                self.logger.info("📋 恢复上下文已过期或无效")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ 读取恢复上下文失败: {e}")
            return False
    
    def get_restart_context(self) -> Optional[RestartContext]:
        """
        获取恢复上下文
        
        Returns:
            RestartContext: 恢复上下文对象
        """
        if not os.path.exists(self.context_file):
            return None
        
        try:
            with open(self.context_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return RestartContext(
                task_id=data.get("task_id", ""),
                last_node_id=data.get("last_node_id", ""),
                timestamp=data.get("timestamp", ""),
                reason=data.get("reason", ""),
                valid=data.get("valid", True)
            )
            
        except Exception as e:
            self.logger.error(f"❌ 解析恢复上下文失败: {e}")
            return None
    
    def prompt_user_for_recovery(self, context: RestartContext) -> bool:
        """
        语音或界面提示用户是否恢复任务
        
        Args:
            context: 恢复上下文
            
        Returns:
            bool: 用户是否选择恢复
        """
        task_name = self._get_task_name(context.task_id)
        reason = context.reason if context.reason else "系统故障"
        
        # 语音提示
        prompt = (
            f"Luna刚才因为{reason}重启了。"
            f"检测到您之前未完成的{task_name}任务，要不要继续？"
        )
        
        self.logger.info(f"🎤 提示用户: {prompt}")
        
        # 这里应该调用TTS播放
        # tts_manager.speak(prompt)
        
        # 模拟用户选择（实际应该通过语音识别或按键获取）
        # 这里返回True作为示例
        user_choice = True  # 实际应该通过UI/语音获取
        
        if user_choice:
            self.logger.info("✅ 用户选择恢复任务")
        else:
            self.logger.info("❌ 用户选择不恢复")
        
        # 记录用户选择到日志
        self._log_user_choice(user_choice, context, reason=reason)
        
        return user_choice
    
    def execute_recovery(self, context: RestartContext) -> bool:
        """
        调用 task_state_manager 加载恢复节点和状态
        
        Args:
            context: 恢复上下文
            
        Returns:
            bool: 是否成功恢复
        """
        self.logger.info(f"🔄 开始恢复任务: {context.task_id}")
        
        try:
            # 1. 尝试从状态管理器加载任务状态
            if self.state_manager:
                # 检查状态文件是否存在
                state_file = os.path.join("data/task_states", f"{context.task_id}_*.json")
                
                # 这里应该加载最近的状态文件
                # 简化示例：直接使用state_manager
                self.logger.info(f"📋 恢复节点: {context.last_node_id}")
                
                # 2. 恢复缓存
                if self.cache_manager:
                    # 尝试恢复缓存
                    self.logger.info("💾 恢复缓存状态...")
            
            # 3. 清除恢复上下文（避免重复恢复）
            self._clear_restart_context()
            
            # 4. 记录恢复日志
            self._log_recovery_success(context)
            
            self.logger.info("✅ 任务恢复成功")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 任务恢复失败: {e}")
            
            # 记录恢复失败
            self._log_recovery_failure(context, str(e))
            
            # 执行失败处理
            self.handle_recovery_failure()
            
            return False
    
    def reset_to_fresh_state(self) -> None:
        """
        清除所有任务缓存，重新初始化系统
        """
        self.logger.info("🧹 清除所有状态，重新开始")
        
        try:
            # 1. 清除恢复上下文
            self._clear_restart_context()
            
            # 2. 清除所有缓存
            if self.cache_manager:
                self.cache_manager.clear_all_cache()
                self.cache_manager.clear_all_snapshots()
            
            # 3. 清除状态管理器
            if self.state_manager:
                # 这里应该清除所有任务状态
                pass
            
            # 4. 清除故障安全标志
            if self.failsafe_trigger:
                self.failsafe_trigger.clear_failsafe_mode()
            
            # 5. 记录重置日志
            self._log_reset()
            
            self.logger.info("✅ 系统已重置，可以重新开始")
            
        except Exception as e:
            self.logger.error(f"❌ 重置失败: {e}")
    
    def handle_recovery_failure(self) -> None:
        """
        若恢复失败 → 提示用户重新开始并写入日志
        """
        self.logger.error("❌ 恢复失败，提示用户重新开始")
        
        # 语音提示
        message = "抱歉，恢复失败。请重新开始任务。"
        self.logger.info(f"🎤 提示用户: {message}")
        
        # 这里应该调用TTS播放
        # tts_manager.speak(message)
        
        # 清除失败状态
        self.reset_to_fresh_state()
    
    def _clear_restart_context(self):
        """清除恢复上下文"""
        if os.path.exists(self.context_file):
            try:
                # 标记为无效而不是删除
                with open(self.context_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                data["valid"] = False
                
                with open(self.context_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                self.logger.debug("🗑️ 恢复上下文已清除")
                
            except Exception as e:
                self.logger.error(f"❌ 清除恢复上下文失败: {e}")
    
    def _get_task_name(self, task_id: str) -> str:
        """
        获取任务名称（简化版）
        
        Args:
            task_id: 任务ID
            
        Returns:
            str: 任务名称
        """
        task_name_map = {
            "hospital_visit": "医院就诊",
            "government_service": "政务服务",
            "shopping_mall": "购物",
            "buy_snack": "购买零食"
        }
        
        return task_name_map.get(task_id, task_id)
    
    def _log_user_choice(self, chose_recovery: bool, context: RestartContext, **kwargs):
        """记录用户选择"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "task_id": context.task_id,
            "last_node_id": context.last_node_id,
            "user_choice": "recover" if chose_recovery else "reset",
            "reason": kwargs.get("reason", "unknown")
        }
        
        self._write_recovery_log(log_entry)
    
    def _log_recovery_success(self, context: RestartContext):
        """记录恢复成功"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "task_id": context.task_id,
            "last_node_id": context.last_node_id,
            "status": "success",
            "reason": "recovery_completed"
        }
        
        self._write_recovery_log(log_entry)
    
    def _log_recovery_failure(self, context: RestartContext, error: str):
        """记录恢复失败"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "task_id": context.task_id,
            "last_node_id": context.last_node_id,
            "status": "failure",
            "error": error
        }
        
        self._write_recovery_log(log_entry)
    
    def _log_reset(self):
        """记录重置操作"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "status": "reset",
            "reason": "user_cancelled_or_recovery_failed"
        }
        
        self._write_recovery_log(log_entry)
    
    def _write_recovery_log(self, log_entry: Dict[str, Any]):
        """写入恢复日志"""
        try:
            # 读取现有日志
            logs = []
            if os.path.exists(self.recovery_log_file):
                with open(self.recovery_log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            
            # 添加新日志
            logs.append(log_entry)
            
            # 只保留最近100条日志
            if len(logs) > 100:
                logs = logs[-100:]
            
            # 写入文件
            with open(self.recovery_log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
            
            self.logger.debug(f"📝 恢复日志已记录")
            
        except Exception as e:
            self.logger.error(f"❌ 写入恢复日志失败: {e}")
    
    def run_recovery_flow(self) -> bool:
        """
        执行完整的恢复流程
        
        Returns:
            bool: 是否成功恢复
        """
        self.logger.info("🔄 开始恢复流程")
        
        # 1. 检查恢复上下文
        if not self.check_restart_context():
            self.logger.info("📋 没有待恢复的任务")
            return False
        
        # 2. 获取恢复上下文
        context = self.get_restart_context()
        if not context:
            self.logger.error("❌ 无法获取恢复上下文")
            return False
        
        self.logger.info(f"📋 发现待恢复任务: {context.task_id} (节点: {context.last_node_id})")
        
        # 3. 提示用户
        user_choice = self.prompt_user_for_recovery(context)
        
        if user_choice:
            # 4. 执行恢复
            success = self.execute_recovery(context)
            
            if success:
                self.logger.info("✅ 恢复流程完成")
                return True
            else:
                self.logger.error("❌ 恢复流程失败")
                return False
        else:
            # 5. 重置系统
            self.reset_to_fresh_state()
            self.logger.info("🔄 用户选择不恢复，系统已重置")
            return False


if __name__ == "__main__":
    # 测试恢复引导模块
    print("🔄 RestartRecoveryFlow测试")
    print("=" * 60)
    
    # 初始化
    recovery_flow = RestartRecoveryFlow()
    
    # 创建模拟恢复上下文
    print("\n1. 创建恢复上下文...")
    context_data = {
        "task_id": "hospital_visit",
        "last_node_id": "goto_department",
        "timestamp": datetime.now().isoformat(),
        "reason": "AI导航模块无响应",
        "valid": True
    }
    
    with open("data/restart_context.json", 'w', encoding='utf-8') as f:
        json.dump(context_data, f, ensure_ascii=False, indent=2)
    
    print(f"   ✓ 恢复上下文已创建: {context_data['task_id']}")
    
    # 测试完整恢复流程
    print("\n2. 执行恢复流程...")
    result = recovery_flow.run_recovery_flow()
    print(f"   恢复结果: {'成功' if result else '未恢复'}")
    
    # 测试检查恢复上下文
    print("\n3. 再次检查恢复上下文...")
    has_context = recovery_flow.check_restart_context()
    print(f"   有恢复上下文: {has_context}")
    
    # 测试重置
    print("\n4. 测试重置系统...")
    recovery_flow.reset_to_fresh_state()
    print("   ✓ 系统已重置")
    
    # 再次检查
    has_context = recovery_flow.check_restart_context()
    print(f"   仍有恢复上下文: {has_context}")
    
    print("\n🎉 RestartRecoveryFlow测试完成！")

