"""
Output Arbiter

模型输出仲裁器。
"""

from typing import List, Dict, Any, Optional


class OutputArbiter:
    """
    输出仲裁器
    
    职责：
    - 在多个模型输出冲突时进行仲裁
    - v1.5: 规则驱动，不"想"，只"按规则选"
    """
    
    def __init__(self):
        """
        初始化仲裁器
        
        v1.5 仲裁顺序固定：
        1. 是否存在主模型合格输出
        2. 否则是否存在次模型合格输出
        3. 否则 → fallback
        """
        # v1.5: 固定优先级规则（可配置，但不动态学习）
        # 主模型优先级（按任务域配置）
        self.primary_models = {
            "navigation": ["vision_model_v1", "yolo_model"],
            "safety": ["safety_model_v1"],
            "inquiry": ["llm_model_v1"],
            "default": []  # 默认无主模型
        }
        
        # 次模型优先级（备选）
        self.secondary_models = {
            "navigation": ["backup_vision_model"],
            "safety": ["backup_safety_model"],
            "inquiry": ["backup_llm_model"],
            "default": []
        }

    def arbitrate(
        self, 
        task_domain: str, 
        normalized_outputs: List[Dict[str, Any]], 
        conflicts: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        根据规则选出最终结果或触发 fallback
        
        Args:
            task_domain: 任务领域
            normalized_outputs: 归一化后的输出列表（已通过 validator）
            conflicts: 冲突列表
            
        Returns:
            仲裁结果：
            {
                "action": "commit" | "fallback",
                "selected_output": Optional[Dict],  # 被选中的输出
                "reason": str  # 决策原因
            }
        """
        if not normalized_outputs:
            return {
                "action": "fallback",
                "selected_output": None,
                "reason": "No valid outputs"
            }
        
        # 获取主模型和次模型列表
        primary_list = self.primary_models.get(task_domain, self.primary_models["default"])
        secondary_list = self.secondary_models.get(task_domain, self.secondary_models["default"])
        
        # 1. 优先选择主模型输出
        for model_id in primary_list:
            for output in normalized_outputs:
                if output.get("model_id") == model_id:
                    return {
                        "action": "commit",
                        "selected_output": output,
                        "reason": f"Primary model selected: {model_id}"
                    }
        
        # 2. 其次选择次模型输出
        for model_id in secondary_list:
            for output in normalized_outputs:
                if output.get("model_id") == model_id:
                    return {
                        "action": "commit",
                        "selected_output": output,
                        "reason": f"Secondary model selected: {model_id}"
                    }
        
        # 3. 如果存在冲突，且无主/次模型匹配，触发 fallback
        if conflicts:
            return {
                "action": "fallback",
                "selected_output": None,
                "reason": f"Conflicts detected and no primary/secondary model match. Conflicts: {len(conflicts)}"
            }
        
        # 4. 无冲突但无主/次模型匹配，选择第一个有效输出（兜底）
        if normalized_outputs:
            return {
                "action": "commit",
                "selected_output": normalized_outputs[0],
                "reason": f"Fallback selection: first valid output ({normalized_outputs[0].get('model_id')})"
            }
        
        # 5. 完全无输出
        return {
            "action": "fallback",
            "selected_output": None,
            "reason": "No valid outputs available"
        }





