# Luna — Navigation Real Executor Input Object v0（真实导航执行器标准化输入对象：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INPUT_OBJECT_V0.md`  
**性质**：Phase-Next-16：真实导航执行器“标准化输入对象”最小设计（冻结对象边界，不接执行器）  

关联：
- 执行器输入层（边界冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INPUT_LAYER_V0.md`
- takeover plan（接管合法入口冻结）：`docs/architecture/LUNA_NAVIGATION_EXECUTOR_TAKEOVER_PLAN_V0.md`
- readiness gate stub（统一只读出口）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTION_READINESS_GATE_STUB_V0.md`
- formal decision 窄路径 allow-progress：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_STUB_VNEXT_NARROW_ALLOW_PROGRESS_V0.md`
- 主线状态（After Takeover Stub）：`docs/architecture/LUNA_PHASE1_MAINLINE_STATUS_AFTER_TAKEOVER_STUB_V0.md`
- 输入对象只读占位输出（placeholder v0）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INPUT_OBJECT_PLACEHOLDER_V0.md`
- 执行器接口契约（冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INTERFACE_CONTRACT_V0.md`
- 执行器本体最小定义（冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_MINIMAL_DEFINITION_V0.md`

---

## A. 文档定位（写死）

- 这是“真实导航执行器标准化输入对象”的最小设计文档。
- 当前目标：冻结执行器输入对象边界（执行器未来真正接收的标准化对象）。
- 当前不做真实执行器接入。
- 当前不做地图接入。
- 当前不做语音联动。
- 当前不做执行期监控实现。
- 当前不改变现有主线行为。

---

## B. 为什么现在要先定义输入对象

- 当前已经有执行器输入层边界（Input Layer v0）。
- 但仍没有“执行器实际接收对象”的统一定义。
- 若不先定义输入对象，后续真实执行器仍会直接读散乱字段或临时拼装输入，造成越层取数与不可回归。
- 因此必须先冻结标准化输入对象，作为“执行器唯一应消费的对象”。

---

## C. 输入对象在系统中的位置（写死）

该标准化输入对象应位于：

- formal decision 之后  
- readiness gate 之后  
- takeover 层之后  
- executor input layer 之内  
- 真实执行器本体之前  

并写死：

- 它不是建议对象
- 不是裁决对象
- 不是 readiness 对象
- 不是 takeover 对象
- 它是“真实执行器唯一应消费的标准化输入对象”

---

## D. 执行器输入对象的最小字段类别（只定义类别与语义，不做实现/细字段表）

> 口径：只定义类别与语义，不设计过细字段表；当前不做任何实现。

### D1. 接管授权类（必需）

用于表示：
- 当前是否已获得合法接管授权
- 授权来自哪一层的正式结果（来源锚点）

边界（写死）：
- 不允许把 `*_stub` / `*_gate` 直接当成授权对象
- 只允许输入层整理后的“正式授权语义”进入该类别

### D2. 目标 / 任务上下文类（必需）

用于表示：
- 执行器正在服务哪个导航任务（任务上下文）
- 当前目标上下文是什么
- 目标是否已通过正式绑定/承接链（“目标上下文已就绪”的语义）

边界（写死）：
- 执行器不应直接接收 `destination_bound_v0`
- 这里只允许输入层整理后的标准化目标上下文进入

### D3. 路径 / 辅助资源类（可占位，未来真实执行必需）

用于表示：
- 地图模式 / 非地图模式 / 混合模式
- 可用的执行辅助资源类型
- 执行器可消费的路径支持模式

边界（写死）：
- 当前只是类别定义
- 不做真实地图对象设计、不接入地图

### D4. 执行约束类（必需）

用于表示：
- 启动策略约束
- 安全约束最终态
- 回退/中断约束
- 其他执行期必须遵守的限制

边界（写死）：
- 约束类是“最终执行态约束”的入口，但当前仅定义类别，不接真实治理实现

### D5. 监控回传绑定类（可占位，未来真实执行必需）

用于表示：
- 执行器进入执行期后，应把状态回传给哪条监控链 / 中台链
- 当前只是绑定关系占位
- 不做真实监控实现

---

## E. 哪些是“最小必需字段类别”（写死）

以下类别是必需的（缺一则输入对象不成立）：

- 接管授权类
- 目标 / 任务上下文类
- 执行约束类

并写死：
- 没有这些，输入对象不成立
- 路径/辅助资源类与监控回传绑定类当前可以是占位，但未来真实执行必不可少

---

## F. 明确哪些上游对象不能直接等同于输入对象（写死，关键边界）

以下对象都不能直接等同于 `navigation_real_executor_input_v0`：

- `mid_platform_formal_decision_stub_v0`
- `formal_decision_allow_progress_path_v0`
- `navigation_real_execution_readiness_gate_stub_v0`
- `navigation_executor_takeover_stub_v0`
- `destination_bound_v0`
- `navigation_handoff_consume_bound_v0`
- `navigation_handoff_post_bound_execution_stub_v0`
- 任意 `*_candidate`
- 任意 `*_stub`
- 任意 `*_gate`

解释（写死）：
- 它们是输入对象的上游依据（候选/建议/门控/接管前状态/占位结果）。
- 它们不是执行器可直接消费的标准化输入对象；禁止真实执行器越层直读。

---

## G. 输入对象的最小语义（写死）

当未来执行器拿到该对象时，仅表示：

- 上游控制链已把执行所需最小信息整理为统一输入
- 执行器可以基于该对象开始自己的接管/执行逻辑
- 这不等于任务完成
- 也不等于执行一定成功

---

## H. 当前仍然不能接真实执行器的原因（写死）

- 当前只有输入对象设计，没有输入对象实现
- 当前没有真实执行器本体
- 当前没有路径/资源真实接入
- 当前没有执行期监控闭环实现
- 当前没有启动策略真实接线
- 当前没有回退/中断治理真实接线

---

## I. 当前不做（写死）

- 不做真实输入对象代码实现
- 不做真实执行器接入
- 不做真实地图接入
- 不做执行期监控接入
- 不做语音启动接入
- 不做回退治理接入
- 不做自动切链

---

## J. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - 执行器输入对象的输入占位设计或对象草图
- 再之后才考虑：
  - 真实执行器接入方案
- 当前不跨这两步

---

## K. 未来输入对象样例（仅说明，不实现、不落代码）

```json
{
  "executor_input_present": true,
  "executor_input_scope": "navigation_real_executor_input_v0",
  "takeover_authorized": true,
  "task_context_ready": true,
  "path_support_mode": "map|non_map|hybrid",
  "execution_constraints_ready": false,
  "monitor_binding_ready": false
}
```

