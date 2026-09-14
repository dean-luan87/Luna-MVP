# Minimum Relevant Cognitive View Contract v1

## Candidate item

`AvailableCognitiveInformationItemV1` is a governed candidate information
reference. It records:

- `information_ref`;
- `object_type`: `SELF` or `EXTERNAL`;
- `information_kind`;
- explicit `support_condition_refs`;
- source and provenance refs;
- `recoverable` and `candidate_only`.

Self items may reference Self State, viewpoint, capability, or resource
information. External items may reference Field, Entity, Relation, Evidence,
or Current World candidates. The item does not assert the referenced object as
Truth.

## Selection rule

The adapter forms one active condition set from:

```text
GoalContext.success_condition_refs
+ governed objective conditions
+ governed role / intent / concern / context conditions
```

An available item is selected exactly when its declared support conditions
intersect that active set. All other items remain excluded. Recoverable
excluded items remain available for a later goal-conditioned selection.

No selection decision reads `scenario_id`, parses a Goal or Context string, or
uses a static Goal-to-reference lookup table. Object type does not change the
selection rule.

## View output

`ARouteMinimumRelevantCognitiveViewCandidateV1` preserves:

- selected Self and External refs;
- excluded and recoverable refs;
- selected source/provenance refs;
- active governed condition refs;
- `current_cognitive_coverage_refs`, equal to the selected information refs;
- Goal, Role, Context, Field, Current World, and cognitive-state references.

It remains `candidate_only=true`, `read_only=true`, and
`truth_declared=false`.

## Isomorphism

```text
Available Self Information
Available External Information
        ↓ same condition-intersection rule
Minimum Relevant Cognitive View Candidate
```

Self-specific identity, resource, capability, viewpoint, and mutation
boundaries remain owned by their existing Self/Capability owners. They are
inputs to selection, not a second cognition algorithm.

## Closure and long-term principles

User-terminal verification closed this contract with `GO — VERIFIED — PHASE
CLOSED`. `Available Cognitive Information` is distinct from `Active Cognitive
Information`. Excluded or dormant information is not deleted or declared
unknown; it remains recoverable and may be reactivated when governed Goal or
Role conditions change.

Self and External information use the same goal-conditioned selection
principle. Self remains special because of its first-person subject position,
information source, capability/resource ownership, and authority/mutation
boundary—not because it uses a separate cognition algorithm.
