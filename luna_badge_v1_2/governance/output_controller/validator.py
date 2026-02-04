"""
Output Validator

模型输出验证器。
"""

from typing import Dict, Any, Tuple


class OutputValidator:
    """
    输出验证器
    
    职责：
    - 验证模型输出的有效性
    - 检查输出是否符合领域约束
    - v1.5: 只做结构校验，不做语义判断
    """
    
    def __init__(self):
        """初始化验证器"""
        # v1.5: 固定验证规则，不动态调整
        pass

    def validate(self, normalized_output: Dict[str, Any]) -> Tuple[bool, str]:
        """
        校验输出是否可被系统使用
        
        Args:
            normalized_output: 归一化后的输出
            
        Returns:
            (is_valid: bool, reason: str)
        """
        # 1. 必需字段检查
        required_fields = ["model_id", "data"]
        for field in required_fields:
            if field not in normalized_output:
                return False, f"Missing required field: {field}"
        
        # 2. data 字段不能为 None（空数据视为无效）
        if normalized_output["data"] is None:
            return False, "Data field is None"
        
        # 3. model_id 必须是非空字符串
        if not isinstance(normalized_output["model_id"], str) or not normalized_output["model_id"]:
            return False, "Invalid model_id"
        
        # 4. confidence 如果存在，必须在 [0, 1] 范围内
        confidence = normalized_output.get("confidence")
        if confidence is not None:
            if not isinstance(confidence, (int, float)):
                return False, "Confidence must be a number"
            if not (0 <= confidence <= 1):
                return False, "Confidence must be in [0, 1]"

        # 5. 禁止裁决/权限类字段（B 输出边界）
        forbidden_fields = {
            "authority",
            "abilities",
            "gate",
            "decision",
            "must_stop",
            "level",
            "impact",
            "intervention_level",
        }
        for field in forbidden_fields:
            if field in normalized_output:
                return False, f"Forbidden field in output: {field}"
        meta = normalized_output.get("meta", {})
        if isinstance(meta, dict):
            for field in forbidden_fields:
                if field in meta:
                    return False, f"Forbidden field in meta: {field}"
        
        # v1.5: 通过所有基础校验
        return True, "Valid"





