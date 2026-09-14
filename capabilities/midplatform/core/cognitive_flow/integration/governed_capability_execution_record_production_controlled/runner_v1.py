"""Controlled, repository-backed producer runner.

This runner performs declaration inspection only.  It does not load or invoke
any model, Provider, Observation, Action, or runtime.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from .yolo11n_producer_entry_v1 import produce_yolo11n_governed_execution_records_v1


def run_governed_record_production_v1(repo_root: Path) -> Dict[str, Any]:
    result = produce_yolo11n_governed_execution_records_v1(repo_root)
    return {
        "phase": "Phase-P1-Midplatform-Governed-Capability-Execution-Record-Production-v1-001",
        "status": result.status,
        "record_bundle_produced": result.bundle is not None,
        "missing_declarations": list(result.missing_declarations),
        "inventory": result.inventory.__dict__,
        "responsible_owners": list(result.responsible_owners),
        "source_refs": list(result.inventory.source_refs),
        "trace_refs": list(result.trace_refs),
        "provenance_refs": list(result.provenance_refs),
        "no_success_synthesized": result.no_success_synthesized,
        "runtime_execution": result.runtime_execution,
        "model_loading": result.model_loading,
        "provider_invocation": result.provider_invocation,
        "observation_execution": result.observation_execution,
        "action_execution": result.action_execution,
        "source_mutation": result.source_mutation,
        "world_truth_declared": result.world_truth_declared,
    }


def main() -> None:
    root = Path(__file__).resolve().parents[6]
    output = run_governed_record_production_v1(root)
    output_dir = root / "_eval_out/governed_capability_execution_record_production_controlled"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "governed_record_production_summary_v1.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
