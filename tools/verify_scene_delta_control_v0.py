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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    out_root = args.output_root if os.path.isabs(args.output_root) else os.path.abspath(os.path.join(REPO_ROOT, args.output_root))

    required_files = [
        "scene_delta_summary.json",
        "scene_delta_inputs.json",
        "scene_processed_states.json",
        "spatiotemporal_delta_anchors.json",
        "scene_delta_decisions.json",
        "repeated_evidence_compression_records.json",
        "scene_delta_trace.jsonl",
        "scene_delta_replay.jsonl",
        "scene_delta_whitebox.jsonl",
        "evaluation_notes.md",
    ]

    results: List[Dict[str, Any]] = []
    missing = [f for f in required_files if not os.path.isfile(os.path.join(out_root, f))]
    results.append(_case("A_outputs_present", len(missing) == 0, {"missing": missing}))
    if missing:
        report = {"verifier": "verify_scene_delta_control_v0", "verdict": "NO_GO", "hard_blockers": missing, "results": results}
        print(json.dumps(report, ensure_ascii=False, indent=2))
        with open(os.path.join(out_root, "verification_result.json"), "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        return 2

    summary = _read_json(os.path.join(out_root, "scene_delta_summary.json"))
    inputs_ = _read_json(os.path.join(out_root, "scene_delta_inputs.json"))
    anchors = _read_json(os.path.join(out_root, "spatiotemporal_delta_anchors.json"))
    decisions = _read_json(os.path.join(out_root, "scene_delta_decisions.json"))
    compress = _read_json(os.path.join(out_root, "repeated_evidence_compression_records.json"))

    trace = _read_jsonl_lines(os.path.join(out_root, "scene_delta_trace.jsonl"))
    replay = _read_jsonl_lines(os.path.join(out_root, "scene_delta_replay.jsonl"))
    whitebox = _read_jsonl_lines(os.path.join(out_root, "scene_delta_whitebox.jsonl"))

    ok_samples_readable = isinstance(summary, dict) and summary.get("processed_count") is not None
    results.append(_case("A_input_samples_readable", ok_samples_readable, {"processed_count": (summary or {}).get("processed_count")}))

    ok_inputs_schema = isinstance(inputs_, list) and len(inputs_) > 0
    if ok_inputs_schema:
        for ev in inputs_:
            if not isinstance(ev, dict):
                ok_inputs_schema = False
                break
            if ev.get("candidate_only") is not True:
                ok_inputs_schema = False
                break
            if ev.get("allows_execute_now") is not False:
                ok_inputs_schema = False
                break
            if not ev.get("spatiotemporal_anchor"):
                ok_inputs_schema = False
                break
            if not ev.get("content_signature"):
                ok_inputs_schema = False
                break
    results.append(_case("B_scene_delta_input_schema_valid", ok_inputs_schema, {"input_count": len(inputs_) if isinstance(inputs_, list) else None}))

    ok_anchor = isinstance(anchors, list) and len(anchors) == (len(inputs_) if isinstance(inputs_, list) else -1)
    results.append(_case("C_spatiotemporal_anchor_generated", ok_anchor, {"anchor_count": len(anchors) if isinstance(anchors, list) else None}))

    ok_sig_present = True
    if isinstance(inputs_, list):
        for ev in inputs_:
            sig = ev.get("content_signature")
            if not isinstance(sig, dict):
                ok_sig_present = False
                break
            if not any(sig.get(k) is not None for k in ("text_signature", "object_signature", "crop_signature", "content_signature", "spatial_signature")):
                ok_sig_present = False
                break
    else:
        ok_sig_present = False
    results.append(_case("D_signature_inputs_present", ok_sig_present, {}))

    ok_decisions = isinstance(decisions, list) and len(decisions) == (len(inputs_) if isinstance(inputs_, list) else -1)
    results.append(_case("E_scene_delta_decision_generated", ok_decisions, {"decision_count": len(decisions) if isinstance(decisions, list) else None}))

    # Minimal subset of 001-Fix A–R: look for at least one decision in expected families.
    status_set = set()
    action_set = set()
    if isinstance(decisions, list):
        for d in decisions:
            if isinstance(d, dict):
                status_set.add(str(d.get("delta_status") or ""))
                action_set.add(str(d.get("delta_action") or ""))

    results.append(_case("F_same_content_same_place_reuse_or_ignore", bool({"reuse_previous", "ignore_duplicate"} & action_set), {"actions_seen": sorted(list(action_set))}))
    results.append(_case("G_new_content_same_place_full_or_partial", bool({"full_reprocess", "partial_update"} & action_set), {"actions_seen": sorted(list(action_set))}))
    results.append(_case("H_content_replaced_recorded", "content_replaced" in status_set, {"statuses_seen": sorted(list(status_set))}))
    results.append(_case("H2_content_removed_recorded", "content_removed" in status_set, {"statuses_seen": sorted(list(status_set))}))
    results.append(_case("I_expired_content_recheck", "expire_and_reprocess" in action_set or "expired" in status_set, {"actions_seen": sorted(list(action_set)), "statuses_seen": sorted(list(status_set))}))

    # Compression record: if any exists, must have canonical_evidence_ref
    ok_compress = isinstance(compress, list)
    ok_compress_canonical = True
    if ok_compress:
        for r in compress:
            if not isinstance(r, dict):
                ok_compress_canonical = False
                break
            if not r.get("canonical_evidence_ref"):
                ok_compress_canonical = False
                break
    else:
        ok_compress_canonical = False
    results.append(_case("J_duplicate_compression_has_canonical", ok_compress_canonical, {"compression_records": len(compress) if isinstance(compress, list) else None}))

    # K compression preserves audit refs: require first/last_seen_at and duplicate_count
    ok_audit = True
    if isinstance(compress, list):
        for r in compress:
            if not isinstance(r, dict):
                ok_audit = False
                break
            for k in ("first_seen_at", "last_seen_at", "duplicate_count"):
                if k not in r:
                    ok_audit = False
                    break
            if not ok_audit:
                break
    else:
        ok_audit = False
    results.append(_case("K_compression_preserves_audit_refs", ok_audit, {}))

    # L default storage_level=individual_local: check trace storage_level
    ok_storage_default = True
    if trace:
        for t in trace:
            if t.get("storage_level") != "individual_local":
                ok_storage_default = False
                break
    else:
        ok_storage_default = False
    results.append(_case("L_default_storage_level_individual_local", ok_storage_default, {}))

    # M/N/O/P boundary flags must always be false/null
    def _all_trace_bool_false(key: str) -> bool:
        if not trace:
            return False
        for t in trace:
            if t.get(key) is not False:
                return False
        return True

    results.append(_case("M_hive_upload_not_invoked", _all_trace_bool_false("hive_upload_invoked"), {}))
    results.append(_case("N_world_model_write_not_invoked", _all_trace_bool_false("world_model_write_invoked"), {}))

    ok_nav_null = True
    if trace:
        for t in trace:
            if t.get("navigation_action") is not None:
                ok_nav_null = False
                break
    else:
        ok_nav_null = False
    results.append(_case("O_navigation_action_null", ok_nav_null, {}))

    ok_tts_false = _all_trace_bool_false("real_tts_invoked")
    results.append(_case("P_real_tts_not_invoked", ok_tts_false, {}))

    ok_trw = len(trace) > 0 and len(replay) > 0 and len(whitebox) > 0
    results.append(_case("Q_trace_replay_whitebox_present", ok_trw, {"trace": len(trace), "replay": len(replay), "whitebox": len(whitebox)}))

    # R no runtime invocation: check decisions flags
    ok_runtime = True
    if isinstance(decisions, list):
        for d in decisions:
            if not isinstance(d, dict):
                ok_runtime = False
                break
            if d.get("runtime_invoked") is not False:
                ok_runtime = False
                break
    else:
        ok_runtime = False
    results.append(_case("R_no_runtime_invocation", ok_runtime, {}))

    hard_blockers: List[str] = []
    ok_all = all(r["ok"] for r in results)
    verdict = "GO" if ok_all else "NO_GO"
    report = {"verifier": "verify_scene_delta_control_v0", "verdict": verdict, "hard_blockers": hard_blockers, "results": results}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    with open(os.path.join(out_root, "verification_result.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

