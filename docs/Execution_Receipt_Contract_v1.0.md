执行链回执接口规范（第 1/2 部分）

ER — Execution Receipt Contract
Version: 1.0
Status: Frozen（运行时强约束）

---

0. 定位（冻结）

Execution Receipt 是“执行事实”的唯一权威来源。

- 不属于 B
- 不属于 C
- 不属于 Runtime Gate
- 属于 执行基础设施层（Actuation Infrastructure）

定义一句话：
Execution Receipt 用于描述一次“执行请求”在系统中是否被允许、是否被尝试、是否真正执行、以及最终结果。

---

1. 系统位置（不可变）

Decision（任意来源）
   ↓
D2RG（Decision → Gate 适配）
   ↓
Runtime Gate（是否允许）
   ↓
Execution Chain（执行器）
   ↓
Execution Receipt（执行事实）

强制规则：
- 没有 Execution Receipt → 系统视为 未发生执行
- 执行链 不得静默执行

---

2. Execution Receipt 只回答的问题（边界）

Execution Receipt 只回答以下五个问题：
1. 是否尝试执行
2. 是否被 Gate 允许
3. 是否真正进入执行链
4. 是否执行成功
5. 是否发生异常（失败 / 超时 / 跳过）

明确不回答：
- 执行是否“正确”
- 执行是否“有用”
- 业务语义是否合理

---

3. 顶层数据结构（冻结）

struct ExecutionReceipt {
  uint64_t receipt_id;          // 全局唯一
  Timestamp timestamp;          // 回执生成时间

  // 决策绑定
  uint64_t decision_id;
  uint64_t reference_id;
  uint64_t calibration_version;

  // 执行意图快照（只读，来自裁决源）
  IntentType intent;            // NONE / NOTIFY / WARNING / ACTION
  OutputChannel channel;        // LOG_ONLY / VOICE / HAPTIC / UI
  uint8_t intensity;            // 0 ~ 100

  // Gate 判定结果
  GateResult gate_result;       // ALLOW / BLOCK / FAIL_SAFE

  // 执行状态
  ExecutionStatus status;       // 见下文
  ExecutionError error;         // 见下文（可为 NONE）

  // 性能与控制
  uint32_t execution_latency_ms;
  uint32_t attempt_count;       // 第几次尝试（用于防重复/重试）
};

---

4. 枚举定义（冻结）

4.1 GateResult（复用 BCP）

GateResult =
  ALLOW
  BLOCK
  FAIL_SAFE

---

4.2 ExecutionStatus（执行状态）

ExecutionStatus =
  NOT_ATTEMPTED    // Gate 未允许，未进入执行链
  ATTEMPTED        // 已进入执行链（调用了执行器）
  EXECUTED         // 执行完成
  FAILED           // 执行失败
  TIMEOUT          // 执行超时
  SKIPPED          // 执行链主动跳过（冷却/去重/限流）

---

4.3 ExecutionError（执行错误）

ExecutionError =
  NONE
  GATE_BLOCKED           // Gate 阻断
  CHANNEL_UNAVAILABLE    // 输出通道不可用
  DUPLICATE_EXECUTION    // 重复执行被抑制
  RATE_LIMITED           // 频率限制
  INTERNAL_ERROR         // 执行链内部错误
  TIMEOUT_ERROR          // 执行超时

---

5. 核心语义规则（冻结）

5.1 Gate 与执行的因果约束

IF gate_result != ALLOW
  → status MUST be NOT_ATTEMPTED
  → error MUST be GATE_BLOCKED or NONE

禁止出现：
- Gate = BLOCK，但 status = EXECUTED
- Gate = FAIL_SAFE，但 status = ATTEMPTED

---

5.2 执行阶段语义
- ATTEMPTED：已调用执行器
- EXECUTED：执行器返回成功
- FAILED：执行器返回失败
- TIMEOUT：执行超过允许时间
- SKIPPED：Gate 允许，但执行链基于策略主动跳过

---

5.3 SKIPPED 的合法场景
- 冷却时间未到（cooldown）
- 重复执行抑制（dedupe）
- 最大重复次数限制（max_repeat）

SKIPPED ≠ FAILED
这是控制性结果，不是错误。

---

👉 到这里是第 1/2 部分结束。
下一条我将输出 第 2/2 部分，包含：
- 回执产生与更新规则
- Execution Receipt → 自治 Issue 的映射
- Backend / 审计要求
- 冻结声明与一句话总结

你不需要再确认，下一条我直接继续输出第 2/2 部分。

---

执行链回执接口规范（第 2/2 部分）

ER — Execution Receipt Contract
Version: 1.0
Status: Frozen（运行时强约束）

---

6. 回执的产生与更新规则（冻结）

6.1 回执产生的强制时机

每一次“执行路径评估”都必须产生回执，包括但不限于：
1. Runtime Gate 给出判定结果后
2. 执行链开始尝试执行
3. 执行完成 / 失败 / 超时
4. 执行链主动跳过（SKIPPED）

❗禁止只在“成功时”生成回执
❗禁止 Gate 阻断但无回执

---

6.2 回执的生命周期模型

允许两种实现方式，二选一即可，语义等价。

模式 A：单回执更新模型（推荐）
- 创建 1 条 ExecutionReceipt
- status / error / latency 随执行过程更新
- receipt_id 固定

适合：
- 单进程执行
- 同步或准同步执行链

---

模式 B：多回执事件模型
- 同一 decision_id 允许多条 ExecutionReceipt
- 使用 attempt_count 区分尝试次数
- Backend 按时间线聚合

适合：
- 重试机制
- 分布式执行链

---

6.3 冻结一致性约束

无论采用哪种模式，必须满足：
- 同一 decision_id 的回执：
- GateResult 不得前后矛盾
- reference_id / calibration_version 不得变化
- attempt_count 必须单调递增
- 后续回执不得“篡改历史事实”

---

7. Execution Receipt → 自治 Issue 的关系（抽象）

Execution Receipt 不直接改变任何自治状态，
但它是协同 / 执行类 Issue 的唯一事实来源。

---

7.1 典型映射模式（示例，不冻结具体 IssueCode）

回执模式	建议 Issue 域
Gate 长期 BLOCK	-COLLAB-（协同阻断）
status = FAILED	-COLLAB-（执行失败）
status = TIMEOUT	-COLLAB-（执行超时）
高频 SKIPPED	-COLLAB-（过度抑制）
attempt_count 异常增长	-PROC-（控制异常）

Issue 的归属模块取决于谁消费回执：
- C 消费 → C-COLLAB-*
- 系统消费 → SYS-*
- B 通常不直接消费执行回执

---

8. Backend / 审计最低能力要求

Backend 必须支持以下最小能力，否则 ER 规范视为未落地：

8.1 回放能力
- 按 decision_id 回放完整链路：

Decision → D2RG → RuntimeGate → ExecutionReceipt

- 支持时间线排序
- 支持 attempt_count 聚合

---

8.2 统计能力（SLO / 运维）

至少支持：
- Gate 阻断率
- 执行成功率
- 执行失败率
- 超时率
- SKIPPED 比例
- 平均 / P95 执行延迟

---

8.3 关联能力

Execution Receipt 必须可关联到：
- AutonomySnapshot（B / C）
- IssueEvent
- 系统版本 / 校准版本

这是事故复盘与责任切割的证据链。

---

9. 安全与合规约束（冻结）

Execution Receipt 禁止包含：
- 用户原始输入
- 音频 / 图像 / 视频
- 可反推出个人身份的信息

仅允许：
- 系统元数据
- 状态 / 枚举 / 数值指标

---

10. 冻结声明（必须写入工程）
1. Execution Receipt 是执行事实的唯一权威
2. 禁止执行链静默执行
3. 禁止上游模块伪造回执
4. 所有自治 / 协同 / 审计判断，必须可追溯到回执

---

11. 一句话系统级总结（封口）

Execution Receipt 将“执行是否发生”从隐式副作用，
提升为系统级、可审计、可聚合的工程事实。

---

至此，整个一期「自治 × 协同 × 执行」闭环已经完整封口：
- 裁决（抽象）
- 适配（D2RG）
- 放行（Runtime Gate）
- 执行（Execution Chain）
- 回执（Execution Receipt）
- 自治 / Issue / Backend

如果你愿意继续，下一步只剩两种收尾级工作（不引入新概念）：
1. 把所有接口串成一张「系统数据流 × 责任边界」文字图
2. 定义一期 MVP 实现清单（哪些必须真做，哪些可空实现）

你选一个，我继续。
