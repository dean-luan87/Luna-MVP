# Terminal-Controlled Trial → Canonical Admission Migration

| Trial input | Current trial owner | Canonical target | Migration disposition |
|---|---|---|---|
| `--source` | Terminal | Observation/acquisition context ref | Keep as explicit test adapter input; later replace with source-owned ref |
| `--model-path` | Terminal | Model Manager governed path ref | Do not promote raw path to Brain/A authority |
| `--dependency-status` | Terminal or probe result | System Diagnostics evidence ref | Preserve unresolved state; later consume governed diagnostic evidence |
| `--declared-checksum` | Terminal or manifest | Model Manifest metadata ref | Populate from governed asset metadata; no CLI default approval |
| `--observed-checksum` | Terminal/provisioning candidate | Integrity evidence ref | Preserve provenance; no checksum computation in this phase |

## Migration sequence

1. Keep the current trial and Provider admission unchanged.
2. Define an adapter that maps terminal inputs to evidence refs, without
   changing their authority.
3. Compose Runtime Admission Assessment from existing Model/Diagnostics/
   Integrity/Provider evidence.
4. Require an accepted Runtime Admission candidate before constructing an
   Executable Capability Candidate.
5. Let the trial consume that candidate while retaining the one-invocation
   and `REQUEST_MORE_EVIDENCE` guards.
6. Remove terminal ownership only after a governed source exists and its
   dependent fixtures/verifiers are migrated.

## Explicit prohibition

The migration adapter must not invent checksum values, mark dependencies
verified, select a model/provider, or turn a terminal readiness argument into
canonical authority.

