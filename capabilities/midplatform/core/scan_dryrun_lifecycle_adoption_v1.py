# -*- coding: utf-8 -*-
"""Phase-DryRun-Lifecycle-Adoption-Scanner-v1-001 — read-only adoption scan."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.core.dryrun_lifecycle_template_v1 import (
    PHASE_TEMPLATE_ID,
    write_json_file,
)

PHASE_ID = "Phase-DryRun-Lifecycle-Adoption-Scanner-v1-001"
SCOPE = "dryrun_lifecycle_adoption_scan_read_only"
FINAL_DECISION_READY = "DRYRUN_LIFECYCLE_ADOPTION_SCAN_READY_FOR_REVIEW"
FINAL_DECISION_BLOCKED = "DRYRUN_LIFECYCLE_ADOPTION_SCAN_BLOCKED"

TEMPLATE_REL_PATH = "capabilities/midplatform/core/dryrun_lifecycle_template_v1.py"
SCANNER_REL_PATH = "capabilities/midplatform/core/scan_dryrun_lifecycle_adoption_v1.py"

SCANNED_ROOTS: Tuple[str, ...] = (
    "capabilities/midplatform",
    "capabilities/field_understanding",
    "capabilities/governance",
)

DEFAULT_OUTPUT_ROOT = _REPO_ROOT / "_tmp_eval_out" / "dryrun_lifecycle_adoption_scan_v1_smoke_v0"
OUTPUT_FILENAME = "dryrun_lifecycle_adoption_scan_v1.json"

TEMPLATE_IMPORT_MARKERS: Tuple[str, ...] = (
    "dryrun_lifecycle_template_v1",
    "from capabilities.midplatform.core.dryrun_lifecycle_template_v1",
)

# Sealed GO modules — Full lifecycle, no retrofit.
FROZEN_FULL_NO_RETROFIT_DIRS: Tuple[str, ...] = (
    "capabilities/midplatform/provider_runtime_governance",
    "capabilities/field_understanding/dryrun",
    "capabilities/field_understanding/spatial_evidence_provider_admission",
    "capabilities/field_understanding/slam_adapter_contract",
    "capabilities/field_understanding/slam_interface",
)

# Sealed GO — Compressed reference implementation, no retrofit.
FROZEN_COMPRESSED_NO_RETROFIT_DIRS: Tuple[str, ...] = (
    "capabilities/midplatform/provider_manager_runtime_skeleton",
)

CONTROLLED_SKELETON_MARKER = "_controlled_skeleton_implementation_"

KEEP_FULL_OR_CUSTOM_PATTERNS: Tuple[str, ...] = (
    "owner_approval",
    "authorization",
    "issuance",
    "record_approval",
    "grant_owner",
    "grant_request",
    "grant_record",
    "repair_",
    "issue_review",
    "yolo_depth",
    "real_model",
    "controlled_real",
    "real_dependency",
    "real_rollback",
    "execution_authorization",
    "controlled_batch_execution",
    "limited_runtime_trial",
    "recovery_execution",
    "rollback_rehearsal",
    "functional_slice_dryrun",
    "module_level_controlled_dryrun",
    "self_work_core_capability_dryrun",
)

EXCLUDE_DRYRUN_LEG_SUFFIXES: Tuple[str, ...] = (
    "_dryrun_and_review_v1.py",
    "_dryrun_repair_v1.py",
    "_dryrun_issue_review_v1.py",
    "_dryrun_planning_v1.py",
    "_dryrun_evaluators_v1.py",
    "_dryrun_items_v1.py",
    "_dryrun_lineage_v1.py",
    "_dryrun_core_v1.py",
)

RUNNER_PREFIX = "run_"
VERIFY_AND_REVIEW_PREFIX = "verify_and_review_"


def _rel(path: Path) -> str:
    try:
        return str(path.relative_to(_REPO_ROOT))
    except ValueError:
        return str(path)


def _path_matches_any(rel_path: str, patterns: Sequence[str]) -> bool:
    lowered = rel_path.lower()
    return any(pattern.lower() in lowered for pattern in patterns)


def _is_excluded_dryrun_leg(path: Path) -> bool:
    name = path.name
    if name.startswith(RUNNER_PREFIX):
        return True
    if name.startswith(VERIFY_AND_REVIEW_PREFIX):
        return True
    return any(name.endswith(suffix) for suffix in EXCLUDE_DRYRUN_LEG_SUFFIXES)


def _imports_template(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    return any(marker in text for marker in TEMPLATE_IMPORT_MARKERS)



def _is_post_dryrun_review_file(name: str) -> bool:
    if name.endswith("_dryrun_and_review_v1.py"):
        return False
    if name.endswith("_post_dryrun_review_v1.py"):
        return True
    return name.startswith("review_") and name.endswith("_post_dryrun_v1.py")


def _find_dryrun_partner(review_path: Path) -> Optional[Path]:
    stem = review_path.stem
    directory = review_path.parent
    candidates: List[Path] = []

    if stem.endswith("_post_dryrun_review_v1"):
        base = stem[: -len("_post_dryrun_review_v1")]
        candidates.append(directory / f"{base}_dryrun_v1.py")
        if base.startswith("review_"):
            middle = base[len("review_") :]
            candidates.append(directory / f"verify_{middle}_dryrun_v1.py")

    if stem.startswith("review_") and stem.endswith("_post_dryrun_v1"):
        middle = stem[len("review_") : -len("_post_dryrun_v1")]
        candidates.append(directory / f"verify_{middle}_dryrun_v1.py")

    for candidate in candidates:
        if candidate.is_file() and not _is_excluded_dryrun_leg(candidate):
            return candidate
    return None


def _iter_py_files(root: Path) -> List[Path]:
    if not root.is_dir():
        return []
    return sorted(p for p in root.rglob("*.py") if p.is_file())


def _detect_full_split_pairs(scan_roots: Sequence[Path]) -> List[Dict[str, Any]]:
    pairs: List[Dict[str, Any]] = []
    seen: Set[Tuple[str, str]] = set()

    for root in scan_roots:
        for review_path in _iter_py_files(root):
            if not _is_post_dryrun_review_file(review_path.name):
                continue
            dryrun_path = _find_dryrun_partner(review_path)
            if dryrun_path is None:
                continue
            key = (_rel(dryrun_path), _rel(review_path))
            if key in seen:
                continue
            seen.add(key)
            pairs.append(
                {
                    "dryrun_file": key[0],
                    "review_file": key[1],
                    "directory": _rel(review_path.parent),
                    "dryrun_imports_template": _imports_template(dryrun_path),
                    "review_imports_template": _imports_template(review_path),
                }
            )
    return pairs


def _detect_compressed_files(scan_roots: Sequence[Path]) -> List[Dict[str, Any]]:
    found: List[Dict[str, Any]] = []
    for root in scan_roots:
        for path in _iter_py_files(root):
            if not path.name.startswith(VERIFY_AND_REVIEW_PREFIX):
                continue
            if not path.name.endswith(".py"):
                continue
            found.append(
                {
                    "file": _rel(path),
                    "directory": _rel(path.parent),
                    "imports_template": _imports_template(path),
                }
            )
    return found


def _detect_matrix_files(scan_roots: Sequence[Path]) -> List[Dict[str, Any]]:
    found: List[Dict[str, Any]] = []
    for root in scan_roots:
        for path in _iter_py_files(root):
            if not path.name.endswith("_dryrun_and_review_v1.py"):
                continue
            found.append(
                {
                    "file": _rel(path),
                    "directory": _rel(path.parent),
                    "imports_template": _imports_template(path),
                }
            )
    return found


def _classify_pair(pair: Dict[str, Any]) -> str:
    directory = pair["directory"]
    dryrun_file = pair["dryrun_file"]

    if _path_matches_any(dryrun_file, KEEP_FULL_OR_CUSTOM_PATTERNS):
        return "keep_full_or_custom"
    if _path_matches_any(pair["review_file"], KEEP_FULL_OR_CUSTOM_PATTERNS):
        return "keep_full_or_custom"
    if CONTROLLED_SKELETON_MARKER in dryrun_file:
        return "controlled_skeleton_merge_on_touch"
    if any(directory == d or directory.startswith(d + "/") for d in FROZEN_FULL_NO_RETROFIT_DIRS):
        return "frozen_full_no_retrofit"
    return "unknown_needs_review"


def _classify_compressed(entry: Dict[str, Any]) -> str:
    directory = entry["directory"]
    if any(directory == d or directory.startswith(d + "/") for d in FROZEN_COMPRESSED_NO_RETROFIT_DIRS):
        return "compressed_template_adopted"
    if entry["imports_template"]:
        return "compressed_template_adopted"
    return "unknown_needs_review"


def _classify_matrix(entry: Dict[str, Any]) -> str:
    if _path_matches_any(entry["file"], KEEP_FULL_OR_CUSTOM_PATTERNS):
        return "keep_full_or_custom"
    if entry["imports_template"]:
        return "matrix_touch_to_align"
    return "matrix_touch_to_align"


def _detect_go_artifacts() -> List[Dict[str, Any]]:
    artifacts: List[Dict[str, Any]] = []
    eval_root = _REPO_ROOT / "_tmp_eval_out"
    if not eval_root.is_dir():
        return artifacts

    for path in sorted(eval_root.rglob("*.json")):
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if not isinstance(doc, dict):
            continue
        decision = doc.get("final_decision")
        if not isinstance(decision, str):
            continue
        if decision.endswith("_POST_DRYRUN_REVIEW_GO") or decision.endswith("_HANDOFF_GO"):
            artifacts.append(
                {
                    "artifact": _rel(path),
                    "final_decision": decision,
                    "phase_id": doc.get("phase_id"),
                }
            )
    return artifacts


def scan_dryrun_lifecycle_adoption_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
) -> Dict[str, Any]:
    scan_roots = [(_REPO_ROOT / rel).resolve() for rel in SCANNED_ROOTS]
    template_path = (_REPO_ROOT / TEMPLATE_REL_PATH).resolve()
    template_present = template_path.is_file()

    full_split_pairs = _detect_full_split_pairs(scan_roots)
    compressed_files = _detect_compressed_files(scan_roots)
    matrix_files = _detect_matrix_files(scan_roots)
    go_artifacts = _detect_go_artifacts()

    categories: Dict[str, List[Any]] = {
        "frozen_full_no_retrofit": [],
        "compressed_template_adopted": [],
        "matrix_touch_to_align": [],
        "controlled_skeleton_merge_on_touch": [],
        "keep_full_or_custom": [],
        "unknown_needs_review": [],
    }

    for pair in full_split_pairs:
        category = _classify_pair(pair)
        categories[category].append({**pair, "adoption_action": _adoption_action(category)})

    for entry in compressed_files:
        category = _classify_compressed(entry)
        categories[category].append({**entry, "adoption_action": _adoption_action(category)})

    for entry in matrix_files:
        category = _classify_matrix(entry)
        categories[category].append({**entry, "adoption_action": _adoption_action(category)})

    template_consumers = sorted(
        {
            item["file"]
            for item in compressed_files + matrix_files
            if item.get("imports_template")
        }
        | {
            pair["dryrun_file"]
            for pair in full_split_pairs
            if pair.get("dryrun_imports_template")
        }
        | {
            pair["review_file"]
            for pair in full_split_pairs
            if pair.get("review_imports_template")
        }
    )

    frozen_dirs_hit = [
        d
        for d in FROZEN_FULL_NO_RETROFIT_DIRS
        if any(p["directory"] == d or p["directory"].startswith(d + "/") for p in full_split_pairs)
    ]
    keep_full_hits = [p for p in full_split_pairs if _classify_pair(p) == "keep_full_or_custom"]
    controlled_hits = [
        p for p in full_split_pairs if _classify_pair(p) == "controlled_skeleton_merge_on_touch"
    ]

    known_keep_full_patterns_applied = len(keep_full_hits) >= 1
    known_no_retrofit_patterns_applied = len(frozen_dirs_hit) >= len(FROZEN_FULL_NO_RETROFIT_DIRS)

    scan_ok = (
        template_present
        and len(full_split_pairs) >= 1
        and len(compressed_files) >= 1
        and len(matrix_files) >= 1
        and known_keep_full_patterns_applied
        and known_no_retrofit_patterns_applied
    )

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    out_path = out_root / OUTPUT_FILENAME

    report: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "Dry-run Lifecycle Adoption Scan",
        "scope": SCOPE,
        "lifecycle_template_id": PHASE_TEMPLATE_ID,
        "scanner_file": SCANNER_REL_PATH,
        "scan_ok": scan_ok,
        "scanned_roots": list(SCANNED_ROOTS),
        "template_file_present": template_present,
        "template_file": TEMPLATE_REL_PATH,
        "full_split_pairs_detected": len(full_split_pairs),
        "compressed_files_detected": len(compressed_files),
        "matrix_files_detected": len(matrix_files),
        "template_consumers_detected": len(template_consumers),
        "known_keep_full_patterns_applied": known_keep_full_patterns_applied,
        "known_no_retrofit_patterns_applied": known_no_retrofit_patterns_applied,
        "frozen_full_dirs_hit": frozen_dirs_hit,
        "frozen_compressed_dirs": list(FROZEN_COMPRESSED_NO_RETROFIT_DIRS),
        "keep_full_or_custom_pattern_count": len(KEEP_FULL_OR_CUSTOM_PATTERNS),
        "go_artifacts_detected": len(go_artifacts),
        "adoption_policy": {
            "planning_only_candidate_only": "compressed_default",
            "matrix_binding_selection": "matrix_default",
            "high_risk_execution_repair_authorization": "keep_full_or_custom",
            "sealed_go_history": "no_retrofit",
        },
        "categories": categories,
        "category_counts": {key: len(value) for key, value in categories.items()},
        "full_split_pairs": full_split_pairs,
        "compressed_files": compressed_files,
        "matrix_files": matrix_files,
        "template_consumers": template_consumers,
        "go_artifacts_sample": go_artifacts[:20],
        "adoption_summary": {
            "frozen_full_no_retrofit": len(categories["frozen_full_no_retrofit"]),
            "compressed_template_adopted": len(categories["compressed_template_adopted"]),
            "matrix_touch_to_align": len(categories["matrix_touch_to_align"]),
            "controlled_skeleton_merge_on_touch": len(
                categories["controlled_skeleton_merge_on_touch"]
            ),
            "keep_full_or_custom": len(categories["keep_full_or_custom"]),
            "unknown_needs_review": len(categories["unknown_needs_review"]),
            "matrix_without_template_import": sum(
                1 for item in matrix_files if not item["imports_template"]
            ),
            "full_split_without_template_import": sum(
                1
                for pair in full_split_pairs
                if not pair["dryrun_imports_template"] and not pair["review_imports_template"]
            ),
        },
        "boundaries": {
            "no_module_modification": True,
            "no_full_module_rewrite": True,
            "no_controlled_skeleton_merge_execution": True,
            "no_real_runtime_touch": True,
            "scan_classify_report_only": True,
        },
        "final_decision": FINAL_DECISION_READY if scan_ok else FINAL_DECISION_BLOCKED,
        "output_file": str(out_path),
    }

    if write_file:
        write_json_file(out_path, report)

    return report


def _adoption_action(category: str) -> str:
    return {
        "frozen_full_no_retrofit": "no_retrofit",
        "compressed_template_adopted": "reference_implementation",
        "matrix_touch_to_align": "align_template_on_touch",
        "controlled_skeleton_merge_on_touch": "merge_on_touch",
        "keep_full_or_custom": "keep_full_or_custom",
        "unknown_needs_review": "manual_review",
    }.get(category, "manual_review")


def main() -> int:
    try:
        report = scan_dryrun_lifecycle_adoption_v1()
    except ValueError as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 1

    print(
        json.dumps(
            {
                "output_file": report.get("output_file"),
                "scan_ok": report["scan_ok"],
                "scanned_roots": report["scanned_roots"],
                "template_file_present": report["template_file_present"],
                "full_split_pairs_detected": report["full_split_pairs_detected"],
                "compressed_files_detected": report["compressed_files_detected"],
                "matrix_files_detected": report["matrix_files_detected"],
                "known_keep_full_patterns_applied": report["known_keep_full_patterns_applied"],
                "known_no_retrofit_patterns_applied": report[
                    "known_no_retrofit_patterns_applied"
                ],
                "category_counts": report["category_counts"],
                "final_decision": report["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if report["final_decision"] == FINAL_DECISION_READY else 1


if __name__ == "__main__":
    raise SystemExit(main())
