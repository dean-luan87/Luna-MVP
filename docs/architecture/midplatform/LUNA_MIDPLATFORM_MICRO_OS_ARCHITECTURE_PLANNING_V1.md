# Luna Midplatform 1.0 — Micro-OS Architecture Planning v1

**Phase**：`Phase-Midplatform-Micro-OS-Architecture-Planning-v1-001`  
**正式形态**：`Luna Midplatform 1.0 = Luna Midplatform Micro-OS Architecture`（中台 1.0 形态）  
**性质**：architecture planning / governance mapping / component placement only

## 阶段定位

本阶段将 Luna 中台正式定义为 **Micro-OS 架构**，即 Luna 内部的信息、任务、模型、模块、驱动、健康度、权限、世界状态、记忆与输出的微型操作系统规划。

本阶段 **不是** 完整 Luna OS 产品化，也 **不是** 设备级操作系统实现；它是中台运行内核的 OS-like architecture planning。

## 核心定义

Luna Midplatform 1.0 在 **L0 Constitution / Governance Kernel** 与 **L8 Health / Watchdog / Recovery Supervisor** 的约束下：

1. 将感知、语音、地图、任务、驱动、世界模型、记忆、系统资源与监管系统的信息 **事件化**
2. 进行 **时空间锚定**
3. 写入 **Working Memory（L3）**
4. 通过 Scheduler、Task Manager、Drive Manager、Information Integration / Allocation（L5–L6）
5. 将信息分配给 Decision Center、Task Chain、Output Gate、Frontend Guidance、Memory Admission、WorldModel Admission 等路径（L7）

## 九层架构 L0–L8

| 层 | 名称 | 职责摘要 |
|----|------|----------|
| L0 | Constitution / Governance Kernel | 全局治理内核，约束 L1–L7 |
| L1 | Hardware / Runtime / Resource Substrate | 资源底座：能不能做、如何降级 |
| L2 | Module Adapter & Input Layer | 模块输出 → standardized_candidate / event |
| L3 | Event Bus & Working Memory Layer | 中台 RAM/cache/queue；≠ Memory/WorldModel |
| L4 | Spatiotemporal World State Layer | 统一时空间坐标组织信息 |
| L5 | Drive / Goal / Task Scheduling Layer | Drive/Task 信号与任务链状态 |
| L6 | Information Integration & Allocation Layer | 模型/规则/算法混合整合与分流 |
| L7 | Decision Context / Output / Memory-WorldModel Bridge | 只输出 candidate/handoff |
| L8 | Health / Watchdog / Recovery Supervisor | 全局监管旁路，监控 L1–L7 |

**注意**：
- L0 不是普通上游模块，而是全局治理内核
- L8 不是普通下游模块，而是全局监管旁路
- WorldModel / Memory 与中台是双向关系：L7 生成 admission candidate；recall 反向进入 L4/L5/L6 作为上下文

## 既有成果归位

本阶段通过 `midplatform_existing_governance_relocation_matrix_v1` 将以下成果归位：

- Constitution / Constitution-Bus / Governance Gate / Validation / Whitebox / Permission / Candidate-Fact → **L0**
- Controlled Runtime / Provider / Model Profile Registry / 资源可用性 → **L1**
- Vision / OCR / ASR / TTS / Map / World Continuity / 传感器 / 用户输入 → **L2**
- Event Bus / Working Memory / Queue / TTL Cache → **L3**
- STCM / Spatiotemporal Consistency / scene slot / world object candidate → **L4**
- Drive / Task Manager / Scheduler / Task Chain → **L5**
- Information Integration / Allocation → **L6**
- Decision Center / Output Gate / Speech Gate / Display Gate / Memory-WorldModel Bridge → **L7**
- Health / Watchdog / Recovery → **L8**

已完成 phase 的 GO 结论 **不被修改**；本阶段只做 architecture relocation。

## 边界条件

- 不启 runtime
- 不调用任何模型
- 不写 Memory / WorldModel
- 不生成真实用户输出
- 不执行真实任务链
- 不修改已有模块 runtime 行为

## 产物

- 代码：`capabilities/midplatform/midplatform_micro_os_architecture_planning_v1.py`
- Run：`tools/evaluation/midplatform/run_midplatform_micro_os_architecture_planning_v1.py`
- Verify：`tools/evaluation/midplatform/verify_midplatform_micro_os_architecture_planning_v1.py`
- 输出：`_tmp_eval_out/midplatform_micro_os_architecture_planning/`

## Final Decision

`MIDPLATFORM_MICRO_OS_ARCHITECTURE_PLANNING_READY_FOR_DRYRUN_AND_REVIEW`

## Recommended Next Phase

`Phase-Midplatform-Micro-OS-Architecture-DryRunAndReview-v1-001`
