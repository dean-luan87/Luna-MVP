#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for OCR provider selection smoke (Phase-OCR-Real-Provider-Adapter-Selection-001)."""

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
        "real_provider_invoked",
        "paddleocr_invoked",
        "rapidocr_replaced",
        "ocr_routing_changed",
        "midplatform_invoked",
        "world_model_written",
    ):
        if aud.get(k) is True:
            bad.append(f"audit_forbidden_true:{k}")
    return bad


def _audit_from_result(res: Dict[str, Any]) -> Dict[str, Any]:
    return res.get("audit") if isinstance(res.get("audit"), dict) else {}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []

    snap_p = root / "ocr_provider_registry_snapshot.json"
    sum_p = root / "ocr_provider_selection_smoke_summary.json"
    rep_p = root / "ocr_provider_selection_report.json"
    aud_p = root / "ocr_provider_selection_audit_report.json"
    ra_p = root / "ocr_provider_selection_case_a_result.json"
    rb_p = root / "ocr_provider_selection_case_b_result.json"
    rc_p = root / "ocr_provider_selection_case_c_result.json"

    for name, p in (
        ("registry_snapshot", snap_p),
        ("summary", sum_p),
        ("selection_report", rep_p),
        ("selection_audit", aud_p),
        ("case_a", ra_p),
        ("case_b", rb_p),
        ("case_c", rc_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{name}")

    if blockers:
        rep = {"schema": "ocr_provider_selection_verifier_report_v0", "smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}
        _write_json(root / "ocr_provider_selection_verifier_report.json", rep)
        print(json.dumps(rep, ensure_ascii=False))
        return 2

    snap = _read_json(snap_p)
    ra = _read_json(ra_p)
    rb = _read_json(rb_p)
    rc = _read_json(rc_p)
    rep = _read_json(rep_p) if rep_p.is_file() else {}

    provs = snap.get("providers") if isinstance(snap.get("providers"), list) else []
    if not provs:
        blockers.append("registry_snapshot_empty_providers")
    keys = {str(p.get("registry_key") or "") for p in provs if isinstance(p, dict)}
    if "ocr_stub" not in keys:
        blockers.append("registry_missing_ocr_stub")
    stub_row = next((p for p in provs if isinstance(p, dict) and p.get("registry_key") == "ocr_stub"), {})
    if stub_row.get("enabled") is not True:
        blockers.append("ocr_stub_must_be_enabled")
    for rk in ("paddleocr_candidate", "rapidocr_candidate"):
        row = next((p for p in provs if isinstance(p, dict) and p.get("registry_key") == rk), None)
        if row is None:
            blockers.append(f"registry_missing_{rk}")
        elif row.get("enabled") is True:
            blockers.append(f"{rk}_must_be_disabled_in_default_registry")

    if str(ra.get("status") or "") != "success":
        blockers.append("case_a_status_must_be_success")
    if str(rep.get("selected_provider") or "") != "ocr_stub":
        blockers.append("case_a_selected_provider_must_be_ocr_stub")
    if not isinstance(ra.get("provider_selection_report"), dict):
        blockers.append("case_a_missing_provider_selection_report")

    if str(rb.get("status") or "") != "success":
        blockers.append("case_b_status_must_be_success")
    aud_b = _audit_from_result(rb)
    if aud_b.get("fallback_to_stub") is not True:
        blockers.append("case_b_fallback_to_stub_must_be_true")

    if str(rc.get("status") or "") != "error":
        blockers.append("case_c_status_must_be_error_misconfiguration")
    if str(rc.get("error") or "") != "misconfiguration_paddle_runtime_without_real_provider":
        blockers.append("case_c_error_code_mismatch")

    for tag, res in (("case_a", ra), ("case_b", rb), ("case_c", rc)):
        blockers.extend([f"{tag}:{x}" for x in _forbidden_audit_true(_audit_from_result(res))])

    if _audit_from_result(ra).get("real_provider_invoked") is True:
        blockers.append("case_a_real_provider_invoked_must_be_false")
    if _audit_from_result(rb).get("real_provider_invoked") is True:
        blockers.append("case_b_real_provider_invoked_must_be_false")
    if _audit_from_result(rc).get("real_provider_invoked") is True:
        blockers.append("case_c_real_provider_invoked_must_be_false")

    aud_c = _audit_from_result(rc)
    if aud_c.get("paddleocr_runtime_provider_enabled") is not True:
        blockers.append("case_c_audit_must_record_paddle_runtime_enabled")

    verdict = "GO" if not blockers else "NO_GO"
    out_rep = {
        "schema": "ocr_provider_selection_verifier_report_v0",
        "phase": "Phase-OCR-Real-Provider-Adapter-Selection-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
    }
    _write_json(root / "ocr_provider_selection_verifier_report.json", out_rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
