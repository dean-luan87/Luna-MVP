# Teacher Performance Evaluation — Plan v1

**Phase:** Phase-P1-Midplatform-Teacher-Performance-Evaluation-v1-001  
**Layer:** Teacher Performance Evaluation（Teacher Validation 之后，Case Library 之前）  
**Status:** Evaluation only — 不影响当前决策，不自动更新 usage policy

## 1. 核心定位

评估的不是「Qwen-VL 是否比人强」，而是：

**Qwen-VL 在什么情况下值得被 Luna 请教。**

```
Teacher Evidence Candidate
        ↓
Teacher Validation Review
        ↓
Teacher Performance Evaluation  ← 本层
        ↓
teacher_usage_profile_candidate
usage_policy_update_candidate
        ↓
Case Library（人工/规则审核后）
```

## 2. 禁止架构

```
Qwen 表现好 → 提高 Qwen 权限 → 自动调用
Evaluation → 直接修改 admission → 影响当前 plan
```

## 3. 正确架构

```
Qwen 表现统计
        ↓
evaluation_candidate / usage_policy_update_candidate
        ↓
人工 / 规则审核
        ↓
更新 teacher_usage_policy（未来阶段）
```

**本层输出均为 `candidate_only` / `not_fact`，`does_not_affect_current_decision: true`。**

## 4. 本阶段要回答的问题

| 问题 | 输出 |
|------|------|
| 什么场景应该调用 Qwen？ | `teacher_usage_profile_candidate` |
| Qwen 信息是否有价值？ | `evidence_accept_rate`, `useful_evidence_rate` |
| Qwen 幻觉情况？ | `teacher_reliability_metrics` |
| Cost 管理？ | `teacher_value_score`, `cost`, `latency` |

## 5. 指标

### Performance Metrics
- `evidence_accept_rate`
- `rejection_rate`
- `hallucination_rate`（unsupported_claim + scene_conflict）
- `teacher_noop_correct_rate`
- `cost_estimate`, `latency_ms`

### Reliability Metrics
- `unsupported_claim_rate`
- `scene_conflict_rate`
- `policy_violation_rate`
- `useful_evidence_rate`

### Value Score
```
teacher_value_score = useful_evidence_rate - (hallucination_rate * 0.5) - (cost_normalized * 0.2)
```

## 6. 场景价值画像（首批）

| 场景 | Qwen 推荐用法 | 原因 |
|------|---------------|------|
| shopfront_sign | low | OCR 已覆盖 |
| subway_platform | medium | 中等不确定 |
| unknown_scene | high | 高不确定 |
| complex_environment | high | 需视觉解释 |
| simple_object | low | 专业工具优先 |

## 7. 未来多 Teacher 扩展

统一比较维度（非「谁回答最好」）：

- 谁在什么任务下最有价值
- 谁幻觉少
- 谁成本低
- 谁适合什么 scene

Teacher Pool: Qwen-VL, Gemini Vision, GPT Vision, InternVL, MiniCPM-V

## 8. 下一阶段

`Phase-P1-Midplatform-Multi-Teacher-Validation-Planning-v1-001`
