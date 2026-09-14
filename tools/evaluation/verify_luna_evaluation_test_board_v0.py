#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-Luna-Evaluation-Test-Board-001 — Static verifier for Luna Evaluation & Test Board docs + example config.

No model execution; no runtime wiring; no routing changes.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

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
    ("overview", Path("docs/architecture/evaluation/LUNA_EVALUATION_TEST_BOARD_OVERVIEW_V0.md")),
    ("levels", Path("docs/architecture/evaluation/LUNA_EVALUATION_TEST_LEVELS_AND_GATE_POLICY_V0.md")),
    ("artifacts", Path("docs/architecture/evaluation/LUNA_EVALUATION_TEST_ARTIFACT_STANDARD_V0.md")),
    ("interrupt", Path("docs/architecture/evaluation/LUNA_EVALUATION_INTERRUPT_AND_RECOVERY_TEST_POLICY_V0.md")),
    ("long_run", Path("docs/architecture/evaluation/LUNA_EVALUATION_LONG_RUN_STABILITY_TEST_POLICY_V0.md")),
    ("task_type", Path("docs/architecture/evaluation/LUNA_EVALUATION_TASK_TYPE_PERFORMANCE_TEST_POLICY_V0.md")),
    ("stcm", Path("docs/architecture/evaluation/LUNA_EVALUATION_CROSS_MODAL_STCM_TEST_POLICY_V0.md")),
    ("admission", Path("docs/architecture/evaluation/LUNA_EVALUATION_MODULE_ADMISSION_TO_TEST_BOARD_V0.md")),
]

REQUIRED_LEVEL_KEYS: Tuple[str, ...] = (
    "level_0_static_contract",
    "level_1_smoke",
    "level_2_functional",
    "level_3_labeled_gt",
    "level_4_batch_recovery",
    "level_5_interrupt_cancellation",
    "level_6_long_run_stability",
    "level_7_task_type_performance",
    "level_8_cross_modal_stcm",
    "level_9_shadow_release_gate",
)

REQUIRED_ARTIFACT_GROUPS = ("base", "long_run", "interrupt", "stcm")

MIN_BASE: Set[str] = {
    "test_summary.json",
    "test_matrix.json",
    "metrics.json",
    "error_report.json",
    "audit_report.json",
    "notes.md",
    "verifier_report.json",
}

MIN_LONG_RUN: Set[str] = {
    "resource_timeseries.jsonl",
    "latency_timeseries.jsonl",
    "stability_report.json",
}

MIN_INTERRUPT: Set[str] = {
    "interrupt_trace.jsonl",
    "recovery_state.json",
    "cancellation_report.json",
}

MIN_STCM: Set[str] = {
    "stcm_event_trace.jsonl",
    "deadline_outcome_matrix.json",
    "stale_result_report.json",
    "voice_notice_report.json",
}

GLOBAL_MARKER_RE = re.compile(
    r"(非\s*OCR\s*专属|非\s*OCR\s*/\s*PaddleOCR\s*专属|Luna\s*全局|全局测试板块|跨模态)",
    re.I,
)


def _doc_global_marker_ok(text: str) -> bool:
    return GLOBAL_MARKER_RE.search(text) is not None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=str(REPO_ROOT))
    ap.add_argument("--output-root", default="", help="Default: <repo-root>/_eval_out/luna_evaluation_test_board_v0")
    args = ap.parse_args()

    repo = _require_repo(args.repo_root)
    if args.output_root.strip():
        out_root = Path(args.output_root).expanduser().resolve()
    else:
        out_root = (repo / "_eval_out" / "luna_evaluation_test_board_v0").resolve()
    out_root.mkdir(parents=True, exist_ok=True)

    blockers: List[str] = []
    soft_followups: List[str] = []

    for key, rel in DOCS:
        p = repo / rel
        if not p.is_file():
            blockers.append(f"missing_doc:{rel.as_posix()}")
            continue
        body = p.read_text(encoding="utf-8")
        if not _doc_global_marker_ok(body):
            blockers.append(f"doc_missing_global_non_ocr_marker:{rel.name}")

    readme = repo / "docs/architecture/README.md"
    if not readme.is_file():
        blockers.append("missing_architecture_readme")
    else:
        rtx = readme.read_text(encoding="utf-8")
        if "Phase-Luna-Evaluation-Test-Board-001" not in rtx:
            blockers.append("readme_missing_phase_luna_evaluation_test_board_001")
        if "LUNA_EVALUATION_TEST_BOARD_OVERVIEW_V0.md" not in rtx:
            blockers.append("readme_missing_test_board_overview_link")

    levels_p = repo / DOCS[1][1]
    if levels_p.is_file():
        lt = levels_p.read_text(encoding="utf-8")
        if not re.search(r"Level\s*9.*后置|后置.*Level\s*9", lt, re.S):
            if "Level 9" not in lt or "后置" not in lt:
                blockers.append("levels_doc_must_state_level9_posterior")
        if not re.search(r"benchmark.*不得|不得.*benchmark", lt, re.I | re.S):
            blockers.append("levels_doc_must_forbid_benchmark_as_release")
        if not re.search(r"上线许可", lt):
            blockers.append("levels_doc_must_mention_release_permission_boundary")

    intr_p = repo / DOCS[3][1]
    if intr_p.is_file():
        it = intr_p.read_text(encoding="utf-8")
        for token in (
            "user_cancel",
            "system_timeout",
            "high_priority_interrupt",
            "power_degraded_interrupt",
            "scene_changed_interrupt",
            "safety_override",
        ):
            if token not in it:
                blockers.append(f"interrupt_doc_missing:{token}")

    lr_p = repo / DOCS[4][1]
    if lr_p.is_file():
        lrt = lr_p.read_text(encoding="utf-8")
        if "30" not in lrt and "30 分钟" not in lrt:
            blockers.append("long_run_doc_missing_30m_tier")
        if "1 小时" not in lrt and "1小时" not in lrt:
            blockers.append("long_run_doc_missing_1h_tier")
        if "4 小时" not in lrt:
            blockers.append("long_run_doc_missing_4h_tier")
        if "8 小时" not in lrt:
            blockers.append("long_run_doc_missing_8h_tier")

    tt_p = repo / DOCS[5][1]
    if tt_p.is_file():
        tt = tt_p.read_text(encoding="utf-8")
        if "Vision" not in tt or "Voice" not in tt:
            blockers.append("task_type_doc_must_name_vision_and_voice")

    stcm_p = repo / DOCS[6][1]
    if stcm_p.is_file():
        st = stcm_p.read_text(encoding="utf-8")
        for token in ("deadline", "stale", "voice", "spatial_anchor"):
            if token not in st.lower():
                blockers.append(f"stcm_doc_missing_keyword:{token}")

    cfg_p = repo / "configs/evaluation/luna_evaluation_test_board_v0.example.json"
    cfg: Dict[str, Any] = {}
    if not cfg_p.is_file():
        blockers.append("missing_config:configs/evaluation/luna_evaluation_test_board_v0.example.json")
    else:
        cfg = _read_json(cfg_p)
        if str(cfg.get("schema_version") or "") != "luna_evaluation_test_board_v0":
            blockers.append("bad_config_schema_version")
        tl = cfg.get("test_levels")
        if not isinstance(tl, dict):
            blockers.append("test_levels_not_object")
        else:
            for k in REQUIRED_LEVEL_KEYS:
                if k not in tl:
                    blockers.append(f"test_levels_missing:{k}")
        ra = cfg.get("required_artifacts")
        if not isinstance(ra, dict):
            blockers.append("required_artifacts_not_object")
        else:
            for g in REQUIRED_ARTIFACT_GROUPS:
                if g not in ra or not isinstance(ra.get(g), list):
                    blockers.append(f"required_artifacts_missing_group:{g}")
            base = set(str(x) for x in (ra.get("base") or []) if isinstance(ra.get("base"), list))
            if not MIN_BASE.issubset(base):
                blockers.append(f"required_artifacts_base_incomplete:missing={sorted(MIN_BASE - base)}")
            lr = set(str(x) for x in (ra.get("long_run") or []) if isinstance(ra.get("long_run"), list))
            if not MIN_LONG_RUN.issubset(lr):
                blockers.append(f"required_artifacts_long_run_incomplete:missing={sorted(MIN_LONG_RUN - lr)}")
            ir = set(str(x) for x in (ra.get("interrupt") or []) if isinstance(ra.get("interrupt"), list))
            if not MIN_INTERRUPT.issubset(ir):
                blockers.append(f"required_artifacts_interrupt_incomplete:missing={sorted(MIN_INTERRUPT - ir)}")
            sr = set(str(x) for x in (ra.get("stcm") or []) if isinstance(ra.get("stcm"), list))
            if not MIN_STCM.issubset(sr):
                blockers.append(f"required_artifacts_stcm_incomplete:missing={sorted(MIN_STCM - sr)}")
        maf = cfg.get("module_admission_required_fields")
        if not isinstance(maf, list):
            blockers.append("module_admission_required_fields_not_list")
        else:
            req = [
                "module_name",
                "capability_type",
                "provider_name",
                "test_levels_supported",
                "input_contract",
                "output_contract",
                "audit_contract",
                "resource_budget",
                "timeout_policy",
                "interrupt_policy",
                "recovery_policy",
                "verifier_path",
                "release_gate_required",
            ]
            mafs = [str(x) for x in maf]
            for f in req:
                if f not in mafs:
                    blockers.append(f"module_admission_missing_field:{f}")

    ov_p = repo / DOCS[0][1]
    if ov_p.is_file():
        ov = ov_p.read_text(encoding="utf-8")
        if re.search(r"\bOCR[- ]only\b|PaddleOCR\s*专属测试板块|测试板块.*仅\s*OCR", ov, re.I):
            blockers.append("overview_doc_sounds_ocr_only_forbidden_phrase")

    hard_blockers = list(blockers)

    if not blockers:
        soft_followups.append(
            "SOFT-001: Per-module numeric thresholds for Level 6/7 to be filled after empirical runs (CONDITIONAL_GO acceptable)."
        )

    verdict = "NO_GO" if blockers else "GO"

    level_matrix_rows: List[Dict[str, Any]] = []
    for i, lk in enumerate(REQUIRED_LEVEL_KEYS):
        entry = (cfg.get("test_levels") or {}).get(lk) if isinstance(cfg.get("test_levels"), dict) else {}
        level_matrix_rows.append(
            {
                "test_level": lk,
                "level_index": i,
                "summary": str((entry or {}).get("summary") or "") if isinstance(entry, dict) else "",
            }
        )

    artifact_matrix_rows: List[Dict[str, Any]] = []
    if isinstance(cfg.get("required_artifacts"), dict):
        for g, names in cfg["required_artifacts"].items():
            if isinstance(names, list):
                for n in names:
                    artifact_matrix_rows.append({"artifact_group": str(g), "artifact_name": str(n)})

    admission_matrix = [
        {"field": f, "required": True} for f in (cfg.get("module_admission_required_fields") or []) if cfg
    ]

    summary: Dict[str, Any] = {
        "schema": "luna_evaluation_test_board_summary_v0",
        "phase": "Phase-Luna-Evaluation-Test-Board-001",
        "verdict": verdict,
        "repo_root": str(repo),
        "output_root": str(out_root),
        "blockers": sorted(set(blockers)),
        "soft_followups": soft_followups,
        "doc_paths_checked": [str(repo / x[1]) for x in DOCS],
        "config_path": str(cfg_p) if cfg_p.is_file() else "",
    }
    _write_json(out_root / "luna_evaluation_test_board_summary.json", summary)
    _write_json(
        out_root / "luna_evaluation_test_level_matrix.json",
        {"schema": "luna_evaluation_test_level_matrix_v0", "rows": level_matrix_rows},
    )
    _write_json(
        out_root / "luna_evaluation_test_artifact_matrix.json",
        {"schema": "luna_evaluation_test_artifact_matrix_v0", "rows": artifact_matrix_rows},
    )
    _write_json(
        out_root / "luna_evaluation_test_module_admission_matrix.json",
        {"schema": "luna_evaluation_test_module_admission_matrix_v0", "rows": admission_matrix},
    )

    rep = {
        "schema": "luna_evaluation_test_board_verifier_report_v0",
        "phase": "Phase-Luna-Evaluation-Test-Board-001",
        "verdict": verdict,
        "output_root": str(out_root),
        "blockers": sorted(set(blockers)),
        "hard_blockers": sorted(set(hard_blockers)),
        "soft_followups": soft_followups,
    }
    _write_json(out_root / "luna_evaluation_test_board_verifier_report.json", rep)

    print(json.dumps({"verifier_output_root": str(out_root), "verdict": verdict, "blockers": rep["blockers"]}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
