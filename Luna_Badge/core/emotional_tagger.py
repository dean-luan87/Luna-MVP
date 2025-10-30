#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
情绪标注器
分析用户语音注释或反馈笔记，提取情绪标签
支持关键词映射到emoji或预定义的标签列表
"""

import json
import os
import logging
from typing import Dict, List, Optional, Set
import re

logger = logging.getLogger(__name__)

class EmotionalTagger:
    """情绪标注器"""
    
    def __init__(self):
        """初始化情绪标注器"""
        # 情绪关键词映射
        self.emotion_keywords = {
            # 正面情绪
            "热闹": ["热闹", "活跃", "繁华", "熙攘", "人声鼎沸", "烟火气"],
            "推荐": ["推荐", "好评", "很赞", "不错", "棒", "好", "值得", "推荐", "nice"],
            "温馨": ["温馨", "温暖", "舒适", "惬意", "舒心", "放松"],
            "安静": ["安静", "清静", "宁静", "幽静", "僻静", "安宁", "静谧"],
            "宽敞": ["宽敞", "开阔", "空旷", "宽阔", "宽大", "空旷"],
            "明亮": ["明亮", "亮堂", "光鲜", "敞亮", "亮"],
            "整洁": ["整洁", "干净", "洁净", "利落", "清爽"],
            
            # 负面情绪
            "嘈杂": ["嘈杂", "吵闹", "喧闹", "嘈杂", "聒噪", "烦人"],
            "拥挤": ["拥挤", "挤", "密", "密不透风", "人满为患", "水泄不通"],
            "昏暗": ["昏暗", "阴暗", "阴暗", "黑", "不亮"],
            "脏乱": ["脏", "乱", "邋遢", "不干净", "污渍", "脏乱差"],
            "烦躁": ["烦躁", "烦", "焦虑", "着急", "焦急", "心急"],
            "等待": ["等待", "排队", "久等", "慢", "拖沓"],
            
            # 中性/功能性标签
            "交通枢纽": ["换乘", "转乘", "中转", "枢纽"],
            "无障碍": ["无障碍", "残障", "轮椅", "残疾人"],
            "紧急": ["紧急", "急救", "急诊", "急"],
            "无障碍电梯": ["无障碍电梯", "残疾人电梯", "轮椅电梯"],
        }
        
        # emoji映射
        self.emotion_emoji = {
            "热闹": "🎉",
            "推荐": "⭐",
            "温馨": "💝",
            "安静": "🤫",
            "宽敞": "🏛️",
            "明亮": "💡",
            "整洁": "✨",
            "嘈杂": "🔊",
            "拥挤": "👥",
            "昏暗": "🌙",
            "脏乱": "🚫",
            "烦躁": "😤",
            "等待": "⏳",
            "交通枢纽": "🚇",
            "无障碍": "♿",
            "紧急": "🚨",
            "无障碍电梯": "♿",
        }
        
        logger.info("💬 情绪标注器初始化完成")
    
    def extract_emotion_tags(self, note: str) -> List[str]:
        """
        从文本中提取情绪标签
        
        Args:
            note: 用户输入文本
            
        Returns:
            List[str]: 情绪标签列表
        """
        if not note:
            return []
        
        # 转换为小写并去除空格
        note_lower = note.lower()
        
        # 匹配的情绪标签
        matched_tags = set()
        
        # 遍历所有情绪关键词
        for emotion, keywords in self.emotion_keywords.items():
            for keyword in keywords:
                # 检查关键词是否在文本中
                if keyword in note_lower:
                    matched_tags.add(emotion)
                    break  # 找到一个就够
        
        # 特殊匹配规则
        matched_tags.update(self._apply_special_rules(note_lower))
        
        return sorted(list(matched_tags))
    
    def _apply_special_rules(self, text: str) -> Set[str]:
        """应用特殊的匹配规则"""
        tags = set()
        
        # 等待时间判断
        if re.search(r'(\d+)\s*分钟.*等', text) or re.search(r'等了\s*(\d+)', text):
            tags.add("等待")
        
        # 人数判断
        if re.search(r'人.*多|拥挤|挤|爆满', text):
            tags.add("拥挤")
        elif re.search(r'人少|没.*人|空.*旷', text):
            tags.add("安静")
        
        # 亮度判断
        if re.search(r'亮.*堂|光.*线.*好|明.*亮', text):
            tags.add("明亮")
        elif re.search(r'暗|光线.*不好|黑', text):
            tags.add("昏暗")
        
        # 清洁度判断
        if re.search(r'干净|整洁|清爽', text):
            tags.add("整洁")
        elif re.search(r'脏|乱|不.*干净', text):
            tags.add("脏乱")
        
        # 交通相关
        if re.search(r'换.*乘|转.*乘|中.*转', text):
            tags.add("交通枢纽")
        
        # 无障碍相关
        if re.search(r'无.*障碍|残.*障|轮椅|残疾人', text):
            tags.add("无障碍")
        
        return tags
    
    def tag_nodes_with_emotion(self, memory_store_path: str, 
                              output_path: str = None) -> Dict:
        """
        为记忆存储中的所有节点标注情绪
        
        Args:
            memory_store_path: 记忆存储文件路径
            output_path: 输出文件路径（如果为None则覆盖原文件）
            
        Returns:
            Dict: 标注统计信息
        """
        if output_path is None:
            output_path = memory_store_path
        
        try:
            # 读取数据
            with open(memory_store_path, 'r', encoding='utf-8') as f:
                memory_data = json.load(f)
            
            if "paths" not in memory_data:
                logger.error("记忆存储中没有路径数据")
                return {"error": "No paths data"}
            
            # 统计信息
            stats = {
                "total_nodes": 0,
                "tagged_nodes": 0,
                "total_tags": 0,
                "tag_distribution": {}
            }
            
            # 为每个节点标注情绪
            for path in memory_data["paths"]:
                nodes = path.get("nodes", [])
                
                for node in nodes:
                    stats["total_nodes"] += 1
                    
                    # 提取标注文本（优先使用note，其次使用label）
                    annotation = node.get("note", "") or node.get("label", "")
                    
                    if annotation:
                        # 提取情绪标签
                        tags = self.extract_emotion_tags(annotation)
                        
                        if tags:
                            # 更新节点的emotion字段
                            # 如果已有emotion，合并去重
                            existing_emotion = node.get("emotion", [])
                            if isinstance(existing_emotion, str):
                                existing_emotion = [existing_emotion]
                            
                            all_tags = sorted(set(existing_emotion + tags))
                            
                            # 只保留主标签（最多3个）
                            node["emotion"] = all_tags[:3]
                            stats["tagged_nodes"] += 1
                            stats["total_tags"] += len(node["emotion"])
                            
                            # 统计标签分布
                            for tag in node["emotion"]:
                                if tag not in stats["tag_distribution"]:
                                    stats["tag_distribution"][tag] = 0
                                stats["tag_distribution"][tag] += 1
                            
                            logger.debug(f"节点 {node.get('label', 'N/A')}: {node['emotion']}")
            
            # 保存更新后的数据
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(memory_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ 情绪标注完成:")
            logger.info(f"   - 总节点数: {stats['total_nodes']}")
            logger.info(f"   - 已标注节点: {stats['tagged_nodes']}")
            logger.info(f"   - 标签总数: {stats['total_tags']}")
            
            # 打印标签分布
            logger.info("\n💬 标签分布:")
            for tag, count in sorted(stats["tag_distribution"].items(), 
                                    key=lambda x: x[1], reverse=True):
                emoji = self.emotion_emoji.get(tag, "")
                logger.info(f"  {emoji} {tag}: {count}")
            
            return stats
            
        except FileNotFoundError:
            logger.error(f"文件不存在: {memory_store_path}")
            return {"error": "File not found"}
        except json.JSONDecodeError:
            logger.error(f"文件格式错误: {memory_store_path}")
            return {"error": "JSON decode error"}
        except Exception as e:
            logger.error(f"情绪标注失败: {e}")
            import traceback
            traceback.print_exc()
            return {"error": str(e)}
    
    def get_emotion_emoji(self, emotion_tag: str) -> str:
        """获取情绪标签对应的emoji"""
        return self.emotion_emoji.get(emotion_tag, "📍")
    
    def add_custom_emotion(self, tag: str, keywords: List[str], emoji: str = "📍") -> None:
        """
        添加自定义情绪标签
        
        Args:
            tag: 标签名称
            keywords: 关键词列表
            emoji: 对应的emoji
        """
        self.emotion_keywords[tag] = keywords
        self.emotion_emoji[tag] = emoji
        logger.info(f"✅ 添加自定义情绪: {tag} ({emoji})")

def main():
    """测试主函数"""
    import sys
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    tagger = EmotionalTagger()
    
    # 测试提取情绪标签
    test_notes = [
        "这个医院人很多，环境很嘈杂",
        "卫生间很干净，推荐使用",
        "等候大厅宽敞明亮，很温馨",
        "需要等待30分钟，有点烦躁",
        "地铁换乘点，人来人往很热闹",
        "无障碍电梯很方便，轮椅可通行",
        "急诊科就在旁边，紧急情况可用",
        "这个地方很安静，适合休息",
    ]
    
    print("\n=== 情绪标签提取测试 ===")
    for note in test_notes:
        tags = tagger.extract_emotion_tags(note)
        emojis = [tagger.get_emotion_emoji(tag) for tag in tags]
        print(f"文本: {note}")
        print(f"  标签: {tags}")
        print(f"  Emoji: {' '.join(emojis)}")
        print()
    
    # 测试批量标注
    memory_file = "data/memory_store.json"
    if os.path.exists(memory_file):
        print("\n=== 批量标注情绪标签 ===")
        stats = tagger.tag_nodes_with_emotion(memory_file)
        print(f"\n标注统计: {stats}")

if __name__ == "__main__":
    main()


