#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OTA更新管理器
支持从远程服务器或U盘加载语音包、播报内容
"""

import os
import json
import shutil
import hashlib
import requests
import logging
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class OTAUpdateManager:
    """OTA更新管理器"""
    
    def __init__(self, base_config_path: str = "config", 
                 base_speech_path: str = "speech",
                 update_mount_path: str = "/mnt/update",
                 remote_server_url: str = ""):
        """
        初始化OTA更新管理器
        
        Args:
            base_config_path: 基础配置路径
            base_speech_path: 基础语音路径
            update_mount_path: 更新挂载路径
            remote_server_url: 远程服务器URL
        """
        self.base_config_path = base_config_path
        self.base_speech_path = base_speech_path
        self.update_mount_path = update_mount_path
        self.remote_server_url = remote_server_url
        
        # 更新状态
        self.update_status = {
            "last_check": None,
            "last_update": None,
            "pending_updates": [],
            "update_history": []
        }
        
        # 支持的更新类型
        self.supported_types = {
            "config": {
                "extensions": [".yaml", ".json", ".yml"],
                "target_path": self.base_config_path
            },
            "speech": {
                "extensions": [".yaml", ".json", ".yml"],
                "target_path": self.base_speech_path
            },
            "voice_pack": {
                "extensions": [".zip", ".tar.gz", ".tar"],
                "target_path": self.base_speech_path
            },
            "model": {
                "extensions": [".pt", ".pth", ".onnx", ".tflite"],
                "target_path": "models"
            }
        }
        
        logger.info("✅ OTA更新管理器初始化完成")
    
    def check_local_updates(self) -> List[Dict[str, Any]]:
        """
        检查本地更新文件
        
        Returns:
            List[Dict[str, Any]]: 发现的更新文件列表
        """
        try:
            updates = []
            
            if not os.path.exists(self.update_mount_path):
                logger.info(f"📁 更新目录不存在: {self.update_mount_path}")
                return updates
            
            # 遍历更新目录
            for root, dirs, files in os.walk(self.update_mount_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, self.update_mount_path)
                    
                    # 检查文件类型
                    file_type = self._get_file_type(file)
                    if file_type:
                        update_info = {
                            "file_path": file_path,
                            "relative_path": relative_path,
                            "file_type": file_type,
                            "file_size": os.path.getsize(file_path),
                            "file_hash": self._calculate_file_hash(file_path),
                            "timestamp": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
                        }
                        updates.append(update_info)
            
            logger.info(f"📁 发现 {len(updates)} 个更新文件")
            return updates
            
        except Exception as e:
            logger.error(f"❌ 检查本地更新失败: {e}")
            return []
    
    def check_remote_updates(self) -> List[Dict[str, Any]]:
        """
        检查远程更新
        
        Returns:
            List[Dict[str, Any]]: 远程更新列表
        """
        try:
            if not self.remote_server_url:
                logger.info("🌐 未配置远程服务器URL")
                return []
            
            # 获取远程更新列表
            response = requests.get(f"{self.remote_server_url}/api/updates", timeout=10)
            response.raise_for_status()
            
            remote_updates = response.json()
            logger.info(f"🌐 发现 {len(remote_updates)} 个远程更新")
            return remote_updates
            
        except Exception as e:
            logger.error(f"❌ 检查远程更新失败: {e}")
            return []
    
    def _get_file_type(self, filename: str) -> Optional[str]:
        """
        获取文件类型
        
        Args:
            filename: 文件名
            
        Returns:
            Optional[str]: 文件类型
        """
        try:
            file_ext = os.path.splitext(filename)[1].lower()
            
            for file_type, info in self.supported_types.items():
                if file_ext in info["extensions"]:
                    return file_type
            
            return None
            
        except Exception as e:
            logger.error(f"❌ 获取文件类型失败: {e}")
            return None
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """
        计算文件哈希值
        
        Args:
            file_path: 文件路径
            
        Returns:
            str: 文件哈希值
        """
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
            
        except Exception as e:
            logger.error(f"❌ 计算文件哈希失败: {e}")
            return ""
    
    def apply_update(self, update_info: Dict[str, Any], backup: bool = True) -> bool:
        """
        应用更新
        
        Args:
            update_info: 更新信息
            backup: 是否备份原文件
            
        Returns:
            bool: 是否更新成功
        """
        try:
            file_path = update_info["file_path"]
            file_type = update_info["file_type"]
            relative_path = update_info["relative_path"]
            
            # 获取目标路径
            target_path = self.supported_types[file_type]["target_path"]
            target_file_path = os.path.join(target_path, relative_path)
            
            # 确保目标目录存在
            os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
            
            # 备份原文件
            if backup and os.path.exists(target_file_path):
                backup_path = f"{target_file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                shutil.copy2(target_file_path, backup_path)
                logger.info(f"📦 原文件已备份: {backup_path}")
            
            # 复制新文件
            shutil.copy2(file_path, target_file_path)
            logger.info(f"✅ 文件更新成功: {target_file_path}")
            
            # 记录更新历史
            self._record_update_history(update_info, "success")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ 应用更新失败: {e}")
            self._record_update_history(update_info, "failed", str(e))
            return False
    
    def apply_all_updates(self, updates: List[Dict[str, Any]], backup: bool = True) -> Dict[str, Any]:
        """
        应用所有更新
        
        Args:
            updates: 更新列表
            backup: 是否备份原文件
            
        Returns:
            Dict[str, Any]: 更新结果统计
        """
        try:
            results = {
                "total": len(updates),
                "success": 0,
                "failed": 0,
                "details": []
            }
            
            for update in updates:
                success = self.apply_update(update, backup)
                if success:
                    results["success"] += 1
                    results["details"].append({
                        "file": update["relative_path"],
                        "status": "success"
                    })
                else:
                    results["failed"] += 1
                    results["details"].append({
                        "file": update["relative_path"],
                        "status": "failed"
                    })
            
            logger.info(f"📊 更新完成: 成功 {results['success']}/{results['total']}")
            return results
            
        except Exception as e:
            logger.error(f"❌ 批量更新失败: {e}")
            return {"total": 0, "success": 0, "failed": 0, "details": []}
    
    def _record_update_history(self, update_info: Dict[str, Any], status: str, error: str = ""):
        """
        记录更新历史
        
        Args:
            update_info: 更新信息
            status: 更新状态
            error: 错误信息
        """
        try:
            history_record = {
                "timestamp": datetime.now().isoformat(),
                "file": update_info["relative_path"],
                "file_type": update_info["file_type"],
                "file_size": update_info["file_size"],
                "file_hash": update_info["file_hash"],
                "status": status,
                "error": error
            }
            
            self.update_status["update_history"].append(history_record)
            
            # 限制历史记录数量
            if len(self.update_status["update_history"]) > 100:
                self.update_status["update_history"] = self.update_status["update_history"][-100:]
                
        except Exception as e:
            logger.error(f"❌ 记录更新历史失败: {e}")
    
    def download_remote_update(self, update_info: Dict[str, Any], download_path: str) -> bool:
        """
        下载远程更新
        
        Args:
            update_info: 更新信息
            download_path: 下载路径
            
        Returns:
            bool: 是否下载成功
        """
        try:
            if not self.remote_server_url:
                logger.error("❌ 未配置远程服务器URL")
                return False
            
            # 构建下载URL
            download_url = f"{self.remote_server_url}/api/download/{update_info['id']}"
            
            # 下载文件
            response = requests.get(download_url, stream=True, timeout=30)
            response.raise_for_status()
            
            # 确保下载目录存在
            os.makedirs(os.path.dirname(download_path), exist_ok=True)
            
            # 保存文件
            with open(download_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"✅ 远程更新下载成功: {download_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 下载远程更新失败: {e}")
            return False
    
    def check_for_updates(self) -> Dict[str, Any]:
        """
        检查所有更新
        
        Returns:
            Dict[str, Any]: 更新检查结果
        """
        try:
            # 检查本地更新
            local_updates = self.check_local_updates()
            
            # 检查远程更新
            remote_updates = self.check_remote_updates()
            
            # 更新状态
            self.update_status["last_check"] = datetime.now().isoformat()
            self.update_status["pending_updates"] = local_updates + remote_updates
            
            result = {
                "local_updates": local_updates,
                "remote_updates": remote_updates,
                "total_updates": len(local_updates) + len(remote_updates),
                "last_check": self.update_status["last_check"]
            }
            
            logger.info(f"🔍 更新检查完成: 本地 {len(local_updates)} 个，远程 {len(remote_updates)} 个")
            return result
            
        except Exception as e:
            logger.error(f"❌ 更新检查失败: {e}")
            return {"local_updates": [], "remote_updates": [], "total_updates": 0}
    
    def get_update_status(self) -> Dict[str, Any]:
        """
        获取更新状态
        
        Returns:
            Dict[str, Any]: 更新状态信息
        """
        return self.update_status.copy()
    
    def save_update_status(self, file_path: str = "logs/ota_status.json"):
        """
        保存更新状态
        
        Args:
            file_path: 状态文件路径
        """
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.update_status, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ 更新状态已保存: {file_path}")
            
        except Exception as e:
            logger.error(f"❌ 保存更新状态失败: {e}")
    
    def load_update_status(self, file_path: str = "logs/ota_status.json"):
        """
        加载更新状态
        
        Args:
            file_path: 状态文件路径
        """
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.update_status = json.load(f)
                
                logger.info(f"✅ 更新状态已加载: {file_path}")
            else:
                logger.info(f"📁 更新状态文件不存在: {file_path}")
                
        except Exception as e:
            logger.error(f"❌ 加载更新状态失败: {e}")
    
    def cleanup_update_files(self, update_paths: List[str]):
        """
        清理更新文件
        
        Args:
            update_paths: 更新文件路径列表
        """
        try:
            for path in update_paths:
                if os.path.exists(path):
                    os.remove(path)
                    logger.info(f"🗑️ 更新文件已清理: {path}")
            
            logger.info(f"✅ 清理完成，共清理 {len(update_paths)} 个文件")
            
        except Exception as e:
            logger.error(f"❌ 清理更新文件失败: {e}")

# 全局OTA更新管理器实例
_global_ota_manager: Optional[OTAUpdateManager] = None

def get_ota_manager() -> OTAUpdateManager:
    """获取全局OTA更新管理器实例"""
    global _global_ota_manager
    if _global_ota_manager is None:
        _global_ota_manager = OTAUpdateManager()
    return _global_ota_manager

def check_for_updates() -> Dict[str, Any]:
    """检查更新"""
    manager = get_ota_manager()
    return manager.check_for_updates()

def apply_updates(updates: List[Dict[str, Any]], backup: bool = True) -> Dict[str, Any]:
    """应用更新"""
    manager = get_ota_manager()
    return manager.apply_all_updates(updates, backup)

# 使用示例
if __name__ == "__main__":
    # 创建OTA更新管理器
    ota_manager = OTAUpdateManager()
    
    # 检查更新
    updates = ota_manager.check_for_updates()
    print(f"发现更新: {updates}")
    
    # 应用更新
    if updates["local_updates"]:
        results = ota_manager.apply_all_updates(updates["local_updates"])
        print(f"更新结果: {results}")
    
    # 保存状态
    ota_manager.save_update_status()
    
    print("✅ OTA更新管理器测试完成")
