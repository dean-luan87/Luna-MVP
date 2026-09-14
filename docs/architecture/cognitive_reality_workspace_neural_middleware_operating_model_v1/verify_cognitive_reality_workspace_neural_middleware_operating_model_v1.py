#!/usr/bin/env python3
"""V2 static verifier for the Reality Workspace operating model phase."""
from pathlib import Path

FLOW = "docs/architecture/cognitive_flow"
REQ = {
    "reality_workspace_operating_model_v1.md": ["Reality Workspace", "Neural System", "Middleware", "Normal operating loop", "Brain Driven Observation", "Neural Driven Monitoring", "Immediate State", "Working Reality", "Stable Reality Pattern"],
    "neural_system_responsibility_model_v1.md": ["high-frequency", "state refresh", "attention maintenance", "resource allocation", "anomaly detection", "Escalation Candidate", "does not own Goal", "Decision Authority"],
    "workspace_neural_interaction_contract_v1.md": ["Capability → Evidence → Reality Workspace → Neural Processing → Workspace Update", "Unknown ↑", "Risk ↑", "Conflict ↑", "Brain Evaluation", "Reducer remains the sole State mutation authority"],
    "middleware_cognitive_bridge_contract_v1.md": ["Capability Registry", "Model Manager", "Protocol Manager", "Diagnostics", "Resource Management", "Cognitive Requirement", "Capability Requirement", "does not understand the world"],
    "cognitive_escalation_protocol_v1.md": ["Escalation Candidate", "unknown_growth", "risk_increase", "conflict_detected", "capability_shortfall", "resource_stress", "temporal_change", "Brain Evaluation"],
    "background_monitoring_model_v1.md": ["Background Monitoring", "Immediate State", "Working Reality", "Stable Reality Pattern", "Escalation Candidate", "does not execute Action"],
    "cognitive_process_manager_positioning_v1.md": ["Cognitive Process Manager", "Task Thread", "Attention Thread", "Monitoring Thread", "Background Thread", "not a Scheduler Runtime", "cannot create an independent Goal"],
    "reality_workspace_runtime_boundary_v1.md": ["not a Runtime", "No Runtime Execution", "No Scheduler implementation", "No real model", "no OCR", "no SLAM", "no Hardware", "no Action Runtime"],
    "operating_model_go_no_go_v1.md": ["Brain Driven Observation", "Neural Driven Monitoring", "Escalation Candidate", "Middleware", "Reducer remains the sole State mutation authority", "No real model", "no OCR", "no SLAM", "WAITING_FOR_USER_TERMINAL_VERIFICATION"],
}


def main():
    root = next((p for p in [Path.cwd(), *Path(__file__).absolute().parents] if (p / FLOW).is_dir()), Path.cwd())
    failures = []
    checks = 0
    for name, terms in REQ.items():
        checks += 1
        path = root / FLOW / name
        if not path.is_file():
            failures.append(f"missing required file: {name}")
            continue
        text = path.read_text()
        for term in terms:
            checks += 1
            if term not in text:
                failures.append(f"missing required contract term: {term} in {name}")
    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failures}")
    print(f"PASSED_CHECK_COUNT: {checks - len(failures)}")
    print(f"FAILED_CHECK_COUNT: {len(failures)}")
    print(f"BLOCKER_COUNT: {len(failures)}")
    if failures:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
