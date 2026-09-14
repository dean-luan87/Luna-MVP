# Cognitive Attention Conflict Resolution Model v1

Attention Conflict Resolution Candidate evaluates competing attention requests without declaring a winner as fact or action.

## Consistency constraints

- Direction consistency: candidates must be compared against Active Goal/Context relevance.
- Depth consistency: requested depth must fit risk, information value, and resource candidates.
- Time consistency: requested duration must fit the current time-window candidate.
- Resource consistency: combined budget cannot exceed the current bounded attention-budget candidate.

Conflicting requests may be preserved, reduced, deferred, or expressed as a conflict candidate. Conflict Resolution != Decision, Action, source deletion, or automatic B Route execution.
