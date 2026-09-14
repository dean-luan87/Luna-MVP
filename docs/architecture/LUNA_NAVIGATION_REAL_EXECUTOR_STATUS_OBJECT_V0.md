# Luna — Navigation Real Executor Status Object v0（真实导航执行器标准化状态对象：设计冻结）

**文件**：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_STATUS_OBJECT_V0.md`  
**性质**：Phase-Next-19：真实导航执行器状态回传对象最小设计（冻结对象边界，不接执行器）  

关联：
- 执行器接口契约（冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INTERFACE_CONTRACT_V0.md`
- 执行器输入对象（冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INPUT_OBJECT_V0.md`
- 执行器接管层方案（冻结）：`docs/architecture/LUNA_NAVIGATION_EXECUTOR_TAKEOVER_PLAN_V0.md`
- readiness gate stub（统一只读出口）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTION_READINESS_GATE_STUB_V0.md`
- 主线状态（After Takeover Stub）：`docs/architecture/LUNA_PHASE1_MAINLINE_STATUS_AFTER_TAKEOVER_STUB_V0.md`
- 状态对象只读占位输出（placeholder v0）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_STATUS_PLACEHOLDER_V0.md`
- 执行期最小监控闭环（冻结）：`docs/architecture/LUNA_EXECUTION_MONITORING_MINIMAL_LOOP_V0.md`
- 执行期监控状态只读占位输出：`docs/architecture/LUNA_EXECUTION_MONITORING_STATUS_PLACEHOLDER_V0.md`

---

## A. 文档定位（写死）

- 这是“真实导航执行器标准化状态对象”的最小设计文档。
- 当前目标：冻结执行器状态回传对象边界（执行器回传给中台/监控链的统一对象）。
- 当前不做真实执行器接入。
- 当前不做执行状态代码实现。
- 当前不做监控链接线实现。
- 当前不改变现有主线行为。

---

## B. 为什么现在要先定义状态对象

- 当前已经有执行器接口契约，也已定义最小回传状态集合（语义枚举）。
- 但还没有“这些状态如何被组织成统一对象”的正式定义。
- 若不先冻结状态对象，后续真实执行器会回传散乱字段，监控链与中台无法稳定消费与治理。
- 因此必须先冻结状态对象，作为回传的统一承载。

---

## C. 状态对象在系统中的位置（写死）

该对象应位于：

- 真实执行器之后  
- 监控链 / 中台消费层之前  
- takeover 层回传链之内  
- 不进入建议层 / 候选层 / 裁决层  

并写清（写死）：

- 它不是建议对象
- 不是 formal decision 对象
- 不是 readiness 对象
- 不是 takeover 授权对象
- 它是“执行器唯一应回传的标准化状态对象”

---

## D. 状态对象的最小字段类别（只定义类别与语义，不做实现/细字段表）

> 口径：只定义类别与语义，不设计过细字段表；当前不做实现。

### D1. 接管状态类（必需）

用于表示：
- takeover 是否开始
- takeover 是否激活
- takeover 是否释放

### D2. 执行状态类（必需）

用于表示：
- execution 是否运行中
- 是否完成
- 是否失败
- 是否中断

### D3. 异常 / 偏航状态类（必需）

用于表示：
- 是否检测到偏航
- 是否不可执行
- 是否环境突变
- 是否建议上游回退（建议语义，不是最终裁决）

### D4. 资源 / 能力状态类（可占位，未来真实接入必需）

用于表示：
- 当前执行器能力是否退化
- 当前是否仍可继续执行
- 资源是否降级

### D5. 回传绑定 / 路由类（可占位，未来真实接入必需）

用于表示：
- 该状态对象应回传给哪条监控链 / 中台链
- 当前只是绑定关系占位
- 不做真实路由实现

---

## E. 哪些是“最小必需字段类别”（写死）

以下类别是必需的（缺一则状态对象不成立）：

- 接管状态类
- 执行状态类
- 异常 / 偏航状态类

并写清（写死）：
- 没有这些，状态对象不成立
- 资源 / 能力状态类、回传绑定 / 路由类当前可以是占位，但未来真实接入必不可少

---

## F. 明确哪些内容不能直接等同于状态对象（写死，关键边界）

以下都不能直接等同于 `navigation_real_executor_status_v0`：

- `takeover_started`
- `takeover_active`
- `takeover_released`
- `execution_running`
- `execution_completed`
- `execution_failed`
- `execution_interrupted`
- `execution_degraded`
- 任意单个事件回调
- 任意监控日志片段
- 任意异常告警片段
- 任意 UI 展示状态

解释（写死）：
- 它们是状态对象的组成依据或单点事件/片段
- 不是中台/监控链应消费的完整标准化状态对象

---

## G. 状态对象的最小语义（写死）

当未来系统拿到该对象时，仅表示：

- 真实执行器已把自身当前执行状态整理成统一回传对象
- 中台/监控链可以基于该对象做观察、记录、治理、回退判断
- 这不等于任务一定完成
- 也不等于系统一定要立刻采取行动

---

## H. 与现有链路的关系（写死）

### 与执行器接口契约

- 接口契约定义执行器应回什么状态类别
- 状态对象定义这些状态如何被标准化组织

### 与 takeover 层

- takeover 层定义接管边界
- 状态对象记录接管后的状态事实
- 两者不能混用

### 与 formal decision / readiness

- formal decision 与 readiness 发生在执行前
- 状态对象发生在执行器接管之后
- 不得反向替代裁决层

### 与监控链 / 中台

- 状态对象未来应由监控链与中台消费
- 当前不接线实现

---

## I. 当前仍然不能接真实执行器的原因（写死）

- 当前只有状态对象设计，没有状态对象实现
- 当前没有真实执行器本体
- 当前没有真实监控链接入
- 当前没有回退治理真实接线
- 当前没有地图/非地图资源真实接线
- 当前没有语音启动与执行播报真实接线

---

## J. 当前不做（写死）

- 不做状态对象代码实现
- 不做真实执行器接入
- 不做监控链接入
- 不做语音/记忆联动
- 不做地图接入
- 不做自动回退治理实现

---

## K. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - 执行器状态对象的占位输出设计
- 再之后才考虑：
  - 真实执行器最小接入方案
- 当前不跨这两步

---

## L. 未来状态对象样例（仅说明，不实现、不落代码）

```json
{
  "executor_status_present": true,
  "executor_status_scope": "navigation_real_executor_status_v0",
  "takeover_state": "takeover_active",
  "execution_state": "execution_running",
  "anomaly_state": "none",
  "executor_capability_state": "normal",
  "status_route_binding_ready": false
}
```

