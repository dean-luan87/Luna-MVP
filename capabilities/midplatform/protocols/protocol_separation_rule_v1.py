# -*- coding: utf-8 -*-
"""Protocol Constraint vs Module Logic Separation Rule — canonical definition."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

RULE_ID = "protocol_constraint_vs_module_logic_separation_rule_v1"
RULE_NAME_EN = "Protocol Constraint vs Module Logic Separation Rule"
RULE_NAME_ZH = "协议约束与模块逻辑分离规则"

DEFINITION_EN = (
    "The protocol layer defines cross-phase, cross-module, and cross-object-lifecycle constraints, "
    "numbering, error codes, execution result structures, whitebox diagnostic binding, and supervision. "
    "The protocol layer does not guarantee module business logic correctness. "
    "Module implementation failure must not be classified as protocol failure by default. "
    "Only when a module violates protocol boundaries, misuses protocol states, bypasses protocol constraints, "
    "or breaks protocol numbering / error codes / execution results / whitebox binding should it be "
    "classified as protocol failure."
)

DEFINITION_ZH = (
    "协议层只定义跨阶段、跨模块、跨对象生命周期的约束、编号、错误码、执行结果结构、"
    "白盒诊断绑定与监督机制。协议层不承担模块业务逻辑正确性。"
    "模块实现失败不得默认归类为协议失败。只有当模块违反协议边界、错误使用协议状态、"
    "绕过协议约束、破坏协议编号/错误码/执行结果/白盒绑定时，才归类为协议失败。"
)

PROTOCOL_LAYER_RESPONSIBILITIES: Tuple[str, ...] = (
    "define constitutional and cross-module boundaries",
    "define candidate vs record separation",
    "define approval candidate vs approval record separation",
    "block unauthorized grant issuance",
    "block unauthorized foundation freeze",
    "standardize error codes and whitebox diagnostic refs",
    "provide reusable protocol_id / error_namespace / execution_result_schema",
    "classify protocol violations vs module failures",
)

MODULE_LAYER_RESPONSIBILITIES: Tuple[str, ...] = (
    "implement phase artifacts and business logic",
    "populate fields and matrices correctly",
    "run module runner and local verifier",
    "read upstream artifacts correctly",
    "implement module-internal algorithms",
)

FAILURE_CLASSIFICATION: Tuple[Dict[str, Any], ...] = (
    {
        "category": "protocol_violation",
        "label_en": "Protocol Violation",
        "label_zh": "协议违规",
        "when": "module violates protocol boundary or misuses protocol state",
        "example": "owner_approval_candidate written as owner_approval_record",
        "example_error_code": "LUNA-PROTO-L1-APPROVAL-ACK-V1::AUTH-001",
        "error_class": "AUTH",
        "detected_by": "protocol_constraint_check",
    },
    {
        "category": "module_process_failure",
        "label_en": "Module Process Failure",
        "label_zh": "模块流程实现问题",
        "when": "artifacts missing, upstream not read, verifier local process gap",
        "example": "required matrix artifact not generated",
        "example_error_code": "module_local::PROC-001",
        "error_class": "PROC",
        "detected_by": "module_verifier",
        "not_protocol_failure_by_default": True,
    },
    {
        "category": "module_business_logic_failure",
        "label_en": "Module Business Logic Failure",
        "label_zh": "模块业务逻辑问题",
        "when": "module algorithm or domain judgment is wrong",
        "example": "module internal decision algorithm incorrect",
        "example_error_code": "module_local::LOGIC-001",
        "error_class": "PROC",
        "detected_by": "module_tests_or_review",
        "not_protocol_failure_by_default": True,
    },
)

OPERATING_MODEL: Tuple[str, ...] = (
    "protocol_standard_smoke_validate_once",
    "module_phases_reference_protocol_id_error_namespace_execution_result_schema",
    "distinguish_protocol_violation_from_module_implementation_failure",
    "protocol_layer_is_guardrail_not_driver",
)

VALIDATE_ONCE_PER_MODULE_RULE_ID = "protocol_validate_once_per_module_rule_v1"
VALIDATE_ONCE_PER_MODULE_RULE_NAME_EN = "Protocol Validate Once Per Module Rule"
VALIDATE_ONCE_PER_MODULE_RULE_NAME_ZH = "协议模块内一次验证规则"

VALIDATE_ONCE_DEFINITION_EN = (
    "A protocol standard receives one full reference validation when a module first integrates it. "
    "After that first validation passes for the module, later failures in the same module default to "
    "module implementation failure / module local PROC failure, not protocol standard failure."
)

VALIDATE_ONCE_DEFINITION_ZH = (
    "协议标准在模块首次接入时执行一次完整引用验证。"
    "一旦该模块首次验证通过，后续同模块测试中若再次出现相关检查失败，"
    "默认归类为 module implementation failure / module local PROC failure，而不是 protocol standard failure。"
)

PROTOCOL_REATTRIBUTION_ALLOWED_WHEN: Tuple[str, ...] = (
    "protocol_id or error_namespace or schema ref changed",
    "protocol standard version upgraded",
    "module switched to new L1/L2 protocol",
    "protocol reference drift detected",
    "shared helper import or validation failure",
    "protocol canonical definition self-contradiction discovered",
)

VALIDATE_ONCE_ATTRIBUTION_RULES: Tuple[Dict[str, Any], ...] = (
    {
        "category": "first_protocol_validation_failed",
        "label_en": "First Protocol Validation Failed",
        "label_zh": "首次协议验证失败",
        "when": "module first integration; protocol reference / schema / namespace / helper may be wrong",
        "default_action": "check protocol reference, schema ref, error_namespace, shared helper",
        "may_be_protocol_failure": True,
    },
    {
        "category": "first_protocol_validation_passed_later_test_failed",
        "label_en": "Later Test Failed After First Protocol Validation Passed",
        "label_zh": "首次协议验证通过后后续测试失败",
        "when": "same module, same protocol refs; later artifact/matrix/runner/verifier failure",
        "default_action": "classify as module implementation failure / module local PROC failure",
        "not_protocol_failure_by_default": True,
    },
    {
        "category": "later_test_failed_due_to_protocol_ref_drift",
        "label_en": "Later Test Failed Due To Protocol Reference Drift",
        "label_zh": "协议引用漂移导致后续测试失败",
        "when": "protocol_id, error_namespace, schema_ref, traceability_rule_ref or helper drift",
        "default_action": "classify as protocol assimilation / reference drift failure",
        "may_be_protocol_failure": True,
    },
    {
        "category": "later_test_failed_due_to_protocol_version_change",
        "label_en": "Later Test Failed Due To Protocol Version Change",
        "label_zh": "协议版本变更导致后续测试失败",
        "when": "protocol standard version upgraded or module switched L1/L2 protocol",
        "default_action": "classify as protocol compatibility failure; re-run first validation",
        "may_be_protocol_failure": True,
    },
)

VALIDATE_ONCE_PROTOCOL_LAYER_DUTIES: Tuple[str, ...] = (
    "confirm module wired protocol correctly on first integration",
    "perform lightweight reference checks afterward",
    "do not re-judge guardrail on every module test by default",
)

VALIDATE_ONCE_MODULE_LAYER_DUTIES: Tuple[str, ...] = (
    "produce correct artifacts, fields, matrices",
    "fix runner and verifier logic failures locally",
    "treat post-first-validation failures as module responsibility unless reattribution triggers apply",
)


def build_validate_once_per_module_rule_document(**extra: Any) -> Dict[str, Any]:
    return {
        "rule_id": VALIDATE_ONCE_PER_MODULE_RULE_ID,
        "rule_name_en": VALIDATE_ONCE_PER_MODULE_RULE_NAME_EN,
        "rule_name_zh": VALIDATE_ONCE_PER_MODULE_RULE_NAME_ZH,
        "definition_en": VALIDATE_ONCE_DEFINITION_EN,
        "definition_zh": VALIDATE_ONCE_DEFINITION_ZH,
        "protocol_reattribution_allowed_when": list(PROTOCOL_REATTRIBUTION_ALLOWED_WHEN),
        "attribution_rules": list(VALIDATE_ONCE_ATTRIBUTION_RULES),
        "protocol_layer_duties": list(VALIDATE_ONCE_PROTOCOL_LAYER_DUTIES),
        "module_layer_duties": list(VALIDATE_ONCE_MODULE_LAYER_DUTIES),
        "lightweight_reference_only_after_first_pass": True,
        "protocol_validate_once_per_module_rule_complete": True,
        **extra,
    }


def build_separation_rule_document(**extra: Any) -> Dict[str, Any]:
    return {
        "rule_id": RULE_ID,
        "rule_name_en": RULE_NAME_EN,
        "rule_name_zh": RULE_NAME_ZH,
        "definition_en": DEFINITION_EN,
        "definition_zh": DEFINITION_ZH,
        "protocol_layer_responsibilities": list(PROTOCOL_LAYER_RESPONSIBILITIES),
        "module_layer_responsibilities": list(MODULE_LAYER_RESPONSIBILITIES),
        "failure_classification": list(FAILURE_CLASSIFICATION),
        "operating_model": list(OPERATING_MODEL),
        "validate_once_per_module_rule_ref": VALIDATE_ONCE_PER_MODULE_RULE_NAME_EN,
        "validate_once_per_module_rule": build_validate_once_per_module_rule_document(),
        "protocol_layer_is_guardrail_not_driver": True,
        "module_implementation_failure_not_protocol_failure_by_default": True,
        "protocol_constraint_module_logic_separation_rule_complete": True,
        **extra,
    }
