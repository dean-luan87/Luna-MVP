# Intent Failure and Responsibility v1

Intent Governance owns:

- incorrect candidate qualification or admission;
- invalid lifecycle mutation, cross-Intent contamination or identity
  collision;
- missing/incorrect version and provenance lineage;
- invalid coexistence, dominance, carryover or handoff;
- unauthorized direct mutation from another owner;
- failure to reject stale, revoked or out-of-scope Intent changes.

It returns an explicit candidate rejection, defer, stale, conflict or blocked
record rather than inventing a commitment. A changed source version is an
applicability signal, not an automatic Intent mutation.

It does not own Goal governance, Concern reasoning, Need, Sufficiency, Task
execution, Capability resolution, Runtime Admission, Provider execution,
Observation acquisition or Loop persistence. Those owners retain their own
failure responsibility.
