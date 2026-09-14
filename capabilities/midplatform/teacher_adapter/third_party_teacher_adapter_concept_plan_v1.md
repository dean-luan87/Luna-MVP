# Third-Party Teacher Adapter — Concept Planning v1

**Phase:** Phase-P1-Midplatform-Third-Party-Teacher-Adapter-Planning-v1-001  
**Layer:** Teacher Adapter（L1/L2 与 L3/L4 之间的顾问层）  
**Status:** Planning only — no real API calls, no training, no fact write

## 1. 核心定位

第三方模型（Gemini / Qwen-VL / GPT Vision / InternVL 等）是 Luna 的**顾问 / 老师 / 能力插件**，不是 Luna 的决策者。

### 禁止架构

```
Image → Gemini → Answer → Luna 执行
```

### 目标架构

```
L1 Situation Understanding
        ↓
L2 Agent Planning
        ↓
需要外部能力（不确定问题）
        ↓
Teacher Adapter（准入 + 路由）
        ↓
teacher_evidence_candidate
        ↓
Luna Review（policy / human）
        ↓
Case Library / Plan Improvement（候选）
```

**工具**解决「确定能力」；**Teacher**解决「不确定问题」。

## 2. Luna 分层中的位置

```
L0 Survival Constitution
L1 Situation Understanding
L2 Agent Planning
    ├── Tool OS Handoff → L3 → L4 Tools（OCR / SAM / SLAM / …）
    └── Teacher Adapter → External VLM Teachers（Gemini / Qwen / GPT / InternVL）
```

Teacher Adapter 与 Tool OS **并列**，不替代 L2 的 `selected_plan_candidate` 所有权。

## 3. Teacher 三种角色

| 角色 | 作用 | 输出类型 |
|------|------|----------|
| Perception Teacher | 帮助理解复杂/未知场景 | `scene_hypothesis_candidate` |
| Planning Teacher | 提供备选计划建议 | `alternative_plan_candidate` |
| Learning Teacher | 产出可审阅学习候选 | `learning_candidate`（经 network_assisted_learning） |

### Perception Teacher

输入：`unknown_scene` + high uncertainty + missing information  
输出示例：

```json
{
  "scene_hypothesis_candidates": [
    {"scene_type": "shopfront_sign", "confidence": 0.42},
    {"scene_type": "subway_platform", "confidence": 0.35}
  ],
  "visual_evidence_candidates": [],
  "uncertainty": 0.35,
  "candidate_only": true,
  "not_fact": true
}
```

不是「这是商店」，而是「候选场景假设」。

### Planning Teacher

可帮助 L2 改进计划竞争，输出 `alternative_plan_candidate`，**不得覆盖** `selected_plan_candidate`。  
最终选择权属于 Agent Planning。

### Learning Teacher

```
Teacher output → Learning Candidate → Policy Review → Case Library → Future Training Dataset
```

禁止：`Teacher output → 直接训练 Luna`

## 4. 统一接口

Luna 不直接认识 Gemini。统一入口：

```python
request_teacher_assistance(
    task_type,
    input_evidence,
    required_output_type,
    policy_context,
)
```

输出统一为 `teacher_evidence_candidate`（含 admission 决策与 provider 路由）。

## 5. Teacher Admission Policy

Teacher 不是无限调用。

| 允许 | 不允许 |
|------|--------|
| `unknown_scene` + high uncertainty + missing info → VLM advisor | `shopfront_sign` + `read_text` + OCR available → 禁止 Gemini 看文字 |
| OCR 不可用时的 VLM fallback advisor | Teacher 输出直接写 fact |
| Planning 冲突时 alternative_plan_candidate | Teacher 覆盖 selected_plan |
| Learning 路径 pending_policy_review | Teacher 直接改 L1 scene owner |

## 6. 与既有模块关系

| 模块 | 关系 |
|------|------|
| L1 Situation Understanding | Teacher 可提供 scene hypothesis，不直接覆盖 scene owner |
| L2 Agent Planning | Teacher 可提供 alternative plan，不覆盖 selected plan |
| L3 Tool OS | Teacher 与 Tool OS 并列；Teacher 不触发 runner |
| network_assisted_learning | Learning Teacher 输出进入 learning_candidate 管线 |
| Perception Tool Layer | 专业工具（OCR 等）优先于通用 VLM |

## 7. Provider 目录（规划）

```
teacher_adapter/
├── providers/
│   ├── gemini_adapter_v1.py
│   ├── qwen_vl_adapter_v1.py
│   ├── gpt_vision_adapter_v1.py
│   └── internvl_adapter_v1.py
├── schemas/
├── governance/
└── evaluation/   # 后续 dry-run / admission 评测
```

本阶段 provider 均为 **deterministic stub**，不发起真实网络请求。

## 8. 本阶段禁止

- 真实 Gemini / Qwen / GPT / InternVL API 调用
- Teacher 输出直接写 fact / 直接改 L1 scene / 直接改 L2 selected plan
- Teacher 触发 runner / Tool OS execution
- 直接训练 Luna 权重
- 修改既有 runner / observation schema

## 9. 下一阶段建议

**优先：** Phase-P1-Midplatform-Third-Party-Teacher-Adapter-DryRun-v1-001  
将 Teacher Adapter 接入 L1→L2 dry-run 链，验证 admission + evidence candidate + policy reject。
