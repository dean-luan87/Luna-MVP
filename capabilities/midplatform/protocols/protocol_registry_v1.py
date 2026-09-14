# -*- coding: utf-8 -*-
"""Luna Midplatform Protocol Registry v1 — pure registry helper, no runtime side effects."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from capabilities.midplatform.protocols.protocol_types_v1 import (
    ProtocolHeader,
    ProtocolLayer,
    ProtocolRegistryEntry,
    build_protocol_id,
)

_REGISTRY: Dict[str, Dict[str, Any]] = {}


def classify_protocol_layer(protocol: Dict[str, Any]) -> Optional[str]:
    layer = protocol.get("protocol_layer") or protocol.get("layer")
    if layer in {e.value for e in ProtocolLayer}:
        return str(layer)
    return None


def register_protocol(entry: ProtocolRegistryEntry) -> Dict[str, Any]:
    payload = entry.to_dict()
    _REGISTRY[entry.suggested_protocol_id] = payload
    return payload


def lookup_protocol(protocol_id: str) -> Optional[Dict[str, Any]]:
    return _REGISTRY.get(protocol_id)


def list_registered_protocols() -> List[Dict[str, Any]]:
    return list(_REGISTRY.values())


def validate_protocol_header(header: ProtocolHeader) -> bool:
    if header.runtime_execution_allowed:
        return False
    if not header.protocol_id.startswith("LUNA-PROTO-"):
        return False
    if not header.error_code_namespace:
        return False
    return True


def register_protocol_header(header: ProtocolHeader) -> Dict[str, Any]:
    if not validate_protocol_header(header):
        raise ValueError(f"invalid protocol header: {header.protocol_id}")
    entry = ProtocolRegistryEntry(
        protocol_name=header.protocol_name,
        suggested_protocol_id=header.protocol_id,
        layer=header.protocol_layer,
        domain=header.protocol_domain,
        status="canonical_standard_defined",
        current_handling="planning_only",
        canonical_required=True,
        module_extension_allowed=header.module_extension_allowed,
        whitebox_binding_required=header.whitebox_binding_required,
        error_namespace=header.error_code_namespace,
        must_not_implement_now=True,
    )
    return register_protocol(entry)


INPUT_OUTPUT_SYMMETRY_PROTOCOL_IDS: Tuple[str, ...] = (
    "LUNA-PROTO-L1-INPUT-CANDIDATE-GOVERNANCE-V1",
    "LUNA-PROTO-L1-OUTPUT-CANDIDATE-GOVERNANCE-V1",
    "LUNA-PROTO-L1-INPUT-OUTPUT-SYMMETRY-V1",
    "LUNA-PROTO-L1-PROTOCOL-TRACEABILITY-GOVERNANCE-V1",
)

REGISTRY_PATCH_PROTOCOL_IDS = INPUT_OUTPUT_SYMMETRY_PROTOCOL_IDS


def build_input_output_symmetry_protocol_headers() -> List[ProtocolHeader]:
    return [
        ProtocolHeader(
            protocol_id="LUNA-PROTO-L1-INPUT-CANDIDATE-GOVERNANCE-V1",
            protocol_layer="L1",
            protocol_domain="INPUT-CANDIDATE",
            protocol_name="Input Candidate Governance",
            protocol_version="V1",
            governance_level="L1 Midplatform System Protocol",
            error_code_namespace="LUNA-PROTO-L1-INPUT-CANDIDATE-GOVERNANCE-V1::*",
            whitebox_binding_required=True,
            module_extension_allowed=True,
            cross_module_applicable=True,
            runtime_execution_allowed=False,
        ),
        ProtocolHeader(
            protocol_id="LUNA-PROTO-L1-OUTPUT-CANDIDATE-GOVERNANCE-V1",
            protocol_layer="L1",
            protocol_domain="OUTPUT-CANDIDATE",
            protocol_name="Output Candidate Governance",
            protocol_version="V1",
            governance_level="L1 Midplatform System Protocol",
            error_code_namespace="LUNA-PROTO-L1-OUTPUT-CANDIDATE-GOVERNANCE-V1::*",
            whitebox_binding_required=True,
            module_extension_allowed=True,
            cross_module_applicable=True,
            runtime_execution_allowed=False,
        ),
        ProtocolHeader(
            protocol_id="LUNA-PROTO-L1-INPUT-OUTPUT-SYMMETRY-V1",
            protocol_layer="L1",
            protocol_domain="INPUT-OUTPUT",
            protocol_name="Input-Output Symmetry",
            protocol_version="V1",
            governance_level="L1 Midplatform System Protocol",
            error_code_namespace="LUNA-PROTO-L1-INPUT-OUTPUT-SYMMETRY-V1::*",
            whitebox_binding_required=True,
            module_extension_allowed=True,
            cross_module_applicable=True,
            runtime_execution_allowed=False,
        ),
        ProtocolHeader(
            protocol_id="LUNA-PROTO-L1-PROTOCOL-TRACEABILITY-GOVERNANCE-V1",
            protocol_layer="L1",
            protocol_domain="PROTOCOL-TRACEABILITY",
            protocol_name="Protocol Traceability Governance",
            protocol_version="V1",
            governance_level="L1 Midplatform System Protocol",
            error_code_namespace="LUNA-PROTO-L1-PROTOCOL-TRACEABILITY-GOVERNANCE-V1::*",
            whitebox_binding_required=True,
            module_extension_allowed=True,
            cross_module_applicable=True,
            runtime_execution_allowed=False,
        ),
    ]


def register_input_output_symmetry_protocol_patch() -> List[Dict[str, Any]]:
    """Register Input/Output/Symmetry/Traceability L1 protocols (patch only)."""
    return [register_protocol_header(header) for header in build_input_output_symmetry_protocol_headers()]


def lookup_input_output_symmetry_protocol(protocol_id: str) -> Optional[Dict[str, Any]]:
    if protocol_id not in INPUT_OUTPUT_SYMMETRY_PROTOCOL_IDS:
        return None
    return lookup_protocol(protocol_id)
