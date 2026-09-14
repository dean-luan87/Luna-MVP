# Minimum Sufficient Field Understanding Controlled DryRun Validation Matrix v1

| Validation | Fixture coverage | Required result |
| --- | --- | --- |
| Schema | All six cases | Required candidate structure is serializable |
| Identity Status | Unknown, Factory, Known Context | `unknown`, `partially_known`, and `known` are represented |
| Behavior Boundary | Dark, Factory, Known Context | Boundary exists independently of Identity completeness |
| Constraint/Identity | Public Space | Neighbor context does not promote Identity |
| Exploration | Exploration Boundary | Candidate is present; permission remains false |
| Information Gap | Information Gap Preservation | Unknown references remain explicit, not completed |
| Provenance | All six cases | Candidate -> Field -> source reference -> trace closes |
| Negative Guards | All six cases | No Fact, Action, authority, direct model action, or State mutation |
| Determinism | run1/run2 | Canonical JSON equality is true |

No fixture asserts that an environment interpretation is correct. The matrix validates only expression and governance boundaries.
