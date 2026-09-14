# Phase-CoreCapability-TRW-Unified-002
# YOLO / OCR RequestTrace Shadow Adapter v0

**阶段定位**：本阶段只实现离线/shadow adapter，把 YOLO/OCR 既有 local trace/replay/whitebox（或 benchmark/offline policy）输出映射为统一 RequestTrace shadow chain；不接 runtime、不重构目录、不进入真实中台主链。

**核心目标**：让 YOLO/OCR 像 Voice 一样可在同一条请求链视图里被观察（shadow-only）。

---

## 1. 输入与输出

### 1.1 输入（只读）

- **YOLO input root**：例如 `logs/offline_mainline_ef004_20260428_105303`（含 `_yolo_shadow_perception` 产物）
- **OCR input root**：例如 `logs/ocr_offline_source_policy_009_normal_20260429_124053`（含 benchmark summary + trace/replay/whitebox/raw_outputs）

### 1.2 输出（新建 output_root）

运行 `tools/evaluate_core_capability_request_trace_shadow_v0.py` 生成：

- `core_capability_request_trace_shadow_summary.json`
- `yolo_request_trace_chains.json`
- `ocr_request_trace_chains.json`
- `core_capability_stage_mapping_report.json`
- `core_capability_missing_field_report.json`
- `core_capability_shadow_trace.jsonl`
- `core_capability_shadow_replay.jsonl`
- `core_capability_shadow_whitebox.jsonl`
- `evaluation_notes.md`

---

## 2. 统一 stage namespace 约束

- **stage_namespace**：`core_capability_request_trace_v0`
- **stage_name**：继承 Phase-CoreCapability-TRW-Unified-001 的统一命名规则：
  `request_trace.stage.<group>.<subgroup>.<stage>`

---

## 3. 统一 ID 与缺失策略（不得伪造）

- `request_id`：
  - 若输入 root 中存在 request_id：继承（`request_id_origin="inherited"`）
  - 否则生成 deterministic shadow request id：`shadow_req_<source_run_id>_<frame_id_or_sample_id>`（`request_id_origin="deterministic_shadow"`）
- `trace_id` / `session_id`：**不得伪造**。缺失则：
  - `trace_id=null`
  - `session_id=null`
  - `missing_fields` 包含 `trace_id`、`session_id`
- `source_run_id`：离线 run 必须存在；可由 input root basename 派生

---

## 4. Local TRW refs 保留策略（不得补假路径）

每个 stage 的 `source_refs` **必须包含键**（值允许为空但必须显式记录）：

- `trace_ref`
- `replay_ref`
- `whitebox_ref`
- `original_summary_ref`
- `source_root`

若某项缺失：
- 在输出的 missing report 中统计
- 不得生成不存在的路径

---

## 5. Hard Audit 不变量（跨线硬约束）

### 5.1 YOLO

- `runtime_invoked=false`
- `downstream_invocation_count=0`
- `navigation_action=null`
- `real_tts_invoked=false`

### 5.2 OCR

- `semantic_interpretation_enabled=false`
- `allows_execute_now=false`
- `downstream_invocation_count=0`
- `navigation_action=null`
- `real_tts_invoked=false`

---

## 6. 明确禁止项（必须）

- 不接 runtime、不修改 YOLO/OCR 已有运行逻辑、不修改 OCR provider 默认策略
- 不接真实播放、不执行真实 TTS
- 不进入 SceneTask/Fusion/Output、不执行导航动作
- 不写真实世界模型、不上传蜂巢、不接推荐系统
- 不接地图/GPS/点云

