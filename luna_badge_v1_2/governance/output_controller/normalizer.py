"""
Output Normalizer

模型输出归一化器。
"""

from typing import Dict, Any, Optional


class OutputNormalizer:
    """
    输出归一化器
    
    职责：
    - 将不同模型的输出格式统一为标准格式
    - 不改变语义，只做格式转换
    - v1.5: 规则化映射，不引入学习
    """
    
    def __init__(self):
        """初始化归一化器"""
        # v1.5: 使用固定映射规则，不动态学习
        pass

    def normalize(self, task_domain: str, raw_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        将模型原始输出转换为任务域标准格式
        
        Args:
            task_domain: 任务领域（如 "navigation", "safety", "inquiry"）
            raw_output: 模型原始输出，必须包含 model_id 和原始输出内容
            
        Returns:
            标准化后的输出结构：
            {
                "model_id": str,
                "model_version": str,
                "data": Any,  # 核心数据
                "confidence": Optional[float],
                "meta": Dict[str, Any]  # 元数据
            }
        """
        # 提取模型信息
        model_id = raw_output.get("model_id", "unknown")
        model_version = raw_output.get("model_version", "unknown")
        
        # v1.5: 简单字段映射，不判断对错，只管"像不像人话"
        # 不同模型的输出字段名可能不同，统一映射到标准字段
        normalized = {
            "model_id": model_id,
            "model_version": model_version,
            "data": raw_output.get("result") or raw_output.get("data") or raw_output.get("output"),
            "confidence": raw_output.get("confidence") or raw_output.get("score"),
            "meta": raw_output.get("meta", {})
        }
        
        # 如果原始输出有额外字段，保留在 meta 中
        for key, value in raw_output.items():
            if key not in ["model_id", "model_version", "result", "data", "output", "confidence", "score", "meta"]:
                normalized["meta"][key] = value
        
        return normalized





