#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Phase-012-Fix RapidOCR 12-sample batch regression artifacts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

INCLUDE_RE = re.compile(r"^ocr_([1-9]|1[0-2])\.(png|jpg|jpeg|webp)$", re.IGNORECASE)


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _nonempty_file(path: Path) -> bool:
    try:
        return path.is_file() and bool(path.read_text(encoding="utf-8").strip())
    except Exception:
        return False


def _case(name: str, ok: bool, details: Dict[str, Any]) -> Dict[str, Any]:
    return {"case": name, "ok": bool(ok), "details": details}


def _collect_hard_audits(per_sample: Path) -> Tuple[List[Dict[str, Any]], List[str]]:
    audits: List[Dict[str, Any]] = []
    errors: List[str] = []
    if not per_sample.is_dir():
        return audits, ["per_sample_missing"]
    for sub in sorted(per_sample.iterdir()):
        if not sub.is_dir() or not sub.name.startswith("011_"):
            continue
        wb = sub / "ocr_stage2_controlled_provider_whitebox.jsonl"
        if not _nonempty_file(wb):
            errors.append(f"missing_whitebox:{sub.name}")
            continue
        try:
            line = wb.read_text(encoding="utf-8").strip().splitlines()[-1]
            ha = json.loads(line).get("hard_audit") or {}
            audits.append(ha if isinstance(ha, dict) else {})
        except Exception as e:
            errors.append(f"parse_fail:{sub.name}:{e!r}")
    return audits, errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    outp = Path(args.output_root).expanduser()
    if not outp.is_absolute():
        raise SystemExit("ERROR: --output-root must be absolute")
    out_root = outp.resolve()

    results: List[Dict[str, Any]] = []
    results.append(_case("A_output_exists", out_root.is_dir(), {"output_root": str(out_root)}))

    sum_path = out_root / "batch_summary.json"
    tsv_path = out_root / "batch_report.tsv"
    results.append(_case("B_batch_summary_exists", sum_path.is_file(), {"path": str(sum_path)}))
    results.append(_case("C_batch_report_tsv_exists", tsv_path.is_file(), {"path": str(tsv_path)}))

    summary = _read_json(sum_path) if sum_path.is_file() else {}

    sf = summary.get("sample_filter") if isinstance(summary.get("sample_filter"), dict) else {}
    results.append(_case("D_sample_filter_present", bool(sf), {}))

    expected = int(sf.get("expected_count") or 12)
    actual = int(sf.get("actual_count") or -1)
    results.append(_case("E_expected_count_12", expected == 12, {"expected_count": expected}))
    results.append(_case("F_actual_count_12", actual == 12, {"actual_count": actual}))

    included = summary.get("included_samples") if isinstance(summary.get("included_samples"), list) else []
    no_stage2 = not any(str(n).startswith("ocr_stage2") for n in included)
    regex_ok = len(included) == 12 and all(isinstance(n, str) and INCLUDE_RE.match(n) for n in included)
    results.append(_case("G_no_ocr_stage2_star_in_included", no_stage2 and regex_ok, {"included_samples": included}))

    per_sample = out_root / "per_sample"
    audits, wb_errs = _collect_hard_audits(per_sample)

    all_rapid = True
    for sub in sorted(per_sample.iterdir()) if per_sample.is_dir() else []:
        if not sub.is_dir() or not sub.name.startswith("011_"):
            continue
        sp = sub / "ocr_stage2_provider_selection.json"
        if not sp.is_file():
            all_rapid = False
            continue
        ps = str(_read_json(sp).get("provider_selected") or "")
        if "rapidocr" not in ps.lower():
            all_rapid = False
        if "macos_vision" in ps.lower():
            all_rapid = False

    n011 = (
        len([x for x in per_sample.iterdir() if x.is_dir() and x.name.startswith("011_")])
        if per_sample.is_dir()
        else 0
    )
    results.append(
        _case(
            "H_provider_all_rapidocr",
            all_rapid and len(audits) == n011,
            {"whitebox_errors": wb_errs, "n011": n011},
        )
    )

    def _all_ha(pred) -> bool:
        return bool(audits) and all(pred(a) for a in audits)

    results.append(_case("I_network_false", _all_ha(lambda a: a.get("network_request_invoked") is False), {"n": len(audits)}))
    results.append(
        _case("J_semantic_false", _all_ha(lambda a: a.get("semantic_interpretation_enabled") is False), {"n": len(audits)})
    )
    results.append(_case("K_midplatform_false", _all_ha(lambda a: a.get("midplatform_invoked") is False), {"n": len(audits)}))
    results.append(_case("L_scene_delta_false", _all_ha(lambda a: a.get("scene_delta_invoked") is False), {"n": len(audits)}))
    results.append(_case("M_world_ctx_false", _all_ha(lambda a: a.get("world_context_invoked") is False), {"n": len(audits)}))
    results.append(_case("N_qwen_false", _all_ha(lambda a: a.get("qwen_invoked") is False), {"n": len(audits)}))
    results.append(_case("O_real_tts_false", _all_ha(lambda a: a.get("real_tts_invoked") is False), {"n": len(audits)}))
    results.append(_case("P_playback_false", _all_ha(lambda a: a.get("playback_invoked") is False), {"n": len(audits)}))
    results.append(
        _case(
            "Q_downstream_zero",
            _all_ha(lambda a: (a.get("downstream_invocation_count") or 0) == 0),
            {"n": len(audits)},
        )
    )
    results.append(
        _case(
            "R_navigation_null",
            _all_ha(lambda a: a.get("navigation_action") in (None, "null")),
            {"n": len(audits)},
        )
    )
    results.append(_case("S_world_write_false", _all_ha(lambda a: a.get("world_write_invoked") is False), {"n": len(audits)}))
    results.append(_case("T_hive_false", _all_ha(lambda a: a.get("hive_upload_invoked") is False), {"n": len(audits)}))

    for fname in (
        "ocr_stage2_batch_rapidocr_trace.jsonl",
        "ocr_stage2_batch_rapidocr_replay.jsonl",
        "ocr_stage2_batch_rapidocr_whitebox.jsonl",
    ):
        p = out_root / fname
        results.append(_case(f"U_{fname}", _nonempty_file(p), {"path": str(p)}))

    bv = summary.get("batch_verdict")
    results.append(_case("V_batch_verdict_present", bv in {"GO", "CONDITIONAL_GO", "NO_GO"}, {"batch_verdict": bv}))
    results.append(_case("W_011_dirs_match_actual_count", n011 == actual, {"n011": n011, "actual_count": actual}))

    all_ok = all(r["ok"] for r in results)
    bv_str = str(bv or "")
    if bv_str == "GO" and all_ok:
        verdict = "GO"
    elif bv_str == "NO_GO" or not all_ok:
        verdict = "NO_GO"
    else:
        verdict = "CONDITIONAL_GO"

    exit_code = 0 if verdict == "GO" else (1 if verdict == "CONDITIONAL_GO" else 2)

    print(
        json.dumps(
            {
                "verifier": "verify_ocr_stage2_batch_rapidocr_eval_v0",
                "verdict": verdict,
                "batch_verdict": bv,
                "output_root": str(out_root),
                "hard_blockers": [r["case"] for r in results if not r["ok"]],
                "results": results,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
