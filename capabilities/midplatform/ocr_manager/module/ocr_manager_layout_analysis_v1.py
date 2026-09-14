from __future__ import annotations

from typing import Any, Dict, Mapping, Sequence, Tuple


def build_ocr_manager_layout_candidates_v1(
    raw_evidence: Sequence[Mapping[str, Any]],
    region_attribution: Sequence[Mapping[str, Any]],
) -> Tuple[Dict[str, Any], ...]:
    block_grouping = []
    paragraph_candidates = []
    label_value_candidates = []
    title_body_candidates = []
    spatial_relations = []

    for index, item in enumerate(raw_evidence):
        text = str(item.get("normalized_text_candidate") or item.get("raw_text") or "")
        block_id = f"block_{index}"
        line_ref = str(item.get("line_ref") or f"line_{index}")
        block_grouping.append(
            {
                "block_id": block_id,
                "line_refs": (line_ref,),
                "region_ref": item.get("region_ref"),
            }
        )

        if ":" in text:
            left, right = text.split(":", 1)
            label_value_candidates.append(
                {
                    "label_candidate": left.strip(),
                    "value_candidate": right.strip(),
                    "confidence": item.get("confidence"),
                }
            )
        if index == 0 and len(text) <= 20:
            title_body_candidates.append(
                {"title_candidate": text, "body_candidate_ref": "remaining_blocks"}
            )
        if len(text.split()) > 4:
            paragraph_candidates.append(
                {"paragraph_id": f"paragraph_{index}", "block_refs": (block_id,)}
            )
        spatial_relations.append(
            {
                "source_block": block_id,
                "relation": "next_to",
                "target_block": f"block_{index + 1}",
            }
        )

    table_candidates = tuple()
    if any("|" in str(item.get("raw_text") or "") for item in raw_evidence):
        table_candidates = ({"table_id": "table_0", "source": "text_delimiter"},)

    return (
        {
            "layout_id": "layout_candidate_v1",
            "block_grouping": tuple(block_grouping),
            "line_grouping": tuple(
                {"line_ref": item.get("line_ref"), "block_id": f"block_{idx}"}
                for idx, item in enumerate(raw_evidence)
            ),
            "paragraph_candidates": tuple(paragraph_candidates),
            "table_candidates": table_candidates,
            "label_value_candidates": tuple(label_value_candidates),
            "title_body_candidates": tuple(title_body_candidates),
            "spatial_relation_candidates": tuple(spatial_relations),
            "candidate_only": True,
        },
    )
