# Luna Midplatform — Scene Graph / Relation Model Smoke IO Decision Review v1

## Scope

Decision review only. Evaluates whether P4 Scene Graph / Relation remains **deferred** or may proceed to **Smoke IO Inspection**.

Does **not** run Scene Graph / Relation models, download weights, perform Smoke IO, Adapter Skeleton, Task Collaboration Planning, or World Model Assembly.

## Upstream Dependencies (P0–P3 Task Collaboration Planning)

| Priority | Adapter | Required Final Decision |
|----------|---------|-------------------------|
| P0 | slam_spatial_mapping | `MIDPLATFORM_SLAM_SPATIAL_MAPPING_TASK_COLLABORATION_PLANNING_READY_FOR_TRACKING_OPTICAL_FLOW_MODEL_SMOKE_IO_INSPECTION` |
| P1 | tracking_optical_flow | `MIDPLATFORM_TRACKING_OPTICALFLOW_TASK_COLLABORATION_PLANNING_READY_FOR_OCR_TEXT_MODEL_SMOKE_IO_INSPECTION` |
| P2 | ocr_text_model | `MIDPLATFORM_OCR_TEXT_TASK_COLLABORATION_PLANNING_READY_FOR_SEGMENTATION_MASK_MODEL_SMOKE_IO_INSPECTION` |
| P3 | segmentation_grounded_mask | `MIDPLATFORM_SEGMENTATION_MASK_TASK_COLLABORATION_PLANNING_READY_FOR_SCENE_GRAPH_RELATION_MODEL_SMOKE_IO_DECISION_REVIEW` |

## Input Source Review

Reviews seven candidate source groups (object, geometry/depth, enhanced field, SLAM spatial, tracking persistence, text anchor, mask/boundary) and classifies each as `sufficient_for_smoke_io`, `partially_sufficient`, `insufficient`, or `blocked`.

## Decision Options

1. `MIDPLATFORM_SCENE_GRAPH_RELATION_MODEL_REMAINS_DEFERRED` → World Model Assembly Precondition Review
2. `MIDPLATFORM_SCENE_GRAPH_RELATION_MODEL_DECISION_REVIEW_READY_FOR_SCENE_GRAPH_RELATION_MODEL_SMOKE_IO_INSPECTION` → Smoke IO Inspection
3. `MIDPLATFORM_SCENE_GRAPH_RELATION_MODEL_BLOCKED_PENDING_OWNER_DECISION` → Owner hold

## Prohibited

- Scene Graph / Relation model execution
- SceneRelationCandidate / WorldRelationCandidate generation
- World model assembly / WorldModelEntry
- Smoke IO inspection (this phase decides only)

## Run

```bash
python3 tools/evaluation/midplatform/run_scene_graph_relation_model_smoke_io_decision_review_v1.py
python3 tools/evaluation/midplatform/verify_scene_graph_relation_model_smoke_io_decision_review_v1.py
```

Output: `_tmp_eval_out/scene_graph_relation_model_smoke_io_decision_review_v1_smoke_v0/`
