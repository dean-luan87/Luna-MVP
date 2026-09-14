# Luna — Formal Decision Information Sufficiency Gates v0（信息充分性门控：设计/占位）

**文件**：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_INFORMATION_GATES_V0.md`  
**性质**：Phase-Next-5：正式裁决层“信息充分性门控”最小设计（先占位，不改裁决行为）  

关联：
- 正式裁决层设计冻结：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_LAYER_V0.md`
- formal decision stub v1：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_STUB_V1.md`
- 门控输入（安全/任务有效性）：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_GATE_INPUTS_V0.md`
- 承接链完整性门控：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_HANDOFF_GATES_V0.md`

---

## A. 文档定位（写死）

- 这是正式裁决层“**信息充分性门控**”的最小设计文档。
- 当前目标：定义执行推进前，信息是否足够的门控输入（作为正式裁决层可消费输入面）。
- 当前不做真实门控实现；当前不改变 formal decision stub v1 的最保守输出边界。

---

## B. 为什么现在必须补“信息充分性门控”

- 当前 formal decision stub v1 已能处理：
  - 安全阻断
  - 任务无效阻断
- 当前已占位：
  - 承接链完整性门控（用于解释“承接链是否准备好”）
- 但仍无法区分：
  - 承接链齐了但信息还不够（例如缺最小动作参数/语境缺失）
  - vs 已具备进入下一阶段判定所需的最低信息
- 因此必须补一类新的门控输入：**信息充分性门控**，用于解释“为什么 pending（信息不足）”。

---

## C. 最小门控输入集合（只定义最小集合）

建议 `formal_decision_information_gates_v0` 最小字段：
- **info_gate_present**：bool
- **task_context_present**：bool
- **required_action_inputs_present**：bool
- **candidate_inputs_present**：bool
- **info_sufficiency_status**：`insufficient | ready_candidate | blocked`
- **consume_mode**：固定 `read_only`

注意（写死）：
- 当前不做 `ready_candidate -> allow_progress`
- 这里只定义语义与占位输出

---

## D. 这类门控输入未来来自哪里（来源说明，占位）

信息充分性门控未来应来自“正式裁决层可消费的最小上游来源”，例如：
- 当前任务语境 / `proposal.task_action`
- 当前承接链相关状态（bound/consume-bound/post-bound stub）
- 当前是否已有推进所需的最小动作参数（例如进入导航链前的最小动作输入，占位）
- 当前是否已有足以支持下一步判断的 candidate / bound / stub 状态

写死：
- 这些不是新建世界模型输入
- 也不是地图输入
- 只是正式裁决层判断“信息够不够”的最小来源整理

---

## E. 最小门控原则（写死）

1. 当前任务语境缺失 → `info_sufficiency_status = "insufficient"`
2. 当前推进所需最小动作参数缺失 → `info_sufficiency_status = "insufficient"`
3. 当前候选/承接状态不足以支持下一步判断 → `info_sufficiency_status = "insufficient"`
4. 即使上述都存在，当前也只能先认为是 `ready_candidate`，不是直接放行执行
5. 若未来发现信息内部存在明确冲突或阻断原因，可标记为 `blocked`（本期仅占位，不实现）

---

## F. 与 formal decision stub 的关系（写死）

- 本轮先定义并占位这类门控输入。
- 本轮不要求 formal decision stub v1 立刻消费它。
- 下一步才考虑 formal decision stub v2/vNext 如何读取它（用于解释 pending 原因）。
- 即使后续读取，也不等于立即放行。

---

## G. 当前不做（写死）

- 不做真实信息充分性算法
- 不做真实放行
- 不做真实导航执行
- 不做地图接入
- 不做跨链自动切换
- 不做缺失信息自动补全

---

## H. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  - 把这类门控输入接到 formal decision stub 下一版
- 再之后才考虑：
  - formal decision 是否允许极窄范围 allow_progress
- 当前不跨这两步

