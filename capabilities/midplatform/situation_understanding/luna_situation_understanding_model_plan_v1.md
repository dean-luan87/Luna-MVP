# Luna Situation Understanding Model v1 — Planning

**Phase:** Phase-P1-Midplatform-Luna-Situation-Understanding-Model-Planning-v1-001  
**Layer:** L1 Situation Understanding  
**Status:** Planning only — no training, no real models, no runner mutation

## 1. 为什么先建 Situation Understanding

Luna 正在从「工具堆叠」转向分层认知架构。若直接接入更多 OCR、SAM、VLM、teacher 模型，底层工具输出会反向牵引 scene 判断（例如 runner 报 `unknown_scene` 而证据指向 `shopfront_sign`）。

Situation Understanding 作为 L1，负责在 Agent Planning 之前回答：

- 我在哪？
- 周围是什么？
- 当前环境与我有什么关系？
- 我现在可能要做什么？
- 我缺什么信息？
- 下一步可能需要哪些能力或工具？

**核心原则：Runner 可以提供 evidence，但不能拥有 scene。**

## 2. Luna 分层架构

```
L0 Survival Constitution     — 生存规则、安全边界
L1 Situation Understanding   — 现状/处境理解（本阶段）
L2 Agent Planning            — 基于处境的目标规划
L3 Tool Operating System     — 工具发现、权限、runner、fact admission
L4 Perception / Action Tools — OCR、SAM、Detection、SLAM、VLM 等
```

本阶段仅规划 L1。

## 3. 边界定义

### 3.1 与 Agent Planning 的边界

| Situation Understanding | Agent Planning |
|-------------------------|----------------|
| 输出 `situation_understanding_candidate` | 输出 action plan / task decomposition |
| 归纳 scene、task clues、missing info | 决定执行顺序与策略 |
| 不直接导航 | 可做导航决策 |

### 3.2 与 Tool OS 的边界

| Situation Understanding | Tool OS |
|-------------------------|---------|
| 输出 `model_need_hints`（likely/optional/not_needed） | 执行工具安装、runner 调度 |
| 不触发 runner | 管理 envelope、sandbox、error |
| 不写 fact | 管理 fact admission |

### 3.3 与 Perception Tool Layer 的边界

| Situation Understanding | Perception Tools |
|-------------------------|------------------|
| 消费 `visual_evidence_candidates` | 产出 region、text、detection 等原始候选 |
| 不调用 OCR/SAM/SLAM | 执行具体感知推理 |
| Perception Layer 已冻结为基线 | 本阶段不修改 |

### 3.4 与 Network-Assisted Learning 的关系

```
Teacher / Web / Human Correction / Test Trace
  → Learning Candidate → Policy Review
  → Situation Case Library
  → (作为 situation_case_refs 输入 L1)
```

- Teacher 输出必须先经 Network-Assisted Learning policy review
- Case library 仅作参考案例，`candidate_only` / `not_fact`
- Teacher 不得直接覆盖 situation output

## 4. 输入 / 输出

**输入：** `situation_understanding_input`  
包含 frame_context、user_goal_candidate、visual_evidence_candidates、situation_case_refs、environment_memory_candidates、human_correction_signals、available_capabilities。

**输出：** `situation_understanding_candidate`  
包含 scene_profile_candidate、survival_context、task_clue_candidates、missing_information_candidates、attention_target_hints、model_need_hints、uncertainty、trace_refs。

所有输出 `candidate_only=true`，`not_fact=true`。

## 5. v1 实现方式

v1 为 **deterministic policy/stub processor**，不是训练模型：

- `luna_situation_understanding_processor_v1.py` 基于 fixture 证据与 policy 规则推理
- 不调用真实 teacher、不联网、不接 runner
- 后续可通过 case library、teacher adapter、真实 job envelope 逐步增强

## 6. 场景策略摘要

| 场景 | likely_needed | not_needed |
|------|---------------|------------|
| shopfront_sign | OCR | SLAM, Tracking, Depth |
| subway_platform | OCR | SLAM (unless navigate) |
| street_crossing | Detection, Depth, Tracking | OCR (unless text evidence) |
| corridor | Depth, SLAM | OCR (unless text evidence) |
| unknown_scene | optional VLM | blanket activate all |

## 7. 本阶段禁止事项

- 真实联网
- 调用真实 teacher（Gemini/GPT/Qwen/Claude）
- 训练模型
- 修改 runner
- 修改 MobileSAM/OCR/Grounding 链路
- 写 fact
- 自动安装工具
- 替代 Agent Planning 或 Tool OS

## 8. 下一阶段建议

**推荐优先：** Phase-P1-Midplatform-Luna-Situation-Understanding-Model-DryRun-v1-001  
将 deterministic Situation Understanding 接入测试板真实 job/envelope，验证 `job_564f1aa93983` 能从 runner `unknown_scene` 修正为 `shopfront_sign` candidate。

**备选：** Phase-P1-Midplatform-Third-Party-Teacher-Model-Adapter-Planning-v1-001
