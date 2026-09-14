# Brain Go / No-Go v1

## Readiness checks

- Brain is defined as a cognitive evaluation center, not a model or executor.
- Global Cognitive State enters through Brain Context Package.
- State Interpretation, Situation Evaluation, Intent Alignment, Option
  Evaluation, Conflict Analysis, Decision Candidate Generation, and Decision
  Trace are defined.
- Value remains a constraint and Drive remains an influence.
- Learning and Memory provide candidates/context without modifying Brain.
- Attention retains resource allocation and observation authority.
- Unknown, Risk, Conflict, Confidence, and Provenance are preserved.
- Decision Candidate remains separate from Action and Action Boundary.
- Brain lifecycle and governance are candidate-based.
- B Route remains an interface placeholder only.

## Required negative guards

No LLM integration; no automatic reasoning Runtime; no Action execution; no
automatic planning; no Prediction; no World Model; no B Simulation Runtime;
no automatic learning; no model training; no hardware calls; no Action
Runtime; no Reality, Field, Memory, Goal, Identity, Attention, or Value
mutation by Brain.

Guard keywords: Option Evaluation; Decision Trace; No automatic reasoning Runtime; No Action execution; No automatic planning; No Prediction; No World Model; No B Simulation Runtime; No automatic learning; No model training; No hardware calls; No Action Runtime; No Reality; Value mutation.

## Authority and stop point

V0 static checks are Agent-only. V1 is not authorized in Planning Only mode.
V2 Final Phase Verification is User Terminal Only. V3 Final Audit and
Decision is ChatGPT Only. V0 does not grant GO. Agent stop status is
WAITING_FOR_USER_TERMINAL_VERIFICATION.

## No-go conditions

Block if Brain can directly access Camera, Model, Hardware, Database, or
Provider; if Brain writes Reality or Field; if Learning modifies Brain; if
Decision Candidate is conflated with Action; if Unknown is fabricated; or if
Brain bypasses Governance, Constitution, Attention, Capability, or the
Decision Boundary.
