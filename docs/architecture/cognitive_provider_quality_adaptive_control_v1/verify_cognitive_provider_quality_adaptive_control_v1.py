"""User-terminal-only V2 verifier for Provider Quality and Adaptive Control v1."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys


def _locate_workspace_root() -> Path:
    """Prefer the invoking Luna workspace over the resolved docs symlink target."""
    candidates = (
        Path.cwd(),
        Path(__file__).absolute().parents[3],
        Path(__file__).resolve().parents[3],
    )
    for candidate in candidates:
        if (candidate / "cognitive").is_dir() and (candidate / "cognitive/contracts").is_dir():
            return candidate
    raise RuntimeError("unable to locate Luna workspace root containing cognitive/contracts")


ROOT = _locate_workspace_root()
RUNNER = ROOT / "cognitive/validation/run_provider_quality_adaptive_control_v1.py"
RESULT_VERIFIER = ROOT / "cognitive/validation/verify_provider_quality_adaptive_control_result_v1.py"
FIXTURE_ROOT = ROOT / "cognitive/validation/fixtures/real_ocr_v1"
REQUIRED_FILES = (
    ROOT / "cognitive/neural/provider_quality_adaptive_control.py",
    ROOT / "cognitive/validation/provider_quality_adaptive_control_skeleton.py",
    ROOT / "cognitive/validation/run_provider_quality_adaptive_control_v1.py",
    ROOT / "cognitive/validation/verify_provider_quality_adaptive_control_result_v1.py",
    ROOT / "cognitive/validation/provider_quality_adaptive_control_trace_schema_v1.json",
    ROOT / "docs/architecture/cognitive_flow/cognitive_provider_quality_adaptive_control_architecture_v1.md",
    ROOT / "docs/architecture/cognitive_flow/cognitive_neural_provider_quality_assessment_model_v1.md",
    ROOT / "docs/architecture/cognitive_flow/cognitive_provider_adaptive_control_boundary_v1.md",
    ROOT / "docs/architecture/cognitive_flow/cognitive_provider_quality_adaptive_control_go_no_go_v1.md",
)
CASES = ("case_e_clear_gate_b12", "case_c_low_quality", "case_d_no_text")


def _run(command: list[str]) -> tuple[int, str]:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(command, cwd=ROOT, env=environment, text=True, capture_output=True, check=False)
    return result.returncode, result.stdout + result.stderr


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []
    checks = 0
    for path in REQUIRED_FILES:
        checks += 1
        if not path.is_file():
            failures.append(f"missing required file: {path.relative_to(ROOT)}")
    checks += 1
    try:
        json.loads((ROOT / "cognitive/validation/provider_quality_adaptive_control_trace_schema_v1.json").read_text(encoding="utf-8"))
    except Exception as exc:
        failures.append(f"trace schema parse failure: {type(exc).__name__}")
    for case in CASES:
        fixture = FIXTURE_ROOT / f"{case}.png"
        first = output_dir / f"{case}-a.json"
        replay = output_dir / f"{case}-b.json"
        for target in (first, replay):
            code, output = _run([sys.executable, str(RUNNER), "--fixture", str(fixture), "--output", str(target)])
            checks += 1
            if code != 0:
                failures.append(f"runner failed for {case}: {output.strip()}")
        code, output = _run([sys.executable, str(RESULT_VERIFIER), "--input", str(first), "--replay", str(replay)])
        checks += 1
        if code != 0 or "FINAL_DECISION: COMPONENT_VALIDATION_PASSED" not in output:
            failures.append(f"component validation failed for {case}: {output.strip()}")
    blocker_count = len(failures)
    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failures}")
    print(f"PASSED_CHECK_COUNT: {checks - blocker_count}")
    print(f"FAILED_CHECK_COUNT: {blocker_count}")
    print(f"BLOCKER_COUNT: {blocker_count}")
    print(f"FINAL_DECISION: {'V2_FINAL_VERIFICATION_PASSED' if not failures else 'BLOCKED_BY_VERIFIER_FAILURE'}")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT" if not failures else "NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
