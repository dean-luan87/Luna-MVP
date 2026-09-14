# Dynamic Cognitive Architecture v2 Freeze Gate

The freeze gate consumes immutable migration and validation evidence. It requires:

- all planned migration records closed or explicitly blocked;
- all mandatory architecture nodes and cognitive-chain edges present;
- unique owners and no old/new dual mainline;
- no unassigned or `TBD` assets;
- boundary checks passed;
- regression results passed for all mandatory capabilities;
- documentation, contracts, manifests, and code mapping consistent;
- compatibility aliases and rollback plans verified where applicable;
- unresolved risks either closed or explicitly accepted by governance.

The gate outputs a `Freeze Decision Candidate`. It does not rewrite the active
Architecture Baseline, enter Intent planning, or authorize implementation. Those
actions require a separate phase decision.

