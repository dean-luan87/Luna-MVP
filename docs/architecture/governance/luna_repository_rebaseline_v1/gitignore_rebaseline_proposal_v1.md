# .gitignore Rebaseline Proposal / Applied Policy v1

Status: scoped worktree edit only; not staged or committed.
Canonical root: /Users/luanlei/Desktop/Luna-Core. No local/global excludes, credentials or remote settings were modified.

| Previous rule | Problem / false positive | Proposed/applied rule | Expected effect |
|---|---|---|---|
| out*.json | outcome_evaluation_candidate_schema_v1.json hidden | Remove basename blacklist; explicit output roots | Outcome schemas remain visible |
| freeze*.json | freeze_policy_v1.json hidden | Remove; /tests/freeze_ci_out.json only for known output | Policy preserved |
| traces/, debug/, snapshots/, reports/ | Nested tests/tools/fixtures hidden | Root-anchored generated paths | tests/traces and fixture snapshots retained |
| *.jsonl | fixtures/contracts and sample traces hidden | Remove; known runtime log directories excluded | JSONL source is reviewed by role |
| *.log, *.trace | Legitimate fixture inputs can be hidden | Remove global extensions; explicit generated dirs | No extension-as-source-authority |
| _eval_out/, _tmp_eval_out/ | Broad relative names | /_eval_out/, /_tmp_eval_out/, /_tmp_eval_inputs/ | Root output/input archive boundary |
| Missing job/output roots | Local machine jobs could be staged | Exact local_runner_bridge/jobs/job_*.json and data/voice/scenario_output | Source sibling modules retained |
| models/** | Model manifests/README can be hidden by parent exclusion | Remove directory blacklist; binary suffix safety net | Declarations visible; weights excluded |
| *.pt, *.bin, media patterns | Valid tiny approved fixture could be hidden | Keep weight/video suffix guard; exact approved exceptions only later | No bulk media admission |
| .env only | .env.local etc exposed | .env and .env.*; exceptions .env.example/.env.template | Templates visible, secrets private |
| .cursor/, .vscode/ | Unanchored and mixed local rules | /.cursor/, /.vscode/; content reviewed separately | No machine-state source admission |
| Global build/cache names | May hide similarly named code directories | Root build products; recursive true caches only | No blanket source-directory ban |

Under-ignore closures also include /evaluation_archive/, /OUT/, root external symlink paths, Luna_Badge_MVP/logs and both historical badge test log trees.
Ignore means do not stage by default; it never means delete.
OUT remains REVIEW_REQUIRED in disposition even though it is ignored.

## Static observations

The four previously misignored paths were checked with git check-ignore --no-index and have no excluding match after the edit:

- docs/architecture/luna_a_route_result_comparison_outcome_evaluation_architecture_planning_v1/outcome_evaluation_candidate_schema_v1.json
- docs/architecture/luna_brain_b5_real_evidence_cognitive_loop_golden_baseline_planning_v1/freeze_policy_v1.json
- tests/traces/test_baseline_check.py
- docs/architecture/voice/fixtures/min_trace_samples.jsonl

capabilities/voice/output/audio_worker_v1.py remains source: output is not globally blacklisted.
.env.local is excluded; .env.example matches the explicit allow exception (a verbose check-ignore line beginning ! is not an exclusion).
Known generated roots and job records match intended exclusions.

## Local exclude overlay

.git/info/exclude contains logs/ and two voice model-tree performance exclusions.
Do not copy that machine-local metadata into baseline.
The confirmed source file backend_bridge/logs/README.md has a narrowly scoped parent/file exception in root .gitignore.
Other logs remain excluded by explicit root/nested generated rules. No !docs/** or !capabilities/** is used.

ignored_before reflects the pre-edit effective untracked snapshot; tracked paths are reconstructed from captured pre-edit rules plus the known local overlay.
The models/yolo/README.md parent-exclusion edge is preserved from the actual pre-edit Git result, not approximated by the rule reconstruction.
ignored_after_proposal is measured with git check-ignore --no-index, so already tracked files are also tested.
Staged/index status is not changed by editing ignore rules.

## Limits

Ignore rules are a convenience guard, not the inclusion manifest or a security scanner.
PNG/JPG/WebP, audio, archived docs and machine-path configurations still require disposition review.
Do not globally whitelist source roots or force-add ignored source without an exact-path exception review.
All later global/local ignore environment changes require reinspection.
