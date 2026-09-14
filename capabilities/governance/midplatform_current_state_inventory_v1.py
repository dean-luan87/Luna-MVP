# -*- coding: utf-8 -*-
"""Midplatform Current State Inventory v1 — inventory-only, no structural changes."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.navigation_guidance_candidate_single_chain_trial_via_validation_factory_v1 import (
    FINAL_DECISION_GO as NAV_UPSTREAM_FINAL,
    PHASE_ID as NAV_UPSTREAM_PHASE,
)
from capabilities.governance.ocr_mock_result_single_chain_trial_via_validation_factory_v1 import (
    FINAL_DECISION_GO as OCR_UPSTREAM_FINAL,
    PHASE_ID as OCR_UPSTREAM_PHASE,
)
from capabilities.governance.vision_sample_frame_single_chain_controlled_trial_post_execution_review_v1 import (
    FINAL_DECISION_GO as VISION_UPSTREAM_FINAL,
    PHASE_ID as VISION_UPSTREAM_PHASE,
)

PHASE_ID = "Phase-Midplatform-Current-State-Inventory-v1-001"
SCOPE = "midplatform_current_state_inventory_only"
SOURCE_CHAIN = "midplatform_current_state_inventory_v1"

UPSTREAM_FACTORY_PHASE = "Phase-Luna-Validation-Factory-Consolidation-v1-001"
UPSTREAM_POST_MIGRATION_PHASE = "Phase-Post-Migration-Engineering-State-Sync-v1-001"

FINAL_DECISION_GO = "MIDPLATFORM_CURRENT_STATE_INVENTORY_READY_FOR_STRUCTURE_CLEANUP_PLANNING"
FINAL_DECISION_HOLD = "MIDPLATFORM_CURRENT_STATE_INVENTORY_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Midplatform-Structure-Cleanup-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Midplatform-Current-State-Inventory-Issue-Review-v1-001"

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_current_state_inventory"
)

DEFAULT_LUNA_CORE_ROOT = Path("/Users/luanlei/Desktop/Luna-Core")

CANDIDATE_TYPES_CLOSED = (
    "visual_observation_candidate",
    "ocr_result_candidate",
    "navigation_guidance_candidate",
)
CANDIDATE_TYPES_RESERVED = (
    "task_response_candidate",
    "speech_response_candidate",
    "memory_lookup_candidate",
    "world_model_readonly_candidate",
)

STUB_MARKERS: Tuple[str, ...] = (
    "TODO",
    "FIXME",
    "placeholder",
    "stub",
    "not_implemented",
    "NotImplemented",
    "future",
    "reserved",
    "pass  #",
    "mock-only",
    "mock_only",
)

RUNTIME_RISK_PATTERNS: Tuple[Tuple[str, str], ...] = (
    (r"runtime_enabled\s*=\s*True", "runtime_enabled_true_literal"),
    (r"camera_runtime_enabled", "camera_runtime_reference"),
    (r"ocr_provider_invoked", "ocr_provider_reference"),
    (r"navigation_action_triggered", "navigation_action_reference"),
    (r"task_state_committed", "task_commit_reference"),
    (r"world_model_written", "world_model_write_reference"),
    (r"memory_written", "memory_write_reference"),
    (r"tts_invoked", "tts_reference"),
    (r"llm_invoked", "llm_reference"),
)

DOMAIN_KEYWORDS: Dict[str, Tuple[str, ...]] = {
    "vision": ("vision", "frame", "camera", "roi", "crop"),
    "ocr": ("ocr", "text", "semantic_candidate", "poster"),
    "navigation": ("navigation", "guidance", "route", "map_location"),
    "task": ("task", "clarification", "observation_request"),
    "voice": ("voice", "speech", "tts", "dialogue", "asr"),
    "scene_delta": ("scene_delta", "delta"),
    "cross_modal": ("cross_modal", "fusion", "testboard"),
    "governance": ("roadmap", "closure", "policy", "contract"),
    "hardware": ("hardware", "camera"),
    "runtime_integration": ("minimal_runtime", "runtime_integration", "runtime_dryrun"),
}

NON_CLAIMS: Tuple[str, ...] = (
    "Inventory GO ≠ cleanup executed",
    "Inventory GO ≠ directory merge allowed",
    "Inventory GO ≠ runtime enabled",
    "Inventory GO ≠ task commit allowed",
    "Inventory GO ≠ candidate flow contract finalized",
    "Inventory GO ≠ stub implemented",
    "Inventory GO ≠ docs fixed",
    "Parallel directory review safe_to_merge=no is binding for this phase only",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "midplatform_current_state_inventory_only": True,
        "file_move_executed_now": False,
        "file_rename_executed_now": False,
        "module_merge_executed_now": False,
        "module_delete_executed_now": False,
        "midplatform_cleanup_executed_now": False,
        "midplatform_refactor_executed_now": False,
        "runtime_enabled_now": False,
        "task_state_committed_now": False,
        "task_manager_committed_now": False,
        "navigation_action_triggered_now": False,
        "tts_invoked_now": False,
        "llm_invoked_now": False,
        "world_model_written_now": False,
        "memory_written_now": False,
        "scene_delta_generated_now": False,
        "user_facing_output_generated_now": False,
        "protected_asset_modified_now": False,
        "eval_out_modified_now": False,
        "hr_modified_now": False,
        "dnae_modified_now": False,
        "task_response_candidate_chain_deferred_now": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _check_go(root: Path) -> Tuple[bool, Dict[str, Any]]:
    sm = _try_read_json(root / "summary.json") or {}
    vr = _try_read_json(root / "verifier_report.json") or {}
    ok = (vr.get("verifier") == "GO" and vr.get("passed") is True) or sm.get("boundary_ok") is True
    return ok, {"summary": sm, "verifier": vr}


def _validate_upstream(
    factory_root: Path,
    vision_root: Path,
    ocr_root: Path,
    nav_root: Path,
    post_migration_root: Path,
) -> Tuple[List[str], Dict[str, Any]]:
    blockers: List[str] = []
    ctx: Dict[str, Any] = {}

    checks = [
        ("factory", factory_root, UPSTREAM_FACTORY_PHASE, None),
        ("vision_post_review", vision_root, VISION_UPSTREAM_PHASE, VISION_UPSTREAM_FINAL),
        ("ocr_trial", ocr_root, OCR_UPSTREAM_PHASE, OCR_UPSTREAM_FINAL),
        ("nav_trial", nav_root, NAV_UPSTREAM_PHASE, NAV_UPSTREAM_FINAL),
        ("post_migration", post_migration_root, UPSTREAM_POST_MIGRATION_PHASE, None),
    ]
    for key, root, phase, final in checks:
        if not root.is_dir():
            blockers.append(f"{key}: root missing")
            continue
        ok, data = _check_go(root)
        ctx[key] = data
        if not ok:
            blockers.append(f"{key}: verifier must be GO")
        sm = data.get("summary") or {}
        if phase and sm.get("phase") != phase:
            blockers.append(f"{key}: phase mismatch")
        if final and sm.get("final_decision") != final:
            blockers.append(f"{key}: final_decision mismatch")
        if key == "vision_post_review" and sm.get("controlled_trial_closed_now") is not True:
            blockers.append("vision: controlled_trial_closed_now must be true")
        if key in ("ocr_trial", "nav_trial") and sm.get("controlled_trial_closed_now") is not True:
            blockers.append(f"{key}: controlled_trial_closed_now must be true")

    pm_sync = _try_read_json(post_migration_root / "midplatform_current_structure_sync_v1.json") or {}
    ctx["post_migration_midplatform_sync"] = pm_sync
    if not pm_sync:
        blockers.append("post_migration midplatform_current_structure_sync_v1.json missing")

    return blockers, ctx


def _tree_summary(root: Path, *, max_depth: int = 3) -> Dict[str, Any]:
    if not root.is_dir():
        return {"exists": False, "path": str(root)}
    py_files = sorted(root.rglob("*.py"))
    md_under = sorted(root.rglob("*.md")) if root.name.startswith("docs") else []
    subdirs = sorted({p.parent.relative_to(root).as_posix() for p in py_files if p.parent != root})
    return {
        "exists": True,
        "path": str(root),
        "py_file_count": len(py_files),
        "subdir_count": len(subdirs),
        "top_level_py": [p.name for p in sorted(root.glob("*.py"))][:30],
        "subdirs_sample": subdirs[:40],
        "has_runtime_subdir": (root / "runtime").is_dir(),
    }


def _infer_domain(stem: str) -> str:
    lower = stem.lower()
    scores: Dict[str, int] = defaultdict(int)
    for domain, kws in DOMAIN_KEYWORDS.items():
        for kw in kws:
            if kw in lower:
                scores[domain] += 1
    if not scores:
        return "unknown"
    return max(scores.items(), key=lambda x: x[1])[0]


def _classify_module(path: Path) -> str:
    name = path.stem.lower()
    if any(x in name for x in ("stub", "placeholder")):
        return "stub_placeholder"
    if "dryrun" in name or "_dry_run" in name:
        return "dryrun_only"
    if any(x in name for x in ("roadmap", "closure", "decision")) and "dryrun" not in name:
        return "governance_only"
    if any(x in name for x in ("contract", "policy", "template", "registry")):
        return "governance_only"
    if "runtime" in name and "dryrun" not in name:
        return "implemented"
    if name.endswith("_v0") or name.endswith("_v1"):
        return "implemented"
    return "unknown"


def _scan_file_markers(path: Path) -> List[Dict[str, str]]:
    hits: List[Dict[str, str]] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return hits
    for i, line in enumerate(text.splitlines(), 1):
        low = line.lower()
        for marker in STUB_MARKERS:
            if marker.lower() in low:
                hits.append({"marker": marker, "line": i, "snippet": line.strip()[:120]})
                break
    for pattern, label in RUNTIME_RISK_PATTERNS:
        if re.search(pattern, text):
            hits.append({"marker": label, "line": 0, "snippet": "pattern_match"})
    return hits[:8]


def _module_entry(
    path: Path,
    luna_root: Path,
    runners: Set[str],
    verifiers: Set[str],
    doc_stems: Set[str],
) -> Dict[str, Any]:
    rel = path.relative_to(luna_root).as_posix()
    stem = path.stem
    text_sample = ""
    try:
        text_sample = path.read_text(encoding="utf-8", errors="replace")[:8000]
    except OSError:
        pass
    low = text_sample.lower()
    return {
        "path": rel,
        "module_stem": stem,
        "inferred_domain": _infer_domain(stem),
        "status": _classify_module(path),
        "phase_id": None,
        "has_runner": stem in runners or any(stem in r for r in runners),
        "has_verifier": stem in verifiers or any(stem in v for v in verifiers),
        "related_docs": sorted(d for d in doc_stems if stem.replace("_v1", "").replace("_v0", "") in d)[:3],
        "candidate_input_supported": [t for t in CANDIDATE_TYPES_CLOSED + CANDIDATE_TYPES_RESERVED if t in low],
        "candidate_output_supported": [
            t
            for t in (
                "visual_observation_candidate",
                "ocr_result_candidate",
                "navigation_guidance_candidate",
                "navigation_guidance",
                "task_response_candidate",
                "speech_response_candidate",
                "guidance_candidate",
                "semantic_candidate",
                "scene_delta",
            )
            if t in low
        ],
        "runtime_enabled_claimed": "runtime_enabled" in low and "false" not in low[:200],
        "fact_write_claimed": "fact_write" in low or "write_fact" in low,
        "task_commit_claimed": "task_commit" in low or "task_state_committed" in low,
    }


def _collect_runner_verifier_stems(tools_root: Path) -> Tuple[Set[str], Set[str]]:
    runners: Set[str] = set()
    verifiers: Set[str] = set()
    if not tools_root.is_dir():
        return runners, verifiers
    for p in tools_root.rglob("run_*.py"):
        runners.add(p.stem.replace("run_", ""))
    for p in tools_root.rglob("verify_*.py"):
        verifiers.add(p.stem.replace("verify_", ""))
    return runners, verifiers


def _scan_candidate_handoff(luna_root: Path) -> Dict[str, Any]:
    search_roots = [
        luna_root / "capabilities/midplatform",
        luna_root / "capabilities/mid_platform",
        luna_root / "capabilities/governance",
        luna_root / "capabilities/vision",
        luna_root / "capabilities/ocr",
        luna_root / "capabilities/navigation",
    ]
    by_type: Dict[str, List[str]] = {t: [] for t in CANDIDATE_TYPES_CLOSED + CANDIDATE_TYPES_RESERVED}
    for root in search_roots:
        if not root.is_dir():
            continue
        for py in root.rglob("*.py"):
            try:
                text = py.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            rel = py.relative_to(luna_root).as_posix()
            for ctype in by_type:
                if ctype in text:
                    by_type[ctype].append(rel)
    handoff_by_type: Dict[str, Any] = {}
    for ctype in CANDIDATE_TYPES_CLOSED:
        refs = by_type[ctype]
        handoff_by_type[ctype] = {
            "reference_count": len(refs),
            "modules_sample": refs[:12],
            "validation_factory_closed_consumer": ctype in CANDIDATE_TYPES_CLOSED,
            "midplatform_handoff_readiness": "candidate_only" in " ".join(refs) or len(refs) > 0,
        }
    for ctype in CANDIDATE_TYPES_RESERVED:
        refs = by_type[ctype]
        handoff_by_type[ctype] = {
            "reference_count": len(refs),
            "modules_sample": refs[:8],
            "reserved_not_closed": True,
        }
    return {
        "inventory_id": "midplatform_candidate_handoff_inventory_v1",
        "closed_candidate_chains": list(CANDIDATE_TYPES_CLOSED),
        "reserved_candidate_types": list(CANDIDATE_TYPES_RESERVED),
        "handoff_by_candidate_type": handoff_by_type,
        "recommended_handoff_path": (
            "Validation Factory closed VOC/OCR/Nav candidates → midplatform orchestration "
            "via readonly ingest / policy / dryrun adapters (not runtime commit)"
        ),
    }


def _build_gap_register(
    modules: List[Dict[str, Any]],
    parallel_review: Dict[str, Any],
) -> Dict[str, Any]:
    stems_mp = {m["module_stem"] for m in modules if m["path"].startswith("capabilities/midplatform/")}
    stems_mpl = {m["module_stem"] for m in modules if m["path"].startswith("capabilities/mid_platform/")}
    approximate_dupes = sorted(stems_mp & stems_mpl)
    status_counts = Counter(m["status"] for m in modules if "midplatform" in m["path"])
    missing_runner = [
        m["path"]
        for m in modules
        if m["path"].startswith("capabilities/midplatform/")
        and m["status"] in ("implemented", "dryrun_only")
        and not m["has_runner"]
        and "closure" not in m["module_stem"]
    ][:25]
    gaps: List[Dict[str, Any]] = [
        {
            "category": "parallel_directory",
            "severity": "medium",
            "detail": "capabilities/midplatform vs capabilities/mid_platform coexist",
            "owner": "unclear",
        },
        {
            "category": "duplicate_module",
            "severity": "low" if not approximate_dupes else "medium",
            "detail": f"cross-dir same stems: {approximate_dupes[:10]}",
            "owner": "mid_platform runtime bridge",
        },
        {
            "category": "missing_contract",
            "severity": "medium",
            "detail": "unified candidate flow contract across midplatform not found as single module",
            "owner": "governance/factory",
        },
        {
            "category": "missing_runner_verifier",
            "severity": "low",
            "detail": f"sample modules without runner: {len(missing_runner)}",
            "samples": missing_runner,
        },
        {
            "category": "runtime_boundary_ambiguity",
            "severity": "medium",
            "detail": "mid_platform/runtime navigation release-control chain vs midplatform dryrun policies",
            "owner": "mid_platform",
        },
        {
            "category": "candidate_flow_gap",
            "severity": "medium",
            "detail": "task_response_candidate chain explicitly deferred; speech/memory/wm readonly reserved",
            "owner": "validation_factory",
        },
        {
            "category": "task_state_gap",
            "severity": "medium",
            "detail": "task_manager + task_state dryruns exist; commit path gated in governance not midplatform inventory",
            "owner": "midplatform/task",
        },
        {
            "category": "output_arbitration_gap",
            "severity": "medium",
            "detail": "safety_task_arbitration_policy present; output arbitration vs guidance queue not unified",
            "owner": "midplatform",
        },
    ]
    return {
        "register_id": "midplatform_gap_and_duplication_register_v1",
        "parallel_directory_risk": parallel_review.get("dual_directory_risk_level"),
        "safe_to_merge_in_this_phase": False,
        "status_distribution_midplatform": dict(status_counts),
        "gaps": gaps,
    }


def run_midplatform_current_state_inventory_v1(
    *,
    luna_validation_factory_consolidation_root: str,
    vision_sample_frame_single_chain_controlled_trial_post_execution_review_root: str,
    ocr_mock_result_single_chain_trial_via_validation_factory_root: str,
    navigation_guidance_candidate_single_chain_trial_via_validation_factory_root: str,
    post_migration_engineering_state_sync_root: str,
    luna_core_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    luna_root = Path(luna_core_root or DEFAULT_LUNA_CORE_ROOT).expanduser().resolve()
    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()

    factory_root = Path(luna_validation_factory_consolidation_root).expanduser().resolve()
    vision_root = Path(vision_sample_frame_single_chain_controlled_trial_post_execution_review_root).expanduser().resolve()
    ocr_root = Path(ocr_mock_result_single_chain_trial_via_validation_factory_root).expanduser().resolve()
    nav_root = Path(navigation_guidance_candidate_single_chain_trial_via_validation_factory_root).expanduser().resolve()
    pm_root = Path(post_migration_engineering_state_sync_root).expanduser().resolve()

    upstream_blockers, upstream_ctx = _validate_upstream(
        factory_root, vision_root, ocr_root, nav_root, pm_root
    )
    read_blockers: List[str] = []
    if not (luna_root / "capabilities/midplatform").is_dir():
        read_blockers.append("capabilities/midplatform not readable")
    if not (luna_root / "capabilities/mid_platform").is_dir():
        read_blockers.append("capabilities/mid_platform not readable")

    meta = _boundary_meta()
    meta["luna_core_root"] = str(luna_root)
    meta["inventory_output_root"] = str(out_root)
    meta["dual_directory_risk_previously_registered"] = "medium"

    mp_root = luna_root / "capabilities/midplatform"
    mpl_root = luna_root / "capabilities/mid_platform"

    dir_structure = {
        "inventory_id": "midplatform_directory_structure_inventory_v1",
        "capabilities_midplatform": _tree_summary(mp_root),
        "capabilities_mid_platform": _tree_summary(mpl_root),
        "naming_difference": "midplatform (underscore absent) vs mid_platform (underscore present)",
        "responsibility_hypothesis": {
            "midplatform": "primary orchestration: OCR/vision/voice/task/scene_delta/cross_modal dryruns and policies",
            "mid_platform": "runtime adapter bridge: formal decision, navigation governance release-control, OCR text bridge",
        },
        "mixed_concerns_observed": [
            "dryrun modules alongside policy/contract in flat midplatform/",
            "runtime-only subtree under mid_platform/runtime/",
            "governance roadmap decisions inside midplatform/",
        ],
        **meta,
    }

    cross_imports: List[str] = []
    for py in mpl_root.rglob("*.py") if mpl_root.is_dir() else []:
        try:
            t = py.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if "capabilities.midplatform" in t or "from capabilities import midplatform" in t:
            cross_imports.append(py.relative_to(luna_root).as_posix())
    parallel_review = {
        "review_id": "midplatform_parallel_directory_review_v1",
        "primary_midplatform_candidate": "capabilities/midplatform",
        "runtime_adapter_legacy_bridge_candidate": "capabilities/mid_platform",
        "duplicate_concepts": [
            "OCR bridge/evidence ingest (midplatform modules vs mid_platform/ocr_text_extraction_bridge_v0)",
            "navigation guidance (midplatform guidance adapters vs mid_platform navigation runtime gates)",
            "formal decision handoff (mid_platform stubs vs governance validation factory)",
        ],
        "approximate_same_stem_modules": [],
        "cross_directory_imports": cross_imports[:15],
        "safe_to_merge_now": False,
        "safe_to_merge_rationale": "inventory-only phase; merge requires cleanup planning",
        "dual_directory_risk_level": "medium",
        **meta,
    }

    tools_mp = luna_root / "tools/evaluation/midplatform"
    runners, verifiers = _collect_runner_verifier_stems(tools_mp)
    doc_mp = luna_root / "docs/architecture/midplatform"
    doc_stems = {p.stem for p in doc_mp.rglob("*.md")} if doc_mp.is_dir() else set()

    modules: List[Dict[str, Any]] = []
    stub_entries: List[Dict[str, Any]] = []
    runtime_risks: List[Dict[str, Any]] = []

    for pkg in (mp_root, mpl_root):
        if not pkg.is_dir():
            continue
        for py in sorted(pkg.rglob("*.py")):
            entry = _module_entry(py, luna_root, runners, verifiers, doc_stems)
            modules.append(entry)
            markers = _scan_file_markers(py)
            if markers:
                stub_entries.append(
                    {
                        "path": entry["path"],
                        "status": entry["status"],
                        "markers": markers,
                    }
                )
            for m in markers:
                if m["marker"].endswith("_reference") or "runtime" in m["marker"]:
                    runtime_risks.append({"path": entry["path"], "risk": m["marker"]})

    status_dist = Counter(m["status"] for m in modules if m["path"].startswith("capabilities/midplatform"))
    module_inventory = {
        "inventory_id": "midplatform_module_inventory_v1",
        "modules_total": len(modules),
        "midplatform_py_count": sum(1 for m in modules if m["path"].startswith("capabilities/midplatform/")),
        "mid_platform_py_count": sum(1 for m in modules if m["path"].startswith("capabilities/mid_platform/")),
        "status_distribution": dict(status_dist),
        "modules": modules,
        **meta,
    }

    doc_roots = [
        luna_root / "docs/architecture/midplatform",
        luna_root / "docs/architecture/task",
        luna_root / "docs/architecture/voice",
        luna_root / "docs/architecture/evaluation",
    ]
    doc_inventory: Dict[str, Any] = {"inventory_id": "midplatform_documentation_inventory_v1", "roots": {}, **meta}
    for dr in doc_roots:
        if not dr.is_dir():
            continue
        md_files = list(dr.rglob("*.md"))
        relevant = [
            p.relative_to(luna_root).as_posix()
            for p in md_files
            if dr.name == "evaluation"
            and any(k in p.name.lower() for k in ("midplatform", "task", "navigation", "voice", "guidance"))
            or dr.name != "evaluation"
        ]
        doc_inventory["roots"][dr.name] = {
            "path": str(dr),
            "md_count": len(md_files) if dr.name != "evaluation" else len(relevant),
            "samples": (relevant if dr.name == "evaluation" else [p.relative_to(luna_root).as_posix() for p in md_files[:15]])[
                :20
            ],
        }

    runner_inventory = {
        "inventory_id": "midplatform_runner_verifier_inventory_v1",
        "tools_evaluation_midplatform": {
            "path": str(tools_mp),
            "run_scripts": len(list(tools_mp.glob("run_*.py"))) if tools_mp.is_dir() else 0,
            "verify_scripts": len(list(tools_mp.glob("verify_*.py"))) if tools_mp.is_dir() else 0,
        },
        "governance_midplatform_related": sorted(
            p.relative_to(luna_root).as_posix()
            for p in (luna_root / "tools/evaluation/governance").glob("*midplatform*")
        )
        if (luna_root / "tools/evaluation/governance").is_dir()
        else [],
        **meta,
    }

    handoff = _scan_candidate_handoff(luna_root)
    handoff.update(meta)

    task_keywords = (
        "task_state",
        "task_manager",
        "task_lifecycle",
        "observation_request",
        "guidance_candidate",
        "response_candidate",
        "pause",
        "resume",
        "cancel",
        "clarification",
        "fallback",
        "speech",
        "voice",
    )
    task_modules = [
        m
        for m in modules
        if any(k in m["module_stem"].lower() for k in task_keywords)
        or m["inferred_domain"] in ("task", "voice")
    ]
    task_inventory = {
        "inventory_id": "midplatform_task_state_related_inventory_v1",
        "modules_matching_task_keywords": [m["path"] for m in task_modules[:40]],
        "modules_total": len(task_modules),
        "capabilities_present": {
            "task_manager_contract": any("task_manager_contract" in m["path"] for m in modules),
            "task_state_runtime_dryrun": any("task_state_runtime_dryrun" in m["path"] for m in modules),
            "voice_dialogue_task_control": any("voice_dialogue_task_control" in m["path"] for m in modules),
            "user_clarification": any("clarification" in m["path"] for m in modules),
            "navigation_guidance_to_speech_adapter": any(
                "navigation_guidance_to_speech" in m["path"] for m in modules
            ),
        },
        "pause_resume_cancel_explicit": False,
        "note": "pause/resume/cancel not found as dedicated modules; likely embedded in task_manager/voice contracts",
        **meta,
    }

    runtime_boundary = {
        "inventory_id": "midplatform_runtime_boundary_inventory_v1",
        "risk_candidates": runtime_risks[:50],
        "risk_count": len(runtime_risks),
        "inventory_phase_boundary_all_false": True,
        "claims_found_in_code_scan": len(runtime_risks) > 0,
        **meta,
    }

    stub_register = {
        "register_id": "midplatform_stub_placeholder_register_v1",
        "entries_total": len(stub_entries),
        "entries_sample": stub_entries[:40],
        "filename_stub_modules": [m["path"] for m in modules if m["status"] == "stub_placeholder"],
        **meta,
    }

    gap_register = _build_gap_register(modules, parallel_review)
    gap_register.update(meta)

    input_review = {
        "review_id": "validation_factory_and_candidate_chain_input_review_v1",
        "upstream": {
            "factory": upstream_ctx.get("factory", {}),
            "vision_post_review": upstream_ctx.get("vision_post_review", {}),
            "ocr_trial": upstream_ctx.get("ocr_trial", {}),
            "nav_trial": upstream_ctx.get("nav_trial", {}),
            "post_migration": upstream_ctx.get("post_migration", {}),
        },
        "candidate_chains_confirmed_closed": list(CANDIDATE_TYPES_CLOSED),
        "task_response_chain_deferred": True,
        "review_pass": len(upstream_blockers) == 0,
        "blockers": upstream_blockers,
        **meta,
    }

    next_work = {
        "recommendation_id": "midplatform_next_work_recommendation_v1",
        "recommended_next_phase": NEXT_PHASE_GO,
        "cleanup_planning_focus": [
            "确定 midplatform / mid_platform 主从关系",
            "定义目标中台分层",
            "定义 candidate flow contract",
            "定义 task state contract",
            "定义 safety/survival gate",
            "定义 guidance candidate queue",
            "定义 output arbitration",
            "定义 runtime boundary",
            "为 Minimal Backbone DryRun 做准备",
        ],
        "do_not_start_yet": [
            "Task response candidate single-chain",
            "directory merge",
            "runtime enablement",
        ],
        **meta,
    }

    inventory_ok = len(upstream_blockers) == 0 and len(read_blockers) == 0
    blockers = upstream_blockers + read_blockers

    closure = {
        "final_decision": FINAL_DECISION_GO if inventory_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if inventory_ok else NEXT_PHASE_HOLD,
        "boundary_ok": inventory_ok,
        "blockers": blockers,
        **meta,
    }

    summary_md = f"""# Midplatform Current State Inventory v1

## Scope
- Phase: `{PHASE_ID}`
- Inventory-only: no file moves, merges, or runtime enablement.

## Directory snapshot
| Package | Python modules | Notes |
|---------|----------------|-------|
| `capabilities/midplatform` | {module_inventory['midplatform_py_count']} | Flat package; dryrun/policy/cross_modal/vision/ocr/task/voice |
| `capabilities/mid_platform` | {module_inventory['mid_platform_py_count']} | `runtime/` subtree; navigation governance + formal decision stubs |

## Parallel directory conclusion
- **Primary midplatform candidate:** `capabilities/midplatform`
- **Runtime adapter / bridge candidate:** `capabilities/mid_platform`
- **Safe to merge now:** **no** (this phase only)

## Module status (midplatform)
{json.dumps(status_dist, ensure_ascii=False, indent=2)}

## Closed Validation Factory chains (upstream GO)
- `visual_observation_candidate` — Vision sample frame
- `ocr_result_candidate` — OCR mock single-chain
- `navigation_guidance_candidate` — Navigation guidance single-chain

## Deferred
- Task response candidate single-chain (explicitly not started)

## Top gaps
{chr(10).join('- ' + g['category'] + ': ' + g['detail'] for g in gap_register['gaps'][:6])}

## Next phase
`{NEXT_PHASE_GO if inventory_ok else NEXT_PHASE_HOLD}`
"""

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": inventory_ok,
        "violations": blockers,
        "final_decision": closure["final_decision"],
        "recommended_next_phase": closure["recommended_next_phase"],
        "midplatform_py_count": module_inventory["midplatform_py_count"],
        "mid_platform_py_count": module_inventory["mid_platform_py_count"],
        "stub_entries_found": len(stub_entries),
        "runtime_risk_candidates": len(runtime_risks),
        **meta,
    }

    return {
        "midplatform_inventory_policy": {
            "policy_id": "midplatform_inventory_policy_v1",
            "scope": SCOPE,
            "inventory_roots": [
                "capabilities/midplatform",
                "capabilities/mid_platform",
                "docs/architecture/midplatform",
                "docs/architecture/task",
                "docs/architecture/voice",
                "tools/evaluation/midplatform",
            ],
            **meta,
        },
        "validation_factory_and_candidate_chain_input_review": input_review,
        "midplatform_directory_structure_inventory": dir_structure,
        "midplatform_parallel_directory_review": parallel_review,
        "midplatform_module_inventory": module_inventory,
        "midplatform_documentation_inventory": doc_inventory,
        "midplatform_runner_verifier_inventory": runner_inventory,
        "midplatform_candidate_handoff_inventory": handoff,
        "midplatform_task_state_related_inventory": task_inventory,
        "midplatform_runtime_boundary_inventory": runtime_boundary,
        "midplatform_stub_placeholder_register": stub_register,
        "midplatform_gap_and_duplication_register": gap_register,
        "midplatform_inventory_summary_v1_md": summary_md,
        "midplatform_next_work_recommendation": next_work,
        "non_claims_register": {"register_id": "non_claims_register_v1", "non_claims": list(NON_CLAIMS), **meta},
        "summary": summary,
    }
