from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.protocol_manager.module.protocol_manager_module_types_v1 import (
    not_fact,
)


def _major(version: str) -> int:
    text = version.strip().lower().lstrip("v")
    if not text:
        return -1
    head = ""
    for char in text:
        if char.isdigit():
            head += char
        else:
            break
    return int(head) if head else -1


def build_protocol_manager_compatibility_candidate_v1(
    input_candidate: Mapping[str, Any],
    version_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    current_version = str(version_candidate.get("current_version") or "")
    target_version = str(version_candidate.get("compatibility_target_version") or "")
    change_set = dict(input_candidate.get("change_set") or {})

    input_changed = bool(change_set.get("input_fields_changed", False))
    output_changed = bool(change_set.get("output_fields_changed", False))
    required_optional_changed = bool(change_set.get("required_optional_changed", False))
    enum_changed = bool(change_set.get("enum_changed", False))
    error_code_changed = bool(change_set.get("error_code_changed", False))
    runtime_boundary_changed = bool(change_set.get("runtime_boundary_changed", False))
    admission_changed = bool(change_set.get("admission_changed", False))
    trace_replay_changed = bool(change_set.get("trace_replay_changed", False))

    current_major = _major(current_version)
    target_major = _major(target_version)

    if not current_version or not target_version:
        compatibility = "unknown"
    elif current_version == target_version and not any(
        [
            input_changed,
            output_changed,
            required_optional_changed,
            enum_changed,
            error_code_changed,
            runtime_boundary_changed,
            admission_changed,
            trace_replay_changed,
        ]
    ):
        compatibility = "exact_match"
    elif runtime_boundary_changed or admission_changed:
        compatibility = "incompatible"
    elif required_optional_changed or error_code_changed:
        compatibility = "migration_required"
    elif enum_changed or trace_replay_changed:
        compatibility = "adapter_required"
    elif current_major >= 0 and target_major >= 0 and target_major < current_major:
        compatibility = "backward_compatible"
    elif current_major >= 0 and target_major >= 0 and target_major > current_major:
        compatibility = "forward_compatible"
    else:
        compatibility = "unknown"

    return {
        "schema_version": "protocol_manager_compatibility_candidate_v1",
        "compatibility_result": compatibility,
        "input_fields_changed": input_changed,
        "output_fields_changed": output_changed,
        "required_optional_changed": required_optional_changed,
        "enum_changed": enum_changed,
        "error_code_changed": error_code_changed,
        "runtime_boundary_changed": runtime_boundary_changed,
        "admission_changed": admission_changed,
        "trace_replay_changed": trace_replay_changed,
        "breaking_change_candidate": compatibility
        in {"migration_required", "incompatible"},
        **not_fact(),
    }
