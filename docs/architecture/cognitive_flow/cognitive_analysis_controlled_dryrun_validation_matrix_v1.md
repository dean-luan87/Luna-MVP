# Cognitive Analysis Controlled DryRun Validation Matrix v1

## Object, reference, semantic, and permission matrices

| Object | Object validation | Reference validation | Semantic validation | Permission validation |
| --- | --- | --- | --- | --- |
| Admission | fields/enums/provenance/trace | source Context/version | insufficient not admitted; stale/revoked signals | read-only Context only |
| Frame | fields/lifecycle | Admission, Context/version | no copied mutable State | no runtime/model handle |
| Hypothesis | fields/status/statement | Frame, Context, Evidence | not Fact; revoked not support | no State command |
| Competing Set | >=2 refs, status | member Hypotheses, Frame/Context | unresolved has no forced dominant | no ranking execution |
| Evidence Assessment | relation/lifecycle | Evidence and Hypothesis | missing != contradicts; revoked distinct | no Evidence mutation |
| Gap Refinement | controlled gap/blocking fields | Frame and source gap | permission restriction preserved | no observation execution |
| Observation Request | required refs/flag | Refinement and Frame | candidate only | `execution_admitted=false` |
| Sufficiency | fields/status | Frame, Context | critical gap/unknown/revoked preserved | not truth/fact admission |
| Result | fields/status/frozen flags | Frame, Sufficiency, all output refs | blocked/stale/provisional status consistent | no Decision/State/runtime writeback |

## Case × check coverage

| Check family | 001 | 002 | 003 | 004 | 005 | 006 | 007 | 008 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Object/enum/provenance/trace | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Local reference closure | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Competing/dominant rule | — | ✓ | — | — | — | — | — | — |
| Contradiction preservation | — | — | ✓ | — | — | — | — | — |
| Insufficiency blocks conclusion | — | — | — | ✓ | — | — | — | — |
| Revocation/stale rule | — | — | — | — | ✓ | — | — | — |
| Temporal unknown rule | — | — | — | — | — | ✓ | — | — |
| Gap/request candidate-only | — | — | — | — | — | — | ✓ | — |
| State writeback denied | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Cross-case reference absence | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

Every future execution must separately collect object, reference, semantic,
permission, and negative-guard checks. A pass in one family cannot compensate
for a failure in another.
