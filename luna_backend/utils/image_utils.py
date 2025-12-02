"""
图像工具函数 (v1.2.0)
"""

import base64
import cv2
import numpy as np
from PIL import Image
import io
from typing import Optional


def decode_base64_image(base64_str: str) -> Optional[np.ndarray]:
    """
    解码base64图片为numpy数组
    
    Args:
        base64_str: base64编码的图片字符串
    
    Returns:
        numpy数组，如果解码失败返回None
    """
    try:
        # 处理data URL格式（data:image/jpeg;base64,...）
        if ',' in base64_str:
            base64_str = base64_str.split(',')[-1]
        
        # 解码base64
        image_bytes = base64.b64decode(base64_str)
        
        # 转换为numpy数组
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            # 尝试用PIL
            img_pil = Image.open(io.BytesIO(image_bytes))
            img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        
        return img
    except Exception as e:
        return None


def image_to_numpy(image_data: bytes) -> Optional[np.ndarray]:
    """
    将图片字节数据转换为numpy数组
    
    Args:
        image_data: 图片字节数据
    
    Returns:
        numpy数组，如果转换失败返回None
    """
    try:
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            # 尝试用PIL
            img_pil = Image.open(io.BytesIO(image_data))
            img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        return img
    except Exception as e:
        return None
