#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Luna-Simulation-Lab-Minimal-Harness-001 — Static verifier for minimal harness docs, config, scripts, runner.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]


def _find_workspace(start: Path) -> Path:
    for p in [start, *start.parents]:
        if (p / "configs/evaluation/simulation/luna_simulation_lab_minimal_harness_v0.example.json").is_file():
            return p.resolve()
    return start.resolve()


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace-root", default="")
    ap.add_argument("--output-root", default="")
    args = ap.parse_args()

    ws = _find_workspace(Path(args.workspace_root).expanduser().resolve() if args.workspace_root.strip() else REPO_ROOT)
    if args.output_root.strip():
        out_root = Path(args.output_root).expanduser().resolve()
    else:
        out_root = (ws / "_eval_out" / "luna_simulation_lab_minimal_harness_verify_v0").resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    blockers: List[str] = []

    doc = ws / "docs/architecture/evaluation/LUNA_SIMULATION_LAB_MINIMAL_HARNESS_V0.md"
    annex = ws / "docs/architecture/evaluation/LUNA_EVALUATION_OCR_SIMULATION_LAB_CONTEXT_SCHEMA_ANNEX_V0.md"
    for p, tag in [(doc, "minimal_harness_doc"), (annex, "ocr_schema_annex")]:
        if not p.is_file():
            blockers.append(f"missing:{p.relative_to(ws)}")
        else:
            t = p.read_text(encoding="utf-8")
            if tag == "minimal_harness_doc" and "developer_full" not in t:
                blockers.append("harness_doc_missing_developer_full")
            if tag == "minimal_harness_doc" and "crash_recovery" not in t:
                blockers.append("harness_doc_missing_crash_recovery")
            if "manual" not in t.lower() and tag == "minimal_harness_doc":
                blockers.append("harness_doc_missing_manual_trigger_note")

    runner = ws / "tools/evaluation/simulation/run_luna_simulation_lab_minimal_harness_v0.py"
    if not runner.is_file():
        blockers.append("missing_runner")

    for sh in (
        "scripts/simulation/run_simulation_lab_developer_full_v0.sh",
        "scripts/simulation/run_simulation_lab_crash_recovery_v0.sh",
    ):
        if not (ws / sh).is_file():
            blockers.append(f"missing:{sh}")

    compose = ws / "scripts/simulation/docker-compose.minimal-harness.v0.yml"
    if not compose.is_file():
        blockers.append("missing:docker-compose.minimal-harness.v0.yml")

    cfg_p = ws / "configs/evaluation/simulation/luna_simulation_lab_minimal_harness_v0.example.json"
    if not cfg_p.is_file():
        blockers.append("missing_harness_config")
    else:
        cfg = _read_json(cfg_p)
        allowed = cfg.get("allowed_profile_ids") or []
        if "developer_full" not in allowed or "crash_recovery" not in allowed:
            blockers.append("harness_config_allowed_profiles_incomplete")
        if cfg.get("default_run_model") is not False:
            blockers.append("harness_config_must_default_run_model_false")

    readme = ws / "docs/architecture/README.md"
    if readme.is_file():
        rt = readme.read_text(encoding="utf-8")
        if "Phase-Luna-Simulation-Lab-Minimal-Harness-001" not in rt:
            blockers.append("readme_missing_minimal_harness_phase")
    else:
        blockers.append("missing_architecture_readme")

    # Dry-run materialize both profiles (no model)
    if not blockers and runner.is_file():
        import subprocess

        for pid in ("developer_full", "crash_recovery"):
            pr = out_root / f"_probe_{pid}"
            r = subprocess.run(
                [
                    sys.executable,
                    str(runner),
                    "--workspace-root",
                    str(ws),
                    "--profile-id",
                    pid,
                    "--output-root",
                    str(pr),
                ],
                cwd=str(ws),
                capture_output=True,
                text=True,
            )
            if r.returncode != 0:
                blockers.append(f"runner_probe_failed:{pid}")
                continue
            sp = pr / "simulation_summary.json"
            if not sp.is_file():
                blockers.append(f"missing_simulation_summary:{pid}")
                continue
            sm = _read_json(sp)
            for fld in (
                "simulation_profile_id",
                "simulation_profile_ref",
                "simulation_output_root",
                "crash_recovery_enabled",
            ):
                if fld not in sm:
                    blockers.append(f"summary_missing_field:{pid}:{fld}")
            if sm.get("run_model") is not False:
                blockers.append(f"summary_run_model_must_be_false_by_default:{pid}")

    verdict = "NO_GO" if blockers else "GO"
    rep = {
        "schema": "luna_simulation_lab_minimal_harness_verifier_report_v0",
        "phase": "Phase-Luna-Simulation-Lab-Minimal-Harness-001",
        "verdict": verdict,
        "workspace_root": str(ws),
        "output_root": str(out_root),
        "blockers": sorted(set(blockers)),
    }
    _write_json(out_root / "luna_simulation_lab_minimal_harness_verifier_report.json", rep)
    print(json.dumps({"verifier_output_root": str(out_root), "verdict": verdict, "blockers": rep["blockers"]}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
