# A-Route Failure Injection Scenario v1

## Boundary

These are controlled architecture fixtures, not a Simulation Runtime, hardware
test, real Provider call, or Action execution. They inject represented input
conditions and inspect candidate traces only.

| Scenario | Injected condition | Expected cognitive response | Boundary assertion |
|---|---|---|---|
| R-01 Ideal environment | evidence, capability, and resources sufficient | complete situated trace with explicit confidence | baseline does not bypass candidate labels |
| R-02 Information insufficient | required evidence is absent or obscured | retain Unknown; lower confidence; request-information candidate | Unknown never becomes Reality fact |
| R-03 Capability degraded | camera unavailable or battery constrained | Self Capability limitation and risk-reduction/help-request candidate | no unsupported confident conclusion |
| R-04 Environment abrupt change | route closes after Decision Candidate | Situation re-assessment and alternative candidate | current plan is not treated as immutable |
| R-05 Erroneous evidence | conflicting or low-provenance observation | Evidence remains candidate; conflict/uncertainty is visible | Evidence does not directly become Reality |
| R-06 Repeated failure | comparable validated outcome deviations recur | pattern and future improvement candidate after validation | a single event cannot change Strategy or Self Model |

## Situated self/world fixture

The `small-horse-crossing` fixture keeps World State constant while varying
Self Capability Context. A shallow crossing may be `currently_impossible` for
one subject and `possible` for another. It validates that the system produces
a Situation Candidate, not a universal action conclusion.

## Evaluation fields

Each fixture records intent integrity, self/world coupling, Evidence confidence,
Unknown factors, decision confidence, failure localization candidate, authority
boundary result, and Experience Candidate eligibility.
