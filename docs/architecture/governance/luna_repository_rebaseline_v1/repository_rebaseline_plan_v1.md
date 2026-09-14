# Repository Rebaseline Plan v1

## Phase contract

Phase: Phase-P0-Luna-Git-Rebaseline-Governance-And-Manifest-Formation-v1-001. Stage: Governance and Manifest Formation. Execution Mode: Planning Only; V0 only.
Previous phase: Phase-P0-Luna-Git-Repository-Rebaseline-Planning-v1-001, user-reported LUNA_GIT_REBASELINE_PLAN_READY_FOR_USER_APPROVAL.
Input assets: .gitignore, current worktree, read-only Git index/history metadata, docs/architecture/luna_canonical_architecture_freeze_v1/{README.md,canonical_module_ledger_v1.md,canonical_legacy_deferred_ledger_v1.md}, module source/contracts/fixtures.
Mandatory pre-read: all nine role/authority/mode/instruction/template/naming/status/failure/compliance assets in ../luna_engineering_execution_and_verification_governance_v1/.
Allowed edits: this directory's seven files, root .gitignore, one docs/architecture/README.md link. Business source and old artifacts remain unchanged.
No checks may be weakened or hardcoded as passed. No scope expansion or automatic next phase.
Expected next: user review of proposed dispositions and gates, not Git execution.

## Snapshot and interpretation

Old HEAD: 051d0c6fb59292ea21819dc93ffaf11f8d72532b, branch phase4_modulator_v1_mvp, dated 2026-03-25.
Pre-existing index paths: 2394; tracked modifications: 17; tracked deletions: 4; staged changes: none at inspection.
Pre-edit untracked nonignored count supplied by preceding audit: 18791; this phase adds seven files and changes visibility.
The per-file inventory is authoritative for this preparation snapshot; no-follow filesystem enumeration excludes .git internals and external symlink contents.
A Git archive ref protects committed history only. It does not protect modified, untracked, ignored files or external symlink targets.
Preserve the complete current worktree in an independently verified backup before any future Git mutation.

## Inclusion method

Rules are proposed classification, not a semantic proof of every file's canonicality.
Current contracts/schemas/policies/registries, controlled implementations, evaluation code, runners/verifiers, fixtures, architecture/governance docs, dependency declarations, shared code and required compatibility are source candidates.
Caches, generated output, local jobs, model weights, raw media, secrets and unknown roles are removed from automatic inclusion first.
Canonical core code is qualified by existing ledgers; controlled/synthetic markers are preserved in source_role. CURRENT means current engineering asset, not production readiness.
Historical documentation is retained for traceability without claiming it remains authoritative.
Lexical matching cannot prove all importlib/sys.path/constructed path behavior. Unresolved candidates remain explicit in each record.

## Legacy / prototype matrix

| Asset | Current dependency evidence | Proposed disposition | Why |
|---|---|---|---|
| core_snapshot | tools/voice/run_voice_interaction_readiness_review_v0.py reads main.py | Source INCLUDE, LEGACY_COMPATIBILITY | Static dependency; no canonical promotion |
| Luna_Badge_MVP | guarded_trial/yolo_stage1_10_frame_executor_v0.py and model_perception/yolo_shadow_adapter_v0.py import YOLOv5Detector | Source INCLUDE; logs excluded; backups reviewed | Controlled dependency closure |
| Luna-mid | test_learning_systems.py and test_learning_manager.py dynamically load core files | INCLUDE, LEGACY_TEST_COMPATIBILITY | Root tests retain legacy dependency |
| Old Decision Center / Task / Watchdog | canonical integration adapters still reference historical skeleton/types | INCLUDE, LEGACY_COMPATIBILITY | Ownership migration stays out of scope |
| modules/voice.py | main.py imports Voice | INCLUDE, LEGACY_COMPATIBILITY | Required old entry dependency |
| capabilities/mid_platform | Existing controlled gates and tools | INCLUDE, CONTROLLED_SOURCE/COMPATIBILITY | Not interchangeable with midplatform |
| root mid_platform | model_governance/README.md declares P0/P1/P2 placeholders and tests | INCLUDE, CONTROLLED/PLANNING | No automatic scoring, execution or registry mutation |
| luna_frontend_package_24files | No external-root Python import found; JS/HTTP dependency not proven | REVIEW_REQUIRED, PROTOTYPE_PRESERVED | User decides maintenance scope; preserve locally |
| luna_backend | Internal imports exist; cross-root use not established by lexical scan | REVIEW_REQUIRED, PROTOTYPE_PRESERVED | Negative import evidence is not proof of dead code |
| Old navigation / demos / viewers | Source retained conservatively with old modules/tests | INCLUDE source as compatibility/prototype; data separately reviewed | No physical cleanup or owner changes |

New-lineage exclusion never authorizes worktree deletion. Untracked historical assets must be backed up externally; old Git history alone cannot preserve them.

## Source scope and review gates

The asset disposition contains exact candidate paths, byte sizes, effective ignore flags, local reference edges, unresolved lexical candidates and external import candidates.
Known gaps include included callers of config.py (portability/security review), real-image fixtures (provenance/privacy/license review), and external model weights (digest/location/license binding).
Generated artifact references may be output destinations or intentional evidence readers; classify their role before marking a gap resolved.
Dynamic imports, relative string concatenations, namespace packages, plugin discovery and third-party version closure are not proven by lexical inspection.
No automatic INCLUDE of UNKNOWN; no secret-containing source accepted; no forced staging to bypass ignore rules.
REMOTE_CREDENTIAL_ROTATION_REQUIRED_BEFORE_PUSH. No credential values, prefixes or original authenticated URL are retained in these assets.
Credential remediation is user-owned and outside this phase. Even old-history pushes require historical secret review.

## Future exact-path export contract

DO NOT RUN YET. After user approval, refresh filesystem/status/ignore/security/dependency checks against the same canonical root.
Resolve every required dependency and review item, then explicitly change approved record status to APPROVED under a newly authorized phase.
Candidate list today: decision == INCLUDE AND approval_status == PROPOSED.
Actual staging list later: decision == INCLUDE AND approval_status == APPROVED, present regular file, no symlink ancestor, no unresolved blocker.
Sort unique repository-relative paths by UTF-8 byte order; prohibit absolute paths, '..' segments, NUL, duplicate/case-collision paths and .git paths.
Export literal paths separated and terminated by NUL to /Users/luanlei/Luna-Rebaseline-Backups/20260910/approved-baseline-paths.nul.
Do not create this file in the repository. Recheck content hashes, executable modes and approved list immediately before staging; any drift invalidates approval.
The list is not produced by globbing capabilities/** or git add .; no blanket force add.

## History preservation and future transition — DO NOT RUN YET

1. Stop parallel edits. Record HEAD, branch, index state, worktree snapshot and every external asset reference.
2. Back up current worktree INCLUDING ignored/untracked files and Git metadata to a protected external location; test a restore in a separate location. Git metadata backup may contain credentials and must never be published.
3. Create/verify old-history bundle for all existing refs in the future authorized execution phase. Bundles do not back up dirty worktree content.
4. Retain phase4_modulator_v1_mvp and all old branches. Plan archive branch archive/pre-rebaseline-20260910 and annotated tag archive-pre-rebaseline-20260910 pointing to the old HEAD. Branch is navigable lineage; tag is a named checkpoint. Neither is created now.
5. Do not use git switch --orphan in this dirty worktree: tracked files can be removed. Approved future plumbing may use git symbolic-ref HEAD refs/heads/luna-current-baseline followed by git read-tree --empty WITHOUT -u, after archive/backup/index checkpoints. These alter HEAD/index, not working files; these commands remain prohibited in this phase.
6. Stage only the approved external NUL list with literal pathspec handling. Review staged path equality, source hashes, modes, symlinks, binary sizes, secret scan and tree contents independently. No recursive git rm.
7. Commit only after a fresh explicit user authorization. Record resulting SHA externally; never invent it or create a self-referential commit hash inside that same commit.
8. Baseline commit records reproducible source, not full correctness. Later source verification must be separately authorized.

Suggested first commit subject:
`chore(repo): establish Luna current source baseline v1`

Suggested body:
- Establishes current Luna source baseline LUNA_CURRENT_SOURCE_BASELINE_V1_20260910.
- Replaces old 2026-03 lineage as active development baseline; historical Git lineage is preserved separately.
- Does not imply full repository verification or production readiness.
- GPT-6 audit findings F-01 through F-11 remain open.
- Future engineering freezes must bind to Git source baseline.

Orphan history keeps old objects/refs and audit context in the existing repository. Deleting .git would discard this protection and is forbidden.
No old main rewrite or force push is planned.

## Remote stages

A: Only after credential rotation/removal is confirmed and both new/old history secrets are reviewed, push explicitly approved archive refs and the independent new branch. No network work now.
B: User inspects remote source tree, baseline completeness, sizes, secrets and old-history reachability.
C: A later explicit decision may change default branch or name main. Never silently overwrite remote main or force-push old lineage.

## Rollback / recovery

- Failed orphan preparation does not erase old history: original branch/archive refs still point to old HEAD.
- Never recover by reset --hard, clean, checkout overwrite, recursive rm or deleting .git.
- Preserve new worktree edits and any new commit/ref first. Inspect old history separately; do not switch branches over unprotected files.
- Authorized recovery can restore saved HEAD/index metadata without touching working files, then reconcile the recorded path manifest.
- A filesystem backup is required to recover untracked/ignored/modified content; history refs cannot do it.
- Verify missing-tracked assets individually. The four old deleted paths remain tombstones; do not restore them mechanically. Two reports are behind an external reports symlink.
- Re-run planning refresh after recovery. No baseline may be called established until the actual commit and approved source tree agree.

## Approval checklist and next execution preconditions

- [ ] User accepts or resolves every REVIEW_REQUIRED asset and dependent source requirement.
- [ ] External assets have portable identifiers, digest, version/source/license/archive location and restore instructions.
- [ ] All approved source files pass security review; history/remote remediation is separately confirmed before any push.
- [ ] Effective ignore policy checked including .git/info/exclude and global excludes; no approved source is hidden.
- [ ] Dependency gaps/dynamic resolution reviewed; source list and required inputs form the declared reproducibility scope.
- [ ] Independent dirty-worktree backup and old-history recovery tested.
- [ ] Exact approved list, byte totals, source manifest hash and mode map are refreshed.
- [ ] User explicitly authorizes Git Rebaseline Execution; this preparation does not do so.
