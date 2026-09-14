# Luna — Navigation Executor Takeover Plan v0（执行器接管层：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_EXECUTOR_TAKEOVER_PLAN_V0.md`  
**性质**：Phase-Next-13：真实导航执行器接管层方案（只冻结接管边界与语义，不接执行器）  

关联：
- 最后门控（类别冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTION_READINESS_GATE_V0.md`
- 最后门控输入面：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTION_READINESS_GATE_INPUTS_V0.md`
- 最后门控统一出口（stub v0）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTION_READINESS_GATE_STUB_V0.md`
- 下游占位消费契约：`docs/architecture/LUNA_NAVIGATION_HANDOFF_POST_BOUND_EXECUTION_STUB_CONSUMPTION_PLAN_V0.md`
- formal decision 窄路径 allow-progress：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_STUB_VNEXT_NARROW_ALLOW_PROGRESS_V0.md`
- 执行器接管层统一只读出口（stub v0）：`docs/architecture/LUNA_NAVIGATION_EXECUTOR_TAKEOVER_STUB_V0.md`
- takeover → executor skeleton 接线（冻结）：`docs/architecture/LUNA_NAVIGATION_EXECUTOR_TAKEOVER_WIRING_V0.md`
- 真实执行器输入层（输入边界冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INPUT_LAYER_V0.md`
- 真实执行器标准化输入对象（对象边界冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INPUT_OBJECT_V0.md`
- 输入对象只读占位输出（placeholder v0）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INPUT_OBJECT_PLACEHOLDER_V0.md`
- 真实执行器接口契约（冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INTERFACE_CONTRACT_V0.md`
- 执行器标准化状态对象（冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_STATUS_OBJECT_V0.md`
- 状态对象只读占位输出（placeholder v0）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_STATUS_PLACEHOLDER_V0.md`
- 执行期最小监控闭环（冻结）：`docs/architecture/LUNA_EXECUTION_MONITORING_MINIMAL_LOOP_V0.md`
- 执行期监控状态只读占位输出：`docs/architecture/LUNA_EXECUTION_MONITORING_STATUS_PLACEHOLDER_V0.md`

---

## A. 文档定位（写死）

- 这是“真实导航执行器接管层”的最小设计文档。
- 当前目标：冻结执行器接管边界与接管语义（可回归、可后续最小接线）。
- 当前不做执行器接入。
- 当前不做地图接入。
- 当前不做语音联动实现。
- 当前不做执行期监控实现。

---

## B. 为什么现在需要“执行器接管层”

- 当前系统已经具备：
  - formal decision 的极窄放行（allow_progress）
  - 下游 stub 对放行结果的消费契约
  - readiness gate 的统一结果（ready_candidate / not_ready / blocked）
- 但仍然缺：
  - 谁来真正接管
  - 接管是否合法
  - 接管后如何回报状态
- 若没有接管层，后续一接执行器就会越层直连、不可治理、难回归。

---

## C. 执行器接管的最小合法入口（写死）

未来执行器只能从以下**组合输入**被合法接管（缺一不可）：

1) `result.metadata["mid_platform_formal_decision_stub_v0"].decision_result == "allow_progress"`  
2) `result.metadata["formal_decision_allow_progress_path_v0"].downstream_placeholder_interface == "navigation_handoff_post_bound_execution_stub_v0"`  
3) `navigation_handoff_post_bound_execution_stub` 下游消费结果满足“已进入可继续推进的占位阶段”（例如 `consumed_pending_execution`）  
4) `result.metadata["navigation_real_execution_readiness_gate_stub_v0"].readiness_status == "ready_candidate"`  

并写死：
- `ready_candidate` 本身不是执行器接管令
- `allow_progress` 本身也不是执行器接管令
- 必须有“执行器接管层”作为最后合法入口，才能把控制权交给执行器

---

## D. 执行器接管的最小语义（写死）

当执行器未来“接管”时，仅表示：
- 系统已把控制权从占位链移交给真实导航执行器
- 后续执行状态必须由执行器与执行期监控链共同反馈
- 接管不等于任务完成
- 接管不等于永不回退

---

## E. 接管前仍需满足的最小边界（写死）

1) **接管授权边界**  
- 当前链路确实允许交给执行器  
- 不存在更高优先级抢占（安全/任务覆盖等更高优先级信号）

2) **单一接管边界**  
- 同一时刻只能有一个合法导航执行器接管当前导航链  
- 不允许并发多执行器竞争接管

3) **输出边界**  
- 执行器接管前，不默认触发“开始导航”播报  
- 语音启动策略应在接管层之后、输出治理层之下另行处理

4) **资源边界**  
- 地图能力、非地图辅助能力、执行监控能力、回退能力若未来接入，必须在接管层之后被消费  
- 不允许绕过接管层直连执行资源

---

## F. 接管后最小回传状态（只定义，不实现）

建议未来最小回传集合（占位语义）：
- `takeover_started`
- `takeover_active`
- `takeover_failed`
- `takeover_interrupted`
- `takeover_released`

说明（写死）：
- 这些是执行器对中台/监控链的最小回传语义
- 当前不实现

---

## G. 接管失败 / 中断 / 回退的最小原则（写死）

- 执行器接管失败时，控制权必须回到中台/上游控制链
- 执行中断时，不允许执行器私自决定后续任务路径
- 回退策略未来必须受中台治理
- 当前不展开实现

---

## H. 与现有链路的关系（写死）

### 与 formal decision

- formal decision 只负责极窄放行
- 不直接把控制权交给执行器

### 与 readiness gate

- readiness gate 只给出“候选就绪”
- 不直接让执行器接管

### 与 post-bound execution stub

- 它是执行器接管前的最后占位链一部分
- 但不是执行器本体

### 与真实执行器

- 真实执行器必须位于接管层之后
- 当前不接入执行器本体

---

## I. 当前仍然不能直接执行的原因（写死）

- 当前没有真实执行器接入
- 当前没有真实接管层实现
- 当前没有执行期监控闭环实现
- 当前没有语音启动策略实现
- 当前没有地图/非地图执行资源真实接入
- 当前没有失败/中断/回退治理实现

---

## J. 当前不做（写死）

- 不做执行器接线
- 不做地图接线
- 不做语音启动实现
- 不做执行监控实现
- 不做回退治理实现
- 不做自动切链

---

## K. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - “执行器接管层”的输入/输出占位设计
- 再之后才考虑：
  - 真实执行器接入方案
- 当前不跨这两步

---

## L. 未来接管结果样例（仅说明，不实现）

```json
{
  "takeover_attempted": true,
  "takeover_scope": "navigation_executor_takeover_v0",
  "takeover_status": "ready_to_takeover|blocked|not_applicable",
  "reason": "..."
}
```

