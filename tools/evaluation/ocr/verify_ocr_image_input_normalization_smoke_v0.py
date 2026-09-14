#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for OCR image input normalization smoke (Phase-OCR-ImageInput-Normalization-Pipeline-001)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

WS_ROOT = Path(__file__).resolve().parents[3]
if str(WS_ROOT) not in sys.path:
    sys.path.insert(0, str(WS_ROOT))


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


def _case_entry(bundle: Any, case_id: str) -> Optional[Dict[str, Any]]:
    if not isinstance(bundle, dict):
        return None
    cases = bundle.get("cases")
    if not isinstance(cases, list):
        return None
    for c in cases:
        if isinstance(c, dict) and str(c.get("case_id")) == case_id:
            return c
    return None


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


def _validate_transform(t: Dict[str, Any]) -> List[str]:
    errs: List[str] = []
    for k in ("original_width", "original_height", "transformed_width", "transformed_height", "scale_x", "scale_y"):
        if k not in t:
            errs.append(f"transform_missing:{k}")
    return errs


def _validate_pack(pack: Dict[str, Any]) -> List[str]:
    from capabilities.ocr_runtime.ocr_provider_input_pack_v0 import validate_provider_input_pack_v0

    return validate_provider_input_pack_v0(pack)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []
    soft: List[str] = []

    probe_p = root / "ocr_image_metadata_probe.json"
    dec_p = root / "ocr_image_input_decision.json"
    pack_p = root / "ocr_provider_input_pack.json"
    mtx_p = root / "ocr_coordinate_transform_matrix.json"
    aud_p = root / "ocr_image_input_normalization_audit_report.json"
    sum_p = root / "ocr_image_input_normalization_summary.json"

    for name, p in (
        ("metadata_probe", probe_p),
        ("input_decision", dec_p),
        ("provider_input_pack_bundle", pack_p),
        ("coordinate_transform_bundle", mtx_p),
        ("audit_report", aud_p),
        ("summary", sum_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{name}")

    if blockers:
        verdict = "NO_GO"
        rep = {
            "schema": "ocr_image_input_normalization_verifier_report_v0",
            "phase": "Phase-OCR-ImageInput-Normalization-Pipeline-001",
            "smoke_root": str(root),
            "verdict": verdict,
            "blockers": blockers,
            "soft_notes": soft,
        }
        _write_json(root / "ocr_image_input_normalization_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
        return 2

    probe_b = _read_json(probe_p)
    dec_b = _read_json(dec_p)
    pack_b = _read_json(pack_p)
    mtx_b = _read_json(mtx_p)
    aud_b = _read_json(aud_p)

    def _must_probe(cid: str) -> Dict[str, Any]:
        ce = _case_entry(probe_b, cid)
        pr = ce.get("probe") if isinstance(ce, dict) else None
        if not isinstance(pr, dict) or not pr.get("width") or not pr.get("height"):
            blockers.append(f"{cid}:missing_or_invalid_probe")
            return {}
        return pr

    def _must_dec(cid: str) -> Dict[str, Any]:
        ce = _case_entry(dec_b, cid)
        d = ce.get("decision") if isinstance(ce, dict) else None
        if not isinstance(d, dict):
            blockers.append(f"{cid}:missing_decision")
            return {}
        return d

    def _must_pack(cid: str) -> Optional[Dict[str, Any]]:
        ce = _case_entry(pack_b, cid)
        pk = ce.get("pack") if isinstance(ce, dict) else None
        if pk is None:
            return None
        if not isinstance(pk, dict):
            blockers.append(f"{cid}:invalid_pack_type")
            return None
        return pk

    def _must_mtx(cid: str) -> Dict[str, Any]:
        ce = _case_entry(mtx_b, cid)
        mx = ce.get("matrix") if isinstance(ce, dict) else None
        if not isinstance(mx, dict):
            blockers.append(f"{cid}:missing_coordinate_matrix")
            return {}
        return mx

    def _result_json(cid: str) -> Dict[str, Any]:
        p = root / cid / "ocr_mainline_bridge_result.json"
        if not p.is_file():
            blockers.append(f"{cid}:missing_bridge_result")
            return {}
        r = _read_json(p)
        return r if isinstance(r, dict) else {}

    _must_probe("small")
    _must_probe("large")
    _must_dec("small")
    _must_dec("large")

    small_pack = _must_pack("small")
    large_pack = _must_pack("large")

    small_res = _result_json("small")
    large_res = _result_json("large")

    if small_pack is None and str(small_res.get("status")) != "rejected":
        blockers.append("small:missing_provider_pack_when_not_rejected")
    if large_pack is None and str(large_res.get("status")) != "rejected":
        blockers.append("large:missing_provider_pack_when_not_rejected")

    def _check_pack_deep(cid: str, pack: Optional[Dict[str, Any]], res: Dict[str, Any]) -> None:
        if pack is None:
            return
        blockers.extend([f"{cid}:pack:{e}" for e in _validate_pack(pack)])
        pol = pack.get("processing_policy") if isinstance(pack.get("processing_policy"), dict) else {}
        strat = str(pol.get("strategy") or "")
        if not strat:
            blockers.append(f"{cid}:missing_processing_strategy")
        schain = pack.get("source_chain")
        if not isinstance(schain, list) or len(schain) < 2:
            blockers.append(f"{cid}:source_chain_incomplete")
        elif "build_provider_input_pack" not in schain:
            blockers.append(f"{cid}:source_chain_missing_pack_marker")
        units = pack.get("input_units")
        if not isinstance(units, list) or not units:
            blockers.append(f"{cid}:input_units_empty")
        ct = pack.get("coordinate_transform")
        if not isinstance(ct, dict):
            blockers.append(f"{cid}:pack_coordinate_transform_missing")
        else:
            blockers.extend([f"{cid}:pack_ct:{e}" for e in _validate_transform(ct)])
        p_audit = pack.get("audit") if isinstance(pack.get("audit"), dict) else {}
        blockers.extend([f"{cid}:pack_audit:{x}" for x in _forbidden_audit_true(p_audit)])

    _check_pack_deep("small", small_pack, small_res)
    _check_pack_deep("large", large_pack, large_res)

    def _policy(pack: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        if not isinstance(pack, dict):
            return {}
        pol = pack.get("processing_policy")
        return pol if isinstance(pol, dict) else {}

    small_pol = _policy(small_pack)
    small_strat = str(small_pol.get("strategy") or "")
    if small_strat not in ("full_image_allowed", "roi_only_stub"):
        soft.append(f"small:unexpected_strategy:{small_strat}")

    large_pol = _policy(large_pack)
    large_strat = str(large_pol.get("strategy") or "")
    if large_strat not in ("downscale", "tile_required", "async"):
        soft.append(f"large:unexpected_strategy:{large_strat}")

    large_ig = large_res.get("input_gate") if isinstance(large_res.get("input_gate"), dict) else {}
    if not bool(large_ig.get("oversized")):
        blockers.append("large:expected_oversized_true")

    large_aud = large_res.get("audit") if isinstance(large_res.get("audit"), dict) else {}
    if not large_aud and isinstance(aud_b, dict):
        large_aud = aud_b.get("large") if isinstance(aud_b.get("large"), dict) else {}
    if large_aud.get("original_image_used_directly") is True:
        blockers.append("large:must_not_use_original_image_directly")

    if large_aud.get("downscale_applied") is True:
        lmx = _must_mtx("large")
        units = lmx.get("units") if isinstance(lmx.get("units"), list) else []
        if not units or not isinstance(units[0], dict):
            blockers.append("large:coordinate_matrix_units_missing")
        else:
            blockers.extend([f"large:mtx:{e}" for e in _validate_transform(units[0])])

    prov = large_res.get("provider_result") if isinstance(large_res.get("provider_result"), dict) else {}
    if str(large_res.get("status")) == "success" and not str(prov.get("input_pack_id") or "").strip():
        blockers.append("large:stub_must_consume_input_pack")

    sprov = small_res.get("provider_result") if isinstance(small_res.get("provider_result"), dict) else {}
    if str(small_res.get("status")) == "success" and not str(sprov.get("input_pack_id") or "").strip():
        blockers.append("small:stub_must_consume_input_pack")

    blockers.extend([f"small:audit:{x}" for x in _forbidden_audit_true(small_res.get("audit") if isinstance(small_res.get("audit"), dict) else {})])
    blockers.extend([f"large:audit:{x}" for x in _forbidden_audit_true(large_aud)])

    if str(small_res.get("status")) != "success":
        blockers.append("small:expected_success")
    if str(large_res.get("status")) != "success":
        blockers.append("large:expected_success")

    verdict: str = "GO" if not blockers else "NO_GO"

    rep = {
        "schema": "ocr_image_input_normalization_verifier_report_v0",
        "phase": "Phase-OCR-ImageInput-Normalization-Pipeline-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "ocr_image_input_normalization_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers, "soft_notes": soft}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
