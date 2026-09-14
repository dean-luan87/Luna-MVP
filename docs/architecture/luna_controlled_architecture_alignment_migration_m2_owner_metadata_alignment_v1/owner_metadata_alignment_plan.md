# M2 Owner Metadata Alignment Plan

## 1. Phase position

`Phase-Luna-Controlled-Architecture-Alignment-Migration-M2-Owner-Metadata-Alignment-v1-001` maps the owner, producer, consumer, write-authority, and forbidden-responsibility boundaries frozen by M1 into planning-only governance metadata candidates.

This phase does not edit active owner metadata. It does not modify capability registry entries, module baselines, schemas, contracts, code, Runtime, or directories outside this phase output directory. Every new asset is a `PLANNING_CANDIDATE`.

## 2. Owner interpretation rule

Architecture-domain placement is not ownership transfer.

- Field System is the architecture domain; Field State Reducer remains the active Field state writer.
- Cognitive OS Governance is the architecture domain; Protocol Manager remains the active protocol module owner.
- Capability Governance contains Model, OCR, and Vision capabilities without becoming their cognitive-output owner.
- Personal Cognitive Network, Intent, Causal Reasoning, Experience Compression, A/B Route, and Decision Arbitration remain architecture or future references and receive no active registry or Runtime authority.

Projection authority never implies source-object ownership or source mutation.

## 3. M2.0 — Owner Inventory Alignment

### Do

- Reconcile M0 module owners, M1 schema owners, active module baselines, and the migration ownership matrix.
- Record current Owner, candidate Owner, architecture position, Owner status, write authority, readers, forbidden responsibility, and source evidence.
- Distinguish `ACTIVE_EXISTING` owner records from `PLANNING_CANDIDATE` future owner records.

### Do not

- Do not write capability registry records.
- Do not edit active owner metadata or active baselines.
- Do not convert an architecture owner into an active implementation claim.

### Input

- M0 module responsibility registry;
- M1 schema ownership mapping;
- controlled migration ownership matrix;
- eight active capability baselines;
- Memory architecture boundary.

### Output

- `owner_alignment_registry_candidate.json`.

### Verification

- all 15 required assets are covered;
- source references resolve;
- existing module Owners remain unchanged;
- future cognitive Owners remain planning candidates.

### Stop condition

Stop if an existing Owner cannot be reconciled, a future Owner is presented as active, or an active metadata edit becomes necessary.

## 4. M2.1 — Responsibility Boundary Alignment

### Do

- Record one responsibility statement per Owner.
- Record disjoint write scopes and governed read scopes.
- Record forbidden responsibilities for every Owner.
- Preserve candidate/fact, Decision/Action, Memory/PCN, and Field/Observation separation.

### Do not

- Do not create a second writer.
- Do not grant PCN source ownership or persistence.
- Do not grant Task Manager Intent or Causal authority.
- Do not grant Observation cognition or Decision authority.

### Input

- M1 contract candidates;
- M0 canonical responsibility language;
- active baseline forbidden-authority sets.

### Output

- `responsibility_boundary_matrix_candidate.json`.

### Verification

- each Owner has responsibility, forbidden responsibility, write scope, and read scope;
- write scopes have one accountable Owner;
- PCN, Task, Observation, and Memory negative boundaries are explicit.

### Stop condition

Stop on duplicate write scope, missing forbidden responsibility, or ownership transfer by projection.

## 5. M2.2 — Metadata Candidate Generation

### Do

- Map active capabilities to Dynamic Cognitive Architecture positions.
- Use `KEEP` where active responsibility already matches.
- Use `BOUNDARY_ALIGNMENT_ONLY` where an architecture-domain label must be recorded without changing the module Owner.
- Use `FUTURE_REFERENCE` for unimplemented cognitive capabilities and boundaries.

### Do not

- Do not use `FUTURE_REFERENCE` as implementation evidence.
- Do not create or update active registry entries.
- Do not set `migration_required` to true in M2.

### Input

- owner alignment registry candidate;
- active module baselines;
- M1 compatibility matrix.

### Output

- `capability_registry_alignment_candidate.json`.

### Verification

- every record uses an allowed alignment type;
- baseline or architecture reference exists;
- all records keep `migration_required=false`;
- no active registry or baseline change is requested.

### Stop condition

Stop if alignment requires an active registry write, baseline edit, capability implementation, or second mainline.

## 6. M2.3 — Conflict Validation

### Do

- Review duplicate Owner, duplicate Writer, Owner drift, and permission conflict risks.
- Record the resolution for every required asset.
- Keep unresolved items in `conflicts` and count them as blockers.

### Do not

- Do not hide conflicts by renaming Owners or weakening forbidden-responsibility rules.
- Do not mark a conflict resolved when active metadata change is required.

### Input

- owner and responsibility candidates;
- M1 owner/write boundaries;
- migration risk register.

### Output

- `owner_conflict_review.json`.

### Verification

- review coverage includes all 15 assets;
- conflict and blocker counts are consistent;
- no dual Owner, dual Writer, Owner drift, or permission conflict remains.

### Stop condition

Stop on any unresolved conflict or any need to modify active Owner metadata.

## 7. M2.4 — Migration Readiness Review

### Do

- Confirm that M2 candidate metadata is complete enough for a future M3 Runtime Boundary Alignment review.
- Confirm that M2 itself performs no migration or Runtime work.
- Record exact created-file and no-side-effect boundaries.

### Do not

- Do not start M3.
- Do not inspect or modify Runtime beyond previously frozen reference boundaries.
- Do not execute migration.

### Input

- completed M2 candidate registries and conflict review;
- phase contract;
- change manifest.

### Output

- V0 static readiness candidate;
- exact user-terminal V2 command.

### Verification

- required files exist and parse;
- verifier compiles with standard-library imports only;
- manifest records no code, Runtime, baseline, registry, or active metadata changes;
- migration remains false and M3 remains false.

### Stop condition

Stop at `WAITING_FOR_USER_TERMINAL_VERIFICATION`. M3 requires separate authorization after user V2 and ChatGPT V3.

## 8. Current planning finding

The M2 planning review finds no required Owner transfer and no active-metadata edit requirement. Existing module Owners remain authoritative, while future cognitive Owners remain planning-only references. This finding is not a migration decision or Runtime readiness claim.
