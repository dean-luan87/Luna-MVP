# Luna — Scene Delta Write Candidate from Vision v0

**Phase**：`Phase-MidPlatform-Scene-Delta-Write-Candidate-From-Vision-Ingest-Stub-001`  
**前置（须均为 GO）**：

- `Vision-Ingest-to-Product-Bus-ReadOnly-Replay-001`  
- `MidPlatform-Vision-Recognition-Evidence-ReadOnly-Ingest-Candidate-001`  
- `Vision-Recognition-Evidence-ReadOnly-Consumer-001`  

## 目标

从 **Vision recognition 只读 event payload**（及 **`ingest_matrix_ref`** 指向的 ingest 矩阵、replay consumer 视图）生成 **`scene_delta_write_candidate_from_vision_v0`**：

- **`candidate_scope=write_candidate_only`**；**`write_allowed=false`**；**`requires_gate_approval=true`**。  
- **`evidence_items`**：逐条保留 frame / ROI / bbox / stub label / synthetic / `not_fact`；**`evidence_role=observed_visual_candidate`**；**`scene_delta_disposition=scene_delta_candidate_later`**。  
- **`spatial_reference`**：`geometry_source=vision_bbox_in_frame`，`coordinate_space=frame_pixel`。  
- **Gate stub**：`gate_required=true`，`gate_status=not_evaluated`，`gate_reason_codes` 含 vision/stub/无 AI/无导航/无世界事实写入等。  
- **禁止**：不得产出语义解释、导航动作、confirmed fact/object 等载荷键；不得把 stub label 当作现实事实。

## 严禁

不写 **Scene Delta**、不写 **MidPlatform fact**、不写 **WorldModel**、不调用 **AI interpretation**、不调用 **导航决策**、不调用 **真实视觉 provider** / YOLO / Supervision 主线 / VLM / OCR、不做数据库写入、不外连真实 Bus。

## 与 OCR 线的关系

与 **Scene Delta write candidate from OCR** 同构：先 **候选 JSON**，再谈 dry-run verifier / executor trace 等下游。

## 实现与命令

见 `../evaluation/LUNA_EVALUATION_SCENE_DELTA_WRITE_CANDIDATE_FROM_VISION_SMOKE_V0.md`。

## 与上一 phase 的关系

输入来自 **Vision read-only bus replay** 产物（见 [LUNA_MIDPLATFORM_VISION_RECOGNITION_INGEST_READONLY_EVENT_PAYLOAD_V0.md](./LUNA_MIDPLATFORM_VISION_RECOGNITION_INGEST_READONLY_EVENT_PAYLOAD_V0.md)）。

## 建议下一跳

**Phase-MidPlatform-Scene-Delta-Write-Candidate-DryRun-Verifier-From-Vision-001**：对 **`scene_delta_write_candidate_from_vision`** 做 **dry-run**（字段完备性、映射矩阵、风险、no-write audit），见 [LUNA_SCENE_DELTA_WRITE_CANDIDATE_DRYRUN_FROM_VISION_V0.md](./LUNA_SCENE_DELTA_WRITE_CANDIDATE_DRYRUN_FROM_VISION_V0.md) 与 `../evaluation/LUNA_EVALUATION_SCENE_DELTA_WRITE_CANDIDATE_DRYRUN_FROM_VISION_V0.md`。
