"""User-terminal-only V2 verifier for Capability Reallocation Candidate v1."""
from __future__ import annotations
import argparse, json, os, subprocess, sys
from pathlib import Path
def root() -> Path:
    for p in (Path.cwd(), Path(__file__).absolute().parents[3], Path(__file__).resolve().parents[3]):
        if (p / "cognitive/contracts").is_dir(): return p
    raise RuntimeError("Luna workspace root unavailable")
ROOT=root(); RUNNER=ROOT/"cognitive/validation/run_capability_reallocation_candidate_v1.py"; VERIFIER=ROOT/"cognitive/validation/verify_capability_reallocation_candidate_result_v1.py"
CASES=("case_a_ocr_good","case_b_ocr_degraded","case_c_ocr_unavailable")
REQUIRED=(RUNNER,VERIFIER,ROOT/"cognitive/neural/capability_reallocation.py",ROOT/"cognitive/middleware/capability_reallocation.py",ROOT/"cognitive/validation/capability_reallocation_candidate_trace_schema_v1.json",ROOT/"docs/architecture/cognitive_flow/cognitive_capability_reallocation_candidate_go_no_go_v1.md")
def run(cmd: list[str]) -> tuple[int,str]:
    env=dict(os.environ); env["PYTHONDONTWRITEBYTECODE"]="1"; p=subprocess.run(cmd,cwd=ROOT,env=env,text=True,capture_output=True); return p.returncode,p.stdout+p.stderr
def main() -> int:
    a=argparse.ArgumentParser(); a.add_argument("--output-dir",required=True); args=a.parse_args(); out=Path(args.output_dir); out.mkdir(parents=True,exist_ok=True); fails=[]; checks=0
    for f in REQUIRED:
        checks+=1
        if not f.is_file(): fails.append(f"missing required file: {f.relative_to(ROOT)}")
    checks+=1
    try: json.loads((ROOT/"cognitive/validation/capability_reallocation_candidate_trace_schema_v1.json").read_text())
    except Exception as exc: fails.append(f"trace schema parse failure: {type(exc).__name__}")
    for case in CASES:
        x=out/f"{case}-a.json"; y=out/f"{case}-b.json"
        for target in (x,y):
            code,msg=run([sys.executable,str(RUNNER),"--scenario",case,"--output",str(target)]); checks+=1
            if code: fails.append(f"runner failed for {case}: {msg.strip()}")
        code,msg=run([sys.executable,str(VERIFIER),"--input",str(x),"--replay",str(y)]); checks+=1
        if code or "FINAL_DECISION: COMPONENT_VALIDATION_PASSED" not in msg: fails.append(f"component validation failed for {case}: {msg.strip()}")
    n=len(fails); print(f"CHECKS: {checks}"); print(f"FAILED_CHECKS: {fails}"); print(f"PASSED_CHECK_COUNT: {checks-n}"); print(f"FAILED_CHECK_COUNT: {n}"); print(f"BLOCKER_COUNT: {n}"); print(f"FINAL_DECISION: {'V2_FINAL_VERIFICATION_PASSED' if not n else 'BLOCKED_BY_VERIFIER_FAILURE'}"); print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT" if not n else "NEXT: REMEDIATE_REPORTED_FAILURES_ONLY"); return 0 if not n else 1
if __name__ == "__main__": raise SystemExit(main())
