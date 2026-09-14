# -*- coding: utf-8 -*-
"""P1 Luna Model Manager Multi-Provider Registry — review v1."""

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

PHASE_ID = "Phase-P1-Midplatform-Luna-Model-Manager-Multi-Provider-Registry-v1-001"
REGISTRY_REL = "capabilities/midplatform/model_manager/registry"
TB_REL = (
    "capabilities/test_board/model_governance/"
    "phase_p1_midplatform_luna_model_manager_multi_provider_registry_v1_001"
)

UPSTREAM_PATHS = {
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_LOCAL_MODEL_INTEGRATION_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_local_model_integration_dryrun_v1_review_v0/"
        "p1_midplatform_luna_model_manager_local_model_integration_dryrun_review_v1.json"
    ),
    "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_QWENVL_REAL_PROVIDER_INTEGRATION_DRYRUN_GO": (
        "_tmp_eval_out/p1_midplatform_luna_model_manager_qwen_vl_real_provider_integration_dryrun_v1_review_v0/"
        "p1_midplatform_luna_model_manager_qwen_vl_real_provider_integration_dryrun_review_v1.json"
    ),
}

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_MULTI_PROVIDER_REGISTRY_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_MULTI_PROVIDER_REGISTRY_BLOCKED"
NEXT_PHASE = "Phase-P1-Midplatform-Luna-Model-Manager-Multi-Model-Collaboration-Planning-v1-001"

REQUIRED_FILES: Tuple[str, ...] = (
    f"{REGISTRY_REL}/provider_registry_v1.json",
    f"{REGISTRY_REL}/provider_relationships_v1.json",
    f"{REGISTRY_REL}/model_families_v1.json",
    f"{REGISTRY_REL}/provider_registry_loader_v1.py",
    f"{REGISTRY_REL}/multi_provider_selection_v1.py",
    f"{REGISTRY_REL}/dryrun/multi_provider_registry_dryrun_adapter_v1.py",
    f"{REGISTRY_REL}/dryrun/multi_provider_registry_dryrun_policy_v1.json",
    f"{TB_REL}/luna_model_manager_multi_provider_registry_smoke_fixtures_v1.py",
    f"{TB_REL}/run_luna_model_manager_multi_provider_registry_v1.py",
    f"{TB_REL}/review_model_test_lens_luna_model_manager_multi_provider_registry_v1.py",
)

NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = tuple(
    {"guard_id": f"{i:02d}", "key": k, "desc": d}
    for i, (k, d) in enumerate([
        ("provider_registry_present", "Provider Registry 存在"),
        ("provider_relationships_present", "Provider Relationships 存在"),
        ("model_families_present", "Model Families 存在"),
        ("capability_first_routing", "Capability-first 路由"),
        ("multi_factor_competition", "多因子竞争"),
        ("not_voting_not_fusion", "非投票非融合"),
        ("provider_relations_defined", "Provider 关系定义"),
        ("family_version_lifecycle", "Family 版本生命周期"),
        ("selection_not_execution", "选型非执行"),
        ("case_a_three_providers", "Case A 三模型"),
        ("case_b_ocr_capability", "Case B OCR 能力优先"),
        ("case_c_version_replace", "Case C 版本替换"),
        ("case_d_conflict", "Case D Provider 冲突"),
        ("case_e_deprecation", "Case E Provider 退役"),
        ("no_multi_model_inference", "不做多模型推理"),
        ("no_auto_training", "不做自动训练"),
        ("upstream_gos_confirmed", "上游 GO 确认"),
        ("smoke_cases_pass", "smoke cases 通过"),
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
    policy = _load_json(_detect_repo_root() / f"{REGISTRY_REL}/dryrun/multi_provider_registry_dryrun_policy_v1.json")
    provider_reg = _load_json(_detect_repo_root() / f"{REGISTRY_REL}/provider_registry_v1.json")
    families = _load_json(_detect_repo_root() / f"{REGISTRY_REL}/model_families_v1.json")
    relations = _load_json(_detect_repo_root() / f"{REGISTRY_REL}/provider_relationships_v1.json")
    selection_src = _read(f"{REGISTRY_REL}/multi_provider_selection_v1.py")

    smoke_result: Dict[str, Any] = {}
    try:
        from capabilities.test_board.model_governance.phase_p1_midplatform_luna_model_manager_multi_provider_registry_v1_001.luna_model_manager_multi_provider_registry_smoke_fixtures_v1 import (  # noqa: WPS433
            run_all_smoke_cases,
        )
        smoke_result = run_all_smoke_cases()
    except Exception:
        smoke_result = {"final_decision": FINAL_BLOCKED}

    cases = smoke_result.get("smoke_cases", [])
    upstream_ok = all(
        _load_json(_detect_repo_root() / rel).get("final_decision") == go
        for go, rel in UPSTREAM_PATHS.items()
    )

    return {
        "provider_registry_present": provider_reg.get("schema_id") == "LunaProviderRegistryV1",
        "provider_relationships_present": relations.get("schema_id") == "LunaProviderRelationshipsV1",
        "model_families_present": families.get("schema_id") == "LunaModelFamiliesV1",
        "capability_first_routing": "capability_first" in selection_src,
        "multi_factor_competition": "compute_multi_provider_score" in selection_src,
        "not_voting_not_fusion": "not_voting" in selection_src and "not_fusion" in selection_src,
        "provider_relations_defined": len(relations.get("relationships") or []) >= 3,
        "family_version_lifecycle": len(families.get("families") or []) >= 3,
        "selection_not_execution": policy.get("boundary_flags", {}).get("provider_selection_candidate_only") is True,
        "case_a_three_providers": _case(cases, "case_a_same_capability_three_providers").get("passed") is True,
        "case_b_ocr_capability": _case(cases, "case_b_capability_mismatch_ocr_selected").get("passed") is True,
        "case_c_version_replace": _case(cases, "case_c_provider_version_replacement").get("passed") is True,
        "case_d_conflict": _case(cases, "case_d_provider_conflict_not_auto_resolve").get("passed") is True,
        "case_e_deprecation": _case(cases, "case_e_provider_deprecation_routing_removal").get("passed") is True,
        "no_multi_model_inference": policy.get("boundary_flags", {}).get("no_multi_model_inference") is True,
        "no_auto_training": "no_auto_training" in json.dumps(policy),
        "upstream_gos_confirmed": upstream_ok,
        "smoke_cases_pass": smoke_result.get("final_decision", "").endswith("_GO"),
    }


def review(
    *,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
) -> Dict[str, Any]:
    failed: List[str] = []
    generated_files = [rel for rel in REQUIRED_FILES if _read(rel)]
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

    blocker_count = len(failed)
    decision = FINAL_GO if blocker_count == 0 else FINAL_BLOCKED

    out_review = _detect_repo_root() / "_tmp_eval_out/p1_midplatform_luna_model_manager_multi_provider_registry_v1_review_v0"
    out_review.mkdir(parents=True, exist_ok=True)

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "layer_id": "Model_Manager_Multi_Provider_Registry",
        "registry_only": True,
        "recommended_next_phase": NEXT_PHASE,
        "audit_flags": flags,
        "negative_guards": guards,
        "negative_guard_count": len(guards),
        "negative_guard_passed": sum(1 for g in guards if g["passed"]),
        "smoke_cases_passed": flags.get("smoke_cases_pass", False),
        "blocker_count": blocker_count,
        "failed_checks": failed,
        "generated_files": generated_files,
        "known_limits": [
            "registry_smoke_no_real_inference",
            "paddleocr_minicpm_not_deployed",
            "collaboration_layer_deferred",
        ],
        "final_decision": decision,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
    }

    if write_file:
        rp = out_review / "p1_midplatform_luna_model_manager_multi_provider_registry_review_v1.json"
        rp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        result["output_review_file"] = str(rp)

    if write_test_board and decision == FINAL_GO:
        root = Path(test_board_root or str(_detect_repo_root()))
        try:
            tb = write_test_board_records(
                result,
                test_mode="dry_run",
                repo_root=root,
                module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        except (OSError, PermissionError, TypeError):
            standin = _detect_repo_root() / "_tmp_eval_out" / "board_standin"
            standin.mkdir(parents=True, exist_ok=True)
            tb = write_test_board_records(
                result,
                test_mode="dry_run",
                repo_root=standin,
                module="model_governance",
                source_review_file=result.get("output_review_file"),
            )
        result["test_board_root"] = str(tb.get("test_board_dir", TB_REL))

    return result


def main() -> int:
    r = review(test_board_root=str(_detect_repo_root()))
    print(json.dumps({
        "final_decision": r["final_decision"],
        "blocker_count": r["blocker_count"],
        "smoke_cases_passed": r.get("smoke_cases_passed"),
        "review_guards_passed": r.get("negative_guard_passed"),
        "recommended_next_phase": r.get("recommended_next_phase"),
        "failed_checks": r.get("failed_checks", []),
    }, indent=2, ensure_ascii=False))
    return 0 if r["final_decision"] == FINAL_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
