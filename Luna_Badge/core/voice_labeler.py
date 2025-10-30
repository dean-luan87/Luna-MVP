#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 语音标签器
通过用户语音输入对节点打标签
"""

import logging
from typing import Optional, Dict, Any
from core.whisper_recognizer import get_whisper_recognizer
from core.scene_memory_system import get_scene_memory_system

logger = logging.getLogger(__name__)

class VoiceLabeler:
    """语音标签器"""
    
    def __init__(self):
        """初始化语音标签器"""
        self.whisper = get_whisper_recognizer()
        self.scene_memory = get_scene_memory_system()
        logger.info("🎤 语音标签器初始化完成")
    
    def label_node(self, path_id: str, node_index: int = None, 
                   duration: int = 5) -> Dict[str, Any]:
        """
        通过语音为节点打标签
        
        Args:
            path_id: 路径ID
            node_index: 节点索引（None表示最后一个节点）
            duration: 录音时长
            
        Returns:
            Dict: 标签结果
        """
        try:
            # 获取路径
            path_memory = self.scene_memory.get_path_memory(path_id)
            if not path_memory:
                return {"success": False, "message": "路径不存在"}
            
            # 确定节点
            if node_index is None:
                node_index = len(path_memory.nodes) - 1
            
            if node_index < 0 or node_index >= len(path_memory.nodes):
                return {"success": False, "message": "节点索引无效"}
            
            node = path_memory.nodes[node_index]
            
            # 录音并识别
            text, details = self.whisper.recognize_from_microphone(duration=duration)
            
            if not text or len(text) < 2:
                return {"success": False, "message": "未识别到有效语音"}
            
            # 更新节点标签
            old_label = node.label
            node.label = text
            
            # 保存
            self.scene_memory.memory_mapper.save_memories()
            
            logger.info(f"✅ 节点标签已更新: {old_label} -> {text}")
            
            return {
                "success": True,
                "message": "标签更新成功",
                "old_label": old_label,
                "new_label": text,
                "confidence": details.get('confidence', 0)
            }
            
        except Exception as e:
            logger.error(f"❌ 语音标签失败: {e}")
            return {"success": False, "message": str(e)}
    
    def batch_label(self, path_id: str, labels: list) -> Dict[str, Any]:
        """
        批量标签节点（非语音方式）
        
        Args:
            path_id: 路径ID
            labels: 标签列表
            
        Returns:
            Dict: 批量标签结果
        """
        try:
            path_memory = self.scene_memory.get_path_memory(path_id)
            if not path_memory:
                return {"success": False, "message": "路径不存在"}
            
            updated_count = 0
            for i, label in enumerate(labels[:len(path_memory.nodes)]):
                path_memory.nodes[i].label = label
                updated_count += 1
            
            self.scene_memory.memory_mapper.save_memories()
            
            return {
                "success": True,
                "message": f"批量标签成功",
                "updated_count": updated_count
            }
            
        except Exception as e:
            logger.error(f"❌ 批量标签失败: {e}")
            return {"success": False, "message": str(e)}


if __name__ == "__main__":
    # 测试语音标签器
    import logging
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 60)
    print("🎤 语音标签器测试")
    print("=" * 60)
    
    labeler = VoiceLabeler()
    
    # 批量标签测试
    result = labeler.batch_label("test_hospital_path", ["挂号区", "心电图室", "报告领取处"])
    print(f"\n批量标签结果: {result}")
    
    print("\n" + "=" * 60)


