# A3 Verifier Independence Review v1

Verifier input source is serialized Runner output files, not Runner memory; it does not rerun Runner and recomputes file, Contract, baseline, count, uniqueness, flags, guards, and reference-summary checks. Current limitation: per-case semantic and guard evidence is trusted at serialized-check granularity rather than fully recomputed. Status: `non_blocking`. Future strengthening: independently recompute each semantic rule, guard proof, warning aggregation, and local reference inventory before Runtime Planning.
