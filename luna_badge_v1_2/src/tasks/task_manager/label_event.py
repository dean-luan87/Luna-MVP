# label_event.py

"""
标签事件：当标签被识别时触发
"""


class LabelEvent:
    def __init__(self, label, confidence, source="unknown"):
        """
        标签事件
        
        参数：
        - label: 标签字符串
        - confidence: 置信度 (0~1)
        - source: 来源 (OCR/YOLO/Scene)
        """
        self.label = label
        self.confidence = confidence
        self.source = source
    
    def __repr__(self):
        return f"LabelEvent(label={self.label}, confidence={self.confidence:.2f}, source={self.source})"










