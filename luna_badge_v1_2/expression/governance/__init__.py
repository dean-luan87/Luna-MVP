"""
Expression Governance (C-4)

表达治理层

职责：
- 决定"要不要说"
- 决定"现在说还是等一下"
- 决定"说几次"
- 决定"要不要确认"
"""

from .expression_gate import ExpressionGate
from .rate_limiter import RateLimiter
from .confirmation_manager import ConfirmationManager
from .escalation_manager import EscalationManager
from .governance_pipeline import GovernancePipeline
from .output_boundary import OutputGovernanceBoundary, GovernanceDecision, DummyPassThrough

__all__ = [
    "ExpressionGate",
    "RateLimiter",
    "ConfirmationManager",
    "EscalationManager",
    "GovernancePipeline",
    "OutputGovernanceBoundary",
    "GovernanceDecision",
    "DummyPassThrough",
]
