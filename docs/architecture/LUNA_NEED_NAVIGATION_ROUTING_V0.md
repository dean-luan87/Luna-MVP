# Luna — Need-Navigation Routing v0（中台只读分流建议层）

**文件**：`docs/architecture/LUNA_NEED_NAVIGATION_ROUTING_V0.md`  
**性质**：P3-1 最小分流建议层（只输出建议；不切换执行链）  

---

## A. 文档定位（写死）

- 这是中台“是否需要导航”的**最小分流建议层**。
- 当前只输出建议，不做真实切换：
  - 不启动导航
  - 不改变任务执行路径
  - 不直接驱动语音/记忆

---

## B. 为什么需要这一层

- 不是所有任务都需要导航。
- 导航是专项链，不是默认主链。
- 在真正切换前，需要先有一个**可观察、可回归**的建议层，供后续中台消费与治理逐步收束。

---

## C. 最小分流结果集合（只允许三类）

- `navigation_required`
- `navigation_not_required`
- `navigation_uncertain`

---

## D. 当前最小判断依据（极克制）

### D1. 任务侧输入

- 当前任务语境（占位）
- `proposal.task_action`（若存在）
- 当前是否显式为“开始导航/去某处”类意图（以 `task_action` 为主）

### D2. 视角侧输入

- `runtime_context.metadata["vision_consumable_slices_v0"]`（若存在）
- `runtime_context.metadata["vision_interpretation_candidates_v0"]`（若存在）
- 是否出现明确“导航需要”类切片/候选（如未来的 `navigation_need_candidate` 切片类型）

### D3. 明确不作为当前依据的内容（写死）

- 不依赖地图
- 不依赖完整记忆模型
- 不依赖完整环境建模
- 不依赖复杂多轮语义推理

---

## E. 当前最小判断口径（只读建议，不是裁决）

- 若 `proposal.task_action == "start_navigation"` → 倾向 `navigation_required`
- 若任务为明确“任务生命周期控制”（例如 `pause_task/resume_task/end_task/switch_task`）→ 倾向 `navigation_not_required`
- 若信息不足、任务边界不清、缺少显式导航意图 → `navigation_uncertain`

写死：这只是建议层，不是最终裁决。

---

## F. 当前不允许做什么（写死）

- 不允许直接切到导航链
- 不允许直接触发语音播报
- 不允许直接清理旧任务
- 不允许直接写入主链事实
- 不允许替代中台后续真正分流裁决

---

## G. 当前最小输出建议（建议位置）

建议写入：
- `result.metadata["need_navigation_routing_v0"]`

最小结构：

```json
{
  "routing_decision": "navigation_required",
  "routing_scope": "need_navigation_routing_v0",
  "reason": "explicit_navigation_task"
}
```

约束（写死）：
- 不加时间/空间字段
- 不膨胀成复杂调度对象
- 只表示“建议结果”

---

## H. 下一步边界（写死）

- 本轮之后，下一步才考虑中台如何消费该建议
- 当前先不做真正的导航/非导航切换
- 当前先不动导航执行链

后续消费契约（设计冻结）：
- `docs/architecture/LUNA_NAVIGATION_NON_NAVIGATION_DISPATCH_CONSUMPTION_PLAN_V0.md`

