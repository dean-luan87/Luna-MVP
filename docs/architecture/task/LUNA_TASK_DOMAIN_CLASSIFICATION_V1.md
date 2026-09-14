# Luna 任务域分类表 v1（系统规格基线 · 定稿）

> **状态**：本文与 [LUNA_INTERNAL_TASK_INSTRUCTION_MAP_V1.md](./LUNA_INTERNAL_TASK_INSTRUCTION_MAP_V1.md)、[LUNA_TASK_PLAN_V1_V2_FINAL_V1.md](./LUNA_TASK_PLAN_V1_V2_FINAL_V1.md) 共同构成 **接模型前的系统规格基线**。  
> **总序**：[LUNA_TASK_PROTOCOL_AND_MODEL_GATE_V1.md](./LUNA_TASK_PROTOCOL_AND_MODEL_GATE_V1.md)。  
> **工程**：一级域常量 `shared/schemas/task_domain_v1.py`；分类输出 `shared/schemas/domain_classification.py` → `DomainClassificationResult`。

---

## 1.1 设计目标

任务域分类层只做三件事：

1. 判断这段长语音/长文本 **主要属于什么任务域**  
2. 决定 **后续进入哪条处理链**  
3. 为 **内部任务指令映射** 提供边界  

**不负责执行**，也 **不负责最终裁决**。

---

## 1.2 一级任务域（v1 固定 8 个，不再扩）

### A. `navigation`

用于 **地点到达、路线切换、路径问询**。

典型表达：带我去医院、去商场、换一家医院、先去厕所再去医院、还有多久到、现在走到哪了。

---

### B. `observation`

用于 **观察、描述、寻找、扫描**。

典型表达：前面是什么、左边有人吗、帮我找手机、附近有没有便利店、持续帮我看前面。

---

### C. `task_control`

用于 **控制当前任务链生命周期** 或 **插入/切换任务**。

典型表达：暂停任务、继续任务、结束当前任务、切换到找厕所、先做这个再回来。

---

### D. `task_query`

用于 **询问当前任务状态、下一步、进度**，**而不是新增动作**。

典型表达：现在到哪了、当前状态、接下来做什么、还有多远。

---

### E. `device_control`

用于 **设备层面的直接控制**。

典型表达：音量大一点、静音、关机、设备现在怎么样。

---

### F. `confirmation_feedback`

用于 **承接确认、否定、修正、停止当前对话**。

典型表达：是、不是、对、不对、不用了、不是那个医院。

---

### G. `no_task_observation`

用于 **无任务态下的一次性观察问询**。

典型表达：前面是什么、附近有什么、左边是什么店。

与 `observation` 的区别：**默认不生成长期任务链**。

---

### H. `unsupported_or_reject`

用于 **当前阶段不支持、越权、危险、无法执行** 的请求。

典型表达：帮我自动挂号、替我发消息、帮我下单买药、做系统当前未接入的外部动作。

---

## 1.3 分类规则（v1）

| 规则 | 内容 |
|------|------|
| **1** | **只能有一个 `primary_domain`**；允许多个 `secondary_domains`。 |
| **2** | **`task_query` 与 `task_control` 强制分离**：「到哪了」是问询；「暂停任务」是控制。 |
| **3** | **`confirmation_feedback` 优先于新任务**：有待确认上下文时，「是/不是」先解释为确认或修正。 |
| **4** | **`no_task_observation` 默认不升级为长期任务**；除非用户明确要求「持续帮我看」「一直提醒我」「带我过去」等。 |
| **5** | **`unsupported_or_reject` 不是失败桶，而是正式域**：表示当前不能做、不该做、或需要 **明确拒绝**。 |

---

## 1.4 分类结果标准结构

长语音解析后的 **分类部分** 建议统一输出为：

```json
{
  "primary_domain": "navigation",
  "secondary_domains": ["observation"],
  "intent_complexity": "multi_step",
  "can_map_to_system_tasks": true,
  "needs_confirmation": false,
  "needs_clarification": false,
  "should_reject": false,
  "rejection_reason_candidate": null,
  "confidence": 0.89
}
```

`intent_complexity` 建议值：`single_step` | `multi_step` | `ambiguous`（可扩展，须在实现中白名单化）。

工程侧：`DomainClassificationResult`（`shared/schemas/domain_classification.py`）。
