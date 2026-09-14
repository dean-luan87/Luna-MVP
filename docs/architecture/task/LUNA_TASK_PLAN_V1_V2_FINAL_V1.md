# Luna task_plan_v1 / v2 / final 正式对象定义（系统规格基线 · 定稿）

> **状态**：本文与 [LUNA_TASK_DOMAIN_CLASSIFICATION_V1.md](./LUNA_TASK_DOMAIN_CLASSIFICATION_V1.md)、[LUNA_INTERNAL_TASK_INSTRUCTION_MAP_V1.md](./LUNA_INTERNAL_TASK_INSTRUCTION_MAP_V1.md) 共同构成 **接模型前的系统规格基线**。  
> **总序**：[LUNA_TASK_PROTOCOL_AND_MODEL_GATE_V1.md](./LUNA_TASK_PROTOCOL_AND_MODEL_GATE_V1.md)。  
> **工程**：`TaskPlan` / `TaskPlanItem` / `PlanDelta`（`shared/schemas/task_plan.py`）。

---

## 3.1 task_plan_v1

**定义**：基于当前输入语义 **直接拆出** 的原始任务计划。

**反映**：

- 用户 **表达顺序**  
- 语义上的主任务与次任务  
- **尚未** 做历史/环境/图书馆增强  

**建议结构**：

```json
{
  "plan_id": "plan_v1_001",
  "plan_version": "v1",
  "source": "raw_user_intent",
  "primary_domain": "navigation",
  "secondary_domains": ["observation"],
  "tasks": [],
  "execution_order": [],
  "constraints": [],
  "clarification_needed": false,
  "confirmation_needed": false,
  "optimization_applied": false,
  "optimization_reason": null,
  "generated_at": "2026-03-30T10:00:00+08:00"
}
```

---

## 3.2 task_plan_v2

**定义**：经过 **知识协同、环境协同、经验协同** 之后生成的 **增强** 任务计划。

**反映**：

- 系统 **建议** 执行顺序  
- 自动补全  
- 历史经验复用  
- 任务优化建议  

**建议结构**：

```json
{
  "plan_id": "plan_v2_001",
  "plan_version": "v2",
  "source": "knowledge_environment_enhanced",
  "base_plan_id": "plan_v1_001",
  "primary_domain": "navigation",
  "secondary_domains": ["observation"],
  "tasks": [],
  "execution_order": [],
  "constraints": [],
  "clarification_needed": false,
  "confirmation_needed": true,
  "optimization_applied": true,
  "optimization_reason": "store_is_on_route_and_more_time_efficient",
  "generated_at": "2026-03-30T10:00:01+08:00"
}
```

**核心新增字段**：`base_plan_id`、`optimization_applied`、`optimization_reason`。

---

## 3.3 task_plan_final

**定义**：经过用户 **确认/修正** 后，**最终进入执行链** 的任务计划。

**反映**：

- 最终执行顺序  
- 最终保留/删除/改写的任务  
- 是否接受系统优化  

**建议结构**：

```json
{
  "plan_id": "plan_final_001",
  "plan_version": "final",
  "source": "user_confirmed",
  "base_plan_id": "plan_v2_001",
  "primary_domain": "navigation",
  "secondary_domains": ["observation"],
  "tasks": [],
  "execution_order": [],
  "constraints": [],
  "clarification_needed": false,
  "confirmation_needed": false,
  "optimization_applied": true,
  "optimization_reason": "user_accepted_reordered_plan",
  "generated_at": "2026-03-30T10:00:05+08:00"
}
```

---

## 3.4 统一任务对象结构（`tasks[]`）

三个 plan 中的 **`tasks[]` 必须统一** 为下列结构（工程侧 `TaskPlanItem`）：

```json
{
  "task_id": "task_001",
  "task_domain": "navigation",
  "task_action": "start_navigation",
  "system_mapping_candidate": "navigation.start",
  "target": {
    "type": "poi_category",
    "value": "mall"
  },
  "constraints": [],
  "priority": "primary",
  "dependency": null,
  "is_temporary": false,
  "requires_confirmation": false,
  "confidence": 0.92
}
```

| 字段 | 说明 |
|------|------|
| `task_domain` | 对齐任务域分类 |
| `task_action` | 人读友好动作名 |
| `system_mapping_candidate` | 对齐内部指令映射表 |
| `target` | 结构化目标 |
| `constraints` | 约束 |
| `priority` | 如 `primary` / `secondary` / `opportunistic` |
| `dependency` | 前置 `task_id` |
| `is_temporary` | 是否临时插入 |
| `requires_confirmation` | 本步是否需确认 |
| `confidence` | 置信度 |

---

## 3.5 plan_delta（建议保留）

用于观察 **V1→V2**、**V2→Final** 的差异，供白盒 / 图书馆 / 蜂巢使用。

```json
{
  "plan_delta": {
    "from_plan_id": "plan_v1_001",
    "to_plan_id": "plan_v2_001",
    "changes": [
      {
        "change_type": "reorder",
        "task_id": "task_002",
        "details": "moved before task_001"
      },
      {
        "change_type": "field_autofill",
        "task_id": "task_001",
        "details": "destination candidate filled from history"
      }
    ]
  }
}
```

工程侧：`PlanDelta` + `PlanChange`（`wrap_plan_delta_nested`）。

---

## 四、系统级硬原则

| 原则 | 内容 |
|------|------|
| **1** | **V1** 永远保留用户 **原始表达顺序**。 |
| **2** | **V2** 可以优化，但 **不能偷偷执行**。 |
| **3** | **Final** 才是 **唯一执行版本**。 |
| **4** | 知识协同、历史补全、任务优化都必须 **可追踪**（`plan_delta`、`optimization_reason`）。 |
| **5** | 历史和环境只能 **增强** 当前任务，**不能覆盖** 用户明确输入。 |

---

## 五、总纲与语音长输入主线衔接

**总纲一句话**：长语音/长文本先生成 **task_plan_v1**，再结合记忆、环境、经验生成 **task_plan_v2**，最后在用户确认或修正后形成 **task_plan_final**；系统智能核心在 **V1→V2 的增强与优化**，不在越权直接执行。

**下一阶段（不接完整模型能力，先接骨架）**：

1. 长输入进入拆解入口  
2. 按 **任务域分类表** 做分类（产出 `DomainClassificationResult`）  
3. 按 **内部任务指令映射表** 做映射  
4. 产出 **task_plan_v1**  
5. 预留 **knowledge_collaboration**、**task_optimization**  
6. 再接入 **长语音拆解模型**（仅产出结构化候选）

详见：[TASKCHAIN_MAINLINE_INTEGRATION_ARCHITECTURE.md](../../TASKCHAIN_MAINLINE_INTEGRATION_ARCHITECTURE.md)、语音输入主线文档 `docs/architecture/voice/LUNA_VOICE_INPUT_MAINLINE_V1.md`。

---

## 附录：输入执行链

```
长语音/长文本
  → 任务域分类（primary_domain）
  → 参数与约束抽取
  → task_plan_v1
  → 知识/环境/经验协同
  → task_plan_v2
  → 用户确认/修正
  → task_plan_final
  → TaskChain / Bridge / Core
```
