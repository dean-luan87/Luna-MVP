#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 用户反馈处理器
处理用户的修正和反馈
"""

import logging
from typing import Optional, Dict, Any
from core.whisper_recognizer import get_whisper_recognizer
from core.scene_memory_system import get_scene_memory_system
from core.tts_manager import speak, TTSStyle

logger = logging.getLogger(__name__)

class UserFeedbackHandler:
    """用户反馈处理器"""
    
    def __init__(self):
        """初始化反馈处理器"""
        self.whisper = get_whisper_recognizer()
        self.scene_memory = get_scene_memory_system()
        
        # 反馈命令关键词
        self.correction_keywords = {
            "修改": "modify",
            "删除": "delete",
            "更正": "correct",
            "调整": "adjust",
            "重新": "retry"
        }
        
        logger.info("💬 用户反馈处理器初始化完成")
    
    def process_feedback(self, path_id: str, feedback_type: str, 
                        target_index: int, new_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理用户反馈
        
        Args:
            path_id: 路径ID
            feedback_type: 反馈类型（modify/delete/add）
            target_index: 目标节点索引
            new_data: 新数据
            
        Returns:
            Dict: 处理结果
        """
        try:
            path_memory = self.scene_memory.get_path_memory(path_id)
            if not path_memory:
                return {"success": False, "message": "路径不存在"}
            
            if target_index < 0 or target_index >= len(path_memory.nodes):
                return {"success": False, "message": "节点索引无效"}
            
            # 根据类型处理
            if feedback_type == "modify":
                # 修改节点
                node = path_memory.nodes[target_index]
                
                if "label" in new_data:
                    old_label = node.label
                    node.label = new_data["label"]
                    logger.info(f"✅ 节点标签已修改: {old_label} -> {node.label}")
                
                if "notes" in new_data:
                    node.notes = new_data["notes"]
                    logger.info(f"✅ 节点备注已修改")
                
            elif feedback_type == "delete":
                # 删除节点
                removed_node = path_memory.nodes.pop(target_index)
                logger.info(f"✅ 节点已删除: {removed_node.label}")
                
            elif feedback_type == "add":
                # 添加节点（需要提供完整节点数据）
                # 这里简化处理，实际需要更完整的节点创建逻辑
                pass
            
            # 保存
            self.scene_memory.memory_mapper.save_memories()
            
            return {
                "success": True,
                "message": f"反馈处理成功",
                "type": feedback_type
            }
            
        except Exception as e:
            logger.error(f"❌ 反馈处理失败: {e}")
            return {"success": False, "message": str(e)}
    
    def listen_for_feedback(self, path_id: str, duration: int = 5) -> Dict[str, Any]:
        """
        听取用户反馈
        
        Args:
            path_id: 路径ID
            duration: 录音时长
            
        Returns:
            Dict: 反馈结果
        """
        try:
            # 询问用户
            speak("请说出您的反馈", style=TTSStyle.GENTLE)
            
            # 录音并识别
            text, details = self.whisper.recognize_from_microphone(duration=duration)
            
            if not text:
                return {"success": False, "message": "未识别到语音"}
            
            # 解析反馈类型
            feedback_type = self._parse_feedback_type(text)
            
            # 尝试解析节点编号
            node_index = self._parse_node_number(text)
            
            if feedback_type and node_index is not None:
                # 处理反馈
                result = self.process_feedback(path_id, feedback_type, node_index, {})
                
                # 语音反馈
                if result["success"]:
                    speak("已收到您的反馈，修改已保存", style=TTSStyle.CHEERFUL)
                else:
                    speak("抱歉，处理失败，请重试", style=TTSStyle.GENTLE)
                
                return result
            else:
                # 未能解析反馈
                speak("抱歉，未能理解您的反馈，请再说一遍", style=TTSStyle.GENTLE)
                return {"success": False, "message": "未能解析反馈"}
            
        except Exception as e:
            logger.error(f"❌ 听取反馈失败: {e}")
            return {"success": False, "message": str(e)}
    
    def _parse_feedback_type(self, text: str) -> Optional[str]:
        """
        解析反馈类型
        
        Args:
            text: 用户输入的文本
            
        Returns:
            Optional[str]: 反馈类型
        """
        text_lower = text.lower()
        
        if any(kw in text_lower for kw in ["删除", "删除", "delete"]):
            return "delete"
        elif any(kw in text_lower for kw in ["修改", "更正", "adjust", "correct"]):
            return "modify"
        elif any(kw in text_lower for kw in ["添加", "add"]):
            return "add"
        else:
            return None
    
    def _parse_node_number(self, text: str) -> Optional[int]:
        """
        解析节点编号
        
        Args:
            text: 用户输入的文本
            
        Returns:
            Optional[int]: 节点索引
        """
        import re
        
        # 尝试提取数字
        numbers = re.findall(r'\d+', text)
        if numbers:
            return int(numbers[0]) - 1  # 转换为0-based索引
        
        # 尝试中文数字
        chinese_numbers = {
            "一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
            "六": 6, "七": 7, "八": 8, "九": 9, "十": 10
        }
        
        for cn_char, num in chinese_numbers.items():
            if cn_char in text:
                return num - 1
        
        return None


if __name__ == "__main__":
    # 测试用户反馈处理器
    import logging
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 60)
    print("💬 用户反馈处理器测试")
    print("=" * 60)
    
    handler = UserFeedbackHandler()
    
    # 测试修改节点
    print("\n1. 测试修改节点:")
    result = handler.process_feedback(
        "test_hospital_path",
        "modify",
        0,
        {"label": "挂号处（修改）"}
    )
    print(f"   结果: {result}")
    
    print("\n" + "=" * 60)
