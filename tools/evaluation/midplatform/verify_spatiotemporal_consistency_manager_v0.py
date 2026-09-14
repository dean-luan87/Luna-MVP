#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Spatiotemporal-Consistency-Manager-001 — Static verifier for STCM docs + example config.

No model execution; no routing changes; no MidPlatform runtime.
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
    ap.add_argument("--output-root", default="", help="Default: <repo-root>/_eval_out/spatiotemporal_consistency_manager_v0")
    args = ap.parse_args()

    repo = _require_repo(args.repo_root)
    if args.output_root.strip():
        out_root = Path(args.output_root).expanduser().resolve()
    else:
        out_root = (repo / "_eval_out" / "spatiotemporal_consistency_manager_v0").resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    blockers: List[str] = []
    matrix: List[Dict[str, Any]] = []

    docs = [
        repo / "docs/architecture/midplatform/LUNA_SPATIOTEMPORAL_CONSISTENCY_MANAGER_V0.md",
        repo / "docs/architecture/midplatform/LUNA_MODEL_CALL_DEADLINE_AND_TIMEOUT_POLICY_V0.md",
        repo / "docs/architecture/midplatform/LUNA_INFORMATION_VALUE_AND_FALLBACK_POLICY_V0.md",
        repo / "docs/architecture/midplatform/LUNA_CROSS_MODAL_TIME_SPACE_GOVERNANCE_V0.md",
        repo / "docs/architecture/evaluation/LUNA_EVALUATION_SPATIOTEMPORAL_CONSISTENCY_MANAGER_V0.md",
        repo / "docs/architecture/evaluation/LUNA_EVALUATION_SPATIOTEMPORAL_CONSISTENCY_MANAGER_GO_NO_GO_PACK_V0.md",
    ]
    for d in docs:
        try:
            rel = str(d.relative_to(repo))
        except ValueError:
            rel = str(d)
        matrix.append({"artifact": rel, "exists": d.is_file()})
        if not d.is_file():
            blockers.append(f"missing_doc:{d.name}")

    cfg_p = repo / "configs/midplatform/spatiotemporal_consistency_manager_v0.example.json"
    try:
        rel_cfg = str(cfg_p.relative_to(repo))
    except ValueError:
        rel_cfg = str(cfg_p)
    matrix.append({"artifact": rel_cfg, "exists": cfg_p.is_file()})
    if not cfg_p.is_file():
        blockers.append("missing_stcm_config_example")
        cfg: Dict[str, Any] = {}
    else:
        cfg = _read_json(cfg_p)

    if str(cfg.get("schema_version") or "") != "spatiotemporal_consistency_manager_v0":
        blockers.append("bad_schema_version")

    mcp = cfg.get("model_call_policy") if isinstance(cfg.get("model_call_policy"), dict) else {}
    if mcp.get("all_calls_require_deadline") is not True:
        blockers.append("model_call_policy_must_require_deadline")
    if mcp.get("all_outputs_require_spatiotemporal_anchor") is not True:
        blockers.append("model_call_policy_must_require_spatiotemporal_anchor")
    if mcp.get("expired_outputs_cannot_drive_action") is not True:
        blockers.append("model_call_policy_must_forbid_expired_driving_action")
    if mcp.get("timeout_must_notify_midplatform") is not True:
        blockers.append("model_call_policy_must_require_timeout_notify_midplatform")

    if not isinstance(cfg.get("deadline_classes"), dict) or not cfg.get("deadline_classes"):
        blockers.append("missing_deadline_classes")

    vnp = cfg.get("voice_notice_policy") if isinstance(cfg.get("voice_notice_policy"), dict) else {}
    if not vnp:
        blockers.append("missing_voice_notice_policy")

    readme = repo / "docs/architecture/README.md"
    if not readme.is_file():
        blockers.append("missing_architecture_readme")
    else:
        rtxt = readme.read_text(encoding="utf-8")
        if "Spatiotemporal Consistency Manager-001" not in rtxt and "STCM" not in rtxt:
            blockers.append("readme_missing_stcm_index")

    gov = repo / "docs/architecture/midplatform/LUNA_SPATIOTEMPORAL_CONSISTENCY_MANAGER_V0.md"
    if gov.is_file():
        gtxt = gov.read_text(encoding="utf-8")
        if "跨模态" not in gtxt:
            blockers.append("stcm_doc_missing_cross_modal_marker")
        if "Vision" not in gtxt and "视觉" not in gtxt:
            blockers.append("stcm_doc_missing_vision_coverage")
        if "Voice" not in gtxt and "语音" not in gtxt:
            blockers.append("stcm_doc_missing_voice_coverage")
        if "OCR" not in gtxt:
            blockers.append("stcm_doc_missing_ocr_coverage")
        if "不是 OCR 子模块" not in gtxt and "非 OCR 专属" not in gtxt:
            blockers.append("stcm_doc_must_reject_ocr_only_framing")
        if "过期" not in gtxt or ("行动" not in gtxt and "任务链" not in gtxt):
            blockers.append("stcm_doc_missing_expired_action_prohibition")
        if "超时" not in gtxt or "静默" not in gtxt or "任务链" not in gtxt:
            blockers.append("stcm_doc_missing_timeout_silent_task_chain_prohibition")

    cross = repo / "docs/architecture/midplatform/LUNA_CROSS_MODAL_TIME_SPACE_GOVERNANCE_V0.md"
    if cross.is_file():
        ctxt = cross.read_text(encoding="utf-8")
        for label, pat in (
            ("cross_modal_missing_ocr_section", r"##\s*1\.\s*OCR"),
            ("cross_modal_missing_vision_section", r"##\s*2\.\s*Vision"),
            ("cross_modal_missing_voice_section", r"##\s*3\.\s*Voice"),
        ):
            if not re.search(pat, ctxt):
                blockers.append(label)

    verdict = "NO_GO" if blockers else "GO"

    summary = {
        "schema": "spatiotemporal_consistency_manager_summary_v0",
        "phase": "Phase-Spatiotemporal-Consistency-Manager-001",
        "verdict": verdict,
        "repo_root": str(repo),
        "output_root": str(out_root),
        "blockers": sorted(set(blockers)),
        "docs_checked": [str(d.relative_to(repo)) for d in docs],
        "config_example": rel_cfg if cfg_p.is_file() else None,
    }
    _write_json(out_root / "spatiotemporal_consistency_manager_summary.json", summary)
    _write_json(
        out_root / "spatiotemporal_consistency_manager_policy_matrix.json",
        {"rows": matrix, "config_keys_top": sorted(cfg.keys()) if cfg else []},
    )
    rep = {
        "schema": "spatiotemporal_consistency_manager_verifier_report_v0",
        "phase": "Phase-Spatiotemporal-Consistency-Manager-001",
        "verdict": verdict,
        "output_root": str(out_root),
        "blockers": sorted(set(blockers)),
    }
    _write_json(out_root / "spatiotemporal_consistency_manager_verifier_report.json", rep)

    print(json.dumps({"verifier_output_root": str(out_root), "verdict": verdict, "blockers": rep["blockers"]}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
