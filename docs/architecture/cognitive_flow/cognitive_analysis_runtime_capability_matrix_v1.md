# A3 Cognitive Analysis Runtime Capability Matrix v1

| capability | input dependency | expected output | authority boundary | blocker condition |
| --- | --- | --- | --- | --- |
| Context Interpretation Candidate | Context Reference with version, trace, and declared lifecycle | candidate interpretation with explicit uncertainty | read Context by reference only; no Context/Snapshot mutation | Context construction/writeback, hidden raw-state access, or Fact claim |
| Evidence Relationship Candidate | supplied Evidence References and provenance/lifecycle signals | candidate relationship assessment and evidence trace | no evidence fetch, mutation, replacement, or truth admission | model/raw observation substitution, evidence mutation, or Fact promotion |
| Hypothesis Candidate | supplied Hypothesis References, Context Reference, and Evidence References | candidate support/contradiction/underdetermination assessment | no forced dominant candidate, Fact promotion, or causal certainty | dominant forced, confidence used as Fact authority, or conclusion emitted |
| Uncertainty Assessment Candidate | declared gaps, conflicts, stale/revoked/unknown signals | explicit uncertainty/warning candidate | unknown remains explicit; no silent completion | unknown suppressed, insufficiency treated as sufficient, or warning removed |
| Semantic Explanation Candidate | Context/Evidence/Hypothesis references with provenance | possible explanation candidate with trace and limits | no Decision, Action, State, Fact, or Memory authority | Decision/Action plan, State mutation, Memory update, or asserted conclusion |
