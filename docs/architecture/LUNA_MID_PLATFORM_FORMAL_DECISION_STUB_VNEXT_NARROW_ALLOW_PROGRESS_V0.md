# Luna — Mid-Platform Formal Decision Stub vNext（Narrow Allow-Progress Path）v0

**文件**：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_STUB_VNEXT_NARROW_ALLOW_PROGRESS_V0.md`  
**性质**：Phase-Next-8：formal decision 首次支持 `allow_progress` 的极窄范围升级（只推进到下游占位接口）  

关联：
- 正式裁决层设计冻结：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_LAYER_V0.md`
- formal decision stub v2（结构化原因）：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_STUB_V2.md`
- allow-progress 放行前提（设计冻结）：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_ALLOW_PROGRESS_PRECONDITIONS_V0.md`
- 导航执行前承接层设计冻结：`docs/architecture/LUNA_NAVIGATION_HANDOFF_POST_BOUND_EXECUTION_PLAN_V0.md`
- 导航执行前承接层 stub（只读占位）：`docs/architecture/LUNA_NAVIGATION_HANDOFF_POST_BOUND_EXECUTION_STUB_V0.md`
- 导航执行前承接层 stub 消费契约（只读）：`docs/architecture/LUNA_NAVIGATION_HANDOFF_POST_BOUND_EXECUTION_STUB_CONSUMPTION_PLAN_V0.md`
- 真实执行前最后门控（冻结）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTION_READINESS_GATE_V0.md`

---

## A. 文档定位（写死）

- 这是 formal decision **首次支持 `allow_progress`** 的极窄范围升级文档。
- 当前目标不是全面放行。
- 当前目标：验证“前提满足时，formal decision 有能力推进到下游占位层”。
- 当前不进入真实导航执行。
- 当前不做地图接入。
- 当前不驱动语音/记忆。

---

## B. 为什么现在只允许极窄范围放行

- 已经定义了 allow-progress 的最小前提（`ALLOW_PROGRESS_PRECONDITIONS_V0`）。
- formal decision stub 已具备阻断与等待的结构化原因（v2）。
- 现在可以开始验证：当所有前提满足时，系统能否进入“下一占位层”。
- 但当前仍缺真实执行器、地图、完整中台裁决上下文，因此：
  - 只能做“窄路径放行”
  - 不能做“全面放行”

---

## C. 本轮允许的放行前提（必须全部满足，写死）

本轮 `allow_progress` 必须同时满足（缺一不可）：

1. 安全前提满足  
2. 任务有效性前提满足  
3. 承接链完整性前提满足  
4. 信息充分性前提满足  
5. 分支一致性前提满足（仅允许最小占位判断）

写死：
- 任一前提缺失 → 不允许 `allow_progress`（必须回退到 v2 的 pending/block 逻辑）

---

## D. 本轮允许的放行目标（写死）

- `allow_progress` 只允许推进到：  
  - **导航执行前承接层下游的只读占位接口**

- 不允许直接推进到：  
  - 真实导航执行器  
  - 地图规划器  
  - 语音链  
  - 记忆链

---

## E. 本轮仍不允许做什么（写死）

- 不允许真实启动导航
- 不允许真实切执行链
- 不允许真实 `switch_branch`
- 不允许直接对用户播报“开始导航”
- 不允许把 `allow_progress` 视为执行完成

---

## F. 与现有链路的关系（写死）

- 正式裁决层首次允许推进，但推进目标只是下游占位接口。
- `navigation_handoff_post_bound_execution_stub_v0` 当前可视为：
  - formal decision 放行后的“下一层占位接收位”（仍只读、仍不执行）。
- 如需新增更明确的只读占位结果，也必须保持极小（仅用于证明窄路径存在）。

