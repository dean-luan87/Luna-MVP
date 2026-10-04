"""Owner-local read surfaces for the two binding identity domains."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional


CAPABILITY_MODEL_BINDING_REGISTRY = "capabilities/midplatform/model_manager/registries/capability_model_binding_registry_v1.json"
MODEL_PROVIDER_BINDING_REGISTRY = "capabilities/midplatform/model_manager/registry/model_provider_binding_registry_v1.json"


def read_capability_model_binding_current_state(
    identity_ref: str,
    *,
    repo_root: Optional[Path] = None,
    expected_source_revision: Optional[str] = None,
    read_purpose: str = "bounded_static_current_state",
) -> Dict[str, Any]:
    return _read_binding(
        identity_ref,
        relative_path=CAPABILITY_MODEL_BINDING_REGISTRY,
        owner_ref="Capability Governance",
        repo_root=repo_root,
        expected_source_revision=expected_source_revision,
        read_purpose=read_purpose,
    )


def read_model_provider_binding_current_state(
    identity_ref: str,
    *,
    repo_root: Optional[Path] = None,
    expected_source_revision: Optional[str] = None,
    read_purpose: str = "bounded_static_current_state",
) -> Dict[str, Any]:
    return _read_binding(
        identity_ref,
        relative_path=MODEL_PROVIDER_BINDING_REGISTRY,
        owner_ref="Provider Governance",
        repo_root=repo_root,
        expected_source_revision=expected_source_revision,
        read_purpose=read_purpose,
    )


def _read_binding(
    identity_ref: str,
    *,
    relative_path: str,
    owner_ref: str,
    repo_root: Optional[Path],
    expected_source_revision: Optional[str],
    read_purpose: str,
) -> Dict[str, Any]:
    root = repo_root or _find_repo_root()
    path = root / relative_path
    if not path.is_file():
        return _unknown(identity_ref, owner_ref, "declaration_source_missing")
    try:
        registry = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return _unknown(identity_ref, owner_ref, "declaration_source_unreadable")
    schema_id = str(registry.get("schema_id", ""))
    version = str(registry.get("version", "")) or "v1"
    source_revision = f"declaration:{schema_id}:{version}" if schema_id else ""
    if not source_revision or (expected_source_revision and expected_source_revision != source_revision):
        return _unknown(identity_ref, owner_ref, "source_revision_mismatch")
    record = next(
        (item for item in registry.get("bindings", ()) if isinstance(item, dict) and item.get("binding_id") == identity_ref),
        None,
    )
    if record is None:
        return _unknown(identity_ref, owner_ref, "binding_identity_not_declared")
    return {
        "identity_ref": identity_ref,
        "owner_ref": owner_ref,
        "lifecycle_state": record.get("lifecycle_state"),
        "compatibility_status": record.get("compatibility_status"),
        "binding_version": record.get("binding_version"),
        "source_revision": source_revision,
        "currentness_basis": "locked_binding_registry_declaration; no_runtime_mutation",
        "replacement_refs": tuple(record.get("superseded_by") or ()),
        "invalidation_refs": tuple(record.get("invalidation_refs") or ()),
        "read_status": "BOUNDED_STATIC_CURRENT_STATE",
        "read_purpose": read_purpose,
        "reason": "binding_state_read_without_eligibility_substitution",
        "reason_refs": tuple(record.get("source_version_refs") or ()),
    }


def _unknown(identity_ref: str, owner_ref: str, reason: str) -> Dict[str, Any]:
    return {
        "identity_ref": identity_ref,
        "owner_ref": owner_ref,
        "lifecycle_state": None,
        "source_revision": None,
        "currentness_basis": None,
        "read_status": "UNKNOWN",
        "reason": reason,
        "reason_refs": (),
    }


def _find_repo_root() -> Path:
    for base in (Path.cwd(), Path(__file__).resolve().parents[6]):
        if (base / "capabilities/test_board/test_board_protocol_v1.py").is_file():
            return base
    return Path.cwd()
