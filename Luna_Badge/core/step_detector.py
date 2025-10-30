"""
模块1：台阶识别 × 数据持久化
实现文件：core/step_detector.py
"""
import json
import os
from datetime import datetime
from typing import Optional, Dict, Any, List


class StepDetector:
    """
    台阶识别模块
    功能：识别楼梯/台阶，通过深度估计或视觉特征判断
    记录识别数据并持久化至本地存储
    """
    
    def __init__(self, data_path="data/step_map.json"):
        self.data_path = data_path
        self.ensure_data_dir()
    
    def ensure_data_dir(self):
        """确保数据目录存在"""
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
    
    def detect_step(self, frame) -> Optional[Dict[str, Any]]:
        """
        模拟视觉识别台阶逻辑：传入图像帧，返回是否检测到台阶
        TODO：后续接入真实深度估计或YOLO模型
        
        Args:
            frame: 图像帧（numpy array或PIL Image）
            
        Returns:
            台阶信息字典，如果未检测到则返回None
        """
        # Placeholder: 模拟检测逻辑
        step_detected = False  # 实际应用中这里应该调用模型检测
        
        if step_detected:
            step_info = {
                "position": (100, 250),
                "height_cm": 15,
                "width_cm": 30,
                "direction": "up",  # up/down
                "steps_count": 5,
                "bbox": [100, 150, 200, 400],  # [x1, y1, x2, y2]
                "confidence": 0.85,
                "timestamp": datetime.now().isoformat()
            }
            return step_info
        return None
    
    def save_step_data(self, step_info: Dict[str, Any]) -> bool:
        """
        将台阶信息追加保存至本地持久化文件
        
        Args:
            step_info: 台阶信息字典
            
        Returns:
            保存是否成功
        """
        if not step_info:
            return False
        
        try:
            # 读取现有数据
            data = []
            if os.path.exists(self.data_path):
                with open(self.data_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            
            # 添加新数据
            data.append(step_info)
            
            # 保存到文件
            with open(self.data_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"保存台阶数据失败: {e}")
            return False
    
    def load_step_data(self) -> List[Dict[str, Any]]:
        """
        加载所有台阶识别记录
        
        Returns:
            台阶记录列表
        """
        if not os.path.exists(self.data_path):
            return []
        
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载台阶数据失败: {e}")
            return []


class StepDataMigration:
    """
    台阶数据迁移模块
    功能：更换设备时自动迁移台阶/结构识别数据
    绑定账号ID，实现状态还原
    """
    
    def __init__(self, data_path="data/step_map.json", migration_dir="data/migration"):
        self.data_path = data_path
        self.migration_dir = migration_dir
        self.ensure_migration_dir()
    
    def ensure_migration_dir(self):
        """确保迁移目录存在"""
        os.makedirs(self.migration_dir, exist_ok=True)
    
    def migrate_step_data_on_device_change(self, account_id: str) -> str:
        """
        绑定账号ID → 上传/下载识别数据 → 在新设备中还原
        模拟实现：本地文件拷贝 + 账号标记
        
        Args:
            account_id: 用户账号ID
            
        Returns:
            备份文件路径
        """
        backup_path = os.path.join(self.migration_dir, f"{account_id}_step_map.json")
        
        # 如果源数据存在，则迁移
        if os.path.exists(self.data_path):
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            
            # 读取原始数据
            with open(self.data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 添加账号绑定信息
            migrated_data = {
                "account_id": account_id,
                "migrated_at": datetime.now().isoformat(),
                "records": data
            }
            
            # 保存到备份路径
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(migrated_data, f, indent=2, ensure_ascii=False)
            
            print(f"台阶数据已迁移至: {backup_path}")
        
        return backup_path
    
    def restore_step_data(self, account_id: str, source_path: str) -> bool:
        """
        从迁移文件恢复台阶数据
        
        Args:
            account_id: 用户账号ID
            source_path: 迁移源文件路径
            
        Returns:
            恢复是否成功
        """
        if not os.path.exists(source_path):
            return False
        
        try:
            # 读取迁移数据
            with open(source_path, 'r', encoding='utf-8') as f:
                migrated_data = json.load(f)
            
            # 验证账号ID
            if migrated_data.get("account_id") != account_id:
                print(f"账号ID不匹配")
                return False
            
            # 恢复数据
            records = migrated_data.get("records", [])
            with open(self.data_path, 'w', encoding='utf-8') as f:
                json.dump(records, f, indent=2, ensure_ascii=False)
            
            print(f"台阶数据已从 {source_path} 恢复")
            return True
            
        except Exception as e:
            print(f"恢复台阶数据失败: {e}")
            return False
