#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 家庭脸部信息注册模块
家人脸部信息注册与身份绑定
"""

import logging
import json
import time
import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum
import numpy as np
import base64

logger = logging.getLogger(__name__)

class RelationshipType(Enum):
    """关系类型"""
    MOTHER = "mother"
    FATHER = "father"
    SISTER = "sister"
    BROTHER = "brother"
    GRANDFATHER = "grandfather"
    GRANDMOTHER = "grandmother"
    SON = "son"
    DAUGHTER = "daughter"
    SPOUSE = "spouse"
    OTHER = "other"

@dataclass
class FamilyMember:
    """家庭成员"""
    face_id: str                     # 人脸ID
    label: str                       # 标签（如"妈妈"）
    relationship: str                # 关系类型
    nickname: Optional[str]          # 昵称
    feature_vector: Optional[str]   # 特征向量（base64编码）
    registered_at: str              # 注册时间
    confidence: float                # 注册置信度
    metadata: Dict[str, Any]        # 元数据

class FamilyFaceRegistry:
    """家庭脸部注册器"""
    
    def __init__(self, storage_file: str = "data/family_faces.json"):
        """
        初始化家庭脸部注册器
        
        Args:
            storage_file: 存储文件路径
        """
        self.logger = logging.getLogger(__name__)
        self.storage_file = storage_file
        
        # 确保数据目录存在
        os.makedirs(os.path.dirname(storage_file), exist_ok=True)
        
        # 家庭成员数据库
        self.family_members: Dict[str, FamilyMember] = {}
        
        # 加载已有数据
        self._load_data()
        
        self.logger.info("👥 家庭脸部注册器初始化完成")
    
    def register_from_voice(self, voice_command: str, image: np.ndarray) -> Dict[str, Any]:
        """
        通过语音命令注册家人
        
        Args:
            voice_command: 语音命令（如"这是我妈"）
            image: 人脸图像
            
        Returns:
            Dict[str, Any]: 注册结果
        """
        # 解析语音命令
        relationship = self._parse_relationship(voice_command)
        label = self._parse_label(voice_command)
        
        # 提取人脸特征
        feature_vector = self._extract_face_features(image)
        
        # 生成face_id
        face_id = self._generate_face_id()
        
        # 创建家庭成员记录
        member = FamilyMember(
            face_id=face_id,
            label=label,
            relationship=relationship,
            nickname=None,
            feature_vector=feature_vector,
            registered_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            confidence=0.9,
            metadata={}
        )
        
        # 保存到数据库
        self.family_members[face_id] = member
        self._save_data()
        
        self.logger.info(f"👥 已注册家人: {label} ({relationship})")
        
        result = {
            "event": "family_member_registered",
            "face_id": face_id,
            "label": label,
            "relationship": relationship,
            "registered_at": member.registered_at,
            "confidence": member.confidence
        }
        
        return result
    
    def register_from_data(self, label: str, relationship: str, 
                          feature_vector: str) -> FamilyMember:
        """
        从数据注册家人
        
        Args:
            label: 标签
            relationship: 关系类型
            feature_vector: 特征向量
            
        Returns:
            FamilyMember: 家庭成员对象
        """
        face_id = self._generate_face_id()
        
        member = FamilyMember(
            face_id=face_id,
            label=label,
            relationship=relationship,
            nickname=None,
            feature_vector=feature_vector,
            registered_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            confidence=0.9,
            metadata={}
        )
        
        self.family_members[face_id] = member
        self._save_data()
        
        return member
    
    def update_member(self, face_id: str, updates: Dict[str, Any]) -> bool:
        """
        更新家庭成员信息
        
        Args:
            face_id: 人脸ID
            updates: 更新内容
            
        Returns:
            bool: 是否成功
        """
        if face_id not in self.family_members:
            self.logger.warning(f"⚠️ 找不到家庭成员: {face_id}")
            return False
        
        member = self.family_members[face_id]
        
        # 更新字段
        if "label" in updates:
            member.label = updates["label"]
        if "nickname" in updates:
            member.nickname = updates["nickname"]
        if "relationship" in updates:
            member.relationship = updates["relationship"]
        if "metadata" in updates:
            member.metadata.update(updates["metadata"])
        
        # 保存
        self._save_data()
        
        self.logger.info(f"👥 已更新家庭成员: {face_id}")
        
        return True
    
    def get_member(self, face_id: str) -> Optional[FamilyMember]:
        """获取家庭成员"""
        return self.family_members.get(face_id)
    
    def list_all_members(self) -> List[FamilyMember]:
        """列出所有家庭成员"""
        return list(self.family_members.values())
    
    def _parse_relationship(self, text: str) -> str:
        """解析关系类型"""
        relationship_map = {
            "妈": RelationshipType.MOTHER.value,
            "爸": RelationshipType.FATHER.value,
            "姐": RelationshipType.SISTER.value,
            "哥": RelationshipType.BROTHER.value,
            "爷爷": RelationshipType.GRANDFATHER.value,
            "奶奶": RelationshipType.GRANDMOTHER.value,
            "儿子": RelationshipType.SON.value,
            "女儿": RelationshipType.DAUGHTER.value
        }
        
        for keyword, relationship in relationship_map.items():
            if keyword in text:
                return relationship
        
        return RelationshipType.OTHER.value
    
    def _parse_label(self, text: str) -> str:
        """解析标签"""
        # 简单提取，实际应该更智能
        if "妈" in text:
            return "妈妈"
        elif "爸" in text:
            return "爸爸"
        elif "姐" in text:
            return "姐姐"
        elif "哥" in text:
            return "哥哥"
        else:
            return "家人"
    
    def _extract_face_features(self, image: np.ndarray) -> str:
        """
        提取人脸特征向量
        
        Args:
            image: 人脸图像
            
        Returns:
            str: base64编码的特征向量
        """
        # TODO: 实现真实的人脸特征提取（如使用face_recognition或DeepFace）
        # 这里返回模拟的特征向量
        dummy_vector = np.random.rand(128).astype(np.float32)
        
        # 转换为base64
        vector_bytes = dummy_vector.tobytes()
        vector_base64 = base64.b64encode(vector_bytes).decode('utf-8')
        
        return vector_base64
    
    def _generate_face_id(self) -> str:
        """生成人脸ID"""
        count = len(self.family_members) + 1
        timestamp = time.strftime("%Y%m%d", time.gmtime())
        return f"face_{timestamp}_{count:03d}"
    
    def _load_data(self):
        """加载数据"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    for face_id, member_data in data.items():
                        member = FamilyMember(**member_data)
                        self.family_members[face_id] = member
                
                self.logger.info(f"✅ 已加载 {len(self.family_members)} 个家庭成员")
            except Exception as e:
                self.logger.error(f"⚠️ 加载数据失败: {e}")
    
    def _save_data(self):
        """保存数据"""
        try:
            data = {}
            for face_id, member in self.family_members.items():
                data[face_id] = asdict(member)
            
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self.logger.debug(f"✅ 已保存 {len(self.family_members)} 个家庭成员")
        except Exception as e:
            self.logger.error(f"⚠️ 保存数据失败: {e}")


# 全局注册器实例
global_family_registry = FamilyFaceRegistry()

def get_family_registry() -> FamilyFaceRegistry:
    """获取家庭注册器实例"""
    return global_family_registry


if __name__ == "__main__":
    # 测试家庭脸部注册器
    import logging
    import numpy as np
    logging.basicConfig(level=logging.INFO)
    
    registry = FamilyFaceRegistry()
    
    print("=" * 70)
    print("👥 家庭脸部注册器测试")
    print("=" * 70)
    
    # 模拟注册
    test_image = np.zeros((100, 100, 3), dtype=np.uint8)
    result = registry.register_from_voice("这是我妈", test_image)
    print("\n注册结果:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 列出所有成员
    print("\n家庭成员列表:")
    members = registry.list_all_members()
    for member in members:
        print(f"  - {member.label} ({member.relationship}) - {member.face_id}")
    
    print("\n" + "=" * 70)


