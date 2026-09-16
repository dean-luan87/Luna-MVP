# F-06 Repository Reconstructability Closure GO V1

## Original finding

```text
F06_ORIGINAL_FINDING = HEAD_CANNOT_RECONSTRUCT_AUDITED_ENGINEERING_OBJECT
```

The original audited state used:

- **Old HEAD:** `051d0c6fb59292ea21819dc93ffaf11f8d72532b`
- **Old branch:** `phase4_modulator_v1_mvp`

The then-current engineering object materially exceeded what that HEAD could
reconstruct. This record does not classify every old untracked item as
canonical source.

## Root cause and finding class

F-06 was repository/source solidification debt:

```text
F06_ROOT_CAUSE_CLASS = SOURCE_BASELINE_AND_VERSION_BINDING_GAP
current engineering source != committed reconstructable Git source identity
```

This was a source/version binding problem, not a cognitive runtime authority
defect.

## Rebaseline remediation

The remediation occurred through the deliberate current-source rebaseline and
subsequent committed engineering lineage, rather than through new F-06 source
changes.

```text
CURRENT_SOURCE_BASELINE_ID = LUNA_CURRENT_SOURCE_BASELINE_V1_20260910
CURRENT_SOURCE_BASELINE_ROOT = 0144bec0a0ffd425222521c907c3bbb3e6e0143f
ROOT_PARENT_COUNT = 0
CURRENT_SOURCE_BASELINE_RECEIPT = 9a9a559160759d5c1b940b580de3c548bb568c15
RECEIPT_PARENT = 0144bec0a0ffd425222521c907c3bbb3e6e0143f
```

Historical source-set hash:

```text
sha256:f6d4853561c8ab33ba7fc585a47c80933347807328fb73ad073e794f7578fe62
```

This hash binds the historical approved rebaseline source set. It is not the
current post-F01-F05 whole-repository hash.

## Baseline disposition

```text
INCLUDE = 21010
EXCLUDE = 11623
EXTERNALIZE = 93
REVIEW_REQUIRED = 0
IGNORED_INCLUDE_COUNT = 0
DEPENDENCY_GAP_COUNT = 0
EXTERNAL_BINDING_INCOMPLETE_COUNT = 0
SECRET_CANDIDATE_COUNT = 0
```

The baseline root tree contains 21,010 committed paths corresponding to the
approved INCLUDE scope.

## Current committed lineage

```text
0144bec0a0ffd425222521c907c3bbb3e6e0143f
→ 9a9a559160759d5c1b940b580de3c548bb568c15
→ 3535f1a158c810aae1ba85a3b1c7d8dfadcec8e3
→ 16e4f8c5095eaad32334d35b5404e01d71853881
→ c5e5a81509ac2ccb053500221a86c4c80cf737f8
→ 2ac8b7fd19a4ebe9d09b83fcc2db528559e956cb
→ edbd72a57ac50dbcd9f19cf3de64c2d36fcaafda
→ a57dc342d67d10d4a3575d5224e9182ff76342b8
→ 04ad9c568406057fc96e816ca1d240a2ad489b0b
→ 2a91b06117450bf60e53cd97905ae9d575cb25dd
```

The 3535, 16e4, and c5e5 commits are intermediate F-01 remediation commits.
The formal freeze points are:

```text
F01 = 2ac8b7fd19a4ebe9d09b83fcc2db528559e956cb
F02 = edbd72a57ac50dbcd9f19cf3de64c2d36fcaafda
F03 = a57dc342d67d10d4a3575d5224e9182ff76342b8
F04 = 04ad9c568406057fc96e816ca1d240a2ad489b0b
F05 = 2a91b06117450bf60e53cd97905ae9d575cb25dd
```

## Reconstruction result

```text
SOURCE_BASELINE_TREE_RECONSTRUCTABLE = PASS
RECEIPT_RECONSTRUCTABLE = PASS
F01_TREE_RECONSTRUCTABLE = PASS
F02_TREE_RECONSTRUCTABLE = PASS
F03_TREE_RECONSTRUCTABLE = PASS
F04_TREE_RECONSTRUCTABLE = PASS
F05_TREE_RECONSTRUCTABLE = PASS
CURRENT_HEAD_TREE_RECONSTRUCTABLE = PASS
CURRENT_HEAD_DESCENDS_FROM_SOURCE_BASELINE = YES
CURRENT_HEAD_DESCENDS_FROM_RECEIPT = YES
CURRENT_TRACKED_SOURCE_DEPENDS_ON_UNCOMMITTED_TRACKED_CHANGES = NO
CURRENT_CANONICAL_SOURCE_ONLY_UNTRACKED_COUNT = 0
```

## External asset boundary

```text
REQUIRED_EXTERNAL_ASSET_COUNT = 9
EXTERNAL_ASSETS_STORED_IN_GIT = NO
EXTERNAL_ASSET_STATIC_BINDING_COMPLETE = YES
EXTERNAL_ASSET_SOURCE_LICENSE_UNKNOWN_COUNT = 9
```

The nine assets comprise one MobileSAM model weight and eight real-image
fixtures. Their external role, digest, and restoration binding are governed
separately. Git source reconstructability is distinct from runtime
environment reproducibility and does not imply that all external assets are
stored in Git. Their source and license provenance is not claimed as known.

## Evidence and source binding

```text
ARTIFACT_SOURCE_BINDING_CONTRACT_EXISTS = YES
CURRENT_FREEZE_SOURCE_BINDING_MODEL_DEFINED = YES
F01_SOURCE_BINDING_PRESENT = YES
F02_SOURCE_BINDING_PRESENT = YES
F03_SOURCE_BINDING_PRESENT = YES
F04_SOURCE_BINDING_PRESENT = YES
F05_SOURCE_BINDING_PRESENT = YES
LEGACY_ARTIFACTS_ALL_RETROACTIVELY_BOUND = NOT_REQUIRED
```

Historical unbound evidence remains historical/legacy evidence. It gains no
new authority merely because the repository was rebaselined.

## Record versus repository reality

- Manifest: descriptive governance record.
- Receipt: descriptive version record.
- Notion and documents: descriptive engineering records.
- Git commit/tree/object: repository source reality.

The authority direction is:

```text
Git object/tree reality
→ manifest / receipt / closure documentation describes it
```

It is not:

```text
documentation says a commit exists
→ reconstructability is proven
```

```text
MANIFEST_RECORD_EQUALS_GIT_REALITY = PASS
RECEIPT_RECORD_EQUALS_GIT_REALITY = PASS
FREEZE_RECORD_EQUALS_GIT_REALITY = PASS
```

## Function and authority boundary

| Function | Canonical responsibility |
|---|---|
| Git | Committed object history, tree reconstruction, ancestry, and version identity |
| Source Baseline Governance | Canonical source-scope classification and baseline identity |
| Artifact Source Binding | Evidence/artifact to source identity binding |
| Freeze Routine | GO scope to explicit immutable commit scope |
| External Asset Governance | Required non-Git asset preservation and binding |
| Docs / Notion | Descriptive engineering ledger only |
| Remote | Distribution and publication only |

Within F-06 scope:

```text
FUNCTION_OVERLOAD = 0
AUTHORITATIVE_CAPABILITY_OVERLAP = 0
MULTIPLE_FINAL_AUTHORITY = 0
```

No Repository Authority Manager is required.

## Remote boundary

```text
LOCAL_GIT_RECONSTRUCTABILITY = PASS
REMOTE_RECONSTRUCTABILITY_THROUGH_COMMIT = 9a9a559160759d5c1b940b580de3c548bb568c15
CURRENT_HEAD_REMOTE_PUBLICATION = NOT_CONFIRMED
REMOTE_PUBLICATION_REQUIRED_FOR_F06_LOCAL_SOURCE_CLOSURE = NO
```

The current HEAD is not claimed as remotely published. F-01 through F-05 are
not claimed as remotely reconstructable. No push was performed.

## P8A adversarial closure

T1 through T15 all passed. The blocked conditions were:

- current HEAD contains the required committed F-01-F05 implementation;
- no staged or unstaged tracked implementation dependency exists;
- no F-01-F05 canonical source exists only as an untracked path;
- source baseline and freeze identities are explicit;
- ancestry and Git trees are reconstructable;
- the historical source hash is correctly scoped;
- external assets are not confused with Git source completeness;
- remote publication is not falsely claimed.

## Closure criteria

```text
C1-C20 = PASS
F06_CLOSURE_CRITERIA_PASS_COUNT = 20/20
F06_CLOSURE_ADJUDICATION = PASS_ALREADY_REMEDIATED_BY_REBASELINE
```

## Remaining caveats

The following remain explicit caveats and are not F-06 blockers:

1. Nine external assets have unknown source/license provenance.
2. Current HEAD remote publication is not confirmed.
3. Historical artifacts are not all retroactively source-bound.
4. Runtime environment reproducibility is not established.
5. Provider, model, camera, and hardware validation is not established.
6. Production Ready is not established.
7. Full Repo GO is not established.
8. `tests/freeze` is not established by F-06.

## Final status

```text
F06_STATUS = CLOSED
F06_TECHNICAL_STATUS = CLOSED
F06_ENGINEERING_STATUS = AWAITING_DOC_ONLY_FREEZE
F06_CLOSURE_TYPE = DOC_ONLY_FREEZE
REPOSITORY_PRODUCTION_SOURCE_CHANGE_COUNT = 0
REPOSITORY_TEST_CHANGE_COUNT = 0
NEW_F06_CLOSURE_DOC_COUNT = 1
REMOTE_PUBLICATION = NOT_CLAIMED
FULL_REPO_GO = NOT_CLAIMED
PRODUCTION_READY = NOT_CLAIMED
RECOMMENDED_NEXT_PHASE = Phase-P8C-Luna-F06-Doc-Only-Engineering-Freeze-v1-001
```

Engineering freeze has not yet occurred.
