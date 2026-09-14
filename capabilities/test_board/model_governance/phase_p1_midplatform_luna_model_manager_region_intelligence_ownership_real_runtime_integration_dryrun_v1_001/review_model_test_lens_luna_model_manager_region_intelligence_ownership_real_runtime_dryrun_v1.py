# -*- coding: utf-8 -*-
"""P1 Ownership Real Runtime Integration — dryrun review v1."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[4]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def _detect_repo_root() -> Path:
    for base in (Path.cwd(), Path(__file__).resolve().parents[4]):
        if (base / "capabilities/test_board/test_board_protocol_v1.py").is_file():
            return base
    return _REPO_ROOT


from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Real-Runtime-Integration-DryRun-v1-001"
DRY_REL = "capabilities/midplatform/model_manager/runtime/mixed_region/ownership_runtime/dryrun"
MM_REL = "capabilities/midplatform/model_manager"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_real_runtime_integration_dryrun_v1_001"
)

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_REAL_RUNTIME_INTEGRATION_PLANNING_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_real_runtime_integration_planning_v1_review_v0/"
        "p1_midplatform_luna_model_manager_region_intelligence_ownership_real_runtime_integration_planning_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_ATTENTION_GATED_REGION_INTELLIGENCE_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_situation_understanding_attention_gated_ri_dryrun_v1_review_v0/"
        "p1_midplatform_luna_situation_understanding_attention_gated_ri_dryrun_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_REAL_RUNTIME_INTEGRATION_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_REGION_INTELLIGENCE_OWNERSHIP_REAL_RUNTIME_INTEGRATION_DRYRUN_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Region-Intelligence-Ownership-Lightweight-Vision-Runtime-Planning-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{DRY_REL}/ownership_runtime_dryrun_adapter_v1.py",
    f"{DRY_REL}/ownership_slot_binding_v1.py",
    f"{DRY_REL}/ownership_discovery_simulator_v1.py",
    f"{DRY_REL}/occlusion_reasoning_simulator_v1.py",
    f"{DRY_REL}/text_owner_assignment_simulator_v1.py",
    f"{DRY_REL}/ownership_evidence_package_builder_v1.py",
    f"{DRY_REL}/per_entity_channel_activation_adapter_v1.py",
    f"{DRY_REL}/ownership_runtime_dryrun_policy_v1.json",
    f"{MM_REL}/luna_model_manager_region_intelligence_ownership_real_runtime_dryrun_types_v1.py",
    f"{MM_REL}/luna_model_manager_region_intelligence_ownership_real_runtime_dryrun_processor_v1.py",
    f"{TB_REL}/luna_model_manager_region_intelligence_ownership_real_runtime_dryrun_fixtures_v1.py",
    f"{TB_REL}/run_luna_model_manager_region_intelligence_ownership_real_runtime_dryrun_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_region_intelligence_ownership_real_runtime_dryrun_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("slot_binding", "Ownership Slot Binding"),
        ("discovery_sim", "Discovery Simulator"),
        ("occlusion_sim", "Occlusion Simulator"),
        ("text_owner_sim", "Text Owner Simulator"),
        ("evidence_builder", "Evidence Package Builder"),
        ("channel_adapter", "Channel Activation Adapter"),
        ("dryrun_adapter", "DryRun Adapter"),
        ("dryrun_policy", "DryRun Policy"),
        ("no_global_ocr", "no_global_ocr"),
        ("no_all_model_activation", "no_all_model_activation"),
        ("attention_gate_required", "attention_gate_required"),
        ("owner_required_for_text", "owner_required_for_text"),
        ("occlusion_not_absence", "occlusion_not_absence"),
        ("reflection_not_real_sign", "reflection_not_real_sign"),
        ("runtime_error_no_silent_fallback", "runtime_error_no_silent_fallback"),
        ("candidate_only_not_fact", "candidate_only_not_fact"),
        ("case_a_stacked", "Case A 叠放纸张"),
        ("case_b_shelf", "Case B 货架价签"),
        ("case_c_reflection", "Case C 玻璃反光"),
        ("case_d_blocked", "Case D Attention Blocked"),
        ("case_e_occluded", "Case E 遮挡缺失"),
        ("case_f_runtime", "Case F Runtime 故障"),
        ("upstream_go", "上游 GO"),
        ("dryrun_pass", "dryrun 通过"),
    ], start=1)
)


def _read(rel: str) -> str:
    for base in (_detect_repo_root(), _REPO_ROOT, Path.cwd()):
        p = base / rel
        if p.is_file():
            return p.read_text(encoding="utf-8")
    return ""


def _load_json(path: Path) -> Dict[str, Any]:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _case(cases: List[Dict[str, Any]], case_id: str) -> Dict[str, Any]:
    return next((c for c in cases if c.get("case_id") == case_id), {})


def _audit() -> Dict[str, bool]:
    policy = _load_json(_detect_repo_root() / f"{DRY_REL}/ownership_runtime_dryrun_policy_v1.json")

    dryrun_result: Dict[str, Any] = {}
    sample: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_region_intelligence_ownership_real_runtime_integration_dryrun_v1_001.luna_model_manager_region_intelligence_ownership_real_runtime_dryrun_fixtures_v1 import (  # noqa: WPS433
            run_all_dryrun_cases,
        )
        from capabilities.midplatform.model_manager.runtime.mixed_region.ownership_runtime.dryrun.ownership_runtime_dryrun_adapter_v1 import (  # noqa: WPS433
            run_ownership_runtime_dryrun,
        )
        dryrun_result = run_all_dryrun_cases()
        sample = run_ownership_runtime_dryrun(fixture_key="stacked_papers")
    except Exception:
        dryrun_result = {"final_decision": FINAL_BLOCKED}

    cases = dryrun_result.get("dryrun_cases", [])
    upstream_ok = all(
        _load_json(_detect_repo_root() / rel).get("final_decision") == go
        for go, rel in UPSTREAM_PATHS.items()
    )
    reflection_case = _case(cases, "case_c_glass_reflection").get("result") or {}

    return {
        "slot_binding": "bind_ownership_slots" in _read(f"{DRY_REL}/ownership_slot_binding_v1.py"),
        "discovery_sim": "simulate_ownership_discovery" in _read(f"{DRY_REL}/ownership_discovery_simulator_v1.py"),
        "occlusion_sim": "simulate_occlusion_reasoning" in _read(f"{DRY_REL}/occlusion_reasoning_simulator_v1.py"),
        "text_owner_sim": "simulate_text_owner_assignment" in _read(f"{DRY_REL}/text_owner_assignment_simulator_v1.py"),
        "evidence_builder": "build_ownership_evidence_package" in _read(f"{DRY_REL}/ownership_evidence_package_builder_v1.py"),
        "channel_adapter": "adapt_per_entity_channel_activation" in _read(f"{DRY_REL}/per_entity_channel_activation_adapter_v1.py"),
        "dryrun_adapter": "run_ownership_runtime_dryrun" in _read(f"{DRY_REL}/ownership_runtime_dryrun_adapter_v1.py"),
        "dryrun_policy": policy.get("schema_id") == "OwnershipRuntimeDryrunPolicyV1",
        "no_global_ocr": sample.get("no_global_ocr") is True,
        "no_all_model_activation": sample.get("no_all_model_activation") is True,
        "attention_gate_required": sample.get("attention_gate_required") is True,
        "owner_required_for_text": sample.get("owner_required_for_text") is True,
        "occlusion_not_absence": sample.get("occlusion_not_absence") is True,
        "reflection_not_real_sign": reflection_case.get("reflection_not_real_sign") is True,
        "runtime_error_no_silent_fallback": _case(cases, "case_f_runtime_failure").get("passed") is True,
        "candidate_only_not_fact": sample.get("candidate_only_not_fact") is True,
        "case_a_stacked": _case(cases, "case_a_stacked_papers").get("passed") is True,
        "case_b_shelf": _case(cases, "case_b_shelf_price_tags").get("passed") is True,
        "case_c_reflection": _case(cases, "case_c_glass_reflection").get("passed") is True,
        "case_d_blocked": _case(cases, "case_d_attention_blocked").get("passed") is True,
        "case_e_occluded": _case(cases, "case_e_occluded_missing").get("passed") is True,
        "case_f_runtime": _case(cases, "case_f_runtime_failure").get("passed") is True,
        "upstream_go": upstream_ok,
        "dryrun_pass": dryrun_result.get("final_decision", "").endswith("_GO"),
    }


def review(*, write_file: bool = True, write_test_board: bool = True, test_board_root: Optional[str] = None) -> Dict[str, Any]:
    failed: List[str] = []
    for rel in REQUIRED_FILES:
        if not _read(rel):
            failed.append(f"file.missing={rel}")

    flags = _audit()
    guards = []
    for spec in NEGATIVE_GUARDS:
        passed = bool(flags.get(spec["key"], False))
        guards.append({**spec, "passed": passed})
        if not passed:
            failed.append(f"guard.{spec['guard_id']}.fail={spec['key']}")

    decision = FINAL_GO if not failed else FINAL_BLOCKED
    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_real_runtime_integration_dryrun_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "layer_id": "Region_Intelligence_Ownership_Runtime_Dryrun",
        "dryrun_only": True,
        "recommended_next_phase": NEXT_PHASE,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_passed": sum(1 for g in guards if g["passed"]),
        "dryrun_cases_passed": flags.get("dryrun_pass", False),
        "blocker_count": len(failed),
        "failed_checks": failed,
        "known_limits": ["dryrun_fixture_only", "no_real_segmentation_models"],
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_model_manager_region_intelligence_ownership_real_runtime_integration_dryrun_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)

    if write_test_board and decision == FINAL_GO:
        root = Path(test_board_root or str(_detect_repo_root()))
        try:
            tb = write_test_board_records(result, test_mode="dry_run", repo_root=root, module="model_governance", source_review_file=result.get("output_review_file"))
        except (OSError, PermissionError, TypeError):
            standin = _detect_repo_root() / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(result, test_mode="dry_run", repo_root=standin, module="model_governance", source_review_file=result.get("output_review_file"))
        result["test_board_root"] = str(tb.get("test_board_dir", TB_REL))

    return result


def main() -> int:
    r = review(test_board_root=str(_detect_repo_root()))
    print(json.dumps({
        "final_decision": r["final_decision"],
        "blocker_count": r["blocker_count"],
        "dryrun_cases_passed": r.get("dryrun_cases_passed"),
        "review_guards_passed": r.get("negative_guard_passed"),
        "recommended_next_phase": r.get("recommended_next_phase"),
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
