"""
Expression Layer (C Layer)

Cognitive Alignment Layer（认知对齐层）

把"Luna 的灵魂（世界语义）"稳定地翻译成"不同身体/场景下用户能听懂的表达"
"""

# C-1: Expression Contract
from .contracts import (
    create_navigation_contract,
    create_safety_contract,
    validate_base_fields,
)

# C-2: Embodiment Context
from .context import (
    EmbodimentProfile,
    EmbodimentSelector,
    DistanceUnit,
    DirectionReference,
    Precision,
)

# C-2.5: Cognitive Calibrator
from .calibrator import (
    ExpressionProtocol,
    CalibratorInput,
    CalibratorOutput,
    CalibratorEngine,
    EmotionEngineHooks,
)

# C-3: Renderer Runtime
from .renderer import (
    RenderProfile,
    ExpressionTemplate,
    TemplateRegistry,
    TemplateSelector,
    ExpressionComposer,
    OutputAdapter,
    RendererPipeline,
)

# C-4: Output Adapter
from .adapters import (
    OutputChannel,
    OutputRouter,
)

# Validators
from .validators import (
    ContractValidator,
)

# Events
from .events import (
    EXPR_INTENT_CREATED,
    EXPR_CONTEXT_SELECTED,
    EXPR_PROTOCOL_SELECTED,
    EXPR_RENDERED,
    EXPR_OUTPUT_ROUTED,
    EXPR_VALIDATION_FAILED,
)

__all__ = [
    # C-1
    "create_navigation_contract",
    "create_safety_contract",
    "validate_base_fields",
    # C-2
    "EmbodimentProfile",
    "EmbodimentSelector",
    "DistanceUnit",
    "DirectionReference",
    "Precision",
    # C-2.5
    "ExpressionProtocol",
    "CalibratorInput",
    "CalibratorOutput",
    "CalibratorEngine",
    "EmotionEngineHooks",
    # C-3
    "RenderProfile",
    "ExpressionTemplate",
    "TemplateRegistry",
    "TemplateSelector",
    "ExpressionComposer",
    "OutputAdapter",
    "RendererPipeline",
    # C-4
    "OutputChannel",
    "OutputRouter",
    # Validators
    "ContractValidator",
    # Events
    "EXPR_INTENT_CREATED",
    "EXPR_CONTEXT_SELECTED",
    "EXPR_PROTOCOL_SELECTED",
    "EXPR_RENDERED",
    "EXPR_OUTPUT_ROUTED",
    "EXPR_VALIDATION_FAILED",
]
