# Cognitive Decision and Execution Separation Architecture Plan v1

## Purpose

This Planning Only phase separates Cognitive Decision Support, Commitment, Execution Boundary, Reality Feedback, and Experience feedback. It does not implement Decision Engine, Action, executor, permission system, Human control, Embodiment, Runtime, or State mutation.

## Separation model

`Understanding -> Candidate -> Evaluation -> Commitment Candidate -> Human / External Executor Boundary -> Outcome Observation -> Experience`.

Current execution boundary: Luna provides governed candidates; Human Action Authority performs real-world action. Future embodiment may receive a Permission-Controlled Action Candidate interface only after separate admission; it is disabled here.
