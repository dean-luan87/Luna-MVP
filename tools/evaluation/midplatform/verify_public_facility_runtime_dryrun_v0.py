#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase-PublicFacility-Runtime-DryRun-001 verifier."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

FORBIDDEN_SPEAK = (
    "这里就是洗手间",
    "请立即从这里出去",
    "前方一定是电梯",
    "这是已确认的公共设施",
)


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dryrun-root", required=True)
    ap.add_argument("--verifier-output-root", default="")
    args = ap.parse_args()

    root = Path(args.dryrun_root).expanduser().resolve()
    vout = (
        Path(args.verifier_output_root).expanduser().resolve()
        if args.verifier_output_root.strip()
        else (root.parent / "public_facility_runtime_dryrun_verify_v0").resolve()
    )
    vout.mkdir(parents=True, exist_ok=True)

    blockers: List[str] = []

    def req(name: str) -> Path:
        p = root / name
        if not p.is_file():
            blockers.append(f"missing:{name}")
        return p

    sum_p = req("public_facility_runtime_dryrun_summary.json")
    fix_p = req("public_facility_runtime_fixture_manifest.json")
    sem_p = req("public_facility_semantic_candidate_matrix.json")
    corr_p = req("public_facility_correction_candidate_matrix.json")
    ev_p = req("public_facility_evidence_composition_matrix.json")
    gate_p = req("public_facility_gate_evaluator_dryrun.json")
    speak_p = req("public_facility_cautious_speak_dryrun_report.json")
    risk_p = req("public_facility_runtime_risk_report.json")
    met_p = req("public_facility_runtime_metrics_binding_report.json")
    bench_p = req("public_facility_runtime_benchmark_link_report.json")
    sim_p = req("public_facility_runtime_simulation_context_report.json")
    nc_p = req("public_facility_runtime_non_claims_report.json")
    aud_p = req("public_facility_runtime_audit_report.json")

    if not blockers:
        sm = _read_json(sum_p)
        for k, val in (
            ("runtime_scope", "dry_run_only"),
            ("semantic_first_required", True),
            ("default_ocr_mainline_allowed", False),
            ("real_ocr_invoked", False),
            ("vision_provider_invoked", False),
            ("visual_symbol_registry_invoked", False),
        ):
            if sm.get(k) != val:
                blockers.append(f"summary_{k}_wrong")

        fix = _read_json(fix_p)
        fixtures = fix.get("fixtures") or []
        if len(fixtures) < 6:
            blockers.append("fixture_count_lt_6")
        fids = {f.get("fixture_id") for f in fixtures if isinstance(f, dict)}
        if "PF_FIXTURE_RESTROOM_TYPO" not in fids:
            blockers.append("missing_toliet_fixture")
        if "PF_FIXTURE_AMBIGUOUS_ICON" not in fids:
            blockers.append("missing_ambiguous_fixture")

        sem = _read_json(sem_p)
        for row in sem.get("rows") or []:
            if not isinstance(row, dict):
                continue
            if row.get("fact_status") != "not_fact":
                blockers.append("semantic_fact_status_not_not_fact")
                break
            if row.get("write_allowed") is not False:
                blockers.append("semantic_write_allowed_not_false")
                break
        toilet = [r for r in sem.get("rows") or [] if r.get("fixture_id") == "PF_FIXTURE_RESTROOM_TYPO"]
        if not toilet or toilet[0].get("raw_ocr_text_preserved") != "Toliet":
            blockers.append("toilet_raw_ocr_not_preserved")

        corr = _read_json(corr_p)
        for row in corr.get("rows") or []:
            if row.get("correction_committed") is not False:
                blockers.append("correction_committed_not_false")
                break

        gate = _read_json(gate_p)
        amb = [r for r in gate.get("rows") or [] if r.get("fixture_id") == "PF_FIXTURE_AMBIGUOUS_ICON"]
        if not amb or amb[0].get("decision") != "hold_for_review":
            blockers.append("ambiguous_decision_not_hold")
        for row in gate.get("rows") or []:
            for k in ("fact_write_allowed", "world_model_write_allowed"):
                if row.get(k) is not False:
                    blockers.append(f"gate_{k}_not_false")
                    break

        speak = _read_json(speak_p)
        if speak.get("tts_invoked") is not False:
            blockers.append("tts_invoked_not_false")
        if speak.get("speech_output_committed") is not False:
            blockers.append("speech_output_committed_not_false")
        all_phrase_text = json.dumps(speak.get("phrases") or [], ensure_ascii=False)
        for forbidden in FORBIDDEN_SPEAK:
            if forbidden in all_phrase_text:
                blockers.append(f"forbidden_wording:{forbidden}")

        risk = _read_json(risk_p)
        for k in ("raw_ocr_text_preserved", "correction_candidate_not_fact", "no_navigation_decision"):
            if risk.get(k) is not True:
                blockers.append(f"risk_{k}_not_true")

        bench = _read_json(bench_p)
        if bench.get("current_phase_generates_benchmark_values") is not False:
            blockers.append("benchmark_generates_values_not_false")
        if bench.get("facility_semantic_accuracy_not_computed") is not True:
            blockers.append("facility_accuracy_not_computed_not_true")

        sim = _read_json(sim_p)
        if sim.get("simulation_profile_id") != "developer_full":
            blockers.append("simulation_profile_id_wrong")
        if sim.get("run_model") is not False:
            blockers.append("sim_run_model_not_false")

        nc = _read_json(nc_p)
        if nc.get("no_benchmark_or_accuracy_claim") is not True:
            blockers.append("non_claims_benchmark_missing")

        aud = _read_json(aud_p)
        for k, val in (
            ("ocr_mainline_invoked", False),
            ("rapidocr_invoked", False),
            ("paddleocr_invoked", False),
            ("model_correction_invoked", False),
            ("ai_interpretation_invoked", False),
            ("tts_invoked", False),
            ("midplatform_fact_written", False),
            ("scene_delta_written", False),
            ("world_model_written", False),
            ("navigation_decision_invoked", False),
            ("runtime_routing_changed", False),
        ):
            if aud.get(k) != val:
                blockers.append(f"audit_{k}_wrong")

    verdict = "GO" if not blockers else "NO_GO"
    report: Dict[str, Any] = {
        "schema": "public_facility_runtime_verifier_report_v0",
        "phase": "PublicFacility-Runtime-DryRun-001",
        "dryrun_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "verifier_output_root": str(vout),
    }
    _write_json(vout / "public_facility_runtime_verifier_report.json", report)
    print(json.dumps({"verdict": verdict, "blockers": blockers, "verifier_output_root": str(vout)}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
