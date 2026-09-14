# Luna Git Freeze Routine v1

## Meaning and scope

GO != ENGINEERING_FROZEN. ENGINEERING_FROZEN != PRODUCTION_READY.
GO is scoped functional/contract verification approved through user-terminal verification and the separate final audit authority.
ENGINEERING_FROZEN adds local documentation, Notion receipt, explicit Git source baseline and source/evidence binding.
This document does not grant GO, create a release, close F-01–F-11, or change canonical cognitive ownership.

The new baseline is CURRENT_LUNA_SOURCE_BASELINE, not FULLY_VERIFIED.
Its first establishment is distinct from a functionally verified Phase freeze.
Existing evidence is UNBOUND_LEGACY_EVIDENCE unless contemporaneous source identity can actually be established; assigning a new commit retrospectively is forbidden.

## Routine

1. Development: dirty worktree allowed. Agent changes only authorized paths; unrelated parallel work stays separate.
2. Scope Freeze: owner declares changed source, contracts, fixtures, policies, dependencies and verifier scope; stop competing writes.
3. Input/Source Manifest: enumerate exact source and input paths, content hashes, executable modes, dependency versions and external references. Record dirty state and HEAD without pretending HEAD represents dirty content.
4. User Terminal Runner/Verifier: user runs the authorized commands against that recorded snapshot. Agent does not execute Final Phase Verifier. Capture full outputs and result digests.
5. GO: only the established user-terminal plus final-audit authority can grant this scoped decision.
6. Local Docs: update phase/module/baseline docs without changing validated behavior.
7. Notion Sync: capture page/version/time receipt, no credential data. Missing sync is a freeze blocker, not permission for the agent to use a network service in an offline phase.
8. Git Diff Review: inspect status, changed/deleted/untracked files, ignored source, selected artifacts, secrets and large binaries. Separate parallel work.
9. Explicit Staging: only approved literal paths. Never default to git add . or blanket force add. Staged path set and content must equal approved scope.
10. Commit: phase/module-bound subject and body; inspect hooks/filters/signing requirements before future execution. Commit is not an implicit runtime/test authorization.
11. Artifact/Source Binding: compare verified source/input manifest with committed source. If different, stop and invalidate or conduct impact review; do not just attach the new SHA.
12. Freeze Receipt: record commit, verified-source hash, runner/verifier digests, docs receipt, Notion receipt, staged scope and unresolved findings.
13. ENGINEERING_FROZEN: only after all receipts and authority gates are satisfied. A separate external receipt or subsequent DOC_ONLY_FREEZE commit avoids self-referential SHA requirements.

## Changes after verification

Any source/schema/contract/fixture/policy/dependency/verifier change must be marked INVALIDATED_FOR_CHANGED_SOURCE or REQUIRES_IMPACT_REVIEW.
An impact review names exact changed paths and explains whether rerunning user verification is required. It cannot silently declare old evidence applicable.
Runner logic and input/external-asset changes also invalidate automatic reuse.
DOC_ONLY_FREEZE is allowed only when executable/verification/input identity is unchanged and a reviewed diff proves documentation-only impact.
Updating a filename, status or hash field cannot upgrade unbound historical evidence.

## Minimal enforcement

- Preserve rejected/insufficient/unresolved outcomes; do not manufacture a pass to freeze.
- No hidden staging of unrelated dirty files.
- No staging secrets, caches, local environment or full output archives.
- If approved source is ignored, resolve the rule explicitly rather than using blanket force add.
- Tags are optional major checkpoints, not required for each small phase.
- Notion/local docs/Git receipts are all required; absence means NOT_FROZEN.
- A failed freeze leaves development recoverable; do not clean/reset the worktree.
- Existing docs/DEVELOPMENT_WORKFLOW.md examples using git add . are historical, not this routine's authority. They were not edited in this phase.
- Remote publication is separate from a local freeze; unresolved remote credentials forbid push.
- This routine is an engineering governance record, never a runtime input or a new canonical business protocol.
