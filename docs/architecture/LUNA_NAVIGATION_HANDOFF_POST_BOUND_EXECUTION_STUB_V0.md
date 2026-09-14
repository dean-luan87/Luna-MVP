# Luna — Navigation Handoff Post-Bound Execution Stub v0（执行前承接层：只读占位）

**文件**：`docs/architecture/LUNA_NAVIGATION_HANDOFF_POST_BOUND_EXECUTION_STUB_V0.md`  
**性质**：P4-2 执行前承接层只读占位 stub（不启动真实导航）  

关联：
- P4-1 执行前承接层设计冻结：`docs/architecture/LUNA_NAVIGATION_HANDOFF_POST_BOUND_EXECUTION_PLAN_V0.md`
- 目标已绑定事实层：`docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_BOUND_MATERIALIZATION_IMPL_V0.md`
- P3-1 建议层：`docs/architecture/LUNA_NEED_NAVIGATION_ROUTING_V0.md`
- P3-3 中台消费 stub：`docs/architecture/LUNA_MID_PLATFORM_DISPATCH_CONSUMPTION_STUB_V0.md`
- 下游消费契约（允许消费 allow_progress，但仍不执行）：`docs/architecture/LUNA_NAVIGATION_HANDOFF_POST_BOUND_EXECUTION_STUB_CONSUMPTION_PLAN_V0.md`

---

## A. 文档定位（写死）

- 这是 P4-2 的执行前承接层**只读占位设计**。
- 当前目标：让导航链正式拥有“真实执行前”的 stub 入口与可观测输出位。
- 当前不做：
  - 真实导航启动
  - 地图接入
  - 跨链自动切换
  - 语音/记忆驱动

---

## B. 当前问题定义

- P4-1 已冻结“执行前承接层”的语义与门控类别。
- 但当前仍没有一个真正的 stub 入口把它接住。
- 若没有 stub，P4-1 仍停留在文档语义，无法形成主线观测位与回归入口。

---

## C. execution stub 的最小定义（写死）

- 它不是执行器
- 不是裁决器
- 不是导航启动器
- 只是“执行前承接层”的正式接收位
- 作用是：读取、检查最小前提、输出承接状态占位

---

## D. 当前最小允许输入（写死）

当前可直接读取的已存在输入：
- `destination_bound_v0`
- `navigation_handoff_consume_bound_v0`

当前只能占位说明、不可真实依赖的输入：
- 中台未来正式裁决结果（当前未实现）

并写死：
- `need_navigation_routing_v0` 不能当执行启动令
- `mid_platform_dispatch_consumption_stub_v0` 不能当执行启动令

---

## E. 当前最小输出位（写死）

固定写入：
- `result.metadata["navigation_handoff_post_bound_execution_stub_v0"]`

最小结构：

```json
{
  "execution_stub_attempted": true,
  "execution_scope": "navigation_handoff_post_bound_execution_stub_v0",
  "execution_state": "execution_pending",
  "reason": "missing_formal_mid_platform_dispatch"
}
```

约束（写死）：
- 不加时间/空间字段
- 不膨胀成复杂执行对象
- 只表示“执行前承接状态占位”

---

## F. 当前最小承接状态集合（只允许 3 类）

- `execution_ready`
- `execution_blocked`
- `execution_pending`

在当前 stub 下的语义（写死）：
- 由于缺少“中台正式裁决结果”，满足最小前提时应保守落到 `execution_pending`
- 不能因为 `destination_bound_v0` 存在就判 `execution_ready`

---

## G. 当前不允许做什么（写死）

- 不允许直接启动导航
- 不允许直接切执行链
- 不允许把 `destination_bound_v0` 单独当执行令
- 不允许把 consume stub 结果当执行令
- 不允许跳过未来正式门控

---

## H. 下一步边界（写死）

- 本轮之后，下一步才考虑“中台正式裁决结果”如何接入这个 stub
- 再之后才考虑“真实导航执行链”
- 当前不跨这两步

