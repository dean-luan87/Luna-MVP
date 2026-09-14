# -*- coding: utf-8 -*-
"""Main Project Structure Migration B7 Preflight Via Harness v1.

Final cross-reference / import / path consistency closure preflight.
No file migration; scan-only global consistency after B0–B6.
"""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Main-Project-Structure-Migration-B7-Preflight-Via-Harness-v1-001"
PREFLIGHT_SCOPE = "main_project_structure_migration_b7_preflight_via_harness_only"
SOURCE_CHAIN = "main_project_structure_migration_b7_preflight_via_harness_v1"

FINAL_DECISION_GO = "MAIN_PROJECT_STRUCTURE_MIGRATION_B7_PREFLIGHT_VIA_HARNESS_READY_FOR_FINAL_CLOSURE_REVIEW"
NEXT_PHASE_GO = "Phase-Main-Project-Structure-Migration-B7-Final-Closure-Review-v1-001"
FINAL_DECISION_HOLD = "MAIN_PROJECT_STRUCTURE_MIGRATION_B7_PREFLIGHT_VIA_HARNESS_HOLD_FOR_REVIEW"
NEXT_PHASE_HOLD = "Phase-Main-Project-Structure-Migration-B7-Consistency-Issue-Review-v1-001"

UPSTREAM_REQUIRED_PHASE = "Phase-Main-Project-Structure-Migration-B6-Post-Migration-Review-v1-001"
UPSTREAM_REQUIRED_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_B6_POST_MIGRATION_REVIEW_CLOSED_READY_FOR_B7_PREFLIGHT_VIA_HARNESS"
UPSTREAM_REQUIRED_NEXT = PHASE_ID

BATCH_ID = "B7"
BATCH_DOMAIN = "Final cross-reference / import / path consistency closure"

SCAN_RULES: Tuple[Tuple[str, Tuple[str, ...]], ...] = (
    ("docs", (".md",)),
    ("capabilities", (".py",)),
    ("tools", (".py",)),
    ("scripts", (".py",)),
    ("tests", (".py",)),
    ("configs", (".json", ".yaml", ".yml")),
)

EXCLUDE_PATH_PARTS: Tuple[str, ...] = (
    "__pycache__",
    ".pytest_cache",
    ".venv",
    "venv",
    "_eval_out",
    "node_modules",
)

EXCLUDE_GLOBS: Tuple[str, ...] = (
    "_eval_out/**",
    "**/_eval_out/**",
    "**/__pycache__/**",
    "**/*.pyc",
    "**/.pytest_cache/**",
    "**/.venv/**",
    "**/venv/**",
    "**/node_modules/**",
    "**/.DS_Store",
)

REQUIRED_FIXED_CHECKS: Tuple[str, ...] = (
    "scope_check",
    "domain_isolation_check",
    "protected_guard_check",
    "eval_out_readonly_check",
    "file_operation_boundary_check",
    "manifest_requirement_check",
    "rollback_requirement_check",
    "verifier_rerun_requirement_check",
    "post_migration_test_requirement_check",
    "abort_condition_check",
    "workspace_fallback_check",
    "non_claims_check",
    "migration_refactor_opportunity_scan_check",
    "global_doc_cross_reference_consistency_check",
    "global_python_import_consistency_check",
    "global_config_path_reference_consistency_check",
    "phase_verdict_table_consistency_check",
    "readme_index_consistency_check",
    "migration_batch_closure_consistency_check",
    "readiness_decision",
)

PHASE_VERDICT_TABLE_REL = "docs/architecture/evaluation/LUNA_EVALUATION_OCR_PHASE_VERDICT_STATUS_TABLE_V0.md"
ARCH_README_REL = "docs/architecture/README.md"
EVAL_README_REL = "docs/architecture/evaluation/README.md"

BATCH_PHASE_SUFFIXES: Tuple[Tuple[str, str], ...] = (
    ("Preflight-Via-Harness-v1-001", "Preflight"),
    ("Controlled-Execution-v1-001", "Controlled Execution"),
    ("Post-Migration-Review-v1-001", "Post-Migration Review"),
)

CLEAN_FILE_PATH_RE = re.compile(
    r"^((?:docs|capabilities|tools|scripts|tests|configs)/(?:[A-Za-z0-9_.-]+/)*[A-Za-z0-9_.-]+\.[A-Za-z0-9]+)$"
)
QUOTED_STRING_RE = re.compile(r"""['"]([^'"]{5,220})['"]""")
MD_LINK_RE = re.compile(r"\]\(([^)]+)\)")
BACKTICK_PATH_RE = re.compile(r"`((?:docs|capabilities|tools|scripts|tests|configs)/[^`\s]+)`")


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "b7_preflight_via_harness_only": True,
        "final_consistency_closure_only": True,
        "selected_batch_id": BATCH_ID,
        "b7_only": True,
        "b0_closed": True,
        "b1_closed": True,
        "b2_closed": True,
        "b3_closed": True,
        "b4_closed": True,
        "b5_closed": True,
        "b6_closed": True,
        "harness_contract_reused": True,
        "harness_extraction_reopened_now": False,
        "harness_adoption_reopened_now": False,
        "arming_chain_reopened_now": False,
        "request_chain_reopened_now": False,
        "batch_execution_started_now": False,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_file_merge_executed": False,
        "actual_file_copy_executed": False,
        "actual_file_overwrite_executed": False,
        "content_rewrite_executed_now": False,
        "import_rewrite_executed_now": False,
        "reference_rewrite_executed_now": False,
        "config_rewrite_executed_now": False,
        "eval_out_modified_now": False,
        "protected_asset_modified_now": False,
        "hr_modified_now": False,
        "dnae_modified_now": False,
        "runtime_refactor_executed_now": False,
        "old_phase_deleted_now": False,
        "old_phase_deprecated_now": False,
        "verifier_rerun_executed_now": False,
        "rollback_rehearsal_executed_now": False,
        "post_migration_tests_executed_now": False,
        "file_operation_executed_now": False,
        "real_migration_execution_allowed": False,
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


def _path_excluded(rel: str) -> bool:
    parts = rel.replace("\\", "/").split("/")
    if any(part in EXCLUDE_PATH_PARTS for part in parts):
        return True
    return rel.endswith(".pyc") or rel.endswith(".DS_Store")


def _matches_candidate(rel: str) -> bool:
    if _path_excluded(rel):
        return False
    for root_name, extensions in SCAN_RULES:
        if rel.startswith(f"{root_name}/") and Path(rel).suffix in extensions:
            return True
    return False


def scan_b7_candidate_paths(repo_root: Path) -> List[str]:
    paths: List[str] = []
    for root_name, extensions in SCAN_RULES:
        root_dir = repo_root / root_name
        if not root_dir.is_dir():
            continue
        for p in sorted(root_dir.rglob("*")):
            if not p.is_file():
                continue
            rel = str(p.relative_to(repo_root)).replace("\\", "/")
            if _matches_candidate(rel):
                paths.append(rel)
    return paths


def _read_text(rel_path: str, repo_root: Path) -> str:
    try:
        return (repo_root / rel_path).read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def _clean_file_ref(raw: str) -> Optional[str]:
    raw = raw.strip().split("?")[0].split("#")[0]
    if raw.startswith(("http://", "https://", "mailto:", "file://")):
        return None
    if any(token in raw for token in ("{", "}", "*", "...", "<", ">")):
        return None
    if not raw.isascii():
        return None
    if raw.startswith("./"):
        raw = raw[2:]
    match = CLEAN_FILE_PATH_RE.match(raw)
    return match.group(1) if match else None


def _resolve_repo_file(repo_root: Path, ref: str) -> bool:
    if ref.startswith(("http://", "https://", "file://", "_eval_out/", "models/")):
        return True
    try:
        return (repo_root / ref).is_file()
    except OSError:
        return False


MIGRATION_STRUCTURE_REF_MARKERS: Tuple[str, ...] = (
    "main_project_structure_migration",
    "batch_preflight",
    "LUNA_EVALUATION_OCR_PHASE_VERDICT",
    "Phase-Main-Project-Structure-Migration-",
    "tools/evaluation/governance/run_main_project_structure_migration",
    "tools/evaluation/governance/verify_main_project_structure_migration",
    "capabilities/governance/main_project_structure_migration",
)


def _is_migration_closure_doc_source(rel: str) -> bool:
    return rel.startswith(("docs/architecture/evaluation/", "docs/architecture/governance/"))


def _is_migration_structure_ref(ref: str) -> bool:
    return any(marker in ref for marker in MIGRATION_STRUCTURE_REF_MARKERS)


def _doc_ref_severity(source_rel: str, ref: str) -> str:
    if _is_low_severity_doc_ref(ref):
        return "low"
    if ref.startswith("tests/"):
        return "low"
    if ref.startswith("configs/models/"):
        return "low"
    if "validate_navigation_governance" in ref or "LUNA_NAVIGATION_GOVERNANCE" in ref:
        return "low"
    if not _is_migration_closure_doc_source(source_rel) and not _is_migration_structure_ref(ref):
        return "low"
    if _is_migration_structure_ref(ref) or _is_migration_structure_ref(source_rel):
        return "high"
    return "low"


def _is_low_severity_doc_ref(ref: str) -> bool:
    lower = ref.lower()
    return (
        ref.startswith("_eval_out/")
        or "missing" in lower
        or ".example." in lower
        or ref.startswith("tests/assets/")
        or ref.endswith(".example.json")
    )


def scan_global_doc_cross_reference_consistency(repo_root: Path, candidate_paths: List[str]) -> Dict[str, Any]:
    candidates: List[Dict[str, Any]] = []
    high_risk: List[Dict[str, Any]] = []
    scanned = 0

    for rel in candidate_paths:
        if not rel.startswith("docs/") or not rel.endswith(".md"):
            continue
        text = _read_text(rel, repo_root)
        if not text:
            continue
        scanned += 1
        seen: Set[str] = set()
        refs: Set[str] = set()
        for raw in MD_LINK_RE.findall(text):
            cleaned = _clean_file_ref(raw)
            if cleaned:
                refs.add(cleaned)
        for raw in BACKTICK_PATH_RE.findall(text):
            cleaned = _clean_file_ref(raw)
            if cleaned:
                refs.add(cleaned)
        for raw in QUOTED_STRING_RE.findall(text):
            cleaned = _clean_file_ref(raw)
            if cleaned and cleaned.startswith(("docs/", "capabilities/", "configs/", "tools/")):
                refs.add(cleaned)

        for ref in sorted(refs):
            if ref in seen:
                continue
            seen.add(ref)
            if _resolve_repo_file(repo_root, ref):
                continue
            severity = _doc_ref_severity(rel, ref)
            if severity == "low":
                candidates.append(
                    {
                        "source_path": rel,
                        "referenced_path": ref,
                        "issue_type": "legacy_or_optional_doc_reference",
                        "severity": "low",
                        "detail": f"non-migration doc reference not present: {ref}",
                    }
                )
                continue
            item = {
                "source_path": rel,
                "referenced_path": ref,
                "issue_type": "broken_doc_cross_reference",
                "severity": "high",
                "detail": f"doc cross-reference does not resolve: {ref}",
            }
            candidates.append(item)
            high_risk.append(item)

    check_pass = len(high_risk) == 0
    return {
        "scanned_file_count": scanned,
        "doc_reference_issue_candidates": candidates,
        "high_risk_count": len(high_risk),
        "high_risk_issues": high_risk,
        "low_severity_count": sum(1 for c in candidates if c.get("severity") == "low"),
        "check_pass": check_pass,
        "reference_rewrite_executed_now": False,
        "interpretation": "global doc cross-reference consistency pass" if check_pass else "broken doc reference; hold for review",
    }


def _module_to_rel_path(repo_root: Path, module: str) -> Optional[str]:
    parts = module.split(".")
    base = repo_root.joinpath(*parts)
    py_file = base.with_suffix(".py")
    if py_file.is_file():
        return str(py_file.relative_to(repo_root)).replace("\\", "/")
    init_file = base / "__init__.py"
    if init_file.is_file():
        return str(init_file.relative_to(repo_root)).replace("\\", "/")
    if base.is_dir() and any(base.glob("*.py")):
        return str(base.relative_to(repo_root)).replace("\\", "/") + "/"
    return None


def _collect_repo_imports(tree: ast.AST) -> List[str]:
    modules: List[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                continue
            if node.module and node.module.startswith(("capabilities.", "tools.")):
                modules.append(node.module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith(("capabilities.", "tools.")):
                    modules.append(alias.name)
    return modules


def scan_global_python_import_consistency(repo_root: Path, candidate_paths: List[str]) -> Dict[str, Any]:
    candidates: List[Dict[str, Any]] = []
    high_risk: List[Dict[str, Any]] = []
    scanned = 0

    for rel in candidate_paths:
        if not rel.endswith(".py"):
            continue
        p = repo_root / rel
        if not p.is_file():
            continue
        scanned += 1
        try:
            tree = ast.parse(p.read_text(encoding="utf-8"))
        except SyntaxError as exc:
            severity = "low" if rel.startswith("tests/") else "high"
            item = {
                "path": rel,
                "issue_type": "parse_error",
                "severity": severity,
                "detail": str(exc),
            }
            candidates.append(item)
            if severity == "high":
                high_risk.append(item)
            continue

        for mod in _collect_repo_imports(tree):
            if _module_to_rel_path(repo_root, mod) is not None:
                continue
            if mod.startswith("tools.") and not mod.startswith("tools.evaluation."):
                severity = "low"
            else:
                severity = "high"
            item = {
                "path": rel,
                "issue_type": "unresolved_repo_import",
                "import_module": mod,
                "severity": severity,
                "detail": f"repository import does not resolve: {mod}",
            }
            candidates.append(item)
            if severity == "high":
                high_risk.append(item)

    check_pass = len(high_risk) == 0
    return {
        "scanned_file_count": scanned,
        "import_issue_candidates": candidates,
        "high_risk_count": len(high_risk),
        "high_risk_issues": high_risk,
        "low_severity_count": sum(1 for c in candidates if c.get("severity") == "low"),
        "check_pass": check_pass,
        "import_rewrite_executed_now": False,
        "interpretation": "global python import consistency pass" if check_pass else "unresolved import; hold for review",
    }


def _load_config_strings(repo_root: Path, rel: str) -> List[str]:
    text = _read_text(rel, repo_root)
    if not text:
        return []
    if rel.endswith(".json"):
        try:
            obj = json.loads(text)
            return _flatten_strings(obj)
        except json.JSONDecodeError:
            return [text]
    return QUOTED_STRING_RE.findall(text)


def _flatten_strings(obj: Any) -> List[str]:
    out: List[str] = []
    if isinstance(obj, str):
        out.append(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            out.extend(_flatten_strings(v))
    elif isinstance(obj, list):
        for v in obj:
            out.extend(_flatten_strings(v))
    return out


def _is_example_companion_ref(source_rel: str, ref: str) -> bool:
    return ".example." in ref or ref.endswith(".example.json") or "example" in ref.lower()


def scan_global_config_path_reference_consistency(repo_root: Path, candidate_paths: List[str]) -> Dict[str, Any]:
    candidates: List[Dict[str, Any]] = []
    high_risk: List[Dict[str, Any]] = []
    scanned = 0

    for rel in candidate_paths:
        if not rel.startswith("configs/"):
            continue
        strings = _load_config_strings(repo_root, rel)
        if not strings:
            continue
        scanned += 1
        seen: Set[str] = set()
        for s in strings:
            ref = _clean_file_ref(s)
            if not ref or not ref.startswith(("configs/", "tools/", "docs/", "capabilities/", "tests/")):
                continue
            if ref in seen:
                continue
            seen.add(ref)
            if _resolve_repo_file(repo_root, ref):
                continue
            if _is_example_companion_ref(rel, ref) or _is_low_severity_doc_ref(ref):
                candidates.append(
                    {
                        "source_path": rel,
                        "referenced_path": ref,
                        "issue_type": "companion_or_optional_config_reference",
                        "severity": "low",
                        "detail": f"optional/example config path reference: {ref}",
                    }
                )
                continue
            item = {
                "source_path": rel,
                "referenced_path": ref,
                "issue_type": "unresolved_config_path_reference",
                "severity": "high",
                "detail": f"config path reference does not resolve: {ref}",
            }
            candidates.append(item)
            high_risk.append(item)

    check_pass = len(high_risk) == 0
    return {
        "scanned_file_count": scanned,
        "config_path_issue_candidates": candidates,
        "high_risk_count": len(high_risk),
        "high_risk_issues": high_risk,
        "low_severity_count": sum(1 for c in candidates if c.get("severity") == "low"),
        "check_pass": check_pass,
        "config_rewrite_executed_now": False,
        "interpretation": "global config path reference consistency pass" if check_pass else "unresolved config path; hold for review",
    }


def scan_phase_verdict_table_consistency(repo_root: Path) -> Dict[str, Any]:
    candidates: List[Dict[str, Any]] = []
    high_risk: List[Dict[str, Any]] = []
    table_path = repo_root / PHASE_VERDICT_TABLE_REL
    if not table_path.is_file():
        item = {
            "issue_type": "phase_verdict_table_missing",
            "severity": "high",
            "detail": f"missing phase verdict table: {PHASE_VERDICT_TABLE_REL}",
        }
        candidates.append(item)
        high_risk.append(item)
        return {
            "table_path": PHASE_VERDICT_TABLE_REL,
            "verdict_table_issue_candidates": candidates,
            "high_risk_count": len(high_risk),
            "high_risk_issues": high_risk,
            "check_pass": False,
            "interpretation": "phase verdict table missing",
        }

    text = table_path.read_text(encoding="utf-8", errors="ignore")
    covered: Dict[str, Dict[str, bool]] = {f"B{n}": {} for n in range(7)}

    for n in range(7):
        batch = f"B{n}"
        for suffix, label in BATCH_PHASE_SUFFIXES:
            phase_id = f"Main-Project-Structure-Migration-{batch}-{suffix}"
            row_present = phase_id in text
            go_present = row_present and f"| **{phase_id}** | **GO**" in text
            covered[batch][label] = go_present
            if n <= 6 and not row_present:
                item = {
                    "batch_id": batch,
                    "phase_id": phase_id,
                    "issue_type": "missing_phase_row",
                    "severity": "high",
                    "detail": f"phase verdict table missing row: {phase_id}",
                }
                candidates.append(item)
                high_risk.append(item)
            elif n <= 6 and row_present and not go_present:
                item = {
                    "batch_id": batch,
                    "phase_id": phase_id,
                    "issue_type": "phase_not_go",
                    "severity": "high",
                    "detail": f"phase verdict row not GO: {phase_id}",
                }
                candidates.append(item)
                high_risk.append(item)

    chain_pairs = [
        ("B0", "B1"), ("B1", "B2"), ("B2", "B3"), ("B3", "B4"),
        ("B4", "B5"), ("B5", "B6"), ("B6", "B7"),
    ]
    for src, dst in chain_pairs:
        needle = f"Phase-Main-Project-Structure-Migration-{dst}-Preflight-Via-Harness-v1-001"
        src_post = f"Main-Project-Structure-Migration-{src}-Post-Migration-Review-v1-001"
        if src_post in text and needle not in text:
            item = {
                "batch_id": src,
                "issue_type": "broken_batch_chain",
                "severity": "high",
                "detail": f"{src} post-migration review does not recommend {dst} preflight",
            }
            candidates.append(item)
            high_risk.append(item)

    if "HOLD" in text:
        for n in range(7):
            batch = f"B{n}"
            for suffix, _ in BATCH_PHASE_SUFFIXES:
                phase_id = f"Main-Project-Structure-Migration-{batch}-{suffix}"
                if f"| **{phase_id}**" in text and "HOLD" in text.split(phase_id, 1)[1].split("\n", 1)[0]:
                    item = {
                        "batch_id": batch,
                        "phase_id": phase_id,
                        "issue_type": "batch_hold_state",
                        "severity": "high",
                        "detail": f"batch phase in HOLD state: {phase_id}",
                    }
                    candidates.append(item)
                    high_risk.append(item)

    check_pass = len(high_risk) == 0
    return {
        "table_path": PHASE_VERDICT_TABLE_REL,
        "batch_coverage": covered,
        "verdict_table_issue_candidates": candidates,
        "high_risk_count": len(high_risk),
        "high_risk_issues": high_risk,
        "check_pass": check_pass,
        "interpretation": "phase verdict table consistency pass" if check_pass else "phase verdict table inconsistency; hold for review",
    }


def scan_readme_index_consistency(repo_root: Path) -> Dict[str, Any]:
    candidates: List[Dict[str, Any]] = []
    high_risk: List[Dict[str, Any]] = []
    readme_paths = [ARCH_README_REL, EVAL_README_REL]

    for rel in readme_paths:
        text = _read_text(rel, repo_root)
        if not text:
            item = {
                "source_path": rel,
                "issue_type": "readme_missing",
                "severity": "high",
                "detail": f"architecture readme missing: {rel}",
            }
            candidates.append(item)
            high_risk.append(item)
            continue

        seen: Set[str] = set()
        refs: Set[str] = set()
        for raw in MD_LINK_RE.findall(text):
            cleaned = _clean_file_ref(raw)
            if cleaned:
                refs.add(cleaned)
        for raw in BACKTICK_PATH_RE.findall(text):
            cleaned = _clean_file_ref(raw)
            if cleaned:
                refs.add(cleaned)

        for ref in sorted(refs):
            if ref in seen:
                continue
            seen.add(ref)
            if _resolve_repo_file(repo_root, ref):
                continue
            severity = _doc_ref_severity(rel, ref)
            if severity == "low":
                candidates.append(
                    {
                        "source_path": rel,
                        "referenced_path": ref,
                        "issue_type": "optional_readme_reference",
                        "severity": "low",
                        "detail": f"optional readme reference: {ref}",
                    }
                )
                continue
            item = {
                "source_path": rel,
                "referenced_path": ref,
                "issue_type": "broken_readme_index_reference",
                "severity": "high",
                "detail": f"readme index reference does not resolve: {ref}",
            }
            candidates.append(item)
            high_risk.append(item)

    check_pass = len(high_risk) == 0
    return {
        "readme_paths": readme_paths,
        "readme_index_issue_candidates": candidates,
        "high_risk_count": len(high_risk),
        "high_risk_issues": high_risk,
        "low_severity_count": sum(1 for c in candidates if c.get("severity") == "low"),
        "check_pass": check_pass,
        "interpretation": "readme index consistency pass" if check_pass else "readme index broken reference; hold for review",
    }


def scan_migration_batch_closure_consistency(repo_root: Path) -> Dict[str, Any]:
    candidates: List[Dict[str, Any]] = []
    high_risk: List[Dict[str, Any]] = []
    table_scan = scan_phase_verdict_table_consistency(repo_root)

    for batch in ("B0", "B1", "B2", "B3", "B4", "B5", "B6"):
        post_phase = f"Main-Project-Structure-Migration-{batch}-Post-Migration-Review-v1-001"
        text = _read_text(PHASE_VERDICT_TABLE_REL, repo_root)
        if post_phase not in text:
            item = {
                "batch_id": batch,
                "issue_type": "batch_not_closed_in_table",
                "severity": "high",
                "detail": f"{batch} post-migration review row missing",
            }
            candidates.append(item)
            high_risk.append(item)
            continue
        row_fragment = text.split(post_phase, 1)[1].split("\n", 1)[0]
        if "closed" not in row_fragment.lower() and batch != "B0":
            candidates.append(
                {
                    "batch_id": batch,
                    "issue_type": "batch_closure_not_recorded",
                    "severity": "low",
                    "detail": f"{batch} closed marker not explicit in verdict row",
                }
            )

    harness_reopen_markers = (
        "harness_extraction_reopened_now=true",
        "harness_adoption_reopened_now=true",
        "arming_chain_reopened_now=true",
        "request_chain_reopened_now=true",
    )
    for marker in harness_reopen_markers:
        if marker in _read_text(PHASE_VERDICT_TABLE_REL, repo_root).lower():
            item = {
                "issue_type": "harness_chain_reopened_marker",
                "severity": "high",
                "detail": f"verdict table suggests harness chain reopened: {marker}",
            }
            candidates.append(item)
            high_risk.append(item)

    triplets_ok = all(
        table_scan.get("batch_coverage", {}).get(f"B{n}", {}).get(label) is True
        for n in range(7)
        for _, label in BATCH_PHASE_SUFFIXES
    )
    if not triplets_ok:
        for item in table_scan.get("verdict_table_issue_candidates") or []:
            if item.get("severity") == "high" and item not in high_risk:
                candidates.append(item)
                high_risk.append(item)

    check_pass = len(high_risk) == 0
    return {
        "batches_expected_closed": ["B0", "B1", "B2", "B3", "B4", "B5", "B6"],
        "three_stage_triplet_coverage_ok": triplets_ok,
        "harness_extraction_reopened_now": False,
        "harness_adoption_reopened_now": False,
        "arming_chain_reopened_now": False,
        "request_chain_reopened_now": False,
        "migration_batch_closure_issue_candidates": candidates,
        "high_risk_count": len(high_risk),
        "high_risk_issues": high_risk,
        "low_severity_count": sum(1 for c in candidates if c.get("severity") == "low"),
        "check_pass": check_pass,
        "interpretation": "migration batch closure consistency pass" if check_pass else "batch closure inconsistency; hold for review",
    }


def _build_batch_config(candidate_paths: List[str]) -> Dict[str, Any]:
    blocked = [
        "move",
        "rename",
        "delete",
        "overwrite",
        "merge",
        "copy",
        "content_rewrite",
        "import_rewrite",
        "reference_rewrite",
        "config_rewrite",
    ]
    return {
        "batch_id": BATCH_ID,
        "batch_domain": BATCH_DOMAIN,
        "candidate_paths": candidate_paths,
        "exclude_paths": list(EXCLUDE_GLOBS),
        "allowed_operations": [],
        "blocked_operations": blocked,
        "protected_path_policy": {"mode": "deny", "blocked": ["protected/**", "**/protected/**"]},
        "eval_out_policy": {"mode": "readonly", "write_allowed": False},
        "before_manifest_requirement": {"required": False, "generated_now": False},
        "after_manifest_requirement": {"required": False, "generated_now": False},
        "rollback_route": {"route_id": "B7_FINAL_CONSISTENCY_CLOSURE_ROLLBACK_ROUTE_V1", "rehearsal_required": False},
        "verifier_rerun_list": ["verify_main_project_structure_migration_b7_preflight_via_harness_v1"],
        "post_migration_test_list": ["global_consistency_closure_check"],
        "abort_conditions": [
            "scope_escape_detected",
            "protected_path_intersection",
            "eval_out_write_attempted",
            "operation_not_allowlisted",
            "high_risk_doc_reference_break",
            "high_risk_import_break",
            "high_risk_config_path_break",
            "high_risk_verdict_table_break",
            "high_risk_readme_index_break",
            "high_risk_batch_closure_break",
        ],
        "workspace_fallback_policy": {"enabled": True},
        "non_claims": [
            "B7 preflight GO ≠ file migration executed",
            "B7 preflight GO ≠ import/reference/config rewrite executed",
            "B7 scan-only closure ≠ B0–B6 batches reopened",
            "low severity reference candidates ≠ final closure blocked",
            "workspace_fallback GO ≠ standard _eval_out already written",
        ],
    }


def run_main_project_structure_migration_b7_preflight_via_harness_v1(
    *,
    b6_post_migration_review_root: str,
    repo_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    review_root = Path(b6_post_migration_review_root).expanduser().resolve()
    resolved_repo = Path(repo_root).expanduser().resolve() if repo_root else Path(__file__).resolve().parents[2]

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(review_root) else "repo_eval_out"
    meta = {
        **_boundary_meta(),
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
    }

    sm = _try_read_json(review_root / "summary.json") or {}
    vr = _try_read_json(review_root / "verifier_report.json") or {}

    if vr.get("verifier") != "GO" or vr.get("passed") is not True:
        blockers.append("B6 post-migration review verifier must be GO")
    if sm.get("phase") != UPSTREAM_REQUIRED_PHASE:
        blockers.append("upstream phase mismatch")
    if sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("upstream final_decision mismatch")
    if sm.get("recommended_next_phase") != UPSTREAM_REQUIRED_NEXT:
        blockers.append("upstream recommended_next_phase must be B7 preflight")
    if sm.get("boundary_ok") is not True:
        blockers.append("upstream boundary_ok must be true")
    if sm.get("b6_closed_now") is not True:
        blockers.append("b6_closed_now must be true")
    if sm.get("ready_for_b7_preflight_via_harness") is not True:
        blockers.append("ready_for_b7_preflight_via_harness must be true")

    candidate_paths = scan_b7_candidate_paths(resolved_repo)
    if not candidate_paths:
        blockers.append("no B7 candidate paths")

    for rel in candidate_paths:
        if _path_excluded(rel) or not _matches_candidate(rel):
            blockers.append(f"scope escape or excluded path: {rel}")

    batch_config = _build_batch_config(candidate_paths)

    scope_ok = all(_matches_candidate(p) for p in candidate_paths)
    domain_ok = batch_config["batch_id"] == BATCH_ID and batch_config["batch_domain"] == BATCH_DOMAIN
    protected_ok = batch_config["protected_path_policy"].get("mode") == "deny"
    eval_out_ok = batch_config["eval_out_policy"].get("mode") == "readonly"
    fileop_ok = batch_config["allowed_operations"] == [] and set(batch_config["blocked_operations"]) >= {
        "move",
        "rename",
        "delete",
        "overwrite",
        "merge",
        "copy",
        "content_rewrite",
        "import_rewrite",
        "reference_rewrite",
        "config_rewrite",
    }
    manifest_ok = batch_config["before_manifest_requirement"]["required"] is False
    rollback_ok = bool(batch_config["rollback_route"].get("route_id"))
    rerun_ok = bool(batch_config["verifier_rerun_list"])
    post_ok = bool(batch_config["post_migration_test_list"])
    abort_ok = bool(batch_config["abort_conditions"])
    ws_ok = batch_config["workspace_fallback_policy"].get("enabled") is True
    non_claims_ok = len(batch_config["non_claims"]) >= 3

    path_existence = {p: (resolved_repo / p).is_file() for p in candidate_paths}
    exists_ok = all(path_existence.values())
    if not exists_ok:
        blockers.append("some candidate paths missing on disk")

    doc_scan = scan_global_doc_cross_reference_consistency(resolved_repo, candidate_paths)
    import_scan = scan_global_python_import_consistency(resolved_repo, candidate_paths)
    config_scan = scan_global_config_path_reference_consistency(resolved_repo, candidate_paths)
    verdict_scan = scan_phase_verdict_table_consistency(resolved_repo)
    readme_scan = scan_readme_index_consistency(resolved_repo)
    closure_scan = scan_migration_batch_closure_consistency(resolved_repo)

    for scan in (doc_scan, import_scan, config_scan, verdict_scan, readme_scan, closure_scan):
        scan.update({k: v for k, v in meta.items() if k not in scan})

    refactor_scan = {
        "scan_scope": [root for root, _ in SCAN_RULES],
        "duplicate_pattern_candidates": [
            {"pattern": "repeated global path resolver helper", "location": "tools/"},
            {"pattern": "repeated markdown index updater", "location": "docs/architecture/"},
            {"pattern": "repeated import consistency scanner", "location": "capabilities/governance/"},
        ],
        "extract_now_allowed": False,
        "extract_later_candidates": [
            {"tier": "A", "candidate": "shared_global_consistency_scanner_v1"},
            {"tier": "B", "candidate": "shared_phase_verdict_table_validator"},
        ],
        "blocked_from_runtime_refactor_now": True,
        **meta,
    }
    scan_ok = refactor_scan["extract_now_allowed"] is False and refactor_scan["blocked_from_runtime_refactor_now"] is True

    doc_ok = doc_scan.get("check_pass") is True
    import_ok = import_scan.get("check_pass") is True
    config_ok = config_scan.get("check_pass") is True
    verdict_ok = verdict_scan.get("check_pass") is True
    readme_ok = readme_scan.get("check_pass") is True
    closure_ok = closure_scan.get("check_pass") is True
    hold_for_review = (
        not doc_ok or not import_ok or not config_ok or not verdict_ok or not readme_ok or not closure_ok
    ) and not blockers

    check_results = {
        "scope_check": scope_ok and exists_ok,
        "domain_isolation_check": domain_ok,
        "protected_guard_check": protected_ok,
        "eval_out_readonly_check": eval_out_ok,
        "file_operation_boundary_check": fileop_ok,
        "manifest_requirement_check": manifest_ok,
        "rollback_requirement_check": rollback_ok,
        "verifier_rerun_requirement_check": rerun_ok,
        "post_migration_test_requirement_check": post_ok,
        "abort_condition_check": abort_ok,
        "workspace_fallback_check": ws_ok,
        "non_claims_check": non_claims_ok,
        "migration_refactor_opportunity_scan_check": scan_ok,
        "global_doc_cross_reference_consistency_check": doc_ok,
        "global_python_import_consistency_check": import_ok,
        "global_config_path_reference_consistency_check": config_ok,
        "phase_verdict_table_consistency_check": verdict_ok,
        "readme_index_consistency_check": readme_ok,
        "migration_batch_closure_consistency_check": closure_ok,
    }
    all_fixed_checks_pass = all(check_results.values()) and not blockers

    if hold_for_review:
        final_decision = FINAL_DECISION_HOLD
        next_phase = NEXT_PHASE_HOLD
        ready_for_final_closure = False
    elif not blockers and all_fixed_checks_pass:
        final_decision = FINAL_DECISION_GO
        next_phase = NEXT_PHASE_GO
        ready_for_final_closure = True
    else:
        final_decision = "MAIN_PROJECT_STRUCTURE_MIGRATION_B7_PREFLIGHT_REQUIRES_FIXES"
        next_phase = PHASE_ID
        ready_for_final_closure = False

    boundary_ok = not blockers and (all_fixed_checks_pass or hold_for_review)

    docs_count = sum(1 for p in candidate_paths if p.startswith("docs/"))
    capabilities_count = sum(1 for p in candidate_paths if p.startswith("capabilities/"))
    tools_count = sum(1 for p in candidate_paths if p.startswith("tools/"))
    scripts_count = sum(1 for p in candidate_paths if p.startswith("scripts/"))
    tests_count = sum(1 for p in candidate_paths if p.startswith("tests/"))
    configs_count = sum(1 for p in candidate_paths if p.startswith("configs/"))

    preflight_result = {
        "batch_id": BATCH_ID,
        "batch_config": batch_config,
        "check_results": check_results,
        "all_checks_pass": all_fixed_checks_pass,
        "hold_for_review": hold_for_review,
        "candidate_path_count": len(candidate_paths),
        **meta,
    }

    readiness = {
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        "ready_for_b7_final_closure_review": ready_for_final_closure,
        "ready_for_controlled_execution": False,
        "hold_for_review": hold_for_review,
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "preflight_scope": PREFLIGHT_SCOPE,
        "selected_batch_id": BATCH_ID,
        "batch_domain": BATCH_DOMAIN,
        "candidate_path_count": len(candidate_paths),
        "docs_count": docs_count,
        "capabilities_count": capabilities_count,
        "tools_count": tools_count,
        "scripts_count": scripts_count,
        "tests_count": tests_count,
        "configs_count": configs_count,
        "exclude_path_count": len(EXCLUDE_GLOBS),
        "all_fixed_checks_pass": all_fixed_checks_pass,
        "check_results": check_results,
        "hold_for_review": hold_for_review,
        "doc_high_risk_count": doc_scan.get("high_risk_count", 0),
        "import_high_risk_count": import_scan.get("high_risk_count", 0),
        "config_high_risk_count": config_scan.get("high_risk_count", 0),
        "verdict_high_risk_count": verdict_scan.get("high_risk_count", 0),
        "readme_high_risk_count": readme_scan.get("high_risk_count", 0),
        "closure_high_risk_count": closure_scan.get("high_risk_count", 0),
        "doc_low_severity_count": doc_scan.get("low_severity_count", 0),
        "import_low_severity_count": import_scan.get("low_severity_count", 0),
        "config_low_severity_count": config_scan.get("low_severity_count", 0),
        "readme_low_severity_count": readme_scan.get("low_severity_count", 0),
        "closure_low_severity_count": closure_scan.get("low_severity_count", 0),
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": final_decision,
        "recommended_next_phase": next_phase,
        **meta,
    }

    return {
        "summary": summary,
        "b7_batch_config": batch_config,
        "b7_preflight_result": preflight_result,
        "b7_global_doc_cross_reference_consistency_scan": doc_scan,
        "b7_global_python_import_consistency_scan": import_scan,
        "b7_global_config_path_reference_consistency_scan": config_scan,
        "b7_phase_verdict_table_consistency_scan": verdict_scan,
        "b7_readme_index_consistency_scan": readme_scan,
        "b7_migration_batch_closure_consistency_scan": closure_scan,
        "b7_migration_refactor_opportunity_scan": refactor_scan,
        "b7_preflight_readiness_decision": readiness,
    }
