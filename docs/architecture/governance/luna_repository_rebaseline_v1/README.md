# Luna Repository Rebaseline Governance v1

Phase: `Phase-P0-Luna-Git-Rebaseline-Governance-And-Manifest-Formation-v1-001`  
Execution Mode: **Planning Only** — governance formation and V0 static inspection.  
Canonical root: `/Users/luanlei/Desktop/Luna-Core`.

## Current work

本阶段位于 GPT-6 全仓审计后的工程可信化阶段。不修认知架构，只回答：当前 Luna 源码是什么、如何被 Git 可靠固化、未来 Runner/Verifier 如何绑定真实 source version。

前置：GPT-6 full repository audit → Repository Source Baseline Audit → Git Rebaseline Planning。
后续（仍需分别授权）：Git Rebaseline Execution → Verifier Trust Hardening → Admission Semantics Hardening → Lineage Hardening → Canonical Ownership Migration → Current World → A-Route Cognitive Result Integration。

Direction: OLD HISTORY PRESERVED + CURRENT LUNA CLEAN REBASELINE + NEW ORPHAN LINEAGE.
Git inclusion does not promote controlled, synthetic, compatibility, planning or deferred assets to canonical runtime.
F-01 through F-11 remain OPEN / KNOWN, including F-06 until an actual reproducible baseline is established.

## Seven assets

- [Plan, boundaries, recovery and approval gates](repository_rebaseline_plan_v1.md)
- [Baseline planning manifest](current_source_baseline_manifest_v1.json)
- [Per-file disposition and static dependency review](baseline_asset_disposition_v1.json)
- [.gitignore changes and inspection](gitignore_rebaseline_proposal_v1.md)
- [Git Freeze Routine](git_freeze_routine_v1.md)
- [Artifact/source binding contract](artifact_source_binding_contract_v1.json)

This README is the seventh asset. The disposition is a machine-readable inventory, not runtime input.
Every decision is PROPOSED, not staging approval. REVIEW_REQUIRED and UNKNOWN cannot be silently included.
Inventory counts describe a live worktree snapshot, not HEAD and not a frozen source tree.

## Authority and stop boundary

Only file reading, static lexical analysis, JSON parsing, scoped governance edits and git read-only checks were authorized.
No Python, imports of repository code, runner, verifier, pytest, Provider, model, runtime or network invocation.
No branch/tag/orphan/index/staging/commit/push/remote mutation. No deletion, move or cleanup.

V0 is an engineering inspection, not verification success. V1 is not authorized. V2 remains user-terminal-only; V3 remains separate.
The phase-specific report status requested by the user does not extend the canonical verification status registry.
Canonical verification posture remains BLOCKED_BEFORE_USER_TERMINAL_VERIFICATION while source-scope gates are unresolved.
No new phase verifier was created: the seven-file boundary does not authorize it.

Governance documents can be ready for user review while source scope remains blocked.
Read the manifest's source_scope_status and execution_gates before any future transition.
