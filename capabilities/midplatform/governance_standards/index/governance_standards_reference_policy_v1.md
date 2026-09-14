# Governance Standards Reference Policy V1

**Phase:** `Phase-P1-Midplatform-Governance-Standards-Packaging-Execution-And-Post-Review-v1-001`

## Rules

1. Subsequent phases **must prefer** canonical paths under `capabilities/midplatform/governance_standards/`.
2. Original phase artifacts remain **historical evidence** — never delete.
3. Main program **must not** embed full governance rule text.
4. Runtime **must** use admission gate outputs.
5. Output adapter **must not** read candidate output without admission.
6. Semantic / fact / navigation **must not** consume inference trial output directly.
7. If `rule_id` exists in inventory — **must reuse**.
8. Extensions require **standard patch phase**.
9. No ad-hoc duplicate governance rules in business phases.

## Reuse-before-create

Search `legacy_rules/legacy_reusable_governance_rules_inventory_v1.json` before creating new rules.

## Standard patch

Canonical rule changes require `Phase-*-Standard-Patch-*` — no silent edits.
