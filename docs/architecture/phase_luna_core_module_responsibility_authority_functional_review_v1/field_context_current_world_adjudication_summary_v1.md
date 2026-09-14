# Field / Context / Current World Adjudication Summary v1

## Overall conclusion

The correct architecture is **three separate but narrow boundaries**:

1. **Field — NARROW / KEEP as source-state boundary.** Governed operational
   environmental state and deterministic transition lineage; Field Reducer is
   the only intended mutation authority, although the repository implementation
   is currently a skeleton.
2. **Context — NARROW / KEEP as situation-framing assembly.** Versioned,
   reference-only binding of source projections, temporal validity and
   provenance; no source ownership duplication.
3. **Current World — NARROW / KEEP as candidate representation.** Observation
   and source-ref-derived cognition-cycle candidate with uncertainty, conflict,
   version and provenance; no Field mutation or World Truth.

## Target owner map

```text
Observation/Evidence ──┬→ Current World candidate ─┐
                       └→ Field Event Admission   │
                           → Field Reducer         ├→ refreshed refs/snapshots → A
Field/read model ──────────────────────────────────┘
Context Foundation assembles source refs/validity around the situation.
Working Envelope carries admitted refs/constraints.
Semantic Working Outline and Cognitive Snapshot are version-linked sibling
derived products, not a strict semantic authority chain.
```

## Main gaps

- `RUNTIME_GAP`: Field reducer, Context Foundation and Current World assets are
  controlled skeleton/candidate implementations, not production runtimes.
- `CONTRACT_GAP`: explicit cross-domain invalidation and source-version
  propagation contract is not fully centralized.
- `ADAPTER_GAP`: B1/B2/Dynamic Flow compatibility paths still carry historical
  terminology and semantic-looking fields.
- `TERMINOLOGY_GAP`: Current World/World Truth and active-hypothesis field names
  need future clarification without changing types in this review.

## Final status

Architecture documentation only. No runtime, type, enum or owner was changed.
