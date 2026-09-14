#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for lightweight real OCR provider adapter smoke (Phase-OCR-Lightweight-Real-Provider-Adapter-001)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _forbidden_audit_true(aud: Dict[str, Any]) -> List[str]:
    bad: List[str] = []
    for k in (
        "paddleocr_invoked",
        "rapidocr_replaced",
        "ocr_routing_changed",
        "midplatform_invoked",
        "world_model_written",
    ):
        if aud.get(k) is True:
            bad.append(f"audit_forbidden_true:{k}")
    return bad


def _audit(res: Dict[str, Any]) -> Dict[str, Any]:
    return res.get("audit") if isinstance(res.get("audit"), dict) else {}


def _reasons(res: Dict[str, Any]) -> str:
    rep = res.get("provider_selection_report") if isinstance(res.get("provider_selection_report"), dict) else {}
    return "|".join(str(x) for x in (rep.get("provider_selection_reason_codes") or []))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []

    paths = {
        "summary": root / "ocr_lightweight_provider_adapter_smoke_summary.json",
        "registry": root / "ocr_lightweight_provider_registry_snapshot.json",
        "selection": root / "ocr_lightweight_provider_selection_report.json",
        "result": root / "ocr_lightweight_provider_result.json",
        "bridge": root / "ocr_lightweight_provider_bridge_pack.json",
        "audit": root / "ocr_lightweight_provider_audit_report.json",
        "notes": root / "ocr_lightweight_provider_notes.md",
        "case_a": root / "ocr_lightweight_provider_case_a_result.json",
        "case_c": root / "ocr_lightweight_provider_case_c_result.json",
        "case_d": root / "ocr_lightweight_provider_case_d_result.json",
    }
    for name, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{name}")

    if blockers:
        rep = {"schema": "ocr_lightweight_provider_verifier_report_v0", "smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}
        _write_json(root / "ocr_lightweight_provider_verifier_report.json", rep)
        print(json.dumps(rep, ensure_ascii=False))
        return 2

    ra = _read_json(paths["case_a"])
    rb = _read_json(paths["result"])
    rc = _read_json(paths["case_c"])
    rd = _read_json(paths["case_d"])
    snap = _read_json(paths["registry"])
    rep = _read_json(paths["selection"])
    bp = _read_json(paths["bridge"])
    aud_b = _read_json(paths["audit"])

    provs = snap.get("providers") if isinstance(snap.get("providers"), list) else []
    keys = {str(p.get("registry_key") or "") for p in provs if isinstance(p, dict)}
    for need in ("ocr_stub", "rapidocr_candidate", "paddleocr_candidate"):
        if need not in keys:
            blockers.append(f"registry_missing:{need}")
    paddle_row = next((p for p in provs if isinstance(p, dict) and p.get("registry_key") == "paddleocr_candidate"), {})
    if paddle_row.get("enabled") is True:
        blockers.append("paddleocr_candidate_must_stay_disabled")

    if str(ra.get("status") or "") != "success":
        blockers.append("case_a_must_success")
    if _audit(ra).get("selected_provider") != "ocr_stub":
        blockers.append("case_a_selected_must_be_stub")
    if _audit(ra).get("paddleocr_runtime_provider_enabled") is True:
        blockers.append("case_a_paddle_flag_must_be_false")

    if str(rb.get("status") or "") != "success":
        blockers.append("case_b_must_success")
    if not isinstance(bp, dict) or str(bp.get("schema_version") or "") != "ocr_evidence_pack_candidate_v0":
        blockers.append("case_b_bridge_pack_invalid")
    rb_aud = _audit(rb)
    invoked_b = rb_aud.get("real_provider_invoked") is True
    sel_b = str(rb_aud.get("selected_provider") or "")
    rs_b = _reasons(rb)
    if invoked_b:
        if sel_b != "rapidocr_candidate":
            blockers.append("case_b_when_invoked_selected_must_be_rapidocr_candidate")
        if rb.get("provider_result", {}).get("real_provider_invoked") is not True:
            blockers.append("case_b_provider_result_must_mark_real_invoke")
    else:
        if "provider_runtime_unavailable" not in rs_b and "lightweight_input_pack_rejected" not in rs_b and "import_failed" not in rs_b:
            blockers.append("case_b_stub_fallback_must_have_known_reason_in_selection_codes")

    if str(rc.get("status") or "") != "success":
        blockers.append("case_c_must_success_stub_fallback")
    if _audit(rc).get("real_provider_invoked") is True:
        blockers.append("case_c_must_not_invoke_real_when_forced_unavailable")
    if "provider_runtime_unavailable" not in _reasons(rc):
        blockers.append("case_c_must_contain_provider_runtime_unavailable")

    if _audit(rd).get("real_provider_invoked") is True:
        blockers.append("case_d_must_not_invoke_real_on_oversized_pack")
    if "edge_exceeds_lightweight_cap" not in _reasons(rd) and str(rd.get("status") or "") not in ("rejected",):
        blockers.append("case_d_expected_edge_reject_or_gate_reject")

    for tag, res in (("case_a", ra), ("case_b", rb), ("case_c", rc), ("case_d", rd)):
        blockers.extend([f"{tag}:{x}" for x in _forbidden_audit_true(_audit(res))])
    if aud_b.get("paddleocr_runtime_provider_enabled") is True:
        blockers.append("audit_paddle_flag_must_be_false")

    verdict = "GO" if not blockers else "NO_GO"
    out_rep = {
        "schema": "ocr_lightweight_provider_verifier_report_v0",
        "phase": "Phase-OCR-Lightweight-Real-Provider-Adapter-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
    }
    _write_json(root / "ocr_lightweight_provider_verifier_report.json", out_rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
