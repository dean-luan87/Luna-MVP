# Luna — Navigation Executor Takeover Wiring Minimal Implementation v0（takeover → executor skeleton 接线：最小实现版）

**文件**：`docs/architecture/LUNA_NAVIGATION_EXECUTOR_TAKEOVER_WIRING_IMPLEMENTATION_V0.md`  
**性质**：Step 5a：Navigation Executor Takeover Wiring Minimal Implementation v0（把接线边界推进到最小非动作实现）  

关联：
- takeover → executor skeleton 接线边界（冻结）：`docs/architecture/LUNA_NAVIGATION_EXECUTOR_TAKEOVER_WIRING_V0.md`
- 执行器本体模块骨架（不可执行）：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_MINIMAL_MODULE_SKELETON_V0.md`
- 输入对象实现版：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_INPUT_OBJECT_IMPLEMENTATION_V0.md`
- 状态对象实现版：`docs/architecture/LUNA_NAVIGATION_REAL_EXECUTOR_STATUS_OBJECT_IMPLEMENTATION_V0.md`
- 监控闭环实现版：`docs/architecture/LUNA_EXECUTION_MONITORING_MINIMAL_LOOP_IMPLEMENTATION_V0.md`

---

## A. 文档定位（写死）

- 这是 takeover → executor skeleton 接线的**最小实现版**文档。
- 当前目标：把接线边界推进到**非动作实现**（最小可运行接线），让 skeleton 进入安全接线态。
- 当前不做真实动作执行。
- 当前不做地图接入。
- 当前不做语音联动。
- 当前不做中台真实治理动作。
- 当前不改变既有裁决边界（formal decision/readiness/takeover 仍只作为前提证据，不被替代）。

---

## B. 为什么现在要先实现接线而不是动作

- 前置对象链与监控闭环最小实现已在位（输入对象 implemented、状态对象 implemented、监控对象 implemented、skeleton 存在）。
- 若接线不推进到最小实现，这些对象链仍停在“文档最后一跳”，无法形成可回归的接线事实。
- 但当前仍不具备进入真实动作执行的条件（禁止地图/动作/治理/语音联动）。
- 因此只能先实现“接到 executor skeleton 的安全态”，证明接线边界可运行且不越权。

---

## C. implemented wiring 的最小定义（写死）

- 它不是动作执行。
- 不是 takeover 授权本身。
- 不是 formal decision。
- 它是“把合法接线前提落实为 executor skeleton 安全接线态”的最小实现：
  - 产出统一接线结果对象
  - 可选调用 skeleton 的接线接口（仍为 no-op/非动作）

---

## D. 当前最小输入依据（写死 8 条，缺一不可）

接线必须满足 8 条前提（缺一不可）：

1) `mid_platform_formal_decision_stub_v0.decision_result == "allow_progress"`
2) `formal_decision_allow_progress_path_v0.downstream_placeholder_interface == "navigation_handoff_post_bound_execution_stub_v0"`
3) 下游 post-bound consumption 已进入“可继续推进占位阶段”
4) `navigation_real_execution_readiness_gate_stub_v0.readiness_status == "ready_candidate"`
5) `navigation_executor_takeover_stub_v0.takeover_status == "ready_to_takeover"`
6) implemented `navigation_real_executor_input_v0` 已存在
7) implemented `navigation_real_executor_status_v0` 已存在
8) implemented `navigation_execution_monitoring_status_v0` 已存在

并写清：

- 缺任一项则不接线
- 不允许脑补
- 这些是接线前提，不是动作执行授权

说明（当前仓库的保守落地口径）：

- 第 3 条目前以 `navigation_handoff_post_bound_execution_stub_v0.execution_state == "execution_pending"` 作为“已进入可继续推进占位阶段”的保守证据（当前尚未有独立 consumption 对象）。

---

## E. 当前最小输出位（写死）

固定写入：

- `result.metadata["navigation_executor_takeover_wiring_v0"]`

最小结构：

```json
{
  "wiring_attempted": true,
  "wiring_scope": "navigation_executor_takeover_wiring_v0",
  "wiring_status": "wired_inactive|wired_ready_to_takeover|blocked|not_applicable",
  "reason": "..."
}
```

约束（写死）：

- 不加时间/空间字段
- 不膨胀成复杂对象
- 只表达“接线是否成立，以及 skeleton 被带入哪种安全态”

---

## F. 当前最小安全状态落实（写死）

接线成功后，skeleton 最多只能进入：

- `wired_inactive`
- `wired_ready_to_takeover`

禁止进入：

- `active`
- `running`
- `executing`

并写死：

- `wired_ready_to_takeover` 不是动作开始
- `wired_inactive` 也不是失败，只是更保守的接线态
- 当前默认应优先保守，不要激进

---

## G. 接线层最小职责（写清）

接线层只负责：

- 校验 8 条前提
- 调用 executor skeleton 的最小接线接口（可选，仍为非动作）
- 让 skeleton 进入安全接线态
- 产出统一接线结果

接线层不负责：

- 触发真实动作
- 触发地图规划
- 触发语音播报
- 驱动中台治理动作
- 决定继续/中断/回退

---

## H. 当前不允许做什么（写死）

- 不允许真实导航动作执行
- 不允许真实地图接入
- 不允许真实语音启动
- 不允许真实中台治理动作
- 不允许把 `wired_ready_to_takeover` 当执行开始
- 不允许绕过后续回退/中断治理入口

---

## I. 落地位置（实现落点）

- builder：`capabilities/mid_platform/runtime/navigation_executor_takeover_wiring_v0.py`
- metadata 聚合写入：`capabilities/voice/runtime/voice_final_text_dispatcher.py`
- skeleton 接线接口（非动作）：`capabilities/navigation/runtime/navigation_real_executor_v0.py`

