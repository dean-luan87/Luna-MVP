"""
Contract Validator (C-1)

合约验证器

核心接口：
- validate(contract) -> ValidationResult

Validator 必须做的检查（一期只做硬校验）：
- 基础校验：必填字段存在、类型正确
- 语义校验：distance_m >= 0, confidence ∈ [0,1], turn_* → direction 不得为空, offset_m >= 0

⚠️ 注意：
Validator 不抛异常，不终止流程
它只是"判定 + 报告"，是否继续由上层决定。
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from ..events import EXPR_VALIDATION_FAILED, EXPR_CONTRACT_INVALID
from ..contracts.base_contract import BaseExpressionContract
from ..contracts.navigation_contract import NavigationExpressionContract


@dataclass
class ValidationResult:
    """
    ValidationResult（新建 dataclass）
    
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    """
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []


class ContractValidator:
    """
    合约验证器
    
    职责：
    - 检查 required keys 存在
    - 类型粗校验（float/str/Optional）
    - 失败发布 expr.validation.failed
    """
    
    def __init__(self, event_bus=None, logger=None):
        """
        初始化验证器
        
        Args:
            event_bus: 事件总线（可选）
            logger: 日志记录器（可选）
        """
        self.event_bus = event_bus
        self.logger = logger
    
    def validate(self, contract: Any) -> ValidationResult:
        """
        验证合约
        
        核心接口：
        - 支持 BaseExpressionContract 及其子类
        - 支持字典格式的合约
        
        Args:
            contract: 合约（BaseExpressionContract 或 Dict）
            
        Returns:
            ValidationResult: 验证结果
        """
        errors: List[str] = []
        warnings: List[str] = []
        
        # 转换为字典格式（如果已经是 dataclass）
        if isinstance(contract, BaseExpressionContract):
            contract_dict = contract.to_dict()
            contract_type = type(contract).__name__
        elif isinstance(contract, dict):
            contract_dict = contract
            contract_type = contract.get("intent_type", "unknown")
        else:
            return ValidationResult(
                is_valid=False,
                errors=[f"Invalid contract type: {type(contract).__name__}"],
                warnings=[]
            )
        
        # 基础校验
        base_errors = self._validate_base_fields(contract_dict)
        errors.extend(base_errors)
        
        # 语义校验（根据合约类型）
        if contract_type == "navigation" or contract_dict.get("intent_type") == "navigation":
            semantic_errors, semantic_warnings = self._validate_navigation_semantics(contract_dict)
            errors.extend(semantic_errors)
            warnings.extend(semantic_warnings)
        
        is_valid = len(errors) == 0
        
        # 如果验证失败，发布事件
        if not is_valid:
            self._publish_contract_invalid(contract_dict, errors)
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings
        )
    
    def _validate_base_fields(self, contract: Dict[str, Any]) -> List[str]:
        """
        验证基础字段
        
        Args:
            contract: 合约字典
            
        Returns:
            List[str]: 错误列表
        """
        errors: List[str] = []
        
        # 检查必填字段
        required_fields = ["intent_type", "source", "confidence", "timestamp"]
        for field in required_fields:
            if field not in contract:
                errors.append(f"Missing required field: {field}")
        
        # 类型校验
        if "confidence" in contract:
            confidence = contract["confidence"]
            if not isinstance(confidence, (int, float)):
                errors.append("confidence must be float")
            elif not (0.0 <= confidence <= 1.0):
                errors.append("confidence must be in [0.0, 1.0]")
        
        if "timestamp" in contract:
            timestamp = contract["timestamp"]
            if not isinstance(timestamp, (int, float)):
                errors.append("timestamp must be float")
        
        return errors
    
    def _validate_navigation_semantics(
        self,
        contract: Dict[str, Any]
    ) -> tuple[List[str], List[str]]:
        """
        验证导航合约语义
        
        语义校验（导航）：
        - distance_m >= 0
        - confidence ∈ [0,1]
        - turn_* → direction 不得为空
        - offset_m 若存在 → >= 0
        
        Args:
            contract: 合约字典
            
        Returns:
            tuple[List[str], List[str]]: (错误列表, 警告列表)
        """
        errors: List[str] = []
        warnings: List[str] = []
        
        # distance_m >= 0
        if "distance_m" in contract:
            distance_m = contract["distance_m"]
            if not isinstance(distance_m, (int, float)):
                errors.append("distance_m must be float")
            elif distance_m < 0:
                errors.append("distance_m must be >= 0")
            elif distance_m == 0:
                # distance_m == 0 只允许在 stop
                action = contract.get("action", "")
                if action not in ["stop"]:
                    warnings.append("distance_m == 0 only allowed for stop action")
        
        # turn_* → direction 不得为空
        action = contract.get("action", "")
        if action in ["turn_left", "turn_right"]:
            direction = contract.get("direction")
            if not direction:
                errors.append(f"{action} requires direction field")
        
        # offset_m 若存在 → >= 0
        if "offset_m" in contract and contract["offset_m"] is not None:
            offset_m = contract["offset_m"]
            if not isinstance(offset_m, (int, float)):
                errors.append("offset_m must be float")
            elif offset_m < 0:
                errors.append("offset_m cannot be negative")
        
        return errors, warnings
    
    def _check_type(self, value: Any, expected_type: type) -> bool:
        """
        类型粗校验
        
        Args:
            value: 值
            expected_type: 期望类型
            
        Returns:
            bool: 是否匹配
        """
        # 处理 Optional 类型
        if hasattr(expected_type, '__origin__') and expected_type.__origin__ is type(None).__class__:
            # Optional 类型，允许 None
            if value is None:
                return True
            # 检查实际类型
            actual_types = expected_type.__args__
            return any(isinstance(value, t) for t in actual_types if t is not type(None))
        
        # 普通类型检查
        return isinstance(value, expected_type)
    
    def _publish_contract_invalid(
        self,
        contract: Dict[str, Any],
        errors: List[str]
    ) -> None:
        """
        发布合约无效事件
        
        Args:
            contract: 合约字典
            errors: 错误列表
        """
        reason = "; ".join(errors)
        
        if self.event_bus:
            self.event_bus.publish(EXPR_CONTRACT_INVALID, {
                "contract": contract,
                "errors": errors,
                "reason": reason
            })
        
        # 日志输出
        log_msg = f"[EXPR_CONTRACT_INVALID] reason={reason}"
        if self.logger:
            if hasattr(self.logger, 'info'):
                self.logger.info("ContractValidator", "contract_invalid", {
                    "contract": contract,
                    "errors": errors
                })
            else:
                self.logger(log_msg)
        else:
            print(log_msg)
