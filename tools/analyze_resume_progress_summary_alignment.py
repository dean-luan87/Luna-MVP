# -*- coding: utf-8 -*-
"""只读：对比关键 case 在 Resume Progress Summary Alignment 后的摘要字段。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from decision_monitor.builder import DecisionMonitorBuilder  # noqa: E402
from decision_monitor.narrative_evidence_tension_review import build_narrative_evidence_tension_review  # noqa: E402
from decision_monitor.run_summary_builder import build_run_summary_reference  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--ctx",
        nargs="*",
        default=[
            "R60_recovery_declared_but_resume_chain_fragile_real_ctx.json",
            "R82_phase_closure_progress_pair_near_critical_candidate_real_ctx.json",
            "R53_main_task_resumed_but_not_progressed_real_ctx.json",
            "R1_container_real_ctx.json",
        ],
    )
    ap.add_argument("--out", default=str(ROOT / "logs" / "resume_progress_summary_alignment_analysis.json"))
    args = ap.parse_args()
    ctx_dir = ROOT / "tests" / "real_scenarios" / "ctx"
    out_rows = []
    for name in args.ctx:
        p = ctx_dir / name
        if not p.is_file():
            print("missing", p, file=sys.stderr)
            return 1
        ctx = json.loads(p.read_text(encoding="utf-8"))
        d = DecisionMonitorBuilder().build(ctx).to_dict()
        rsr = build_run_summary_reference(d)
        if hasattr(rsr, "to_dict"):
            rsr = rsr.to_dict()
        net = build_narrative_evidence_tension_review(d)
        inp = d.get("inputs")
        if hasattr(inp, "to_dict"):
            inp = inp.to_dict()
        tcs = d.get("task_chain_state_snapshot")
        if hasattr(tcs, "to_dict"):
            tcs = tcs.to_dict()
        out_rows.append(
            {
                "ctx_file": name,
                "inputs_scenario_resume": inp.get("scenario_task_resume_target"),
                "inputs_recovery_frag_expected": inp.get("recovery_declared_but_resume_chain_fragile_expected"),
                "tcs_task_resume_target": tcs.get("task_resume_target"),
                "resume_main_progress_alignment_summary": tcs.get("resume_main_progress_alignment_summary"),
                "resume_chain_fragility_summary": rsr.get("resume_chain_fragility_summary"),
                "process_observation_summary": rsr.get("process_observation_summary"),
                "pc": net.phase_closure_outcome_tension,
                "lg": net.local_global_progress_tension,
            }
        )
    report = {"cases": out_rows}
    outp = Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("wrote:", outp, file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
