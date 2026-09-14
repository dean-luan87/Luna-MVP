#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-STCM-Event-Skeleton-001 — Static verifier for STCM event skeleton + trace contract docs + registry JSON.

No model execution; no runtime wiring; no routing changes.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

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


REQUIRED_EVENT_TYPES: Set[str] = {
    "stcm_model_call_requested",
    "stcm_model_call_started",
    "stcm_model_call_completed",
    "stcm_model_call_timeout",
    "stcm_fallback_decision",
    "stcm_result_discarded",
    "stcm_voice_notice_requested",
    "stcm_voice_notice_dropped",
    "stcm_anchor_revalidated",
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=str(REPO_ROOT))
    ap.add_argument("--output-root", default="", help="Default: <repo-root>/_eval_out/stcm_event_skeleton_v0")
    args = ap.parse_args()

    repo = _require_repo(args.repo_root)
    if args.output_root.strip():
        out_root = Path(args.output_root).expanduser().resolve()
    else:
        out_root = (repo / "_eval_out" / "stcm_event_skeleton_v0").resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    blockers: List[str] = []
    type_matrix: List[Dict[str, Any]] = []
    fields_matrix: List[Dict[str, Any]] = []

    sk = repo / "docs/architecture/midplatform/LUNA_STCM_EVENT_SKELETON_AND_TRACE_CONTRACT_V0.md"
    if not sk.is_file():
        blockers.append("missing_event_skeleton_doc")
    else:
        skt = sk.read_text(encoding="utf-8")
        if not re.search(r"不.{0,20}接入\s*runtime|不接\s*runtime|不实装\s*runtime", skt, re.I):
            blockers.append("skeleton_doc_must_state_no_runtime_wiring")
        if re.search(r"已接\s*runtime|runtime\s*已接线|mainline\s*wired", skt, re.I):
            blockers.append("skeleton_doc_suggests_runtime_wired")

    reg_md = repo / "docs/architecture/midplatform/LUNA_STCM_EVENT_TYPE_REGISTRY_V0.md"
    if not reg_md.is_file():
        blockers.append("missing_event_type_registry_doc")

    eval_docs = [
        repo / "docs/architecture/evaluation/LUNA_EVALUATION_STCM_EVENT_SKELETON_V0.md",
        repo / "docs/architecture/evaluation/LUNA_EVALUATION_STCM_EVENT_SKELETON_GO_NO_GO_PACK_V0.md",
    ]
    for ed in eval_docs:
        if not ed.is_file():
            blockers.append(f"missing_eval_doc:{ed.name}")

    cfg_p = repo / "configs/midplatform/stcm_event_type_registry_v0.example.json"
    if not cfg_p.is_file():
        blockers.append("missing_event_registry_example_json")
        cfg: Dict[str, Any] = {}
    else:
        cfg = _read_json(cfg_p)
        if str(cfg.get("schema_version") or "") != "stcm_event_type_registry_v0":
            blockers.append("bad_registry_schema_version")
        et = cfg.get("event_types") if isinstance(cfg.get("event_types"), dict) else {}
        if len(et) < 9:
            blockers.append("event_types_count_below_9")
        for k in REQUIRED_EVENT_TYPES:
            if k not in et or not isinstance(et.get(k), dict):
                blockers.append(f"missing_event_type:{k}")
                continue
            rf = et[k].get("required_fields")
            if not isinstance(rf, list):
                blockers.append(f"required_fields_not_list:{k}")
                continue
            fs = set(str(x) for x in rf)
            for req in ("event_id", "event_type"):
                if req not in fs:
                    blockers.append(f"{k}_missing_{req}")
            if "trace_id" not in fs and "call_id" not in fs:
                blockers.append(f"{k}_missing_trace_or_call_id")
            fields_matrix.append({"event_type": k, "required_field_count": len(rf), "required_fields": sorted(fs)})
            type_matrix.append({"event_type": k, "defined": True, "description": str(et[k].get("description") or "")})

        to = et.get("stcm_model_call_timeout") or {}
        trf = set(str(x) for x in (to.get("required_fields") or []) if isinstance(to.get("required_fields"), list))
        if "notified_midplatform" not in trf:
            blockers.append("timeout_event_missing_notified_midplatform")

        vn = et.get("stcm_voice_notice_requested") or {}
        vrf = set(str(x) for x in (vn.get("required_fields") or []) if isinstance(vn.get("required_fields"), list))
        for fld in ("deadline_at", "expires_at"):
            if fld not in vrf:
                blockers.append(f"voice_notice_requested_missing_{fld}")

        rd = et.get("stcm_result_discarded") or {}
        rdf = set(str(x) for x in (rd.get("required_fields") or []) if isinstance(rd.get("required_fields"), list))
        if "discard_reason" not in rdf:
            blockers.append("result_discarded_missing_discard_reason")

        ar = et.get("stcm_anchor_revalidated") or {}
        arf = set(str(x) for x in (ar.get("required_fields") or []) if isinstance(ar.get("required_fields"), list))
        if "spatial_anchor_valid" not in arf:
            blockers.append("anchor_revalidated_missing_spatial_anchor_valid")

    readme = repo / "docs/architecture/README.md"
    if not readme.is_file():
        blockers.append("missing_architecture_readme")
    else:
        rtxt = readme.read_text(encoding="utf-8")
        if "STCM-Event-Skeleton-001" not in rtxt and "stcm_event_skeleton" not in rtxt.lower():
            blockers.append("readme_missing_stcm_event_skeleton_index")

    gaps = [
        {
            "gap_id": "STCM-EVENT-GAP-001",
            "description": "Map/Memory-specific STCM events deferred to later registry minor.",
            "severity": "low",
        },
        {
            "gap_id": "STCM-GAP-001",
            "description": "Inherited: OcrEvidencePack lacks pack-level observed_at/valid_until — completed events may need parallel trace fields.",
            "severity": "medium",
        },
        {
            "gap_id": "STCM-GAP-002",
            "description": "Inherited: Voice trace canonical IDs — align notice_id/call_id binding when unified export is frozen.",
            "severity": "low",
        },
    ]
    _write_json(out_root / "stcm_event_gap_report.json", {"gaps": gaps, "schema": "stcm_event_gap_report_v0"})

    verdict = "NO_GO" if blockers else "GO"

    summary = {
        "schema": "stcm_event_skeleton_summary_v0",
        "phase": "Phase-STCM-Event-Skeleton-001",
        "verdict": verdict,
        "repo_root": str(repo),
        "output_root": str(out_root),
        "blockers": sorted(set(blockers)),
        "event_type_count": len(cfg.get("event_types", {})) if isinstance(cfg.get("event_types"), dict) else 0,
    }
    _write_json(out_root / "stcm_event_skeleton_summary.json", summary)
    _write_json(out_root / "stcm_event_type_matrix.json", {"rows": type_matrix, "schema": "stcm_event_type_matrix_v0"})
    _write_json(
        out_root / "stcm_event_required_fields_matrix.json",
        {"rows": fields_matrix, "schema": "stcm_event_required_fields_matrix_v0"},
    )

    rep = {
        "schema": "stcm_event_skeleton_verifier_report_v0",
        "phase": "Phase-STCM-Event-Skeleton-001",
        "verdict": verdict,
        "output_root": str(out_root),
        "blockers": sorted(set(blockers)),
    }
    _write_json(out_root / "stcm_event_skeleton_verifier_report.json", rep)

    print(json.dumps({"verifier_output_root": str(out_root), "verdict": verdict, "blockers": rep["blockers"]}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
