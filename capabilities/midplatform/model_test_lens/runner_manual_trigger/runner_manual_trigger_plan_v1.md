# Runner Manual Trigger Plan V1

**Phase:** `Phase-P1-Midplatform-Model-Test-Lens-Detection-OCR-Runner-Manual-Trigger-Planning-v1-001`  
**System ID:** `LunaModelTestLensRunnerManualTriggerV1`  
**Status:** Planning only（本阶段不调用 Detection/OCR runner、不跑模型、不写 fact、不改 Visual Expression System）

## 上游（全部 GO）

- Observation Attention Layer Planning + UI Execution  
- Visual Expression System Planning + UI Execution  
- Followup Runner Route Planning  
- Followup Runner Route UI Queue Execution + Post Review（Negative guards 30/30）  
- `browser_runtime_guard_v1.js` 浏览器守卫继承有效

## 三层关系（本阶段钉死）

| 层 | 语义 | 本阶段 |
|----|------|--------|
| `runner_task_candidate` | **可以考虑做什么** — 治理层队列项，recommended route only | 已 GO（UI 队列） |
| `runner_invocation_request` | **准备申请执行什么** — 手动触发前的准入门禁对象 | **本阶段规划终点** |
| `runner_execution` | **真正跑模型** — runner job / model call | **禁止** |

若将 `runner_invocation_request` 与 `runner_execution` 混同，后续 fact admission 将无法治理。

## 核心链路（规划冻结）

```
Segmentation region (region_id, mask, prompt_label_candidate)
        ↓
Observation Attention record
        ↓
followup_model_route_candidate
        ↓
runner_task_candidate (queue_state: candidate | pinned | excluded | …)
        ↓
pinned runner_task_candidate          ← 生成 request 的唯一入口
        ↓
runner_invocation_request             ← 本阶段规划终点
  (admission_status: pending_admission | admitted | rejected)
  (execution_status: not_executed ONLY)
        ↓
runner execution                      ← 未来阶段 only
```

**本阶段终点：** `runner_invocation_request` schema + 手动触发准入门禁 + Detection/OCR 路由边界。  
**本阶段禁止：** runner 执行、模型调用、fact 写入、导航决策、UI 实现、自动触发。

## 核心问题

> 已 **pin** 的 `runner_task_candidate` 什么时候允许转成 `runner_invocation_request`？

### 回答（规划冻结）

1. **唯一入口：** 仅 `queue_state === pinned` 的 `runner_task_candidate` 可生成 request。  
2. **禁止入口：** `excluded`、`blocked_by_policy` 不可生成；`stale_candidate` 需重新确认后才可生成。  
3. **candidate 未 pin：** 不可直接生成 request（须先 pin）。  
4. **P2/P3 manual_only：** 必须 pin 后才可 request（与队列规则一致）。  
5. **路由匹配：** OCR request 仅来自 OCR route；Detection request 仅来自 Detection route。  
6. **禁止 bypass：** UI / API 不得绕过 `runner_task_candidate` 直接构造 request。

## runner_invocation_request 定义

见 `schemas/runner_manual_trigger/runner_invocation_request_schema_v1.json`。

### 关键字段

| 字段 | 说明 |
|------|------|
| `invocation_request_id` | `rir_{runner_type}_{region_id}_{seq}` |
| `source_runner_task_candidate_id` | 溯源 pinned task |
| `source_region_id` | segmentation region |
| `source_attention_record_id` | observation attention |
| `source_followup_model_route_candidate_id` | route candidate ref |
| `requested_runner_type` | `Detection` / `OCR`（本阶段 scope） |
| `requested_by` | `manual_user_trigger` / `developer_test_trigger` |
| `trigger_mode` | `manual_only` |
| `admission_status` | `pending_admission` / `admitted` / `rejected` |
| `execution_status` | **仅允许** `not_executed` |
| `input_payload_ref` | envelope / frame ref（不执行） |
| `region_crop_ref` / `region_geometry_ref` | 空间输入引用 |
| `route_reason` | 透传自 task candidate |
| `trace_chain` | 完整溯源链 |
| `candidate_only` / `not_fact` / `not_executed` / `no_navigation_decision` | 边界标记 |

## 手动触发准入门禁

见 `schemas/runner_manual_trigger/manual_runner_trigger_admission_policy_v1.json`。

### 准入状态机（request 层）

**允许 admission_status：**

- `pending_admission` — 刚生成，待治理复核  
- `admitted` — 通过门禁，仍 **not_executed**  
- `rejected` — 拒绝生成或复核不通过  
- `cancelled` — 用户取消

**禁止 admission_status：** `running`, `executed`, `completed`

**执行状态（execution_status）：**

- 本阶段 **唯一合法值：** `not_executed`

**禁止 execution_status：**

- `running`, `executed`, `completed`, `failed_with_model_output`, `fact_written`, `navigation_decided`

## Detection / OCR 路由边界

见 `schemas/runner_manual_trigger/detection_ocr_manual_trigger_route_policy_v1.json`。

### Detection request 允许来源

- object-like candidate  
- label uncertain (`prompt_label_candidate` 低置信)  
- `correction_boosted`（priority signal only，非 ground truth）  
- `dynamic_candidate` by label — **不得**确认为 dynamic  
- `needs_tracking_review` 可 **建议** Detection，但 **不得替代** Tracking runner

### OCR request 允许来源

- `static_candidate`  
- text-likely region（sign / screen / poster / label）  
- `ocr_required === true`  
- human correction「这个文字应该读」（priority signal only）

### 禁止

- OCR 对明显 dynamic-only region 自动触发  
- Detection 对纯 text-only region 强行触发（除非 label uncertain）  
- request 结果直接写 fact  
- request 结果直接进入 navigation  
- request 文案暗示「已执行」

## trace_chain 要求

每个 `runner_invocation_request` 必须包含非空 `trace_chain`：

```json
[
  {"stage": "segmentation_region", "ref": "<region_id>"},
  {"stage": "observation_attention_record", "ref": "<attention_record_id>"},
  {"stage": "followup_model_route_candidate", "ref": "<route_ref>"},
  {"stage": "runner_task_candidate", "ref": "<rtc_id>", "queue_state": "pinned"},
  {"stage": "runner_invocation_request", "ref": "<rir_id>"}
]
```

不得存在 orphan request（缺少任一上游 ref）。

## UI 未来表达（本阶段不实现）

| 元素 | 规划 |
|------|------|
| pinned 队列项 | 可出现「生成检测请求」「生成 OCR 请求」 |
| 点击行为 | 仅生成 `runner_invocation_request` candidate |
| 展示区 | 「待准入请求」区 |
| 禁止文案 | 「开始检测」「开始 OCR」「立即执行」 |
| 建议文案 | `生成检测请求` / `生成 OCR 请求` / `送入准入检查` / `暂不执行` |
| 主图 | 不变；request 不在 canvas 画执行态 |

### 浏览器运行守卫继承

未来 UI 实现须：

- `app.js` 使用 `window.xxx`，禁止裸 `global`  
- 继续加载 `browser_runtime_guard_v1.js`  
- 不得在 request 生成路径引入 Node-only 全局对象

## 与 Followup Runner Route Queue 的关系

| Queue state | 可生成 request |
|-------------|----------------|
| `pinned` | ✅ |
| `candidate` | ❌ 须先 pin |
| `excluded` | ❌ |
| `stale_candidate` | ❌ 须重新确认 |
| `blocked_by_policy` | ❌ |

Pin / exclude **不改变** `priority_level`；生成 request **不触发** runner。

## 推荐下一阶段

`Phase-P1-Midplatform-Model-Test-Lens-Detection-OCR-Runner-Manual-Trigger-UI-Execution-v1-001`  
（UI：pinned 项 → 生成 request → 待准入区；仍不执行 runner）
