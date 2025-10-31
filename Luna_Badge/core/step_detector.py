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
        视觉识别台阶逻辑：传入图像帧，返回是否检测到台阶
        支持YOLO模型检测
        
        Args:
            frame: 图像帧（numpy array或PIL Image）
            
        Returns:
            台阶信息字典，如果未检测到则返回None
        """
        try:
            # 尝试使用YOLO模型检测
            import numpy as np
            from ultralytics import YOLO
            
            # 初始化YOLO模型（如果未初始化）
            if not hasattr(self, 'yolo_model') or self.yolo_model is None:
                try:
                    self.yolo_model = YOLO('yolov8n.pt')
                    print("✅ YOLO模型加载成功（台阶检测）")
                except Exception as e:
                    print(f"⚠️ YOLO模型加载失败: {e}")
                    return None
            
            # 确保frame是numpy array
            if not isinstance(frame, np.ndarray):
                import cv2
                frame = np.array(frame)
            
            # YOLO检测
            results = self.yolo_model(frame, verbose=False)
            
            # 查找台阶相关的物体
            step_keywords = ['stairs', 'stair', 'step']
            
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        class_id = int(box.cls)
                        class_name = result.names[class_id]
                        confidence = float(box.conf)
                        
                        # 检查是否是台阶相关
                        for keyword in step_keywords:
                            if keyword in class_name.lower():
                                # 提取边界框
                                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                                
                                # 判断方向（简单判断：根据高度）
                                height = y2 - y1
                                width = x2 - x1
                                direction = "up" if height > width else "forward"
                                
                                step_info = {
                                    "position": (int((x1 + x2) / 2), int((y1 + y2) / 2)),
                                    "height_cm": int(height * 0.1),  # 假设缩放
                                    "width_cm": int(width * 0.1),
                                    "direction": direction,
                                    "steps_count": 1,  # 简化为1
                                    "bbox": [int(x1), int(y1), int(x2), int(y2)],
                                    "confidence": confidence,
                                    "timestamp": datetime.now().isoformat()
                                }
                                return step_info
            
            return None
            
        except ImportError:
            print("⚠️ 未安装YOLO，使用模拟检测")
            return None
        except Exception as e:
            print(f"⚠️ 台阶检测错误: {e}")
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

