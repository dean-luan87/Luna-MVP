import json

from roi_learning_c1.pipeline import run_c1_from_timeline


def test_pipeline_promote_when_strong(tmp_path):
    p = tmp_path / "t.jsonl"
    lines = []
    for _ in range(60):
        lines.append(
            json.dumps(
                {
                    "roi_debug": {
                        "roi_hints": [{"area_type": "exit_area"}],
                        "roi_hit": {"hit": True},
                    },
                    "roi_perception_debug": {"reference_count": 1},
                }
            )
        )
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")

    proposals = run_c1_from_timeline(str(p))
    assert proposals
    top = proposals[0]
    assert top.roi_kind == "exit_area"
    assert top.suggestion in ("PROMOTE_TO_DEFAULT", "OBSERVE")
    assert top.score >= 0.45
