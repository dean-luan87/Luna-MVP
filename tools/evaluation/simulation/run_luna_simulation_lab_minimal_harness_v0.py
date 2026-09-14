#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Luna-Simulation-Lab-Minimal-Harness-001 — Materialize Simulation Lab run context.

Default: NO model execution. NO runtime wiring. NO routing changes.
Optional: --execute-child runs a user-supplied command (manual, explicit only).
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ALLOWED_PROFILES = frozenset({"developer_full", "crash_recovery"})


def _find_workspace(start: Path) -> Path:
    for p in [start, *start.parents]:
        if (p / "configs/evaluation/simulation/luna_simulation_lab_profiles_v0.example.json").is_file():
            return p.resolve()
    raise SystemExit(
        "ERROR: cannot locate workspace root (missing configs/evaluation/simulation/luna_simulation_lab_profiles_v0.example.json)"
    )


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _load_profile(profiles_path: Path, profile_id: str) -> Dict[str, Any]:
    cfg = _read_json(profiles_path)
    for row in cfg.get("profiles") or []:
        if isinstance(row, dict) and str(row.get("profile_id") or "") == profile_id:
            return row
    raise SystemExit(f"ERROR: profile_id not found in {profiles_path}: {profile_id}")


def _host_resource_snapshot() -> Dict[str, Any]:
    out: Dict[str, Any] = {"schema": "luna_simulation_lab_resource_report_v0", "sampled_at_utc": _utc_now()}
    try:
        import psutil  # type: ignore

        vm = psutil.virtual_memory()
        out["memory_total_mb"] = round(vm.total / (1024 * 1024), 2)
        out["memory_available_mb"] = round(vm.available / (1024 * 1024), 2)
        out["cpu_count_logical"] = psutil.cpu_count(logical=True)
        out["cpu_percent"] = psutil.cpu_percent(interval=0.1)
    except Exception as e:
        out["psutil_error"] = f"{type(e).__name__}: {e}"
    return out


def _utc_now() -> str:
    return _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _crash_recovery_enabled(profile: Dict[str, Any]) -> bool:
    fi = profile.get("fault_injection") if isinstance(profile.get("fault_injection"), dict) else {}
    return bool(fi.get("enable_subprocess_kill") or fi.get("simulate_exit_139"))


def _suggest_batch_recovery_cmd(workspace: Path, profile_id: str) -> Optional[str]:
    if profile_id != "crash_recovery":
        return None
    core = workspace
    if (workspace / "tools").is_symlink():
        core = (workspace / "tools").resolve().parent
    mat = os.environ.get(
        "LUNA_PADDLEOCR_MATERIALIZE_ROOT",
        "/Users/luanlei/LunaRuntime/logs/evaluation/paddleocr_manifest_v1_cache_materialize_001_20260512_071635Z",
    )
    pinned = os.path.join(mat, "snapshot/paddleocr_manifest_v1_pinned_manifest_candidate.json")
    manifest = str(core / "configs/evaluation/ocr/paddleocr_labeled_set_manifest_v0.example.json")
    out = workspace / "_eval_out" / "paddleocr_labeled_set_batch_recovery_v0_bs5_simlab_crash_recovery"
    return (
        f"python3 {core}/tools/evaluation/ocr/run_paddleocr_labeled_set_batch_recovery_v0.py "
        f"--repo-root {core} "
        f"--materialize-root {mat} "
        f"--pinned-manifest {pinned} "
        f"--labeled-set-manifest {manifest} "
        f"--batch-size 5 "
        f"--output-root {out}"
    )


def _parse_child_result(
    proc: subprocess.CompletedProcess[str],
) -> Tuple[Optional[int], Optional[int], Optional[float]]:
    exit_code = int(proc.returncode) if proc.returncode is not None else None
    signal = None
    if exit_code is not None and exit_code < 0:
        signal = -exit_code
    rss_mb = None
    return exit_code, signal, rss_mb


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace-root", default="", help="Luna-Workspace-Min (or repo with simulation configs)")
    ap.add_argument("--profile-id", required=True, choices=sorted(ALLOWED_PROFILES))
    ap.add_argument(
        "--profiles-config",
        default="configs/evaluation/simulation/luna_simulation_lab_profiles_v0.example.json",
    )
    ap.add_argument(
        "--harness-config",
        default="configs/evaluation/simulation/luna_simulation_lab_minimal_harness_v0.example.json",
    )
    ap.add_argument("--output-root", default="", help="Default: <workspace>/_eval_out/simulation_lab_minimal_harness_v0/<profile_id>")
    ap.add_argument(
        "--execute-child",
        action="store_true",
        help="Explicitly run --child-cmd (NEVER default; not for CI)",
    )
    ap.add_argument("--child-cmd", default="", help="Shell command to run under this profile context")
    ap.add_argument("--batch-size", type=int, default=0, help="Recorded into simulation_summary when child runs")
    ap.add_argument("--crash-sample-ref", default="", help="Path or id ref after child crash")
    ap.add_argument("--merge-child-summary", default="", help="Optional batch_recovery simulation_summary path to merge fields")
    args = ap.parse_args()

    ws = _find_workspace(Path(args.workspace_root).expanduser().resolve() if args.workspace_root.strip() else Path(__file__).resolve().parents[3])
    profiles_path = (ws / args.profiles_config).resolve()
    profile = _load_profile(profiles_path, args.profile_id)

    if args.output_root.strip():
        out_root = Path(args.output_root).expanduser().resolve()
    else:
        out_root = (ws / "_eval_out" / "simulation_lab_minimal_harness_v0" / args.profile_id).resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    profile_ref = f"{profiles_path}#profile_id={args.profile_id}"
    crash_en = _crash_recovery_enabled(profile)
    suggested = _suggest_batch_recovery_cmd(ws, args.profile_id)

    child_ran = False
    exit_code: Optional[int] = None
    signal: Optional[int] = None
    rss_mb: Optional[float] = None
    batch_size = int(args.batch_size) if args.batch_size > 0 else None
    crash_sample_ref = args.crash_sample_ref.strip() or None

    if args.execute_child:
        if not args.child_cmd.strip():
            if args.profile_id == "crash_recovery" and suggested:
                raise SystemExit(
                    "ERROR: --execute-child requires --child-cmd (suggested command printed in notes.md only; not auto-run)"
                )
            raise SystemExit("ERROR: --execute-child requires non-empty --child-cmd")
        child_ran = True
        proc = subprocess.run(args.child_cmd, shell=True, cwd=str(ws), capture_output=True, text=True)
        exit_code, signal, rss_mb = _parse_child_result(proc)
        err_tail = (proc.stderr or "")[-4000:]
        _write_json(
            out_root / "child_run_capture.json",
            {
                "schema": "luna_simulation_lab_child_run_capture_v0",
                "command": args.child_cmd,
                "exit_code": exit_code,
                "signal": signal,
                "stderr_tail": err_tail,
            },
        )

    if args.merge_child_summary.strip():
        mp = Path(args.merge_child_summary).expanduser().resolve()
        if mp.is_file():
            merged = _read_json(mp)
            if isinstance(merged, dict):
                exit_code = merged.get("exit_code", exit_code)
                signal = merged.get("signal", signal)
                batch_size = merged.get("batch_size", batch_size)
                crash_sample_ref = merged.get("crash_sample_ref", crash_sample_ref)

    summary: Dict[str, Any] = {
        "schema": "luna_simulation_lab_run_summary_v0",
        "phase": "Phase-Luna-Simulation-Lab-Minimal-Harness-001",
        "simulation_profile_id": args.profile_id,
        "simulation_profile_ref": profile_ref,
        "simulation_output_root": str(out_root),
        "profiles_config": str(profiles_path),
        "harness_schema": "luna_simulation_lab_minimal_harness_v0",
        "run_model": child_ran,
        "manual_trigger_only": True,
        "crash_recovery_enabled": crash_en,
        "exit_code": exit_code,
        "signal": signal,
        "rss_mb": rss_mb,
        "batch_size": batch_size,
        "crash_sample_ref": crash_sample_ref,
        "suggested_child_command": suggested,
        "updated_at_utc": _utc_now(),
        "disclaimer": "Mac Simulation Lab is engineering screening only; not hardware or performance certification.",
    }
    _write_json(out_root / "simulation_summary.json", summary)

    resource = _host_resource_snapshot()
    resource["simulation_profile_id"] = args.profile_id
    resource["simulation_output_root"] = str(out_root)
    _write_json(out_root / "resource_report.json", resource)

    audit = {
        "schema": "luna_simulation_lab_audit_report_v0",
        "simulation_profile_id": args.profile_id,
        "runtime_integration": False,
        "ocr_routing_changed": False,
        "rapidocr_replaced": False,
        "network_request_invoked": child_ran,
        "model_invoked": child_ran,
        "forbidden_runtime_changes_respected": True,
        "forbidden_runtime_changes": profile.get("forbidden_runtime_changes") or [],
        "ci_auto_run": False,
    }
    _write_json(out_root / "audit_report.json", audit)

    notes_lines = [
        f"# Simulation Lab minimal harness — `{args.profile_id}`",
        "",
        f"- **output_root**: `{out_root}`",
        f"- **profile_ref**: `{profile_ref}`",
        "- **default**: no model run; materialize context only",
        "- **not**: hardware cert, performance cert, or long-run cert",
        "",
        "## Manual child run (optional)",
        "",
        "To run a child command under this profile (explicit only):",
        "",
        "```bash",
        "python3 tools/evaluation/simulation/run_luna_simulation_lab_minimal_harness_v0.py \\",
        f"  --workspace-root {ws} \\",
        f"  --profile-id {args.profile_id} \\",
        f"  --output-root {out_root} \\",
        '  --execute-child \\',
        '  --child-cmd "<your command>"',
        "```",
        "",
    ]
    if suggested:
        notes_lines.extend(
            [
                "## Suggested batch recovery (crash_recovery; do not run from CI)",
                "",
                "```bash",
                suggested,
                "```",
                "",
                "After run, merge with:",
                "",
                "```bash",
                "python3 tools/evaluation/simulation/run_luna_simulation_lab_minimal_harness_v0.py \\",
                f"  --workspace-root {ws} \\",
                "  --profile-id crash_recovery \\",
                f"  --output-root {out_root} \\",
                "  --merge-child-summary <path/to/batch_recovery_summary.json>",
                "```",
                "",
            ]
        )
    (out_root / "notes.md").write_text("\n".join(notes_lines) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "simulation_output_root": str(out_root),
                "simulation_profile_id": args.profile_id,
                "run_model": child_ran,
                "simulation_summary": str(out_root / "simulation_summary.json"),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
