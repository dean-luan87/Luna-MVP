# Luna Controlled Architecture Alignment Migration Sequence v1

## Position

This document defines the future controlled migration order for Luna Dynamic
Cognitive Architecture v2. It is a planning asset only. It does not change code,
Runtime, directories, active baselines, or existing architecture assets.

The sequence is monotonic:

```text
M0 Documentation Alignment
  ↓
M1 Schema / Contract Alignment
  ↓
M2 Owner Metadata Alignment
  ↓
M3 Runtime Boundary Alignment
  ↓
M4 Migration Integrity Validation
  ↓
M5 Architecture Freeze
```

No phase may be skipped. Each future phase needs separate authorization, its own
scope, V0/V1 authority decision, user-terminal V2, and ChatGPT V3 audit.

## Phase M0 — Documentation Alignment

### Do

- Reconcile Dynamic Cognitive Architecture v2 terminology with canonical current
  assets and owners.
- Mark every item as existing, architecture-only, future migration, or blocked.
- Add cross-references from the new architecture candidate to source assets.
- Preserve the original documents and record supersession rather than silently
  rewriting history.

### Do not

- Do not modify Python code, Runtime, module APIs, schemas, directories, or active
  baselines.
- Do not describe Personal Cognitive Network, Causal Runtime, B Route Runtime, or
  Experience Compression Runtime as implemented.

### Input

- Architecture v2 candidate;
- existing asset migration inventory;
- cognitive ownership matrix;
- active capability baselines;
- prior V2/V3 phase evidence.

### Output

- documentation-alignment change set candidate;
- canonical terminology map;
- unresolved-document conflict register;
- immutable pre-alignment references.

### Verification

- all links resolve;
- every claim is labelled implemented, architecture-only, or future;
- no existing owner is overwritten;
- no code or Runtime file changes;
- old and new documents do not claim two active mainlines.

### Stop condition

Stop when an asset has no canonical owner, a document claims an unimplemented
Runtime, or a terminology change would alter existing API semantics.

## Phase M1 — Schema / Contract Alignment

### Do

- Define compatibility-only candidate contracts for Field Context projection,
  Personal Cognitive Network references, Intent binding, Causal candidates,
  Experience Memory projections, A/B handoff, and Decision inputs.
- Preserve candidate/fact, trace/replay, unknown, admission, revision, and
  revocation semantics.
- Define rollback and legacy compatibility before any future adapter work.

### Do not

- Do not implement adapters, mutate schemas used by active modules, write Memory,
  create network persistence, run models, or execute cognitive flows.

### Input

- M0 verified documentation mapping;
- existing public schemas and API contracts;
- owner matrix;
- dependency graph;
- risk register.

### Output

- contract-alignment candidates;
- compatibility matrix;
- rollback contract candidates;
- blocked-contract list.

### Verification

- producer and consumer are explicit;
- each contract has one owning responsibility;
- candidate/fact semantics and failure behavior are explicit;
- source owner precedence is preserved;
- no circular migration dependency is introduced.

### Stop condition

Stop when a contract creates a second writer, transfers source ownership to the
Personal Cognitive Network, bypasses Field State, or cannot preserve legacy API
compatibility.

## Phase M2 — Owner Metadata Alignment

### Do

- Align registry and architecture metadata to the frozen ownership matrix.
- Record old owner label, canonical owner, responsibility, forbidden authority,
  and compatibility evidence for each bounded asset slice.
- Keep active module baselines immutable unless a separately governed rebaseline
  trigger is proven.

### Do not

- Do not move files, rename imports, merge modules, delete historical assets, or
  use metadata changes to grant Runtime authority.

### Input

- M1 verified contract candidates;
- active registry entries and module baselines;
- ownership matrix;
- duplicate-owner risk register.

### Output

- owner-metadata patch candidate;
- owner compatibility evidence;
- duplicate-owner closure candidate;
- explicit blocked owner records.

### Verification

- every responsibility has one canonical owner;
- every asset retains an accountable current owner;
- PCN owns only links, activation, and projection;
- Task Manager, Model Manager, Memory, Field, and Action boundaries match their
  baselines;
- no `TBD` or unassigned owner reaches the next stage.

### Stop condition

Stop on any owner conflict, ownership transfer by projection, or baseline change
without an approved rebaseline workflow.

## Phase M3 — Runtime Boundary Alignment

### Do

- Plan and review future interface boundaries between verified contracts and
  existing Runtime surfaces.
- Treat the root A3 Runtime and documentation-only cognitive Runtime skeletons as
  distinct existing assets until explicit compatibility is proven.
- Define one bounded future integration slice, rollback, monitoring, and failure
  isolation at a time.

### Do not

- Do not activate Runtime, change schedulers, invoke models/providers, write
  databases, execute actions, or infer that similarly named legacy fields already
  implement Architecture v2.

### Input

- verified M0–M2 artifacts;
- existing Runtime interface inventory;
- module baselines and public APIs;
- boundary and regression contracts.

### Output

- Runtime-boundary alignment candidate;
- bounded integration-slice candidate;
- rollback and monitoring plan;
- explicit non-equivalence records for legacy Runtime names.

### Verification

- no Runtime or business runner is executed in planning mode;
- Decision remains separate from Action;
- Task Manager remains orchestration only;
- Model/OCR/Vision remain capability/evidence providers;
- Field reducer and source owners remain authoritative.

### Stop condition

Stop when a Runtime interface would bypass governance, change an active API, grant
new authority implicitly, or lack a reversible migration plan.

## Phase M4 — Migration Integrity Validation

### Do

- Validate architecture completeness, asset ownership, boundary integrity,
  migration dependency closure, documentation/code consistency, and regression
  preservation using separately authorized checks.
- Cover Field State Reducer, Observation, Vision, OCR, Model Admission, Task
  Manager, Protocol Manager, Memory boundaries, Decision/Action separation, and
  trace/replay.
- Produce passed, blocked, or remediation-required results with immutable evidence.

### Do not

- Do not weaken checks, edit baselines to match failures, hardcode pass, execute
  unapproved Runtime, or freeze the architecture automatically.

### Input

- closed M0–M3 migration records;
- before/after evidence;
- compatibility and rollback evidence;
- required regression registry;
- unresolved risk register.

### Output

- architecture integrity result candidate;
- ownership and boundary result candidates;
- chain and regression result candidates;
- remediation or rollback candidate.

### Verification

- all required architecture nodes are present;
- all owners are resolved and unique by responsibility;
- the migration chain is closed and acyclic;
- all mandatory regression results pass;
- no old/new dual mainline remains;
- user-terminal V2 and ChatGPT V3 are required.

### Stop condition

Stop on any failed or not-run mandatory check, unresolved critical risk, broken
chain edge, missing rollback evidence, or boundary violation.

## Phase M5 — Architecture Freeze

### Do

- Consume immutable M4 evidence and prepare a Dynamic Cognitive Architecture v2
  freeze decision candidate.
- Record closed migration records, residual risks, compatibility aliases, and the
  exact baseline candidate to be promoted.

### Do not

- Do not rewrite the active baseline, start Intent/PCN/Causal implementation, or
  enter the next phase automatically.

### Input

- complete M4 integrity results;
- closed migration and risk records;
- rollback evidence;
- documentation/code mapping;
- user V2 and ChatGPT V3 evidence.

### Output

- freeze decision candidate;
- remediation-required candidate; or
- blocked candidate.

### Verification

- P3/M4 integrity gate is complete;
- every mandatory condition in the freeze contract is satisfied;
- no unassigned asset, duplicate mainline, or unresolved critical risk remains;
- baseline activation still requires separate authority.

### Stop condition

Stop unless all mandatory conditions are satisfied. A freeze candidate is not a
Runtime activation and does not authorize the next implementation phase.

## Global planning boundary

This phase defines the sequence only. Current values are:

- `migration_execution = false`;
- `runtime_change = false`;
- `directory_change = false`;
- `existing_asset_change = false`;
- `architecture_freeze = false`.

