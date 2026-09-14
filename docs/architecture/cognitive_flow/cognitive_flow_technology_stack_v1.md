# Cognitive Flow Technology Stack v1

## Selection Rule

Open-source components may supply storage, transport, indexing, graph traversal, orchestration, or observability. They cannot supply Luna's Field definition, evidence admission, hypothesis semantics, decision authority, experience judgment, or Hive value model.

| Technology | A0 status | Intended bounded role | Deferred decision / reason |
| --- | --- | --- | --- |
| Python | adopt for planning prototypes and contract tooling | deterministic domain services, schema/contract utilities, controlled evaluators | runtime implementation waits for A1/A2 contracts |
| PostgreSQL | defer | transactional persistence for approved records | no storage design before Field and Experience lifecycles stabilize |
| JSONB | defer with PostgreSQL | versioned flexible candidate payloads and provenance envelopes | must not become an ungoverned fact bucket |
| pgvector | defer | retrieval aid over approved evidence/experience references | vector similarity cannot decide experience reuse or truth |
| NetworkX | evaluate in A3/A5 | bounded local graph analysis for hypotheses and branch relation prototypes | no durable graph authority or Field definition |
| Neo4j | defer | optional cross-episode/branch graph storage | Neo4j cannot define Field, resolve contradictions, or own semantics |
| NATS | defer | lightweight event transport after protocol and delivery authority are stable | no real stream until admission/backpressure contracts exist |
| Kafka | defer | high-volume append-only event transport if scale requires it | no adoption before event lifecycle and operational need are proven |
| Temporal | defer | authorized long-running exploration and review workflow orchestration | workflows cannot become cognitive logic or action authority |
| OpenTelemetry | evaluate in A2 | traces across observation, admission, analysis, delivery, and outcome | trace telemetry is not evidence or a decision record |
| FastAPI | defer | explicit bounded API surfaces for approved modules | no public service before authority, auth, and lifecycle contracts are set |

## A0 Baseline

The current phase adopts no new operational technology. Planning outputs are Markdown only. Python is the expected first implementation language because the current Midplatform is Python-based, but this is not authorization to create runtime services.

## Non-Substitution Examples

- Neo4j may store links; it cannot define a Field or infer a governing relation type.
- An LLM may propose a hypothesis; it cannot be the source of fact or final conclusion.
- Vector search may retrieve similar episodes; it cannot judge whether experience applies.
- Kafka/NATS may transport events; neither admits them.
- Temporal may coordinate authorized work; it cannot decide what Luna should do.

