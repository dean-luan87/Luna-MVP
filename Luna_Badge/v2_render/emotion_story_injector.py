#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EmotionMap v2 情绪叙事注入器
为每个节点和路径注入情绪标签、提示文字、叙事引导
"""

import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class EmotionStoryInjector:
    """情绪叙事注入器"""
    
    def __init__(self):
        """初始化注入器"""
        # 情绪预设
        self.emotion_presets = {
            "elevator": ["嘈杂", "推荐"],
            "toilet": ["安静", "推荐"],
            "entrance": ["明亮", "温馨"],
            "hospital": ["安静", "担忧"],
            "stairs": ["安静"],
            "destination": ["温馨", "推荐"],
        }
        
        # 叙事模板
        self.story_templates = {
            "嘈杂": "这里人流较多，请注意安全",
            "安静": "这里比较安静，适合休息",
            "推荐": "推荐途经此处",
            "温馨": "氛围温馨舒适",
            "担忧": "请注意周围环境",
            "明亮": "光线充足，视野开阔",
        }
        
        logger.info("💬 情绪叙事注入器初始化完成")
    
    def inject_emotion_story(self, path_data: Dict) -> Dict:
        """
        为每个节点和路径注入情绪标签、提示文字、叙事引导
        
        Args:
            path_data: 原始路径数据
            
        Returns:
            Dict: 注入情绪后的路径数据
        """
        try:
            # 复制路径数据
            enhanced_data = path_data.copy()
            
            # 处理每个节点
            if "nodes" in enhanced_data:
                for node in enhanced_data["nodes"]:
                    node_type = node.get("type", "").lower()
                    
                    # 注入情绪标签
                    if node_type in self.emotion_presets:
                        emotions = self.emotion_presets[node_type]
                        node["emotion"] = emotions
                        
                        # 生成叙事文字
                        story_texts = []
                        for emotion in emotions:
                            if emotion in self.story_templates:
                                story_texts.append(self.story_templates[emotion])
                        
                        if story_texts:
                            node["story_hint"] = " ".join(story_texts)
            
            logger.info("✅ 情绪叙事注入完成")
            return enhanced_data
            
        except Exception as e:
            logger.error(f"❌ 注入失败: {e}")
            return path_data
    
    def add_path_narrative(self, path_data: Dict) -> Dict:
        """
        添加路径级别的叙事引导
        
        Args:
            path_data: 路径数据
            
        Returns:
            Dict: 添加叙事后的数据
        """
        try:
            # 根据路径类型添加开场白
            path_name = path_data.get("path_name", "")
            
            if "医院" in path_name:
                path_data["opening_narrative"] = "欢迎来到医院导航系统，我将为您提供清晰的路线指引和情绪提示。"
            elif "商城" in path_name or "购物" in path_name:
                path_data["opening_narrative"] = "购物中心导航已就绪，为您标注最舒适的路线。"
            else:
                path_data["opening_narrative"] = "开始导航，祝您旅途愉快。"
            
            return path_data
            
        except Exception as e:
            logger.error(f"❌ 添加叙事失败: {e}")
            return path_data


def main():
    """测试函数"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    injector = EmotionStoryInjector()
    
    # 测试数据
    test_path = {
        "path_id": "test_path",
        "path_name": "医院导航路径",
        "nodes": [
            {"type": "entrance", "label": "医院入口"},
            {"type": "elevator", "label": "电梯"},
            {"type": "toilet", "label": "卫生间"},
        ]
    }
    
    result = injector.inject_emotion_story(test_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

