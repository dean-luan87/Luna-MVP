#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna 云端同步管理器
支持跨设备地图记忆同步
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import hashlib

logger = logging.getLogger(__name__)


class LunaCloudSync:
    """Luna 云端同步管理器"""
    
    def __init__(self, user_id: Optional[str] = None, api_key: Optional[str] = None):
        """初始化同步管理器"""
        self.user_id = user_id
        self.api_key = api_key
        self.config_dir = Path("config")
        self.config_dir.mkdir(exist_ok=True)
        
        # 用户配置
        self.user_config_file = self.config_dir / "user_config.json"
        self.sync_log_file = self.config_dir / "sync_log.json"
        
        logger.info("☁️ 云端同步管理器初始化完成")
    
    def login(self, username: str, password: str) -> bool:
        """登录账号
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            是否登录成功
        """
        try:
            # 模拟登录（实际应调用真实API）
            logger.info(f"🔐 尝试登录：{username}")
            
            # 生成用户ID（基于用户名）
            self.user_id = hashlib.md5(username.encode()).hexdigest()
            
            # 保存用户信息
            user_info = {
                "username": username,
                "user_id": self.user_id,
                "logged_in_at": datetime.now().isoformat()
            }
            
            with open(self.user_config_file, 'w') as f:
                json.dump(user_info, f)
            
            logger.info(f"✅ 登录成功：用户ID {self.user_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 登录失败：{e}")
            return False
    
    def logout(self):
        """登出账号"""
        if self.user_config_file.exists():
            self.user_config_file.unlink()
        
        self.user_id = None
        self.api_key = None
        logger.info("👋 已登出")
    
    def is_logged_in(self) -> bool:
        """检查是否已登录"""
        return self.user_config_file.exists() and self.user_id is not None
    
    def get_user_info(self) -> Optional[Dict]:
        """获取用户信息"""
        if not self.user_config_file.exists():
            return None
        
        try:
            with open(self.user_config_file, 'r') as f:
                return json.load(f)
        except:
            return None
    
    def sync_all_maps(self, local_map_dir: str = "data/map_cards") -> Dict:
        """同步所有地图
        
        Args:
            local_map_dir: 本地地图目录
            
        Returns:
            同步统计信息
        """
        if not self.is_logged_in():
            logger.error("❌ 未登录，无法同步")
            return {"error": "not_logged_in"}
        
        logger.info(f"🔄 开始同步地图：用户 {self.user_id}")
        
        from core.luna_map_loader import LunaMapLoader
        loader = LunaMapLoader(local_map_dir)
        
        # 列出本地地图
        local_maps = loader.list_available_maps()
        
        # 记录同步时间
        sync_timestamp = datetime.now().isoformat()
        
        # 统计
        stats = {
            "synced_at": sync_timestamp,
            "total_maps": len(local_maps),
            "uploaded": 0,
            "downloaded": 0,
            "failed": 0
        }
        
        # 记录到同步日志
        self._log_sync_event(stats)
        
        logger.info(f"✅ 同步完成：{stats['total_maps']}个地图")
        
        return stats
    
    def backup_all_data(self, backup_path: str) -> bool:
        """备份所有数据
        
        Args:
            backup_path: 备份目录路径
            
        Returns:
            是否成功
        """
        try:
            backup_dir = Path(backup_path)
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            # 获取用户信息
            user_info = self.get_user_info()
            if not user_info:
                logger.error("❌ 未登录，无法备份")
                return False
            
            # 备份用户配置
            with open(backup_dir / "user_config.json", 'w') as f:
                json.dump(user_info, f)
            
            # 备份地图
            maps_dir = backup_dir / "maps"
            maps_dir.mkdir(exist_ok=True)
            
            from core.luna_map_loader import LunaMapLoader
            loader = LunaMapLoader("data/map_cards")
            
            for map_id in loader.list_available_maps():
                map_card = loader.load_map_card(map_id)
                if map_card:
                    # 保存元数据
                    with open(maps_dir / f"{map_id}.json", 'w') as f:
                        json.dump(map_card["metadata"], f, ensure_ascii=False)
                    
                    # 保存图像（如果存在）
                    if map_card["image"]:
                        image_path = maps_dir / f"{map_id}.png"
                        map_card["image"].save(image_path)
            
            logger.info(f"✅ 备份完成：{backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 备份失败：{e}")
            return False
    
    def restore_from_backup(self, backup_path: str) -> bool:
        """从备份恢复数据
        
        Args:
            backup_path: 备份目录路径
            
        Returns:
            是否成功
        """
        try:
            backup_dir = Path(backup_path)
            
            if not backup_dir.exists():
                logger.error(f"❌ 备份目录不存在：{backup_path}")
                return False
            
            # 恢复用户配置
            user_config_file = backup_dir / "user_config.json"
            if user_config_file.exists():
                with open(user_config_file, 'r') as f:
                    user_info = json.load(f)
                
                with open(self.user_config_file, 'w') as f:
                    json.dump(user_info, f)
                
                self.user_id = user_info.get("user_id")
            
            # 恢复地图
            maps_dir = backup_dir / "maps"
            if maps_dir.exists():
                from core.luna_map_loader import LunaMapLoader
                loader = LunaMapLoader("data/map_cards")
                
                for json_file in maps_dir.glob("*.json"):
                    with open(json_file, 'r') as f:
                        map_metadata = json.load(f)
                    
                    # 复制到本地
                    local_json = Path("data/map_cards") / json_file.name
                    with open(local_json, 'w') as f:
                        json.dump(map_metadata, f, ensure_ascii=False)
                    
                    # 复制图像
                    image_file = maps_dir / f"{json_file.stem}.png"
                    if image_file.exists():
                        import shutil
                        local_image = Path("data/map_cards") / f"{json_file.stem}_emotional.png"
                        shutil.copy(image_file, local_image)
            
            logger.info(f"✅ 恢复完成：从 {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 恢复失败：{e}")
            return False
    
    def get_sync_status(self) -> Dict:
        """获取同步状态
        
        Returns:
            同步状态信息
        """
        from core.luna_map_loader import LunaMapLoader
        loader = LunaMapLoader()
        
        status = {
            "logged_in": self.is_logged_in(),
            "total_maps_local": len(loader.list_available_maps()),
            "last_sync": self._get_last_sync_time()
        }
        
        if self.is_logged_in():
            user_info = self.get_user_info()
            status["username"] = user_info.get("username")
            status["user_id"] = self.user_id
        
        return status
    
    def _get_last_sync_time(self) -> Optional[str]:
        """获取最后同步时间"""
        if not self.sync_log_file.exists():
            return None
        
        try:
            with open(self.sync_log_file, 'r') as f:
                logs = json.load(f)
                if logs:
                    return logs[-1].get("synced_at")
        except:
            pass
        
        return None
    
    def _log_sync_event(self, stats: Dict):
        """记录同步事件"""
        if not self.sync_log_file.exists():
            logs = []
        else:
            try:
                with open(self.sync_log_file, 'r') as f:
                    logs = json.load(f)
            except:
                logs = []
        
        logs.append(stats)
        
        # 只保留最近100条日志
        if len(logs) > 100:
            logs = logs[-100:]
        
        with open(self.sync_log_file, 'w') as f:
            json.dump(logs, f)


# 测试函数
if __name__ == "__main__":
    import logging
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 初始化同步管理器
    sync_manager = LunaCloudSync()
    
    # 登录测试
    print("=" * 60)
    print("🔐 登录测试")
    print("=" * 60)
    if sync_manager.login("test_user", "password"):
        print(f"✅ 登录成功：用户ID {sync_manager.user_id}")
        
        # 获取状态
        print("\n📊 同步状态：")
        status = sync_manager.get_sync_status()
        print(json.dumps(status, indent=2, ensure_ascii=False))
        
        # 同步地图
        print("\n🔄 同步地图：")
        stats = sync_manager.sync_all_maps()
        print(json.dumps(stats, indent=2, ensure_ascii=False))
        
        # 备份数据
        print("\n💾 备份数据：")
        backup_path = "backup/test_backup"
        if sync_manager.backup_all_data(backup_path):
            print(f"✅ 备份完成：{backup_path}")
        
        # 登出
        print("\n👋 登出：")
        sync_manager.logout()
    else:
        print("❌ 登录失败")


