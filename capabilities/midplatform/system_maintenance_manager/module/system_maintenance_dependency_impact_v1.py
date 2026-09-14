from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.system_maintenance_manager.module.system_maintenance_manager_module_types_v1 import (
    not_fact,
)


def build_system_maintenance_dependency_impact_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    deps = tuple(input_candidate.get("dependency_refs") or ())
    missing = tuple(str(d) for d in deps if str(d).startswith("missing:"))
    impacted = tuple(str(d).replace("missing:", "") for d in missing)
    return {
        "schema_version": "system_maintenance_dependency_impact_v1",
        "dependency_impact": {
            "dependency_refs": deps,
            "dependency_unavailable": bool(missing),
            "impacted_capabilities": impacted,
            "impact_level": "high" if missing else "low",
        },
        **not_fact(),
    }
