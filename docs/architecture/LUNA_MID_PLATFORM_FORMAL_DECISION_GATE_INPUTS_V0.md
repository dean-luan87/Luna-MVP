# Luna — Mid-Platform Formal Decision Gate Inputs v0（正式裁决层门控输入：设计/占位）

**文件**：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_GATE_INPUTS_V0.md`  
**性质**：Phase-Next：正式裁决层门控输入最小设计（先补输入面，不改执行行为）  

关联：
- 正式裁决层设计冻结：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_LAYER_V0.md`
- 正式裁决层只读 stub：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_STUB_V0.md`

---

## A. 文档定位（写死）

- 这是正式裁决层门控输入的最小设计文档。
- 当前目标：补齐两类门控输入面：
  1) **安全门控输入**  
  2) **任务有效性 / 挂起状态输入**
- 当前不做完整门控实现，不改变真实执行行为。

---

## B. 为什么现在必须补门控输入

- 当前正式裁决 stub 之所以只能 `hold_pending`，不是因为裁决层不存在，而是因为缺少关键门控输入。
- 若不先补齐“安全”和“任务有效性”两类上游输入，正式裁决层无法开始具备条件化判断能力（只能永远保守）。
- 因此本轮优先把输入面与落点钉住，后续再逐步把它们接入裁决逻辑。

---

## C. 安全门控输入最小定义（语义，不展开实现）

建议未来承载位（占位）：
- `runtime_context.metadata["safety_gate_v0"]`

最小字段：
- **safety_gate_present**：bool（是否存在安全门控输入）
- **safety_status**：`safe | guarded | blocked`（最小集合）
- **safety_preempt_active**：bool（是否处于安全抢占状态）

写死：
- 若安全输入缺失，正式裁决层不得脑补，只能继续保守。

---

## D. 任务有效性 / 挂起状态最小定义（语义，不展开实现）

建议未来承载位（占位）：
- `runtime_context.metadata["task_validity_v0"]`

最小字段：
- **task_validity_present**：bool（是否存在任务有效性输入）
- **task_validity_status**：`active | suspended | expired | overridden`（最小集合）

写死：
- 若任务有效性输入缺失，正式裁决层不得脑补，只能继续保守。

---

## E. 这两类门控输入未来来自哪里（分层说明，占位）

- **安全门控输入**：未来来自安全模块 / 风险中心 / 抢占状态（系统级来源）
- **任务有效性输入**：未来来自任务链 / Task Hub / Task Cache / Suspension Watcher（系统级来源）

写死：
- 本节只做来源分层说明，不在本轮落实现。

---

## F. 当前最小消费边界（写死）

- 正式裁决层可读这两类门控输入。
- 视角链、解释层、导航链 **不能**直接伪造它们。
- 语音链 **不能**生成它们。
- 本轮仅允许：只读承接或占位约定。

---

## G. 当前不做（写死）

- 不做安全模块实现
- 不做任务挂起治理实现
- 不做任务缓存恢复实现
- 不做真实 formal decision 规则升级
- 不做真实导航执行放行

---

## H. 下一步边界（写死）

- 本轮之后，下一步才考虑把这两类门控输入接到 formal decision stub。
- 再之后才考虑让 formal decision stub 从 `hold_pending` 变成条件化输出（例如允许输出 `block_execution` 等）。

