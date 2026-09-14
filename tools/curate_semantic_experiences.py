from __future__ import annotations

import argparse
import json
from pathlib import Path

from observe.semantic_stability.loader import load_profiles
from world_knowledge.schema import InterpretationExperienceCard
from world_knowledge.loop.curator import curate_interpretation_experience
from world_knowledge.sources.library_source import CuratedLibrarySource


def _sanitize_filename(name: str) -> str:
    return "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profiles", required=True, help="semantic stability json path")
    ap.add_argument("--out-dir", required=True, help="output directory for curated cards")
    ap.add_argument("--version", type=int, default=1)
    args = ap.parse_args()

    profiles = load_profiles(args.profiles)
    library = CuratedLibrarySource()

    curated_cards = []
    for p in profiles:
        card = InterpretationExperienceCard(
            roi_kind=p.key.roi_kind,
            category=p.key.category,
            meaning=p.key.meaning,
            stability=p.score.stability,
            confidence=p.score.confidence,
            environment_id=p.environment_id,
            scope=p.scope,
            source="timeline_c3_1",
            evidence=p.score.evidence,
            version=args.version,
        )
        status = curate_interpretation_experience(library, card)
        if status == "CURATED":
            curated_cards.append(card)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for card in curated_cards:
        key = f"interpretation::{card.roi_kind}::{card.category}::{card.meaning}"
        filename = _sanitize_filename(key) + ".json"
        path = out_dir / filename
        with open(path, "w", encoding="utf-8") as f:
            json.dump(card.__dict__, f, ensure_ascii=False, indent=2)

    print(f"Curated {len(curated_cards)} cards to {out_dir}")


if __name__ == "__main__":
    main()
