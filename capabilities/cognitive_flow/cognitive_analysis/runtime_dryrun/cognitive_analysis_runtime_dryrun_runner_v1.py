"""Fixture-only Runner for the A3 Runtime Skeleton DryRun v1."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from ..runtime.cognitive_analysis_runtime_skeleton_v1 import CognitiveAnalysisRuntimeSkeletonV1
from ..runtime.cognitive_analysis_runtime_types_v1 import CognitiveAnalysisRuntimeRequestV1
from .cognitive_analysis_runtime_dryrun_serializer_v1 import serialize_json_v1, write_json_v1
from .cognitive_analysis_runtime_dryrun_types_v1 import (
    RUNTIME_SKELETON_DRYRUN_FIXTURE_REF_V1,
    RUNTIME_SKELETON_DRYRUN_PHASE_V1,
    RUNTIME_SKELETON_DRYRUN_RUN_ID_V1,
    CognitiveAnalysisRuntimeDryRunResultV1,
)


RUN_RESULT_FILENAME_V1 = "cognitive_analysis_runtime_dryrun_run_result_v1.json"
SUMMARY_FILENAME_V1 = "cognitive_analysis_runtime_dryrun_summary_v1.md"


def build_runtime_skeleton_request_fixture_v1() -> CognitiveAnalysisRuntimeRequestV1:
    """Create one fixed reference-only input; it is not a real Context or analysis."""
    return CognitiveAnalysisRuntimeRequestV1(
        context_ref="context:runtime_skeleton_dryrun",
        evidence_refs=("evidence:runtime_skeleton_dryrun",),
        hypothesis_refs=("hypothesis:runtime_skeleton_dryrun",),
        analysis_question_ref="analysis_question:runtime_skeleton_dryrun",
    )


def run_runtime_skeleton_dryrun_v1(
    output_dir: Path,
) -> CognitiveAnalysisRuntimeDryRunResultV1:
    """Call only the controlled Skeleton and serialize its zero-side-effect envelope."""
    request = build_runtime_skeleton_request_fixture_v1()
    skeleton_result = CognitiveAnalysisRuntimeSkeletonV1().execute(request)
    flags = skeleton_result.runtime_flags
    result = CognitiveAnalysisRuntimeDryRunResultV1(
        phase=RUNTIME_SKELETON_DRYRUN_PHASE_V1,
        run_id=RUNTIME_SKELETON_DRYRUN_RUN_ID_V1,
        request_fixture_ref=RUNTIME_SKELETON_DRYRUN_FIXTURE_REF_V1,
        runtime_authorization_status="NOT_AUTHORIZED",
        skeleton_result=skeleton_result,
        runtime_executed=flags.runtime_executed,
        simulation_only=flags.simulation_only,
        model_invoked=flags.model_invoked,
        network_invoked=flags.network_invoked,
        database_invoked=flags.database_invoked,
        state_writeback=flags.state_writeback,
        decision_executed=flags.decision_executed,
        external_invocation_observed=False,
        deterministic_serialization=False,
        warning_count=len(skeleton_result.warning_codes),
        blocker_count=0,
        final_candidate_decision="RUNTIME_SKELETON_DRYRUN_CANDIDATE_PASS",
        determinism_status="DETERMINISM_UNVERIFIED",
        determinism_evidence={},
        side_effect_evidence={
            "runtime_executed": "DECLARED_NOT_EXECUTED",
            "model_invoked": "DECLARED_NOT_EXECUTED",
            "network_invoked": "DECLARED_NOT_EXECUTED",
            "database_invoked": "DECLARED_NOT_EXECUTED",
            "external_invocation_observed": "DECLARED_NOT_EXECUTED",
            "state_writeback": "DECLARED_NOT_EXECUTED",
            "decision_executed": "DECLARED_NOT_EXECUTED",
        },
    )
    independent_request = build_runtime_skeleton_request_fixture_v1()
    independent_skeleton_result = CognitiveAnalysisRuntimeSkeletonV1().execute(independent_request)
    independent_result = CognitiveAnalysisRuntimeDryRunResultV1(
        **{**result.__dict__, "skeleton_result": independent_skeleton_result},
    )
    canonical_a = serialize_json_v1(result)
    canonical_b = serialize_json_v1(independent_result)
    deterministic = canonical_a == canonical_b
    input_digest = hashlib.sha256(serialize_json_v1(request).encode("utf-8")).hexdigest()
    proof = {
        "input_identity": RUNTIME_SKELETON_DRYRUN_FIXTURE_REF_V1,
        "input_digest": f"sha256:{input_digest}",
        "reconstruction_a": "independent_skeleton_reconstruction_a",
        "reconstruction_b": "independent_skeleton_reconstruction_b",
        "canonical_digest_a": f"sha256:{hashlib.sha256(canonical_a.encode('utf-8')).hexdigest()}",
        "canonical_digest_b": f"sha256:{hashlib.sha256(canonical_b.encode('utf-8')).hexdigest()}",
        "comparison": "MATCH" if deterministic else "MISMATCH",
    }
    result = CognitiveAnalysisRuntimeDryRunResultV1(
        **{
            **result.__dict__,
            "deterministic_serialization": deterministic,
            "determinism_status": "DETERMINISM_VERIFIED" if deterministic else "DETERMINISM_UNVERIFIED",
            "determinism_evidence": proof,
        },
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    write_json_v1(output_dir / RUN_RESULT_FILENAME_V1, result)
    (output_dir / SUMMARY_FILENAME_V1).write_text(
        "# A3 Runtime Skeleton DryRun\n\n"
        f"runtime_executed: {result.runtime_executed}\n"
        f"simulation_only: {result.simulation_only}\n"
        f"blocker_count: {result.blocker_count}\n",
        encoding="utf-8",
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    print(serialize_json_v1(run_runtime_skeleton_dryrun_v1(Path(args.output_dir))))


if __name__ == "__main__":
    main()
