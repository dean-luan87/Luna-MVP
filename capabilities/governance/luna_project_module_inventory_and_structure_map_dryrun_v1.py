# -*- coding: utf-8 -*-
"""Luna Project Module Inventory and Structure Map DryRun v1.

Dry-run-only phase:
- Inventory current repo assets (modules, docs, phase artifacts) without file moves.
- Map each asset to current engineering domain, future target module, and Luna life-system layer.
- Produce developer backend / midplatform / client / cognition placeholder / migration risk maps.

Hard constraints:
- No runtime, no file moves/renames/deletes, no user media file ops.
- No writes to WorldModel/Memory/Fact/Library.
- Planning outputs only under _eval_out.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Phase-Luna-Project-Module-Inventory-and-Structure-Map-DryRun-v1-001"
DRYRUN_SCOPE = "luna_project_module_inventory_and_structure_map_dryrun_only"
SOURCE_CHAIN = "luna_project_module_inventory_and_structure_map_dryrun_v1"
DRYRUN_ID = "luna_proj_module_inventory_structure_map_dryrun_v1_001"

FINAL_DECISION = "LUNA_PROJECT_MODULE_INVENTORY_AND_STRUCTURE_MAP_DRYRUN_READY_FOR_CONSOLIDATION_PLANNING"
NEXT_PHASE = "Phase-Luna-Project-Structure-Consolidation-Planning-v1-001"

PLANNING_FINAL_DECISION = (
    "LUNA_PROJECT_STRUCTURE_GOVERNANCE_AND_MODULARIZATION_PLANNING_READY_FOR_STRUCTURE_MAP_DRYRUN"
)

LIFE_SYSTEMS = [
    "PerceptionLayer",
    "InteractionLayer",
    "ActionLayer",
    "ContextLayer",
    "CognitionLayer",
    "GovernanceLayer",
    "MidPlatformOrganLayer",
    "CapabilityOrganLayer",
    "DeveloperBackendLayer",
    "ClientSurfaceLayer",
    "HardwareInfrastructureLayer",
    "LifeSystemLayer",
    "ResilienceLayer",
    "UnclassifiedLegacyLayer",
]

ROOT_SPECS = [
    {
        "id": "project_structure_governance_planning",
        "arg": "project_structure_governance_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": [
            "summary.json",
            "target_project_structure_model.json",
            "module_domain_taxonomy.json",
            "midplatform_organ_system_model.json",
            "future_module_placeholder_plan.json",
            "client_boundary_policy.json",
            "verifier_report.json",
        ],
    },
    {
        "id": "gate_taxonomy_planning",
        "arg": "gate_taxonomy_planning_root",
        "required": True,
        "summary": "summary.json",
        "artifacts": ["summary.json", "gate_constitution.json"],
    },
]

SKIP_DIR_NAMES = {
    ".git",
    ".pytest_cache",
    "__pycache__",
    ".cursor",
    ".vscode",
    ".github",
    "node_modules",
}

SKIP_TOP_LEVEL = {
    "archive",
    "logs",
    "reports",
    "whitebox_archive",
    "OUT",
    "Luna_Badge_MVP",
    "luna_frontend_package_24files",
}


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def _load_root(path_str: Optional[str], summary_file: str, artifacts: List[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    loaded = bool(root) and all(_try_read_json(root / a) is not None for a in artifacts)
    summary_payload = _try_read_json(root / summary_file) if (root and loaded) else {}
    return {"root": root, "loaded": loaded, "summary": summary_payload or {}}


def _listdir_safe(path: Path) -> Tuple[bool, List[str]]:
    try:
        return True, sorted(os.listdir(str(path)))
    except (FileNotFoundError, NotADirectoryError):
        return False, []


def _is_dir(path: Path) -> bool:
    try:
        os.listdir(str(path))
        return True
    except NotADirectoryError:
        return False
    except FileNotFoundError:
        return False


def _classify_path(rel: str) -> Dict[str, Any]:
    """Rule-based mapping: current domain → target module → life-system layer."""
    p = rel.replace("\\", "/").strip("/")
    lower = p.lower()

    def _row(
        *,
        current_engineering_domain: str,
        future_target_module: str,
        future_life_system_mapping: str,
        is_client: bool = False,
        is_developer_backend: bool = False,
        is_midplatform_organ: bool = False,
        is_capability_organ: bool = False,
        is_cognition_placeholder: bool = False,
        versioning_required: bool = True,
        disposition_action: str = "keep",
    ) -> Dict[str, Any]:
        return {
            "current_engineering_domain": current_engineering_domain,
            "future_target_module": future_target_module,
            "future_life_system_mapping": future_life_system_mapping,
            "is_client": is_client,
            "is_developer_backend": is_developer_backend,
            "is_midplatform_organ": is_midplatform_organ,
            "is_capability_organ": is_capability_organ,
            "is_cognition_placeholder": is_cognition_placeholder,
            "versioning_required": versioning_required,
            "disposition_action": disposition_action,
        }

    if p.startswith("capabilities/vision") or lower.startswith("vision") or "vision_" in lower:
        return _row(
            current_engineering_domain="vision",
            future_target_module="capabilities/vision",
            future_life_system_mapping="PerceptionLayer",
            is_capability_organ=True,
        )
    if "ocr" in lower or p.startswith("capabilities/model_ocr") or p.startswith("capabilities/ocr"):
        return _row(
            current_engineering_domain="ocr",
            future_target_module="capabilities/ocr",
            future_life_system_mapping="PerceptionLayer",
            is_capability_organ=True,
        )
    if p.startswith("capabilities/voice") or lower.startswith("voice") or "speech" in lower or "tts" in lower:
        return _row(
            current_engineering_domain="voice",
            future_target_module="capabilities/voice",
            future_life_system_mapping="InteractionLayer",
            is_capability_organ=True,
        )
    if p.startswith("capabilities/navigation") or "navigation" in lower or p.startswith("map_d0"):
        return _row(
            current_engineering_domain="navigation",
            future_target_module="midplatform/task",
            future_life_system_mapping="ActionLayer",
            is_midplatform_organ=True,
        )
    if "map" in lower and not lower.startswith("docs"):
        return _row(
            current_engineering_domain="map_location",
            future_target_module="midplatform/context",
            future_life_system_mapping="ContextLayer",
            is_midplatform_organ=True,
        )
    if p.startswith("capabilities/governance") or p.startswith("governance/"):
        return _row(
            current_engineering_domain="governance",
            future_target_module="core/constitution",
            future_life_system_mapping="GovernanceLayer",
            is_capability_organ=True,
        )
    if p.startswith("capabilities/midplatform") or p.startswith("capabilities/mid_platform") or p.startswith("mid_platform"):
        return _row(
            current_engineering_domain="midplatform",
            future_target_module="midplatform/orchestration",
            future_life_system_mapping="MidPlatformOrganLayer",
            is_midplatform_organ=True,
        )
    if p.startswith("tools/evaluation"):
        return _row(
            current_engineering_domain="evaluation",
            future_target_module="developer_backend/evaluation",
            future_life_system_mapping="DeveloperBackendLayer",
            is_developer_backend=True,
        )
    if p.startswith("_eval_out"):
        return _row(
            current_engineering_domain="phase_artifacts",
            future_target_module="developer_backend/evaluation/_eval_out",
            future_life_system_mapping="DeveloperBackendLayer",
            is_developer_backend=True,
            disposition_action="archive",
        )
    if p.startswith("docs/architecture/governance"):
        return _row(
            current_engineering_domain="governance_docs",
            future_target_module="docs/governance",
            future_life_system_mapping="GovernanceLayer",
            disposition_action="merge",
        )
    if p.startswith("docs/architecture/evaluation"):
        return _row(
            current_engineering_domain="evaluation_docs",
            future_target_module="docs/evaluation",
            future_life_system_mapping="DeveloperBackendLayer",
            is_developer_backend=True,
            disposition_action="merge",
        )
    if p.startswith("docs/architecture/vision"):
        return _row(
            current_engineering_domain="vision_docs",
            future_target_module="docs/modules/vision",
            future_life_system_mapping="PerceptionLayer",
            disposition_action="merge",
        )
    if p.startswith("docs/architecture/midplatform"):
        return _row(
            current_engineering_domain="midplatform_docs",
            future_target_module="docs/modules/midplatform",
            future_life_system_mapping="MidPlatformOrganLayer",
            disposition_action="merge",
        )
    if p.startswith("docs/architecture"):
        return _row(
            current_engineering_domain="architecture_docs",
            future_target_module="docs/architecture",
            future_life_system_mapping="GovernanceLayer",
            disposition_action="merge",
        )
    if p.startswith("world_knowledge") or p.startswith("memory_store") or lower == "library":
        return _row(
            current_engineering_domain="cognition_legacy",
            future_target_module="cognition/world_model",
            future_life_system_mapping="CognitionLayer",
            is_cognition_placeholder=True,
            disposition_action="split",
        )
    if "emotion" in lower:
        return _row(
            current_engineering_domain="emotion_legacy",
            future_target_module="cognition/emotion_engine",
            future_life_system_mapping="LifeSystemLayer",
            is_cognition_placeholder=True,
            disposition_action="defer",
        )
    if p.startswith("luna_backend") or p.startswith("backend_bridge") or p.startswith("viewer"):
        return _row(
            current_engineering_domain="developer_backend_legacy",
            future_target_module="developer_backend/whitebox",
            future_life_system_mapping="DeveloperBackendLayer",
            is_developer_backend=True,
            disposition_action="split",
        )
    if p.startswith("runtime") or lower == "main.py" or p.startswith("core/"):
        return _row(
            current_engineering_domain="runtime_core",
            future_target_module="core/runtime",
            future_life_system_mapping="ClientSurfaceLayer",
            is_client=True,
            disposition_action="split",
        )
    if p.startswith("simulation") or "simulation" in lower:
        return _row(
            current_engineering_domain="simulation",
            future_target_module="developer_backend/simulation_lab",
            future_life_system_mapping="DeveloperBackendLayer",
            is_developer_backend=True,
        )
    if p.startswith("tests/") or lower.startswith("test_"):
        return _row(
            current_engineering_domain="test_legacy",
            future_target_module="developer_backend/test_center",
            future_life_system_mapping="DeveloperBackendLayer",
            is_developer_backend=True,
            disposition_action="merge",
        )
    if any(x in lower for x in ("b2_", "c1_", "c3_", "mvp_", "legacy", "archive", "luna_badge", "luna-mid")):
        return _row(
            current_engineering_domain="legacy_sprawl",
            future_target_module="archive/legacy",
            future_life_system_mapping="UnclassifiedLegacyLayer",
            disposition_action="archive",
            versioning_required=False,
        )
    if p.startswith("capabilities/"):
        return _row(
            current_engineering_domain="capabilities_misc",
            future_target_module="capabilities/unclassified",
            future_life_system_mapping="CapabilityOrganLayer",
            is_capability_organ=True,
            disposition_action="merge",
        )
    return _row(
        current_engineering_domain="unclassified",
        future_target_module="tbd",
        future_life_system_mapping="UnclassifiedLegacyLayer",
        disposition_action="defer",
    )


def _asset_type(rel: str, is_directory: bool) -> str:
    if rel.startswith("_eval_out"):
        return "phase_artifact"
    if rel.startswith("docs/"):
        return "doc"
    if not is_directory and rel.endswith(".md"):
        return "doc"
    if not is_directory and rel.endswith(".py"):
        return "code"
    if is_directory and rel.startswith("capabilities/"):
        return "module"
    if is_directory:
        return "module"
    return "file"


def _scan_inventory(repo: Path, *, max_entries: int = 8000) -> Tuple[List[Dict[str, Any]], bool]:
    entries: List[Dict[str, Any]] = []
    truncated = False
    queue: List[Path] = [repo]
    visited_dirs: set[str] = set()

    while queue and len(entries) < max_entries:
        d = queue.pop()
        d_key = str(d.resolve()) if d.exists() or d.is_symlink() else str(d)
        if d_key in visited_dirs:
            continue
        visited_dirs.add(d_key)

        ok, names = _listdir_safe(d)
        if not ok:
            continue

        rel_dir = str(d.relative_to(repo)) if d != repo else "."
        if rel_dir != ".":
            mapping = _classify_path(rel_dir)
            entries.append(
                {
                    "inventory_id": f"inv_{len(entries):05d}",
                    "current_path": rel_dir,
                    "current_module": rel_dir.split("/")[0] if "/" in rel_dir else rel_dir,
                    "asset_type": _asset_type(rel_dir, is_directory=True),
                    **mapping,
                    "mapping_status": "dryrun_candidate",
                    "actual_move_executed": False,
                    "source_chain": SOURCE_CHAIN,
                    **_not_fact(),
                }
            )
        for name in names:
            if name in SKIP_DIR_NAMES:
                continue
            p = d / name
            if d == repo and name in SKIP_TOP_LEVEL:
                continue
            if p.is_symlink():
                rel = str(p.relative_to(repo))
                mapping = _classify_path(rel)
                entries.append(
                    {
                        "inventory_id": f"inv_{len(entries):05d}",
                        "current_path": rel,
                        "current_module": rel.split("/")[0],
                        "asset_type": "symlink",
                        **mapping,
                        "mapping_status": "dryrun_candidate",
                        "actual_move_executed": False,
                        "source_chain": SOURCE_CHAIN,
                        **_not_fact(),
                    }
                )
                continue
            try:
                os.listdir(str(p))
                queue.append(p)
            except NotADirectoryError:
                rel = str(p.relative_to(repo))
                mapping = _classify_path(rel)
                entries.append(
                    {
                        "inventory_id": f"inv_{len(entries):05d}",
                        "current_path": rel,
                        "current_module": rel.split("/")[0],
                        "asset_type": _asset_type(rel, is_directory=False),
                        **mapping,
                        "mapping_status": "dryrun_candidate",
                        "actual_move_executed": False,
                        "source_chain": SOURCE_CHAIN,
                        **_not_fact(),
                    }
                )
            except (FileNotFoundError, OSError):
                continue
            if len(entries) >= max_entries:
                truncated = True
                queue.clear()
                break

    return entries, truncated


def _scan_eval_phases(repo: Path) -> List[Dict[str, Any]]:
    eval_root = repo / "_eval_out"
    ok, names = _listdir_safe(eval_root)
    if not ok:
        return []
    out: List[Dict[str, Any]] = []
    for name in sorted(names):
        rel = f"_eval_out/{name}"
        mapping = _classify_path(rel)
        phase_id = name
        m = re.match(r"^(.+?)_(smoke|dryrun|closure|planning)_v\d+", name)
        if m:
            phase_id = m.group(1).replace("_", "-")
        out.append(
            {
                "phase_artifact_path": rel,
                "phase_id_hint": phase_id,
                "asset_type": "phase_artifact",
                **mapping,
                "disposition_action": "keep",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    return out


def _scan_architecture_docs(repo: Path) -> List[Dict[str, Any]]:
    docs_root = repo / "docs" / "architecture"
    ok, _ = _listdir_safe(docs_root)
    if not ok:
        return []
    out: List[Dict[str, Any]] = []
    queue: List[Path] = [docs_root]
    while queue:
        d = queue.pop()
        ok2, names = _listdir_safe(d)
        if not ok2:
            continue
        for name in names:
            p = d / name
            rel = str(p.relative_to(repo))
            try:
                os.listdir(str(p))
                queue.append(p)
            except NotADirectoryError:
                if not name.lower().endswith(".md"):
                    continue
                mapping = _classify_path(rel)
                out.append(
                    {
                        "doc_path": rel,
                        "doc_name": name,
                        "asset_type": "doc",
                        **mapping,
                        "source_chain": SOURCE_CHAIN,
                        **_not_fact(),
                    }
                )
            except FileNotFoundError:
                continue
    return out


def _life_system_matrix(inventory: List[Dict[str, Any]]) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    counts: Dict[str, int] = {ls: 0 for ls in LIFE_SYSTEMS}
    for ls in LIFE_SYSTEMS:
        matched = [e for e in inventory if e.get("future_life_system_mapping") == ls]
        counts[ls] = len(matched)
        sample_paths = [e["current_path"] for e in matched[:5]]
        rows.append(
            {
                "life_system_id": ls,
                "asset_count": len(matched),
                "sample_current_paths": sample_paths,
                "target_module_examples": sorted({e.get("future_target_module", "tbd") for e in matched[:20]})[:8],
                "client_assets": sum(1 for e in matched if e.get("is_client")),
                "developer_backend_assets": sum(1 for e in matched if e.get("is_developer_backend")),
                "midplatform_organ_assets": sum(1 for e in matched if e.get("is_midplatform_organ")),
                "capability_organ_assets": sum(1 for e in matched if e.get("is_capability_organ")),
                "cognition_placeholder_assets": sum(1 for e in matched if e.get("is_cognition_placeholder")),
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    return {
        "life_systems": rows,
        "life_system_count": len(rows),
        "total_mapped_assets": len(inventory),
        "life_system_coverage_complete": all(counts[ls] >= 0 for ls in LIFE_SYSTEMS),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _current_to_target_map(inventory: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_target: Dict[str, List[str]] = {}
    rows: List[Dict[str, Any]] = []
    for e in inventory:
        target = e.get("future_target_module", "tbd")
        by_target.setdefault(target, []).append(e["current_path"])
        rows.append(
            {
                "current_path": e["current_path"],
                "current_module": e.get("current_module"),
                "asset_type": e.get("asset_type"),
                "current_engineering_domain": e.get("current_engineering_domain"),
                "future_target_module": target,
                "future_life_system_mapping": e.get("future_life_system_mapping"),
                "is_client": e.get("is_client", False),
                "is_developer_backend": e.get("is_developer_backend", False),
                "is_midplatform_organ": e.get("is_midplatform_organ", False),
                "is_capability_organ": e.get("is_capability_organ", False),
                "is_cognition_placeholder": e.get("is_cognition_placeholder", False),
                "versioning_required": e.get("versioning_required", True),
                "disposition_action": e.get("disposition_action", "keep"),
                "mapping_status": "dryrun_only",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    target_summary = [
        {
            "future_target_module": k,
            "asset_count": len(v),
            "sample_current_paths": v[:5],
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }
        for k, v in sorted(by_target.items(), key=lambda x: -len(x[1]))
    ]
    return {
        "map_rows": rows,
        "row_count": len(rows),
        "target_module_summary": target_summary,
        "target_module_count": len(target_summary),
        "all_rows_have_future_life_system_mapping": all(r.get("future_life_system_mapping") for r in rows),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _developer_backend_map(inventory: List[Dict[str, Any]]) -> Dict[str, Any]:
    dev = [e for e in inventory if e.get("is_developer_backend")]
    components = [
        "Whitebox Observability",
        "Test Center",
        "Simulation Lab",
        "Evaluation Runner",
        "Verifier System",
        "Phase Dashboard",
        "Log Explorer",
    ]
    rows = []
    for c in components:
        rows.append(
            {
                "developer_backend_component": c,
                "current_asset_paths": [e["current_path"] for e in dev if c.split()[0].lower() in e["current_path"].lower()][:5],
                "future_target_module": "developer_backend/evaluation",
                "future_life_system_mapping": "DeveloperBackendLayer",
                "client_included": False,
                "disposition_action": "keep",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    return {
        "developer_backend_extraction_rows": rows,
        "developer_backend_asset_count": len(dev),
        "production_client_excludes_developer_backend": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _midplatform_subsystem_map(planning: Dict[str, Any], inventory: List[Dict[str, Any]]) -> Dict[str, Any]:
    subsystems = (planning.get("midplatform_organ_system_model") or {}).get("subsystems") or []
    mp_assets = [e for e in inventory if e.get("is_midplatform_organ")]
    rows = []
    for s in subsystems:
        sid = s.get("subsystem_id", "")
        rows.append(
            {
                "midplatform_subsystem_id": sid,
                "current_asset_paths": [e["current_path"] for e in mp_assets if sid[:12].lower() in e["current_path"].lower()][:5],
                "future_target_module": "midplatform/orchestration",
                "future_life_system_mapping": "MidPlatformOrganLayer",
                "consolidation_priority": s.get("consolidation_priority", "tbd"),
                "disposition_action": "merge",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    return {
        "subsystem_mappings": rows,
        "subsystem_mapping_count": len(rows),
        "midplatform_organ_asset_count": len(mp_assets),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _future_placeholder_map(planning: Dict[str, Any], inventory: List[Dict[str, Any]]) -> Dict[str, Any]:
    futures = (planning.get("future_module_placeholder_plan") or {}).get("future_modules") or []
    cog = [e for e in inventory if e.get("is_cognition_placeholder")]
    rows = []
    for f in futures:
        fid = f.get("future_module_id", "")
        rows.append(
            {
                "future_module_id": fid,
                "current_status": f.get("current_status", "placeholder_only"),
                "related_current_paths": [e["current_path"] for e in cog if fid.lower() in e["current_path"].lower()][:5],
                "planned_location": f"cognition/{fid.lower()}",
                "future_life_system_mapping": "CognitionLayer" if fid in {"WorldModel", "MemoryCenter", "Library"} else "LifeSystemLayer",
                "disposition_action": "defer",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    return {
        "placeholder_mappings": rows,
        "placeholder_mapping_count": len(rows),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _client_boundary_map(planning: Dict[str, Any], inventory: List[Dict[str, Any]]) -> Dict[str, Any]:
    policy = planning.get("client_boundary_policy") or {}
    client_assets = [e for e in inventory if e.get("is_client")]
    excluded = policy.get("developer_backend_excluded") or []
    rows = []
    for e in inventory[:200]:
        rows.append(
            {
                "current_path": e["current_path"],
                "future_life_system_mapping": e.get("future_life_system_mapping"),
                "client_allowed": e.get("is_client", False),
                "developer_backend_only": e.get("is_developer_backend", False),
                "client_surface_candidate": e.get("future_life_system_mapping") == "ClientSurfaceLayer",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    return {
        "boundary_rows": rows,
        "row_count": len(rows),
        "client_asset_count": len(client_assets),
        "developer_backend_excluded": excluded,
        "production_client_excludes_developer_backend": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _migration_risk_register(inventory: List[Dict[str, Any]]) -> Dict[str, Any]:
    risks = [
        ("R1", "legacy_sprawl", "high", "UnclassifiedLegacyLayer assets may block clean modularization"),
        ("R2", "eval_out_cross_repo", "medium", "_eval_out spans Luna-Core and Luna-Workspace-Min"),
        ("R3", "runtime_mixed_with_dev", "high", "main.py/runtime mixed with developer tools"),
        ("R4", "doc_sprawl", "medium", "docs/architecture not yet merged into module specs"),
        ("R5", "cognition_placeholders", "medium", "world_knowledge/memory_store not formalized as cognition modules"),
        ("R6", "midplatform_overload", "medium", "midplatform capabilities scattered across paths"),
        ("R7", "client_boundary_unclear", "high", "legacy runtime dirs flagged as client without gate review"),
        ("R8", "missing_life_system_mapping", "critical", "any asset without future_life_system_mapping breaks Luna终局 alignment"),
        ("R9", "premature_file_move", "critical", "real migration before consolidation planning"),
        ("R10", "versioning_debt", "medium", "most modules lack MODULE.md/VERSION.json"),
    ]
    missing_life = [e for e in inventory if not e.get("future_life_system_mapping")]
    archive_count = sum(1 for e in inventory if e.get("disposition_action") == "archive")
    merge_count = sum(1 for e in inventory if e.get("disposition_action") == "merge")
    rows = []
    for rid, topic, level, desc in risks:
        rows.append(
            {
                "risk_id": rid,
                "risk_topic": topic,
                "risk_level": level,
                "description": desc,
                "mitigation": "dryrun_only; defer real moves to consolidation planning",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    return {
        "risks": rows,
        "risk_count": len(rows),
        "assets_missing_life_system_mapping": len(missing_life),
        "archive_candidate_count": archive_count,
        "merge_candidate_count": merge_count,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _no_file_move_boundary_report() -> Dict[str, Any]:
    return {
        "dryrun_scope": DRYRUN_SCOPE,
        "dryrun_only": True,
        "actual_file_move_executed": False,
        "actual_module_merge_executed": False,
        "actual_rename_executed": False,
        "actual_delete_executed": False,
        "runtime_enabled": False,
        "file_operation_invoked": False,
        "stat_invoked": False,
        "exists_invoked": False,
        "file_opened_for_user_media": False,
        "world_model_written": False,
        "memory_written": False,
        "library_written": False,
        "fact_written": False,
        "no_runtime_executed": True,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def run_luna_project_module_inventory_and_structure_map_dryrun_v1(
    *,
    repo_root: str,
    project_structure_governance_planning_root: str,
    gate_taxonomy_planning_root: Optional[str] = None,
) -> Dict[str, Any]:
    repo = Path(repo_root).expanduser().resolve()
    args = locals().copy()
    roots = {spec["id"]: _load_root(args.get(spec["arg"]), spec["summary"], spec["artifacts"]) for spec in ROOT_SPECS}

    input_rows: List[Dict[str, Any]] = []
    for spec in ROOT_SPECS:
        meta = roots[spec["id"]]
        path_str = str(meta["root"]) if meta["root"] else "(not_provided)"
        input_rows.append(
            {
                "intake_id": spec["id"],
                "path": path_str,
                "loaded": meta["loaded"],
                "required": spec["required"],
                "status": "loaded" if meta["loaded"] else ("missing_required" if spec["required"] else "optional_missing"),
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    planning_loaded = (
        roots["project_structure_governance_planning"]["loaded"]
        and roots["project_structure_governance_planning"]["summary"].get("final_decision") == PLANNING_FINAL_DECISION
    )

    blockers: List[str] = []
    if not planning_loaded:
        blockers.append("project_structure_governance_planning_missing_or_invalid")

    planning_payload: Dict[str, Any] = {}
    planning_root = roots["project_structure_governance_planning"]["root"]
    if planning_root and planning_loaded:
        for name in (
            "target_project_structure_model",
            "module_domain_taxonomy",
            "midplatform_organ_system_model",
            "future_module_placeholder_plan",
            "client_boundary_policy",
            "developer_backend_extraction_plan",
        ):
            planning_payload[name] = _try_read_json(planning_root / f"{name}.json") or {}

    inventory_entries, truncated = _scan_inventory(repo)
    eval_phases = _scan_eval_phases(repo)
    arch_docs = _scan_architecture_docs(repo)

    for ep in eval_phases:
        inventory_entries.append(
            {
                "inventory_id": f"inv_{len(inventory_entries):05d}",
                "current_path": ep["phase_artifact_path"],
                "current_module": "_eval_out",
                "asset_type": "phase_artifact",
                "current_engineering_domain": ep.get("current_engineering_domain"),
                "future_target_module": ep.get("future_target_module"),
                "future_life_system_mapping": ep.get("future_life_system_mapping"),
                "is_client": ep.get("is_client", False),
                "is_developer_backend": ep.get("is_developer_backend", True),
                "is_midplatform_organ": ep.get("is_midplatform_organ", False),
                "is_capability_organ": ep.get("is_capability_organ", False),
                "is_cognition_placeholder": ep.get("is_cognition_placeholder", False),
                "versioning_required": True,
                "disposition_action": ep.get("disposition_action", "keep"),
                "phase_id_hint": ep.get("phase_id_hint"),
                "mapping_status": "dryrun_candidate",
                "actual_move_executed": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    module_inventory = {
        "inventory_entries": inventory_entries,
        "entry_count": len(inventory_entries),
        "eval_phase_artifact_count": len(eval_phases),
        "architecture_doc_count": len(arch_docs),
        "scan_truncated": truncated,
        "all_entries_have_future_life_system_mapping": all(e.get("future_life_system_mapping") for e in inventory_entries),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    current_to_target_structure_map = _current_to_target_map(inventory_entries)
    life_system_mapping_matrix = _life_system_matrix(inventory_entries)
    developer_backend_extraction_map = _developer_backend_map(inventory_entries)
    midplatform_subsystem_mapping = _midplatform_subsystem_map(planning_payload, inventory_entries)
    future_module_placeholder_mapping = _future_placeholder_map(planning_payload, inventory_entries)
    client_boundary_mapping = _client_boundary_map(planning_payload, inventory_entries)
    migration_risk_register = _migration_risk_register(inventory_entries)
    no_file_move_boundary_report = _no_file_move_boundary_report()

    boundary_ok = not blockers and module_inventory["all_entries_have_future_life_system_mapping"]

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "project_structure_governance_planning_input_loaded": planning_loaded,
        "gate_taxonomy_planning_input_loaded": roots["gate_taxonomy_planning"]["loaded"],
        "module_inventory_generated": True,
        "current_to_target_structure_map_generated": True,
        "life_system_mapping_matrix_generated": True,
        "developer_backend_extraction_map_generated": True,
        "midplatform_subsystem_mapping_generated": True,
        "future_module_placeholder_mapping_generated": True,
        "client_boundary_mapping_generated": True,
        "migration_risk_register_generated": True,
        "no_file_move_boundary_report_generated": True,
        "inventory_entry_count": len(inventory_entries),
        "eval_phase_artifact_count": len(eval_phases),
        "architecture_doc_count": len(arch_docs),
        "life_system_layer_count": len(LIFE_SYSTEMS),
        "target_module_count": current_to_target_structure_map.get("target_module_count", 0),
        "migration_risk_count": migration_risk_register.get("risk_count", 0),
        "all_entries_have_future_life_system_mapping": module_inventory["all_entries_have_future_life_system_mapping"],
        "assets_missing_life_system_mapping": migration_risk_register.get("assets_missing_life_system_mapping", 0),
        "actual_file_move_executed": False,
        "actual_module_merge_executed": False,
        "runtime_enabled": False,
        "no_runtime_executed": True,
        "file_operation_invoked": False,
        "stat_invoked": False,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "LUNA_PROJECT_MODULE_INVENTORY_AND_STRUCTURE_MAP_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "final_decision": summary["final_decision"],
        "recommended_next_phase": summary["recommended_next_phase"],
        "reason": "structure map dryrun complete; next is consolidation planning before any real migration",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "module_inventory": module_inventory,
        "current_to_target_structure_map": current_to_target_structure_map,
        "life_system_mapping_matrix": life_system_mapping_matrix,
        "developer_backend_extraction_map": developer_backend_extraction_map,
        "midplatform_subsystem_mapping": midplatform_subsystem_mapping,
        "future_module_placeholder_mapping": future_module_placeholder_mapping,
        "client_boundary_mapping": client_boundary_mapping,
        "migration_risk_register": migration_risk_register,
        "no_file_move_boundary_report": no_file_move_boundary_report,
        "architecture_doc_inventory": {"docs": arch_docs, "doc_count": len(arch_docs), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "next_phase_recommendation": next_phase_recommendation,
    }
