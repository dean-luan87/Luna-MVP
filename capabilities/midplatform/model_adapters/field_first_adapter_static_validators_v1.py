# -*- coding: utf-8 -*-
"""Field-First adapter static validators v1 — manifest and placeholder checks."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.model_adapters.field_first_adapter_contracts_v1 import (
    PROHIBITED_ADAPTER_ACTIONS,
    PROHIBITED_ADAPTER_IMPORTS,
)
from capabilities.midplatform.model_adapters.field_first_adapter_types_v1 import MANIFEST_FIELDS


def validate_manifest_entry(entry: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for f in MANIFEST_FIELDS:
        if f not in entry:
            issues.append(f"missing_field:{f}")
    if entry.get("download_authorized") is True:
        issues.append("download_authorized_must_be_false")
    if entry.get("weights_downloaded") is True:
        issues.append("weights_downloaded_must_be_false")
    if entry.get("inference_ready") is True:
        issues.append("inference_ready_must_be_false")
    if entry.get("runtime_build_completed") is True:
        issues.append("runtime_build_completed_must_be_false")
    if entry.get("adapter_required") is not True:
        issues.append("adapter_required_must_be_true")
    return len(issues) == 0, issues


def validate_all_manifests(entries: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
    all_issues: List[str] = []
    for entry in entries:
        ok, issues = validate_manifest_entry(entry)
        if not ok:
            all_issues.extend([f"{entry.get('model_project_id', '?')}:{i}" for i in issues])
    return len(all_issues) == 0, all_issues


def validate_no_prohibited_imports_in_source(source: str) -> Tuple[bool, List[str]]:
    found = [imp for imp in PROHIBITED_ADAPTER_IMPORTS if f"import {imp}" in source or f"from {imp}" in source]
    return len(found) == 0, found


def validate_placeholder_only_flags(adapter: Dict[str, Any]) -> bool:
    return adapter.get("placeholder_only") is True and adapter.get("inference_allowed") is False


def validate_prohibited_actions_absent(actions_present: List[str]) -> Tuple[bool, List[str]]:
    found = [a for a in actions_present if a in PROHIBITED_ADAPTER_ACTIONS]
    return len(found) == 0, found
