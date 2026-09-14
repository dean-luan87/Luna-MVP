#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import json
import os
import time
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = os.path.abspath(os.environ.get("LUNA_REPO_ROOT") or os.getcwd())
if REPO_ROOT not in __import__("sys").path:
    __import__("sys").path.insert(0, REPO_ROOT)


def _resolve(p: str) -> str:
    return p if os.path.isabs(p) else os.path.abspath(os.path.join(REPO_ROOT, p))


def _read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _read_jsonl_count(path: str) -> int:
    if not os.path.isfile(path):
        return 0
    n = 0
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                n += 1
    return n


def _write_json(path: str, obj: Any) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


def _safe_list(x: Any) -> List[Any]:
    return x if isinstance(x, list) else []


def _dist(values: List[str]) -> Dict[str, int]:
    d: Dict[str, int] = {}
    for v in values:
        d[v] = d.get(v, 0) + 1
    return d


def _scan_candidate_boundary_violations(candidates: List[Dict[str, Any]]) -> Dict[str, int]:
    counts = {
        "world_model_write_invoked_true": 0,
        "hive_upload_invoked_true": 0,
        "navigation_action_nonnull": 0,
        "real_tts_invoked_true": 0,
        "recommendation_invoked_true": 0,
        "fabricated_gps_nonnull": 0,
        "source_evidence_refs_empty": 0,
    }
    for c in candidates:
        if not isinstance(c, dict):
            continue
        gov = c.get("governance") if isinstance(c.get("governance"), dict) else {}
        if gov.get("world_model_write_invoked") is True:
            counts["world_model_write_invoked_true"] += 1
        if gov.get("hive_upload_invoked") is True:
            counts["hive_upload_invoked_true"] += 1
        if gov.get("navigation_action") is not None:
            counts["navigation_action_nonnull"] += 1
        if gov.get("real_tts_invoked") is True:
            counts["real_tts_invoked_true"] += 1
        if gov.get("recommendation_invoked") is True:
            counts["recommendation_invoked_true"] += 1

        geo = (((c.get("observed_where") or {}) if isinstance(c.get("observed_where"), dict) else {}).get("geo_location") or {})
        if isinstance(geo, dict) and (geo.get("lat") is not None or geo.get("lng") is not None):
            counts["fabricated_gps_nonnull"] += 1

        refs = c.get("source_evidence_refs")
        if not isinstance(refs, list) or len(refs) == 0:
            counts["source_evidence_refs_empty"] += 1
    return counts


def _load_root(root: str) -> Dict[str, Any]:
    """
    Each root is expected to be ContextEvidence-003 evaluation output_root.
    """
    required_files = [
        "world_context_evidence_summary.json",
        "world_context_evidence_candidates.json",
        "commercial_activity_evidence_candidates.json",
        "world_change_event_candidates.json",
        "trust_and_lifecycle_records.json",
        "world_context_evidence_trace.jsonl",
        "world_context_evidence_replay.jsonl",
        "world_context_evidence_whitebox.jsonl",
        "world_context_evidence_verification_report.json",
    ]
    missing = [f for f in required_files if not os.path.isfile(os.path.join(root, f))]

    summary = _read_json(os.path.join(root, "world_context_evidence_summary.json")) if os.path.isfile(os.path.join(root, "world_context_evidence_summary.json")) else {}
    verifier = _read_json(os.path.join(root, "world_context_evidence_verification_report.json")) if os.path.isfile(os.path.join(root, "world_context_evidence_verification_report.json")) else {}
    candidates = _read_json(os.path.join(root, "world_context_evidence_candidates.json")) if os.path.isfile(os.path.join(root, "world_context_evidence_candidates.json")) else []
    commercial = _read_json(os.path.join(root, "commercial_activity_evidence_candidates.json")) if os.path.isfile(os.path.join(root, "commercial_activity_evidence_candidates.json")) else []
    world_change = _read_json(os.path.join(root, "world_change_event_candidates.json")) if os.path.isfile(os.path.join(root, "world_change_event_candidates.json")) else []

    trace_n = _read_jsonl_count(os.path.join(root, "world_context_evidence_trace.jsonl"))
    replay_n = _read_jsonl_count(os.path.join(root, "world_context_evidence_replay.jsonl"))
    whitebox_n = _read_jsonl_count(os.path.join(root, "world_context_evidence_whitebox.jsonl"))

    # matrices / distributions
    ev_types = [str(c.get("evidence_type") or "") for c in _safe_list(candidates) if isinstance(c, dict)]
    lifecycle_statuses = [str(((c.get("lifecycle") or {}) if isinstance(c.get("lifecycle"), dict) else {}).get("evidence_status") or "") for c in _safe_list(candidates) if isinstance(c, dict)]
    ttl_policies = [str(((c.get("lifecycle") or {}) if isinstance(c.get("lifecycle"), dict) else {}).get("ttl_policy") or "") for c in _safe_list(candidates) if isinstance(c, dict)]
    anchor_types = [str((((c.get("observed_where") or {}) if isinstance(c.get("observed_where"), dict) else {}).get("spatial_anchor_type")) or "") for c in _safe_list(candidates) if isinstance(c, dict)]
    where_sources = [str(c.get("observed_where_source") or "") for c in _safe_list(candidates) if isinstance(c, dict)]
    integrity = [str(c.get("source_ref_integrity_status") or "") for c in _safe_list(candidates) if isinstance(c, dict)]
    chain_depths = [len(c.get("source_reference_chain") or []) if isinstance(c.get("source_reference_chain"), list) else 0 for c in _safe_list(candidates) if isinstance(c, dict)]

    anchor_refs_present = 0
    for c in _safe_list(candidates):
        if not isinstance(c, dict):
            continue
        ow = c.get("observed_where") if isinstance(c.get("observed_where"), dict) else {}
        if isinstance(ow, dict) and ow.get("spatiotemporal_anchor_ref"):
            anchor_refs_present += 1

    boundary_counts = _scan_candidate_boundary_violations([c for c in _safe_list(candidates) if isinstance(c, dict)])

    return {
        "root": root,
        "missing_required_files": missing,
        "verifier_verdict": (verifier.get("verdict") if isinstance(verifier, dict) else None),
        "counts": {
            "world_context_evidence_candidates": len(_safe_list(candidates)),
            "commercial_activity_evidence_candidates": len(_safe_list(commercial)),
            "world_change_event_candidates": len(_safe_list(world_change)),
            "trace": trace_n,
            "replay": replay_n,
            "whitebox": whitebox_n,
            "anchor_ref_present_count": anchor_refs_present,
        },
        "distributions": {
            "evidence_type": _dist(ev_types),
            "lifecycle_evidence_status": _dist(lifecycle_statuses),
            "ttl_policy": _dist(ttl_policies),
            "spatial_anchor_type": _dist(anchor_types),
            "observed_where_source": _dist(where_sources),
            "source_ref_integrity_status": _dist(integrity),
            "source_reference_chain_depth": _dist([str(d) for d in chain_depths]),
        },
        "boundary_counts": boundary_counts,
        "summary_boundaries": (summary.get("boundaries") if isinstance(summary, dict) else None),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--roots", nargs="+", required=True)
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    roots = [str(r) for r in args.roots]
    out_root = _resolve(args.output_root)
    os.makedirs(out_root, exist_ok=True)

    hard_blockers: List[str] = []
    root_rows: List[Dict[str, Any]] = []
    for r in roots:
        abs_r = _resolve(r)
        if not os.path.isdir(abs_r):
            hard_blockers.append(f"root_not_readable:{r}")
            root_rows.append({"root": r, "root_abs": abs_r, "error": "not_a_directory"})
            continue
        row = _load_root(abs_r)
        row["root_input_arg"] = r
        row["root_abs"] = abs_r
        root_rows.append(row)
        if row.get("missing_required_files"):
            hard_blockers.append(f"root_missing_files:{r}")
        if row.get("verifier_verdict") != "GO":
            hard_blockers.append(f"root_verifier_not_GO:{r}")

    # Aggregate matrices
    total_candidates = sum(int((rr.get("counts") or {}).get("world_context_evidence_candidates") or 0) for rr in root_rows if isinstance(rr, dict))
    total_commercial = sum(int((rr.get("counts") or {}).get("commercial_activity_evidence_candidates") or 0) for rr in root_rows if isinstance(rr, dict))
    total_world_change = sum(int((rr.get("counts") or {}).get("world_change_event_candidates") or 0) for rr in root_rows if isinstance(rr, dict))

    # Candidate matrix (merge distributions)
    def merge_dist(key: str) -> Dict[str, int]:
        out: Dict[str, int] = {}
        for rr in root_rows:
            dist = ((rr.get("distributions") or {}) if isinstance(rr, dict) else {}).get(key)
            if not isinstance(dist, dict):
                continue
            for k, v in dist.items():
                try:
                    out[str(k)] = out.get(str(k), 0) + int(v)
                except Exception:
                    continue
        return out

    root_matrix = {"roots": root_rows}
    candidate_matrix = {
        "totals": {"world_context_evidence_candidates": total_candidates, "commercial_activity_evidence_candidates": total_commercial, "world_change_event_candidates": total_world_change},
        "distributions": {
            "evidence_type": merge_dist("evidence_type"),
            "lifecycle_evidence_status": merge_dist("lifecycle_evidence_status"),
            "ttl_policy": merge_dist("ttl_policy"),
            "spatial_anchor_type": merge_dist("spatial_anchor_type"),
            "observed_where_source": merge_dist("observed_where_source"),
            "source_ref_integrity_status": merge_dist("source_ref_integrity_status"),
            "source_reference_chain_depth": merge_dist("source_reference_chain_depth"),
        },
    }

    # Anchor alignment summary
    anchor_alignment = {
        "roots_with_any_anchor_ref": sum(1 for rr in root_rows if int((rr.get("counts") or {}).get("anchor_ref_present_count") or 0) > 0),
        "anchor_ref_present_total": sum(int((rr.get("counts") or {}).get("anchor_ref_present_count") or 0) for rr in root_rows),
        "observed_where_source_distribution": candidate_matrix["distributions"]["observed_where_source"],
        "spatial_anchor_type_distribution": candidate_matrix["distributions"]["spatial_anchor_type"],
    }

    # Source reference chain summary
    source_chain_summary = {
        "integrity_distribution": candidate_matrix["distributions"]["source_ref_integrity_status"],
        "chain_depth_distribution": candidate_matrix["distributions"]["source_reference_chain_depth"],
    }

    # Trust / lifecycle / policy summary (presence is enforced by per-root verifier; keep distribution only)
    trust_lifecycle_policy = {
        "lifecycle_status_distribution": candidate_matrix["distributions"]["lifecycle_evidence_status"],
        "ttl_policy_distribution": candidate_matrix["distributions"]["ttl_policy"],
    }

    # Boundary summary
    boundary_totals: Dict[str, int] = {}
    for rr in root_rows:
        bc = rr.get("boundary_counts") if isinstance(rr, dict) else None
        if not isinstance(bc, dict):
            continue
        for k, v in bc.items():
            try:
                boundary_totals[str(k)] = boundary_totals.get(str(k), 0) + int(v)
            except Exception:
                continue
    boundary_summary = {"boundary_counts": boundary_totals, "boundary_ok": all(int(v) == 0 for v in boundary_totals.values())}

    # TRW summary
    trw = {
        "trace_total": sum(int((rr.get("counts") or {}).get("trace") or 0) for rr in root_rows),
        "replay_total": sum(int((rr.get("counts") or {}).get("replay") or 0) for rr in root_rows),
        "whitebox_total": sum(int((rr.get("counts") or {}).get("whitebox") or 0) for rr in root_rows),
    }
    trw["all_nonempty"] = trw["trace_total"] > 0 and trw["replay_total"] > 0 and trw["whitebox_total"] > 0

    regression_summary = {
        "phase": "Phase-WorldModel-ContextEvidence-004",
        "tool": "run_world_context_evidence_regression_v0.py",
        "roots": roots,
        "generated_at_ms": int(time.time() * 1000),
        "hard_blockers": hard_blockers,
        "verdict_hint": "GO" if not hard_blockers and boundary_summary["boundary_ok"] else "NO_GO",
        "closure_recommendation": "close_as_closed_v0_candidate_only" if not hard_blockers and boundary_summary["boundary_ok"] else "do_not_close",
    }

    _write_json(os.path.join(out_root, "world_context_evidence_regression_summary.json"), regression_summary)
    _write_json(os.path.join(out_root, "world_context_evidence_root_matrix.json"), root_matrix)
    _write_json(os.path.join(out_root, "world_context_evidence_candidate_matrix.json"), candidate_matrix)
    _write_json(os.path.join(out_root, "world_context_anchor_alignment_summary.json"), anchor_alignment)
    _write_json(os.path.join(out_root, "world_context_source_reference_chain_summary.json"), source_chain_summary)
    _write_json(os.path.join(out_root, "world_context_trust_lifecycle_policy_summary.json"), trust_lifecycle_policy)
    _write_json(os.path.join(out_root, "world_context_boundary_summary.json"), boundary_summary)
    _write_json(os.path.join(out_root, "world_context_trace_replay_whitebox_summary.json"), trw)

    notes = []
    notes.append("# WorldContextEvidence Regression Notes (Phase-WorldModel-ContextEvidence-004)\n\n")
    notes.append(f"- generated_at_ms: {regression_summary['generated_at_ms']}\n")
    notes.append(f"- roots: {roots}\n")
    notes.append(f"- hard_blockers: {hard_blockers if hard_blockers else 'none'}\n")
    notes.append(f"- closure_recommendation: {regression_summary['closure_recommendation']}\n")
    notes.append("\n## Boundary summary\n")
    for k, v in boundary_totals.items():
        notes.append(f"- {k}: {v}\n")
    with open(os.path.join(out_root, "regression_notes.md"), "w", encoding="utf-8") as f:
        f.write("".join(notes))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

