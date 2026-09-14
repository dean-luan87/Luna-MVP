# A3 Controlled DryRun Canonical Output Baseline v1

Alignment purpose: correct document references to the actually verified output.

- canonical baseline: `_eval_out/a3_cognitive_analysis_controlled_dryrun_v1_smoke_v0_run1/`
- deterministic comparison: `_eval_out/a3_cognitive_analysis_controlled_dryrun_v1_smoke_v0_run2/`
- deprecated nonexistent reference: `_eval_out/a3_cognitive_analysis_controlled_dryrun_v1_smoke_v0/`
- legacy reference status: `deprecated_nonexistent_reference`

Run1 is the sole canonical baseline: Runner/Verifier passed, 8/8 cases,
zero blockers/dangling/cross-case refs, 24 guards, immutable fixtures,
expected eight warnings, zero runtime/writeback, and six output files.
Run2 is comparison evidence only, never a second baseline.

Inventory: run result, case results, negative guard report, reference closure,
verification result, and summary. Final Closure must use run1; it may read
run2 only as deterministic evidence. Future reruns require a new suffix (for
example `run3`) and may not overwrite/rename history. No implementation or
output artifact changed in this alignment phase.
