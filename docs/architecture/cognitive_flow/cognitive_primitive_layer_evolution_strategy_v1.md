# Luna Cognitive Primitive Layer Evolution Strategy v1

## Extension Principle

Luna may add Primitive types, attributes, Context-specific variants, and domain-specific variants without allowing external providers to define its cognitive structure. Internal Primitive evolution is governed by Luna's candidate, traceability, and authority boundaries rather than provider payload shape.

## Allowed Evolution

| evolution | requirement |
| --- | --- |
| new Primitive family | declared internal purpose, candidate semantics, provenance/trace retention, and Field/Decision boundary |
| attribute evolution | compatible interpretation, uncertainty retention, and consumer impact assessment |
| Context-specific Primitive | explicit Context scope; no Context writeback or general truth claim |
| domain-specific Primitive | mapping to common candidate envelope and no parallel Fact/State authority |

## Change Restrictions

Primitive evolution must not:

- weaken `candidate_only=true` or `fact_status=not_fact`;
- make provider labels/type systems Luna's canonical internal vocabulary;
- add a State mutation, Fact, Decision, Action, Memory, or Runtime permission;
- change Field Kernel/Reducer ownership; or
- suppress provenance, trace, uncertainty, or contradictory candidates.

High-impact changes that alter candidate meaning, primitive family semantics, field-event mapping, or consumer/Protocol compatibility require separate Protocol and governance review with migration/rollback evidence.

