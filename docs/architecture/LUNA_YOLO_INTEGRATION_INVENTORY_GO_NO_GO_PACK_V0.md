# LUNA — YOLO Integration Inventory Go/No-Go Pack v0 (Phase-ModelPerception-002A)

## Inputs (documents)
- Inventory:
  - `docs/architecture/LUNA_EXISTING_YOLO_INTEGRATION_INVENTORY_V0.md`
- Adapter mapping:
  - `docs/architecture/LUNA_YOLO_TO_PERCEPTION_SIGNAL_ADAPTER_MAPPING_V0.md`
- Gap register:
  - `docs/architecture/LUNA_YOLO_SHADOW_ADAPTER_GAP_REGISTER_V0.md`

## Decision
### Result
**GO**

### Why GO
- Found existing YOLO-style object detection capability (`YOLOv5Detector`) with clear output fields (bbox/class/conf).
- Found Ultralytics YOLO wrapper usage (yolo11 OCR line), confirming project familiarity with ultralytics interfaces.
- Confirmed YOLO is **not** integrated into the current phone_local PerceptionEval chain under ModelPerception-001 contract (as expected).
- Frozen an explicit YOLO→Perception-001 mapping that:
  - maps detection primarily to `object_stability_signal`
  - limits `spatial_passability_signal` and `risk_field_signal` to candidate-only hints with hard disclaimers
  - declares OCR/dynamic as not_available under detection-only scope
- Produced a gap register covering adapter/trace/replay/disable/fallback/gate integration requirements.
- No runtime modifications; no model invocations; no evaluation chain reruns.

## Go / Conditional-Go / No-Go criteria (frozen for this phase)
### GO
Allow entering the next phase:
- **Phase-ModelPerception-002B — YOLO Shadow Adapter Implementation v0**
because:
- detection capability exists and can be isolated
- adapter mapping and gaps are explicit
- no execute/default-on coupling is required for the adapter

### CONDITIONAL_GO
Not used for this phase conclusion.

### NO_GO
Not applicable; YOLO/object detection capability was found.

## Hard blockers
- `[]`

## Soft follow-ups (implementation-phase considerations)
- Replace `torch.hub.load` with pinned, locally managed weights to avoid uncontrolled downloads.
- If tracking is desired, define a real tracking contract; do not treat simplified `DeepSortTracker` as stable tracking without upgrades.
- Resolve `mock_yolo.py` missing dependency (`core/yolo_detector.py` not_found) or replace mock with contract-aligned fixtures.

## Recommended next phase (do not auto-enter)
- **Phase-ModelPerception-002B — YOLO Shadow Adapter Implementation v0**
  - shadow-only, candidate-only, disable+fallback, replay/whitebox mandatory, SceneContext gates mandatory.

## Explicit boundary re-statement (for audit)
- 默认路径仍未开启
- 未进入 full controlled trial
- 未扩大真实 side effects 面
- 未执行 controlled_live_stream
- 未扩 Option A
- 未执行导航动作
- 未真实播报
- 未新增 YOLO runtime
- 本阶段只做 existing YOLO inventory 与 adapter mapping，不实现

