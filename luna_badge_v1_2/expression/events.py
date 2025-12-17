"""
Expression Events (C Layer)

定义事件名常量（字符串即可）
"""

# Expression Intent 事件
EXPR_INTENT_CREATED = "expr.intent.created"

# Context 事件
EXPR_CONTEXT_SELECTED = "expr.context.selected"

# Protocol 事件
EXPR_PROTOCOL_SELECTED = "expr.protocol.selected"

# Render 事件
EXPR_RENDERED = "expr.rendered"

# Output 事件
EXPR_OUTPUT_ROUTED = "expr.output.routed"

# Validation 事件
EXPR_VALIDATION_FAILED = "expr.validation.failed"
EXPR_CONTRACT_INVALID = "expr.contract.invalid"
