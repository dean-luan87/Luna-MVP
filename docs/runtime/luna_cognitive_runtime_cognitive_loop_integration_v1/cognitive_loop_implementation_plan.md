# Cognitive Runtime Loop Integration Implementation Plan

## Scope

Connect the existing side-effect-free Runtime Foundation to a first Cognitive Tick. The tick assembles a context package, activates a workspace context, exposes an attention candidate, invokes a Brain boundary placeholder, records stage traces, and writes candidate state only to the runtime-owned state domain.

## Separation

Runtime Tick advances system time and receives events. Cognitive Tick consumes a prepared runtime state and produces a candidate package. Runtime Tick never creates a Decision Candidate by itself.

## Non-goals

No model, LLM, provider, hardware, camera, microphone, Action Runtime, real Learning, Emotion Runtime, Social Runtime, or Memory Consolidation is included.

## Validation

V0 parses and compiles all assets. User V2 executes an in-memory fixture covering event → context → workspace → attention → Brain boundary → candidate → trace → runtime candidate state. ChatGPT performs V3 audit.
