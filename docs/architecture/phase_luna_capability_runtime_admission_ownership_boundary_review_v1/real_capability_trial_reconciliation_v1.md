# Real Capability Trial Reconciliation

## Current CLI inputs

The existing child Runner supports:

| Argument | Default | Current classification | Target source |
|---|---|---|---|
| `--source` | `/Users/luanlei/Desktop/Luna-Workspace-Min/input_videos/phone_local_batch_001/s3_real_frame_001.jpg` | TEMPORARY_TERMINAL_OWNER | Observation/acquisition context |
| `--model-path` | `/Users/luanlei/Desktop/Luna-Core/vision/detection/yolo/yolo11n.pt` | TEMPORARY_TERMINAL_OWNER | Model Manager governed asset path |
| `--dependency-status` | `PYTHON_DEPENDENCY_UNRESOLVED` | TEMPORARY_TERMINAL_OWNER | System Diagnostics evidence |
| `--declared-checksum` | `None` | TEMPORARY_TERMINAL_OWNER | Model Manifest / Model Governance |
| `--observed-checksum` | `None` | TEMPORARY_TERMINAL_OWNER | Integrity verification evidence |

There is no separate real-execution flag in the inspected child CLI. Admission
is determined from the supplied inputs and the existing model/provider path.

## Contract interpretation

The child is a valid controlled test adapter: it makes missing readiness
explicit and blocks Provider invocation when dependency/checksum/model admission
is unresolved. It should not be treated as the canonical owner of those five
fields. No Provider semantics need to change to make this reconciliation.

## Future direction

```text
terminal-owned test readiness input
  → existing Model/Diagnostics/Integrity evidence adapters
  → existing Capability Admission review
  → unchanged Provider admission and single-invocation path
```

The current trial can later consume an admitted Runtime Admission candidate
without changing the YOLO invocation limit or `REQUEST_MORE_EVIDENCE` behavior.

