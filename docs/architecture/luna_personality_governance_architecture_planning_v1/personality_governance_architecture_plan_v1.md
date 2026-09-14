# Luna Personality Governance Architecture Planning v1

## Phase position

- Phase: `Phase-Luna-Personality-Governance-Architecture-Planning-v1-001`
- Execution Mode: `Planning Only`
- Canonical owner: `Personality Governance`
- Scope: a narrow, candidate-only semantic governance layer for personality evidence, trait candidates, profile candidates, and revision lineage.
- Stop status: `WAITING_FOR_USER_TERMINAL_VERIFICATION`

This phase defines contracts and boundaries only. It does not create a Personality runtime, Emotion Engine, memory/experience semantic compression, persistence, learning execution, parameter activation, model call, scheduler, task, device, or action capability.

## Owner decision

`Personality Governance` is the single canonical owner for:

- `PersonalityTraitCandidateV1`
- `PersonalityProfileCandidateV1`
- personality evidence admission and sensitivity review
- trait confidence, evidence strength, repetition, context diversity, temporal span, stability, uncertainty, contradiction, and counterexample governance
- personality revision, supersession, revocation, expiration, trace, and provenance
- candidate-only evidence handoff to and from existing owners

No parallel first-level owner may be created for `trait_governance`, `persona_governance`, `temperament_governance`, or `character_governance`.

## Semantic freezes

```text
Personality != Self
Personality != Emotion
Personality != Preference
Personality != Memory
Personality != Learning Pattern
Personality != Dynamic Regulation Parameter
Personality Trait Candidate != Activated Trait
Repeated Behavior != Personality Truth
Repeated Emotion != Personality Trait
Temporary Regulation Pattern != Personality Trait
User Correction > Inferred Personality Candidate
Personality Evolution Evidence != Personality Mutation
```

The module may preserve multiple uncertain or contradictory candidates. A profile is a structured set of trait candidates, not a single personality score, immutable identity, diagnosis, or action policy.

## Trait and profile semantics

`PersonalityTraitCandidateV1` records a bounded candidate over one taxonomy dimension. It keeps all source-owner references, including Self, Memory/Experience, Learning, Emotion, Regulation, and Interaction references, without taking ownership of their semantics. `candidate_only=true`, `activated=false`, `persisted=false`, and `truth_declared=false` are mandatory.

`PersonalityProfileCandidateV1` is a non-flattened collection of trait candidates. It may contain `uncertain`, `contested`, context-specific, and contradictory candidates simultaneously. It never directly decides task, intent, action, device, scheduler, or runtime behavior.

## Stability and evolution

The stability ladder is `EMERGING`, `TENTATIVE`, `SEMI_STABLE`, `STABLE_CANDIDATE`, `CONTESTED`, `REVISING`, `SUPERSEDED`, `REVOKED`, and `EXPIRED`. A single behavior or a single context repetition cannot establish a trait. Cross-context, cross-time, and diverse evidence can raise a candidate only through governed admission. Counterexamples remain attached and can lower or block stability. Explicit user correction has precedence over inferred evidence and creates revision lineage.

## Boundary map

- Self Governance may emit personality evidence candidates; Self Attribution, Self Continuity, and Self evolution evidence remain Self-owned. Personality may hold a `self_refs` reference but cannot mutate Self.
- Memory/Experience may provide behavior, interaction, preference, social, task, emotional-experience, and success/failure references. Memory does not directly write personality.
- Cognitive Learning may provide behavior-pattern, interaction-pattern, long-term-tendency, contradiction, and counterexample candidates. Learning does not activate a trait.
- Emotion may provide `EmotionToPersonalityEvidenceCandidate`; a temporary mood or repeated emotion remains evidence, not a trait. The Emotion Engine is not implemented here.
- Dynamic Regulation may expose long-term regulation-pattern evidence. Regulation parameters and parameter genomes remain Regulation-owned and cannot become personality traits automatically.
- PCN relationships, roles, and social links provide context only. A relationship or role is not global personality.
- Intent provides intent context/reference only. Personality cannot mutate or own intent.

## Privacy, trace, and idempotency

Personality is high-sensitivity long-term subject data. `DO_NOT_GENERALIZE`, `DO_NOT_TRANSFER`, and `DO_NOT_PERSIST_CANDIDATE` are hard boundaries. `cross_user_transfer=false` is frozen. Every candidate must remain reverse-locatable through Personality Evidence, source-owner references, cognitive cycle trace, and original source evidence. Contradictions, counterexamples, and revision lineage may not be discarded. Duplicate evidence, candidates, profiles, revisions, revocations, and replayed evidence are guarded; user correction has precedence.

## Deferred semantic compression

`semantic_compression_status = DEFERRED_TO_EMOTION_ENGINE`. This phase has no semantic compression execution, affective memory compression, emotion-memory summary, or personality-memory fusion. Future references are nullable only.

## Audit classification

- A: narrow Personality planning contracts, schemas, taxonomy, admission, stability, privacy, trace, idempotency, scenario, guard, gap, and deferred assets.
- B: existing typed candidate/reference interfaces that need future cross-owner contract formalization before implementation.
- C: historical owner names or runtime assets that conflict with the current canonical owner/boundary and must not be reused as owners.
- D: deliberately deferred Emotion Engine, runtime, persistence, activation, compression, and model/side-effect work.

## Implementation entry rule

Any future controlled implementation must add a new phase and owner-specific types under this contract. It must preserve candidate-only semantics, source-owner immutability, user-correction precedence, revision lineage, privacy restrictions, and all negative guards. This planning phase itself modifies no existing module.
