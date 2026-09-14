"""Attention boundary for the first loop; selection is contract-only."""
from __future__ import annotations

from typing import Any, Mapping

from .context_assembler import ContextPackage
from .workspace_runtime_adapter import WorkspaceContext


class AttentionRuntimeInterface:
    """Exposes an attention candidate without implementing an attention algorithm."""

    def select(self, context: ContextPackage, workspace: WorkspaceContext) -> dict[str, Any]:
        return {
            "selection_mode": "contract_only",
            "context_id": context.context_id,
            "workspace_id": workspace.context_id,
            "selected_information": list(context.available_information),
            "unknowns": list(context.unknowns),
        }
