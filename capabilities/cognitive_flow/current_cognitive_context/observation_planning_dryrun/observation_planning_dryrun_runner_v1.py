"""Fixed declaration runner; never executes observation."""
from __future__ import annotations
import argparse
from dataclasses import asdict
from pathlib import Path
from typing import Mapping
from .observation_planning_types_v1 import ObservationPlanningCandidateV1
from .observation_planning_serializer_v1 import canonical_json_dumps_v1, write_canonical_json_v1

_CASES = (
    ("navigation_context", "navigation_context", "transition_observation"),
    ("home_context", "social_context", "task_observation"),
    ("workplace_context", "task_context", "risk_observation"),
    ("unknown_field_context", "unknown_environment_context", "uncertainty_reduction_observation"),
    ("risk_context", "risk_awareness_context", "survival_observation"),
    ("goal_change_context", "exploration_context", "task_observation"),
)

def _once_v1() -> Mapping[str, object]:
    cases = []
    for case_id, context_type, observation_type in _CASES:
        candidate = ObservationPlanningCandidateV1("plan:" + case_id, observation_type, "context:" + context_type, "field:" + case_id, "attention:" + case_id, "goal:" + case_id, "survival:" + case_id, "gap:" + case_id, "provenance:" + case_id, "trace:observation-plan:" + case_id)
        cases.append({"case_id": case_id, "candidate": asdict(candidate)})
    return {"schema_version":"luna.context_driven_observation_planning_dryrun.v1","cases":cases,"runtime_flags":{"dryrun_executed":True,"fixture_only":True,"simulation_only":True,"runtime_executed":False,"model_invoked":False,"provider_invoked":False,"sensor_invoked":False,"observation_executed":False,"decision_created":False,"action_created":False,"permission_granted":False,"memory_updated":False,"learning_integrated":False,"hive_integrated":False,"reducer_integrated":False,"state_mutation":False}}

def run_observation_planning_dryrun_v1(output_dir: Path) -> Mapping[str, object]:
    one, two = _once_v1(), _once_v1(); payload = dict(one); payload["case_count"] = len(one["cases"]); payload["deterministic_run2_equal"] = canonical_json_dumps_v1(one) == canonical_json_dumps_v1(two); output_dir.mkdir(parents=True, exist_ok=True); write_canonical_json_v1(output_dir / "observation_planning_dryrun_result_v1.json", payload); return payload

def main() -> None:
    p=argparse.ArgumentParser(); p.add_argument("--output-dir",required=True,type=Path); a=p.parse_args(); r=run_observation_planning_dryrun_v1(a.output_dir); print(canonical_json_dumps_v1({"case_count":r["case_count"],"deterministic_run2_equal":r["deterministic_run2_equal"]}))
if __name__ == "__main__": main()
