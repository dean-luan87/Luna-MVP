# Cognitive Primitive Layer Controlled Skeleton Plan v1

The A3 skeleton is an isolated in-memory builder for five internal Primitive Candidate families. It reuses the frozen Translation reference/provenance boundary and complements—not replaces—the existing A1 `cognitive_primitives` candidate API.

It exposes only `create_candidate()`, `validate_candidate()`, and `serialize_candidate()`. It does not invoke Translation, a model, Provider, database, Field Kernel, Reducer, Admission, Read Model, Runtime, or consumer.

