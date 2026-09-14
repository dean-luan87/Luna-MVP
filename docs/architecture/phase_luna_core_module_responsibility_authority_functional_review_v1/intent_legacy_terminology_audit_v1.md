# Intent Legacy Terminology Audit v1

| Term/family | Classification | Canonical interpretation |
|---|---|---|
| Intent Governance / Intent owner | CANONICAL | independent Intent authority |
| Potential Intent | CANONICAL CANDIDATE | pre-admission possibility |
| Intent Candidate | CANONICAL CANDIDATE | structured non-binding proposal |
| active/dominant/carryover Intent | CANDIDATE / DEFERRED GOVERNANCE | lifecycle concepts represented by controlled assets |
| user intent / system intent | TERMINOLOGY_ONLY | source/provenance qualifier, not separate owners |
| task intent / behavior intent | LEGACY_OVERLAP | Task/Behavior influence or proposal; cannot own Intent |
| navigation/route intent | LEGACY_OVERLAP | domain-specific proposal/ref unless explicitly governed |
| inferred intent | CANDIDATE | inference label, never admitted truth by itself |
| intent as Need/goal/plan | TERMINOLOGY_GAP | must be rewritten to the ontology in `intent_ontology_boundary_v1.md` |

The strongest repository conflict is naming: `IntentCandidateV1` and lifecycle
states such as `ACTIVE_CANDIDATE` are candidate-only, while older prose calls
Intent “authority” or “active.” Recommended canonical reading is that only an
admitted Intent has authoritative lifecycle state; candidate labels remain
candidate until a later governance implementation defines the persistence
boundary. No rename is made in this phase.
