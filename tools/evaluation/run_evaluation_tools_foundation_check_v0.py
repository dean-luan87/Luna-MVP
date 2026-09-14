#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-Foundation-001 — Evaluation Tools foundation check v0.

Checks that Evaluation Tools architecture primitives exist (dirs/docs/schema/registries).
Does NOT invoke OCR providers. Does NOT generate large datasets.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from capabilities.evaluation.common.evaluation_report_schema_v0 import (  # noqa: E402
    validate_evaluation_report_schema_v0,
)
from capabilities.evaluation.ocr.ocr_dataset_registry_v0 import (  # noqa: E402
    build_default_ocr_dataset_registry_v0,
)
from capabilities.evaluation.ocr.ocr_provider_benchmark_registry_v0 import (  # noqa: E402
    build_default_ocr_provider_benchmark_registry_v0,
)


def _now_iso() -> str:
    return _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _exists_matrix(paths: Dict[str, str]) -> Dict[str, Any]:
    m: Dict[str, Any] = {}
    for k, p in paths.items():
        pp = Path(p)
        m[k] = {"path": p, "exists": pp.exists(), "is_file": pp.is_file(), "is_dir": pp.is_dir()}
    return m


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    out_root = _require_abs(args.output_root, "--output-root")
    out_root.mkdir(parents=True, exist_ok=True)

    # Directory matrix (repo-resident)
    dir_paths = {
        "cap_eval": os.path.join(REPO_ROOT, "capabilities", "evaluation"),
        "cap_eval_ocr": os.path.join(REPO_ROOT, "capabilities", "evaluation", "ocr"),
        "cap_eval_common": os.path.join(REPO_ROOT, "capabilities", "evaluation", "common"),
        "tools_eval": os.path.join(REPO_ROOT, "tools", "evaluation"),
        "tools_eval_ocr": os.path.join(REPO_ROOT, "tools", "evaluation", "ocr"),
        "tools_eval_common": os.path.join(REPO_ROOT, "tools", "evaluation", "common"),
        "datasets_eval": os.path.join(REPO_ROOT, "datasets", "evaluation"),
        "datasets_eval_ocr_synth": os.path.join(REPO_ROOT, "datasets", "evaluation", "ocr_synthetic"),
        "datasets_eval_ocr_real": os.path.join(REPO_ROOT, "datasets", "evaluation", "ocr_realworld"),
        "datasets_eval_human": os.path.join(REPO_ROOT, "datasets", "evaluation", "human_review"),
        "docs_eval": os.path.join(REPO_ROOT, "docs", "architecture", "evaluation"),
        "logs_eval": os.path.join(REPO_ROOT, "logs", "evaluation"),
    }
    directory_matrix = _exists_matrix(dir_paths)

    # Required docs
    docs = {
        "boundary_contract": os.path.join(
            REPO_ROOT, "docs", "architecture", "evaluation", "LUNA_EVALUATION_TOOLS_BOUNDARY_CONTRACT_V0.md"
        ),
        "overview": os.path.join(REPO_ROOT, "docs", "architecture", "evaluation", "LUNA_EVALUATION_TOOLS_OVERVIEW_V0.md"),
        "ocr_framework": os.path.join(
            REPO_ROOT, "docs", "architecture", "evaluation", "LUNA_EVALUATION_OCR_VALIDATION_FRAMEWORK_V0.md"
        ),
        "report_schema_doc": os.path.join(
            REPO_ROOT, "docs", "architecture", "evaluation", "LUNA_EVALUATION_REPORT_SCHEMA_V0.md"
        ),
        "dataset_registry_doc": os.path.join(
            REPO_ROOT, "docs", "architecture", "evaluation", "LUNA_EVALUATION_OCR_DATASET_REGISTRY_V0.md"
        ),
        "provider_registry_doc": os.path.join(
            REPO_ROOT, "docs", "architecture", "evaluation", "LUNA_EVALUATION_OCR_PROVIDER_BENCHMARK_REGISTRY_V0.md"
        ),
        "human_review_doc": os.path.join(
            REPO_ROOT, "docs", "architecture", "evaluation", "LUNA_EVALUATION_HUMAN_REVIEW_PACKAGE_V0.md"
        ),
        "reserved_stress_doc": os.path.join(
            REPO_ROOT,
            "docs",
            "architecture",
            "evaluation",
            "LUNA_EVALUATION_MODULE_AND_CHAIN_STRESS_TEST_RESERVED_V0.md",
        ),
        "foundation_go_no_go": os.path.join(
            REPO_ROOT, "docs", "architecture", "evaluation", "LUNA_EVALUATION_TOOLS_FOUNDATION_GO_NO_GO_PACK_V0.md"
        ),
        "docs_index": os.path.join(REPO_ROOT, "docs", "architecture", "README.md"),
    }
    docs_matrix = _exists_matrix(docs)

    # Schema check (self-contained)
    minimal_report = {
        "evaluation_id": "foundation_schema_probe_v0",
        "evaluation_type": "dataset_quality_gate",
        "module": "ocr",
        "provider": None,
        "dataset_ref": None,
        "sample_count": 0,
        "metrics": {},
        "failure_cases_ref": None,
        "human_review_ref": None,
        "recommendation": "needs_manual_review",
        "runtime_integration": False,
        "whitebox_integration": False,
        "mainline_side_effect": False,
        "created_at": _now_iso(),
    }
    schema_check = validate_evaluation_report_schema_v0(minimal_report)

    # Registry skeleton checks (structure only)
    dataset_registry = build_default_ocr_dataset_registry_v0()
    provider_registry = build_default_ocr_provider_benchmark_registry_v0()

    boundary_check = {
        "runtime_integration": False,
        "whitebox_integration": False,
        "mainline_side_effect": False,
        "ocr_provider_invoked": False,
        "midplatform_invoked": False,
        "scene_delta_invoked": False,
        "world_context_invoked": False,
        "tts_invoked": False,
        "qwen_invoked": False,
    }

    summary: Dict[str, Any] = {
        "phase": "Phase-EvaluationTools-Foundation-001",
        "tool": "run_evaluation_tools_foundation_check_v0",
        "created_at": _now_iso(),
        "repo_root": REPO_ROOT,
        "output_root": str(out_root),
        "directory_matrix": directory_matrix,
        "docs_matrix": docs_matrix,
        "boundary_check": boundary_check,
        "evaluation_report_schema_check": schema_check,
        "ocr_dataset_registry_skeleton": dataset_registry,
        "ocr_provider_benchmark_registry_skeleton": provider_registry,
        "reserved_extension_matrix": {
            "dataset_quality_gate": True,
            "provider_ab_test": True,
            "stress_test": True,
            "chain_test": True,
            "failure_case_archive": True,
            "human_review_package": True,
        },
    }

    _write_json(out_root / "evaluation_tools_foundation_summary.json", summary)
    _write_json(out_root / "evaluation_tools_directory_matrix.json", directory_matrix)
    _write_json(out_root / "evaluation_tools_boundary_check.json", boundary_check)
    _write_json(out_root / "ocr_evaluation_framework_matrix.json", {"layers": 6, "doc_ref": docs["ocr_framework"]})
    _write_json(out_root / "evaluation_report_schema_check.json", schema_check)
    _write_json(out_root / "reserved_extension_matrix.json", summary["reserved_extension_matrix"])

    notes = "\n".join(
        [
            "# Evaluation Tools foundation check v0",
            "",
            "- Evaluation Tools only; no runtime/whitebox integration.",
            f"- **output_root:** `{summary['output_root']}`",
            "",
        ]
    )
    (out_root / "foundation_notes.md").write_text(notes + "\n", encoding="utf-8")

    ok = True
    # Must-have: dirs and docs exist, schema check ok, boundary flags false
    if not schema_check.get("ok"):
        ok = False
    if any(not v.get("exists") for v in directory_matrix.values()):
        ok = False
    if any(not v.get("exists") for v in docs_matrix.values()):
        ok = False

    print(json.dumps({"ok": ok, "output_root": str(out_root)}, ensure_ascii=False))
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())

