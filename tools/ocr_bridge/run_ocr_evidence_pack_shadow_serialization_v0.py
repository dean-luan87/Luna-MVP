#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-OCRBridge-Implementation-001 — Shadow serialization binding for OcrEvidencePackV0.

Reads OCR-007 eligibility outputs + Review-001 + RFC-001 log roots (paths only).
Does not call OCR providers or MidPlatform; does not mutate mainline runtime.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from capabilities.ocr_bridge.ocr_evidence_pack_shadow_serializer_v0 import (  # noqa: E402
    build_shadow_ocr_evidence_pack_v0,
    build_shadow_pack_trace_record_v0,
    read_env_flags_for_report_v0,
    read_routing_pack_from_eligibility_root_v0,
    resolve_boundary_eval_root_v0,
    serialize_ocr_evidence_pack_shadow_v0,
    validate_shadow_source_refs_v0,
)
from capabilities.ocr_bridge.ocr_evidence_pack_validator_v0 import validate_ocr_evidence_pack_v0  # noqa: E402
from capabilities.ocr_bridge.ocr_evidence_pack_contract_v0 import load_non_ocr_types_from_boundary_map_v0  # noqa: E402


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _append_jsonl(path: Path, row: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _read_json_if(path: Path) -> Any:
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--eligibility-gate-root", required=True)
    ap.add_argument("--bridge-review-root", required=True)
    ap.add_argument("--rfc-root", required=True)
    ap.add_argument("--boundary-eval-root", default="", help="Override boundary eval root")
    ap.add_argument("--output-root", default="")
    args = ap.parse_args()

    eg = _require_abs(args.eligibility_gate_root, "--eligibility-gate-root")
    br = _require_abs(args.bridge_review_root, "--bridge-review-root")
    rfc = _require_abs(args.rfc_root, "--rfc-root")
    boundary_root = resolve_boundary_eval_root_v0(eg, args.boundary_eval_root)

    if args.output_root.strip():
        out = _require_abs(args.output_root, "--output-root")
    else:
        stamp = _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%SZ")
        out = (Path.home() / "LunaRuntime" / "logs" / f"ocr_bridge_shadow_serialization_001_{stamp}").resolve()
    out.mkdir(parents=True, exist_ok=True)

    routing_pack = read_routing_pack_from_eligibility_root_v0(eg)
    envelope, pack, ref_initial = build_shadow_ocr_evidence_pack_v0(
        routing_pack=routing_pack,
        eligibility_gate_root=str(eg),
        boundary_eval_root=str(boundary_root),
        bridge_review_root=str(br),
        rfc_root=str(rfc),
    )

    non_ocr = load_non_ocr_types_from_boundary_map_v0(boundary_root / "ocr_capability_boundary_map.json")
    val = validate_ocr_evidence_pack_v0(pack=pack, non_ocr_types=non_ocr)

    ref_report = validate_shadow_source_refs_v0(pack=pack)
    ref_report["binding_refs"] = (ref_initial.get("binding_refs") or {}) if isinstance(ref_initial, dict) else {}

    missing = ref_report.get("missing_source_refs") or []
    forwarding_mode = str((pack.get("midplatform_contract") or {}).get("forwarding_mode") or "blocked")
    if missing and forwarding_mode == "eligible_text_only":
        forwarding_mode = "blocked"
        pack.setdefault("midplatform_contract", {})
        pack["midplatform_contract"]["forwarding_mode"] = "blocked"

    fwd_block = {
        "midplatform_forwarding_enabled": False,
        "fact_text_layer_enabled": False,
        "runtime_side_effect": False,
        "rationale": [
            "Phase-OCRBridge-Implementation-001 mandatory shadow bind",
            "no_midplatform_invocation",
            "raw_text_joined_must_not_be_sole_midplatform_input_per_freeze_docs",
        ],
        "missing_source_refs": missing,
        "effective_forwarding_mode": forwarding_mode,
    }

    shadow_doc = {
        "shadow_envelope": envelope,
        "pack": pack,
    }

    ts = _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    trace_path = out / "ocr_bridge_shadow_trace.jsonl"
    replay_path = out / "ocr_bridge_shadow_replay.jsonl"
    audit_path = out / "ocr_bridge_shadow_audit.jsonl"
    for p in (trace_path, replay_path, audit_path):
        if p.is_file():
            p.unlink()

    tr = build_shadow_pack_trace_record_v0(
        shadow_envelope=envelope,
        validation_passed=bool(val.get("validation_passed")),
        forwarding_mode=forwarding_mode,
    )
    tr["ts"] = ts
    _append_jsonl(trace_path, tr)

    _append_jsonl(
        replay_path,
        {
            "ts": ts,
            "shadow_pack_id": envelope.get("shadow_pack_id"),
            "pack_id": pack.get("pack_id"),
            "eligible_count": len(pack.get("eligible_text_evidence") or []),
            "routing_pack_id": routing_pack.get("routing_pack_id"),
        },
    )

    _append_jsonl(
        audit_path,
        {
            "ts": ts,
            "hard_audit": pack.get("hard_audit"),
            "validation_passed": val.get("validation_passed"),
            "forged_runtime_like_refs": ref_report.get("forged_runtime_like_refs"),
        },
    )

    review_summary = _read_json_if(br / "ocr_bridge_interface_freeze_summary.json")
    rfc_summary = _read_json_if(rfc / "ocr_bridge_runtime_binding_rfc_summary.json")

    summary = {
        "phase": "Phase-OCRBridge-Implementation-001",
        "eligibility_gate_root": str(eg),
        "bridge_review_root": str(br),
        "rfc_root": str(rfc),
        "boundary_eval_root": str(boundary_root),
        "output_root": str(out),
        "shadow_envelope": envelope,
        "validation_passed": val.get("validation_passed"),
        "constraints": {
            "ocr_provider_invoked": False,
            "midplatform_invoked": False,
            "scene_delta_invoked": False,
            "world_context_invoked": False,
            "world_write_invoked": False,
            "hive_upload_invoked": False,
            "qianwen_invoked": False,
            "tts_invoked": False,
            "playback_invoked": False,
            "mainline_routing_changed": False,
            "recommendation_engine_invoked": False,
        },
        "readiness_posture": "CONDITIONAL_GO_shadow_offline_binding_only",
        "verdict": "GO" if val.get("validation_passed") and not ref_report.get("forged_runtime_like_refs") else "CONDITIONAL_GO",
        "inputs": {
            "bridge_review_summary_present": review_summary is not None,
            "rfc_summary_present": rfc_summary is not None,
        },
        "env_flags_observed": read_env_flags_for_report_v0(),
        "recommended_defaults_note": "CLI-driven shadow run; do not auto-enable forward or fact layer via env in this phase.",
    }

    notes = out / "ocr_bridge_shadow_notes.md"
    notes.write_text(
        "\n".join(
            [
                "# OCR Bridge — Shadow OcrEvidencePack Serialization (Implementation-001)",
                "",
                f"- **eligibility_gate_root**: `{eg}`",
                f"- **bridge_review_root**: `{br}`",
                f"- **rfc_root**: `{rfc}`",
                f"- **boundary_eval_root**: `{boundary_root}`",
                f"- **output_root**: `{out}`",
                "",
                "- **Shadow only**: `source_ref_status=shadow_or_offline_ref`; no `runtime:` / `production:` / `midplatform:` forged refs.",
                f"- **validation_passed**: `{val.get('validation_passed')}`",
                "",
            ]
        ),
        encoding="utf-8",
    )

    _write_json(out / "ocr_evidence_pack_shadow_summary.json", summary)
    _write_json(out / "ocr_evidence_pack_shadow.json", serialize_ocr_evidence_pack_shadow_v0(shadow_envelope=envelope, pack=pack))
    _write_json(out / "ocr_evidence_pack_shadow_validation_report.json", val)
    _write_json(out / "ocr_evidence_pack_shadow_source_ref_report.json", ref_report)
    _write_json(out / "ocr_evidence_pack_shadow_forwarding_block_report.json", fwd_block)

    print(json.dumps({"output_root": str(out), "shadow_pack_id": envelope.get("shadow_pack_id")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
