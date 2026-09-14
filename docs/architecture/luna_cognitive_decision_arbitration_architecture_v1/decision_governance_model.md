# Decision Governance Model v1

## Governance sequence

1. Confirm the candidate set came from Brain and is grounded in Current
   Understanding.
2. Preserve Goal, Value Utility, Self State, Risk, confidence, and unknowns.
3. Apply Constitution and Self hard constraints first.
4. Compare remaining candidates and record tradeoffs.
5. Emit a Selected Decision Candidate with a trace reference.
6. Leave Action admission to Action Boundary and future Runtime.

Self has veto context but does not silently rewrite Brain rules. Value Utility
supports ranking but does not own the decision. B Route can be a future
simulation input only; it cannot override the current A-route candidate.

## Reconsideration

The states `Proposed`, `Evaluated`, `Approved`, `Active`, `Invalidated`, and
`Reconsidered` describe a candidate lifecycle. A red light, capability
failure, new Evidence, or changed Field may invalidate a candidate. The phase
does not implement automatic transitions or execution.
