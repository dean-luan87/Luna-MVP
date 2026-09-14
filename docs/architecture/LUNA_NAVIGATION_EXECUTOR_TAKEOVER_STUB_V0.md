# Luna — Navigation Executor Takeover Stub v0（执行器接管层：统一只读出口）

**文件**：`docs/architecture/LUNA_NAVIGATION_EXECUTOR_TAKEOVER_STUB_V0.md`  
**性质**：Phase-Next-14：执行器接管层只读 stub（统一输出位；不接真实执行器）  

关联：
- 执行器接管层方案（合法入口冻结）：`docs/architecture/LUNA_NAVIGATION_EXECUTOR_TAKEOVER_PLAN_V0.md`
- 最后门控统一出口（readiness stub v0）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTION_READINESS_GATE_STUB_V0.md`
- 下游占位消费契约：`docs/architecture/LUNA_NAVIGATION_HANDOFF_POST_BOUND_EXECUTION_STUB_CONSUMPTION_PLAN_V0.md`
- formal decision 窄路径 allow-progress：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_STUB_VNEXT_NARROW_ALLOW_PROGRESS_V0.md`

---

## A. 文档定位（写死）

- 这是执行器接管层的**只读 stub** 设计。
- 当前目标：让接管层拥有统一输出位，形成可观察、可回归的“接管前状态占位结果”。
- 当前不接真实执行器。
- 当前不接地图。
- 当前不驱动语音/记忆。
- 当前不改变现有执行行为。

---

## B. 为什么现在要做 takeover stub

- 执行器接管合法入口已经冻结（Takeover Plan v0）。
- 但当前还没有一个统一的接管层输出。
- 若没有这个输出，后续真实执行器仍会直接读散乱状态，形成越层直连。
- 因此必须先让接管层有自己的只读结果（统一出口）。

---

## C. takeover stub 的最小定义（写死）

- 它不是执行器
- 不是地图规划器
- 不是语音启动器
- 只是执行器接管层的统一只读判断出口
- 作用：读取“接管合法入口”相关状态，输出当前是否“可进入接管前状态”的占位结果

---

## D. 当前最小输入（写死，缺一不可）

只读以下输入（不脑补、不补缺）：

1) `result.metadata["mid_platform_formal_decision_stub_v0"]`  
   - 且 `decision_result == "allow_progress"`

2) `result.metadata["formal_decision_allow_progress_path_v0"]`  
   - 且 `downstream_placeholder_interface == "navigation_handoff_post_bound_execution_stub_v0"`

3) post-bound execution stub 下游消费相关状态  
   - 满足“已进入可继续推进的占位阶段”，例如：`consumed_pending_execution`
   - **说明（写死）**：若当前仓库尚未实现该消费结果键，则只能使用等价占位依据（例如已观察到 `navigation_handoff_post_bound_execution_stub_v0` 处于 `execution_pending` 且 bound/consume-bound 已存在），否则一律视为不满足

4) `result.metadata["navigation_real_execution_readiness_gate_stub_v0"]`  
   - 且 `readiness_status == "ready_candidate"`

并写死：
- 缺一不可
- 不允许脑补
- 这些只是接管前依据，不是接管完成信号

---

## E. 当前最小输出位（写死）

固定写入：
- `result.metadata["navigation_executor_takeover_stub_v0"]`

最小结构（建议）：

```json
{
  "takeover_attempted": true,
  "takeover_scope": "navigation_executor_takeover_stub_v0",
  "takeover_status": "ready_to_takeover|blocked|not_applicable",
  "reason": "..."
}
```

约束（写死）：
- 不加时间/空间字段
- 不膨胀成复杂对象
- 只表示接管层统一占位结果

---

## F. 当前最小结果集合（只允许 3 类，写死）

1) **ready_to_takeover**
- 合法入口条件全部满足
- 仅表示“未来真实执行器可尝试接管前的最后占位状态已成立”
- 不等于真实执行器已经接管

2) **blocked**
- 存在明确阻断条件
- 当前不应继续推进到真实执行器接管

3) **not_applicable**
- 当前不属于发给执行器接管层的链路，或缺少最小接管依据
- 因此不消费

---

## G. 最小判断规则（克制，写死）

规则 1：全部合法入口成立 → `ready_to_takeover`
- decision_result == allow_progress
- 下游接口匹配
- 下游消费结果已进入可继续推进占位阶段
- readiness gate == ready_candidate

规则 2：存在明确阻断 → `blocked`
- 若 readiness gate == blocked（或未来出现明确定义为阻断的输入）

规则 3：其他情况 → `not_applicable`

写死：
- 当前不扩复杂原因树
- 先保证最小合法入口成立时能统一输出

---

## H. 当前不允许做什么（写死）

- 不允许真实执行器接管
- 不允许触发真实导航开始
- 不允许触发地图规划
- 不允许播报“开始导航”
- 不允许把 ready_to_takeover 当任务完成
- 不允许绕过后续真实执行器接入层

---

## I. 与现有链路的关系（写死）

### 与 formal decision

- formal decision 只负责极窄放行
- 不直接输出接管结果

### 与 readiness gate

- readiness gate 只给出真实执行前最后门控的统一结果
- 不直接输出接管结果

### 与 post-bound execution stub

- post-bound stub 消费 allow-progress
- takeover stub 位于其后、真实执行器之前

### 与真实执行器

- 真实执行器未来只能读取 takeover 层或其后续正式接管层结果
- 当前不接入执行器本体

