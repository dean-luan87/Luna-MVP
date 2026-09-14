#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-ModelOCR-004A verifier for macOS Vision OCR raw text harness (v0).

Checks (A-L):
A. provider availability check
B. input video readable (if provided) OR output_root has per-sample results
C. raw text candidates schema valid
D. bbox present or explicitly null
E. confidence present or explicitly null
F. raw_text_joined present
G. allows_execute_now=false
H. semantic_interpretation_enabled=false
I. real_tts_invoked=false
J. downstream not invoked (summary governance)
K. trace/replay/whitebox files exist and non-empty
L. evidence boundary preserved (no fields that suggest navigation/semantics)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List


REPO_ROOT = os.path.abspath(os.environ.get("LUNA_REPO_ROOT") or os.getcwd())
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


FORBIDDEN_KEYS = {
    "navigation",
    "scene_task",
    "fusion",
    "output_action",
    "execute_action",
    "direction",
    "turn_left",
    "turn_right",
    "go_straight",
    "semantic_summary",
}


def _load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _schema_valid(sample: Dict[str, Any]) -> bool:
    if sample.get("provider_id") != "macos_vision_ocr_system_v0":
        return False
    if sample.get("model_config_id") != "macos_vision_ocr_system_v0":
        return False
    if sample.get("provider_method") not in ("vision_framework", "bridge", "unavailable"):
        return False
    if sample.get("semantic_interpretation_enabled") is not False:
        return False
    if sample.get("allows_execute_now") is not False:
        return False
    if sample.get("real_tts_invoked") is not False:
        return False
    if sample.get("raw_text_joined_strategy") not in ("model_order", "bbox_top_left", "empty", "unknown"):
        return False
    cands = sample.get("raw_text_candidates")
    if not isinstance(cands, list):
        return False
    for c in cands:
        if not isinstance(c, dict):
            return False
        for k in [
            "text_id",
            "text",
            "normalized_text",
            "bbox",
            "bbox_status",
            "confidence",
            "confidence_status",
            "frame_id",
            "timestamp_ms",
            "line_order",
            "allows_execute_now",
        ]:
            if k not in c:
                return False
        if c.get("bbox_status") not in ("present", "not_available"):
            return False
        if c.get("confidence_status") not in ("present", "not_available"):
            return False
        if c.get("bbox") is None and c.get("bbox_status") != "not_available":
            return False
        if c.get("bbox") is not None and c.get("bbox_status") != "present":
            return False
        if c.get("confidence") is None and c.get("confidence_status") != "not_available":
            return False
        if c.get("confidence") is not None and c.get("confidence_status") != "present":
            return False
        if c.get("allows_execute_now") is not False:
            return False
    if "raw_text_joined" not in sample:
        return False
    return True


def _has_bbox_declared(sample: Dict[str, Any]) -> bool:
    cands = sample.get("raw_text_candidates") if isinstance(sample.get("raw_text_candidates"), list) else []
    if cands == []:
        return True
    if any(isinstance(c, dict) and c.get("bbox") is not None for c in cands):
        return True
    return all(isinstance(c, dict) and c.get("bbox") is None for c in cands)


def _has_conf_declared(sample: Dict[str, Any]) -> bool:
    cands = sample.get("raw_text_candidates") if isinstance(sample.get("raw_text_candidates"), list) else []
    if cands == []:
        return True
    if any(isinstance(c, dict) and c.get("confidence") is not None for c in cands):
        return True
    return all(isinstance(c, dict) and c.get("confidence") is None for c in cands)


def _forbidden_key_scan(obj: Any) -> int:
    cnt = 0
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(k, str) and k.lower() in FORBIDDEN_KEYS:
                cnt += 1
            cnt += _forbidden_key_scan(v)
    elif isinstance(obj, list):
        for x in obj:
            cnt += _forbidden_key_scan(x)
    return cnt


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True, help="Output root produced by evaluate tool")
    args = ap.parse_args()

    out_root = os.path.abspath(os.path.join(REPO_ROOT, str(args.output_root))) if not os.path.isabs(str(args.output_root)) else os.path.abspath(str(args.output_root))

    # A. provider availability
    from capabilities.model_ocr.macos_vision_ocr_adapter_v0 import MacOSVisionOCRAdapterV0

    adapter = MacOSVisionOCRAdapterV0()
    avail, err = adapter.is_available()

    # Load artifacts
    summary_path = os.path.join(out_root, "ocr_raw_text_summary.json")
    per_path = os.path.join(out_root, "per_sample_ocr_raw_text_results.json")
    trace_path = os.path.join(out_root, "ocr_raw_text_trace.jsonl")
    replay_path = os.path.join(out_root, "ocr_raw_text_replay.jsonl")
    whitebox_path = os.path.join(out_root, "ocr_raw_text_whitebox.jsonl")

    hard_blockers: List[str] = []
    soft_followups: List[str] = []

    checks: Dict[str, Any] = {}
    checks["A_provider_available"] = {"ok": bool(avail), "error": err}

    if not os.path.exists(summary_path) or not os.path.exists(per_path):
        hard_blockers.append("missing_required_outputs")
        checks["B_outputs_present"] = {"ok": False}
        result = {"phase": "Phase-ModelOCR-004A", "verifier": "verify_macos_vision_ocr_raw_text_v0", "checks": checks, "hard_blockers": hard_blockers, "soft_followups": soft_followups}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2

    summary = _load_json(summary_path)
    per = _load_json(per_path)
    checks["B_outputs_present"] = {"ok": True, "summary": os.path.relpath(summary_path, REPO_ROOT), "per_sample": os.path.relpath(per_path, REPO_ROOT)}

    missing_input = bool((summary.get("input") or {}).get("missing_input_samples"))
    checks["B_input_readable_or_documented"] = {
        "ok": not missing_input,
        "missing_input_samples": missing_input,
        "reason": (summary.get("input") or {}).get("video_error") if isinstance(summary.get("input"), dict) else None,
    }
    if missing_input:
        hard_blockers.append("missing_input_samples")

    if not isinstance(per, list):
        hard_blockers.append("per_sample_not_list")
        per = []

    if len(per) == 0:
        hard_blockers.append("no_samples_in_output")

    schema_ok = sum(1 for s in per if isinstance(s, dict) and _schema_valid(s))
    bbox_ok = sum(1 for s in per if isinstance(s, dict) and _has_bbox_declared(s))
    conf_ok = sum(1 for s in per if isinstance(s, dict) and _has_conf_declared(s))
    joined_ok = sum(1 for s in per if isinstance(s, dict) and isinstance(s.get("raw_text_joined"), str))
    n = len(per) or 1

    checks["C_schema_valid_rate"] = {
        "ok": schema_ok == len(per),
        "valid": schema_ok,
        "total": len(per),
        "partial_ok": 0 < schema_ok < len(per),
    }
    checks["D_bbox_present_or_declared_rate"] = {"ok": bbox_ok == len(per), "ok_n": bbox_ok, "total": len(per)}
    checks["E_conf_present_or_declared_rate"] = {"ok": conf_ok == len(per), "ok_n": conf_ok, "total": len(per)}
    checks["F_raw_text_joined_present_rate"] = {"ok": joined_ok == len(per), "ok_n": joined_ok, "total": len(per)}

    # No per-sample hard_blockers (empty candidates are allowed; hard_blockers are not)
    hb_samples = [s.get("sample_id") for s in per if isinstance(s, dict) and (s.get("hard_blockers") or [])]
    checks["C2_per_sample_hard_blockers"] = {"ok": len(hb_samples) == 0, "count": len(hb_samples), "samples": hb_samples[:10]}
    if hb_samples:
        soft_followups.append(f"per_sample_hard_blockers_count:{len(hb_samples)}")

    # G/H/I governance
    checks["G_allows_execute_now_false"] = {"ok": all(isinstance(s, dict) and s.get("allows_execute_now") is False for s in per)}
    checks["H_semantic_interpretation_disabled"] = {"ok": all(isinstance(s, dict) and s.get("semantic_interpretation_enabled") is False for s in per)}
    checks["I_real_tts_invoked_false"] = {"ok": all(isinstance(s, dict) and s.get("real_tts_invoked") is False for s in per)}

    # J downstream not invoked
    downstream_ok = bool((summary.get("governance") or {}).get("downstream_invoked") is False) if isinstance(summary, dict) else False
    mic = (summary.get("metrics") or {}).get("downstream_invocation_count")
    mic_ok = mic in (None, 0)
    checks["J_downstream_not_invoked"] = {"ok": downstream_ok and mic_ok, "downstream_invoked": not downstream_ok, "downstream_invocation_count": mic}

    # K trace/replay/whitebox exist and non-empty
    def _non_empty(p: str) -> bool:
        return os.path.exists(p) and os.path.getsize(p) > 0

    checks["K_trace_files_present"] = {
        "ok": _non_empty(trace_path) and _non_empty(replay_path) and _non_empty(whitebox_path),
        "trace": _non_empty(trace_path),
        "replay": _non_empty(replay_path),
        "whitebox": _non_empty(whitebox_path),
    }

    # L forbidden semantic/nav fields scan (best-effort)
    forbidden_cnt = _forbidden_key_scan(summary) + _forbidden_key_scan(per)
    checks["L_forbidden_key_count"] = {"ok": forbidden_cnt == 0, "count": forbidden_cnt}

    # Hard blockers aggregation
    if forbidden_cnt > 0:
        hard_blockers.append("forbidden_semantic_nav_fields_detected")
    if not checks["A_provider_available"]["ok"]:
        hard_blockers.append("provider_unavailable")
    if schema_ok == 0 and len(per) > 0:
        hard_blockers.append("schema_invalid_all_samples")
    elif 0 < schema_ok < len(per):
        soft_followups.append(f"partial_schema_valid:{schema_ok}/{len(per)}")
    if not checks["K_trace_files_present"]["ok"]:
        hard_blockers.append("trace_files_missing_or_empty")
    if not checks["G_allows_execute_now_false"]["ok"] or not checks["H_semantic_interpretation_disabled"]["ok"] or not checks["I_real_tts_invoked_false"]["ok"]:
        hard_blockers.append("governance_invariant_failed")
    if not checks["J_downstream_not_invoked"]["ok"]:
        hard_blockers.append("downstream_invoked")

    # de-dupe stable order
    hard_blockers = list(dict.fromkeys(hard_blockers))

    if hard_blockers:
        verdict = "NO_GO"
    elif soft_followups:
        verdict = "CONDITIONAL_GO"
    else:
        verdict = "GO"

    result = {
        "phase": "Phase-ModelOCR-004A",
        "verifier": "verify_macos_vision_ocr_raw_text_v0",
        "output_root": os.path.relpath(out_root, REPO_ROOT) if out_root.startswith(REPO_ROOT) else out_root,
        "checks": checks,
        "verdict": verdict,
        "hard_blockers": hard_blockers,
        "soft_followups": soft_followups,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if verdict == "NO_GO" else 0


if __name__ == "__main__":
    raise SystemExit(main())

