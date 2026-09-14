# Sufficiency Model Options

## Option A — Keep current model

```text
all active Required Conditions must be covered
```

### Advantages

- No schema or engine change.
- Deterministic exact-reference behavior.
- Easy to trace and validate.
- Preserves the already closed Required Condition / Need contracts.

### Disadvantages

- Acquisition sources can be accidentally modeled as conjunctive objective
  requirements.
- A valid signage result cannot satisfy an exit-direction requirement if flow
  was separately declared required.
- Encourages unnecessary Need, Branch, and Strategy expansion.
- Does not express “one of these governed bases is sufficient.”

### Intrusion and economy

Lowest implementation intrusion, but the highest risk of cognitive over-
acquisition and branch/strategy inflation when upstream rules are source-
oriented.

### Decision

Not recommended as the long-term model. It is only safe when governance has
already supplied semantically atomic requirements with no alternative bases.

## Option B — Semantic Cognitive Requirement plus Alternative Satisfaction Basis

```text
Requirement R
  can be satisfied by Basis A OR Basis B OR Basis C
```

### Advantages

- Directly separates “what must be known” from “what can satisfy it.”
- Supports multiple acquisition paths without making them jointly required.
- Keeps Information Need as requirement-minus-coverage.
- Lets Acquisition Strategy remain downstream and candidate-only.
- Minimal conceptual change to current exact-reference architecture.

### Disadvantages

- Requires an explicit governed relation and a defined alternative satisfaction
  rule.
- Needs clear handling for stale, conflicting, or invalid bases.
- Existing coverage refs need a governed mapping to the requirement they satisfy.

### Intrusion and economy

Moderate but bounded intrusion: extend the Required Condition / Coverage
semantic boundary and its evaluator; keep Need, Branch, Strategy, Sufficiency,
and Stop ownership. It should reduce unnecessary downstream expansion while
preserving multiple candidate paths.

### Decision

Recommended.

## Option C — Multiple Sufficient Condition Sets

```text
Set 1: A + B
OR
Set 2: C
OR
Set 3: D + E
```

### Advantages

- Expresses compound alternatives and complementary evidence.
- Can model more complex minimum sufficient combinations.

### Disadvantages

- Introduces set-algebra / Boolean semantics, ambiguity around partial
  satisfaction, conflict, and precedence.
- Increases trace, validator, and lifecycle complexity.
- Risks pulling Strategy Coordination into semantic sufficiency decisions.

### Intrusion and economy

High intrusion. It may eventually improve cognitive economy, but premature
implementation would add combinatorial alternatives before Option B is stable.

### Decision

Defer. Do not implement in this review.

## Recommendation

Choose **Option B** as the smallest semantically sufficient direction. Start
with one requirement and explicit alternative bases. Do not introduce a
general Boolean DSL, confidence algebra, evidence fusion, or strategy
coordination as part of that correction.
