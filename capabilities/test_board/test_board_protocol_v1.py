# -*- coding: utf-8 -*-
"""Test Board Protected Artifact Rule — protocol v1 (global governance asset).

This module fixes a GLOBAL test-governance rule that all later phases must reuse:
every virtual test, real test, dry-run, runtime trial, post-review and closure
review — anything touching a test process or a test conclusion — MUST be written
to the test board and marked protected / non-deletable.

Key distinction (do not conflate):
  _tmp_eval_out = per-run review output (may be a temporary evaluation artifact)
  test_board    = long-term, protected, NON-DELETABLE test evidence layer

The test board is the durable evidence layer; `_tmp_eval_out` is a working
review surface. A phase may write both, but the test board record is the one that
must be preserved.

Required field flags (every later phase must carry these as true):
  test_board_record_required        = true
  test_process_record_required      = true
  test_conclusion_record_required   = true
  test_artifact_protected           = true
  test_record_non_deletable         = true
  test_deletion_forbidden           = true

Each test phase MUST produce at least:
  test_process_record, test_result_summary, test_conclusion_record,
  test_artifact_refs, protected_marker, non_deletable_notice.

Six global governance rules to append to every later phase:
  1. All virtual and real test artifacts must be written to the test board.
  2. Test process records must be preserved.
  3. Test conclusions must be preserved.
  4. Test board artifacts are protected and must not be deleted.
  5. Cleanup scripts must not remove protected test board artifacts.
  6. Any test artifact deletion requires explicit governance approval.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PROTOCOL_ID = "TestBoardProtectedArtifactRuleV1"
PROTOCOL_PHASE_REF = "Phase-Test-Board-Protected-Artifact-Rule-v1-001"
SOURCE_CHAIN = "test_board_protocol_v1"

# Test board root, relative to repo root.
TEST_BOARD_REL_ROOT = "capabilities/test_board"

# --------------------------------------------------------------------------- #
# Required field flags — every later phase must carry these as true.
# --------------------------------------------------------------------------- #
REQUIRED_TEST_BOARD_FIELDS: Dict[str, bool] = {
    "test_board_record_required": True,
    "test_process_record_required": True,
    "test_conclusion_record_required": True,
    "test_artifact_protected": True,
    "test_record_non_deletable": True,
    "test_deletion_forbidden": True,
}

# --------------------------------------------------------------------------- #
# Six global governance rules appended to every later phase.
# --------------------------------------------------------------------------- #
TEST_BOARD_GOVERNANCE_RULES: Tuple[str, ...] = (
    "all_virtual_and_real_test_artifacts_must_be_written_to_the_test_board",
    "test_process_records_must_be_preserved",
    "test_conclusions_must_be_preserved",
    "test_board_artifacts_are_protected_and_must_not_be_deleted",
    "cleanup_scripts_must_not_remove_protected_test_board_artifacts",
    "any_test_artifact_deletion_requires_explicit_governance_approval",
)

# --------------------------------------------------------------------------- #
# Test board modules. A phase routes to exactly one module by id/scope match.
# --------------------------------------------------------------------------- #
TEST_BOARD_MODULES: Tuple[str, ...] = (
    "model_governance",
    "recognition_models",
    "midplatform",
    "runtime_trials",
    "general",
)

# Routing keywords (checked against the lowercased phase_id/scope).
_MODULE_ROUTING: Tuple[Tuple[str, Tuple[str, ...]], ...] = (
    ("runtime_trials", ("runtime-trial", "runtime_trial", "execution-dryrun", "execution_dryrun", "execution-trace", "execution_trace", "streaming")),
    ("recognition_models", ("recognition-model", "recognition_model", "p1-", "p0-", "p1_", "p0_", "model-p1", "download-license", "download_license", "output-adapter", "multi-model")),
    ("midplatform", ("midplatform", "interface-layer", "interface_layer", "model-control", "model_control", "model-data-handling", "model_data_handling", "admission")),
    ("model_governance", ("governance", "closure", "post-review", "post_review")),
)

# --------------------------------------------------------------------------- #
# Required record types (>= 6 per phase).
# --------------------------------------------------------------------------- #
REQUIRED_RECORD_TYPES: Tuple[str, ...] = (
    "test_process_record",
    "test_result_summary",
    "test_conclusion_record",
    "test_artifact_refs",
    "protected_marker",
    "non_deletable_notice",
)

# Allowed test-mode classifications.
# NOTE: "planning" was added by Phase-TestBoard-Planning-Mode-Protocol-Patch-v1-001
# as a first-class planning test_mode. It does NOT replace "virtual_test"; both
# remain valid. All previously valid modes are preserved unchanged. Adding a mode
# is backward compatible: existing records, directories and manifests are not
# modified, migrated or deleted by this addition.
TEST_MODES: Tuple[str, ...] = (
    "planning",
    "virtual_test",
    "dry_run",
    "real_test",
    "runtime_trial",
    "post_review",
    "closure_review",
)


def is_valid_test_mode(mode: str) -> bool:
    """Validation helper: is `mode` an allowed test_mode?"""
    return mode in TEST_MODES


@dataclass(frozen=True)
class TestBoardProtectedArtifactRule:
    protocol_id: str
    protocol_phase_ref: str
    test_board_rel_root: str
    required_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]
    modules: Tuple[str, ...]
    required_record_types: Tuple[str, ...]
    test_modes: Tuple[str, ...]
    source_chain: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)


def build_test_board_protected_artifact_rule_v1() -> TestBoardProtectedArtifactRule:
    return TestBoardProtectedArtifactRule(
        protocol_id=PROTOCOL_ID,
        protocol_phase_ref=PROTOCOL_PHASE_REF,
        test_board_rel_root=TEST_BOARD_REL_ROOT,
        required_fields=dict(REQUIRED_TEST_BOARD_FIELDS),
        governance_rules=TEST_BOARD_GOVERNANCE_RULES,
        modules=TEST_BOARD_MODULES,
        required_record_types=REQUIRED_RECORD_TYPES,
        test_modes=TEST_MODES,
        source_chain=SOURCE_CHAIN,
    )


# Module-level singleton of the rule, exported for later phases to import as
# `TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1`.
TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1 = build_test_board_protected_artifact_rule_v1()


def build_test_board_protocol_matrix_v1() -> Dict[str, Any]:
    rule = build_test_board_protected_artifact_rule_v1()
    return {
        "protocol_id": PROTOCOL_ID,
        "protocol_phase_ref": PROTOCOL_PHASE_REF,
        "source_chain": SOURCE_CHAIN,
        "test_board_protected_artifact_rule": candidate_to_dict(rule),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS),
        "test_board_governance_rules": list(TEST_BOARD_GOVERNANCE_RULES),
        "test_board_modules": list(TEST_BOARD_MODULES),
        "required_record_types": list(REQUIRED_RECORD_TYPES),
        "test_modes": list(TEST_MODES),
    }


def resolve_module(phase_id: str, scope: str = "") -> str:
    """Route a phase to exactly one test board module by id/scope keywords."""
    hay = f"{phase_id} {scope}".lower()
    for module, keywords in _MODULE_ROUTING:
        if any(k in hay for k in keywords):
            return module
    return "general"


def _slug(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return slug or "phase"


def write_test_board_records(
    review_result: Dict[str, Any],
    *,
    test_mode: str,
    repo_root: Path,
    module: Optional[str] = None,
    source_review_file: Optional[str] = None,
    extra_artifact_refs: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Write the 6 protected, non-deletable test board records for a phase.

    Returns a manifest dict (also written as `test_board_manifest.json`). This is
    the durable evidence layer; callers may additionally write to `_tmp_eval_out`.
    """
    phase_id = review_result.get("phase_id", "unknown_phase")
    scope = review_result.get("source_chain", review_result.get("lifecycle_variant", ""))
    if module is None:
        module = resolve_module(phase_id, scope)
    if test_mode not in TEST_MODES:
        raise ValueError(f"invalid test_mode={test_mode!r}; allowed={TEST_MODES}")

    phase_dir = _slug(phase_id)
    board_dir = repo_root / TEST_BOARD_REL_ROOT / module / phase_dir
    board_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc).isoformat()
    protected_flags = dict(REQUIRED_TEST_BOARD_FIELDS)

    final_decision = review_result.get("final_decision")
    blocker_count = review_result.get("blocker_count")
    passed_checks = review_result.get("passed_checks", [])
    failed_checks = review_result.get("failed_checks", [])

    # Collect a compact set of count fields from the review for the summary.
    count_fields = {
        k: v for k, v in review_result.items()
        if k.endswith("_count") and isinstance(v, (int, float))
    }

    artifact_refs: List[str] = []
    if source_review_file:
        artifact_refs.append(source_review_file)
    if review_result.get("output_review_file"):
        artifact_refs.append(review_result["output_review_file"])
    if extra_artifact_refs:
        artifact_refs.extend(extra_artifact_refs)

    common = {
        "protocol_id": PROTOCOL_ID,
        "phase_id": phase_id,
        "module": module,
        "test_mode": test_mode,
        "recorded_at_utc": now,
        **protected_flags,
    }

    records: Dict[str, Dict[str, Any]] = {
        "test_process_record": {
            **common,
            "record_type": "test_process_record",
            "scope": scope,
            "steps_executed": review_result.get("dryrun_governance_rules")
            or review_result.get("planning_governance_rules")
            or review_result.get("governance_rules", []),
            "passed_check_count": len(passed_checks),
            "failed_check_count": len(failed_checks),
            "stage_refs": review_result.get("stage_refs", []),
            "upstream_sealed_phase_review": review_result.get("upstream_sealed_phase_review", {}),
        },
        "test_result_summary": {
            **common,
            "record_type": "test_result_summary",
            "final_decision": final_decision,
            "blocker_count": blocker_count,
            "count_fields": count_fields,
        },
        "test_conclusion_record": {
            **common,
            "record_type": "test_conclusion_record",
            "conclusions": review_result.get("conclusions", {}),
            "final_decision": final_decision,
        },
        "test_artifact_refs": {
            **common,
            "record_type": "test_artifact_refs",
            "artifact_refs": artifact_refs,
            "source_review_file": source_review_file,
        },
        "protected_marker": {
            **common,
            "record_type": "protected_marker",
            "protected": True,
            "non_deletable": True,
        },
        "non_deletable_notice": {
            **common,
            "record_type": "non_deletable_notice",
            "notice": (
                "This test board record is protected and non-deletable. Cleanup scripts must not "
                "remove it. Any deletion requires explicit governance approval."
            ),
            "governance_rules": list(TEST_BOARD_GOVERNANCE_RULES),
            "deletion_requires_governance_approval": True,
        },
    }

    written: List[str] = []
    for record_type, payload in records.items():
        out_path = board_dir / f"{record_type}.json"
        out_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        written.append(str(out_path))

    manifest = {
        "protocol_id": PROTOCOL_ID,
        "protocol_phase_ref": PROTOCOL_PHASE_REF,
        "phase_id": phase_id,
        "module": module,
        "test_mode": test_mode,
        "test_board_dir": str(board_dir),
        "recorded_at_utc": now,
        "required_record_types": list(REQUIRED_RECORD_TYPES),
        "written_records": written,
        "written_record_count": len(written),
        "required_test_board_fields": protected_flags,
        "test_board_governance_rules": list(TEST_BOARD_GOVERNANCE_RULES),
        "final_decision": final_decision,
        "blocker_count": blocker_count,
        "all_required_records_present": all(
            (board_dir / f"{rt}.json").is_file() for rt in REQUIRED_RECORD_TYPES
        ),
    }
    manifest_path = board_dir / "test_board_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    manifest["manifest_path"] = str(manifest_path)
    return manifest
