B Autonomy Snapshot & Backend Reporting 接口规范

B-ASR (B Autonomy Snapshot & Reporting)
Version: 1.0
Status: Frozen（运行时强约束）

---

0. 设计定位（先写死）
- ASR 是上报接口，不是控制接口
- 只读、单向、不可回调
- 不参与实时裁决
- 是自治系统的“事实记录层”

一句话定义：
ASR 负责“如实汇报”，不负责“当场处理”。

---

1. 架构位置（不可变）

B Module
  ├─ Issue Emitter
  ├─ Autonomy State Aggregator
  └─ ASR Client
        ↓
Autonomy Backend
  ├─ Snapshot Store
  ├─ Issue Event Store
  ├─ Timeline / Analytics
  └─ Audit & Replay

---

2. 上报对象总览（两类，缺一不可）

ASR 必须上报以下两类数据，且语义分离：
1. 自治快照（Snapshot） —— 当前“状态”
2. 自治事件（Issue Event） —— 发生过的“事实”

---

3. 自治快照接口（Snapshot）

3.1 Snapshot 上报时机（冻结）

必须在以下时机上报：
- B_OverallState 发生变化
- 子状态发生变化（PROC / OUT / COLLAB）
- 周期性心跳（低频）

❗ Snapshot 是“状态面”，不是日志流。

---

3.2 B_AutonomySnapshot 结构

struct B_AutonomySnapshot {
  uint64_t module_instance_id;
  Timestamp timestamp;

  // Overall
  B_OverallState overall_state;

  // Sub-states
  InternalProcessState internal_process;
  OutputQualityState output_quality;
  CollaborationState collaboration;

  // Context
  uint64_t reference_id;
  uint64_t calibration_version;
  SystemMode system_mode;

  // Active Issues (IDs only)
  std::vector<IssueCode> active_issues;
};

冻结规则：
- Snapshot 不包含 Issue 详情
- Snapshot 必须自洽（状态 ↔ issue 不矛盾）
- Snapshot 是覆盖式，不是增量

---

3.3 Snapshot 上报接口

void report_snapshot(const B_AutonomySnapshot& snapshot);

---

4. 自治事件接口（Issue Event）

4.1 Issue Event 上报原则（冻结）
- 每一个 Issue 触发 / 升级 / 恢复都必须上报
- Issue Event 是时间序列事实
- 不允许合并、不允许覆盖

---

4.2 AutonomyIssueEvent 结构

struct AutonomyIssueEvent {
  IssueCode issue_code;
  IssueLevel level;
  IssueDomain domain;     // PROC / OUT / COLLAB
  IssueScope scope;       // INTERNAL / COLLAB

  Timestamp timestamp;
  uint64_t module_instance_id;

  // Optional context
  uint64_t reference_id;
  uint64_t calibration_version;

  IssueEventType event_type; // RAISED | UPDATED | CLEARED
  std::string description;   // 可读，但不参与逻辑
};

---

4.3 Issue Event 上报接口

void report_issue_event(const AutonomyIssueEvent& event);

---

5. Snapshot 与 Issue 的一致性约束（非常重要）

冻结一致性规则
1. Snapshot 中的 active_issues
- 必须是当前未 CLEARED 的 IssueCode 集合
2. Snapshot 的子状态
- 必须可由 active_issues 聚合得到
3. Snapshot 的 overall_state
- 必须与 State → Action 表一致

后台可以、也应该做一致性校验。

---

6. 上报可靠性与降级策略

6.1 上报失败处理（冻结）
- 上报失败 不得影响 B 模块运行
- 不得阻塞自治逻辑
- 允许：
- 本地缓存
- 延迟重试
- 批量补发

---

6.2 丢失容忍度
- Snapshot：允许丢失（下一次覆盖）
- Issue Event：不允许丢失

Issue Event 是审计证据。

---

7. Backend 最小能力假设（对齐接口）

Backend 必须支持：
- 按 module_instance_id 聚合
- 按时间线重放 Issue → State
- 快照对齐 Issue
- 导出审计报告

ASR 不假设 Backend 的分析策略。

---

8. 安全与合规（最低要求）
- 上报数据 不得包含用户隐私
- 不得包含原始输入内容
- 仅限系统与自治元数据

---

9. 接口冻结声明
- ASR 为 自治观测接口
- 不允许在 B 模块内绕过
- 不允许将 ASR 作为控制通道
- 后续版本只允许 向后兼容扩展

---

一句话工程总结（可写在文档首页）

B 自治 Snapshot 与 Issue Event 上报接口，通过将自治状态与问题事实严格分离，
为系统提供可回溯、可审计、可运营的自治观测能力，
而不干扰任何实时决策路径。

---

到这里，你已经完整具备 B 模块自治的四大件：
1. Issue 目录
2. 状态机
3. State → Action
4. 心跳 + 上报

这是一个可以直接交给工程团队落地的自治系统。

如果继续，逻辑上只剩两个方向：
- C 模块自治（完全复用这套范式）
- 后台自治分析与运营视图（SLO / MTBF / 风险分布）

你选一个，我直接展开。
