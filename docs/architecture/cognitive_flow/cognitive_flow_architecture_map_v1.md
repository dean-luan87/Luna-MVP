# Cognitive Flow Architecture Map v1

## A-route end-to-end map

```text
Field Observation
  -> Primitive / Concept Understanding
  -> Situation Understanding
  -> Context Formation
  -> Intent / Goal Understanding
  -> Affordance Understanding
  -> Capability Awareness
  -> Attention Allocation
  -> Information Gap / Value
  -> Cognitive Sufficiency Assessment
  -> Cognitive Routing
       -> A Route: minimum sufficient / pattern-match candidates
       -> B Route: deep-reasoning support candidates
  -> Reasoning / Causality / Counterfactual
  -> Future Space / Branch Governance
  -> Optimization
  -> Decision Candidate Formation
  -> Decision Commitment Candidate
  -> Execution Monitoring Candidate
  -> Outcome Observation / Evaluation
  -> Experience Candidate
  -> Cognitive Information Compression
  -> Internal Representation Evolution
  -> Population / Culture / Gene Pool Candidate
  -> next cognitive cycle
```

## Stage boundary map

| Stage | Candidate input | Candidate output | May affect Decision? | May mutate State? |
|---|---|---|---|---|
| Observation/primitive/concept | governed field/evidence references | primitive/concept candidates | No | No |
| Situation/context/intent/goal | understanding candidates | interpretation and goal candidates | No | No |
| Affordance/capability/attention | situation/context/goal/resource candidates | opportunity, limitation, attention candidates | No | No |
| Information value/sufficiency/routing | gaps, risk, time/resource, experience candidates | cognitive-path candidates | No | No |
| A/B reasoning | route, causal, counterfactual, future candidates | understanding/evaluation support candidates | No | No |
| Optimization/decision candidate/commitment | candidate spaces and constraints | value, option, commitment candidates | No; future Decision consumes them | No |
| Monitoring/outcome/experience | commitment/outcome candidates | deviation, outcome, experience candidates | No | No |
| Compression/evolution/population | experience/representation candidates | representation/culture/gene-pool candidates | No | No |

Every row remains candidate-only. Decision Candidate Formation is not Future Decision, and no row grants Action or permission.
