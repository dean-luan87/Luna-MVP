"""Runtime-to-workspace adapter with no Reality mutation."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional

from .context_assembler import ContextPackage


@dataclass(frozen=True)
class WorkspaceContext:
    context_id: str
    current_event: Mapping[str, Any]
    current_task: Optional[str]
    situation: str


class WorkspaceRuntimeAdapter:
    def __init__(self) -> None:
        self._active: Optional[WorkspaceContext] = None

    def activate(self, context: ContextPackage) -> WorkspaceContext:
        self._active = WorkspaceContext(
            context_id=context.context_id,
            current_event=dict(context.event_context),
            current_task=context.event_context.get("task"),
            situation=context.situation,
        )
        return self._active

    def current(self) -> Optional[WorkspaceContext]:
        return self._active
