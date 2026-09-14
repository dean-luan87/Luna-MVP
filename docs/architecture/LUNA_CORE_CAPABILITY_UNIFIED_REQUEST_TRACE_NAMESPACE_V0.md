# Phase-CoreCapability-TRW-Unified-001
# YOLO / OCR / Voice Unified RequestTrace Stage Namespace Definition v0

**阶段定位**：本阶段只定义三条核心能力线在统一 RequestTrace 视图中的 stage namespace 与映射原则；不实现 runtime、不做 adapter、不重构目录。  
**核心目标**：先把“同一条请求链里怎么观察”定义清楚，再谈实现与架构调整。

---

## 1. 统一 namespace（v0）

**顶层标识**：`core_capability_request_trace_v0`

**一级分组（建议）**：

1. `perception.yolo`
2. `perception.ocr`
3. `output.voice`
4. `governance.midplatform`（占位）
5. `governance.scene_delta`（占位）
6. `world.context_evidence`（占位）
7. `world.write_readiness`（占位）

> 本阶段重点：前三个（YOLO/OCR/Voice）。其余为“后续治理阶段的位置占位”，不实现。

---

## 2. 统一命名规则（stage_name）

统一 RequestTrace stage 命名空间采用：

`request_trace.stage.<group>.<subgroup>.<stage>`

例如：

- `request_trace.stage.perception.yolo.detector_invocation`
- `request_trace.stage.perception.ocr.raw_text_result`
- `request_trace.stage.output.voice.speech_gate`

---

## 3. 统一字段最小要求（跨线）

所有 stage 至少应可提供（缺失必须显式记录 missing，不得伪造）：

- `request_id`（最小统一主键）
- `trace_id`（可空，但必须可观测 missing）
- `session_id`（可空，但必须可观测 missing）
- `source_run_id`（离线 run 必须存在）
- `stage_name` / `stage_order`
- `trace_ref` / `replay_ref` / `whitebox_ref`（至少一项存在；映射不得丢失原始 refs）
- `runtime_invoked`（bool；不得伪造为 true）
- `downstream_invocation_count`（int；不得伪造）

---

## 4. 与既有体系的兼容约束

- Voice 已存在 `voice_output_governance_v0` stage namespace；本阶段必须给出兼容映射（见 voice compatibility 文档）。
- YOLO/OCR 当前以 local trace/replay/whitebox 为主；本阶段只定义 stage 与字段口径，不实现 adapter。

---

## 5. MidPlatform / SceneDelta / World / WriteReadiness 后续 stage 位置（占位，只定义不实现）

> 说明：这些 stage 位置用于未来把 OCR→MidPlatform→SceneDelta→WorldContextEvidence→WriteReadiness 的治理链纳入统一请求链视图。  
> 本阶段只占位命名，不实现 adapter，不改变任何既有闭包状态。

### 5.1 MidPlatform（governance.midplatform）

- `request_trace.stage.governance.midplatform.evidence_input`
- `request_trace.stage.governance.midplatform.filtering`
- `request_trace.stage.governance.midplatform.delta_route`
- `request_trace.stage.governance.midplatform.candidate_output`

### 5.2 SceneDelta（governance.scene_delta）

- `request_trace.stage.governance.scene_delta.anchor`
- `request_trace.stage.governance.scene_delta.signature_compare`
- `request_trace.stage.governance.scene_delta.delta_decision`
- `request_trace.stage.governance.scene_delta.compression`

### 5.3 WorldContextEvidence（world.context_evidence）

- `request_trace.stage.world.context_evidence.candidate_build`
- `request_trace.stage.world.context_evidence.anchor_alignment`
- `request_trace.stage.world.context_evidence.trust_lifecycle_policy`

### 5.4 WriteReadiness（world.write_readiness）

- `request_trace.stage.world.write_readiness.check`
- `request_trace.stage.world.write_readiness.contamination_guard`
- `request_trace.stage.world.write_readiness.provisional_policy`

---

## 5. 边界声明（必须）

- 本阶段只做定义：不实现 runtime、不接真实播放、不执行真实 TTS、不接地图/GPS/点云、不进入 SceneTask/Fusion/Output、不写真实世界模型。

