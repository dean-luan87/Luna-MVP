from __future__ import annotations

import argparse
import json
import os
from typing import Any, Dict, List, Tuple


def _read_json(p: str) -> Any:
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def _read_jsonl_count(p: str) -> int:
    n = 0
    with open(p, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                n += 1
    return n


def _ok(name: str, ok: bool, details: str = "") -> Dict[str, Any]:
    return {"check": name, "ok": bool(ok), "details": details}


def _get(d: Dict[str, Any], path: List[str]) -> Any:
    cur: Any = d
    for k in path:
        if not isinstance(cur, dict) or k not in cur:
            return None
        cur = cur[k]
    return cur


def _candidate_schema_minimal_ok(c: Dict[str, Any]) -> Tuple[bool, str]:
    required_top = [
        "world_context_evidence_id",
        "candidate_only",
        "evidence_type",
        "source_modalities",
        "source_evidence_refs",
        "observed_at",
        "observed_where",
        "observed_where_source",
        "spatial_anchor_confidence",
        "anchor_status",
        "content",
        "trust",
        "lifecycle",
        "world_model_policy",
        "source_reference_chain",
        "source_layers",
        "missing_source_refs",
        "source_ref_integrity_status",
        "governance",
        "trace_ref",
        "replay_ref",
        "whitebox_ref",
    ]
    for k in required_top:
        if k not in c:
            return False, f"missing:{k}"
    if c.get("candidate_only") is not True:
        return False, "candidate_only_not_true"

    if _get(c, ["observed_at", "timestamp_ms"]) is None:
        return False, "missing_observed_at.timestamp_ms"
    if _get(c, ["observed_where", "spatial_anchor_type"]) is None:
        return False, "missing_observed_where.spatial_anchor_type"

    for tk in ("trust_score", "cross_validation_status"):
        if _get(c, ["trust", tk]) is None:
            return False, f"missing_trust.{tk}"
    for lk in ("evidence_status", "ttl_policy", "requires_revalidation", "last_seen_at", "seen_count"):
        if _get(c, ["lifecycle", lk]) is None:
            return False, f"missing_lifecycle.{lk}"
    for pk in ("write_policy", "task_planning_impact", "shareable_to_hive", "requires_user_confirmation"):
        if _get(c, ["world_model_policy", pk]) is None:
            return False, f"missing_world_model_policy.{pk}"

    g = c.get("governance") if isinstance(c.get("governance"), dict) else {}
    if g.get("world_model_write_invoked") is not False:
        return False, "governance.world_model_write_invoked_not_false"
    if g.get("hive_upload_invoked") is not False:
        return False, "governance.hive_upload_invoked_not_false"
    if g.get("navigation_action") is not None:
        return False, "governance.navigation_action_not_null"
    if g.get("real_tts_invoked") is not False:
        return False, "governance.real_tts_invoked_not_false"
    if g.get("recommendation_invoked") is not False:
        return False, "governance.recommendation_invoked_not_false"

    return True, "ok"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    root = args.output_root
    checks: List[Dict[str, Any]] = []

    # A. input readable (output root exists)
    checks.append(_ok("A_output_root_exists", os.path.isdir(root), root))

    # B. files exist
    required_files = [
        "world_context_evidence_summary.json",
        "world_context_evidence_candidates.json",
        "commercial_activity_evidence_candidates.json",
        "world_change_event_candidates.json",
        "trust_and_lifecycle_records.json",
        "world_context_evidence_trace.jsonl",
        "world_context_evidence_replay.jsonl",
        "world_context_evidence_whitebox.jsonl",
        "evaluation_notes.md",
    ]
    missing = [f for f in required_files if not os.path.exists(os.path.join(root, f))]
    checks.append(_ok("B_required_files_present", len(missing) == 0, f"missing={missing}"))

    if missing:
        report = {"verdict": "NO_GO", "checks": checks}
        with open(os.path.join(root, "world_context_evidence_verification_report.json"), "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        return 2

    # load
    summary = _read_json(os.path.join(root, "world_context_evidence_summary.json"))
    candidates = _read_json(os.path.join(root, "world_context_evidence_candidates.json"))
    commercial = _read_json(os.path.join(root, "commercial_activity_evidence_candidates.json"))
    world_change = _read_json(os.path.join(root, "world_change_event_candidates.json"))

    # C. candidate schema valid
    schema_fail = []
    for c in candidates:
        ok, why = _candidate_schema_minimal_ok(c) if isinstance(c, dict) else (False, "candidate_not_dict")
        if not ok:
            schema_fail.append({"id": c.get("world_context_evidence_id") if isinstance(c, dict) else None, "why": why})
            if len(schema_fail) >= 5:
                break
    checks.append(_ok("C_candidate_schema_minimal_valid", len(schema_fail) == 0, f"first_failures={schema_fail}"))

    # D/E/F/G/H/I/J. presence is covered by minimal schema; add aggregate sanity
    checks.append(_ok("D_observed_at_present", all(_get(c, ["observed_at", "timestamp_ms"]) is not None for c in candidates), ""))
    checks.append(_ok("E_observed_where_present", all(_get(c, ["observed_where", "spatial_anchor_type"]) is not None for c in candidates), ""))
    checks.append(_ok("F_world_model_policy_present", all(isinstance(c.get("world_model_policy"), dict) for c in candidates), ""))
    checks.append(_ok("G_source_evidence_refs_present", all(isinstance(c.get("source_evidence_refs"), list) for c in candidates), ""))
    checks.append(_ok("H_trust_present", all(isinstance(c.get("trust"), dict) for c in candidates), ""))
    checks.append(_ok("I_lifecycle_present", all(isinstance(c.get("lifecycle"), dict) for c in candidates), ""))
    checks.append(_ok("J_governance_present", all(isinstance(c.get("governance"), dict) for c in candidates), ""))

    # W. observed_where_source present
    checks.append(_ok("W_observed_where_source_present", all(isinstance(c.get("observed_where_source"), str) and c.get("observed_where_source") for c in candidates), ""))

    # X. source_reference_chain present
    checks.append(_ok("X_source_reference_chain_present", all(isinstance(c.get("source_reference_chain"), list) and len(c.get("source_reference_chain")) >= 1 for c in candidates), ""))

    # AC. source_layers present
    checks.append(_ok("AC_source_layers_present", all(isinstance(c.get("source_layers"), list) and len(c.get("source_layers")) >= 1 for c in candidates), ""))

    # AD. source_ref_integrity_status present
    checks.append(_ok("AD_source_ref_integrity_status_present", all(isinstance(c.get("source_ref_integrity_status"), str) and c.get("source_ref_integrity_status") in ("complete", "partial", "broken") for c in candidates), ""))

    # Z. no fabricated GPS
    z_ok = True
    z_bad = []
    for c in candidates:
        geo = _get(c, ["observed_where", "geo_location"])
        if isinstance(geo, dict):
            if geo.get("lat") is not None or geo.get("lng") is not None:
                z_ok = False
                z_bad.append(c.get("world_context_evidence_id"))
                break
    checks.append(_ok("Z_no_fabricated_gps", z_ok, f"bad={z_bad[:3]}"))

    # AA. spatiotemporal_anchor_ref inherited when SceneDelta candidate has scene_delta layer
    aa_ok = True
    aa_bad = []
    for c in candidates:
        layers = c.get("source_layers") if isinstance(c.get("source_layers"), list) else []
        if "scene_delta" in layers:
            anchor_ref = _get(c, ["observed_where", "spatiotemporal_anchor_ref"])
            if anchor_ref is None:
                aa_ok = False
                aa_bad.append(c.get("world_context_evidence_id"))
                break
    checks.append(_ok("AA_scenedelta_anchor_inherited", aa_ok, f"bad={aa_bad[:3]}"))

    # AB. source_modalities only contains real sensing modalities
    allowed_mods = {"ocr", "yolo", "map", "gps", "visual_symbol", "user_feedback"}
    ab_ok = True
    ab_bad = []
    for c in candidates:
        mods = c.get("source_modalities")
        if not isinstance(mods, list):
            ab_ok = False
            ab_bad.append(c.get("world_context_evidence_id"))
            break
        if any(m not in allowed_mods for m in mods):
            ab_ok = False
            ab_bad.append(c.get("world_context_evidence_id"))
            break
    checks.append(_ok("AB_source_modalities_sensing_only", ab_ok, f"bad={ab_bad[:3]}"))

    # Y. missing_source_refs present when upstream ref missing (integrity partial/broken)
    y_ok = True
    y_bad = []
    for c in candidates:
        integrity = c.get("source_ref_integrity_status")
        missing = c.get("missing_source_refs")
        if integrity in ("partial", "broken"):
            if not (isinstance(missing, list) and len(missing) >= 1):
                y_ok = False
                y_bad.append(c.get("world_context_evidence_id"))
                break
    checks.append(_ok("Y_missing_source_refs_when_incomplete", y_ok, f"bad={y_bad[:3]}"))

    # AE. missing source_evidence_refs -> hard blocker
    ae_ok = True
    ae_bad = []
    for c in candidates:
        refs = c.get("source_evidence_refs")
        if not isinstance(refs, list) or len(refs) == 0:
            ae_ok = False
            ae_bad.append(c.get("world_context_evidence_id"))
            break
    checks.append(_ok("AE_source_evidence_refs_non_empty_hard_gate", ae_ok, f"bad={ae_bad[:3]}"))

    # AF. unknown anchor forces requires_revalidation=true
    af_ok = True
    af_bad = []
    for c in candidates:
        sat = _get(c, ["observed_where", "spatial_anchor_type"])
        if sat == "unknown":
            if _get(c, ["lifecycle", "requires_revalidation"]) is not True:
                af_ok = False
                af_bad.append(c.get("world_context_evidence_id"))
                break
    checks.append(_ok("AF_unknown_anchor_requires_revalidation", af_ok, f"bad={af_bad[:3]}"))

    # K. commercial short_ttl + revalidation + not primary decision
    k_ok = True
    k_bad = []
    for cc in commercial:
        if not isinstance(cc, dict):
            k_ok = False
            k_bad.append("commercial_not_dict")
            break
        if cc.get("expiry_policy") != "short_ttl" or cc.get("requires_revalidation") is not True:
            k_ok = False
            k_bad.append(cc.get("commercial_activity_evidence_id"))
            break
        if cc.get("allowed_for_primary_task_decision") is not False:
            k_ok = False
            k_bad.append(cc.get("commercial_activity_evidence_id"))
            break
        if cc.get("navigation_action") is not None:
            k_ok = False
            k_bad.append(cc.get("commercial_activity_evidence_id"))
            break
    checks.append(_ok("K_commercial_short_ttl_revalidation_and_not_primary", k_ok, f"bad={k_bad[:3]}"))

    # L/M/N. world change mapping presence when present in input
    wc_change_types = set()
    for w in world_change:
        if isinstance(w, dict):
            wc_change_types.add(w.get("change_type"))
    checks.append(_ok("M_content_replaced_maps_to_world_change_event_candidate", ("content_replaced" in wc_change_types) or (len(world_change) == 0), f"types={sorted([t for t in wc_change_types if t])}"))
    checks.append(_ok("N_content_removed_maps_to_world_change_event_candidate", ("content_removed" in wc_change_types) or (len(world_change) == 0), f"types={sorted([t for t in wc_change_types if t])}"))

    # L. expired requires_revalidation (when expired appears)
    expired_candidates = [c for c in candidates if isinstance(c, dict) and _get(c, ["lifecycle", "evidence_status"]) == "expired_candidate"]
    l_ok = True
    if expired_candidates:
        l_ok = all(_get(c, ["lifecycle", "requires_revalidation"]) is True for c in expired_candidates)
    checks.append(_ok("L_expired_maps_to_requires_revalidation", l_ok, f"expired_count={len(expired_candidates)}"))

    # O/P. duplicate/uncertain do not create persistent fact (enforced by no_write)
    o_ok = True
    o_bad = []
    for c in candidates:
        if not isinstance(c, dict):
            continue
        st = _get(c, ["lifecycle", "evidence_status"])
        if st in ("uncertain_candidate", "candidate"):
            wp = _get(c, ["world_model_policy", "write_policy"])
            if wp not in ("no_write", "low_priority_candidate", "scene_local_candidate"):
                o_ok = False
                o_bad.append(c.get("world_context_evidence_id"))
                break
    checks.append(_ok("O_duplicate_or_uncertain_not_persistent_write", o_ok, f"bad={o_bad[:3]}"))

    # Q-R-S-T-U. governance boundaries (all candidates)
    gov_ok = True
    for c in candidates:
        if not isinstance(c, dict):
            gov_ok = False
            break
        g = c.get("governance") if isinstance(c.get("governance"), dict) else {}
        if g.get("world_model_write_invoked") is not False:
            gov_ok = False
            break
        if g.get("hive_upload_invoked") is not False:
            gov_ok = False
            break
        if g.get("navigation_action") is not None:
            gov_ok = False
            break
        if g.get("real_tts_invoked") is not False:
            gov_ok = False
            break
        if g.get("recommendation_invoked") is not False:
            gov_ok = False
            break
    checks.append(_ok("Q_boundary_world_model_write_false", gov_ok, ""))

    # V. trace/replay/whitebox present and non-empty
    trace_n = _read_jsonl_count(os.path.join(root, "world_context_evidence_trace.jsonl"))
    replay_n = _read_jsonl_count(os.path.join(root, "world_context_evidence_replay.jsonl"))
    whitebox_n = _read_jsonl_count(os.path.join(root, "world_context_evidence_whitebox.jsonl"))
    checks.append(_ok("V_trace_replay_whitebox_non_empty", trace_n > 0 and replay_n > 0 and whitebox_n > 0, f"trace={trace_n}, replay={replay_n}, whitebox={whitebox_n}"))

    # Extra: summary boundary flags
    bound = summary.get("boundaries") if isinstance(summary, dict) else {}
    checks.append(_ok("R_summary_boundaries_present", isinstance(bound, dict), ""))
    if isinstance(bound, dict):
        checks.append(_ok("S_summary_no_world_write", bound.get("world_model_write_invoked") is False, str(bound.get("world_model_write_invoked"))))
        checks.append(_ok("T_summary_no_hive", bound.get("hive_upload_invoked") is False, str(bound.get("hive_upload_invoked"))))
        checks.append(_ok("U_summary_nav_null", bound.get("navigation_action") is None, str(bound.get("navigation_action"))))

    verdict = "GO" if all(c["ok"] for c in checks) else "NO_GO"
    report = {"verdict": verdict, "checks": checks, "counts": (summary.get("counts") if isinstance(summary, dict) else None)}
    with open(os.path.join(root, "world_context_evidence_verification_report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

