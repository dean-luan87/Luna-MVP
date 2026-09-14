# Scenario and Negative Coverage

Structural fixtures cover two stages of the exit scenario:

1. Two door candidates with unresolved signage produce an A-owned unresolved
   Hypothesis, `INSUFFICIENT` Sufficiency and a targeted Next Observation.
2. A follow-up ROI contains additional OCR evidence and an A-owned revised
   Hypothesis; a Decision candidate may be supplied by Decision Governance.

No expected exit identity is used by the pass predicate.

Negative coverage includes missing provenance, missing frame, stale Provider
Result, Detection/OCR conflict, no evidence, raw schema isolation, attempted
mutation and Provider autonomous re-observation.

Real mode additionally requires an actual external response and mapped
Evidence; a structural payload cannot satisfy that condition.

