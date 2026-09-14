#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Luna-Simulation-Lab-001 — Static verifier for Luna Simulation Lab docs + profile example JSON.

No model execution; no runtime wiring; no routing changes.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _require_repo(p: str) -> Path:
    pp = Path(p).expanduser().resolve()
    if not pp.is_dir():
        raise SystemExit(f"ERROR: --repo-root must be directory: {p}")
    return pp


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


DOCS: List[Tuple[str, Path]] = [
    ("overview", Path("docs/architecture/evaluation/LUNA_SIMULATION_LAB_OVERVIEW_V0.md")),
    ("profile_standard", Path("docs/architecture/evaluation/LUNA_SIMULATION_LAB_PROFILE_STANDARD_V0.md")),
    ("resource", Path("docs/architecture/evaluation/LUNA_SIMULATION_LAB_RESOURCE_SIMULATION_POLICY_V0.md")),
    ("input_sensor", Path("docs/architecture/evaluation/LUNA_SIMULATION_LAB_INPUT_SENSOR_SIMULATION_POLICY_V0.md")),
    ("fault_interrupt", Path("docs/architecture/evaluation/LUNA_SIMULATION_LAB_FAULT_AND_INTERRUPT_SIMULATION_POLICY_V0.md")),
    ("stcm", Path("docs/architecture/evaluation/LUNA_SIMULATION_LAB_STCM_SIMULATION_POLICY_V0.md")),
    ("go_pack", Path("docs/architecture/evaluation/LUNA_SIMULATION_LAB_GO_NO_GO_PACK_V0.md")),
]

HARDWARE_DISCLAIMER_RE = re.compile(
    r"(不等同真实硬件|不等价于真实硬件|不是真实硬件认证|工程筛选环境|后置必须环节|真实硬件验证)",
)

FORBIDDEN_EQUIV_RE = re.compile(
    r"(Mac\s*模拟\s*(完全)?等价\s*真实硬件|等同真实硬件认证|模拟环境\s*等同于\s*量产)",
    re.I,
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=str(REPO_ROOT))
    ap.add_argument("--output-root", default="", help="Default: <repo-root>/_eval_out/luna_simulation_lab_v0")
    args = ap.parse_args()

    repo = _require_repo(args.repo_root)
    if args.output_root.strip():
        out_root = Path(args.output_root).expanduser().resolve()
    else:
        out_root = (repo / "_eval_out" / "luna_simulation_lab_v0").resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    blockers: List[str] = []
    soft_followups: List[str] = []

    for _, rel in DOCS:
        p = repo / rel
        if not p.is_file():
            blockers.append(f"missing_doc:{rel.as_posix()}")
            continue
        txt = p.read_text(encoding="utf-8")
        if FORBIDDEN_EQUIV_RE.search(txt):
            blockers.append(f"doc_forbidden_hardware_equivalence_claim:{rel.name}")
        if not HARDWARE_DISCLAIMER_RE.search(txt):
            blockers.append(f"doc_missing_hardware_disclaimer:{rel.name}")

    readme = repo / "docs/architecture/README.md"
    if not readme.is_file():
        blockers.append("missing_architecture_readme")
    else:
        rtx = readme.read_text(encoding="utf-8")
        if "Phase-Luna-Simulation-Lab-001" not in rtx:
            blockers.append("readme_missing_phase_luna_simulation_lab_001")
        if "LUNA_SIMULATION_LAB_OVERVIEW_V0.md" not in rtx:
            blockers.append("readme_missing_simulation_lab_overview_link")

    ov = repo / DOCS[0][1]
    if ov.is_file():
        ovt = ov.read_text(encoding="utf-8")
        if "Evaluation Test Board" not in ovt and "Test Board" not in ovt:
            blockers.append("overview_missing_test_board_relation")
        if "SIGSEGV" not in ovt and "exit 139" not in ovt.lower():
            blockers.append("overview_missing_paddleocr_exit139_relation")

    cfg_p = repo / "configs/evaluation/simulation/luna_simulation_lab_profiles_v0.example.json"
    profiles: List[Dict[str, Any]] = []
    if not cfg_p.is_file():
        blockers.append("missing_config:configs/evaluation/simulation/luna_simulation_lab_profiles_v0.example.json")
    else:
        cfg = _read_json(cfg_p)
        if str(cfg.get("schema_version") or "") != "luna_simulation_lab_profiles_v0":
            blockers.append("bad_config_schema_version")
        pr = cfg.get("profiles")
        if not isinstance(pr, list):
            blockers.append("profiles_not_array")
        else:
            profiles = [x for x in pr if isinstance(x, dict)]
            if len(profiles) < 10:
                blockers.append(f"profiles_count_below_10:got={len(profiles)}")
            ids = [str(p.get("profile_id") or "") for p in profiles]
            if "developer_full" not in ids:
                blockers.append("missing_profile:developer_full")
            if not any("low_memory" in i for i in ids):
                blockers.append("missing_profile_family:low_memory")
            if not any("low_cpu" in i for i in ids):
                blockers.append("missing_profile_family:low_cpu")
            if "offline" not in ids:
                blockers.append("missing_profile:offline")
            if not any("network_unstable" in i for i in ids):
                blockers.append("missing_profile_family:network_unstable")
            if not any("long_run" in i for i in ids):
                blockers.append("missing_profile_family:long_run")
            if "crash_recovery" not in ids:
                blockers.append("missing_profile:crash_recovery")
            if "stcm_deadline_stress" not in ids:
                blockers.append("missing_profile:stcm_deadline_stress")

            for p in profiles:
                pid = str(p.get("profile_id") or "")
                if not pid:
                    blockers.append("profile_missing_profile_id")
                    continue
                if not isinstance(p.get("resource_limits"), dict):
                    blockers.append(f"profile_missing_resource_limits:{pid}")
                ed = p.get("expected_degradation")
                if not isinstance(ed, list) or len(ed) < 1:
                    blockers.append(f"profile_missing_expected_degradation:{pid}")
                ra = p.get("required_artifacts")
                if not isinstance(ra, list) or len(ra) < 1:
                    blockers.append(f"profile_missing_required_artifacts:{pid}")
                if not isinstance(p.get("forbidden_runtime_changes"), list):
                    blockers.append(f"profile_missing_forbidden_runtime_changes:{pid}")

    profile_matrix = [
        {
            "profile_id": str(p.get("profile_id") or ""),
            "network_mode": str((p.get("network_policy") or {}).get("mode") or "") if isinstance(p.get("network_policy"), dict) else "",
            "memory_mb": (p.get("resource_limits") or {}).get("memory_mb") if isinstance(p.get("resource_limits"), dict) else None,
            "cpu_cores": (p.get("resource_limits") or {}).get("cpu_cores") if isinstance(p.get("resource_limits"), dict) else None,
        }
        for p in profiles
    ]

    gaps = [
        {
            "gap_id": "SIM-LAB-GAP-001",
            "description": "Real hardware certification lab remains mandatory post Mac Simulation Lab; Mac results are engineering screening only.",
            "severity": "high",
        },
        {
            "gap_id": "SIM-LAB-GAP-002",
            "description": "Executable harness (Docker Compose / UTM recipes / delay injectors) to be added in a follow-on phase.",
            "severity": "medium",
        },
        {
            "gap_id": "SIM-LAB-GAP-003",
            "description": "Cross-arch QEMU emulation is not authoritative for performance SLA (documented; enforce in reports).",
            "severity": "low",
        },
    ]

    if not blockers:
        soft_followups.append(
            "SOFT-001: Implement Docker/UTM harness scripts and pin input bundles for each profile (CONDITIONAL_GO acceptable until merged)."
        )

    verdict = "NO_GO" if blockers else "GO"
    hard_blockers = list(blockers)

    summary: Dict[str, Any] = {
        "schema": "luna_simulation_lab_summary_v0",
        "phase": "Phase-Luna-Simulation-Lab-001",
        "verdict": verdict,
        "repo_root": str(repo),
        "output_root": str(out_root),
        "profile_count": len(profiles),
        "blockers": sorted(set(blockers)),
        "soft_followups": soft_followups,
        "config_path": str(cfg_p) if cfg_p.is_file() else "",
    }
    _write_json(out_root / "luna_simulation_lab_summary.json", summary)
    _write_json(
        out_root / "luna_simulation_lab_profile_matrix.json",
        {"schema": "luna_simulation_lab_profile_matrix_v0", "rows": profile_matrix},
    )
    _write_json(out_root / "luna_simulation_lab_gap_report.json", {"schema": "luna_simulation_lab_gap_report_v0", "gaps": gaps})
    rep = {
        "schema": "luna_simulation_lab_verifier_report_v0",
        "phase": "Phase-Luna-Simulation-Lab-001",
        "verdict": verdict,
        "output_root": str(out_root),
        "blockers": sorted(set(blockers)),
        "hard_blockers": sorted(set(hard_blockers)),
        "soft_followups": soft_followups,
    }
    _write_json(out_root / "luna_simulation_lab_verifier_report.json", rep)

    print(json.dumps({"verifier_output_root": str(out_root), "verdict": verdict, "blockers": rep["blockers"]}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
