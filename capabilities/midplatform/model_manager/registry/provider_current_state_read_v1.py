"""Provider Governance-owned bounded current-state read surface."""

from __future__ import annotations

from typing import Any, Dict, Optional

from capabilities.midplatform.model_manager.registry.provider_registry_loader_v1 import (
    load_provider_registry,
)


def read_provider_current_state(
    identity_ref: str,
    *,
    expected_source_revision: Optional[str] = None,
    read_purpose: str = "bounded_static_current_state",
) -> Dict[str, Any]:
    """Return a Provider-owned view; legacy records without provider_id fail closed."""

    registry = load_provider_registry()
    schema_id = str(registry.get("schema_id", ""))
    version = str(registry.get("version", ""))
    source_revision = f"declaration:{schema_id}:{version}" if schema_id and version else ""
    if not source_revision or (expected_source_revision and expected_source_revision != source_revision):
        return _unknown(identity_ref, "source_revision_mismatch")
    record = next(
        (
            item for item in registry.get("providers", ())
            if isinstance(item, dict) and str(item.get("provider_id", "")) == identity_ref
        ),
        None,
    )
    if record is None:
        return _unknown(identity_ref, "provider_identity_not_uniquely_declared")
    return {
        "identity_ref": identity_ref,
        "owner_ref": "Provider Governance",
        "lifecycle_state": record.get("lifecycle_state"),
        "admission_status": record.get("admission_status"),
        "activation_state": record.get("activation_state"),
        "source_revision": source_revision,
        "currentness_basis": "locked_provider_registry_declaration; provider_state_only",
        "replacement_refs": tuple(record.get("superseded_by") or ()),
        "invalidation_refs": tuple(record.get("invalidation_refs") or ()),
        "read_status": "BOUNDED_STATIC_CURRENT_STATE",
        "read_purpose": read_purpose,
        "reason": "provider_identity_read_without_model_state_substitution",
        "reason_refs": tuple(record.get("source_version_refs") or ()),
    }


def _unknown(identity_ref: str, reason: str) -> Dict[str, Any]:
    return {
        "identity_ref": identity_ref,
        "owner_ref": "Provider Governance",
        "lifecycle_state": None,
        "source_revision": None,
        "currentness_basis": None,
        "read_status": "UNKNOWN",
        "reason": reason,
        "reason_refs": (),
    }
