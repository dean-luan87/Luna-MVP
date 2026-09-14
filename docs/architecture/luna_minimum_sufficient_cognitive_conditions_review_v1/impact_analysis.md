# Impact Analysis

## Immediate fixture impact

The Scenario 12 fixture is the first correction target. Its current helper
creates each `condition_ref` as an independent rule and assigns a unique
`minimum_set_ref` to each rule. That is appropriate for genuinely conjunctive
requirements, but not for `signage` and `flow` as alternative ways to learn
one exit direction.

The same modeling pattern affects Scenarios 02, 03, 04, and 07. Their traces
remain useful as controlled demonstrations of the current rule-driven chain,
but they must not be interpreted as proof of minimum-sufficient alternative
reasoning.

## Canonical contract impact

Option B requires a thin semantic extension at the Required Condition / Current
Cognitive Coverage boundary. The extension should express:

```text
requirement_ref
→ governed satisfaction basis refs
→ alternative/any-valid-basis semantics
```

The existing `satisfaction_coverage_refs` should not silently change from its
current subset/AND meaning into OR meaning. The alternative relation must be
explicit and governed.

Information Need can continue to consume requirement refs and coverage
resolution. Branch Formation and Acquisition Strategy Formation can continue
to consume Need/Gap and explicit basis refs respectively.

## Runtime impact

No runtime changes are made by this review. A future implementation would be
limited to:

- evaluating explicit alternative satisfaction basis membership;
- returning satisfied requirement refs separately from unresolved requirement
  refs;
- preserving current candidate-only / read-only / non-Truth flags;
- keeping Need subtraction downstream and unchanged in responsibility.

No Attention, Observation Demand, Capability Resolution, Resource Merge,
Provider, Model, Decision, Task, or Action logic is required for this semantic
correction.

## Cognitive economy impact

Under the current conjunction model, adding one possible source can add one
Need remainder, one Branch, and one or more Strategies even after another source
has already supplied the necessary semantic fact. This is the over-expansion
visible in Scenario 12.

Option B should reduce unnecessary active requirements while retaining multiple
candidate acquisition paths. It must not force a single acquisition winner;
multiple paths can remain candidates until later governance.

## Truth and mutation impact

The review does not authorize any truth promotion. Satisfaction means current
cognitive coverage satisfies a governed requirement for the current scope; it
does not declare permanent World Truth, Field Truth, ownership, identity, or
action permission.
