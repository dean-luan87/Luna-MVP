#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-ModelOCR-010 — Read-only regression over Phase-009 OCR offline source policy evidence runs.
Does not modify product runtime.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
from typing import Any, Dict, List, Tuple

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from capabilities.model_ocr.offline_source_policy_v0 import (  # noqa: E402
    FORBIDDEN_DEFAULT_CHAIN_PROVIDERS,
    SOURCE_POLICY_ID_OCR_V0,
)

EXPECTED_NORMAL_SELECTED = "rapidocr_ppocrv4_mobile_onnx"
EXPECTED_FALLBACK_SELECTED = "rapidocr_current"
EXPECTED_FALLBACK_REASON = "rapidocr_ppocrv4_disabled"

REQUIRED_AUDIT_KEYS_TOP = (
    "source_policy_id",
    "policy_applied",
    "provider_attempt_order",
    "provider_selected",
    "fallback_used",
    "fallback_reason",
    "selection_audit",
)

REQUIRED_AUDIT_KEYS_SELECTION = (
    "source_policy_id",
    "offline_evaluation",
    "raw_text_only",
    "semantic_interpretation_enabled",
    "allows_execute_now",
    "real_tts_invoked",
    "downstream_invocation_count",
    "forbidden_semantic_output_count",
    "raw_text_candidate_schema_valid",
    "dependency_ready",
    "model_assets_status",
)


def _now_iso() -> str:
    return _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: str, obj: Any) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def _artifact_paths(root: str, provider_key: str) -> Tuple[str, str, str]:
    t = os.path.join(root, "trace", f"{provider_key}_trace.jsonl")
    r = os.path.join(root, "replay", f"{provider_key}_replay.jsonl")
    w = os.path.join(root, "whitebox", f"{provider_key}_whitebox.jsonl")
    return t, r, w


def _analyze_root(label: str, root: str) -> Dict[str, Any]:
    root = os.path.abspath(root)
    summ_path = os.path.join(root, "ocr_benchmark_summary.json")
    out: Dict[str, Any] = {"label": label, "root": root, "summary_path": summ_path, "readable": os.path.isfile(summ_path)}
    if not out["readable"]:
        out["error"] = "ocr_benchmark_summary.json_missing"
        return out

    s = _read_json(summ_path)
    out["summary"] = s
    sel = s.get("ocr_offline_source_selection") or {}
    pk = str(s.get("provider_selected") or sel.get("provider_selected") or "")

    tref, rref, wref = _artifact_paths(root, pk)
    out["provider_key_for_artifacts"] = pk
    out["trace_path"] = tref
    out["replay_path"] = rref
    out["whitebox_path"] = wref
    out["trace_exists"] = os.path.isfile(tref) and os.path.getsize(tref) > 0
    out["replay_exists"] = os.path.isfile(rref) and os.path.getsize(rref) > 0
    out["whitebox_exists"] = os.path.isfile(wref) and os.path.getsize(wref) > 0

    gov = s.get("governance") or {}
    out["governance_leakage"] = gov.get("governance_leakage", None)
    out["forbidden_provider_selected"] = pk in FORBIDDEN_DEFAULT_CHAIN_PROVIDERS

    return out


def _audit_matrix(normal: Dict[str, Any], fallback: Dict[str, Any]) -> Dict[str, Any]:
    n = normal.get("summary") or {}
    f = fallback.get("summary") or {}
    keys_n = set(n.keys())
    keys_f = set(f.keys())
    present_both = sorted(keys_n & keys_f)
    sa_n = n.get("selection_audit") or (n.get("ocr_offline_source_selection") or {}).get("selection_audit") or {}
    sa_f = f.get("selection_audit") or (f.get("ocr_offline_source_selection") or {}).get("selection_audit") or {}
    req_sa = {k: (k in sa_n and k in sa_f) for k in REQUIRED_AUDIT_KEYS_SELECTION}
    return {
        "required_top_level_policy_fields": {k: (k in keys_n and k in keys_f) for k in REQUIRED_AUDIT_KEYS_TOP},
        "required_selection_audit_fields_both": req_sa,
        "selection_audit_keys_normal": sorted(sa_n.keys()),
        "selection_audit_keys_fallback": sorted(sa_f.keys()),
        "overlap_summary_keys_count": len(present_both),
    }


def _hard_gates(normal: Dict[str, Any], fallback: Dict[str, Any]) -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []

    def add(name: str, ok: bool, detail: Any) -> None:
        checks.append({"check": name, "pass": bool(ok), "detail": detail})

    ns = normal.get("summary") or {}
    fs = fallback.get("summary") or {}

    add("normal_root_readable", normal.get("readable"), normal.get("root"))
    add("fallback_root_readable", fallback.get("readable"), fallback.get("root"))

    nsel = str(ns.get("provider_selected") or (ns.get("ocr_offline_source_selection") or {}).get("provider_selected") or "")
    nfu = ns.get("fallback_used")
    if nfu is None:
        nfu = (ns.get("ocr_offline_source_selection") or {}).get("fallback_used")

    fsel = str(fs.get("provider_selected") or (fs.get("ocr_offline_source_selection") or {}).get("provider_selected") or "")
    ffu = fs.get("fallback_used")
    if ffu is None:
        ffu = (fs.get("ocr_offline_source_selection") or {}).get("fallback_used")
    freason = fs.get("fallback_reason")
    if freason is None:
        freason = (fs.get("ocr_offline_source_selection") or {}).get("fallback_reason")

    n_pid = str(ns.get("source_policy_id") or (ns.get("ocr_offline_source_selection") or {}).get("source_policy_id") or "")
    n_pa = ns.get("policy_applied")
    if n_pa is None:
        n_pa = (ns.get("ocr_offline_source_selection") or {}).get("policy_applied")

    add("normal_provider_selected", nsel == EXPECTED_NORMAL_SELECTED, nsel)
    add("normal_fallback_used_false", nfu is False, nfu)
    add("fallback_provider_selected", fsel == EXPECTED_FALLBACK_SELECTED, fsel)
    add("fallback_fallback_used_true", ffu is True, ffu)
    add("fallback_reason", str(freason) == EXPECTED_FALLBACK_REASON, freason)
    add("source_policy_id", n_pid == SOURCE_POLICY_ID_OCR_V0, n_pid)
    add("policy_applied_true", n_pa is True, n_pa)

    ng = (ns.get("governance") or {}).get("governance_leakage", 0)
    fg = (fs.get("governance") or {}).get("governance_leakage", 0)
    add("governance_leakage_zero_both", ng == 0 and fg == 0, {"normal": ng, "fallback": fg})

    add("forbidden_not_selected_normal", not normal.get("forbidden_provider_selected"), nsel)
    add("forbidden_not_selected_fallback", not fallback.get("forbidden_provider_selected"), fsel)

    add("normal_trace_replay_whitebox", normal.get("trace_exists") and normal.get("replay_exists") and normal.get("whitebox_exists"), {})
    add("fallback_trace_replay_whitebox", fallback.get("trace_exists") and fallback.get("replay_exists") and fallback.get("whitebox_exists"), {})

    audit_ok = all(
        k in ns and k in fs for k in ("source_policy_id", "policy_applied", "provider_selected", "fallback_used")
    )
    add("required_audit_top_fields", audit_ok, list(REQUIRED_AUDIT_KEYS_TOP))

    all_pass = all(c["pass"] for c in checks)
    return {"all_pass": all_pass, "checks": checks}


def _boundary_summary() -> Dict[str, Any]:
    return {
        "product_runtime_modified": False,
        "closure_statement": "Phase-ModelOCR-010 is documentation + read-only regression only; no product runtime OCR default was changed.",
        "explicit_provider_mode_compatibility": "run_ocr_raw_text_benchmark_v0.py without --source-policy retains legacy multi-provider --providers behavior (Phase-009).",
        "forbidden_integrations_this_phase": [
            "yolo",
            "midplatform",
            "scenetask_fusion_output",
            "semantic_condensation",
            "navigation_execution",
            "real_tts",
            "controlled_live_stream",
            "option_a_expansion",
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--normal-root", required=True)
    ap.add_argument("--fallback-root", required=True)
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    out_root = os.path.abspath(args.output_root)
    os.makedirs(out_root, exist_ok=True)

    normal = _analyze_root("normal_009", args.normal_root)
    fallback = _analyze_root("fallback_009", args.fallback_root)

    matrix = {
        "normal": {k: normal[k] for k in normal if k not in ("summary",)},
        "fallback": {k: fallback[k] for k in fallback if k not in ("summary",)},
        "expected": {
            "source_policy_id": SOURCE_POLICY_ID_OCR_V0,
            "normal_provider_selected": EXPECTED_NORMAL_SELECTED,
            "fallback_provider_selected": EXPECTED_FALLBACK_SELECTED,
            "fallback_reason": EXPECTED_FALLBACK_REASON,
        },
    }
    # drop huge nested summary from matrix copy — keep refs only
    matrix["normal"]["summary_phase"] = (normal.get("summary") or {}).get("phase")
    matrix["fallback"]["summary_phase"] = (fallback.get("summary") or {}).get("phase")

    audit_matrix = _audit_matrix(normal, fallback)
    boundary = _boundary_summary()
    gates = _hard_gates(normal, fallback)

    regression_summary = {
        "phase": "Phase-ModelOCR-010",
        "tool": "run_ocr_offline_source_policy_regression_v0.py",
        "timestamp": _now_iso(),
        "input": {
            "normal_root": os.path.abspath(args.normal_root),
            "fallback_root": os.path.abspath(args.fallback_root),
            "source_policy_id": SOURCE_POLICY_ID_OCR_V0,
        },
        "hard_gates": gates,
        "verdict": "GO" if gates.get("all_pass") else "NO_GO",
        "governance_leakage_reported": {
            "normal": (normal.get("summary") or {}).get("governance", {}).get("governance_leakage"),
            "fallback": (fallback.get("summary") or {}).get("governance", {}).get("governance_leakage"),
        },
        "forbidden_provider_registry": sorted(FORBIDDEN_DEFAULT_CHAIN_PROVIDERS),
        "boundary": boundary,
        "explicit_provider_compatibility_note": boundary["explicit_provider_mode_compatibility"],
    }

    _write_json(os.path.join(out_root, "ocr_offline_source_policy_regression_summary.json"), regression_summary)
    _write_json(os.path.join(out_root, "ocr_offline_source_policy_regression_matrix.json"), matrix)
    _write_json(os.path.join(out_root, "ocr_offline_source_policy_audit_field_matrix.json"), audit_matrix)
    _write_json(os.path.join(out_root, "ocr_offline_source_policy_boundary_summary.json"), boundary)

    notes = "\n".join(
        [
            "# OCR Offline Source Policy Regression v0 (Phase-ModelOCR-010)",
            "",
            f"- **normal root:** `{args.normal_root}`",
            f"- **fallback root:** `{args.fallback_root}`",
            f"- **verdict:** `{regression_summary['verdict']}`",
            "",
            "## Hard gates",
            "",
            "```json",
            json.dumps(gates, ensure_ascii=False, indent=2),
            "```",
            "",
            "## Allowed to drift (metrics)",
            "",
            "- OCR accuracy, latency, exact match, bbox_iou — not gates for 010 closure.",
            "",
            "## Must not drift",
            "",
            "- Selected provider, fallback_reason, policy_id, governance_leakage, forbidden selections, audit presence, trace/replay/whitebox.",
            "",
        ]
    )
    with open(os.path.join(out_root, "regression_notes.md"), "w", encoding="utf-8") as f:
        f.write(notes)

    print(
        json.dumps(
            {"ok": True, "output_root": out_root, "verdict": regression_summary["verdict"], "all_pass": gates.get("all_pass")},
            ensure_ascii=False,
        )
    )
    return 0 if gates.get("all_pass") else 2


if __name__ == "__main__":
    raise SystemExit(main())
