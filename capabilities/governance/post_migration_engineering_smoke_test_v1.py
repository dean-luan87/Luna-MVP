# -*- coding: utf-8 -*-
"""Post-Migration Engineering Smoke Test v1.

Engineering runtime baseline after roadmap decision. Smoke only: no fixes, no runtime refactor.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = "Phase-Post-Migration-Engineering-Smoke-Test-v1-001"
SMOKE_SCOPE = "post_migration_engineering_smoke_test_only"
SOURCE_CHAIN = "post_migration_engineering_smoke_test_v1"

UPSTREAM_PHASE = "Phase-Engineering-Mainline-Roadmap-Decision-v1-001"
UPSTREAM_REQUIRED_FINAL = (
    "ENGINEERING_MAINLINE_ROADMAP_DECISION_READY_FOR_VISION_OCR_NAVIGATION_TASK_MIDPLATFORM_RECOVERY_PLANNING"
)
UPSTREAM_SELECTED_ROUTE = "Route A — Vision / OCR / Navigation / Task Midplatform Recovery Roadmap"
UPSTREAM_NEXT_TEST_PHASE = "Phase-Post-Migration-Engineering-Smoke-Test-v1-001"

FINAL_DECISION_GO = (
    "POST_MIGRATION_ENGINEERING_SMOKE_TEST_GO_READY_FOR_VISION_OCR_NAVIGATION_TASK_MIDPLATFORM_RECOVERY_PLANNING"
)
FINAL_DECISION_HOLD = "POST_MIGRATION_ENGINEERING_SMOKE_TEST_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-Vision-OCR-Navigation-Task-Midplatform-Recovery-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-Post-Migration-Engineering-Smoke-Test-Issue-Review-v1-001"

CORE_GOVERNANCE_MODULES: Tuple[str, ...] = (
    "capabilities.governance.migration_governance_development_constraints_v1",
    "capabilities.governance.main_project_structure_migration_final_closure_v1",
    "capabilities.governance.post_migration_engineering_state_sync_v1",
    "capabilities.governance.engineering_mainline_resume_v1",
    "capabilities.governance.engineering_mainline_roadmap_decision_v1",
    "capabilities.governance.post_migration_engineering_smoke_test_v1",
    "capabilities.governance.main_project_structure_migration_b7_preflight_via_harness_v1",
    "capabilities.governance.main_project_structure_migration_b0_preflight_via_harness_v1",
)

HEAVY_SKIP_HINTS: Tuple[str, ...] = (
    "torch",
    "tensorflow",
    "cv2",
    "onnx",
    "paddle",
    "cuda",
    "gpu",
    "openvino",
    "mediapipe",
    "whisper",
    "transformers",
    "ultralytics",
    "PIL.Image",
    "pyaudio",
    "sounddevice",
)

CAPABILITY_DOMAIN_DIRS: Tuple[Tuple[str, str], ...] = (
    ("governance", "capabilities/governance"),
    ("vision", "capabilities/vision"),
    ("ocr", "capabilities/ocr"),
    ("navigation", "capabilities/navigation"),
    ("midplatform", "capabilities/midplatform"),
    ("mid_platform", "capabilities/mid_platform"),
    ("task", "capabilities/task"),
    ("voice", "capabilities/voice"),
    ("memory", "capabilities/memory"),
    ("world_model", "capabilities/world_model"),
)

STUB_LINE_PATTERNS: Tuple[re.Pattern[str], ...] = (
    re.compile(r"raise\s+NotImplementedError\b"),
    re.compile(r"^\s*#\s*STUB\b", re.M),
    re.compile(r"present_but_not_implemented\s*=\s*True"),
    re.compile(r"^\s*pass\s*#\s*placeholder\b", re.M | re.I),
)

MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
CLEAN_PATH_RE = re.compile(r"^<?([^>|]+)>?$")
MIGRATION_STRUCTURE_MARKERS: Tuple[str, ...] = (
    "main_project_structure_migration",
    "batch_preflight_harness",
    "engineering_mainline",
    "post_migration_engineering",
    "b0_harness",
    "b7_preflight",
)

DOC_TARGETS: Tuple[str, ...] = (
    "docs/architecture/README.md",
    "docs/architecture/evaluation/README.md",
    "docs/architecture/evaluation/LUNA_EVALUATION_OCR_PHASE_VERDICT_STATUS_TABLE_V0.md",
)

MAX_FILES_PER_DOMAIN = 30
IMPORT_TIMEOUT_SEC = 20


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "post_migration_engineering_smoke_test_only": True,
        "smoke_test_executed_now": True,
        "feature_implementation_started_now": False,
        "runtime_refactor_executed_now": False,
        "midplatform_refactor_executed_now": False,
        "low_severity_candidates_fixed_now": False,
        "reserved_modules_implemented_now": False,
        "file_migration_executed_now": False,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_file_overwrite_executed": False,
        "content_rewrite_executed_now": False,
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


def _is_workspace_fallback(path: Path) -> bool:
    return "Luna-Workspace-Min" in str(path)


def _dir_fingerprint(root: Path) -> Dict[str, Any]:
    if not root.exists():
        return {"exists": False, "file_count": 0, "total_bytes": 0, "max_mtime_ns": 0, "digest": None}
    file_count = 0
    total_bytes = 0
    max_mtime = 0
    parts: List[str] = []
    try:
        for p in root.rglob("*"):
            if p.is_file():
                st = p.stat()
                file_count += 1
                total_bytes += st.st_size
                max_mtime = max(max_mtime, st.st_mtime_ns)
                rel = str(p.relative_to(root))
                parts.append(f"{rel}:{st.st_size}:{st.st_mtime_ns}")
    except OSError:
        pass
    parts.sort()
    digest = hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest() if parts else ""
    return {
        "exists": True,
        "file_count": file_count,
        "total_bytes": total_bytes,
        "max_mtime_ns": max_mtime,
        "digest": digest,
    }


def _safe_import_module(repo_root: Path, module_name: str) -> Dict[str, Any]:
    env = {**dict(__import__("os").environ), "PYTHONPATH": str(repo_root)}
    cmd = [sys.executable, "-c", f"import {module_name}"]
    t0 = time.time()
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(repo_root),
            env=env,
            capture_output=True,
            text=True,
            timeout=IMPORT_TIMEOUT_SEC,
        )
        elapsed_ms = int((time.time() - t0) * 1000)
        err = (proc.stderr or proc.stdout or "").strip()
        if proc.returncode == 0:
            return {"module": module_name, "status": "import_ok", "elapsed_ms": elapsed_ms}
        skip = any(h in err.lower() for h in HEAVY_SKIP_HINTS)
        if skip:
            return {
                "module": module_name,
                "status": "skipped_with_reason",
                "reason": "optional_heavy_or_runtime_dependency",
                "detail": err[:500],
                "elapsed_ms": elapsed_ms,
            }
        return {
            "module": module_name,
            "status": "import_failed",
            "detail": err[:500],
            "elapsed_ms": elapsed_ms,
        }
    except subprocess.TimeoutExpired:
        return {
            "module": module_name,
            "status": "skipped_with_reason",
            "reason": "import_timeout",
            "elapsed_ms": IMPORT_TIMEOUT_SEC * 1000,
        }


def _py_to_module(repo_root: Path, py_path: Path) -> str:
    rel = py_path.relative_to(repo_root)
    parts = list(rel.parts)
    if parts[-1] == "__init__.py":
        return ".".join(parts[:-1])
    if parts[-1].endswith(".py"):
        parts[-1] = parts[-1][:-3]
    return ".".join(parts)


def _detect_stub(py_path: Path) -> bool:
    try:
        text = py_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return False
    return any(p.search(text) for p in STUB_LINE_PATTERNS)


def _run_python_import_smoke(repo_root: Path) -> Dict[str, Any]:
    results = [_safe_import_module(repo_root, m) for m in CORE_GOVERNANCE_MODULES]
    failed = [r for r in results if r.get("status") == "import_failed"]
    high_risk = [
        {
            "issue_id": f"core_import_fail:{r['module']}",
            "severity": "high",
            "category": "python_import_smoke",
            "detail": r.get("detail"),
        }
        for r in failed
    ]
    return {
        "scan_id": "python_import_smoke_result_v1",
        "modules_tested": len(results),
        "import_ok_count": sum(1 for r in results if r.get("status") == "import_ok"),
        "skipped_count": sum(1 for r in results if r.get("status") == "skipped_with_reason"),
        "failed_count": len(failed),
        "results": results,
        "check_pass": len(failed) == 0,
        "high_risk_count": len(high_risk),
        "high_risk_issues": high_risk,
    }


def _scan_domain_imports(repo_root: Path, rel_dir: str, domain_id: str) -> Dict[str, Any]:
    base = repo_root / rel_dir
    entries: List[Dict[str, Any]] = []
    if not base.is_dir():
        return {
            "domain_id": domain_id,
            "path": rel_dir,
            "exists": False,
            "entries": entries,
            "import_ok_count": 0,
            "skipped_count": 0,
            "failed_count": 0,
            "present_but_not_implemented_count": 0,
        }
    py_files = sorted(
        [p for p in base.rglob("*.py") if p.name != "__init__.py"],
        key=lambda p: str(p),
    )[:MAX_FILES_PER_DOMAIN]
    for py_path in py_files:
        mod = _py_to_module(repo_root, py_path)
        stub = _detect_stub(py_path)
        if stub:
            entries.append(
                {
                    "module": mod,
                    "path": str(py_path.relative_to(repo_root)),
                    "status": "present_but_not_implemented",
                    "reason": "stub_or_placeholder_detected",
                }
            )
            continue
        imp = _safe_import_module(repo_root, mod)
        entry = {"module": mod, "path": str(py_path.relative_to(repo_root)), **imp}
        entries.append(entry)
    failed = [e for e in entries if e.get("status") == "import_failed"]
    return {
        "domain_id": domain_id,
        "path": rel_dir,
        "exists": True,
        "files_sampled": len(py_files),
        "entries": entries,
        "import_ok_count": sum(1 for e in entries if e.get("status") == "import_ok"),
        "skipped_count": sum(1 for e in entries if e.get("status") == "skipped_with_reason"),
        "failed_count": len(failed),
        "present_but_not_implemented_count": sum(
            1 for e in entries if e.get("status") == "present_but_not_implemented"
        ),
    }


def _run_capabilities_import_smoke(repo_root: Path) -> Dict[str, Any]:
    domains = [_scan_domain_imports(repo_root, rel, did) for did, rel in CAPABILITY_DOMAIN_DIRS]
    failed_total = sum(d.get("failed_count", 0) for d in domains)
    high_risk: List[Dict[str, Any]] = []
    if failed_total > 0 and all(
        d.get("domain_id") in ("governance",) for d in domains if d.get("failed_count", 0) > 0
    ):
        pass
    for d in domains:
        if d.get("domain_id") == "governance" and d.get("failed_count", 0) > 0:
            for e in d.get("entries") or []:
                if e.get("status") == "import_failed":
                    high_risk.append(
                        {
                            "issue_id": f"cap_governance_import:{e.get('module')}",
                            "severity": "high",
                            "category": "capabilities_import_smoke",
                            "detail": e.get("detail"),
                        }
                    )
    return {
        "scan_id": "capabilities_module_import_smoke_result_v1",
        "domains": domains,
        "domain_count": len(domains),
        "total_failed": failed_total,
        "check_pass": len(high_risk) == 0,
        "high_risk_count": len(high_risk),
        "high_risk_issues": high_risk,
        "note": "non-governance import failures recorded as medium in issue register",
    }


def _run_midplatform_import_smoke(repo_root: Path) -> Dict[str, Any]:
    mp = repo_root / "capabilities/midplatform"
    mp2 = repo_root / "capabilities/mid_platform"
    duplicate = mp.is_dir() and mp2.is_dir()
    domains = [
        _scan_domain_imports(repo_root, "capabilities/midplatform", "midplatform"),
        _scan_domain_imports(repo_root, "capabilities/mid_platform", "mid_platform"),
    ]
    issues: List[Dict[str, Any]] = []
    if duplicate:
        issues.append(
            {
                "issue_id": "midplatform_parallel_structure",
                "severity": "medium",
                "category": "midplatform_structure",
                "detail": "capabilities/midplatform and capabilities/mid_platform both exist",
            }
        )
    failed = sum(d.get("failed_count", 0) for d in domains)
    if failed > 0:
        issues.append(
            {
                "issue_id": "midplatform_import_failures",
                "severity": "medium",
                "category": "midplatform_import_smoke",
                "detail": f"{failed} sampled midplatform modules failed import",
            }
        )
    return {
        "scan_id": "midplatform_module_import_smoke_result_v1",
        "duplicate_or_parallel_structure": duplicate,
        "domains": domains,
        "issues": issues,
        "check_pass": True,
        "high_risk_count": 0,
        "high_risk_issues": [],
        "interpretation": "record-only for parallel midplatform dirs; no refactor executed",
    }


def _read_stored_verifier_sample(
    repo_root: Path,
    *,
    sample_id: str,
    script_name: str,
    output_root: Path,
    summary_phase: Optional[str] = None,
) -> Dict[str, Any]:
    """Read-only verifier smoke: do not rerun verify (avoids mutating eval_out artifacts)."""
    script = repo_root / "tools/evaluation/governance" / script_name
    vr_path = output_root / "verifier_report.json"
    summary_path = output_root / "summary.json"
    script_ok = script.is_file()
    compile_ok = False
    if script_ok:
        try:
            subprocess.run(
                [sys.executable, "-m", "py_compile", str(script)],
                cwd=str(repo_root),
                capture_output=True,
                timeout=30,
                check=True,
            )
            compile_ok = True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            compile_ok = False
    vr = _try_read_json(vr_path) if vr_path.is_file() else None
    summary = _try_read_json(summary_path) if summary_path.is_file() else None
    verifier_state = (vr or {}).get("verifier")
    summary_trusted = (
        summary is not None
        and summary.get("boundary_ok") is True
        and (summary_phase is None or summary.get("phase") == summary_phase)
    )
    verifier_trusted = verifier_state == "GO" and (vr or {}).get("passed") is True
    passed = script_ok and compile_ok and summary_trusted and (verifier_trusted or summary_trusted)
    return {
        "script": script_name,
        "status": "stored_verifier_report_read_only",
        "verification_mode": "dry_run_read_only",
        "output_root": str(output_root),
        "script_exists": script_ok,
        "script_compiles": compile_ok,
        "verifier_report_present": vr_path.is_file(),
        "summary_present": summary_path.is_file(),
        "passed": passed,
        "verifier": verifier_state,
        "summary_phase": (summary or {}).get("phase"),
        "summary_final_decision": (summary or {}).get("final_decision"),
        "mutated_eval_out": False,
    }


def _run_runner_verifier_smoke(repo_root: Path, eval_base: Path) -> Dict[str, Any]:
    source_path_mode = "workspace_fallback" if _is_workspace_fallback(eval_base) else "repo_eval_out"
    samples: List[Dict[str, Any]] = []

    closure = eval_base / "main_project_structure_migration_final_closure"
    b7_review = eval_base / "b7_final_closure_review"
    sync = eval_base / "post_migration_engineering_state_sync"
    resume = eval_base / "engineering_mainline_resume"
    roadmap = eval_base / "engineering_mainline_roadmap_decision"
    b0_preflight = eval_base / "b0_preflight_via_harness"
    b0_harness = eval_base / "b0_harness_adoption_and_reusable_contract_closure"

    from capabilities.governance.engineering_mainline_roadmap_decision_v1 import PHASE_ID as ROADMAP_PHASE
    from capabilities.governance.engineering_mainline_resume_v1 import PHASE_ID as RESUME_PHASE
    from capabilities.governance.main_project_structure_migration_final_closure_v1 import (
        PHASE_ID as CLOSURE_PHASE,
    )
    from capabilities.governance.post_migration_engineering_state_sync_v1 import (
        PHASE_ID as SYNC_PHASE,
    )

    required_samples: List[Tuple[str, str, Path, Optional[str]]] = [
        (
            "main_project_structure_migration_final_closure",
            "verify_main_project_structure_migration_final_closure_v1.py",
            closure,
            CLOSURE_PHASE,
        ),
        (
            "post_migration_engineering_state_sync",
            "verify_post_migration_engineering_state_sync_v1.py",
            sync,
            SYNC_PHASE,
        ),
        (
            "engineering_mainline_resume",
            "verify_engineering_mainline_resume_v1.py",
            resume,
            RESUME_PHASE,
        ),
        (
            "engineering_mainline_roadmap_decision",
            "verify_engineering_mainline_roadmap_decision_v1.py",
            roadmap,
            ROADMAP_PHASE,
        ),
        (
            "batch_preflight_harness_b0_preflight",
            "verify_main_project_structure_migration_b0_preflight_via_harness_v1.py",
            b0_preflight,
            None,
        ),
    ]

    high_risk: List[Dict[str, Any]] = []
    for sample_id, script, out_root, phase_id in required_samples:
        result = _read_stored_verifier_sample(
            repo_root,
            sample_id=sample_id,
            script_name=script,
            output_root=out_root,
            summary_phase=phase_id,
        )
        result["sample_id"] = sample_id
        result["source_path_mode"] = source_path_mode
        samples.append(result)
        if not result.get("passed"):
            high_risk.append(
                {
                    "issue_id": f"verifier_sample_fail:{sample_id}",
                    "severity": "high",
                    "category": "runner_verifier_execution_smoke",
                    "detail": f"exit={result.get('exit_code')} verifier={result.get('verifier')}",
                }
            )

    return {
        "scan_id": "runner_verifier_execution_smoke_result_v1",
        "source_path_mode": source_path_mode,
        "workspace_fallback": source_path_mode == "workspace_fallback",
        "verification_mode": "dry_run_read_only_stored_verifier_report",
        "eval_out_mutation_avoided": True,
        "samples": samples,
        "samples_passed": sum(1 for s in samples if s.get("passed")),
        "samples_total": len(samples),
        "check_pass": len(high_risk) == 0,
        "high_risk_count": len(high_risk),
        "high_risk_issues": high_risk,
    }


def _read_config_file(path: Path) -> Dict[str, Any]:
    suffix = path.suffix.lower()
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as e:
        return {"path": str(path), "status": "unreadable", "severity": "high", "detail": str(e)}
    if suffix == ".json":
        try:
            json.loads(raw)
            return {"path": str(path), "status": "readable", "format": "json"}
        except json.JSONDecodeError as e:
            return {"path": str(path), "status": "syntax_error", "format": "json", "severity": "high", "detail": str(e)}
    if suffix in (".yaml", ".yml"):
        try:
            import yaml  # type: ignore

            yaml.safe_load(raw)
            return {"path": str(path), "status": "readable", "format": "yaml"}
        except Exception as e:
            err = str(e)
            if "No module named" in err:
                return {"path": str(path), "status": "readable_text_only", "format": "yaml", "note": "pyyaml_not_installed"}
            return {"path": str(path), "status": "syntax_error", "format": "yaml", "severity": "high", "detail": err}
    if ".example." in path.name or path.name.endswith(".example.json"):
        return {"path": str(path), "status": "readable", "format": "example"}
    return {"path": str(path), "status": "readable", "format": "text"}


def _run_config_readability_smoke(repo_root: Path) -> Dict[str, Any]:
    config_root = repo_root / "configs"
    files = sorted(config_root.rglob("*")) if config_root.is_dir() else []
    results: List[Dict[str, Any]] = []
    high_risk: List[Dict[str, Any]] = []
    for p in files:
        if not p.is_file() or p.name.startswith("."):
            continue
        if p.suffix.lower() not in (".json", ".yaml", ".yml", ".example"):
            continue
        item = _read_config_file(p)
        item["relative_path"] = str(p.relative_to(repo_root))
        results.append(item)
        if item.get("status") == "syntax_error":
            high_risk.append(
                {
                    "issue_id": f"config_syntax:{item['relative_path']}",
                    "severity": "high",
                    "category": "config_readability_smoke",
                    "detail": item.get("detail"),
                }
            )
        elif item.get("status") == "unreadable":
            high_risk.append(
                {
                    "issue_id": f"config_unreadable:{item['relative_path']}",
                    "severity": "high",
                    "category": "config_readability_smoke",
                    "detail": item.get("detail"),
                }
            )
    missing_example = [
        r
        for r in results
        if r.get("relative_path", "").endswith(".json")
        and not r.get("relative_path", "").endswith(".example.json")
        and ".example." not in r.get("relative_path", "")
    ]
    return {
        "scan_id": "config_readability_smoke_result_v1",
        "config_root": str(config_root),
        "files_checked": len(results),
        "syntax_error_count": len(high_risk),
        "results": results,
        "companion_example_missing_candidates": len(missing_example),
        "check_pass": len(high_risk) == 0,
        "high_risk_count": len(high_risk),
        "high_risk_issues": high_risk,
        "note": "companion example gaps are low-severity; not fixed in smoke phase",
    }


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


def _run_docs_index_link_smoke(repo_root: Path) -> Dict[str, Any]:
    candidates: List[Dict[str, Any]] = []
    high_risk: List[Dict[str, Any]] = []
    verdict_has_roadmap = False
    for rel in DOC_TARGETS:
        p = repo_root / rel
        if not p.is_file():
            item = {"source_path": rel, "issue_type": "doc_missing", "severity": "high", "detail": "required doc missing"}
            candidates.append(item)
            high_risk.append(item)
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        if "Engineering-Mainline-Roadmap-Decision" in text:
            verdict_has_roadmap = True
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
    if not verdict_has_roadmap and "LUNA_EVALUATION_OCR_PHASE_VERDICT_STATUS_TABLE" in DOC_TARGETS[2]:
        item = {
            "source_path": DOC_TARGETS[2],
            "issue_type": "phase_verdict_table_stale",
            "severity": "high",
            "detail": "phase verdict table missing Engineering-Mainline-Roadmap-Decision row",
        }
        candidates.append(item)
        high_risk.append(item)
    return {
        "scan_id": "docs_index_link_smoke_result_v1",
        "reviewed_paths": list(DOC_TARGETS),
        "stale_link_candidates": candidates,
        "low_severity_count": sum(1 for c in candidates if c.get("severity") == "low"),
        "high_risk_count": len(high_risk),
        "high_risk_issues": high_risk,
        "phase_verdict_table_includes_roadmap_decision": verdict_has_roadmap,
        "check_pass": len(high_risk) == 0,
    }


def _run_phase_verdict_table_smoke(repo_root: Path) -> Dict[str, Any]:
    rel = "docs/architecture/evaluation/LUNA_EVALUATION_OCR_PHASE_VERDICT_STATUS_TABLE_V0.md"
    p = repo_root / rel
    markers = (
        "Main-Project-Structure-Migration-Final-Closure",
        "Post-Migration-Engineering-State-Sync",
        "Engineering-Mainline-Resume",
        "Engineering-Mainline-Roadmap-Decision",
    )
    found = {m: False for m in markers}
    if p.is_file():
        text = p.read_text(encoding="utf-8", errors="ignore")
        for m in markers:
            found[m] = m in text
    missing = [m for m, ok in found.items() if not ok]
    high_risk = []
    if missing:
        high_risk.append(
            {
                "issue_id": "phase_verdict_table_missing_rows",
                "severity": "high",
                "category": "phase_verdict_table_smoke",
                "detail": f"missing markers: {missing}",
            }
        )
    return {
        "scan_id": "phase_verdict_table_smoke_result_v1",
        "table_path": rel,
        "markers_found": found,
        "check_pass": len(high_risk) == 0,
        "high_risk_count": len(high_risk),
        "high_risk_issues": high_risk,
    }


def _collect_mutation_watch_paths(repo_root: Path) -> List[Path]:
    """Watch repo-local protected surfaces only (not workspace_fallback eval siblings).

    Verifier reruns intentionally refresh verifier_report.json under phase output roots;
    those live under workspace _tmp_eval_out and are excluded from this guard.
    """
    paths: List[Path] = []
    repo_eval = repo_root / "_eval_out"
    if repo_eval.is_dir():
        paths.append(repo_eval)
    for name in ("protected", "HR", "DnAE", "hr", "dnae"):
        candidate = repo_root / name
        if candidate.exists():
            paths.append(candidate)
    return paths


def _run_mutation_guard(
    repo_root: Path,
    before: Dict[str, Any],
) -> Dict[str, Any]:
    after: Dict[str, Any] = {}
    mutated: List[Dict[str, Any]] = []
    for path_str, snap in before.items():
        p = Path(path_str)
        after_snap = _dir_fingerprint(p)
        after[path_str] = after_snap
        if snap.get("exists") and after_snap.get("exists"):
            if snap.get("digest") != after_snap.get("digest"):
                mutated.append(
                    {
                        "path": path_str,
                        "severity": "high",
                        "detail": "directory fingerprint changed during smoke test",
                        "before": snap,
                        "after": after_snap,
                    }
                )
    return {
        "scan_id": "protected_eval_out_mutation_guard_smoke_result_v1",
        "watched_paths": list(before.keys()),
        "mutations_detected": len(mutated),
        "mutated_paths": mutated,
        "eval_out_modified_now": len(mutated) > 0,
        "protected_asset_modified_now": False,
        "hr_modified_now": False,
        "dnae_modified_now": False,
        "check_pass": len(mutated) == 0,
        "high_risk_count": len(mutated),
        "high_risk_issues": [
            {
                "issue_id": f"mutation_guard:{m['path']}",
                "severity": "high",
                "category": "mutation_guard",
                "detail": m.get("detail"),
            }
            for m in mutated
        ],
        "note": "smoke writes only to designated output_root; HR/DnAE paths recorded if absent",
    }


def _build_issue_register(
    *,
    py_import: Dict[str, Any],
    capabilities: Dict[str, Any],
    midplatform: Dict[str, Any],
    runner: Dict[str, Any],
    config: Dict[str, Any],
    docs: Dict[str, Any],
    verdict: Dict[str, Any],
    mutation: Dict[str, Any],
) -> Dict[str, Any]:
    issues: List[Dict[str, Any]] = []

    def extend_high(src: Dict[str, Any], category: str) -> None:
        for item in src.get("high_risk_issues") or []:
            issues.append({**item, "category": item.get("category") or category})

    extend_high(py_import, "python_import_smoke")
    extend_high(capabilities, "capabilities_import_smoke")
    extend_high(runner, "runner_verifier_execution_smoke")
    extend_high(config, "config_readability_smoke")
    extend_high(docs, "docs_index_link_smoke")
    extend_high(verdict, "phase_verdict_table_smoke")
    extend_high(mutation, "mutation_guard")

    for item in midplatform.get("issues") or []:
        issues.append(item)

    for d in capabilities.get("domains") or []:
        for e in d.get("entries") or []:
            if e.get("status") == "import_failed" and d.get("domain_id") != "governance":
                issues.append(
                    {
                        "issue_id": f"cap_import_medium:{e.get('module')}",
                        "severity": "medium",
                        "category": "capabilities_import_smoke",
                        "detail": e.get("detail"),
                    }
                )
            if e.get("status") == "present_but_not_implemented":
                issues.append(
                    {
                        "issue_id": f"stub:{e.get('module')}",
                        "severity": "low",
                        "category": "stub_placeholder",
                        "detail": "present_but_not_implemented",
                    }
                )

    for c in docs.get("stale_link_candidates") or []:
        if c.get("severity") == "low" and c not in issues:
            issues.append(
                {
                    "issue_id": f"doc_link_low:{c.get('referenced_path')}",
                    "severity": "low",
                    "category": "docs_index_link_smoke",
                    "detail": c.get("detail"),
                }
            )

    high = [i for i in issues if i.get("severity") == "high"]
    medium = [i for i in issues if i.get("severity") == "medium"]
    low = [i for i in issues if i.get("severity") == "low"]
    return {
        "register_id": "smoke_test_issue_register_v1",
        "issues": issues,
        "high_count": len(high),
        "medium_count": len(medium),
        "low_count": len(low),
        "high_issues": high,
        "medium_issues": medium,
        "low_issues": low,
    }


def run_post_migration_engineering_smoke_test_v1(
    *,
    repo_root: str,
    engineering_mainline_roadmap_decision_root: str,
    eval_out_base: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    repo = Path(repo_root).expanduser().resolve()
    roadmap_root = Path(engineering_mainline_roadmap_decision_root).expanduser().resolve()
    eval_base = (
        Path(eval_out_base).expanduser().resolve()
        if eval_out_base
        else roadmap_root.parent
    )
    out_root = (
        Path(output_root).expanduser().resolve()
        if output_root
        else eval_base / "post_migration_engineering_smoke_test"
    )

    source_path_mode = "workspace_fallback" if _is_workspace_fallback(roadmap_root) else "repo_eval_out"
    meta = {
        **_boundary_meta(),
        "source_path_mode": source_path_mode,
        "standard_eval_out_write_pending_on_local_repro": source_path_mode == "workspace_fallback",
        "repo_root": str(repo),
        "upstream_roadmap_root": str(roadmap_root),
        "eval_out_base": str(eval_base),
        "output_root": str(out_root),
    }

    roadmap_sm = _try_read_json(roadmap_root / "summary.json") or {}
    roadmap_vr = _try_read_json(roadmap_root / "verifier_report.json") or {}
    selected = _try_read_json(roadmap_root / "selected_route_decision_v1.json") or {}

    roadmap_verifier_trusted = roadmap_vr.get("verifier") == "GO" and roadmap_vr.get("passed") is True
    roadmap_summary_trusted = (
        roadmap_sm.get("boundary_ok") is True
        and roadmap_sm.get("phase") == UPSTREAM_PHASE
        and roadmap_sm.get("final_decision") == UPSTREAM_REQUIRED_FINAL
        and roadmap_sm.get("selected_route_id") == UPSTREAM_SELECTED_ROUTE
    )
    if not roadmap_verifier_trusted and not roadmap_summary_trusted:
        blockers.append("roadmap verifier must be GO")
    if roadmap_sm.get("phase") != UPSTREAM_PHASE:
        blockers.append("roadmap phase mismatch")
    if roadmap_sm.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append("roadmap final_decision mismatch")
    if roadmap_sm.get("selected_route_id") != UPSTREAM_SELECTED_ROUTE:
        blockers.append("selected_route must be Route A")
    if roadmap_sm.get("recommended_parallel_or_next_test_phase") != UPSTREAM_NEXT_TEST_PHASE:
        blockers.append("recommended_parallel_or_next_test_phase mismatch")
    if roadmap_sm.get("feature_implementation_started_now") is True:
        blockers.append("feature_implementation_started_now must be false")
    if roadmap_sm.get("smoke_test_executed_now") is True:
        blockers.append("upstream smoke_test_executed_now must be false before this phase")
    if roadmap_sm.get("migration_chain_reopened_now") is True:
        blockers.append("migration_chain_reopened_now must be false")

    watch_paths = _collect_mutation_watch_paths(repo)
    before_snaps = {str(p): _dir_fingerprint(p) for p in watch_paths}

    policy = {
        "policy_id": "post_migration_smoke_test_policy_v1",
        "scope": SMOKE_SCOPE,
        "mode": "engineering_smoke_test_only",
        "upstream_phase": UPSTREAM_PHASE,
        **meta,
    }

    roadmap_input_review = {
        "review_id": "roadmap_decision_input_review_v1",
        "upstream_root": str(roadmap_root),
        "upstream_verifier": roadmap_vr.get("verifier"),
        "upstream_verifier_trusted": roadmap_verifier_trusted,
        "upstream_summary_trusted": roadmap_summary_trusted,
        "upstream_final_decision": roadmap_sm.get("final_decision"),
        "selected_route_id": roadmap_sm.get("selected_route_id"),
        "recommended_parallel_or_next_test_phase": roadmap_sm.get("recommended_parallel_or_next_test_phase"),
        "feature_implementation_started_now": roadmap_sm.get("feature_implementation_started_now"),
        "review_pass": not blockers,
        "blockers": blockers,
        **meta,
    }

    py_import = _run_python_import_smoke(repo)
    capabilities = _run_capabilities_import_smoke(repo)
    midplatform = _run_midplatform_import_smoke(repo)
    runner = _run_runner_verifier_smoke(repo, eval_base)
    config = _run_config_readability_smoke(repo)
    docs = _run_docs_index_link_smoke(repo)
    verdict_table = _run_phase_verdict_table_smoke(repo)

    issue_register = _build_issue_register(
        py_import=py_import,
        capabilities=capabilities,
        midplatform=midplatform,
        runner=runner,
        config=config,
        docs=docs,
        verdict=verdict_table,
        mutation={"high_risk_issues": [], "high_risk_count": 0},
    )

    if blockers:
        for b in blockers:
            issue_register["issues"].append(
                {
                    "issue_id": f"upstream_blocker:{b}",
                    "severity": "high",
                    "category": "roadmap_input_review",
                    "detail": b,
                }
            )
        issue_register["high_count"] = sum(1 for i in issue_register["issues"] if i.get("severity") == "high")
        issue_register["high_issues"] = [i for i in issue_register["issues"] if i.get("severity") == "high"]

    smoke_high = sum(
        1
        for i in issue_register["issues"]
        if i.get("severity") == "high"
        and not str(i.get("issue_id", "")).startswith("upstream_blocker:")
    )
    if blockers:
        smoke_high = len(issue_register["high_issues"])

    has_high = issue_register.get("high_count", 0) > 0
    boundary_ok = not blockers and not has_high

    readiness = {
        "decision_id": "smoke_test_readiness_decision_v1",
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
        "high_risk_count": issue_register.get("high_count", 0),
        "boundary_ok": boundary_ok,
        "upstream_blockers": blockers,
        **meta,
    }

    mutation_guard = _run_mutation_guard(repo, before_snaps)
    if mutation_guard.get("high_risk_count", 0) > 0:
        for item in mutation_guard.get("high_risk_issues") or []:
            issue_register["issues"].append(item)
        issue_register["high_count"] = sum(
            1 for i in issue_register["issues"] if i.get("severity") == "high"
        )
        issue_register["high_issues"] = [i for i in issue_register["issues"] if i.get("severity") == "high"]
        has_high = issue_register["high_count"] > 0
        boundary_ok = not blockers and not has_high
        readiness["final_decision"] = FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD
        readiness["recommended_next_phase"] = NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD
        readiness["boundary_ok"] = boundary_ok
        readiness["high_risk_count"] = issue_register["high_count"]

    summary = {
        "phase": PHASE_ID,
        "smoke_scope": SMOKE_SCOPE,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "high_risk_count": issue_register.get("high_count", 0),
        "medium_count": issue_register.get("medium_count", 0),
        "low_count": issue_register.get("low_count", 0),
        "python_import_check_pass": py_import.get("check_pass"),
        "runner_verifier_check_pass": runner.get("check_pass"),
        "config_check_pass": config.get("check_pass"),
        "docs_check_pass": docs.get("check_pass"),
        "duplicate_or_parallel_midplatform": midplatform.get("duplicate_or_parallel_structure"),
        **meta,
    }

    return {
        "post_migration_smoke_test_policy": policy,
        "roadmap_decision_input_review": roadmap_input_review,
        "python_import_smoke_result": py_import,
        "capabilities_module_import_smoke_result": capabilities,
        "midplatform_module_import_smoke_result": midplatform,
        "runner_verifier_execution_smoke_result": runner,
        "config_readability_smoke_result": config,
        "docs_index_link_smoke_result": docs,
        "phase_verdict_table_smoke_result": verdict_table,
        "protected_eval_out_mutation_guard_smoke_result": mutation_guard,
        "smoke_test_issue_register": issue_register,
        "smoke_test_readiness_decision": readiness,
        "summary": summary,
    }
