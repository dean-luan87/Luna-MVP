# Minimum Sufficient Field Understanding Skeleton Validation Matrix v1

| Validation area | Static requirement | Boundary protected |
| --- | --- | --- |
| Schema | Required fields and known schema version exist | Unstructured cognitive input is not admitted |
| Identity status | `known`, `partially_known`, or `unknown` only | Unknown is preserved rather than treated as failure |
| Behavior boundary | Allowed/forbidden candidates plus risk/exploration mappings exist | Behavior description is not an Action or permission |
| Traceability | Provenance source references exist and its trace matches `trace_ref` | Candidate origin remains inspectable |
| Temporal/spatial scope | Both mappings are explicit | Constraint remains scoped rather than universalized |
| Candidate boundary | All five not-* flags remain true | No Fact, State, Decision, or Action promotion |
| Negative input guard | Authority-bearing and external payload fields are rejected | No bypass to Reducer, Memory, Learning, or provider logic |
| Serialization | Sorted-key canonical JSON only | Stable non-executing representation |

The next DryRun, if separately authorized, must cover Identity Unknown, Dark Environment, Factory, Partial Understanding, and Expansion cases. This phase creates none of those fixtures and executes no case.
