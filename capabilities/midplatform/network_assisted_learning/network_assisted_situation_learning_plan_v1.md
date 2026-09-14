# Network-Assisted Situation Learning Plan V1

**Phase:** `Phase-P1-Midplatform-Network-Assisted-Situation-Learning-Planning-v1-001`  
**System ID:** `LunaMidplatformNetworkAssistedSituationLearningPlanningV1`  
**Status:** Planning only — no real network, no real teacher models, no training

## 定位

服务 **Situation Understanding Layer**，为 Luna 转向认知系统建立外部学习治理通道：

```
Network / Teacher / Human Correction / Test Trace
  → Learning Candidate
  → Policy Review
  → Situation Case Library
  → Training Dataset Candidate
  → Future Luna Situation Understanding Model
```

**核心原则：三方模型可以教 Luna，但不能直接改 Luna。**

## 为什么不能直接联网训练

1. 网络数据版权、隐私、可信度不可控  
2. Teacher 输出可能违反 Luna 核心规则（如文字任务默认 SLAM）  
3. 无 provenance / review 的样本会污染 Situation Understanding  
4. 直接训练会绕过 `candidate_only` / `not_fact` / admission 治理链  

## 为什么三方模型只能是 Teacher / Advisor

- Teacher 输出 = `teacher_model_label_candidate`，不是 fact  
- 不得直接进入 `training_dataset` final  
- 不得修改 Luna 模型权重  
- 不得覆盖 Luna policy  
- 必须经过 `policy_review` + 可选 `human_review`  

## 三层关系

| 层 | 对象 | 角色 |
|----|------|------|
| 学习输入 | `situation_learning_candidate` | 外部信号归一化后的待审候选 |
| 案例库 | `situation_case_record` | 通过 review 的 Situation 参考案例（非 fact） |
| 训练候选 | `situation_training_dataset_candidate` | 未来模型训练素材（pending human approval） |

## 来源可信度

| 来源 | trust_tier 典型 | 用途 |
|------|-----------------|------|
| internal_policy / test_trace | high–medium | regression case、规则补强 |
| human_correction | medium–high | 任务/场景纠正信号 |
| teacher_model (stub) | medium | scene/task/tool hints |
| web_reference | low–unknown | 仅 reference / clue，不 auto train |
| synthetic_case | medium | 规划与 smoke |

## 如何进入 Situation Understanding Model

本阶段止于 `situation_training_dataset_candidate`。  
未来阶段：human-approved dataset → Luna Situation Model training（独立 phase）。

## 与 Agent Planning / Tool OS / Runner 边界

| 层 | 本阶段关系 |
|----|-----------|
| Agent Planning | 不消费 learning candidate 做决策 |
| Tool OS | learning candidate 不得安装/下载工具 |
| Runner | learning candidate 不得触发 runner |
| Fact Admission | learning candidate 不得写 fact |

## 上游 GO

- Perception Tool Layer Freeze GO  
- Scene-Task Model Activation Execution GO  

## Smoke Cases（6）

| Case | 输入 | 预期 |
|------|------|------|
| A Teacher 店招 | OCR activate, SLAM noop | accept_as_case_candidate |
| B Teacher 错误 SLAM | text + SLAM | reject / unsafe_rule |
| C Web reference | 门头特征 | pending_policy_review, 不 auto train |
| D Human correction | 应读文字 | learning candidate + case candidate |
| E Test trace | job_564f1aa93983 | regression case, 不改 runner |
| F Dataset | accepted cases | pending_human_approval |

## 本阶段禁止

- 真实联网  
- 调用 Gemini / GPT / Qwen / Claude 等真实 teacher  
- 下载模型 / 训练模型  
- 修改 runner / MobileSAM / OCR 链路  
- 写 fact / 自动安装工具  
- teacher 输出直接覆盖 Luna policy  

## 下一阶段建议

- `Phase-P1-Midplatform-Luna-Situation-Understanding-Model-Planning-v1-001`  
- `Phase-P1-Midplatform-Third-Party-Teacher-Model-Adapter-Planning-v1-001`  
