# Luna — Navigation Real Execution Readiness Gate v0（真实执行前最后门控：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTION_READINESS_GATE_V0.md`  
**性质**：Phase-Next-10：从“占位层消费结果”进入“真实导航执行器接管前状态”的最后门控层（只冻结门控集合，不接执行器）  

关联：
- 下游占位消费契约：`docs/architecture/LUNA_NAVIGATION_HANDOFF_POST_BOUND_EXECUTION_STUB_CONSUMPTION_PLAN_V0.md`
- formal decision 窄路径 allow-progress：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_STUB_VNEXT_NARROW_ALLOW_PROGRESS_V0.md`
- 导航执行前承接层设计冻结：`docs/architecture/LUNA_NAVIGATION_HANDOFF_POST_BOUND_EXECUTION_PLAN_V0.md`
- 导航执行前承接层 stub（只读占位）：`docs/architecture/LUNA_NAVIGATION_HANDOFF_POST_BOUND_EXECUTION_STUB_V0.md`
- 最后门控输入面（v0，占位承接）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTION_READINESS_GATE_INPUTS_V0.md`
- 最后门控统一只读出口（stub v0）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTION_READINESS_GATE_STUB_V0.md`

---

## A. 文档定位（写死）

- 这是导航链进入**真实导航执行器**前的最后门控层设计文档。
- 当前目标：冻结“真实执行前的最小门控集合”（可回归、可后续最小接线）。
- 当前不做真实执行器接入。
- 当前不做地图接入。
- 当前不做语音启动。
- 当前不做执行期闭环实现。

---

## B. 为什么现在需要这一层

- 当前已经具备：
  - formal decision 的极窄放行（allow_progress）
  - 下游占位 stub 的消费契约（consumed_pending_execution 等）
- 但这仍然只是“占位层到占位层”的放行。
- 如果没有“真实执行前最后门控”，后续一旦接入执行器就会越权、不可控。
- 因此必须先定义：什么条件下系统才有资格把控制权交给真实执行器。

---

## C. 当前进入真实执行器前的最小门控类别（只定义 5 类，写死）

> 口径：这里只定义门控类别与最低要求，不做实现算法，不脑补缺失能力。

### C1. 执行器存在性门控

- 系统中存在可用的真实导航执行器
- 执行器状态正常
- 当前允许接管（具备接管信号或能力开关）

### C2. 路径/辅助资源可用性门控

- 地图可用性 **或** 非地图辅助能力可用性
- 至少有一种执行期辅助资源可用
- 当前不能默认假设地图一定存在

### C3. 执行期监控闭环门控

- 进入执行后，必须存在最小监控闭环
- 至少能观察执行：成功/失败/中断/偏航（最小枚举语义）
- 当前若无监控闭环，不应交给执行器

### C4. 启动策略门控

- 是否允许对用户发起“开始导航”类启动行为
- 是否已有对应的输出治理/语音策略
- 当前不能默认执行器一接手就可播报

### C5. 回退/中断门控

- 若执行失败、环境变化、任务被覆盖，是否存在最小回退路径
- 当前若无回退机制，不应轻易进入真实执行

---

## D. 当前真实执行前的最小语义（写死）

即使前面的占位链都满足，只有当“真实执行前最后门控”也满足时，系统才有资格从：
- `consumed_pending_execution`

继续推进到：
- “真实执行器接管前状态”

并写死：
- 这仍不等于执行完成
- 只是允许交给执行器的前一步

---

## E. 当前仍然不能直接执行的原因（写死）

- 当前没有真实导航执行器接入
- 当前没有真实地图/非地图辅助执行资源接入
- 当前没有执行期监控闭环实现
- 当前没有启动语音策略接入
- 当前没有回退/中断治理实现

---

## F. 与现有链路的关系（写死）

### 与 formal decision

- formal decision 只负责放行到下游占位层
- 不直接负责真实执行器接管

### 与 post-bound execution stub

- 当前 stub 只消费 allow-progress（并输出占位状态/消费语义）
- 未来“真实执行前最后门控”应位于 stub 之后、执行器之前

### 与真实执行器

- 真实执行器必须位于本门控层之后
- 当前不接入执行器本体

---

## G. 当前不做（写死）

- 不做真实导航执行器实现
- 不做地图接入
- 不做执行期监控实现
- 不做语音启动实现
- 不做回退策略实现
- 不做自动切链

---

## H. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - “真实执行前最后门控”的只读占位输入面
- 再之后才考虑：
  - 真实执行器接入方案
- 当前不跨这两步

---

## I. 未来门控输出样例（仅说明，不实现）

```json
{
  "readiness_gate_present": true,
  "readiness_status": "not_ready|ready_candidate|blocked",
  "reason": "..."
}
```

