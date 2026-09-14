# Qwen-VL Teacher Adapter — Integration Planning v1

**Phase:** Phase-P1-Midplatform-Single-Teacher-QwenVL-Integration-Planning-v1-001  
**Provider:** `qwen_vl`  
**Role:** `perception_teacher` only  
**Status:** Planning + Deterministic Mock — no real API, no network, no tool execution

## 1. 核心定位

Qwen-VL 是 Luna 的 **Perception Teacher（视觉顾问）**，不是 Luna Brain。

```
L1 Situation Understanding
        ↓
L2 Agent Planning
        ↓
L2.5 Decision Validation
        ↓
Teacher Adapter
        ↓
Qwen-VL Teacher Evidence Candidate
        ↓
Teacher Validation Review (luna_teacher_validation_processor)
        ↓
Case Library / Future Learning
```

### 禁止架构

```
Image → Qwen-VL → Answer → Luna 执行
Qwen-VL → Scene Owner
Qwen-VL → Plan Owner
Qwen-VL → Fact
```

### 目标架构

```
Plan → Qwen-VL Challenge → teacher_evidence_candidate → Validation → accept/reject/uncertain
```

Teacher **不在** Agent Planning 上方。

## 2. Qwen-VL 职责边界

### 只负责

| 输出类型 | 说明 |
|----------|------|
| `scene_hypothesis_candidate` | 场景理解候选 |
| `visual_attention_candidate` | 视觉注意力/区域候选 |
| `task_clue_candidate` | 任务线索候选 |

### 不负责

- 决策
- 规划
- 调度工具
- 修改 Scene（L1 owner）
- 修改 Plan（L2 owner）
- 写 Fact
- 触发 Runner

## 3. 输入边界

Teacher 输入必须来自 **Luna Evidence Layer**：

| 允许 | 禁止 |
|------|------|
| `image_ref` | internal state |
| `observation_candidate` | fact database |
| `situation_candidate` | private memory |
| `plan_candidate` | policy hidden rules |
| `missing_information` | |

## 4. 输出 Schema

统一输出 `teacher_evidence_candidate`（**不是** `teacher_result` / `teacher_fact` / `teacher_decision`）。

必填元数据：

- `teacher_provider: qwen_vl`
- `teacher_role: perception_teacher`
- `candidate_only: true`
- `not_fact: true`
- `confidence_candidate`
- `supporting_reason`
- `uncertainty`
- `trace_refs`

## 5. Teacher Validation 接入

复用 `luna_teacher_validation_processor.review_teacher_evidence()`，验证：

1. 是否支持当前 L1 Situation
2. 是否符合 Constitution / Policy
3. 是否试图覆盖 Luna Plan 所有权
4. 是否存在 hallucination risk（unsupported claim）
5. 是否需要 human review

## 6. Smoke Cases（Planning）

| Case | 场景 | 期望 |
|------|------|------|
| A | 店招 job_564f1aa93983 + OCR plan + Qwen `possible_text_region` | `accepted_as_evidence`，plan 不变 |
| B | 店招 + Qwen 建议 SLAM | `rejected_by_policy`（tool mismatch） |
| C | unknown_scene + Qwen scene hypothesis | `accepted_as_evidence`，不覆盖 L1 |
| D | Qwen "This is Starbucks" 无 OCR 证据 | `rejected_by_policy`（unsupported_claim） |
| E | L2 navigate + Qwen OCR 线索 | `accepted_as_evidence`，plan 不变 |

## 7. 治理规则

见 `governance/qwen_vl_teacher_governance_policy_v1.json`：

- `qwen_not_scene_owner`
- `qwen_not_plan_owner`
- `qwen_not_fact_source`
- `qwen_not_execution_controller`
- `evidence_only_output`
- `validation_required`
- `trace_required`
- `uncertainty_required`

## 8. 本阶段限制

- 不调用真实 Qwen API
- 不联网
- 不执行 Tool
- 不修改 L1 Situation Owner
- 不修改 L2 Agent Plan
- 不触发 Runner
- 不写 Fact
- 不训练模型

## 9. 下一阶段

`Phase-P1-Midplatform-Single-Teacher-QwenVL-Integration-DryRun-v1-001` — 全链路 DryRun（L1→L2→L2.5→Qwen→Validation）。
