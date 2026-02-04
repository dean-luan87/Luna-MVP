"""
Conflict Detector

模型输出冲突检测器。
"""

from typing import List, Dict, Any


class ConflictDetector:
    """
    冲突检测器
    
    职责：
    - 检测多个模型输出之间的冲突
    - v1.5: 只做显式冲突检测（字段级对比），不做语义推理
    """
    
    def __init__(self):
        """初始化冲突检测器"""
        # v1.5: 固定冲突规则，不引入模糊匹配
        pass

    def detect(self, normalized_outputs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        检测输出冲突
        
        v1.5 冲突定义（严格、简单）：
        - 同一 task_domain
        - 核心结论字段不同
        - 且都通过 validator
        
        Args:
            normalized_outputs: 归一化后的输出列表（已通过 validator）
            
        Returns:
            冲突描述列表，每个冲突包含：
            {
                "type": str,  # 冲突类型
                "models": List[str],  # 涉及的模型ID列表
                "field": str,  # 冲突字段
                "values": List[Any]  # 不同的值
            }
        """
        conflicts = []
        
        if len(normalized_outputs) < 2:
            # 少于2个输出，无冲突
            return conflicts
        
        # v1.5: 简单字段级冲突检测
        # 比较所有输出的核心字段（data）
        data_values = {}
        for idx, output in enumerate(normalized_outputs):
            model_id = output.get("model_id", f"model_{idx}")
            data = output.get("data")
            
            # 如果 data 是字典，比较关键字段
            if isinstance(data, dict):
                # 对于字典类型，比较所有键值对
                data_key = str(sorted(data.items()))
            else:
                # 对于非字典类型，直接比较值
                data_key = str(data)
            
            if data_key not in data_values:
                data_values[data_key] = []
            data_values[data_key].append({
                "model_id": model_id,
                "value": data
            })
        
        # 如果同一个 data_key 对应多个模型，且值不同，则存在冲突
        if len(data_values) > 1:
            # 有多个不同的 data 值，存在冲突
            conflicting_models = []
            conflicting_values = []
            for models_list in data_values.values():
                for item in models_list:
                    conflicting_models.append(item["model_id"])
                    conflicting_values.append(item["value"])
            
            conflicts.append({
                "type": "data_conflict",
                "models": conflicting_models,
                "field": "data",
                "values": conflicting_values
            })
        
        return conflicts





