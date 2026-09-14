# Luna Context Foundation Controlled Skeleton Implementation v1

Status: `CONTROLLED_SKELETON_CANDIDATE`

Phase: `Phase-Luna-Context-Foundation-Controlled-Skeleton-Implementation-v1-001`

Execution Mode: `Controlled Skeleton Implementation`

## 1. Stage goal

This stage translates the frozen Context Foundation planning candidates into a controlled Python skeleton. It provides immutable types, a pure protocol, reference-only assembly, trace metadata, static validators, four synthetic fixtures, and a controlled runner.

It does not implement user understanding, Intent, Causal Reasoning, Decision, Emotion computation, Memory access, Field mutation, Runtime integration, or real Context generation.

## 2. Input

The skeleton accepts source-owned `ProjectionReferenceV1` values only:

- Field State System projection reference;
- Observation Manager projection reference;
- Memory System projection reference;
- Self System projection reference;
- Role System / Social Self projection reference;
- Relationship System / Social Self projection reference;
- Emotion Context Boundary / Integration Layer projection reference;
- optional Mental Field Continuity reference.

Every projection carries source Owner, reference identifier, version, timestamp, validity, confidence, Unknown state, provenance, and trace metadata. No source payload or source Writer authority is copied into Context.

## 3. Output

The only output is an immutable `ContextEnvelopeCandidateV1` with:

- `context_id`;
- `version`;
- `temporal_scope`;
- seven optional source projection references;
- optional `mental_field_continuity_reference`;
- `provenance`;
- `trace_reference`.

The candidate always declares:

```text
skeleton_only = true
real_context_generation = false
runtime_executed = false
state_mutation = false
```

## 4. Context ownership boundary

Context Foundation owns only:

- Context Envelope Candidate assembly;
- Context reference validation and preservation;
- Context candidate version metadata;
- Context trace candidate metadata.

It does not own Field State, Observation, Memory, Self, Role, Relationship, Emotion, Intent, Causal, Decision, Action, or Runtime state.

Forbidden flows remain:

```text
Context -> Fact
Context -> Intent
Context -> Causal Explanation
Context -> Decision
Context -> Action
Context -> Source Mutation
```

## 5. Mental Field Carryover

`MentalFieldContinuityReferenceV1` preserves only cross-Field reference metadata:

- previous and current Field references;
- continuity type;
- duration-scope reference;
- intensity reference;
- release-condition references;
- Unknown, provenance, and source-Owner references.

It is not Memory, not Emotion State, and not Causal Explanation. The skeleton performs no pressure calculation, emotion calculation, cause inference, source mutation, or persistence.

## 6. Static validators

The validators confirm:

1. a Projection Owner exists and matches its Projection kind;
2. reference metadata is complete;
3. Unknown, Uncertain, and Multiple Candidates remain representable;
4. Context performs no Fact write;
5. Context creates no Intent output;
6. Context creates no Causal output;
7. Context owns no mutation authority;
8. carryover remains reference-only.

## 7. Synthetic fixtures

The controlled fixture set contains:

1. work-to-home Field transition with Mental Field carryover;
2. a minimal weather Context;
3. a tiredness expression with cause preserved as Unknown;
4. a job-change question with Role, Relationship, Memory, Self, and Emotion references but no Intent.

## 8. Side-effect boundary

- no Runtime execution;
- no database, file-state, network, model, provider, or device call;
- no source-object storage or mutation;
- no active Schema or Contract change;
- no modification of passed Context Planning or Alignment assets.

The Controlled Runner is a synthetic component asset. The phase instruction does not authorize Agent execution of it; the Agent performs V0 static checks only.

## 9. Stop condition

Stop after all required code and documentation assets pass V0 file, JSON, AST, compile, import-boundary, and side-effect checks. The Final Phase Verifier is reserved for the user terminal.

