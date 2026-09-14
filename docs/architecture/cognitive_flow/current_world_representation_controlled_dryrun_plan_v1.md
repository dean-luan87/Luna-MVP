# Current World Representation Controlled DryRun Plan v1

## 1. Planning-only purpose

This document reserves a future controlled dry-run plan for integration-contract review. It creates no runner, verifier, fixture file, runtime, reducer call, Read Model call, simulation execution, static check, database access, model call, or network access.

## 2. Fixed future fixture boundary

All future fixtures must be caller-fixed, synthetic, and immutable: an Admitted Event fixture, separate Reducer Output fixture, Field State, State Version, Transition Record, Field History Projection, Field Snapshot, and declared Context Inputs. They must not call a real Reducer or use system time/random identifiers as fact data.

## 3. Planned cases

| Case | Fixed setup | Required contract observation |
| --- | --- | --- |
| 1. Complete normal chain | Complete admitted event through separately supplied Snapshot and Context inputs | Reference and version chain is complete; only Reducer Output supplies State. |
| 2. State Version incomplete time | State Version has unknown/estimated temporal information | `state_version_chain_incomplete` or `temporal_order_unknown` is retained; chronology is not guessed. |
| 3. Snapshot updated, Context stale | New Snapshot version follows an older Context | Older Context becomes stale/refresh-required; it is not overwritten. |
| 4. Same Snapshot, multiple Contexts | One Snapshot with multiple distinct subject/task/goal scopes | Context isolation holds; no selection writes back to Snapshot or State. |
| 5. Context insufficient | Required declared input is absent or a critical gap blocks scope | `context_insufficient` blocks Cognitive Analysis entry; no model fill or default sufficiency. |
| 6. Evidence revoked | A source Evidence reference is marked revoked after derivation | Affected representation remains traceable and becomes `refresh_required`; no guessed replacement. |

## 4. Future checks

Future controlled review must check: reference/version-chain integrity; sole Reducer mutation authority; Snapshot/Context read-only behavior; retention of unknowns; recoverable exclusions; Context isolation; no raw-event Read Model fallback; and no Cognitive Analysis write-back.

## 5. Stop condition and exclusions

The future dry-run only verifies integration-contract behavior. It does not establish real-world correctness, model quality, Context-selection quality, Hypothesis validity, Decision quality, persistence, concurrency, performance, cross-device time correction, or networking. No execution is authorized by this planning document.
