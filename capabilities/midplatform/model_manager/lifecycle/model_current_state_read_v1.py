"""Model Governance-owned bounded current-state read surface.

This is a read-only declaration view for the bounded static baseline phase. It
does not mutate lifecycle state, infer state from model_families, or claim a
production-mutable current state.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from capabilities.midplatform.model_manager.registry.provider_registry_loader_v1 import (
    load_model_registry,
)


def read_model_current_state(
    identity_ref: str,
    *,
    expected_source_revision: Optional[str] = None,
    read_purpose: str = "bounded_static_current_state",
) -> Dict[str, Any]:
    """Return a bounded static Model Governance view or a closed failure."""

    registry = load_model_registry()
    schema_id = str(registry.get("schema_id", ""))
    version = str(registry.get("version", ""))
    source_revision = f"declaration:{schema_id}:{version}" if schema_id and version else ""
    if not source_revision or (expected_source_revision and expected_source_revision != source_revision):
        return _unknown(identity_ref, "source_revision_mismatch")
    record = next(
        (
            item for item in registry.get("models", ())
            if isinstance(item, dict)
            and identity_ref in (str(item.get("model_id", "")), str(item.get("model_asset_id", "")))
        ),
        None,
    )
    if record is None:
        return _unknown(identity_ref, "identity_not_declared")
    return {
        "identity_ref": identity_ref,
        "owner_ref": "Model Governance",
        "lifecycle_state": record.get("lifecycle_state"),
        "admission_status": record.get("admission_status"),
        "activation_state": record.get("activation_state"),
        "source_revision": source_revision,
        "currentness_basis": "locked_model_registry_declaration; no_runtime_mutation",
        "replacement_refs": tuple(record.get("superseded_by") or ()),
        "invalidation_refs": tuple(record.get("invalidation_refs") or ()),
        "read_status": "BOUNDED_STATIC_CURRENT_STATE",
        "read_purpose": read_purpose,
        "reason": "owner_declaration_read_without_cross_identity_substitution",
        "reason_refs": tuple(record.get("source_version_refs") or ()),
    }


def _unknown(identity_ref: str, reason: str) -> Dict[str, Any]:
    return {
        "identity_ref": identity_ref,
        "owner_ref": "Model Governance",
        "lifecycle_state": None,
        "source_revision": None,
        "currentness_basis": None,
        "read_status": "UNKNOWN",
        "reason": reason,
        "reason_refs": (),
    }
