"""User-terminal runner for the controlled cognitive exploration sandbox."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from .cognitive_exploration_sandbox_v1 import run_controlled_cognitive_exploration_sandbox


OUTPUT_DIR = Path("_eval_out/controlled_cognitive_exploration_sandbox_v1_smoke_v0")


def _summary_markdown(trace: object) -> str:
    lines = [
        "# Controlled Cognitive Exploration Sandbox Trace Summary",
        "",
        f"Phase: `{trace.phase_id}`",
        f"Sandbox: `{trace.sandbox_version}`",
        f"Synthetic only: `{trace.synthetic_only}`",
        f"Scenario count: `{trace.scenario_count}`",
        "",
        "This is a human-review trace. Cognitive logic observations are not contract verdicts.",
        "",
    ]
    for scenario in trace.scenarios:
        round_zero = scenario.round_0
        lines.extend(
            [
                f"## {scenario.scenario_id} — {scenario.scenario_name}",
                "",
                f"Problem: `{scenario.scenario_metadata['problem']}`",
                f"Behavior class: `{scenario.expected_behavior_class}`",
                f"Round 0: needs={len(round_zero.information_needs)}, "
                f"branches={len(round_zero.branches)}, "
                f"admitted={len(round_zero.governance_result.admitted_branch_refs)}, "
                f"deferred={len(round_zero.governance_result.deferred_branch_refs)}, "
                f"rejected={len(round_zero.governance_result.rejected_branch_refs)}, "
                f"strategies={len(round_zero.strategy_candidates)}",
            ]
        )
        if scenario.simulated_return is not None:
            lines.append(
                "Simulated return: `SANDBOX_SIMULATED_ACQUISITION_RETURN` "
                f"coverage_additions={list(scenario.simulated_return.coverage_addition_refs)}`"
            )
        if scenario.round_1 is not None:
            round_one = scenario.round_1
            lines.append(
                f"Round 1: needs={len(round_one.information_needs)}, "
                f"branches={len(round_one.branches)}, "
                f"admitted={len(round_one.governance_result.admitted_branch_refs)}, "
                f"deferred={len(round_one.governance_result.deferred_branch_refs)}, "
                f"rejected={len(round_one.governance_result.rejected_branch_refs)}, "
                f"strategies={len(round_one.strategy_candidates)}"
            )
            lines.append(
                "Delta: "
                f"needs(-{len(scenario.cognitive_delta['needs_removed'])}/+{len(scenario.cognitive_delta['needs_added'])}), "
                f"branches(-{len(scenario.cognitive_delta['branches_removed'])}/+{len(scenario.cognitive_delta['branches_added'])}), "
                f"strategies(-{len(scenario.cognitive_delta['strategies_removed'])}/+{len(scenario.cognitive_delta['strategies_added'])})"
            )
        lines.extend(
            [
                f"Cognitive economy: `{scenario.cognitive_economy}`",
                f"Lineage valid: `{scenario.lineage_integrity}`",
                f"Cognitive logic observations: `{list(scenario.cognitive_logic_observations)}`",
                f"Boundary observations: `{list(scenario.boundary_observations)}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Aggregate",
            "",
            f"`{trace.aggregate_cognitive_economy}`",
            "",
            "The sandbox does not decide whether a scenario cognitively converged.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the controlled multi-scenario cognitive exploration sandbox."
    )
    parser.parse_args()
    trace = run_controlled_cognitive_exploration_sandbox()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "cognitive_trace.json").write_text(
        json.dumps(asdict(trace), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (OUTPUT_DIR / "cognitive_trace_summary.md").write_text(
        _summary_markdown(trace), encoding="utf-8"
    )
    print(json.dumps(asdict(trace), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()


__all__ = ["main", "OUTPUT_DIR"]
