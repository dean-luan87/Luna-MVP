# -*- coding: utf-8 -*-
"""Luna Midplatform Protocol Types v1 — pure schema / dataclass definitions, no runtime side effects."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class ProtocolLayer(str, Enum):
    L0 = "L0"
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"


class ProtocolErrorClass(str, Enum):
    CONST = "CONST"
    PROC = "PROC"
    IFACE = "IFACE"
    ASSIM = "ASSIM"
    EVID = "EVID"
    STATE = "STATE"
    AUTH = "AUTH"
    TTL = "TTL"
    TRACE = "TRACE"
    WB = "WB"
    HEALTH = "HEALTH"


class ProtocolSeverity(str, Enum):
    BLOCKER = "blocker"
    WARNING = "warning"
    INFO = "info"


class ProtocolHealthStatus(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    DRIFT_DETECTED = "DRIFT_DETECTED"
    QUARANTINED = "QUARANTINED"


class ProtocolExecutionOutcome(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"


@dataclass(frozen=True)
class ProtocolHeader:
    protocol_id: str
    protocol_layer: str
    protocol_domain: str
    protocol_name: str
    protocol_version: str
    governance_level: str
    constitution_refs: List[str] = field(default_factory=list)
    process_contract_refs: List[str] = field(default_factory=list)
    interface_contract_refs: List[str] = field(default_factory=list)
    assimilation_contract_refs: List[str] = field(default_factory=list)
    whitebox_binding_required: bool = True
    error_code_namespace: str = ""
    module_extension_allowed: bool = True
    cross_module_applicable: bool = True
    runtime_execution_allowed: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "protocol_id": self.protocol_id,
            "protocol_layer": self.protocol_layer,
            "protocol_domain": self.protocol_domain,
            "protocol_name": self.protocol_name,
            "protocol_version": self.protocol_version,
            "governance_level": self.governance_level,
            "constitution_refs": list(self.constitution_refs),
            "process_contract_refs": list(self.process_contract_refs),
            "interface_contract_refs": list(self.interface_contract_refs),
            "assimilation_contract_refs": list(self.assimilation_contract_refs),
            "whitebox_binding_required": self.whitebox_binding_required,
            "error_code_namespace": self.error_code_namespace,
            "module_extension_allowed": self.module_extension_allowed,
            "cross_module_applicable": self.cross_module_applicable,
            "runtime_execution_allowed": self.runtime_execution_allowed,
        }


@dataclass(frozen=True)
class ProtocolRegistryEntry:
    protocol_name: str
    suggested_protocol_id: str
    layer: str
    domain: str
    status: str
    current_handling: str
    canonical_required: bool
    module_extension_allowed: bool
    whitebox_binding_required: bool
    error_namespace: str
    related_governance_debt: List[str] = field(default_factory=list)
    must_not_implement_now: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "protocol_name": self.protocol_name,
            "suggested_protocol_id": self.suggested_protocol_id,
            "layer": self.layer,
            "domain": self.domain,
            "status": self.status,
            "current_handling": self.current_handling,
            "canonical_required": self.canonical_required,
            "module_extension_allowed": self.module_extension_allowed,
            "whitebox_binding_required": self.whitebox_binding_required,
            "error_namespace": self.error_namespace,
            "related_governance_debt": list(self.related_governance_debt),
            "must_not_implement_now": self.must_not_implement_now,
        }


def build_protocol_id(layer: str, domain: str, name: str, version: str) -> str:
    layer_upper = layer.upper().replace("L", "L") if layer.startswith("L") else layer.upper()
    domain_upper = domain.upper().replace("_", "-").replace(" ", "-")
    name_upper = name.upper().replace("_", "-").replace(" ", "-")
    version_upper = version.upper().replace("V", "V") if version.upper().startswith("V") else f"V{version}"
    return f"LUNA-PROTO-{layer_upper}-{domain_upper}-{name_upper}-{version_upper}"
