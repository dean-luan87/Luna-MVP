# Luna Model Manager — Multi-Model Collaboration Plan v1

**Phase:** `Phase-P1-Midplatform-Luna-Model-Manager-Multi-Model-Collaboration-Planning-v1-001`  
**Layer:** Model Manager → Collaboration Engine  
**Mode:** Planning only — 定义多能力编排，非多模型同时推理。

---

## 1. 战略定位

Multi-Provider Registry 已解决：

> 「我要什么能力，应该找谁」（竞争 / Provider Selection）

本阶段解决：

> 「一个任务是否需要多个能力共同完成，以及多个模型如何协作」

**关键区分：**

```
Model Collaboration ≠ Model Competition
```

| Registry（竞争） | Collaboration（协作） |
|------------------|----------------------|
| Qwen vs InternVL vs Gemini | Text Detection + OCR + VLM Context |
| 谁更适合 unknown_scene | 店招识别需要哪些能力组合 |
| provider_selection_candidate | collaboration_plan_candidate |

---

## 2. 认知链

```
Luna Goal
    ↓
Capability Requirement
    ↓
Model Manager
    ↓
Collaboration Planner
    ↓
Multi Capability Collaboration Plan
    ↓
Provider Sequence / Parallel Strategy
    ↓
Evidence Fusion
    ↓
Decision Validation
    ↓
Fact Admission
```

---

## 3. 三种协作模式

### 3.1 Pipeline Collaboration（流水线）— 第一优先级

每个模型负责**自己的能力**，顺序协作。

```
Image → Text Detector → OCR Recognition → VLM Context Check → "几号线方向"
```

店招识别：

```
Text Detection + OCR Recognition + VLM Context Reasoning
```

不是 Qwen VS OCR，而是三个**不同角色**。

### 3.2 Parallel Evidence（并行证据）

未知环境：

```
Qwen-VL:     可能是商场入口
InternVL:    可能是商业建筑
Grounding:   检测到入口结构
```

不是投票 → **evidence set** → Validation。

### 3.3 Challenge Mode（挑战模式）

L2 计划调用 OCR → Validation 发现 uncertainty high → 请求 Teacher Challenge：

```
Qwen: 可能不是店招，而是活动海报
```

只是 challenger，**不改变 L2 计划**。

---

## 4. 明确不做

| 禁止 | 原因 |
|------|------|
| 多模型投票 | 人类也不是三专家投票决定事实 |
| 自动融合答案 | Qwen=A + InternVL=B → 综合，易幻觉 |
| 每张图全跑 Qwen+Gemini+InternVL | 成本不可控 |
| Challenge 覆盖 L2 计划 | 协作层不拥有决策权 |

正确路径：

```
Evidence Fusion → Validation → Candidate
```

---

## 5. Model OS 完整形态

```
Capability Marketplace（Registry）
        +
Collaboration Engine（本阶段）
```

类比 Windows：应用商店安装 APP → 协作系统多个 APP 完成一个任务。

```
Luna Brain
    |
    ├── Situation Understanding (L1)
    ├── Agent Planning (L2)
    ├── Decision Validation (L2.5)
    ├── Model Manager
    |       ├── Registry
    |       ├── Lifecycle
    |       ├── Routing
    |       └── Collaboration  ← 本阶段
    └── Tool OS
```

---

## 6. 模块结构

```
capabilities/midplatform/model_manager/collaboration/
├── multi_model_collaboration_plan_v1.md
├── collaboration_types_v1.py
├── collaboration_planner_v1.py
├── evidence_fusion_processor_v1.py
├── model_conflict_processor_v1.py
├── collaboration_policy_v1.json
└── schemas/
    ├── collaboration_plan_schema.json
    ├── evidence_fusion_schema.json
    └── conflict_schema.json
```

---

## 7. Planning Smoke Cases

| Case | 场景 | 验证 |
|------|------|------|
| A | identify_place 店招 | pipeline plan + fusion_candidate |
| B | unknown_scene | parallel evidence_collection_plan |
| C | Qwen 机场 vs InternVL 商场 | model_conflict_candidate，禁止按分听谁 |
| D | GPU 不足 | collaboration_degradation_candidate，禁止静默降级 |

---

## 8. 下一阶段

`Phase-P1-Midplatform-Luna-Model-Manager-Multi-Model-Collaboration-DryRun-v1-001`
