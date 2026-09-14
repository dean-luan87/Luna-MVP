# Luna — Mid-Platform Formal Decision Stub v0（中台正式裁决层：只读占位）

**文件**：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_STUB_V0.md`  
**性质**：Phase-Next-2：正式裁决层只读占位 stub（固定输出位；不进入真实裁决/执行）  

关联：
- 正式裁决层设计冻结：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_LAYER_V0.md`

---

## A. 文档定位（写死）

- 这是正式裁决层的**只读占位设计**。
- 当前目标：让正式裁决层第一次拥有固定输出位（主链可观察）。
- 当前不做：
  - 真实裁决实现
  - 执行切换
  - 导航启动
  - 语音/记忆驱动

---

## B. 当前问题定义

- 现在已经有“正式裁决层”的设计冻结，但没有真正的 stub 输出位。
- 若没有 stub，正式裁决层仍只是文档语义，无法形成主线观测位与回归入口。
- 因此本轮先占住：**现有关键输入面 → 正式裁决层只读 stub → `result.metadata` 观测**。

---

## C. formal decision stub 的最小定义（写死）

- 它不是正式裁决器
- 不是导航执行器
- 不是任务切换器
- 只是“正式裁决层”的只读占位输出
- 作用是：读取当前已存在关键输入，**保守**收束为一个正式裁决结果占位

---

## D. 当前最小允许输入（写死）

写死：只读取当前已经存在且稳定的输入面（来自 `result.metadata`）：
- `need_navigation_routing_v0`
- `mid_platform_dispatch_consumption_stub_v0`
- `destination_bound_v0`
- `navigation_handoff_consume_bound_v0`
- `navigation_handoff_post_bound_execution_stub_v0`

并明确（写死）：
- 安全状态 / 任务有效性状态当前若未真实存在，只能视为“缺失门控输入”，不得伪造。

---

## E. 当前最小输出位（写死）

固定写入：
- `result.metadata["mid_platform_formal_decision_stub_v0"]`

最小结构：

```json
{
  "decision_attempted": true,
  "decision_scope": "mid_platform_formal_decision_stub_v0",
  "decision_result": "hold_pending",
  "reason": "missing_required_gate_inputs"
}
```

约束（写死）：
- 不加时间/空间字段
- 不膨胀成复杂裁决对象
- 只表示正式裁决层的占位结果

---

## F. 当前最小结果集合（沿用设计冻结，但本轮只落保守子集）

沿用正式裁决层结果集合：
- `allow_progress`
- `hold_pending`
- `block_execution`
- `switch_branch`（本轮可只占位，不要求产出）

并写死：
- 由于当前缺少任务有效性/安全门控等真实输入，本轮大多数情况下必须保守落到 `hold_pending`。
- 不能因为某几个前置条件满足就轻易输出 `allow_progress`。

---

## G. 当前不允许做什么（写死）

- 不允许直接切导航链
- 不允许直接触发导航执行
- 不允许直接驱动语音
- 不允许直接写记忆
- 不允许伪造缺失门控输入
- 不允许把建议层结果直接当最终裁决

---

## H. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  1) 正式裁决层如何接入更多真实门控输入  
  2) 再把某类裁决结果接到真实执行链  
- 当前不跨这两步。

