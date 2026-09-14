"""Interaction handoff skeleton: pass-through references only."""

from __future__ import annotations

from typing import Dict, Tuple

from .personal_cognitive_interaction_types_v1 import InteractionReferenceCandidate


def prepare_interaction_handoff_candidates(
    case: Dict[str, object],
) -> Tuple[InteractionReferenceCandidate, ...]:
    refs = case.get("interaction_refs", ())
    out = []
    for index, item in enumerate(refs):
        if not isinstance(item, dict):
            continue
        out.append(
            InteractionReferenceCandidate(
                interaction_reference=str(
                    item.get("interaction_reference", f"ir-{index}")
                ),
                interaction_type=str(item.get("interaction_type", "COEXISTENCE")),
                related_refs=tuple(str(x) for x in item.get("related_refs", ())),
                source_context_ref=str(
                    item.get(
                        "source_context_ref", case.get("context_id", "ctx-unknown")
                    )
                ),
                status=str(item.get("status", "CANDIDATE")),
                candidate_only=True,
                pcn_owns_interaction_kernel=False,
            )
        )
    return tuple(out)
