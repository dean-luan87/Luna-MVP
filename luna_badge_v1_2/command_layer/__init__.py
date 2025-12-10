"""
Command Layer - v1.4.4

命令解析与任务参数补全层
在 Inquiry → DecisionCore → TaskChain 之前新增的命令处理层
"""

from .envelope import CommandEnvelope
from .semantic_normalizer import NormalizedCommand, normalize_command
from .ecs_resolver import ResolutionResult, resolve_slots, FakeMemoryClient, FakePOIClient
from .prefix_detector import detect_prefix
from .non_command_handler import handle_non_command
from .help_center_stub import handle_help_center
from .mapping import normalized_to_parsed_intent

__all__ = [
    "CommandEnvelope",
    "NormalizedCommand",
    "normalize_command",
    "ResolutionResult",
    "resolve_slots",
    "FakeMemoryClient",
    "FakePOIClient",
    "detect_prefix",
    "handle_non_command",
    "handle_help_center",
    "normalized_to_parsed_intent",
]

