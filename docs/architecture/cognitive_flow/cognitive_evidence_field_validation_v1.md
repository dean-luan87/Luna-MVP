# Cognitive Evidence Field Validation v1

## V0 synthetic validation design

| Scenario | Evidence candidates | Expected candidate outcome | Prohibited outcome |
| --- | --- | --- | --- |
| multi-source support | camera exit sign, OCR EXIT, VLM possible exit | Evidence Reinforcement Candidate with retained uncertainty | exit fact or action |
| source conflict | OCR open, camera closed | Evidence Conflict Candidate | automatic source winner or decision |
| experience interference | historical airport entrance expectation, current absence evidence | Experience Applicability Reduction Candidate | experience alters evidence/reality |

This phase only defines cases; it does not execute a synthetic runner. A separate Controlled DryRun phase is required before evidence-code validation.
