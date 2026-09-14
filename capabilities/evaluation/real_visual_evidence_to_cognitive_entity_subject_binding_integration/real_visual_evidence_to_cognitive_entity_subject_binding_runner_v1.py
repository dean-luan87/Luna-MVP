"""User-terminal Runner for L1 visual subject-candidate binding."""

from __future__ import annotations

import argparse
import json

from .engine_v1 import (
    RealVisualEvidenceCognitiveEntitySubjectBindingEngineV1,
    _repo_root,
    jsonable,
)


ROOT = _repo_root()
OUTPUT_DIR = (
    ROOT
    / "_eval_out/real_visual_evidence_to_cognitive_entity_subject_binding_integration_v1"
)
DEFAULT_SOURCE = ROOT / "_tmp_eval_inputs/roboflow_real_exit_v1/source_image.jpg"


def build_runner_summary_v1(*, source_ref: str = str(DEFAULT_SOURCE)) -> dict:
    return jsonable(
        RealVisualEvidenceCognitiveEntitySubjectBindingEngineV1(ROOT).run(
            source_ref=source_ref
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Bind real visual evidence to a candidate-only Cognitive Primitive entity."
    )
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    args = parser.parse_args()
    summary = build_runner_summary_v1(source_ref=args.source)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True)
    (OUTPUT_DIR / "runner_summary_v1.json").write_text(output + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()

