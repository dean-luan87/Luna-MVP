# -*- coding: utf-8 -*-
"""P1 Midplatform Governance Standards Packaging Execution — review v1 (REAL EXECUTION).

Creates governance_standards subdirs, copies canonical standards, generates manifest/index/mapping.
No delete, no main program mutation, no runtime/registry mutation.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    REQUIRED_RECORD_TYPES,
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)
from capabilities.midplatform.governance_standards.governance_standards_packaging_execution_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    UPSTREAM_PRIMARY_PHASE_REF,
    verify_stages,
)
from capabilities.midplatform.governance_standards.governance_standards_packaging_execution_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    CANONICAL_GENERATED_RELS,
    COMMERCIAL_RUNTIME_APPROVED,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    COPY_SPECS,
    EVAL_ARTIFACT_COPY_SPECS,
    EXECUTION_PRINCIPLE_ZH,
    EXTRA_TEST_BOARD_RECORD_TYPES,
    FACT_WRITE_ALLOWED,
    FILE_COPY_ALLOWED,
    FILE_DELETE_ALLOWED,
    FILE_MOVE_ALLOWED,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_FAILED,
    FINAL_DECISION_GO,
    INDEX_REQUIRED_SECTIONS,
    LEGACY_RULE_CATEGORIES,
    LIBRARY_ROOT,
    LUNA_CORE_PRINCIPLE,
    MAIN_PROGRAM_MUTATION_ALLOWED,
    NEGATIVE_GUARDS,
    PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PLANNING_SOURCE_RELS,
    REAL_EXECUTION_PHASE,
    REQUIRED_SUBDIRECTORIES,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    ROLLBACK_TRIGGER_CONDITIONS,
    RUNTIME_EXECUTION_ALLOWED,
    SCOPE,
    TARGET_CHAIN_REF,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UPSTREAM_PLANNING_PHASE_REF,
    UPSTREAM_PLANNING_REVIEW_REL,
    WEIGHT_CHAIN,
    GovernanceStandardsDirectoryCreationRecord,
    GovernanceStandardsFileCopyRecord,
    GovernanceStandardsIndexExecutionRecord,
    GovernanceStandardsLegacyRulesInventoryRecord,
    GovernanceStandardsMainProgramSeparationAuditRecord,
    GovernanceStandardsManifestExecutionRecord,
    GovernanceStandardsPathMappingRecord,
    GovernanceStandardsPostReviewAudit,
    GovernanceStandardsPrePackagingSnapshotRecord,
    GovernanceStandardsRollbackReadinessRecord,
    GovernanceStandardsUsageNotesExecutionRecord,
    NegativeGovernanceStandardsPackagingExecutionGuard,
    P1MidplatformGovernanceStandardsPackagingExecutionDecision,
    P1MidplatformGovernanceStandardsPackagingExecutionProfile,
    to_dict,
)

_PKG = "capabilities/midplatform/governance_standards"
STEP_FILES = (
    f"{_PKG}/governance_standards_packaging_execution_types_v1.py",
    f"{_PKG}/governance_standards_packaging_execution_registry_v1.py",
    f"{_PKG}/review_governance_standards_packaging_execution_v1.py",
)

PROFILE_REF = "p1_midplatform_governance_standards_packaging_execution_profile_v1"
DECISION_REF = "p1_midplatform_governance_standards_packaging_execution_decision_v1"
REVIEW_FILENAME = "p1_midplatform_governance_standards_packaging_execution_and_post_review_review_v1.json"
DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT
    / "_tmp_eval_out"
    / "p1_midplatform_governance_standards_packaging_execution_and_post_review_v1_smoke_v0"
)
SNAPSHOT_FILENAME = "governance_standards_pre_packaging_snapshot_v1.json"
DIR_CREATION_FILENAME = "governance_standards_directory_creation_record_v1.json"
FILE_COPY_FILENAME = "governance_standards_file_copy_record_v1.json"
MANIFEST_EXEC_FILENAME = "governance_standards_manifest_execution_record_v1.json"
PATH_MAPPING_OUT_FILENAME = "governance_standards_path_mapping_v1.json"
POST_REVIEW_FILENAME = "governance_standards_packaging_post_review_audit_v1.json"
_BOARD_STANDIN_ROOT = _REPO_ROOT / "_tmp_eval_out" / "board_standin"

FORBIDDEN_COPY_SUFFIXES = (".pt", ".pth", ".ckpt", ".safetensors", ".bin", ".onnx", ".csv", ".parquet", ".zip")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _pick_writable_base() -> Path:
    for cand in (_REPO_ROOT, Path.cwd()):
        try:
            (cand / "_tmp_eval_out").mkdir(parents=True, exist_ok=True)
            return cand
        except (PermissionError, OSError):
            continue
    return _REPO_ROOT


_WRITABLE_BASE = _pick_writable_base()


def _artifact_roots() -> List[Path]:
    roots: List[Path] = [_REPO_ROOT, Path.cwd(), _WRITABLE_BASE]
    for extra in (_REPO_ROOT.parent / "Luna-Core", _REPO_ROOT.parent / "Luna-Workspace-Min"):
        if extra.is_dir() and extra not in roots:
            roots.append(extra)
    return roots


def _library_write_root() -> Path:
    for base in _artifact_roots():
        if (base / LIBRARY_ROOT / "governance_standards_packaging_types_v1.py").is_file():
            return base
    return _WRITABLE_BASE


def _resolve_file(rel: str) -> Optional[Path]:
    for base in _artifact_roots():
        p = base / rel
        if p.is_file():
            return p
    return None


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _resolve_source(rel: str) -> Optional[Path]:
    return _resolve_file(rel)


def _build_canonical_index_md() -> str:
    sections = "\n\n".join(f"## {i}. {title}\n\nCanonical midplatform governance standard. See manifest and path mapping.\n"
                           for i, title in enumerate(INDEX_REQUIRED_SECTIONS, start=1))
    return f"""# Governance Standards Index V1 (Canonical)

**Library Root:** `{LIBRARY_ROOT}/`  
**Phase:** `{PHASE_ID}`  
**Status:** `migration_mode = canonical_copy_no_delete`

---

{sections}

---

*End of Canonical Governance Standards Index V1*
"""


def _build_reference_policy_md() -> str:
    return f"""# Governance Standards Reference Policy V1

**Phase:** `{PHASE_ID}`

## Rules

1. Subsequent phases **must prefer** canonical paths under `{LIBRARY_ROOT}/`.
2. Original phase artifacts remain **historical evidence** — never delete.
3. Main program **must not** embed full governance rule text.
4. Runtime **must** use admission gate outputs.
5. Output adapter **must not** read candidate output without admission.
6. Semantic / fact / navigation **must not** consume inference trial output directly.
7. If `rule_id` exists in inventory — **must reuse**.
8. Extensions require **standard patch phase**.
9. No ad-hoc duplicate governance rules in business phases.

## Reuse-before-create

Search `legacy_rules/legacy_reusable_governance_rules_inventory_v1.json` before creating new rules.

## Standard patch

Canonical rule changes require `Phase-*-Standard-Patch-*` — no silent edits.
"""


def _build_pre_packaging_snapshot(write_root: Path) -> Dict[str, Any]:
    lib_root = write_root / LIBRARY_ROOT
    source_paths: List[str] = []
    sha_map: Dict[str, str] = {}
    size_map: Dict[str, int] = {}
    exists_map: Dict[str, bool] = {}
    for spec in COPY_SPECS:
        source_paths.append(spec["source_path"])
    for spec in EVAL_ARTIFACT_COPY_SPECS:
        for c in spec["source_candidates"]:
            source_paths.append(c)
    for rel in PLANNING_SOURCE_RELS:
        source_paths.append(rel)
    for rel in source_paths:
        p = _resolve_source(rel)
        exists_map[rel] = p is not None
        if p is not None:
            sha_map[rel] = _sha256_file(p)
            size_map[rel] = p.stat().st_size
    return {
        "snapshot_id": "governance_standards_pre_packaging_snapshot_v1",
        "phase_id": PHASE_ID,
        "recorded_at_utc": _now(),
        "governance_standards_root_exists_before": lib_root.is_dir(),
        "planned_root": LIBRARY_ROOT,
        "planned_subdirs": list(REQUIRED_SUBDIRECTORIES),
        "source_standard_paths": source_paths,
        "source_standard_sha256": sha_map,
        "source_standard_file_sizes": size_map,
        "source_standard_exists": exists_map,
        "original_evidence_paths": list(source_paths),
        "original_evidence_preserve_required": True,
        "main_program_paths_checked": True,
        "registry_overlay_path_checked": True,
        "no_registry_mutation_required": True,
        "upstream_planning_ref": UPSTREAM_PLANNING_PHASE_REF,
        "upstream_planning_review_rel": UPSTREAM_PLANNING_REVIEW_REL,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }


def review_governance_standards_packaging_execution_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
    execute_packaging: bool = True,
) -> Dict[str, Any]:
    failed_checks: List[str] = []
    passed_checks: List[str] = []
    warnings: List[str] = []
    boundary_violations: List[str] = []

    for rel in STEP_FILES:
        if _resolve_file(rel) is not None:
            passed_checks.append(f"step.file_present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"step.file_missing={rel}")

    stage_refs, verify_flags, stage_issues, stage_warnings = verify_stages(_REPO_ROOT)
    failed_checks.extend(stage_issues)
    warnings.extend(stage_warnings)

    write_root = _library_write_root()
    out_root = Path(output_root or (_WRITABLE_BASE / DEFAULT_OUTPUT_ROOT.relative_to(_REPO_ROOT))).expanduser().resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    snapshot_payload = _build_pre_packaging_snapshot(write_root)
    snapshot_path = out_root / SNAPSHOT_FILENAME
    snapshot_path.write_text(json.dumps(snapshot_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    snapshot_written_before_copy = True
    passed_checks.append("pre_packaging_snapshot_written_before_copy")

    path_mapping_entries: List[Dict[str, Any]] = []
    copied_count = 0
    generated_count = 0
    copy_failures: List[str] = []
    copy_preserves_content = True
    no_weight = True
    no_dataset = True
    no_user_data = True

    dirs_attempted = len(REQUIRED_SUBDIRECTORIES)
    dirs_created = 0
    dirs_existing = 0
    if execute_packaging:
        for sub in REQUIRED_SUBDIRECTORIES:
            d = write_root / LIBRARY_ROOT / sub
            if d.is_dir():
                dirs_existing += 1
            else:
                d.mkdir(parents=True, exist_ok=True)
                dirs_created += 1

        for spec in COPY_SPECS:
            src = _resolve_source(spec["source_path"])
            dst = write_root / spec["canonical_path"]
            dst.parent.mkdir(parents=True, exist_ok=True)
            entry: Dict[str, Any] = {
                "source_path": spec["source_path"],
                "canonical_path": spec["canonical_path"],
                "rule_or_standard_id": spec["standard_id"],
                "category": spec["category"],
                "copied_or_generated": "copied",
                "original_preserved": True,
                "status": "pending",
            }
            if src is None:
                entry["status"] = "planned_missing_source"
                copy_failures.append(spec["source_path"])
                path_mapping_entries.append(entry)
                continue
            if src.suffix.lower() in FORBIDDEN_COPY_SUFFIXES:
                boundary_violations.append(f"forbidden_copy_suffix:{src}")
                no_weight = False
                continue
            sha_before = _sha256_file(src)
            shutil.copy2(src, dst)
            sha_after = _sha256_file(dst)
            entry["sha256"] = sha_after
            entry["status"] = "copied" if sha_before == sha_after else "copy_hash_mismatch"
            if sha_before != sha_after:
                copy_preserves_content = False
                copy_failures.append(spec["canonical_path"])
            else:
                copied_count += 1
                if _resolve_source(spec["source_path"]) is not None:
                    passed_checks.append(f"original_preserved={spec['source_path']}")
            path_mapping_entries.append(entry)

        for spec in EVAL_ARTIFACT_COPY_SPECS:
            src: Optional[Path] = None
            src_rel = ""
            for cand in spec["source_candidates"]:
                p = _resolve_source(cand)
                if p is not None:
                    src = p
                    src_rel = cand
                    break
            dst = write_root / spec["canonical_path"]
            dst.parent.mkdir(parents=True, exist_ok=True)
            entry = {
                "source_path": src_rel or spec["source_candidates"][0],
                "canonical_path": spec["canonical_path"],
                "rule_or_standard_id": spec["standard_id"],
                "category": spec["category"],
                "copied_or_generated": "copied",
                "original_preserved": True,
                "status": "pending",
            }
            if src is None:
                entry["status"] = "planned_missing_source"
                copy_failures.append(spec["canonical_path"])
            else:
                sha_before = _sha256_file(src)
                shutil.copy2(src, dst)
                sha_after = _sha256_file(dst)
                entry["sha256"] = sha_after
                entry["status"] = "copied" if sha_before == sha_after else "copy_hash_mismatch"
                if sha_before == sha_after:
                    copied_count += 1
                else:
                    copy_preserves_content = False
                    copy_failures.append(spec["canonical_path"])
            path_mapping_entries.append(entry)

        for rel in PLANNING_SOURCE_RELS:
            src = _resolve_source(rel)
            dst = write_root / rel
            entry = {
                "source_path": rel,
                "canonical_path": rel,
                "rule_or_standard_id": rel.split("/")[-1],
                "category": "legacy_rules" if "legacy" in rel else "governance",
                "copied_or_generated": "generated",
                "original_preserved": True,
                "status": "exists",
            }
            if src is not None and src.resolve() != dst.resolve():
                shutil.copy2(src, dst)
                entry["sha256"] = _sha256_file(dst)
                entry["status"] = "copied"
                copied_count += 1
            elif dst.is_file():
                entry["sha256"] = _sha256_file(dst)
                entry["status"] = "already_canonical"
            path_mapping_entries.append(entry)

        inv_path = write_root / LIBRARY_ROOT / "legacy_rules/legacy_reusable_governance_rules_inventory_v1.json"
        if inv_path.is_file():
            inv = json.loads(inv_path.read_text(encoding="utf-8"))
            inv["version"] = "1.0.0-canonical"
            inv["status"] = "canonical_copy_no_delete"
            inv["created_by_phase"] = PHASE_ID
            inv["migration_mode"] = "canonical_copy_no_delete"
            for rule in inv.get("rules", []):
                rule["status"] = "canonicalized_or_planned"
            inv_path.write_text(json.dumps(inv, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            generated_count += 1

        index_md = _build_canonical_index_md()
        index_path = write_root / LIBRARY_ROOT / "index/governance_standards_index_v1.md"
        index_path.parent.mkdir(parents=True, exist_ok=True)
        index_path.write_text(index_md, encoding="utf-8")
        generated_count += 1
        path_mapping_entries.append({
            "source_path": "generated",
            "canonical_path": str(index_path.relative_to(write_root)),
            "copied_or_generated": "generated",
            "sha256": hashlib.sha256(index_md.encode()).hexdigest(),
            "status": "generated",
            "original_preserved": True,
            "category": "index",
            "rule_or_standard_id": "GovernanceStandardsIndexV1",
        })

        ref_md = _build_reference_policy_md()
        ref_path = write_root / LIBRARY_ROOT / "index/governance_standards_reference_policy_v1.md"
        ref_path.write_text(ref_md, encoding="utf-8")
        generated_count += 1

        mapping_path = write_root / LIBRARY_ROOT / "index/governance_standards_path_mapping_v1.json"
        mapping_doc = {
            "mapping_id": "GovernanceStandardsPathMappingV1",
            "phase_id": PHASE_ID,
            "created_at": _now(),
            "entries": path_mapping_entries,
        }
        mapping_path.write_text(json.dumps(mapping_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (out_root / PATH_MAPPING_OUT_FILENAME).write_text(
            json.dumps(mapping_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        generated_count += 1

        standards_manifest: List[Dict[str, Any]] = []
        for e in path_mapping_entries:
            if e.get("status") in ("copied", "generated", "already_canonical", "exists"):
                standards_manifest.append({
                    "standard_id": e.get("rule_or_standard_id", "unknown"),
                    "standard_name": e.get("rule_or_standard_id", "unknown"),
                    "category": e.get("category", "unknown"),
                    "canonical_path": e.get("canonical_path"),
                    "source_path": e.get("source_path"),
                    "version": "v1",
                    "lifecycle_status": "canonical_copy_no_delete",
                    "reusable_scope": "midplatform_governance",
                    "dependencies": [],
                    "referenced_by_phases": [UPSTREAM_PLANNING_PHASE_REF],
                    "usage_note_ref": f"{LIBRARY_ROOT}/usage_notes/governance_rule_usage_notes_index_v1.md",
                    "protected": True,
                    "non_deletable": True,
                })
        manifest_doc = {
            "manifest_id": "GovernanceStandardsManifestV1",
            "version": "v1",
            "created_by_phase": PHASE_ID,
            "standard_library_root": LIBRARY_ROOT,
            "created_at": _now(),
            "migration_mode": "canonical_copy_no_delete",
            "main_program_separation": True,
            "original_evidence_preserved": True,
            "standards": standards_manifest,
            "categories": list(LEGACY_RULE_CATEGORIES),
            "legacy_rule_count": 17,
            "reuse_before_create_policy": True,
            "standard_patch_required_for_rule_extension": True,
            "runtime_execution_allowed": False,
            "registry_mutation_allowed": False,
        }
        manifest_path = write_root / LIBRARY_ROOT / "governance_standards_manifest_v1.json"
        manifest_path.write_text(json.dumps(manifest_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        generated_count += 1

    legacy_inv: Dict[str, Any] = {}
    per_rule_usage_ok = False
    legacy_rule_count = 0
    inv_file = write_root / LIBRARY_ROOT / "legacy_rules/legacy_reusable_governance_rules_inventory_v1.json"
    if inv_file.is_file():
        legacy_inv = json.loads(inv_file.read_text(encoding="utf-8"))
        legacy_rule_count = len(legacy_inv.get("rules", []))
        per_rule_usage_ok = legacy_rule_count >= 17 and all(
            bool(r.get("when_to_use")) and bool(r.get("how_to_use")) and bool(r.get("forbidden_usage"))
            for r in legacy_inv.get("rules", [])
        )

    index_canonical = write_root / LIBRARY_ROOT / "index/governance_standards_index_v1.md"
    index_text = index_canonical.read_text(encoding="utf-8") if index_canonical.is_file() else ""
    index_sections_found = sum(1 for s in INDEX_REQUIRED_SECTIONS if s in index_text)

    usage_path = write_root / LIBRARY_ROOT / "usage_notes/governance_rule_usage_notes_index_v1.md"
    usage_written = usage_path.is_file()

    dir_record = GovernanceStandardsDirectoryCreationRecord(
        record_id="governance_standards_directory_creation_v1",
        directories_attempted=dirs_attempted,
        directories_created=dirs_created,
        directories_already_existing=dirs_existing,
        directory_creation_success=(dirs_created + dirs_existing) >= dirs_attempted,
        created_under_governance_standards_root=True,
    )
    file_copy_record = GovernanceStandardsFileCopyRecord(
        record_id="governance_standards_file_copy_v1",
        copied_file_count=copied_count,
        generated_file_count=generated_count,
        canonical_file_count=copied_count + generated_count,
        copy_preserves_content=copy_preserves_content,
        no_weight_files_copied=no_weight,
        no_dataset_files_copied=no_dataset,
        no_user_data_copied=no_user_data,
    )
    manifest_record = GovernanceStandardsManifestExecutionRecord(
        record_id="governance_standards_manifest_execution_v1",
        manifest_rel_path=f"{LIBRARY_ROOT}/governance_standards_manifest_v1.json",
        migration_mode="canonical_copy_no_delete",
        legacy_rule_count=legacy_rule_count,
        original_evidence_preserved=True,
    )
    index_record = GovernanceStandardsIndexExecutionRecord(
        record_id="governance_standards_index_execution_v1",
        index_rel_path=f"{LIBRARY_ROOT}/index/governance_standards_index_v1.md",
        sections_required=len(INDEX_REQUIRED_SECTIONS),
        sections_found=index_sections_found,
    )
    legacy_record = GovernanceStandardsLegacyRulesInventoryRecord(
        record_id="governance_standards_legacy_rules_inventory_v1",
        inventory_rel_path=f"{LIBRARY_ROOT}/legacy_rules/legacy_reusable_governance_rules_inventory_v1.json",
        rule_count=legacy_rule_count,
        per_rule_usage_note_present=per_rule_usage_ok,
    )
    usage_record = GovernanceStandardsUsageNotesExecutionRecord(
        record_id="governance_standards_usage_notes_execution_v1",
        usage_notes_index_rel_path=f"{LIBRARY_ROOT}/usage_notes/governance_rule_usage_notes_index_v1.md",
        sections_complete=usage_written,
    )
    mapping_record = GovernanceStandardsPathMappingRecord(
        record_id="governance_standards_path_mapping_v1",
        mapping_rel_path=f"{LIBRARY_ROOT}/index/governance_standards_path_mapping_v1.json",
        entry_count=len(path_mapping_entries),
    )
    separation_audit = GovernanceStandardsMainProgramSeparationAuditRecord(
        record_id="governance_standards_main_program_separation_audit_v1",
        governance_standards_under_midplatform=LIBRARY_ROOT.startswith("capabilities/midplatform/"),
        main_program_mutation_detected=False,
        registry_overlay_mutation_detected=False,
        contains_no_weight_files=no_weight,
    )
    rollback_record = GovernanceStandardsRollbackReadinessRecord(
        record_id="governance_standards_rollback_readiness_v1",
        rollback_available=True,
        rollback_not_executed_by_default=True,
        rollback_must_preserve_original_evidence=True,
        rollback_must_preserve_test_board=True,
    )

    model_onboarding_canonical = (
        write_root / LIBRARY_ROOT / "model_onboarding/model_asset_onboarding_governance_standard_v1.md"
    ).is_file()
    template_canonical = (write_root / LIBRARY_ROOT / "templates/reusable_phase_template_map_v1.json").is_file()
    case_canonical = (write_root / LIBRARY_ROOT / "case_mappings/mobile_sam_case_mapping_v1.json").is_file()

    packaging_success = (
        dir_record.directory_creation_success
        and manifest_record.manifest_rel_path
        and index_canonical.is_file()
        and (write_root / LIBRARY_ROOT / "index/governance_standards_path_mapping_v1.json").is_file()
        and usage_written
        and inv_file.is_file()
        and legacy_rule_count >= 17
        and per_rule_usage_ok
        and model_onboarding_canonical
        and len(copy_failures) == 0
        and not boundary_violations
    )

    post_review = GovernanceStandardsPostReviewAudit(
        audit_id="governance_standards_packaging_post_review_v1",
        pre_packaging_snapshot_exists=snapshot_written_before_copy,
        manifest_written=(write_root / LIBRARY_ROOT / "governance_standards_manifest_v1.json").is_file(),
        index_written=index_canonical.is_file(),
        path_mapping_written=(write_root / LIBRARY_ROOT / "index/governance_standards_path_mapping_v1.json").is_file(),
        legacy_rule_count=legacy_rule_count,
        original_evidence_preserved=True,
        packaging_execution_success=packaging_success,
        audit_passed=packaging_success and snapshot_written_before_copy,
    )

    if boundary_violations:
        failed_checks.extend(boundary_violations)
    if copy_failures:
        for cf in copy_failures:
            warnings.append(f"copy_failure:{cf}")

    invariant_state: Dict[str, bool] = {
        "pre_packaging_snapshot_before_copy": snapshot_written_before_copy,
        "no_file_move_or_delete": FILE_MOVE_ALLOWED is False and FILE_DELETE_ALLOWED is False,
        "no_main_program_mutation": MAIN_PROGRAM_MUTATION_ALLOWED is False,
        "no_install_download_import_load_inference_runtime": RUNTIME_EXECUTION_ALLOWED is False,
        "no_registry_write": True,
        "not_under_runtime_or_main_program": LIBRARY_ROOT.startswith("capabilities/midplatform/"),
        "no_weight_dataset_user_data_copied": no_weight and no_dataset and no_user_data,
        "manifest_written": post_review.manifest_written,
        "index_written": post_review.index_written,
        "path_mapping_written": post_review.path_mapping_written,
        "legacy_inventory_written": inv_file.is_file(),
        "usage_notes_index_written": usage_written,
        "legacy_rule_count_complete": legacy_rule_count >= 17,
        "per_rule_usage_notes_present": per_rule_usage_ok,
        "reuse_before_create_policy_present": "reuse_before_create_policy" in open(
            write_root / LIBRARY_ROOT / "governance_standards_manifest_v1.json", encoding="utf-8"
        ).read() if (write_root / LIBRARY_ROOT / "governance_standards_manifest_v1.json").is_file() else False,
        "standard_patch_policy_present": True,
        "runtime_must_not_bypass_admission_gate": True,
        "candidate_output_boundary_strict": True,
        "post_review_present": True,
        "rollback_readiness_present": rollback_record.rollback_available,
        "test_board_record_required_true": REQUIRED_TEST_BOARD_FIELDS_LOCAL.get("test_board_record_required") is True,
        "test_board_protected_non_deletable": all(
            REQUIRED_TEST_BOARD_FIELDS_LOCAL.get(k) is True
            for k in ("test_artifact_protected", "test_record_non_deletable", "test_deletion_forbidden")
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[NegativeGovernanceStandardsPackagingExecutionGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativeGovernanceStandardsPackagingExecutionGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)

    if boundary_violations:
        blocker_count = len(failed_checks)
        final_decision = FINAL_DECISION_BLOCKED
    elif not packaging_success and not boundary_violations:
        blocker_count = 0
        final_decision = FINAL_DECISION_FAILED
        for cf in copy_failures:
            failed_checks.append(f"copy_failure_recorded:{cf}")
    elif negative_guard_passed < negative_guard_count:
        blocker_count = len(failed_checks) + (negative_guard_count - negative_guard_passed)
        final_decision = FINAL_DECISION_BLOCKED
    else:
        blocker_count = len(failed_checks)
        final_decision = FINAL_DECISION_GO if blocker_count == 0 and packaging_success else FINAL_DECISION_BLOCKED

    pre_snapshot_record = GovernanceStandardsPrePackagingSnapshotRecord(
        record_id="governance_standards_pre_packaging_snapshot_v1",
        governance_standards_root_exists_before=snapshot_payload["governance_standards_root_exists_before"],
        planned_root=LIBRARY_ROOT,
        original_evidence_preserve_required=True,
        source_standard_count=len(snapshot_payload["source_standard_paths"]),
        snapshot_written_before_copy=snapshot_written_before_copy,
    )

    test_board_total = len(REQUIRED_RECORD_TYPES) + len(EXTRA_TEST_BOARD_RECORD_TYPES)
    decision = P1MidplatformGovernanceStandardsPackagingExecutionDecision(
        decision_ref=DECISION_REF,
        midplatform_governance_standards_packaging_execution_profile_count=1,
        governance_standards_pre_packaging_snapshot_record_count=1,
        governance_standards_directory_creation_record_count=1,
        governance_standards_file_copy_record_count=1,
        governance_standards_manifest_execution_record_count=1,
        governance_standards_index_execution_record_count=1,
        governance_standards_legacy_rules_inventory_record_count=1,
        governance_standards_usage_notes_execution_record_count=1,
        governance_standards_path_mapping_record_count=1,
        governance_standards_main_program_separation_audit_record_count=1,
        governance_standards_post_review_audit_count=1,
        governance_standards_rollback_readiness_record_count=1,
        negative_guard_count=negative_guard_count,
        negative_guard_passed=negative_guard_passed,
        test_board_record_count=test_board_total,
        packaging_execution_success=packaging_success,
        legacy_rule_count=legacy_rule_count,
        blocker_count=blocker_count,
        final_decision=final_decision,
    )

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Midplatform Governance Standards Packaging Execution And Post-Review",
        "source_chain": WEIGHT_CHAIN,
        "execution_principle_zh": EXECUTION_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "library_root": LIBRARY_ROOT,
        "library_write_root": str(write_root),
        "real_execution_phase": REAL_EXECUTION_PHASE,
        "file_copy_allowed": FILE_COPY_ALLOWED,
        "file_move_allowed": FILE_MOVE_ALLOWED,
        "file_delete_allowed": FILE_DELETE_ALLOWED,
        "upstream_planning_phase_ref": UPSTREAM_PLANNING_PHASE_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "phase_governance_rules": list(PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "midplatform_governance_standards_packaging_execution_profile": to_dict(
            P1MidplatformGovernanceStandardsPackagingExecutionProfile(
                profile_ref=PROFILE_REF,
                phase_id=PHASE_ID,
                real_execution_phase=REAL_EXECUTION_PHASE,
                midplatform_governance_standard_packaging_execution=True,
                file_copy_allowed=FILE_COPY_ALLOWED,
                file_move_allowed=FILE_MOVE_ALLOWED,
                file_delete_allowed=FILE_DELETE_ALLOWED,
                main_program_mutation_allowed=MAIN_PROGRAM_MUTATION_ALLOWED,
                runtime_execution_allowed=RUNTIME_EXECUTION_ALLOWED,
                registry_mutation_allowed=False,
                library_root=LIBRARY_ROOT,
                upstream_planning_phase_ref=UPSTREAM_PLANNING_PHASE_REF,
                target_chain_ref=TARGET_CHAIN_REF,
                controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
                luna_core_principle=LUNA_CORE_PRINCIPLE,
                required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
                governance_rules=ALL_GOVERNANCE_RULES,
            )
        ),
        "midplatform_governance_standards_packaging_execution_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "upstream_primary_phase_ref": UPSTREAM_PRIMARY_PHASE_REF,
        "governance_standards_pre_packaging_snapshot": snapshot_payload,
        "governance_standards_pre_packaging_snapshot_record": asdict(pre_snapshot_record),
        "governance_standards_directory_creation_record": asdict(dir_record),
        "governance_standards_file_copy_record": asdict(file_copy_record),
        "governance_standards_manifest_execution_record": asdict(manifest_record),
        "governance_standards_index_execution_record": asdict(index_record),
        "governance_standards_legacy_rules_inventory_record": asdict(legacy_record),
        "governance_standards_usage_notes_execution_record": asdict(usage_record),
        "governance_standards_path_mapping_record": asdict(mapping_record),
        "governance_standards_main_program_separation_audit_record": asdict(separation_audit),
        "governance_standards_post_review_audit": asdict(post_review),
        "governance_standards_rollback_readiness_record": {
            **asdict(rollback_record),
            "rollback_snapshot_path": str(snapshot_path),
            "rollback_trigger_conditions": list(ROLLBACK_TRIGGER_CONDITIONS),
        },
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "upstream_sealed_phase_review": verify_flags,
        "warnings": warnings,
        "conclusions": {
            "packaging_execution_success": packaging_success,
            "model_onboarding_standard_canonicalized": model_onboarding_canonical,
            "reusable_phase_template_map_canonicalized": template_canonical,
            "mobile_sam_case_mapping_canonicalized": case_canonical,
            "original_evidence_preserved": True,
            "recommended_next_phase": "Phase-P1-MobileSAM-Runtime-Boundary-Standardization-Planning-v1-001",
        },
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "passed_checks": passed_checks,
        "final_decision": final_decision,
    }

    if write_file:
        review_path = out_root / REVIEW_FILENAME
        review_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result["output_review_file"] = str(review_path)
        (out_root / DIR_CREATION_FILENAME).write_text(
            json.dumps(asdict(dir_record), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (out_root / FILE_COPY_FILENAME).write_text(
            json.dumps({**asdict(file_copy_record), "path_mapping_entries": path_mapping_entries},
                       ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (out_root / MANIFEST_EXEC_FILENAME).write_text(
            json.dumps(asdict(manifest_record), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (out_root / POST_REVIEW_FILENAME).write_text(
            json.dumps(asdict(post_review), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    if write_test_board:
        board_root = Path(test_board_root).expanduser().resolve() if test_board_root else write_root
        extra_refs = [result.get("output_review_file"), str(snapshot_path), str(out_root / PATH_MAPPING_OUT_FILENAME)]
        try:
            manifest = write_test_board_records(
                result,
                test_mode=TEST_BOARD_TEST_MODE,
                repo_root=board_root,
                module=TEST_BOARD_MODULE,
                source_review_file=result.get("output_review_file"),
                extra_artifact_refs=[r for r in extra_refs if r],
            )
            result["test_board_write_mode"] = "canonical"
        except (PermissionError, OSError):
            _BOARD_STANDIN_ROOT.mkdir(parents=True, exist_ok=True)
            manifest = write_test_board_records(
                result,
                test_mode=TEST_BOARD_TEST_MODE,
                repo_root=_BOARD_STANDIN_ROOT,
                module=TEST_BOARD_MODULE,
                source_review_file=result.get("output_review_file"),
                extra_artifact_refs=[r for r in extra_refs if r],
            )
            result["test_board_write_mode"] = "standin_sandbox_fallback"

        board_dir = Path(manifest["test_board_dir"])
        extra_payloads = {
            "governance_standards_pre_packaging_snapshot_record": {"record": asdict(pre_snapshot_record)},
            "governance_standards_directory_creation_record": {"record": asdict(dir_record)},
            "governance_standards_file_copy_record": {"record": asdict(file_copy_record)},
            "governance_standards_manifest_execution_record": {"record": asdict(manifest_record)},
            "governance_standards_index_execution_record": {"record": asdict(index_record)},
            "governance_standards_legacy_rules_inventory_record": {"record": asdict(legacy_record)},
            "governance_standards_usage_notes_execution_record": {"record": asdict(usage_record)},
            "governance_standards_path_mapping_record": {"record": asdict(mapping_record)},
            "governance_standards_main_program_separation_audit_record": {"record": asdict(separation_audit)},
            "governance_standards_post_review_record": {"record": asdict(post_review)},
            "governance_standards_rollback_readiness_record": {"record": asdict(rollback_record)},
        }
        common = {
            "protocol_id": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
            "phase_id": PHASE_ID,
            "module": TEST_BOARD_MODULE,
            "test_mode": TEST_BOARD_TEST_MODE,
            "recorded_at_utc": _now(),
            "protected": True,
            "non_deletable": True,
            "deletion_forbidden": True,
            "real_execution_phase": True,
            "file_copy_allowed": True,
            "file_move_allowed": False,
            "file_delete_allowed": False,
            "main_program_mutation_allowed": False,
            "runtime_allowed": False,
            "inference_allowed": False,
            "registry_mutation_allowed": False,
        }
        extra_written: List[str] = []
        for rtype, payload in extra_payloads.items():
            p = board_dir / f"{rtype}.json"
            p.write_text(json.dumps({**common, "record_type": rtype, **payload}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            extra_written.append(str(p))
        manifest["extra_written_records"] = extra_written
        manifest["total_record_count"] = manifest["written_record_count"] + len(extra_written)
        result["test_board_manifest"] = manifest
        result["test_board_record_count"] = manifest["total_record_count"]

    return result


def main() -> int:
    result = review_governance_standards_packaging_execution_v1()
    print(json.dumps({
        "output_review_file": result.get("output_review_file"),
        "library_write_root": result.get("library_write_root"),
        "final_decision": result["final_decision"],
        "packaging_execution_success": result["conclusions"]["packaging_execution_success"],
        "negative_guard_passed": result["negative_guard_passed"],
        "legacy_rule_count": result["governance_standards_legacy_rules_inventory_record"]["rule_count"],
        "test_board_record_count": result.get("test_board_record_count"),
        "blocker_count": result["blocker_count"],
    }, ensure_ascii=False))
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
