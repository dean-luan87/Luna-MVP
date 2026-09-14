# Loop Authority Leakage Inventory

These are static findings from the current Dynamic Flow and Loop candidate
implementations. No code is changed here.

| Current location / behavior | Current appearance | Classification | Target boundary |
|---|---|---|---|
| Dynamic Flow next Need selection | selects Need from plan refs | C. cognition / semantic judgment | A/B selects; Loop stores ref |
| Dynamic Flow evidence handling | maps evidence to INSUFFICIENT/SUFFICIENT/RECONSIDER | C. cognition / semantic judgment | A/B judges; Flow/Loop store transition |
| GoalSufficiencyCandidateV1 | emits goal sufficiency and stop | C. cognition / semantic judgment | A local; Brain global adjudication |
| Dynamic Flow reconsideration helper | forms reconsideration candidate | C. cognition / semantic judgment | A/B judges; Flow transports |
| Dynamic Flow next-step disposition | emits CONTINUE/REPLAN/REQUEST_MORE_EVIDENCE | C. cognition / semantic judgment | A/B owns reasoning direction |
| LoopLocalState current_minimum_need_ref | stores Need ref | A. state storage only | KEEP in Loop |
| LoopLocalState hypothesis_lineage_refs | stores lineage | A. state storage only | KEEP; A/B owns hypothesis |
| LoopIdentity requirement_refs | stores Requirement refs | A. state storage only | KEEP; Capability owns resolution |
| CapabilityCandidatePathV1 | stores Need to Scope/Resolution path | A. state storage only | KEEP; A/B requests |
| CapabilityGrowthGuardCandidateV1 | records growth gates | E. ambiguous | Shared governance evaluates |
| ContinuityAssessmentCandidateV1 | compares authoritative refs | C/E. mixed | A/B evaluates meaning; Loop stores |
| ResumeAssessmentCandidateV1.decision | emits KEEP/SUPERSEDE/REPLAN/COMPLETE/WAITING | C. cognition / semantic judgment | Brain/A/B decides; Loop mechanics |
| BranchReservationCandidateV1 | carries branch/merge refs | A. state storage only | KEEP; Brain materializes |
| ClosureAssessment.closure_reason | suggests closure reason | C. cognition / semantic judgment | A/B suggests; Brain/Flow accepts |
| LifecycleClosureCandidateV1 | records accepted lifecycle transition | B. mechanical lifecycle operation | KEEP after governed acceptance |
| BrainAssimilationCandidateV1 | carries handoff disposition | B. mechanical handoff | KEEP candidate-only |
| Closure package/history boundary | packages refs and trace | A/B. storage/handoff | KEEP; no compression |

## Summary

The main leakage is not external mutation. The implementation is candidate-only
and guarded. The leakage is that Dynamic Flow and Loop envelopes express
semantic judgments assigned by the target to A/B reasoning and Brain
adjudication. Later migration should narrow authority without deleting state
version, trace, provenance, pause/wait/resume, closure or package mechanics.
