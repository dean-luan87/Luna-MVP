"""
OCR扫描器
挂号凭证结构化识别
"""

import logging
import cv2
import numpy as np
from typing import Dict, Any, Optional, List, Tuple
import re

logger = logging.getLogger(__name__)


class RegistrationOCRScanner:
    """挂号凭证OCR扫描器"""
    
    def __init__(self):
        """初始化OCR扫描器"""
        self.logger = logging.getLogger(__name__)
        
        # 科室关键词映射
        self.department_keywords = {
            "内科": ["内科", "内"],
            "外科": ["外科", "外"],
            "儿科": ["儿科", "儿"],
            "妇科": ["妇科", "妇"],
            "牙科": ["牙科", "口腔科", "口腔", "牙"],
            "眼科": ["眼科", "眼"],
            "耳鼻喉科": ["耳鼻喉科", "耳鼻喉", "耳"],
            "皮肤科": ["皮肤科", "皮肤"],
            "精神科": ["精神科", "精神", "心理"]
        }
        
        # 楼层关键词
        self.floor_keywords = ["楼", "层", "F", "floor"]
        
        # 房间号关键词
        self.room_keywords = ["室", "号", "房", "诊室"]
        
        self.logger.info("📄 OCR扫描器初始化完成")
    
    def scan_registration_slip(self, image: np.ndarray) -> Dict[str, Any]:
        """
        扫描挂号凭条
        
        Args:
            image: 输入图像
        
        Returns:
            Dict[str, Any]: 识别结果
        """
        try:
            # 图像预处理
            processed_image = self._preprocess_image(image)
            
            # 文本区域检测
            text_regions = self._detect_text_regions(processed_image)
            
            # OCR识别（模拟）
            ocr_results = self._simulate_ocr(text_regions)
            
            # 结构化解析
            parsed_info = self._parse_registration_info(ocr_results)
            
            return {
                "success": True,
                "raw_text": ocr_results,
                "parsed_info": parsed_info,
                "confidence": self._calculate_confidence(parsed_info)
            }
            
        except Exception as e:
            self.logger.error(f"❌ OCR扫描失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "raw_text": [],
                "parsed_info": {},
                "confidence": 0.0
            }
    
    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """图像预处理"""
        # 转换为灰度图
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # 高斯模糊去噪
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        
        # 自适应阈值二值化
        binary = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        return binary
    
    def _detect_text_regions(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """检测文本区域"""
        # 使用轮廓检测
        contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        text_regions = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            # 过滤太小的区域
            if w > 20 and h > 10:
                text_regions.append((x, y, w, h))
        
        return text_regions
    
    def _simulate_ocr(self, text_regions: List[Tuple[int, int, int, int]]) -> List[str]:
        """模拟OCR识别（实际应使用pytesseract或其他OCR引擎）"""
        # 模拟识别结果
        mock_results = [
            "虹口医院",
            "内科",
            "3楼",
            "305室",
            "排队号: 15",
            "2025-10-28 10:30"
        ]
        
        return mock_results
    
    def _parse_registration_info(self, ocr_results: List[str]) -> Dict[str, Any]:
        """解析挂号信息"""
        parsed = {
            "hospital_name": "",
            "department": "",
            "floor": 0,
            "room": "",
            "queue_number": "",
            "appointment_time": "",
            "raw_text": ocr_results
        }
        
        # 解析医院名称
        for text in ocr_results:
            if "医院" in text:
                parsed["hospital_name"] = text
                break
        
        # 解析科室
        for text in ocr_results:
            for dept_name, keywords in self.department_keywords.items():
                if any(keyword in text for keyword in keywords):
                    parsed["department"] = dept_name
                    break
            if parsed["department"]:
                break
        
        # 解析楼层
        for text in ocr_results:
            floor_match = re.search(r'(\d+)[楼|层|F]', text)
            if floor_match:
                parsed["floor"] = int(floor_match.group(1))
                break
        
        # 解析房间号
        for text in ocr_results:
            room_match = re.search(r'(\d+)[室|号|房]', text)
            if room_match:
                parsed["room"] = room_match.group(1)
                break
        
        # 解析排队号
        for text in ocr_results:
            queue_match = re.search(r'排队号[：:]?\s*(\d+)', text)
            if queue_match:
                parsed["queue_number"] = queue_match.group(1)
                break
        
        # 解析预约时间
        for text in ocr_results:
            time_match = re.search(r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})', text)
            if time_match:
                parsed["appointment_time"] = time_match.group(1)
                break
        
        return parsed
    
    def _calculate_confidence(self, parsed_info: Dict[str, Any]) -> float:
        """计算识别置信度"""
        confidence_factors = []
        
        # 医院名称
        if parsed_info["hospital_name"]:
            confidence_factors.append(0.2)
        
        # 科室
        if parsed_info["department"]:
            confidence_factors.append(0.3)
        
        # 楼层
        if parsed_info["floor"] > 0:
            confidence_factors.append(0.2)
        
        # 房间号
        if parsed_info["room"]:
            confidence_factors.append(0.2)
        
        # 排队号
        if parsed_info["queue_number"]:
            confidence_factors.append(0.1)
        
        return sum(confidence_factors)
    
    def validate_registration_info(self, parsed_info: Dict[str, Any]) -> Dict[str, Any]:
        """验证挂号信息完整性"""
        missing_fields = []
        
        if not parsed_info["hospital_name"]:
            missing_fields.append("医院名称")
        
        if not parsed_info["department"]:
            missing_fields.append("科室")
        
        if parsed_info["floor"] == 0:
            missing_fields.append("楼层")
        
        if not parsed_info["room"]:
            missing_fields.append("房间号")
        
        is_complete = len(missing_fields) == 0
        
        return {
            "is_complete": is_complete,
            "missing_fields": missing_fields,
            "confidence": parsed_info.get("confidence", 0.0)
        }


# 全局OCR扫描器实例
_global_ocr_scanner: Optional[RegistrationOCRScanner] = None


def get_ocr_scanner() -> RegistrationOCRScanner:
    """获取全局OCR扫描器实例"""
    global _global_ocr_scanner
    if _global_ocr_scanner is None:
        _global_ocr_scanner = RegistrationOCRScanner()
    return _global_ocr_scanner


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("📄 OCR扫描器测试")
    print("=" * 70)
    
    scanner = get_ocr_scanner()
    
    # 测试1: 模拟图像扫描
    print("\n1. 模拟图像扫描...")
    mock_image = np.zeros((200, 400, 3), dtype=np.uint8)
    result = scanner.scan_registration_slip(mock_image)
    
    print(f"   扫描成功: {result['success']}")
    print(f"   置信度: {result['confidence']:.2f}")
    print(f"   解析信息: {result['parsed_info']}")
    
    # 测试2: 验证信息完整性
    print("\n2. 验证信息完整性...")
    validation = scanner.validate_registration_info(result['parsed_info'])
    print(f"   信息完整: {validation['is_complete']}")
    if validation['missing_fields']:
        print(f"   缺失字段: {validation['missing_fields']}")
    
    print("\n" + "=" * 70)

