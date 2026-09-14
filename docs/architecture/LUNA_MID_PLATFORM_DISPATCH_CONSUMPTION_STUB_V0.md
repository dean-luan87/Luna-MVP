# Luna — Mid-Platform Dispatch Consumption Stub v0（中台分流消费占位：只读）

**文件**：`docs/architecture/LUNA_MID_PLATFORM_DISPATCH_CONSUMPTION_STUB_V0.md`  
**性质**：P3-3 中台分流消费占位设计（只读接住 `need_navigation_routing_v0`；不夺权）  

关联：
- P3-1 建议层：`docs/architecture/LUNA_NEED_NAVIGATION_ROUTING_V0.md`
- P3-2 消费契约：`docs/architecture/LUNA_NAVIGATION_NON_NAVIGATION_DISPATCH_CONSUMPTION_PLAN_V0.md`

---

## A. 文档定位（写死）

- 这是 P3-3 的中台分流消费占位设计。
- 当前目标：让中台主层第一次**正式接住**分流建议结果（只读消费 + 可观察）。
- 当前不做：
  - 真实裁决
  - 执行切换
  - 导航启动
  - 语音/记忆驱动

---

## B. 当前问题定义

- 现在已经有 `need_navigation_routing_v0`（只读建议结果）。
- 也已经有 P3-2 定义的未来消费语义与边界纪律。
- 但当前还缺一个“中台主层正式消费入口”来接住这个建议结果。
- 若没有入口，后续真正裁决层将缺少稳定承接面，容易悬空或越权接线。

---

## C. dispatch consumption stub 的最小定义（写死）

- 它不是裁决器
- 不是任务执行器
- 不是导航启动器
- 只是中台主层的正式接收位
- 作用是：**读取、记录、保留、可观察**

---

## D. 当前允许接收什么（写死）

- 当前只接收：`need_navigation_routing_v0`
- 不直接接收：视角原始 slice
- 不直接接收：解释层原始 candidate
- 不直接接收：自然语言结论

---

## E. 当前不允许做什么（写死）

- 不允许直接切到导航链
- 不允许直接改变当前任务执行路径
- 不允许直接驱动语音
- 不允许直接写记忆
- 不允许把建议结果升格为主链正式事实

---

## F. 当前最小输出/观测位（建议）

建议写入：
- `result.metadata["mid_platform_dispatch_consumption_stub_v0"]`

最小结构：

```json
{
  "consume_attempted": true,
  "consume_scope": "mid_platform_dispatch_consumption_stub_v0",
  "routing_decision_seen": "navigation_required",
  "consume_mode": "read_only"
}
```

约束（写死）：
- 不加时间/空间字段
- 不膨胀成复杂调度对象
- 只做中台主层占位观测

---

## G. 下一步边界（写死）

- 本轮之后，下一步才考虑“中台正式裁决层”
- 再之后才考虑“导航/非导航执行切换”
- 当前不跨这两步

