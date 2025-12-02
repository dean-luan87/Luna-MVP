"""
视觉-语言融合模块（借鉴Talk2Nav）
用于融合视觉检测结果和语音指令，提高导航准确性
"""

import logging
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class VisualObject:
    """视觉对象"""
    class_name: str
    bbox: tuple  # (x, y, w, h)
    confidence: float
    text: Optional[str] = None  # OCR识别的文字

@dataclass
class LanguageIntent:
    """语言意图"""
    action: str  # 'go_to', 'find', 'navigate'
    target: str  # 'toilet', 'elevator', 'room_101'
    location: Optional[str] = None  # '三楼', 'left', 'right'

class VisualLanguageFusion:
    """视觉-语言融合模块（借鉴Talk2Nav的双重注意力机制）"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # 关键词映射表
        self.facility_keywords = {
            'toilet': ['洗手间', '卫生间', '厕所', 'toilet', 'restroom', 'WC'],
            'elevator': ['电梯', 'elevator', 'lift', '升降机'],
            'exit': ['出口', 'exit', 'entrance', '入口'],
            'stairs': ['楼梯', 'stairs', 'staircase'],
            'room': ['房间', 'room', '室', '号']
        }
        
        self.direction_keywords = {
            'left': ['左', 'left', '←'],
            'right': ['右', 'right', '→'],
            'forward': ['直行', 'straight', 'forward', '↑', '前'],
            'back': ['后退', 'back', '↓', '后']
        }
        
        self.logger.info("✅ 视觉-语言融合模块初始化完成")
    
    def fuse(self, visual_detection: Dict[str, Any], voice_command: str) -> Optional[Dict[str, Any]]:
        """
        融合视觉检测和语音指令
        
        Args:
            visual_detection: {
                'objects': List[VisualObject],
                'texts': List[str],
                'signboards': List[Dict],
                'room_numbers': List[str]
            }
            voice_command: 用户语音指令（如"我要去洗手间"）
        
        Returns:
            融合后的导航决策，如果没有匹配则返回None
        """
        # 1. 视觉注意力：提取关键物体
        visual_key_objects = self._extract_key_objects(visual_detection)
        
        # 2. 语言注意力：提取指令意图
        language_intent = self._extract_intent(voice_command)
        
        # 3. 交叉匹配：找到视觉中匹配语言指令的物体
        matched_objects = self._match_visual_language(visual_key_objects, language_intent)
        
        # 4. 生成导航决策
        if matched_objects:
            navigation_decision = self._generate_decision(matched_objects, language_intent)
            return navigation_decision
        
        return None
    
    def _extract_key_objects(self, visual_detection: Dict[str, Any]) -> List[VisualObject]:
        """视觉注意力：提取关键物体"""
        key_objects = []
        
        # 提取检测到的物体
        for obj in visual_detection.get('objects', []):
            if isinstance(obj, dict):
                key_objects.append(VisualObject(
                    class_name=obj.get('class', ''),
                    bbox=obj.get('bbox', (0, 0, 0, 0)),
                    confidence=obj.get('confidence', 0.0)
                ))
        
        # 提取标识牌
        for signboard in visual_detection.get('signboards', []):
            if isinstance(signboard, dict):
                sign_type = signboard.get('type', '')
                key_objects.append(VisualObject(
                    class_name=f"{sign_type}_sign",
                    bbox=signboard.get('bbox', (0, 0, 0, 0)),
                    confidence=signboard.get('confidence', 0.0),
                    text=signboard.get('text', '')
                ))
        
        # 提取OCR文字（可能包含房间号、方向指示等）
        for text in visual_detection.get('texts', []):
            if isinstance(text, dict):
                text_content = text.get('text', '')
                # 检查是否是房间号
                room_match = re.search(r'(\d+)[室号]|room\s*(\d+)', text_content, re.IGNORECASE)
                if room_match:
                    key_objects.append(VisualObject(
                        class_name='room_number',
                        bbox=text.get('bbox', (0, 0, 0, 0)),
                        confidence=text.get('confidence', 0.0),
                        text=text_content
                    ))
        
        return key_objects
    
    def _extract_intent(self, voice_command: str) -> LanguageIntent:
        """语言注意力：提取指令意图"""
        voice_lower = voice_command.lower()
        
        # 提取动作
        action = 'go_to'  # 默认动作
        if any(kw in voice_lower for kw in ['找', 'find', '寻找']):
            action = 'find'
        elif any(kw in voice_lower for kw in ['导航', 'navigate', '去', 'go']):
            action = 'go_to'
        
        # 提取目标
        target = None
        location = None
        
        for facility, keywords in self.facility_keywords.items():
            if any(kw in voice_command for kw in keywords):
                target = facility
                break
        
        # 提取位置信息（楼层、方向等）
        floor_match = re.search(r'(\d+)[楼层]|(\d+)[Ff]', voice_command)
        if floor_match:
            location = floor_match.group(1) or floor_match.group(2)
        
        # 提取方向
        for direction, keywords in self.direction_keywords.items():
            if any(kw in voice_command for kw in keywords):
                location = direction
                break
        
        return LanguageIntent(
            action=action,
            target=target or 'unknown',
            location=location
        )
    
    def _match_visual_language(self, visual_objects: List[VisualObject], 
                               language_intent: LanguageIntent) -> List[Dict[str, Any]]:
        """交叉匹配：找到视觉中匹配语言指令的物体"""
        matched_objects = []
        
        for obj in visual_objects:
            match_score = 0.0
            
            # 1. 类别匹配
            if language_intent.target != 'unknown':
                # 检查物体类别是否匹配目标
                if language_intent.target in obj.class_name:
                    match_score += 0.5
                
                # 检查文字内容是否匹配
                if obj.text:
                    for keyword in self.facility_keywords.get(language_intent.target, []):
                        if keyword in obj.text.lower():
                            match_score += 0.3
                            break
            
            # 2. 位置匹配（如果有位置信息）
            if language_intent.location:
                if language_intent.location in obj.text or language_intent.location in obj.class_name:
                    match_score += 0.2
            
            # 3. 置信度加权
            match_score *= obj.confidence
            
            if match_score > 0.3:  # 匹配阈值
                matched_objects.append({
                    'object': obj,
                    'match_score': match_score
                })
        
        # 按匹配度排序
        matched_objects.sort(key=lambda x: x['match_score'], reverse=True)
        
        return matched_objects
    
    def _generate_decision(self, matched_objects: List[Dict[str, Any]], 
                          language_intent: LanguageIntent) -> Dict[str, Any]:
        """生成导航决策"""
        if not matched_objects:
            return None
        
        best_match = matched_objects[0]
        obj = best_match['object']
        
        # 计算方向（基于物体在图像中的位置）
        bbox = obj.bbox
        image_center_x = 320  # 假设图像宽度640
        obj_center_x = bbox[0] + bbox[2] / 2
        
        if obj_center_x < image_center_x - 100:
            direction = 'left'
        elif obj_center_x > image_center_x + 100:
            direction = 'right'
        else:
            direction = 'forward'
        
        # 生成消息
        if language_intent.target == 'toilet':
            message = f"检测到洗手间标识，在您的{'左侧' if direction == 'left' else '右侧' if direction == 'right' else '前方'}"
        elif language_intent.target == 'elevator':
            message = f"检测到电梯标识，在您的{'左侧' if direction == 'left' else '右侧' if direction == 'right' else '前方'}"
        elif obj.class_name == 'room_number':
            message = f"检测到房间号：{obj.text}"
        else:
            message = f"检测到目标物体，在您的{'左侧' if direction == 'left' else '右侧' if direction == 'right' else '前方'}"
        
        return {
            'direction': direction,
            'message': message,
            'confidence': best_match['match_score'],
            'matched_object': {
                'class': obj.class_name,
                'text': obj.text,
                'bbox': obj.bbox
            }
        }






