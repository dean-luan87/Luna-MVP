# Cognitive Memory Runtime Integration Implementation Plan

## Scope

Implement a deterministic in-memory pipeline that records cognitive outcomes as Experience Records, produces Memory Candidates, requires explicit Memory Governance review, stores validated entries in separate Self and Social stores, and retrieves context-bound candidates.

## Self Rhythm integration

Self Rhythm supplies an advisory retention budget. Low-power and recovery modes reduce candidate intake hints and prefer high-value records. Memory Runtime does not control resources, scheduling, models, or providers; Runtime retains acceptance authority.

## Non-goals

No automatic learning, model training, weight update, personality rewrite, Emotion Runtime, Social Runtime, direct Brain override, Reality mutation, Identity mutation, Goal mutation, or external persistence.

## Validation

V0 parses/contracts and compiles the skeleton. User V2 exercises capture → candidate → explicit review → commit → scope-separated retrieval and verifies that unvalidated candidates cannot be stored.
