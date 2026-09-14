"""
负责将 vision_bundle 转成可返回的 JSON 结构 (v1.2.0)
"""

import json
from typing import Any, Dict, Optional
from datetime import datetime


class VisualSerializer:
    """视觉序列化器"""
    
    @staticmethod
    def dumps(data: Any, ensure_ascii: bool = False, indent: Optional[int] = None) -> str:
        """
        将数据序列化为JSON字符串
        
        Args:
            data: 要序列化的数据
            ensure_ascii: 是否确保ASCII编码
            indent: 缩进级别（None表示不缩进）
        
        Returns:
            JSON字符串
        """
        return json.dumps(data, ensure_ascii=ensure_ascii, indent=indent, default=str)
    
    @staticmethod
    def loads(json_str: str) -> Any:
        """
        将JSON字符串反序列化为Python对象
        
        Args:
            json_str: JSON字符串
        
        Returns:
            Python对象
        """
        return json.loads(json_str)
    
    @staticmethod
    def serialize_with_metadata(data: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        序列化数据并添加元数据
        
        Args:
            data: 要序列化的数据
            metadata: 元数据字典
        
        Returns:
            包含元数据的JSON字符串
        """
        result = {
            "data": data,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        }
        return VisualSerializer.dumps(result)
    
    @staticmethod
    def serialize_for_api(data: Dict[str, Any], success: bool = True, error_code: int = 0) -> str:
        """
        序列化为API响应格式
        
        Args:
            data: 响应数据
            success: 是否成功
            error_code: 错误码
        
        Returns:
            API响应格式的JSON字符串
        """
        response = {
            "success": success,
            "code": error_code,
            "timestamp": int(datetime.now().timestamp() * 1000),
            "data": data
        }
        return VisualSerializer.dumps(response)

