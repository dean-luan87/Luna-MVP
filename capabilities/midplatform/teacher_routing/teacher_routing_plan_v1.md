# Teacher Routing Layer — Planning v1

**Phase:** Phase-P1-Midplatform-Teacher-Routing-Layer-Planning-v1-001  
**Layer:** Teacher Router（L2.5 与 Teacher Adapter 之间）  
**Status:** Planning only — deterministic routing, no multi-teacher voting

## 1. 核心定位

Luna 不是「几个模型一起投票」，而是：

```
Situation → Task / Missing Information → Teacher Router → Teacher Adapter → Evidence → Validation → Decision
```

**核心问题不是「有几个模型？」，而是「当前问题应该问哪个模型？」**

## 2. 架构位置

```
L1 Situation Understanding
        ↓
L2 Agent Planning
        ↓
L2.5 Decision Validation
        ↓
Teacher Router          ← 本层（教师选择器）
        ↓
Teacher Adapter
        ↓
Teacher Evidence Candidate
        ↓
Teacher Validation
```

## 3. 禁止架构

```
问题 → Qwen → Gemini → GPT → 投票
```

## 4. 两个核心注册表

### Teacher Capability Registry
记录每个 Teacher **会什么 / 不擅长什么**（类似能力注册表）。

### Teacher Routing Policy
根据 Situation + Task + Missing Information 决定路由目标。

## 5. 路由结果类型

| route_type | 说明 |
|------------|------|
| `tool_os` | 专业工具已覆盖，不走 Teacher |
| `teacher_single` | 单个 Teacher |
| `teacher_multi_candidate` | 多 Teacher 候选（规划阶段仅 candidate） |
| `noop` | 不需要 Teacher |

## 6. Smoke Cases

| Case | 场景 | 期望路由 |
|------|------|----------|
| A | 店招 + text + OCR plan | OCR tool，not Qwen |
| B | unknown_scene + high uncertainty | qwen_vl perception |
| C | 复杂商场找餐厅 | qwen_vl + planning teacher candidate |
| D | 精确 OCR 需求 | OCR route，Qwen 不擅长 |

## 7. 边界

- Router **不执行** Teacher / Tool
- Router **不写** fact
- Router **不覆盖** L2 plan / L1 scene
- 输出均为 `routing_candidate` / `candidate_only`

## 8. 下一阶段

`Phase-P1-Midplatform-Multi-Teacher-Validation-Planning-v1-001`
