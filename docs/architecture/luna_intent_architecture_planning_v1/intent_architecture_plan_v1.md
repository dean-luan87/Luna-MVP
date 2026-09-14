# Luna Intent Architecture Planning v1

Status: PLANNING_CANDIDATE

## Phase position

This phase plans the Intent architecture that follows the closed Context Foundation and Personal Cognitive Network (PCN) boundaries. It creates candidate semantics and contracts only. It does not implement an Intent runtime, activate schemas, modify an existing owner, or authorize Causal, Decision, Action, Task, persistence, model, or Runtime behavior.

Intent Governance is the sole candidate owner of Intent semantics. Context owns current-state description. PCN owns cross-object connection, activation, and contextual projection. Neither Context nor PCN creates Intent.

## Canonical candidate definition

Intent is the subjective, future-oriented, directional, state-changing tendency formed under the joint influence of current Context, personal cognitive state, Self state, Field/Role/Relationship constraints, Memory/Experience references, Emotion influence, resource condition, and other admitted provenance.

In concise form, Intent answers: **“I tend to move the next state in which direction?”**

Intent is not an Action, Decision, Task, Goal, Desire, Need, Drive, Emotion, Attention allocation, Context output, PCN activation, strong cognitive link, repeated activation, Field pressure, or Role obligation. These objects may constrain or influence an Intent candidate but cannot own, assert, promote, decide, or execute it.

## Formation model

The planning flow is:

```text
source-owned references
        ↓
Potential Intent Candidate
        ↓  provenance-preserving qualification
Intent Candidate set
        ↓  coexistence / conflict / suppression / amplification
Temporary Dominance Candidate
        ↓
Intent-to-Causal Handoff Candidate
```

A Potential Intent Candidate means only that incomplete evidence may indicate a forming tendency. Promotion is never automatic and requires preserved source references, Context references, PCN projection references, provenance, formation trace, uncertainty, alternative candidates, and an explanation of why the candidate exists.

Multiple Intent candidates may coexist, conflict, nest, become suppressed or dormant, reactivate, or temporarily dominate. Competition does not select an action. Temporary dominance does not delete other candidates and is not Decision arbitration.

## Continuity and carryover

A Field or Context transition does not terminate Intent. An unfinished work tendency can persist after a physical transition from office to home when supported by unfinished-state evidence, importance, Role obligation, Memory activation, Field residue, or Emotion influence. Intent carryover is related to Mental Field Continuity but does not own or merge with it.

No fixed duration, candidate-count cap, nesting-depth cap, score threshold, retention threshold, or winner-take-all rule is frozen in this planning phase.

## Lifecycle semantics

The following are planning candidates, not a production enum or runtime FSM:

- `UNKNOWN`
- `POTENTIAL`
- `FORMING`
- `ACTIVE_CANDIDATE`
- `SUPPRESSED`
- `DORMANT`
- `REACTIVATED`
- `RESOLVED_CANDIDATE`
- `ABANDONED_CANDIDATE`

Short-lived, persistent, recurring, dormant, reactivated, and evolving patterns are all valid. Strength, confidence, priority, and truth status remain separate dimensions. None implies a Decision.

## Owner and mutation boundary

Intent Governance may own only Intent Candidate, Potential Intent Candidate, Intent State Candidate, Intent Interaction Candidate, and Intent Trace Candidate. It may not own or mutate Context, PCN, Self, Field, Role, Relationship, Memory, Experience, Emotion, Value, Causal, Decision, Action, Task, Runtime, or Reality.

Self, Field, Role, Relationship, Memory, Experience, Emotion, and Resource states remain source-owned references. They can constrain, suppress, amplify, or qualify Intent candidates through candidate contracts. Influence never grants mutation authority.

## Resource behavior

Resource constraints may reduce projection breadth, expansion breadth, or historical-reference breadth. They may not delete source records or dormant candidates, alter truth, force a winner, manufacture an Intent, or decide an Action.

## Downstream handoff

The only downstream output in this phase is an Intent-to-Causal Handoff Candidate containing Intent Candidate references, competition/suppression references, Context/PCN/Field/Role references, Resource references, provenance, and uncertainty. It contains no causal explanation, decision, action, task, goal transfer, or runtime command.

Intent asks what future state is sought, avoided, or maintained. Causal asks why, what causes what, and what might happen if conditions change. Decision asks which admissible course to select.

## Existing asset alignment

The earlier Cognitive Intent Architecture remains a reference requiring semantic alignment, not a parallel canonical implementation. “Cognitive Intent Signal”, “Attention Intent”, and downstream “Action Intent” are narrower legacy terms and must not be equated with the subject-level Intent defined here. The active canonical owner remains Intent Governance as frozen by the architecture alignment series.

## Stop boundary

This phase ends after planning assets, candidate contracts, a scenario suite, a risk review, an open-question registry, a change manifest, and a read-only verifier have been created. No existing asset, active schema, active contract, owner metadata, Context/PCN module, Task Manager, Runtime, or implementation code is changed.
