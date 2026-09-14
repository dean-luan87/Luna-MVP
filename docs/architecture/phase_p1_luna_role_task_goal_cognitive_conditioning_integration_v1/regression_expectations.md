# Regression expectations

The existing Full E2E cognitive-logic regression should now exercise its
controlled contrasts through Gateway and A-Route and report independent:

```text
operational_result = PASS
cognitive_logic_result = PASS
final_decision = GO
```

The assertion remains evidence-based: it compares observed conditioned
Attention, relevance, relation interpretation, Hypothesis, Current World, and
Sufficiency output. Physical Field refs must remain unchanged for Role/Task
contrasts; missing and conflicting evidence retain their existing guarded
semantics.

Decision contrast normalization is separate from provenance validation. The
runner retains the raw Decision Candidate signature and execution-specific
refs for traceability, but contrast comparisons use the observed canonical
Decision Governance semantic projection: resolved option meaning, decision
state, utility/risk candidates, eligibility, veto reasons, confirmation, and
reversibility. Candidate IDs, scenario IDs, trace IDs, and provenance
namespaces are identity fields and must not by themselves establish a
cognitive change or an irrelevant-field regression.
