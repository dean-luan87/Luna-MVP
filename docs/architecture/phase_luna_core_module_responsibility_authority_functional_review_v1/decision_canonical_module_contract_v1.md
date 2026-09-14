# Decision Governance — Canonical Module Contract v1

## Canonical purpose

Decision Governance converts an admitted A local recommendation into an
auditable, constraint-bound commitment about what should be done, deferred,
stopped, or escalated, without performing A reasoning, organizing Task
dependencies, resolving Capability, or executing Action.

## Why it exists

Removing this boundary removes the owner of the transition from semantic
recommendation to commitment. A would otherwise have to commit and execute;
Brain would have to become every local decision engine; Task would have to
reinterpret purpose; or Action would have to authorize its own cause. The
irreducible responsibility is commitment under admitted options, provenance,
global constraints, reversibility and supersession.

## Authority and responsibility

Decision Governance may evaluate supplied options and authoritatively admit,
defer, abstain, suspend, supersede or revoke a Decision commitment within
Brain-supplied policy. A owns the underlying local reasoning and supplies a
DecisionCandidate/recommendation. Brain remains able to veto, override,
suspend, supersede, revoke or constrain the option set without becoming the
normal local decision engine.

The repository contract is deliberately candidate-oriented: controlled output
exposes `candidate_only`, `decision_output=False`, `action_triggered=False`
and `task_created=False`. These guards define the seam; they do not prove that
runtime commitment is complete.

## Canonical flow

`A local disposition → DecisionCandidate → Brain policy/constraint intake →
Decision Governance commitment → Task or narrow direct Action handoff →
execution/result evaluation → OutcomeCandidate → Brain assimilation`.

## Disposition

**NARROW** as an independent canonical governance boundary. Keep commitment,
option and handoff authority; remove legacy reasoning, planning, Provider
selection and execution behavior. Timing: `CONTRACT_ONLY /
RUNTIME_CONSOLIDATION_LATER`.
