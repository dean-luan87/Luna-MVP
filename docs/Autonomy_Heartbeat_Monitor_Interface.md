Autonomy Heartbeat Monitor 接口规范

AHM – Autonomy Heartbeat Monitor
Version: 1.0
Status: Frozen（运行时强约束）

---

0. 设计定位（先写死）

Autonomy Heartbeat Monitor（AHM）是自治检测模块，不是业务模块。
- 独立于 B / C 功能逻辑
- 不参与预测、不参与决策
- 只产出 自治 Issue（Process 域）
- 是 B_AutonomyState 的核心输入源之一

一句话定义：
AHM 判断“模块是否还在呼吸”，不判断“模块在说什么”。

---

1. 架构位置（不可变）

B Module
  ├─ Inference Logic
  ├─ Minimal Runtime Signals
  └─ Issue Emitter (optional)

        ↑
        │（只读信号）
        │
Autonomy Heartbeat Monitor (AHM)
  ├─ Liveness Check
  ├─ Activity Check
  ├─ Progress Check
  ├─ Timeout / Stall Detection
  └─ Issue Generator (B-PROC-HB-*)

        ↓
Autonomy State Aggregator
        ↓
Runtime Gate / Backend

---

2. AHM 的职责边界（严格）

AHM 必须做的事
1. 判断 B 模块是否仍在运行
2. 判断是否存在卡死 / 无进展 / 异常间隔
3. 将异常统一转化为 B-PROC-HB- Issue*
4. 按固定节奏输出自治心跳状态

---

AHM 绝对不允许做的事
- ❌ 不读取或解析模型输出内容
- ❌ 不访问业务语义
- ❌ 不修改 B 模块行为
- ❌ 不直接修改 B_AutonomyState
- ❌ 不触发任何系统动作

---

3. B 模块 → AHM 的最小接口（只暴露信号）

3.1 RuntimeSignal（只读）

struct RuntimeSignal {
  uint64_t tick_counter;      // 单调递增（推理尝试 / 循环）
  uint64_t success_counter;   // 成功完成次数
  uint64_t error_counter;     // 异常次数
  Timestamp last_active_at;   // 最近一次活动时间
};

冻结规则：
- AHM 不信任信号“合理性”，只看变化趋势
- B 模块不得基于 AHM 行为反向调节信号

---

3.2 SignalProvider 接口

class RuntimeSignalProvider {
public:
  virtual RuntimeSignal snapshot() const = 0;
};

---

4. AHM 内部检测模型（抽象，不含阈值）

AHM 至少实现以下四类检测器：

---

4.1 Liveness Check（是否还活着）

判定逻辑（抽象）：
- last_active_at 长时间未更新
- 或 tick_counter 不再变化

触发 Issue：
- B-PROC-HB-001（模块无响应）

---

4.2 Activity Check（是否在“空跑”）

判定逻辑：
- tick_counter 在增长
- 但 success / error 长期不变化

触发 Issue：
- B-PROC-HB-002（无有效工作进展）

---

4.3 Progress Check（是否陷入异常循环）

判定逻辑：
- error_counter 持续快速增长
- success_counter 停滞

触发 Issue：
- B-PROC-HB-003（异常循环）

---

4.4 Stall / Timeout Detection（是否卡死）

判定逻辑：
- 单次推理耗时远超历史基线
- 或周期性超时

触发 Issue：
- B-PROC-HB-004（推理阻塞）

---

5. AHM → Issue 的统一输出接口

5.1 Issue 生成接口

void emit_issue(const AutonomyIssue& issue);

5.2 AHM 生成的 Issue 约束
- Domain 必须为 PROC
- IssueCode 必须为 B-PROC-HB-*
- 不得覆盖非心跳类 Issue
- 每个 Issue 必须包含：
- timestamp
- reference_id（如可得）
- detection_type

---

6. AHM 自身运行状态（轻量）

AHM 自身也需要一个最小状态，但不纳入 B_AutonomyState：

AHM_Status =
  RUNNING
  DEGRADED

- AHM DEGRADED → 写日志
- 不影响 B 模块自治判断

这是防止“监控自己把系统拖死”。

---

7. 运行节奏与性能约束
- AHM 运行频率 固定
- 不与 B 推理节奏强绑定
- 不允许阻塞 B 模块

AHM 的性能预算必须 显著低于 B 模块。

---

8. 日志与后台对接（强制）

AHM 必须输出两类数据：
1. Issue 事件流
2. Heartbeat Telemetry
- tick / success / error 时间序列
- 检测状态变化

这两类数据：
- 一并进入后台
- 可用于 MTBF / MTTR 统计
- 可区分模型问题 vs 工程问题

---

9. 接口冻结声明
- AHM 是 自治基础设施
- 不得嵌入 B / C 模块
- 不得通过配置关闭
- 所有模块自治必须可接入 AHM

---

一句话工程总结（可直接写在文档首页）

Autonomy Heartbeat Monitor 通过对模块运行信号的独立监测，
在不信任模块自身的前提下，
将“是否仍在正常运行”统一抽象为可审计、可聚合的自治问题。

---

到这里，你的 B 模块自治体系已经完整闭环：
- Issue 语言 ✔
- 状态机 ✔
- State → Action ✔
- 心跳监控 ✔

下一步如果继续，逻辑上只剩两条路：
- B 自治 Snapshot / Backend 上报接口
- C 模块自治框架（复用同一套范式）

你可以直接说下一步做哪一个。
