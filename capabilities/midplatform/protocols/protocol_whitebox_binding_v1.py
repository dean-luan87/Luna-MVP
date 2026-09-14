# -*- coding: utf-8 -*-
"""Luna Midplatform Protocol Whitebox Diagnostic Binding v1 — contract only, no runtime integration."""

from __future__ import annotations

from typing import Dict


def build_whitebox_diagnostic_ref(
    *,
    phase_id: str,
    protocol_id: str,
    error_code: str,
    artifact_ref: str,
    field_path: str,
) -> Dict[str, str]:
    trace_id = f"{phase_id}:{protocol_id}:{error_code}".replace(" ", "-")
    return {
        "whitebox_trace_ref": f"wb://{trace_id}",
        "diagnostic_node_ref": f"diag://{phase_id}/{artifact_ref}/{field_path}",
        "binding_mode": "contract_only",
        "runtime_integration": False,
    }
