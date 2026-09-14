#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-OCR-Provider-Runtime-Governance-Standard-001 — Static verifier for OCR governance docs + example config.

No OCR execution; no routing changes.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _require_repo(p: str) -> Path:
    pp = Path(p).expanduser().resolve()
    if not pp.is_dir():
        raise SystemExit(f"ERROR: --repo-root must be directory: {p}")
    return pp


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=str(REPO_ROOT))
    ap.add_argument("--output-root", default="", help="Default: <repo-root>/_eval_out/ocr_provider_governance_standard_v0")
    args = ap.parse_args()

    repo = _require_repo(args.repo_root)
    if args.output_root.strip():
        out_root = Path(args.output_root).expanduser().resolve()
    else:
        out_root = (repo / "_eval_out" / "ocr_provider_governance_standard_v0").resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    blockers: List[str] = []
    matrix: List[Dict[str, Any]] = []

    docs = [
        repo / "docs/architecture/ocr/LUNA_OCR_PROVIDER_RUNTIME_GOVERNANCE_STANDARD_V0.md",
        repo / "docs/architecture/ocr/LUNA_OCR_PROVIDER_LEVELS_AND_USAGE_POLICY_V0.md",
        repo / "docs/architecture/ocr/LUNA_OCR_TRIGGER_GATE_AND_ROI_POLICY_V0.md",
        repo / "docs/architecture/ocr/LUNA_OCR_CACHE_AND_SCENE_DELTA_POLICY_V0.md",
        repo / "docs/architecture/ocr/LUNA_OCR_PROVIDER_ADMISSION_CHECKLIST_V0.md",
        repo / "docs/architecture/evaluation/LUNA_EVALUATION_OCR_PROVIDER_GOVERNANCE_STANDARD_V0.md",
        repo / "docs/architecture/evaluation/LUNA_EVALUATION_OCR_PROVIDER_GOVERNANCE_STANDARD_GO_NO_GO_PACK_V0.md",
    ]
    for d in docs:
        try:
            rel = str(d.relative_to(repo))
        except ValueError:
            rel = str(d)
        matrix.append({"artifact": rel, "exists": d.is_file()})
        if not d.is_file():
            blockers.append(f"missing_doc:{d.name}")

    cfg_p = repo / "configs/ocr/ocr_provider_runtime_governance_v0.example.json"
    try:
        rel_cfg = str(cfg_p.relative_to(repo))
    except ValueError:
        rel_cfg = str(cfg_p)
    matrix.append({"artifact": rel_cfg, "exists": cfg_p.is_file()})
    if not cfg_p.is_file():
        blockers.append("missing_governance_config_example")
        cfg: Dict[str, Any] = {}
    else:
        cfg = _read_json(cfg_p)

    if str(cfg.get("schema_version") or "") != "ocr_provider_runtime_governance_v0":
        blockers.append("bad_schema_version")

    levels = cfg.get("provider_levels") if isinstance(cfg.get("provider_levels"), dict) else {}
    for lk in ("level_0", "level_1", "level_2", "level_3"):
        if lk not in levels or not isinstance(levels.get(lk), dict):
            blockers.append(f"missing_provider_level:{lk}")
        else:
            lv = levels[lk]
            if "name" not in lv or "runs_model" not in lv:
                blockers.append(f"incomplete_provider_level:{lk}")

    tp = cfg.get("trigger_policy") if isinstance(cfg.get("trigger_policy"), dict) else {}
    if tp.get("default_frame_wise_ocr_allowed") is not False:
        blockers.append("trigger_must_disallow_default_frame_wise_ocr")
    if tp.get("full_image_realtime_ocr_allowed") is not False:
        blockers.append("trigger_must_disallow_full_image_realtime_ocr_default")
    if tp.get("roi_first") is not True:
        blockers.append("trigger_must_require_roi_first")

    if not isinstance(cfg.get("roi_policy"), dict):
        blockers.append("missing_roi_policy")
    if not isinstance(cfg.get("cache_policy"), dict):
        blockers.append("missing_cache_policy")
    if not isinstance(cfg.get("runtime_budget"), dict):
        blockers.append("missing_runtime_budget")

    ep = cfg.get("evidence_policy") if isinstance(cfg.get("evidence_policy"), dict) else {}
    if ep.get("provider_output_is_fact") is not False:
        blockers.append("evidence_must_state_provider_output_is_not_fact")
    if ep.get("must_pass_ocr_bridge") is not True:
        blockers.append("evidence_must_require_ocr_bridge")
    if ep.get("direct_midplatform_write_allowed") is True or ep.get("direct_world_model_write_allowed") is True:
        blockers.append("evidence_must_forbid_direct_midplatform_or_world_writes")

    fa = cfg.get("forbidden_actions") if isinstance(cfg.get("forbidden_actions"), dict) else {}
    if not fa:
        blockers.append("missing_forbidden_actions")
    for fk in (
        "replace_runtime_provider_without_release_gate",
        "bypass_ocr_bridge",
        "write_world_model_directly",
        "change_routing_from_evaluation",
        "business_module_direct_ocr_provider_call",
        "ocr_provider_direct_midplatform_write",
        "evaluation_provider_to_production_route",
    ):
        if fk not in fa:
            blockers.append(f"missing_forbidden_action_key:{fk}")

    orch = cfg.get("orchestration_policy") if isinstance(cfg.get("orchestration_policy"), dict) else {}
    if orch.get("only_gateway_selects_provider") is not True:
        blockers.append("orchestration_must_set_only_gateway_selects_provider")
    if orch.get("business_modules_submit_ocr_request_only") is not True:
        blockers.append("orchestration_must_require_ocr_request_only_from_business_modules")

    oreq = cfg.get("ocr_request_contract_v0") if isinstance(cfg.get("ocr_request_contract_v0"), dict) else {}
    rf = oreq.get("required_fields") if isinstance(oreq.get("required_fields"), list) else []
    for fld in (
        "request_id",
        "task_context",
        "scene_context",
        "urgency",
        "input_type",
        "image_ref",
        "roi_refs",
        "expected_output",
        "privacy_level",
        "latency_budget_ms",
        "allow_remote",
        "allow_heavy_ocr",
        "cache_policy",
        "source_task_id",
    ):
        if fld not in rf:
            blockers.append(f"ocr_request_contract_missing_field:{fld}")

    odd = cfg.get("ocr_dispatch_decision_contract_v0") if isinstance(cfg.get("ocr_dispatch_decision_contract_v0"), dict) else {}
    df = odd.get("required_fields") if isinstance(odd.get("required_fields"), list) else []
    for fld in (
        "decision",
        "selected_level",
        "selected_provider",
        "input_strategy",
        "sync_allowed",
        "max_roi_count",
        "fallback_provider",
        "reason_codes",
        "estimated_latency_ms",
        "budget_impact",
        "evidence_required",
    ):
        if fld not in df:
            blockers.append(f"ocr_dispatch_decision_contract_missing_field:{fld}")

    pam = cfg.get("provider_admission_matrix_v0") if isinstance(cfg.get("provider_admission_matrix_v0"), dict) else {}
    decl = pam.get("required_declarations_per_provider") if isinstance(pam.get("required_declarations_per_provider"), list) else []
    for fld in (
        "provider_name",
        "provider_level",
        "supported_input_type",
        "supported_output_depth",
        "latency_class",
        "memory_class",
        "offline_capability",
        "remote_dependency",
        "privacy_risk",
        "fallback_policy",
        "evidence_contract_supported",
        "bridge_pack_supported",
    ):
        if fld not in decl:
            blockers.append(f"provider_admission_matrix_missing_declaration:{fld}")

    plrr = cfg.get("provider_level_response_requirements_v0") if isinstance(cfg.get("provider_level_response_requirements_v0"), dict) else {}
    for lk in ("level_0", "level_1", "level_2", "level_3"):
        if lk not in plrr or not isinstance(plrr.get(lk), dict):
            blockers.append(f"missing_provider_level_response_requirements:{lk}")

    rsp = cfg.get("runtime_selection_policy_v0") if isinstance(cfg.get("runtime_selection_policy_v0"), dict) else {}
    rules = rsp.get("rules") if isinstance(rsp.get("rules"), list) else []
    if len(rules) < 1:
        blockers.append("runtime_selection_policy_v0_must_have_rules")

    readme = repo / "docs/architecture/README.md"
    if not readme.is_file():
        blockers.append("missing_architecture_readme")
    else:
        rtxt = readme.read_text(encoding="utf-8")
        if "OCR Provider Runtime Governance Standard-001" not in rtxt and "LUNA_OCR_PROVIDER_RUNTIME_GOVERNANCE_STANDARD_V0" not in rtxt:
            blockers.append("readme_missing_governance_index")
        if re.search(r"PaddleOCR[^\n]{0,80}默认\s*runtime|默认\s*runtime[^\n]{0,40}PaddleOCR", rtxt, re.I):
            blockers.append("readme_suggests_paddleocr_as_default_runtime")

    gov = repo / "docs/architecture/ocr/LUNA_OCR_PROVIDER_RUNTIME_GOVERNANCE_STANDARD_V0.md"
    if gov.is_file():
        gtxt = gov.read_text(encoding="utf-8")
        if "逐帧" not in gtxt and "frame" not in gtxt.lower():
            blockers.append("governance_doc_missing_trigger_framing_concept")
        if re.search(r"PaddleOCR[^\n]{0,120}默认\s*(provider|主路径|runtime)", gtxt, re.I):
            blockers.append("governance_doc_suggests_paddleocr_as_default")
        if "OCRRequest" not in gtxt:
            blockers.append("governance_doc_missing_ocr_request_contract")
        if "OCRDispatchDecision" not in gtxt and "OCRExecutionPlan" not in gtxt:
            blockers.append("governance_doc_missing_dispatch_decision_contract")
        if "OCR Orchestrator" not in gtxt:
            blockers.append("governance_doc_missing_ocr_orchestrator")

    verdict = "NO_GO" if blockers else "GO"

    summary = {
        "schema": "ocr_provider_governance_standard_summary_v0",
        "phase": "Phase-OCR-Provider-Runtime-Governance-Standard-001",
        "verdict": verdict,
        "repo_root": str(repo),
        "output_root": str(out_root),
        "blockers": sorted(set(blockers)),
        "docs_checked": [str(d.relative_to(repo)) for d in docs],
        "config_example": rel_cfg if cfg_p.is_file() else None,
    }
    _write_json(out_root / "ocr_provider_governance_standard_summary.json", summary)
    _write_json(
        out_root / "ocr_provider_governance_standard_policy_matrix.json",
        {"rows": matrix, "config_keys_top": sorted(cfg.keys()) if cfg else []},
    )

    rep = {
        "schema": "ocr_provider_governance_standard_verifier_report_v0",
        "phase": "Phase-OCR-Provider-Runtime-Governance-Standard-001",
        "verdict": verdict,
        "output_root": str(out_root),
        "blockers": sorted(set(blockers)),
    }
    _write_json(out_root / "ocr_provider_governance_standard_verifier_report.json", rep)

    print(json.dumps({"verifier_output_root": str(out_root), "verdict": verdict, "blockers": rep["blockers"]}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
