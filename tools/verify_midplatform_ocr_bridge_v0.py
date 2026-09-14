#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import json
import os
from typing import Any, Dict, List

REPO_ROOT = os.path.abspath(os.environ.get("LUNA_REPO_ROOT") or os.getcwd())
if REPO_ROOT not in __import__("sys").path:
    __import__("sys").path.insert(0, REPO_ROOT)


def _read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _read_jsonl_lines(path: str) -> List[Dict[str, Any]]:
    if not os.path.isfile(path):
        return []
    rows: List[Dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception:
                continue
    return rows


def _case(name: str, ok: bool, details: Any = None) -> Dict[str, Any]:
    return {"case": name, "ok": bool(ok), "details": details}


def _scan_for_forbidden_nonnull(obj: Any, forbidden_keys: List[str]) -> Dict[str, int]:
    # Counts occurrences of forbidden keys with non-null values.
    counts = {k: 0 for k in forbidden_keys}

    def rec(x: Any) -> None:
        if isinstance(x, dict):
            for k, v in x.items():
                if isinstance(k, str) and k in forbidden_keys and v is not None:
                    counts[k] += 1
                rec(v)
        elif isinstance(x, list):
            for it in x:
                rec(it)

    rec(obj)
    return counts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    out_root = args.output_root if os.path.isabs(args.output_root) else os.path.abspath(os.path.join(REPO_ROOT, args.output_root))

    required_files = [
        "midplatform_ocr_bridge_summary.json",
        "midplatform_ocr_evidence_inputs.json",
        "scene_delta_control_results.json",
        "filter_results.json",
        "midplatform_text_extraction_candidates.json",
        "world_context_evidence_candidates.json",
        "ambient_context_candidates.json",
        "midplatform_ocr_bridge_trace.jsonl",
        "midplatform_ocr_bridge_replay.jsonl",
        "midplatform_ocr_bridge_whitebox.jsonl",
        "evaluation_notes.md",
    ]

    results: List[Dict[str, Any]] = []
    missing = [f for f in required_files if not os.path.isfile(os.path.join(out_root, f))]
    results.append(_case("A_outputs_present", len(missing) == 0, {"missing": missing}))
    if missing:
        verdict = "NO_GO"
        hard_blockers = missing
        report = {"verifier": "verify_midplatform_ocr_bridge_v0", "verdict": verdict, "hard_blockers": hard_blockers, "results": results}
        print(json.dumps(report, ensure_ascii=False, indent=2))
        with open(os.path.join(out_root, "verification_result.json"), "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        return 2

    summary = _read_json(os.path.join(out_root, "midplatform_ocr_bridge_summary.json"))
    evidence_inputs = _read_json(os.path.join(out_root, "midplatform_ocr_evidence_inputs.json"))
    delta_results = _read_json(os.path.join(out_root, "scene_delta_control_results.json"))
    filter_results = _read_json(os.path.join(out_root, "filter_results.json"))
    text_candidates = _read_json(os.path.join(out_root, "midplatform_text_extraction_candidates.json"))
    world_candidates = _read_json(os.path.join(out_root, "world_context_evidence_candidates.json"))
    ambient_candidates = _read_json(os.path.join(out_root, "ambient_context_candidates.json"))

    trace_rows = _read_jsonl_lines(os.path.join(out_root, "midplatform_ocr_bridge_trace.jsonl"))
    replay_rows = _read_jsonl_lines(os.path.join(out_root, "midplatform_ocr_bridge_replay.jsonl"))
    whitebox_rows = _read_jsonl_lines(os.path.join(out_root, "midplatform_ocr_bridge_whitebox.jsonl"))

    # B evidence inputs schema (contract boundary)
    ok_evidence = True
    if not isinstance(evidence_inputs, list):
        ok_evidence = False
    else:
        for ev in evidence_inputs:
            if not isinstance(ev, dict):
                ok_evidence = False
                break
            if ev.get("candidate_only") is not True:
                ok_evidence = False
                break
            if ev.get("semantic_interpretation_enabled") is not False:
                ok_evidence = False
                break
            if ev.get("allows_execute_now") is not False:
                ok_evidence = False
                break
            if ev.get("real_tts_invoked") is not False:
                ok_evidence = False
                break
            if int(ev.get("downstream_invocation_count") or 0) != 0:
                ok_evidence = False
                break
            if not ev.get("trace_ref"):
                ok_evidence = False
                break
            if not ev.get("whitebox_ref"):
                ok_evidence = False
                break
    results.append(_case("B_evidence_inputs_schema", ok_evidence, {"evidence_count": len(evidence_inputs) if isinstance(evidence_inputs, list) else None}))

    # C delta control
    ok_delta = isinstance(delta_results, list) and len(delta_results) > 0
    if ok_delta:
        for d in delta_results:
            if not isinstance(d, dict):
                ok_delta = False
                break
            for k in ("crop_signature", "text_signature", "layout_signature", "object_signature", "delta_status", "delta_decision", "change_summary"):
                if k not in d:
                    ok_delta = False
                    break
            if not d.get("delta_control_id"):
                ok_delta = False
                break
    results.append(_case("C_delta_control_generated", ok_delta, {"delta_count": len(delta_results) if isinstance(delta_results, list) else None}))

    # D filter results
    ok_filter = isinstance(filter_results, list) and len(filter_results) > 0
    if ok_filter:
        for fr in filter_results:
            if not isinstance(fr, dict):
                ok_filter = False
                break
            for k in (
                "filter_result_id",
                "evidence_id",
                "visual_text_relevance_class",
                "block_applied",
                "block_level",
                "block_reason",
                "retained_evidence_ref",
                "eligible_for_recheck",
                "allowed_to_task_candidate",
                "allowed_for_primary_task_decision",
                "allowed_for_ambient_context_candidate",
                "ambient_context_candidate_context_type",
                "trace_ref",
                "whitebox_ref",
            ):
                if k not in fr:
                    ok_filter = False
                    break
    results.append(_case("D_filter_results_generated", ok_filter, {"filter_count": len(filter_results) if isinstance(filter_results, list) else None}))

    # E candidates boundary constraints
    ok_text = True
    if not isinstance(text_candidates, list):
        ok_text = False
    else:
        for c in text_candidates:
            if not isinstance(c, dict):
                ok_text = False
                break
            if c.get("candidate_only") is not True:
                ok_text = False
                break
            if c.get("semantic_summary") is not None:
                ok_text = False
                break
            if c.get("navigation_action") is not None:
                ok_text = False
                break
            if c.get("allows_execute_now") is not False:
                ok_text = False
                break
    results.append(_case("E_text_candidates_contract", ok_text, {"text_candidate_count": len(text_candidates) if isinstance(text_candidates, list) else None}))

    ok_world = True
    if not isinstance(world_candidates, list):
        ok_world = False
    else:
        for w in world_candidates:
            if not isinstance(w, dict):
                ok_world = False
                break
            if "observed_at" not in w or "observed_where" not in w or "trust" not in w or "lifecycle" not in w or "world_model_policy" not in w:
                ok_world = False
                break
            if "timestamp_ms" not in w["observed_at"]:
                ok_world = False
                break
            if "spatial_anchor_type" not in w["observed_where"]:
                ok_world = False
                break
            for k in ("trust_score", "cross_validation_status", "fraud_risk_status"):
                if k not in w["trust"]:
                    ok_world = False
                    break
            for k in ("ttl_policy", "expires_at", "requires_revalidation", "evidence_status"):
                if k not in w["lifecycle"]:
                    ok_world = False
                    break
            if w["world_model_policy"].get("shareable_to_hive") is not False:
                ok_world = False
                break
            if w["world_model_policy"].get("requires_user_confirmation") is not False:
                ok_world = False
                break
    results.append(_case("F_world_context_candidates_contract", ok_world, {"world_context_count": len(world_candidates) if isinstance(world_candidates, list) else None}))

    ok_ambient = True
    if not isinstance(ambient_candidates, list):
        ok_ambient = False
    else:
        for a in ambient_candidates:
            if not isinstance(a, dict):
                ok_ambient = False
                break
            if a.get("navigation_action") is not None:
                ok_ambient = False
                break
            if a.get("allowed_for_primary_task_decision") is not False:
                ok_ambient = False
                break
            if a.get("allowed_for_experience_enrichment") is not True:
                ok_ambient = False
                break
            if a.get("expiry_policy") != "short_ttl":
                ok_ambient = False
                break
            if a.get("requires_revalidation") is not True:
                ok_ambient = False
                break
    results.append(_case("G_ambient_context_candidates_contract", ok_ambient, {"ambient_count": len(ambient_candidates) if isinstance(ambient_candidates, list) else None}))

    # F files present + non-empty
    ok_trace = len(trace_rows) > 0 and len(replay_rows) > 0 and len(whitebox_rows) > 0
    results.append(_case("H_trace_replay_whitebox_nonempty", ok_trace, {"trace": len(trace_rows), "replay": len(replay_rows), "whitebox": len(whitebox_rows)}))

    ok_whitebox = True
    if ok_trace:
        for wb in whitebox_rows:
            if not isinstance(wb, dict):
                ok_whitebox = False
                break
            for k in ("why_relevance_class", "why_world_context_written", "why_ambient_context_created", "why_blocked", "governance_boundary_status", "confidence_thresholds"):
                if k not in wb:
                    ok_whitebox = False
                    break
    results.append(_case("I_whitebox_fields_present", ok_whitebox, {}))

    # Forbidden non-null check
    forbidden_nonnull_keys = ["navigation_action", "semantic_summary"]
    forbidden_counts = _scan_for_forbidden_nonnull(
        {
            "evidence_inputs": evidence_inputs,
            "text_candidates": text_candidates,
            "world_candidates": world_candidates,
            "ambient_candidates": ambient_candidates,
        },
        forbidden_keys=forbidden_nonnull_keys,
    )
    ok_forbidden = all(v == 0 for v in forbidden_counts.values())
    results.append(_case("J_forbidden_nonnull_keys", ok_forbidden, forbidden_counts))

    verdict = "GO" if all(r["ok"] for r in results if r["case"] not in ("A_outputs_present",)) and results[-1]["ok"] else "NO_GO"
    # make verdict robust
    verdict = "GO" if all(r["ok"] for r in results) else "NO_GO"

    hard_blockers: List[str] = []
    if verdict != "GO":
        hard_blockers = [r["case"] for r in results if not r["ok"]]

    report = {"verifier": "verify_midplatform_ocr_bridge_v0", "verdict": verdict, "hard_blockers": hard_blockers, "results": results}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    with open(os.path.join(out_root, "verification_result.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        f.write("\n")

    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

