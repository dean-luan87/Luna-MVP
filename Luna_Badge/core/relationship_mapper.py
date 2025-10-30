#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 关系图谱映射器模块
管理人与人之间的语义关系与行为偏好
"""

import logging
import json
import time
import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)

class SocialAttribute(Enum):
    """社交属性"""
    INTIMATE = "intimate"         # 亲密
    FAMILIAR = "familiar"         # 熟悉
    CALM = "calm"                 # 安静
    ACTIVE = "active"             # 活跃
    PROTECTIVE = "protective"    # 保护性

class AlertLevel(Enum):
    """警报等级"""
    NONE = "none"                # 无警报
    LOW = "low"                  # 低
    MEDIUM = "medium"           # 中
    HIGH = "high"               # 高

class PreferredTone(Enum):
    """偏好语调"""
    GENTLE = "gentle"           # 温和
    CHEERFUL = "cheerful"       # 欢快
    CALM = "calm"              # 平静
    URGENT = "urgent"          # 紧急

@dataclass
class RelationshipProfile:
    """关系配置"""
    face_id: str
    relation: str               # 关系
    nickname: str              # 昵称
    preferred_tone: str        # 偏好语调
    alert_level: str          # 警报等级
    emotion_tag: str          # 情绪标签
    social_attributes: List[str]  # 社交属性
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "face_id": self.face_id,
            "relation": self.relation,
            "nickname": self.nickname,
            "preferred_tone": self.preferred_tone,
            "alert_level": self.alert_level,
            "emotion_tag": self.emotion_tag,
            "social_attributes": self.social_attributes
        }

class RelationshipMapper:
    """关系图谱映射器"""
    
    def __init__(self, storage_file: str = "data/relationship_map.json"):
        """
        初始化关系映射器
        
        Args:
            storage_file: 存储文件路径
        """
        self.logger = logging.getLogger(__name__)
        self.storage_file = storage_file
        
        # 确保数据目录存在
        os.makedirs(os.path.dirname(storage_file), exist_ok=True)
        
        # 关系数据库
        self.profiles: Dict[str, RelationshipProfile] = {}
        
        # 默认关系配置
        self.default_profiles = {
            "mother": {
                "preferred_tone": PreferredTone.GENTLE.value,
                "alert_level": AlertLevel.NONE.value,
                "emotion_tag": "calm",
                "social_attributes": [SocialAttribute.INTIMATE.value, SocialAttribute.PROTECTIVE.value]
            },
            "father": {
                "preferred_tone": PreferredTone.GENTLE.value,
                "alert_level": AlertLevel.NONE.value,
                "emotion_tag": "calm",
                "social_attributes": [SocialAttribute.INTIMATE.value, SocialAttribute.PROTECTIVE.value]
            },
            "brother": {
                "preferred_tone": PreferredTone.CHEERFUL.value,
                "alert_level": AlertLevel.NONE.value,
                "emotion_tag": "active",
                "social_attributes": [SocialAttribute.FAMILIAR.value]
            }
        }
        
        # 加载数据
        self._load_data()
        
        self.logger.info("👥 关系图谱映射器初始化完成")
    
    def create_profile(self, face_id: str, relation: str, 
                      nickname: str = None) -> RelationshipProfile:
        """
        创建关系配置
        
        Args:
            face_id: 人脸ID
            relation: 关系
            nickname: 昵称
            
        Returns:
            RelationshipProfile: 关系配置
        """
        # 获取默认配置
        default_config = self.default_profiles.get(relation, {
            "preferred_tone": PreferredTone.GENTLE.value,
            "alert_level": AlertLevel.NONE.value,
            "emotion_tag": "calm",
            "social_attributes": [SocialAttribute.FAMILIAR.value]
        })
        
        profile = RelationshipProfile(
            face_id=face_id,
            relation=relation,
            nickname=nickname or self._generate_default_nickname(relation),
            preferred_tone=default_config["preferred_tone"],
            alert_level=default_config["alert_level"],
            emotion_tag=default_config["emotion_tag"],
            social_attributes=default_config["social_attributes"]
        )
        
        self.profiles[face_id] = profile
        self._save_data()
        
        self.logger.info(f"👥 已创建关系配置: {relation} ({nickname})")
        
        return profile
    
    def get_relation_by_face(self, face_id: str) -> Optional[RelationshipProfile]:
        """
        根据人脸ID获取关系
        
        Args:
            face_id: 人脸ID
            
        Returns:
            Optional[RelationshipProfile]: 关系配置
        """
        return self.profiles.get(face_id)
    
    def get_broadcast_preference(self, face_id: str) -> Dict[str, Any]:
        """
        获取播报偏好
        
        Args:
            face_id: 人脸ID
            
        Returns:
            Dict[str, Any]: 播报偏好
        """
        profile = self.profiles.get(face_id)
        
        if not profile:
            return {
                "preferred_tone": PreferredTone.GENTLE.value,
                "alert_level": AlertLevel.LOW.value,
                "emotion_tag": "neutral"
            }
        
        return {
            "preferred_tone": profile.preferred_tone,
            "alert_level": profile.alert_level,
            "emotion_tag": profile.emotion_tag,
            "social_attributes": profile.social_attributes
        }
    
    def list_all_known_faces(self) -> List[RelationshipProfile]:
        """
        列出所有已知人脸
        
        Returns:
            List[RelationshipProfile]: 关系配置列表
        """
        return list(self.profiles.values())
    
    def update_preference(self, face_id: str, updates: Dict[str, Any]) -> bool:
        """
        更新偏好设置
        
        Args:
            face_id: 人脸ID
            updates: 更新内容
            
        Returns:
            bool: 是否成功
        """
        if face_id not in self.profiles:
            self.logger.warning(f"⚠️ 找不到关系配置: {face_id}")
            return False
        
        profile = self.profiles[face_id]
        
        # 更新字段
        if "preferred_tone" in updates:
            profile.preferred_tone = updates["preferred_tone"]
        if "alert_level" in updates:
            profile.alert_level = updates["alert_level"]
        if "emotion_tag" in updates:
            profile.emotion_tag = updates["emotion_tag"]
        if "nickname" in updates:
            profile.nickname = updates["nickname"]
        if "social_attributes" in updates:
            profile.social_attributes = updates["social_attributes"]
        
        # 保存
        self._save_data()
        
        self.logger.info(f"👥 已更新关系配置: {face_id}")
        
        return True
    
    def _generate_default_nickname(self, relation: str) -> str:
        """生成默认昵称"""
        nickname_map = {
            "mother": "小妈",
            "father": "小爸",
            "brother": "小哥",
            "sister": "小姐"
        }
        return nickname_map.get(relation, "家人")
    
    def _load_data(self):
        """加载数据"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    for face_id, profile_data in data.items():
                        profile = RelationshipProfile(**profile_data)
                        self.profiles[face_id] = profile
                
                self.logger.info(f"✅ 已加载 {len(self.profiles)} 个关系配置")
            except Exception as e:
                self.logger.error(f"⚠️ 加载数据失败: {e}")
    
    def _save_data(self):
        """保存数据"""
        try:
            data = {}
            for face_id, profile in self.profiles.items():
                data[face_id] = profile.to_dict()
            
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self.logger.debug(f"✅ 已保存 {len(self.profiles)} 个关系配置")
        except Exception as e:
            self.logger.error(f"⚠️ 保存数据失败: {e}")


# 全局映射器实例
global_relationship_mapper = RelationshipMapper()

def get_relationship_mapper() -> RelationshipMapper:
    """获取关系映射器实例"""
    return global_relationship_mapper


if __name__ == "__main__":
    # 测试关系映射器
    import logging
    logging.basicConfig(level=logging.INFO)
    
    mapper = RelationshipMapper()
    
    print("=" * 70)
    print("👥 关系图谱映射器测试")
    print("=" * 70)
    
    # 创建配置
    profile = mapper.create_profile("face_001", "mother", "小妈")
    print("\n创建配置:")
    print(json.dumps(profile.to_dict(), ensure_ascii=False, indent=2))
    
    # 获取关系
    relation = mapper.get_relation_by_face("face_001")
    print("\n获取关系:")
    print(json.dumps(relation.to_dict(), ensure_ascii=False, indent=2))
    
    # 获取播报偏好
    preference = mapper.get_broadcast_preference("face_001")
    print("\n播报偏好:")
    print(json.dumps(preference, ensure_ascii=False, indent=2))
    
    print("\n" + "=" * 70)

