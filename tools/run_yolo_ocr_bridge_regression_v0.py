#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import os
import sys
import subprocess
import datetime as _dt
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def _now_iso() -> str:
    return _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: str, obj: Any) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def _run_cmd_json(cmd: List[str]) -> Tuple[int, Optional[Dict[str, Any]], str, str]:
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out = proc.stdout.strip()
    err = proc.stderr.strip()
    parsed: Optional[Dict[str, Any]] = None
    if out:
        try:
            parsed = json.loads(out)
        except Exception:
            # Some verifiers may print JSON with leading/trailing lines; attempt last JSON object.
            try:
                last = out.splitlines()[-1]
                parsed = json.loads(last)
            except Exception:
                parsed = None
    return proc.returncode, parsed, out, err


def _flatten_bridge_results(per_sample_path: str) -> List[Dict[str, Any]]:
    data = _read_json(per_sample_path)
    out: List[Dict[str, Any]] = []
    if isinstance(data, list):
        for s in data:
            if not isinstance(s, dict):
                continue
            bridge = s.get("bridge")
            if not isinstance(bridge, dict):
                continue
            br = bridge.get("bridge_results")
            if isinstance(br, list):
                out.extend([x for x in br if isinstance(x, dict)])
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skeleton-root", required=True, help="Bridge-002 output root (skeleton mode)")
    ap.add_argument("--evidence-root", required=True, help="Bridge-003 output root (real yolo-root evidence)")
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    skeleton_root = os.path.abspath(args.skeleton_root)
    evidence_root = os.path.abspath(args.evidence_root)
    out_root = os.path.abspath(args.output_root)
    os.makedirs(out_root, exist_ok=True)

    skeleton_summary_p = os.path.join(skeleton_root, "yolo_ocr_bridge_summary.json")
    evidence_summary_p = os.path.join(evidence_root, "yolo_ocr_bridge_summary.json")
    skeleton_per_sample_p = os.path.join(skeleton_root, "per_sample_yolo_ocr_bridge_results.json")
    evidence_per_sample_p = os.path.join(evidence_root, "per_sample_yolo_ocr_bridge_results.json")

    skeleton_parse_report = os.path.join(skeleton_root, "yolo_root_parse_report.json")
    evidence_parse_report = os.path.join(evidence_root, "yolo_root_parse_report.json")

    results_matrix: List[Dict[str, Any]] = []
    hard_blockers: List[str] = []

    # 1) Verifier A: skeleton root
    skeleton_verifier_cmd = [
        sys.executable,
        os.path.join(REPO_ROOT, "tools", "verify_yolo_ocr_offline_bridge_v0.py"),
        "--output-root",
        skeleton_root,
    ]
    sk_rc, sk_ver_json, sk_out, sk_err = _run_cmd_json(skeleton_verifier_cmd)
    skeleton_verdict = (sk_rc == 0)
    results_matrix.append(
        {
            "case": "skeleton_verifier_AQ",
            "skeleton_verdict": "GO" if skeleton_verdict else "NO_GO",
            "returncode": sk_rc,
            "stderr_head": (sk_err or "")[:200],
        }
    )
    if not skeleton_verdict:
        hard_blockers.append("skeleton_verifier_failed")

    # 2) Verifier B: evidence root
    evidence_verifier_cmd = [
        sys.executable,
        os.path.join(REPO_ROOT, "tools", "verify_yolo_ocr_bridge_evidence_run_v0.py"),
        "--output-root",
        evidence_root,
    ]
    ev_rc, ev_ver_json, ev_out, ev_err = _run_cmd_json(evidence_verifier_cmd)
    evidence_verdict = (ev_rc == 0)
    results_matrix.append(
        {
            "case": "evidence_verifier_AQ+evidence_gates",
            "evidence_verdict": "GO" if evidence_verdict else "NO_GO",
            "returncode": ev_rc,
            "stderr_head": (ev_err or "")[:200],
        }
    )
    if not evidence_verdict:
        hard_blockers.append("evidence_verifier_failed")

    # Load summaries and parse reports (for hard checks / scale register).
    try:
        skeleton_summary = _read_json(skeleton_summary_p)
    except Exception as e:
        skeleton_summary = {}
        hard_blockers.append("skeleton_summary_read_failed")
        results_matrix.append({"case": "skeleton_summary_read", "ok": False, "error": repr(e)})

    try:
        evidence_summary = _read_json(evidence_summary_p)
    except Exception as e:
        evidence_summary = {}
        hard_blockers.append("evidence_summary_read_failed")
        results_matrix.append({"case": "evidence_summary_read", "ok": False, "error": repr(e)})

    try:
        evidence_parse = _read_json(evidence_parse_report) if os.path.isfile(evidence_parse_report) else {}
    except Exception as e:
        evidence_parse = {}
        hard_blockers.append("evidence_parse_report_read_failed")
        results_matrix.append({"case": "evidence_parse_report_read", "ok": False, "error": repr(e)})

    parsed_sample_count = int(evidence_parse.get("parsed_sample_count") or 0)
    parsed_detection_count = int(evidence_parse.get("parsed_detection_count") or 0)

    # 3) Counts
    evidence_proposals_count = int(evidence_summary.get("proposal_generated_count") or evidence_summary.get("proposal_count_total") or 0)
    evidence_results_count = int(evidence_summary.get("bridge_result_generated_count") or evidence_summary.get("bridge_result_count_total") or 0)

    results_matrix.append(
        {
            "case": "evidence_proposal_and_result_counts",
            "proposal_count": evidence_proposals_count,
            "bridge_result_count": evidence_results_count,
            "ok": evidence_proposals_count > 0 and evidence_results_count > 0,
        }
    )
    if not (evidence_proposals_count > 0 and evidence_results_count > 0):
        hard_blockers.append("evidence_missing_proposal_or_result")

    # 4) Governance leakage and boundary fields
    gov_sk = (skeleton_summary.get("governance") or {}).get("governance_leakage", None)
    gov_ev = (evidence_summary.get("governance") or {}).get("governance_leakage", None)
    gov_ok = (gov_sk == 0 and gov_ev == 0)
    results_matrix.append({"case": "governance_leakage_zero", "skeleton": gov_sk, "evidence": gov_ev, "ok": gov_ok})
    if not gov_ok:
        hard_blockers.append("governance_leakage_nonzero")

    # 5) Candidate-only / raw-text-only governance flags (direct field scan)
    def _scan_governance_fields(per_sample_p: str) -> Dict[str, Any]:
        bridge_results = _flatten_bridge_results(per_sample_p)
        if not bridge_results:
            return {"bridge_result_count": 0, "ok": False}
        ok = True
        failures: List[str] = []
        for r in bridge_results:
            if r.get("candidate_only") is not True:
                ok = False
                failures.append("candidate_only_false")
            if r.get("semantic_interpretation_enabled") is not False:
                ok = False
                failures.append("semantic_interpretation_not_false")
            if r.get("allows_execute_now") is not False:
                ok = False
                failures.append("allows_execute_now_not_false")
            if r.get("real_tts_invoked") is not False:
                ok = False
                failures.append("real_tts_invoked_not_false")
            if int(r.get("downstream_invocation_count") or 0) != 0:
                ok = False
                failures.append("downstream_invocation_count_nonzero")
        return {"bridge_result_count": len(bridge_results), "ok": ok, "failures": sorted(set(failures))}

    sk_scan = _scan_governance_fields(skeleton_per_sample_p) if os.path.isfile(skeleton_per_sample_p) else {"ok": False}
    ev_scan = _scan_governance_fields(evidence_per_sample_p) if os.path.isfile(evidence_per_sample_p) else {"ok": False}
    results_matrix.append({"case": "candidate_only_and_boundary_fields_skeleton", **sk_scan})
    results_matrix.append({"case": "candidate_only_and_boundary_fields_evidence", **ev_scan})
    if not sk_scan.get("ok") or not ev_scan.get("ok"):
        hard_blockers.append("boundary_field_scan_failed")

    # 6) Trace/replay/whitebox presence (both roots)
    def _nonempty_file(p: str) -> bool:
        return os.path.isfile(p) and os.path.getsize(p) > 0

    trace_files = [
        ("skeleton_trace", os.path.join(skeleton_root, "yolo_ocr_bridge_trace.jsonl")),
        ("skeleton_replay", os.path.join(skeleton_root, "yolo_ocr_bridge_replay.jsonl")),
        ("skeleton_whitebox", os.path.join(skeleton_root, "yolo_ocr_bridge_whitebox.jsonl")),
        ("evidence_trace", os.path.join(evidence_root, "yolo_ocr_bridge_trace.jsonl")),
        ("evidence_replay", os.path.join(evidence_root, "yolo_ocr_bridge_replay.jsonl")),
        ("evidence_whitebox", os.path.join(evidence_root, "yolo_ocr_bridge_whitebox.jsonl")),
    ]
    trace_ok = all(_nonempty_file(p) for _, p in trace_files)
    trace_detail = {name: _nonempty_file(p) for name, p in trace_files}
    results_matrix.append({"case": "trace_replay_whitebox_nonempty", "ok": trace_ok, "detail": trace_detail})
    if not trace_ok:
        hard_blockers.append("trace_replay_whitebox_missing_or_empty")

    # 7) Attribution & OCR policy id (light scan)
    def _scan_attribution_and_policy(per_sample_p: str, expected_policy_id: str) -> Dict[str, Any]:
        bridge_results = _flatten_bridge_results(per_sample_p)
        if not bridge_results:
            return {"bridge_result_count": 0, "ok": False}
        ok = True
        yolo_attr_ok = True
        ocr_attr_ok = True
        policy_ok = True
        for r in bridge_results:
            sa = r.get("source_attribution") or {}
            ysrc = sa.get("yolo_source")
            osrc = sa.get("ocr_source")
            if not isinstance(ysrc, dict) or not ysrc:
                yolo_attr_ok = False
            if not isinstance(osrc, dict) or not osrc:
                ocr_attr_ok = False
            if str(r.get("ocr_source_policy_id") or "") != str(expected_policy_id):
                policy_ok = False
        ok = yolo_attr_ok and ocr_attr_ok and policy_ok
        return {"bridge_result_count": len(bridge_results), "ok": ok, "yolo_attribution_ok": yolo_attr_ok, "ocr_attribution_ok": ocr_attr_ok, "policy_ok": policy_ok}

    expected_policy_id = str((evidence_summary.get("ocr_source_policy_id") or ""))
    sk_attr = _scan_attribution_and_policy(skeleton_per_sample_p, expected_policy_id)
    ev_attr = _scan_attribution_and_policy(evidence_per_sample_p, expected_policy_id)
    results_matrix.append({"case": "attribution_and_policy_skeleton", **sk_attr})
    results_matrix.append({"case": "attribution_and_policy_evidence", **ev_attr})
    if not sk_attr.get("ok") or not ev_attr.get("ok"):
        hard_blockers.append("attribution_or_policy_scan_failed")

    # Determine verdict with sample scale limitation rule.
    scale_too_small = parsed_sample_count < 2 or parsed_detection_count < 2

    hard_ok = (len(hard_blockers) == 0)
    if hard_ok:
        verdict = "CONDITIONAL_GO" if scale_too_small else "GO"
    else:
        verdict = "NO_GO"

    closure_recommendation = {
        "verdict": verdict,
        "offline_bridge_status": "closed_v0",
        "closure_scope": "offline_bridge_only",
        "evidence_scale_register": {
            "parsed_sample_count": parsed_sample_count,
            "parsed_detection_count": parsed_detection_count,
            "note": "Bridge-003 minimal real evidence run; expansion should be scheduled in a future branch.",
        },
        "future_branches": [
            "Bridge-003 evidence expansion (more real yolo-root samples)",
            "MidPlatform OCR raw text extraction bridge (separate definition/contract)",
            "Scene delta control (separate definition/contract)",
            "Complex layout OCR branch (separate definition/contract)",
        ],
    }

    # Schema matrix (lightweight; primary schema gates come from verifiers).
    def _schema_stats(proposals_p: str) -> Dict[str, Any]:
        if not os.path.isfile(proposals_p):
            return {"proposal_count": 0, "required_keys_present_ratio": None}
        props = _read_json(proposals_p)
        if not isinstance(props, list):
            return {"proposal_count": 0, "required_keys_present_ratio": None}
        required_keys = [
            "proposal_id",
            "proposal_source",
            "source_detection_id",
            "frame_id",
            "timestamp_ms",
            "image_ref",
            "crop_region",
            "original_bbox",
            "padded_crop_region",
            "source_object",
            "ocr_trigger_type",
            "crop_signature",
            "delta_control_deferred",
        ]
        present_counts = 0
        total_props = 0
        for p in props:
            if not isinstance(p, dict):
                continue
            total_props += 1
            if all(k in p for k in required_keys):
                present_counts += 1
        ratio = (present_counts / max(1, total_props)) if total_props else None
        return {"proposal_count": len(props), "required_keys_present_ratio": ratio}

    schema_sk = _schema_stats(os.path.join(skeleton_root, "ocr_crop_proposals.json"))
    schema_ev = _schema_stats(os.path.join(evidence_root, "ocr_crop_proposals.json"))

    attribution_summary = {
        "expected_policy_id": expected_policy_id,
        "skeleton": {"yolo_attribution_ok": sk_attr.get("yolo_attribution_ok"), "ocr_attribution_ok": sk_attr.get("ocr_attribution_ok"), "policy_ok": sk_attr.get("policy_ok")},
        "evidence": {"yolo_attribution_ok": ev_attr.get("yolo_attribution_ok"), "ocr_attribution_ok": ev_attr.get("ocr_attribution_ok"), "policy_ok": ev_attr.get("policy_ok")},
        "skeleton_bridge_results_scanned": sk_attr.get("bridge_result_count"),
        "evidence_bridge_results_scanned": ev_attr.get("bridge_result_count"),
    }

    boundary_summary = {
        "candidate_only_and_raw_text_only": {"skeleton_ok": sk_scan.get("ok"), "evidence_ok": ev_scan.get("ok")},
        "governance_leakage_zero": {"skeleton": gov_sk, "evidence": gov_ev},
        "trace_replay_whitebox_nonempty": trace_detail,
        "runtime_and_downstream_mutation": "offline-only (validated by candidate-only flags + verifiers)",
    }

    regression_summary = {
        "phase": "Phase-ModelOCR-YOLO-Bridge-004",
        "tool": "run_yolo_ocr_bridge_regression_v0.py",
        "timestamp": _now_iso(),
        "verdict": verdict,
        "skeleton_root": skeleton_root,
        "evidence_root": evidence_root,
        "skeleton_verifier_passed": skeleton_verdict,
        "evidence_verifier_passed": evidence_verdict,
        "proposal_generated_count_evidence": evidence_proposals_count,
        "bridge_result_generated_count_evidence": evidence_results_count,
        "ocr_source_policy_id": expected_policy_id,
        "parsed_sample_count_evidence": parsed_sample_count,
        "parsed_detection_count_evidence": parsed_detection_count,
        "scale_too_small": scale_too_small,
        "governance": {"governance_leakage_skeleton": gov_sk, "governance_leakage_evidence": gov_ev},
        "hard_blockers": hard_blockers,
        "soft_followups": [
            "expand evidence run for regression baseline (more samples/frames) in a future phase",
            "add regression coverage tiers (small/medium/large evidence batches) when Bridge-004 is reopened",
        ]
        if scale_too_small
        else ["sample scale is sufficient for baseline; future expansion remains optional"],
        "closure_recommendation": closure_recommendation,
    }

    _write_json(os.path.join(out_root, "yolo_ocr_bridge_regression_summary.json"), regression_summary)
    _write_json(os.path.join(out_root, "yolo_ocr_bridge_regression_matrix.json"), {"cases": results_matrix})
    _write_json(
        os.path.join(out_root, "yolo_ocr_bridge_schema_matrix.json"),
        {"skeleton": schema_sk, "evidence": schema_ev},
    )
    _write_json(os.path.join(out_root, "yolo_ocr_bridge_boundary_summary.json"), boundary_summary)
    _write_json(os.path.join(out_root, "yolo_ocr_bridge_attribution_summary.json"), attribution_summary)

    with open(os.path.join(out_root, "regression_notes.md"), "w", encoding="utf-8") as nf:
        nf.write(
            "\n".join(
                [
                    "# YOLO × OCR Offline Bridge Regression Notes v0",
                    "",
                    f"- skeleton-root: {skeleton_root}",
                    f"- evidence-root: {evidence_root}",
                    "",
                    "## Evidence scale limitation",
                    f"- parsed_sample_count: {parsed_sample_count}",
                    f"- parsed_detection_count: {parsed_detection_count}",
                    "",
                    "## Closure intent",
                    "- Freeze closed_v0 for offline bridge contract/skeleton/evidence gates.",
                    "- Mark this evidence as minimal; schedule expansion as a future branch (not reopened in this phase).",
                    "",
                    "## Hard blockers",
                    f"- {hard_blockers if hard_blockers else '[]'}",
                    "",
                ]
            )
        )

    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())

