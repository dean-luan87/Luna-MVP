# Luna — Execution Monitoring Minimal Loop v0（执行期最小监控闭环：设计冻结）

**文件**：`docs/architecture/LUNA_EXECUTION_MONITORING_MINIMAL_LOOP_V0.md`  
**性质**：Phase-Next-23：执行期最小监控闭环定义（冻结可观测/可回传/可治理边界，不接执行器）  

关联：
- 执行器本体最小定义：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_MINIMAL_DEFINITION_V0.md`
- 执行器接口契约：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INTERFACE_CONTRACT_V0.md`
- 执行器输入对象：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INPUT_OBJECT_V0.md`
- 执行器状态对象：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_STATUS_OBJECT_V0.md`
- 接入就绪评审：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INTEGRATION_READINESS_REVIEW_V0.md`
- 回退/中断治理入口（冻结）：`docs/architecture/LUNA_NAVIGATION_ROLLBACK_AND_INTERRUPTION_GOVERNANCE_ENTRY_V0.md`

---

## A. 文档定位（写死）

- 这是“执行期最小监控闭环”的设计文档。
- 当前目标：冻结执行后最小可观测、可回传、可治理的闭环边界。
- 当前不做真实监控实现。
- 当前不做真实执行器接入。
- 当前不做地图接入。
- 当前不做语音/记忆联动。
- 当前不改变现有主线行为。

---

## B. 为什么现在必须先定义监控闭环

- 当前执行器相关输入/输出/接口/本体边界已基本定义。
- 但没有执行期监控闭环，就无法安全进入真实执行器接入阶段。
- 没有监控闭环就无法判断：
  - 是否真的在执行
  - 是否已偏航
  - 是否已失败
  - 是否应中断/回退
- 因此监控闭环是硬阻断项之一，必须先定义。

---

## C. 执行期监控闭环的最小定义（写死）

执行期最小监控闭环是：

- 围绕执行器运行状态、异常状态、能力状态、偏航状态形成的最小“观测—标准化—回传—上游治理”闭环。

它不是：

- 正式裁决层
- readiness gate
- takeover 授权层
- 语音输出层
- 回退策略最终裁决层

核心一句（写死）：

**监控闭环负责持续观测执行状态并回传可治理信号；是否继续、是否中断、是否回退仍由上游治理决定。**

---

## D. 最小监控对象类别（只定义类别，不发散）

1) **接管状态监控**
- takeover 是否开始
- takeover 是否激活
- takeover 是否释放

2) **执行状态监控**
- 是否 running
- 是否 completed
- 是否 failed
- 是否 interrupted

3) **异常 / 偏航监控**
- 是否偏航
- 是否不可执行
- 是否环境突变
- 是否出现需要上游介入的异常

4) **能力 / 资源状态监控**
- 执行器能力是否 degraded
- 资源是否退化
- 是否仍具备继续执行的最低能力

5) **回传路由监控**
- 当前状态是否已正确进入中台/监控链
- 当前仅作为未来占位语义，不做真实路由实现

---

## E. 最小监控闭环动作（只定义步骤，不做实现）

1) **观测**
- 执行器周期性/事件性产生状态（事实信号）

2) **标准化**
- 状态被组织成标准化状态对象（例如 `navigation_real_executor_status_v0` 的正式实现版）

3) **回传**
- 状态回传给中台/监控链（回传链路本期不实现）

4) **上游消费**
- 中台/监控链消费这些状态，决定是否继续、是否中断、是否回退（治理层本期不实现）

---

## F. 最小状态语义分组（至少 4 组）

1) **正常推进**
- 可继续执行
- 当前未见异常

2) **退化运行**
- 仍可继续，但能力下降
- 未来可能需上游收缩能力/提醒

3) **中断/暂停候选**
- 当前不宜继续推进
- 需要上游决定是否暂停/接管/回退

4) **失败/不可执行候选**
- 当前执行无法继续
- 必须回传给上游治理链

---

## G. 哪些事件必须立即回传（写死）

至少包括：

- `execution_failed`
- `execution_interrupted`
- `execution_degraded`
- 明确偏航
- 明确不可执行
- takeover 异常释放

并写死：

- 这些事件不能仅停留在执行器内部
- 必须形成标准化状态回传（作为上游治理可消费的信号）

---

## H. 监控闭环明确不负责什么（写死）

监控闭环不负责：

- 正式裁决
- readiness 判断
- takeover 合法性授权
- 语音输出策略
- 回退策略最终裁决
- 记忆写入

---

## I. 与现有链路的关系（写死）

### 与执行器本体

- 执行器本体产生执行状态（事实）
- 监控闭环负责观察并组织回传（信号治理）

### 与状态对象

- 状态对象是监控闭环的标准化输出载体之一
- 监控闭环不等于状态对象本身（闭环包含观测/标准化/回传/上游消费）

### 与中台 / 治理链

- 监控闭环把“事实状态”送回中台/治理链
- 上游决定后续动作

### 与回退 / 中断治理

- 监控闭环负责发现并回传问题
- 回退是否发生由后续治理层决定

---

## J. 当前仍然不能进入真实执行器接入的原因（写死）

- 当前只有监控闭环定义，没有监控实现
- 当前没有真实执行器状态产出
- 当前没有真实状态回传路由
- 当前没有中台消费这些状态的真实治理接线
- 当前没有回退/中断治理真实实现
- 当前没有启动策略真实接线

---

## K. 当前不做（写死）

- 不做真实监控实现
- 不做真实执行器接入
- 不做地图接入
- 不做语音/记忆联动
- 不做回退治理实现
- 不做自动切链

---

## L. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - 监控状态对象 placeholder 或监控链输入输出占位
- 再之后才考虑：
  - 真实执行器最小接入实验线
- 当前不跨这两步

---

## M. 未来监控闭环状态样例（仅说明，不实现、不落代码）

```json
{
  "monitoring_loop_present": true,
  "monitoring_scope": "execution_monitoring_minimal_loop_v0",
  "execution_state": "execution_running",
  "anomaly_state": "none",
  "degradation_state": "normal",
  "upstream_report_required": false
}
```

