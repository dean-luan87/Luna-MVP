#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run Midplatform Module Definition Template Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.governance.midplatform_module_definition_template_planning_v1 import (
    run_midplatform_module_definition_template_planning_v1,
)

DEFAULT_DC_MODULE = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_decision_center_module_planning"
)
DEFAULT_OUTPUT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "midplatform_module_definition_template_planning"
)

OUTPUT_FILES: Tuple[Tuple[str, str], ...] = (
    ("summary", "summary.json"),
    ("midplatform_module_definition_template_policy", "midplatform_module_definition_template_policy_v1.json"),
    (
        "decision_center_module_planning_input_review",
        "decision_center_module_planning_input_review_v1.json",
    ),
    ("midplatform_module_definition_template", "midplatform_module_definition_template_v1.json"),
    (
        "decision_center_module_full_definition_exemplar",
        "decision_center_module_full_definition_exemplar_v1.json",
    ),
    ("template_adoption_requirement", "template_adoption_requirement_v1.json"),
    ("non_claims_register", "non_claims_register_v1.json"),
    (
        "midplatform_module_definition_template_planning_decision",
        "midplatform_module_definition_template_planning_decision_v1.json",
    ),
)


def _write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-root", default=DEFAULT_OUTPUT)
    p.add_argument("--decision-center-module-planning-root", default=DEFAULT_DC_MODULE)
    args = p.parse_args()

    result = run_midplatform_module_definition_template_planning_v1(
        midplatform_decision_center_module_planning_root=args.decision_center_module_planning_root,
        output_root=args.output_root,
    )

    out = Path(args.output_root)
    for key, fname in OUTPUT_FILES:
        _write(out / fname, result[key])

    sm = result["summary"]
    print(
        json.dumps(
            {
                "output_root": str(out),
                "planning_pass": sm.get("planning_pass"),
                "final_decision": sm.get("final_decision"),
                "template_established": True,
            },
            ensure_ascii=False,
        )
    )
    return 0 if sm.get("planning_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
