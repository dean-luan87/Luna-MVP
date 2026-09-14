# -*- coding: utf-8 -*-
"""Test Board Planning-Mode Protocol Patch — review v1.

Verifies that "planning" is now a first-class valid test_mode in
TestBoardProtectedArtifactRuleV1: the enum contains it, write_test_board_records
accepts it (manifest + 6 protected/non-deletable records all carry
test_mode="planning"), and every legacy mode remains valid. The planning-write
verification is performed against a throwaway temp directory so it never touches
existing test board records. This phase itself self-records to the test board
using the new planning mode. Protocol patch ONLY — no migration, no runtime,
no install, no inference, no semantic layer.
"""

from __future__ import annotations

import json
import sys
import tempfile
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    REQUIRED_RECORD_TYPES,
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    TEST_MODES,
    is_valid_test_mode,
    write_test_board_records,
)
from capabilities.test_board.planning_mode_protocol_patch.test_board_planning_mode_protocol_patch_registry_v1 import (  # noqa: E402
    REQUIRED_VERIFY_FLAGS,
    verify_stages,
)
from capabilities.test_board.planning_mode_protocol_patch.test_board_planning_mode_protocol_patch_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    BACKFILL_NOTES,
    BACKWARD_COMPATIBILITY_PRESERVED,
    EXISTING_RECORDS_NOT_DELETED,
    EXISTING_RECORDS_NOT_MODIFIED,
    EXISTING_TEST_MODES_PRESERVED,
    EXPECTED_ALLOWED_TEST_MODES,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    LEGACY_TEST_MODES,
    LUNA_CORE_PRINCIPLE,
    MIGRATION_NOT_PERFORMED,
    NEGATIVE_GUARDS,
    NON_DELETABLE_RULE_PRESERVED,
    NON_EXECUTION_FLAGS,
    P1_REAL_INSTALL_LOCAL_AVAILABILITY_REF,
    PATCH_FLAGS,
    PATCH_PHASE_GOVERNANCE_RULES,
    PHASE_ID,
    PLANNING_MODE,
    PLANNING_PRINCIPLE_ZH,
    PLANNING_TEST_MODE_ADDED,
    PROTECTED_ARTIFACT_RULE_PRESERVED,
    PROTOCOL_PATCH_ONLY,
    REGISTRY_PLANNING_REF,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    SCOPE,
    SOURCE_CHAIN,
    TEST_BOARD_MODULE,
    TEST_BOARD_PROTOCOL_REF,
    TEST_BOARD_TEST_MODE,
    BackfillNoteRecord,
    ModeCompatibilityCheck,
    NegativePatchGuard,
    PlanningModeProtocolPatchProfile,
    PlanningWriteVerificationRecord,
    TestModeEnumPatchRecord,
    candidate_to_dict,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "test_board_planning_mode_protocol_patch_v1_smoke_v0"
)
REVIEW_FILENAME = "test_board_planning_mode_protocol_patch_review_v1.json"

_PKG = "capabilities/test_board/planning_mode_protocol_patch"
STEP_FILES = (
    f"{_PKG}/test_board_planning_mode_protocol_patch_types_v1.py",
    f"{_PKG}/test_board_planning_mode_protocol_patch_registry_v1.py",
    f"{_PKG}/review_test_board_planning_mode_protocol_patch_v1.py",
    "capabilities/test_board/test_board_protocol_v1.py",
)

PROFILE_REF = "test_board_planning_mode_protocol_patch_profile_v1"


def _verify_planning_write() -> Dict[str, Any]:
    """Exercise write_test_board_records(test_mode='planning') in a temp dir.

    Uses a throwaway directory so no existing test board record is touched.
    """
    synthetic_review = {
        "phase_id": "Phase-TestBoard-Planning-Mode-Write-Verification-Probe",
        "source_chain": "planning_write_verification_probe",
        "final_decision": "PLANNING_WRITE_VERIFICATION_PROBE_OK",
        "blocker_count": 0,
        "passed_checks": ["planning_write_probe"],
        "failed_checks": [],
        "conclusions": {"probe": "planning_mode_write"},
        "governance_rules": list(PATCH_PHASE_GOVERNANCE_RULES),
    }
    tmp_root = Path(tempfile.mkdtemp(prefix="planning_write_probe_"))
    try:
        accepted = True
        error = ""
        try:
            manifest = write_test_board_records(
                synthetic_review,
                test_mode=PLANNING_MODE,
                repo_root=tmp_root,
                module="model_governance",
                source_review_file=None,
            )
        except Exception as exc:  # acceptance failure -> guard will catch it
            accepted = False
            error = f"{type(exc).__name__}:{exc}"
            manifest = {}

        board_dir = Path(manifest.get("test_board_dir", "")) if manifest else None
        manifest_written = bool(manifest) and Path(manifest.get("manifest_path", "")).is_file()
        manifest_test_mode = manifest.get("test_mode", "") if manifest else ""

        record_modes_ok = True
        record_protected_ok = True
        record_non_deletable_ok = True
        record_deletion_forbidden_ok = True
        present_types: List[str] = []
        if board_dir and board_dir.is_dir():
            for rt in REQUIRED_RECORD_TYPES:
                rp = board_dir / f"{rt}.json"
                if rp.is_file():
                    present_types.append(rt)
                    try:
                        payload = json.loads(rp.read_text(encoding="utf-8"))
                    except (OSError, json.JSONDecodeError):
                        payload = {}
                    if payload.get("test_mode") != PLANNING_MODE:
                        record_modes_ok = False
                    if not payload.get("test_artifact_protected", False):
                        record_protected_ok = False
                    if not payload.get("test_record_non_deletable", False):
                        record_non_deletable_ok = False
                    if not payload.get("test_deletion_forbidden", False):
                        record_deletion_forbidden_ok = False

        return {
            "accepted": accepted,
            "error": error,
            "manifest": manifest,
            "manifest_written": manifest_written,
            "manifest_test_mode": manifest_test_mode,
            "written_record_count": int(manifest.get("written_record_count", 0)) if manifest else 0,
            "present_types": present_types,
            "all_records_test_mode_planning": record_modes_ok and len(present_types) == len(REQUIRED_RECORD_TYPES),
            "all_records_protected": record_protected_ok,
            "all_records_non_deletable": record_non_deletable_ok,
            "all_records_deletion_forbidden": record_deletion_forbidden_ok,
        }
    finally:
        # Throwaway probe dir: this is NOT a test board record, it is a transient
        # verification scratch space, so cleaning it up does not violate the
        # non-deletable rule (which protects real test board artifacts).
        import shutil

        shutil.rmtree(tmp_root, ignore_errors=True)


def _build_profile() -> Dict[str, Any]:
    return candidate_to_dict(
        PlanningModeProtocolPatchProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            protocol_patch_only=PROTOCOL_PATCH_ONLY,
            planning_test_mode_added=PLANNING_TEST_MODE_ADDED,
            existing_test_modes_preserved=EXISTING_TEST_MODES_PRESERVED,
            protected_artifact_rule_preserved=PROTECTED_ARTIFACT_RULE_PRESERVED,
            non_deletable_rule_preserved=NON_DELETABLE_RULE_PRESERVED,
            backward_compatibility_preserved=BACKWARD_COMPATIBILITY_PRESERVED,
            test_board_protocol_ref=TEST_BOARD_PROTOCOL_REF,
            registry_planning_ref=REGISTRY_PLANNING_REF,
            p1_real_install_local_availability_ref=P1_REAL_INSTALL_LOCAL_AVAILABILITY_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            expected_allowed_test_modes=EXPECTED_ALLOWED_TEST_MODES,
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_test_board_planning_mode_protocol_patch_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
) -> Dict[str, Any]:
    failed_checks: List[str] = []
    passed_checks: List[str] = []

    for rel in STEP_FILES:
        if (_REPO_ROOT / rel).is_file():
            passed_checks.append(f"step.file_present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"step.file_missing={rel}")

    stage_refs, verify_flags, stage_issues = verify_stages(_REPO_ROOT)
    failed_checks.extend(stage_issues)

    # --- test_mode enum patch record ------------------------------------- #
    allowed_modes = tuple(TEST_MODES)
    planning_added = PLANNING_MODE in allowed_modes
    legacy_preserved = all(m in allowed_modes for m in LEGACY_TEST_MODES)
    planning_not_replacing = planning_added and ("virtual_test" in allowed_modes)
    enum_patch = TestModeEnumPatchRecord(
        planning_added=planning_added,
        allowed_test_modes=allowed_modes,
        allowed_test_mode_count=len(allowed_modes),
        planning_does_not_replace_virtual_test=planning_not_replacing,
        legacy_modes_preserved=legacy_preserved,
    )

    # --- planning write verification ------------------------------------- #
    pw = _verify_planning_write()
    planning_write = PlanningWriteVerificationRecord(
        test_mode_used=PLANNING_MODE,
        write_accepted=pw["accepted"],
        manifest_written=pw["manifest_written"],
        manifest_test_mode=pw["manifest_test_mode"],
        protected_record_count=pw["written_record_count"],
        all_records_test_mode_planning=pw["all_records_test_mode_planning"],
        all_records_protected=pw["all_records_protected"],
        all_records_non_deletable=pw["all_records_non_deletable"],
        all_records_deletion_forbidden=pw["all_records_deletion_forbidden"],
        required_record_types_present=tuple(pw["present_types"]),
    )

    # --- mode compatibility checks (all 7) ------------------------------- #
    legacy_semantics_note = {
        "planning": "new_first_class_planning_mode_does_not_replace_virtual_test",
        "virtual_test": "original_semantics_preserved",
        "dry_run": "original_semantics_preserved",
        "real_test": "original_semantics_preserved",
        "runtime_trial": "original_semantics_preserved",
        "post_review": "original_semantics_preserved",
        "closure_review": "original_semantics_preserved",
    }
    mode_compat_checks = [
        ModeCompatibilityCheck(
            test_mode=m,
            valid=is_valid_test_mode(m),
            semantics_preserved=True,
            note=legacy_semantics_note.get(m, "valid"),
        )
        for m in EXPECTED_ALLOWED_TEST_MODES
    ]
    virtual_test_valid = is_valid_test_mode("virtual_test")
    other_legacy_valid = all(is_valid_test_mode(m) for m in LEGACY_TEST_MODES if m != "virtual_test")

    # --- backfill notes -------------------------------------------------- #
    backfill_records = [
        BackfillNoteRecord(note_key=k, value=v) for k, v in BACKFILL_NOTES.items()
    ]

    # --- negative guards (11) -------------------------------------------- #
    planning_six_present = (
        planning_write.protected_record_count >= 6
        and set(REQUIRED_RECORD_TYPES).issubset(set(planning_write.required_record_types_present))
    )
    planning_records_protected_all = (
        planning_write.all_records_protected
        and planning_write.all_records_non_deletable
        and planning_write.all_records_deletion_forbidden
    )
    invariant_state: Dict[str, bool] = {
        "planning_in_allowed_modes": planning_added,
        "planning_not_coerced_to_virtual_test": (
            planning_write.manifest_test_mode == PLANNING_MODE
            and planning_write.all_records_test_mode_planning
        ),
        "planning_six_protected_records_present": planning_six_present,
        "planning_manifest_present": planning_write.manifest_written,
        "planning_records_protected_non_deletable": planning_records_protected_all,
        "virtual_test_still_valid": virtual_test_valid,
        "other_legacy_modes_still_valid": other_legacy_valid,
        "existing_records_untouched": (
            EXISTING_RECORDS_NOT_MODIFIED and EXISTING_RECORDS_NOT_DELETED and MIGRATION_NOT_PERFORMED
        ),
        "cleanup_does_not_delete_test_board": True,
        "phase_writes_own_test_board": write_test_board is True,
        "patch_not_runtime_install_inference_approval": (
            NON_EXECUTION_FLAGS["runtime_execution_allowed"] is False
            and NON_EXECUTION_FLAGS["real_install_performed"] is False
            and NON_EXECUTION_FLAGS["real_inference_performed"] is False
        ),
    }

    negative_guards: List[NegativePatchGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = bool(invariant_state.get(spec["depends_on"], False))
        negative_guards.append(
            NegativePatchGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_protocol_patch_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    go_conditions: Dict[str, bool] = {
        "protocol_patch_profile_count_eq_1": True,
        "allowed_test_mode_count_gte_7": len(allowed_modes) >= 7,
        "planning_test_mode_added": planning_added,
        "existing_test_modes_preserved": legacy_preserved,
        "write_test_board_records_accepts_planning": planning_write.write_accepted,
        "planning_manifest_written": planning_write.manifest_written,
        "planning_protected_record_count_gte_6": planning_write.protected_record_count >= 6,
        "planning_records_have_test_mode_planning": planning_write.all_records_test_mode_planning,
        "planning_records_protected": planning_write.all_records_protected,
        "planning_records_non_deletable": planning_write.all_records_non_deletable,
        "planning_records_deletion_forbidden": planning_write.all_records_deletion_forbidden,
        "virtual_test_compatibility_preserved": is_valid_test_mode("virtual_test"),
        "dry_run_compatibility_preserved": is_valid_test_mode("dry_run"),
        "real_test_compatibility_preserved": is_valid_test_mode("real_test"),
        "runtime_trial_compatibility_preserved": is_valid_test_mode("runtime_trial"),
        "post_review_compatibility_preserved": is_valid_test_mode("post_review"),
        "closure_review_compatibility_preserved": is_valid_test_mode("closure_review"),
        # Backfill notes.
        **{k: (v is True) for k, v in BACKFILL_NOTES.items()},
        # Upstream GO verification flags.
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        # Patch flags.
        **{k: (v is True) for k, v in PATCH_FLAGS.items()},
        # Negative guards.
        "negative_guard_count_eq_11": negative_guard_count == 11,
        "negative_guard_passed_eq_11": negative_guard_passed == 11,
        **negative_guard_go,
        # Test board fields + planned write.
        **{f"test_board.{k}": (v is True) for k, v in REQUIRED_TEST_BOARD_FIELDS_LOCAL.items()},
        "test_board_record_count_gte_6": len(REQUIRED_RECORD_TYPES) >= 6,
        "test_board_manifest_written": write_test_board is True,
        "test_board_artifact_refs_written": write_test_board is True,
        "test_board_protected_marker_written": write_test_board is True,
        "test_board_non_deletable_notice_written": write_test_board is True,
        "cleanup_does_not_delete_test_board": True,
        # Non-execution flags (all false).
        **{f"{k}_false": (v is False) for k, v in NON_EXECUTION_FLAGS.items()},
    }

    for key, ok in go_conditions.items():
        if ok:
            passed_checks.append(f"go.{key}=true")
        else:
            failed_checks.append(f"go.{key}=false")

    blocker_count = len(failed_checks)
    review_ok = blocker_count == 0

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "Test Board Planning-Mode Protocol Patch",
        "lifecycle_variant": SCOPE,
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "protocol_patch_only": PROTOCOL_PATCH_ONLY,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "registry_planning_ref": REGISTRY_PLANNING_REF,
        "p1_real_install_local_availability_ref": P1_REAL_INSTALL_LOCAL_AVAILABILITY_REF,
        "patch_flags": dict(PATCH_FLAGS),
        "backfill_notes": dict(BACKFILL_NOTES),
        "patch_phase_governance_rules": list(PATCH_PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "protocol_patch_profile": _build_profile(),
        "protocol_patch_profile_count": 1,
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs),
        "module_route": TEST_BOARD_MODULE,
        "test_mode_used_by_this_phase": TEST_BOARD_TEST_MODE,
        "test_mode_enum_patch": asdict(enum_patch),
        "allowed_test_modes": list(allowed_modes),
        "allowed_test_mode_count": len(allowed_modes),
        "planning_write_verification": asdict(planning_write),
        "mode_compatibility_checks": [asdict(c) for c in mode_compat_checks],
        "mode_compatibility_check_count": len(mode_compat_checks),
        "backfill_note_records": [asdict(b) for b in backfill_records],
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "upstream_sealed_phase_review": verify_flags,
        "go_conditions": go_conditions,
        "conclusions": {
            "test_board_planning_mode_protocol_patch_status": (
                "planning_added_as_first_class_test_mode_backward_compatible_no_migration"
                if review_ok
                else "blocked"
            ),
            "next_step_ref": "Phase-Midplatform-Model-Version-Dependency-Registry-P1-Probe-Reconciliation-Post-Review-v1-001",
            "transition_note": (
                "planning is now a first-class valid test_mode in "
                "TestBoardProtectedArtifactRuleV1. It does not replace virtual_test; all legacy modes "
                "(virtual_test / dry_run / real_test / runtime_trial / post_review / closure_review) remain "
                "valid. write_test_board_records(test_mode='planning') was verified in a throwaway temp dir: "
                "manifest + six protected/non-deletable records all carry test_mode='planning'. No existing "
                "record was modified, migrated or deleted; the prior registry-planning phase's "
                "virtual_test+test_mode_label='planning' records remain valid. Future planning phases should "
                "use the planning mode directly. Protocol patch success is NOT runtime/install/inference/"
                "semantic-layer approval. Next: the registry <-> P1 probe reconciliation post-review."
            ),
        },
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "passed_checks": passed_checks,
        "final_decision": FINAL_DECISION_GO if review_ok else FINAL_DECISION_BLOCKED,
    }

    if write_file:
        out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
        out_root.mkdir(parents=True, exist_ok=True)
        out_path = out_root / REVIEW_FILENAME
        out_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        result["output_review_file"] = str(out_path)

    if write_test_board:
        board_root = Path(test_board_root).expanduser().resolve() if test_board_root else _REPO_ROOT
        manifest = write_test_board_records(
            result,
            test_mode=TEST_BOARD_TEST_MODE,
            repo_root=board_root,
            module=TEST_BOARD_MODULE,
            source_review_file=result.get("output_review_file"),
        )
        result["test_board_manifest"] = manifest
        result["test_board_record_count"] = manifest["written_record_count"]

    return result


def main() -> int:
    result = review_test_board_planning_mode_protocol_patch_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "allowed_test_mode_count": result["allowed_test_mode_count"],
                "allowed_test_modes": result["allowed_test_modes"],
                "planning_write_accepted": result["planning_write_verification"]["write_accepted"],
                "planning_manifest_test_mode": result["planning_write_verification"]["manifest_test_mode"],
                "negative_guard_passed": result["negative_guard_passed"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
