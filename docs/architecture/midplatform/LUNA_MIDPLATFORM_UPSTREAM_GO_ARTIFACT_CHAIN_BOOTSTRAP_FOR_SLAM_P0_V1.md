# Luna Midplatform — Upstream GO Artifact Chain Bootstrap for SLAM P0 v1

## Scope

Controlled upstream GO artifact bootstrap for SLAM P0 Task Collaboration Planning. Does **not** add capabilities, protocols, model adapters, World Model Assembly, Scene Graph Smoke IO, Task Reasoning, or action outputs.

## Problem

SLAM P0 revalidation is `REVALIDATION_BLOCKED_BY_UPSTREAM_GAP`. P0 TCP artifacts exist but `verifier=HOLD` because upstream stages are not GO in `_tmp_eval_out/`.

## Strategy

1. Analyze blocked chain from SLAM P0 tail to foundation root
2. Run minimal upstream chain in dependency order from first non-GO stage
3. **Stop immediately** on first HOLD/BLOCKED/FAIL after run+verify
4. If full chain GO, rerun SLAM smoke IO → adapter skeleton → TCP → revalidation
5. Confirm P0 visibility for Scene Graph Decision Review

## Prohibited

- Fake GO artifacts or forced summary mutation
- World Model Assembly
- Scene Graph Smoke IO
- Field Simulation
- Real model download / inference

## Run

```bash
python3 tools/evaluation/midplatform/run_upstream_go_artifact_chain_bootstrap_for_slam_p0_v1.py
python3 tools/evaluation/midplatform/verify_upstream_go_artifact_chain_bootstrap_for_slam_p0_v1.py
```

Output: `_tmp_eval_out/upstream_go_artifact_chain_bootstrap_for_slam_p0_v1_smoke_v0/`
