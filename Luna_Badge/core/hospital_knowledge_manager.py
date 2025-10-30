"""
医院知识管理器
管理医院流程、科室位置、服务时间的长期记忆
"""

import logging
import json
import os
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class DepartmentInfo:
    """科室信息"""
    name: str
    building: str
    floor: int
    room: str
    phone: Optional[str] = None
    hours: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "building": self.building,
            "floor": self.floor,
            "room": self.room,
            "phone": self.phone,
            "hours": self.hours
        }


@dataclass
class HospitalCorrection:
    """医院信息修正记录"""
    field: str
    old_value: Any
    new_value: Any
    source: str  # "user", "system", "api"
    timestamp: str
    confidence: float = 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "field": self.field,
            "old_value": self.old_value,
            "new_value": self.new_value,
            "source": self.source,
            "timestamp": self.timestamp,
            "confidence": self.confidence
        }


class HospitalKnowledgeManager:
    """医院知识管理器"""
    
    def __init__(self, storage_file: str = "data/hospital_knowledge.json"):
        """初始化医院知识管理器"""
        self.logger = logging.getLogger(__name__)
        self.storage_file = storage_file
        self.hospital_data: Dict[str, Any] = {}
        self.corrections: List[HospitalCorrection] = []
        
        # 默认医院材料清单
        self.default_materials = {
            "required": ["医保卡", "病历本"],
            "optional": ["身份证", "现金", "银行卡"],
            "notes": "部分医院已无需身份证"
        }
        
        self._load_data()
        self.logger.info("🏥 医院知识管理器初始化完成")
    
    def get_hospital_info(self, hospital_name: str) -> Dict[str, Any]:
        """
        获取医院信息
        
        Args:
            hospital_name: 医院名称
        
        Returns:
            Dict[str, Any]: 医院信息
        """
        if hospital_name not in self.hospital_data:
            # 创建新的医院记录
            self.hospital_data[hospital_name] = {
                "name": hospital_name,
                "departments": {},
                "materials": self.default_materials.copy(),
                "last_updated": datetime.now().isoformat(),
                "corrections": []
            }
            self._save_data()
        
        return self.hospital_data[hospital_name]
    
    def add_department(self,
                      hospital_name: str,
                      department: DepartmentInfo) -> bool:
        """
        添加科室信息
        
        Args:
            hospital_name: 医院名称
            department: 科室信息
        
        Returns:
            bool: 是否成功添加
        """
        hospital_info = self.get_hospital_info(hospital_name)
        
        # 检查是否已存在
        if department.name in hospital_info["departments"]:
            old_info = hospital_info["departments"][department.name]
            # 记录变更
            if old_info != department.to_dict():
                correction = HospitalCorrection(
                    field=f"{department.name}.location",
                    old_value=old_info,
                    new_value=department.to_dict(),
                    source="system",
                    timestamp=datetime.now().isoformat()
                )
                self.corrections.append(correction)
                hospital_info["corrections"].append(correction.to_dict())
        
        hospital_info["departments"][department.name] = department.to_dict()
        hospital_info["last_updated"] = datetime.now().isoformat()
        
        self._save_data()
        self.logger.info(f"🏥 已添加科室信息: {hospital_name} - {department.name}")
        return True
    
    def update_department(self,
                        hospital_name: str,
                        department_name: str,
                        field: str,
                        new_value: Any,
                        source: str = "user") -> bool:
        """
        更新科室信息
        
        Args:
            hospital_name: 医院名称
            department_name: 科室名称
            field: 字段名
            new_value: 新值
            source: 来源（user/system/api）
        
        Returns:
            bool: 是否成功更新
        """
        hospital_info = self.get_hospital_info(hospital_name)
        
        if department_name not in hospital_info["departments"]:
            self.logger.warning(f"⚠️ 科室不存在: {department_name}")
            return False
        
        old_value = hospital_info["departments"][department_name].get(field)
        
        # 记录修正
        correction = HospitalCorrection(
            field=f"{department_name}.{field}",
            old_value=old_value,
            new_value=new_value,
            source=source,
            timestamp=datetime.now().isoformat()
        )
        self.corrections.append(correction)
        hospital_info["corrections"].append(correction.to_dict())
        
        # 更新信息
        hospital_info["departments"][department_name][field] = new_value
        hospital_info["last_updated"] = datetime.now().isoformat()
        
        self._save_data()
        self.logger.info(f"🏥 已更新科室信息: {department_name}.{field} = {new_value}")
        return True
    
    def get_department_location(self,
                               hospital_name: str,
                               department_name: str) -> Optional[Dict[str, Any]]:
        """
        获取科室位置信息
        
        Args:
            hospital_name: 医院名称
            department_name: 科室名称
        
        Returns:
            Optional[Dict[str, Any]]: 科室位置信息
        """
        hospital_info = self.get_hospital_info(hospital_name)
        return hospital_info["departments"].get(department_name)
    
    def get_required_materials(self, hospital_name: str) -> Dict[str, Any]:
        """
        获取医院所需材料
        
        Args:
            hospital_name: 医院名称
        
        Returns:
            Dict[str, Any]: 材料清单
        """
        hospital_info = self.get_hospital_info(hospital_name)
        return hospital_info.get("materials", self.default_materials)
    
    def update_materials(self,
                        hospital_name: str,
                        materials: Dict[str, Any]) -> bool:
        """
        更新医院材料清单
        
        Args:
            hospital_name: 医院名称
            materials: 材料清单
        
        Returns:
            bool: 是否成功更新
        """
        hospital_info = self.get_hospital_info(hospital_name)
        hospital_info["materials"] = materials
        hospital_info["last_updated"] = datetime.now().isoformat()
        
        self._save_data()
        self.logger.info(f"🏥 已更新材料清单: {hospital_name}")
        return True
    
    def get_corrections_history(self, hospital_name: str) -> List[Dict[str, Any]]:
        """
        获取医院修正历史
        
        Args:
            hospital_name: 医院名称
        
        Returns:
            List[Dict[str, Any]]: 修正历史
        """
        hospital_info = self.get_hospital_info(hospital_name)
        return hospital_info.get("corrections", [])
    
    def _load_data(self):
        """加载数据"""
        os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.hospital_data = data.get("hospitals", {})
                    self.corrections = [HospitalCorrection(**c) for c in data.get("corrections", [])]
                self.logger.info("✅ 已加载医院知识数据")
            except Exception as e:
                self.logger.error(f"❌ 加载医院知识数据失败: {e}")
    
    def _save_data(self):
        """保存数据"""
        try:
            data = {
                "hospitals": self.hospital_data,
                "corrections": [c.to_dict() for c in self.corrections],
                "last_updated": datetime.now().isoformat()
            }
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.logger.debug("💾 医院知识数据已保存")
        except Exception as e:
            self.logger.error(f"❌ 保存医院知识数据失败: {e}")


# 全局医院知识管理器实例
_global_hospital_knowledge: Optional[HospitalKnowledgeManager] = None


def get_hospital_knowledge_manager() -> HospitalKnowledgeManager:
    """获取全局医院知识管理器实例"""
    global _global_hospital_knowledge
    if _global_hospital_knowledge is None:
        _global_hospital_knowledge = HospitalKnowledgeManager()
    return _global_hospital_knowledge


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("🏥 医院知识管理器测试")
    print("=" * 70)
    
    manager = get_hospital_knowledge_manager()
    
    # 测试1: 添加科室信息
    print("\n1. 添加科室信息...")
    dept = DepartmentInfo("牙科", "门诊楼", 3, "305", "021-12345678", "8:00-17:00")
    manager.add_department("虹口医院", dept)
    
    # 测试2: 更新科室信息
    print("\n2. 更新科室信息...")
    manager.update_department("虹口医院", "牙科", "floor", 2, "user")
    
    # 测试3: 获取科室位置
    print("\n3. 获取科室位置...")
    location = manager.get_department_location("虹口医院", "牙科")
    print(f"   牙科位置: {location}")
    
    # 测试4: 获取材料清单
    print("\n4. 获取材料清单...")
    materials = manager.get_required_materials("虹口医院")
    print(f"   材料清单: {materials}")
    
    # 测试5: 获取修正历史
    print("\n5. 获取修正历史...")
    corrections = manager.get_corrections_history("虹口医院")
    print(f"   修正记录数: {len(corrections)}")
    
    print("\n" + "=" * 70)

