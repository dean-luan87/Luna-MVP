# vision_pipeline/b2/v03/b2_audit/rules/base.py
"""
抽象规则基类
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class AuditRule(ABC):
    """验收规则基类"""
    
    rule_id: str = ""
    description: str = ""
    
    @abstractmethod
    def check(self, ctx) -> Optional[Dict[str, Any]]:
        """
        检查规则
        
        :param ctx: AuditContext 对象
        :return: None → PASS, dict → FAIL / WARN
        """
        pass
