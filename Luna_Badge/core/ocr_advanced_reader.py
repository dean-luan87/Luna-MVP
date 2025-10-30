#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge OCR识别增强模块
支持识别图文混排结构（如说明书、使用手册）
"""

import logging
import cv2
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import re
import time

logger = logging.getLogger(__name__)

class ContentType(Enum):
    """内容类型"""
    TITLE = "title"             # 标题
    SUBTITLE = "subtitle"       # 副标题
    PARAGRAPH = "paragraph"     # 段落
    BULLET_POINT = "bullet_point"  # 要点
    WARNING = "warning"         # 警告
    NOTE = "note"              # 注意事项
    LIST_ITEM = "list_item"     # 列表项
    UNKNOWN = "unknown"        # 未知

@dataclass
class OCRTextBlock:
    """OCR文本块"""
    text: str                  # 文本内容
    content_type: ContentType  # 内容类型
    confidence: float          # 置信度
    bbox: Tuple[int, int, int, int]  # 边界框
    language: str              # 语言 (zh/en)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "text": self.text,
            "content_type": self.content_type.value,
            "confidence": self.confidence,
            "bbox": self.bbox,
            "language": self.language
        }

@dataclass
class OCRResult:
    """OCR结果"""
    text: str                  # 完整文本
    blocks: List[OCRTextBlock]  # 文本块
    summary: str              # 结构化摘要
    language: str             # 主要语言
    timestamp: float          # 时间戳
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "text": self.text,
            "blocks": [b.to_dict() for b in self.blocks],
            "summary": self.summary,
            "language": self.language,
            "timestamp": self.timestamp
        }

class OCRAdvancedReader:
    """OCR高级阅读器"""
    
    def __init__(self):
        """初始化OCR阅读器"""
        self.logger = logging.getLogger(__name__)
        
        # 标题模式
        self.title_patterns = [
            r'^[一二三四五六七八九十\d]+[\.、．\s]',  # 数字编号标题
            r'^第[一二三四五六七八九十\d]+[章节]',      # 章节标题
            r'^[A-Z][a-z]+\s+\d+',                     # 英文编号
        ]
        
        # 要点模式
        self.bullet_patterns = [
            r'^[•·▪▫●○]',  # 圆点
            r'^[①②③④⑤⑥⑦⑧⑨⑩]',  # 圆圈数字
            r'^[\d]+[\.\)）]',  # 数字编号
            r'^[a-zA-Z][\.\)）]',  # 字母编号
        ]
        
        # 警告模式
        self.warning_patterns = [
            r'警告|WARNING',
            r'注意|CAUTION',
            r'危险|DANGER',
            r'禁止|FORBIDDEN',
        ]
        
        # 注意事项模式
        self.note_patterns = [
            r'注意|NOTE',
            r'提示|TIP',
            r'建议|SUGGESTION',
        ]
        
        self.logger.info("📄 OCR高级阅读器初始化完成")
    
    def read_document(self, image: np.ndarray) -> OCRResult:
        """
        读取文档
        
        Args:
            image: 输入图像
            
        Returns:
            OCRResult: OCR结果
        """
        try:
            # 模拟OCR识别（实际应使用Tesseract或PaddleOCR）
            text = self._simulate_ocr(image)
            
            # 检测语言
            language = self._detect_language(text)
            
            # 文本块分割
            blocks = self._segment_text(text, image.shape)
            
            # 分类内容类型
            blocks = self._classify_blocks(blocks)
            
            # 生成摘要
            summary = self._generate_summary(blocks)
            
            result = OCRResult(
                text=text,
                blocks=blocks,
                summary=summary,
                language=language,
                timestamp=time.time()
            )
            
            self.logger.info(f"📄 OCR识别完成: {len(blocks)}个块, 语言={language}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"OCR识别失败: {e}")
            return OCRResult(
                text="",
                blocks=[],
                summary="",
                language="unknown",
                timestamp=time.time()
            )
    
    def _simulate_ocr(self, image: np.ndarray) -> str:
        """
        模拟OCR识别（占位符实现）
        
        Args:
            image: 输入图像
            
        Returns:
            str: 识别的文本
        """
        # 实际的OCR实现应该使用pytesseract或PaddleOCR
        # 这里返回模拟数据用于测试
        
        sample_text = """产品使用说明书
一、产品简介
本产品是一款智能导航设备，专为视障用户设计。

二、注意事项
1. 请妥善保管设备
2. 避免水浸
• 保持干燥
• 定期充电
3. 首次使用请先充电

三、警告
警告：请勿在极端环境下使用
危险：禁止私自拆卸设备"""
        
        return sample_text
    
    def _detect_language(self, text: str) -> str:
        """
        检测语言
        
        Args:
            text: 文本
            
        Returns:
            str: 语言代码 (zh/en/mixed)
        """
        # 简单的语言检测
        zh_pattern = r'[\u4e00-\u9fa5]'
        en_pattern = r'[a-zA-Z]'
        
        zh_count = len(re.findall(zh_pattern, text))
        en_count = len(re.findall(en_pattern, text))
        
        total = zh_count + en_count
        
        if total == 0:
            return "unknown"
        
        if zh_count > total * 0.5:
            return "zh"
        elif en_count > total * 0.5:
            return "en"
        else:
            return "mixed"
    
    def _segment_text(self, text: str, image_shape: Tuple[int, int, int]) -> List[OCRTextBlock]:
        """
        文本分割
        
        Args:
            text: 完整文本
            image_shape: 图像尺寸
            
        Returns:
            List[OCRTextBlock]: 文本块列表
        """
        blocks = []
        lines = text.split('\n')
        
        height, width = image_shape[:2]
        line_height = height / max(len(lines), 1)
        
        for i, line in enumerate(lines):
            if not line.strip():
                continue
            
            # 估算边界框
            bbox = (10, int(i * line_height), width - 20, int(line_height))
            
            block = OCRTextBlock(
                text=line.strip(),
                content_type=ContentType.UNKNOWN,
                confidence=0.9,  # 模拟置信度
                bbox=bbox,
                language="mixed"
            )
            
            blocks.append(block)
        
        return blocks
    
    def _classify_blocks(self, blocks: List[OCRTextBlock]) -> List[OCRTextBlock]:
        """
        分类文本块
        
        Args:
            blocks: 文本块列表
            
        Returns:
            List[OCRTextBlock]: 分类后的文本块
        """
        for block in blocks:
            text = block.text
            
            # 检查标题
            if any(re.match(pattern, text) for pattern in self.title_patterns):
                block.content_type = ContentType.TITLE
                continue
            
            # 检查要点
            if any(re.match(pattern, text) for pattern in self.bullet_patterns):
                block.content_type = ContentType.BULLET_POINT
                continue
            
            # 检查警告
            if any(re.search(pattern, text, re.IGNORECASE) for pattern in self.warning_patterns):
                block.content_type = ContentType.WARNING
                continue
            
            # 检查注意事项
            if any(re.search(pattern, text, re.IGNORECASE) for pattern in self.note_patterns):
                block.content_type = ContentType.NOTE
                continue
            
            # 默认段落
            block.content_type = ContentType.PARAGRAPH
        
        return blocks
    
    def _generate_summary(self, blocks: List[OCRTextBlock]) -> str:
        """
        生成结构化摘要
        
        Args:
            blocks: 文本块列表
            
        Returns:
            str: 摘要文本
        """
        summary_parts = []
        
        for block in blocks:
            if block.content_type == ContentType.TITLE:
                summary_parts.append(f"标题: {block.text}")
            elif block.content_type == ContentType.BULLET_POINT:
                summary_parts.append(f"  • {block.text}")
            elif block.content_type == ContentType.WARNING:
                summary_parts.append(f"⚠️ 警告: {block.text}")
            elif block.content_type == ContentType.NOTE:
                summary_parts.append(f"📌 注意: {block.text}")
        
        return '\n'.join(summary_parts)
    
    def extract_key_points(self, ocr_result: OCRResult) -> List[str]:
        """
        提取关键要点
        
        Args:
            ocr_result: OCR结果
            
        Returns:
            List[str]: 关键要点列表
        """
        key_points = []
        
        for block in ocr_result.blocks:
            if block.content_type in [
                ContentType.BULLET_POINT,
                ContentType.WARNING,
                ContentType.NOTE
            ]:
                key_points.append(block.text)
        
        return key_points


# 全局阅读器实例
global_ocr_reader = OCRAdvancedReader()

def read_document(image: np.ndarray) -> OCRResult:
    """读取文档的便捷函数"""
    return global_ocr_reader.read_document(image)


if __name__ == "__main__":
    # 测试OCR高级阅读器
    import logging
    logging.basicConfig(level=logging.INFO)
    
    reader = OCRAdvancedReader()
    
    # 创建测试图像
    test_image = np.ones((480, 640, 3), dtype=np.uint8) * 255
    
    # 读取文档
    result = reader.read_document(test_image)
    
    print("\n" + "=" * 60)
    print("📄 OCR识别结果")
    print("=" * 60)
    
    print(f"\n完整文本:\n{result.text}")
    
    print(f"\n文本块数: {len(result.blocks)}")
    print("\n文本块详情:")
    for i, block in enumerate(result.blocks, 1):
        print(f"  {i}. [{block.content_type.value}] {block.text}")
    
    print(f"\n结构化摘要:\n{result.summary}")
    
    print(f"\n语言: {result.language}")
    
    # 提取关键要点
    key_points = reader.extract_key_points(result)
    print(f"\n关键要点 ({len(key_points)}个):")
    for point in key_points:
        print(f"  • {point}")
    
    print("\n" + "=" * 60)

