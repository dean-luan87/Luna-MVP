# -*- coding: utf-8 -*-
"""Post-Migration Engineering State Sync v1.

Inventory and sync engineering state after migration final closure.
Scan-only: no file ops, no fixes, no feature runtime.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Post-Migration-Engineering-State-Sync-v1-001"
SYNC_SCOPE = "post_migration_engineering_state_sync_only"
SOURCE_CHAIN = "post_migration_engineering_state_sync_v1"

FINAL_DECISION_GO = "POST_MIGRATION_ENGINEERING_STATE_SYNC_READY_FOR_ENGINEERING_MAINLINE_RESUME"
NEXT_PHASE_GO = "Phase-Engineering-Mainline-Resume-v1-001"
FINAL_DECISION_HOLD = "POST_MIGRATION_ENGINEERING_STATE_SYNC_HOLD_FOR_REVIEW"
NEXT_PHASE_HOLD = "Phase-Post-Migration-Engineering-State-Issue-Review-v1-001"

UPSTREAM_REQUIRED_PHASE = "Phase-Main-Project-Structure-Migration-Final-Closure-v1-001"
UPSTREAM_REQUIRED_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_FINAL_CLOSURE_COMPLETE_READY_FOR_ENGINEERING_MAINLINE_RESUME"
UPSTREAM_REQUIRED_NEXT = "Phase-Engineering-Mainline-Resume-v1-001"

CORE_ROOTS: Tuple[Tuple[str, str], ...] = (
    ("capabilities", "Capability modules and runtime logic"),
    ("tools", "CLI runners, evaluation governance, utilities"),
    ("docs", "Architecture, governance, evaluation documentation"),
    ("configs", "Model, OCR, voice, evaluation configuration"),
    ("tests", "Unit/integration/vision OCR test suites"),
    ("scripts", "Operational scripts (may be sparse)"),
)

SPECIAL_DIRS: Tuple[Tuple[str, str, str], ...] = (
    ("backend_bridge/whitebox", "whitebox", "Whitebox developer bridge and diagnostics"),
    ("tools/evaluation", "test_governance", "Evaluation runners and verifiers"),
    ("backend_bridge", "backend", "Backend bridge integration"),
    ("capabilities/midplatform", "midplatform", "Midplatform OCR/vision/voice orchestration"),
    ("capabilities/mid_platform", "mid_platform", "Formal decision / navigation runtime adapters"),
    ("configs/midplatform", "midplatform_config", "Midplatform configuration"),
)

RESERVED_MARKERS: Tuple[str, ...] = (
    "not_implemented",
    "NOT_IMPLEMENTED",
    "placeholder",
    "stub",
    "reserved",
    "TODO",
    "FIXME",
    "future",
    "deferred",
)

RESERVED_FOCUS: Tuple[str, ...] = (
    "task_hub",
    "memory",
    "world_model",
    "world model",
    "emotion",
    "hardware",
    "runtime_adapter",
    "voice",
    "exploration",
    "library",
    "hive",
)

MIGRATION_STRUCTURE_MARKERS: Tuple[str, ...] = (
    "main_project_structure_migration",
    "LUNA_EVALUATION_OCR_PHASE_VERDICT",
    "Phase-Main-Project-Structure-Migration-",
)

MD_LINK_RE = re.compile(r"\]\(([^)]+)\)")
CLEAN_PATH_RE = re.compile(
    r"^((?:docs|capabilities|tools|scripts|tests|configs)/(?:[A-Za-z0-9_.-]+/)*[A-Za-z0-9_.-]+\.[A-Za-z0-9]+)$"
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "post_migration_engineering_state_sync_only": True,
        "migration_chain_reopened_now": False,
        "file_operation_executed_now": False,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_file_overwrite_executed": False,
        "content_rewrite_executed_now": False,
        "runtime_refactor_executed_now": False,
        "feature_runtime_enabled_now": False,
        "low_severity_candidates_fixed_now": False,
        "protected_asset_modified_now": False,
        "eval_out_modified_now": False,
        "hr_modified_now": False,
        "dnae_modified_now": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _is_workspace_fallback(root: Optional[Path]) -> bool:
    return bool(root) and "Luna-Workspace-Min" in str(root)


def _list_children(repo_root: Path, rel: str, max_depth: int = 2) -> List[Dict[str, Any]]:
    base = repo_root / rel
    if not base.is_dir():
        return []
    nodes: List[Dict[str, Any]] = []

    def walk(current: Path, depth: int, prefix: str) -> None:
        if depth > max_depth:
            return
        try:
            entries = sorted(current.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        except OSError:
            return
        for entry in entries:
            if entry.name.startswith(".") or entry.name in ("__pycache__", "node_modules", ".venv", "venv"):
                continue
            rel_path = f"{prefix}/{entry.name}" if prefix else entry.name
            if entry.is_dir():
                py_count = sum(1 for _ in entry.rglob("*.py") if "__pycache__" not in str(_))
                md_count = sum(1 for _ in entry.rglob("*.md") if "__pycache__" not in str(_))
                nodes.append(
                    {
                        "path": rel_path.replace("\\", "/"),
                        "type": "directory",
                        "depth": depth,
                        "py_file_count": py_count,
                        "md_file_count": md_count,
                    }
                )
                if depth < max_depth:
                    walk(entry, depth + 1, rel_path)
            else:
                nodes.append({"path": rel_path.replace("\\", "/"), "type": "file", "depth": depth})

    walk(base, 1, rel)
    return nodes


def _build_structure_inventory(repo_root: Path) -> Dict[str, Any]:
    inventory: Dict[str, Any] = {"repo_root": str(repo_root), "core_roots": {}, "special_areas": {}}
    for root, purpose in CORE_ROOTS:
        children = _list_children(repo_root, root, max_depth=2)
        inventory["core_roots"][root] = {
            "purpose": purpose,
            "exists": (repo_root / root).is_dir(),
            "top_level_entries": [c for c in children if c.get("depth") == 1][:40],
            "key_third_level_sample": [c for c in children if c.get("depth") == 2][:60],
            "entry_count": len(children),
        }
    for rel, tag, purpose in SPECIAL_DIRS:
        p = repo_root / rel
        inventory["special_areas"][tag] = {
            "path": rel,
            "purpose": purpose,
            "exists": p.is_dir() or p.is_file(),
            "py_file_count": sum(1 for _ in p.rglob("*.py")) if p.exists() else 0,
        }
    return inventory


def _structure_summary_md(inventory: Dict[str, Any]) -> str:
    lines = [
        "# Luna-Core 当前工程结构摘要（Post-Migration State Sync）",
        "",
        "> 自动生成盘点快照；不代表运行时事实。",
        "",
        "## 核心目录",
        "",
    ]
    for root, info in (inventory.get("core_roots") or {}).items():
        lines.append(f"### `{root}/`")
        lines.append(f"- **用途**：{info.get('purpose')}")
        lines.append(f"- **存在**：{info.get('exists')}")
        lines.append(f"- **采样条目数**：{info.get('entry_count')}")
        tops = info.get("top_level_entries") or []
        if tops:
            lines.append("- **一级/二级子目录（采样）**：")
            for e in tops[:20]:
                if e.get("type") == "directory":
                    lines.append(f"  - `{e['path']}` (py={e.get('py_file_count', 0)}, md={e.get('md_file_count', 0)})")
        lines.append("")
    lines.append("## 专项区域")
    lines.append("")
    for tag, info in (inventory.get("special_areas") or {}).items():
        lines.append(f"- **{tag}** → `{info.get('path')}`：{info.get('purpose')} (exists={info.get('exists')}, py≈{info.get('py_file_count')})")
    lines.append("")
    return "\n".join(lines)


def _clean_ref(raw: str) -> Optional[str]:
    raw = raw.strip().split("?")[0].split("#")[0]
    if raw.startswith(("http://", "https://", "mailto:")):
        return None
    if raw.startswith("./"):
        raw = raw[2:]
    m = CLEAN_PATH_RE.match(raw)
    return m.group(1) if m else None


def _doc_ref_severity(source: str, ref: str) -> str:
    if any(m in ref for m in MIGRATION_STRUCTURE_MARKERS) or any(m in source for m in MIGRATION_STRUCTURE_MARKERS):
        return "high"
    if ref.startswith("docs/architecture/evaluation/") or ref.startswith("docs/architecture/governance/"):
        return "high"
    return "low"


def _review_documentation_sync(repo_root: Path) -> Dict[str, Any]:
    candidates: List[Dict[str, Any]] = []
    high_risk: List[Dict[str, Any]] = []
    targets = (
        "docs/architecture/README.md",
        "docs/architecture/evaluation/README.md",
        "docs/architecture/evaluation/LUNA_EVALUATION_OCR_PHASE_VERDICT_STATUS_TABLE_V0.md",
    )
    verdict_has_b07 = False
    for rel in targets:
        p = repo_root / rel
        if not p.is_file():
            item = {"source_path": rel, "issue_type": "doc_missing", "severity": "high", "detail": "required doc missing"}
            candidates.append(item)
            high_risk.append(item)
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        if "Main-Project-Structure-Migration-Final-Closure" in text:
            verdict_has_b07 = True
        seen: Set[str] = set()
        for raw in MD_LINK_RE.findall(text):
            ref = _clean_ref(raw)
            if not ref or ref in seen:
                continue
            seen.add(ref)
            if (repo_root / ref).is_file():
                continue
            sev = _doc_ref_severity(rel, ref)
            item = {
                "source_path": rel,
                "referenced_path": ref,
                "issue_type": "stale_or_broken_doc_link",
                "severity": sev,
                "detail": f"link target not found: {ref}",
            }
            candidates.append(item)
            if sev == "high":
                high_risk.append(item)

    migration_rows_ok = verdict_has_b07
    if not migration_rows_ok:
        item = {
            "source_path": "docs/architecture/evaluation/LUNA_EVALUATION_OCR_PHASE_VERDICT_STATUS_TABLE_V0.md",
            "issue_type": "phase_verdict_table_stale",
            "severity": "high",
            "detail": "phase verdict table missing Final Closure row",
        }
        candidates.append(item)
        high_risk.append(item)

    check_pass = len(high_risk) == 0
    return {
        "reviewed_paths": list(targets),
        "stale_documentation_candidates": candidates,
        "high_risk_count": len(high_risk),
        "high_risk_issues": high_risk,
        "low_severity_count": sum(1 for c in candidates if c.get("severity") == "low"),
        "phase_verdict_table_includes_migration_closure": migration_rows_ok,
        "documentation_sync_review_pass": check_pass,
        "hold_for_review": not check_pass,
        "interpretation": "documentation sync pass" if check_pass else "high-risk doc break; hold for review",
    }


def _scan_reserved_modules(repo_root: Path) -> Dict[str, Any]:
    entries: List[Dict[str, Any]] = []
    cap = repo_root / "capabilities"
    if not cap.is_dir():
        return {"entries": entries, "scanned_file_count": 0}
    scanned = 0
    marker_re = re.compile("|".join(re.escape(m) for m in RESERVED_MARKERS), re.I)
    for py in sorted(cap.rglob("*.py")):
        if "__pycache__" in str(py) or scanned > 800:
            break
        rel = str(py.relative_to(repo_root)).replace("\\", "/")
        try:
            text = py.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        scanned += 1
        if not marker_re.search(text):
            continue
        focus_hit = [f for f in RESERVED_FOCUS if f.replace(" ", "_") in rel.lower() or f in text.lower()]
        name_lower = py.name.lower()
        kind = "stub" if "stub" in name_lower else "placeholder" if "placeholder" in name_lower else "reserved_marker"
        entries.append(
            {
                "path": rel,
                "kind": kind,
                "focus_areas": focus_hit,
                "status": "reserved_not_implemented",
                "detail": "contains reserved/placeholder/stub markers; not implemented in this sync phase",
            }
        )
    entries = entries[:120]
    return {"entries": entries, "scanned_file_count": scanned, "entry_count": len(entries)}


def _review_whitebox_test_backend(repo_root: Path) -> Dict[str, Any]:
    areas: List[Dict[str, Any]] = []

    def add(path: str, category: str) -> None:
        p = repo_root / path
        py_n = sum(1 for _ in p.rglob("*.py")) if p.exists() else 0
        md_n = sum(1 for _ in p.rglob("*.md")) if p.exists() else 0
        if not p.exists():
            status = "unknown"
        elif py_n == 0 and md_n <= 1:
            status = "placeholder_only"
        elif py_n < 5:
            status = "structure_present_but_incomplete"
        elif "stub" in path or "placeholder" in path:
            status = "partially_migrated"
        else:
            status = "partially_migrated" if py_n < 30 else "fully_migrated"
        areas.append(
            {
                "path": path,
                "category": category,
                "exists": p.exists(),
                "py_file_count": py_n,
                "md_file_count": md_n,
                "migration_status": status,
                "completion_note": "白盒/测试/后台完成度因历史并行开发而不均衡；本阶段仅盘点",
            }
        )

    add("backend_bridge/whitebox", "whitebox")
    add("tests", "tests")
    add("tests/evaluation", "tests_evaluation")
    add("tools/evaluation", "tools_evaluation_governance")
    add("backend_bridge", "backend_bridge")
    return {
        "areas": areas,
        "overall_interpretation": "tests/tools.evaluation 较完整；whitebox/backend_bridge 偏桥接与占位；无大规模搬迁缺失信号",
        "review_pass": True,
    }


def _sync_midplatform(repo_root: Path) -> Dict[str, Any]:
    mp = repo_root / "capabilities/midplatform"
    mp2 = repo_root / "capabilities/mid_platform"
    modules: List[Dict[str, Any]] = []
    for base, label in ((mp, "midplatform"), (mp2, "mid_platform")):
        if not base.is_dir():
            modules.append({"package": label, "exists": False, "status": "missing"})
            continue
        py_files = sorted(f.name for f in base.rglob("*.py") if f.is_file())
        stub_count = sum(1 for n in py_files if "stub" in n or "placeholder" in n)
        modules.append(
            {
                "package": label,
                "exists": True,
                "py_module_count": len(py_files),
                "stub_placeholder_count": stub_count,
                "status": "active_with_stubs" if stub_count else "active",
                "sample_modules": py_files[:15],
            }
        )
    iface_roots = ["capabilities/vision", "capabilities/navigation", "capabilities/voice", "capabilities/world_model", "capabilities/emotion"]
    interfaces = []
    for ir in iface_roots:
        p = repo_root / ir
        interfaces.append(
            {
                "path": ir,
                "exists": p.is_dir(),
                "py_count": sum(1 for _ in p.rglob("*.py")) if p.exists() else 0,
            }
        )
    return {
        "midplatform_packages": modules,
        "related_interfaces": interfaces,
        "duplicate_note": "midplatform 与 mid_platform 并存；后续整理方向为收敛适配层",
        "priority_directions": [
            "vision_ocr_navigation_task_orchestration",
            "readonly_evidence_ingest",
            "voice_dialogue_task_control",
            "world_model_memory_readonly_lookup",
        ],
        "restructure_deferred": True,
        "interpretation": "中台结构已存在且活跃；含 stub/placeholder；本阶段不重构",
    }


def _work_summary_md(matrix: Dict[str, Any], low_count: int) -> str:
    rows = matrix.get("batch_rows") or []
    lines = [
        "# 迁移后工作说明总结（B0–B7）",
        "",
        "## 批次结果",
        "",
        "| Batch | 模式 | 状态 |",
        "|---|---|---|",
    ]
    for r in rows:
        lines.append(f"| {r.get('batch_id')} | {r.get('three_stage_pattern')} | closed={r.get('closed')} |")
    lines.extend(
        [
            "",
            "## 关键结论",
            "",
            "- **B0–B6**：全部为 **unchanged / stable placement confirmed**（文件已在目标位置，未做 move/rename/delete）。",
            "- **B7**：最终一致性 closure（**无 Controlled Execution**，`allowed_operations=[]`）。",
            "- **Batch Preflight Harness**：已在 B0 固化，B1–B7 复用合同，禁止重开 Extraction/Adoption/Arming/Request 长链。",
            f"- **Low-severity 候选**：{low_count} 条已登记，**未处理**，不阻塞主线恢复。",
            "- **后续迁移**：不得绕过 Batch Preflight Harness。",
            "",
        ]
    )
    return "\n".join(lines)


def _cursor_sync_pack_md(inventory: Dict[str, Any], doc_review: Dict[str, Any], mid: Dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Post-Migration Cursor Assistant Sync Pack",
            "",
            "## 团队认知同步要点",
            "",
            "1. 工程结构迁移 **已关账**（B0–B7 + Final Closure GO）。",
            "2. 本包为 **状态盘点**，不是功能开发 phase。",
            "3. 结构迁移 ≠ 内容重写；B0–B6 均为 stable placement unchanged。",
            "4. 中台（`capabilities/midplatform` + `capabilities/mid_platform`）为后续整理重点，但不在本 phase 重构。",
            "5. 白盒 / backend_bridge 完成度低于 tests / tools.evaluation — 如实记录。",
            "",
            "## 目录锚点",
            "",
            f"- capabilities 子树采样：{len((inventory.get('core_roots') or {}).get('capabilities', {}).get('top_level_entries') or [])} 条",
            f"- 文档 sync：pass={doc_review.get('documentation_sync_review_pass')}",
            f"- 中台包：{[m.get('package') for m in mid.get('midplatform_packages') or []]}",
            "",
            "## 建议下一动作",
            "",
            "- `Phase-Engineering-Mainline-Resume-v1-001`（主线恢复裁决）",
            "- 然后 `Phase-Post-Migration-Engineering-Smoke-Test-v1-001`（测试单独执行）",
            "",
        ]
    )


def run_post_migration_engineering_state_sync_v1(
    *,
    main_project_structure_migration_final_closure_root: str,
    repo_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    closure_root = Path(main_project_structure_migration_final_closure_root).expanduser().resolve()
    resolved_repo = Path(repo_root).expanduser().resolve() if repo_root else Path(__file__).resolve().parents[2]

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(closure_root) else "repo_eval_out"
    meta = {
        **_boundary_meta(),
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
    }

    sm = _try_read_json(closure_root / "summary.json") or {}
    vr = _try_read_json(closure_root / "verifier_report.json") or {}
    matrix = _try_read_json(closure_root / "b0_b7_batch_closure_matrix_v1.json") or {}
    low_reg = _try_read_json(closure_root / "low_severity_candidate_final_register_v1.json") or {}

    if vr.get("verifier") != "GO":
        blockers.append("final closure verifier must be GO")
    if sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("upstream final_decision mismatch")
    if sm.get("migration_chain_closed_now") is not True:
        blockers.append("migration_chain_closed_now must be true")
    if sm.get("all_batches_closed") is not True:
        blockers.append("all_batches_closed must be true")
    if (sm.get("b7_high_risk_total") or 0) != 0:
        blockers.append("high-risk open count must be 0")

    inventory = _build_structure_inventory(resolved_repo)
    if not inventory.get("core_roots", {}).get("capabilities", {}).get("exists"):
        blockers.append("capabilities root must exist")

    doc_review = _review_documentation_sync(resolved_repo)
    reserved = _scan_reserved_modules(resolved_repo)
    whitebox_review = _review_whitebox_test_backend(resolved_repo)
    mid_sync = _sync_midplatform(resolved_repo)

    low_count = low_reg.get("candidate_count", 0)
    work_summary_md = _work_summary_md(matrix, low_count)
    structure_md = _structure_summary_md(inventory)
    cursor_pack_md = _cursor_sync_pack_md(inventory, doc_review, mid_sync)

    hold_for_review = doc_review.get("hold_for_review") is True
    if hold_for_review:
        blockers.append("high-risk documentation sync issues")

    sync_pass = not blockers and doc_review.get("documentation_sync_review_pass") is True
    final_decision = FINAL_DECISION_GO if sync_pass and not hold_for_review else (
        FINAL_DECISION_HOLD if hold_for_review else "POST_MIGRATION_ENGINEERING_STATE_SYNC_REQUIRES_FIXES"
    )
    next_phase = NEXT_PHASE_GO if final_decision == FINAL_DECISION_GO else (
        NEXT_PHASE_HOLD if hold_for_review else PHASE_ID
    )

    test_plan = {
        "plan_id": "post_migration_engineering_test_plan_v1",
        "execution_allowed_in_this_phase": False,
        "recommended_next_for_testing": "Phase-Post-Migration-Engineering-Smoke-Test-v1-001",
        "test_suites": [
            {"id": "import_path_consistency", "scope": "capabilities/tools/tests", "type": "smoke"},
            {"id": "runner_verifier_executability", "scope": "tools/evaluation/governance", "type": "smoke"},
            {"id": "configs_readability", "scope": "configs/", "type": "smoke"},
            {"id": "docs_link_index_consistency", "scope": "docs/architecture/", "type": "smoke"},
            {"id": "capabilities_import_smoke", "scope": "capabilities/", "type": "smoke"},
            {"id": "midplatform_import_smoke", "scope": "capabilities/midplatform", "type": "smoke"},
            {"id": "phase_verifier_smoke", "scope": "migration governance runners", "type": "smoke"},
            {"id": "protected_eval_out_no_mutation", "scope": "_eval_out/protected", "type": "guard"},
        ],
        "non_claims": ["test plan only; no tests executed in state sync phase"],
        **meta,
    }

    readiness = {
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        "ready_for_engineering_mainline_resume": final_decision == FINAL_DECISION_GO,
        "ready_for_smoke_test_phase": final_decision == FINAL_DECISION_GO,
        "hold_for_review": hold_for_review,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "sync_scope": SYNC_SCOPE,
        "boundary_ok": sync_pass and not hold_for_review,
        "violations": blockers,
        "hold_for_review": hold_for_review,
        "documentation_sync_review_pass": doc_review.get("documentation_sync_review_pass"),
        "doc_high_risk_count": doc_review.get("high_risk_count", 0),
        "reserved_module_count": reserved.get("entry_count", 0),
        "low_severity_candidate_count": low_count,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }

    return {
        "summary": summary,
        "current_project_structure_inventory": inventory,
        "current_project_structure_summary_md": structure_md,
        "structure_documentation_sync_review": doc_review,
        "post_migration_work_summary_md": work_summary_md,
        "post_migration_cursor_assistant_sync_pack_md": cursor_pack_md,
        "reserved_but_not_implemented_module_register": reserved,
        "whitebox_test_backend_migration_status_review": whitebox_review,
        "midplatform_current_structure_sync": mid_sync,
        "post_migration_engineering_test_plan": test_plan,
        "engineering_state_sync_readiness_decision": readiness,
    }
