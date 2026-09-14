# Luna — Mid-Platform Formal Decision Layer v0（中台正式裁决层：设计冻结）

**文件**：`docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_LAYER_V0.md`  
**性质**：下一阶段首入口（Phase-Next-1）：中台正式裁决层最小设计（可冻结、可回归）  

---

## A. 文档定位（写死）

- 这是 Luna 系统 **中台正式裁决层** 的最小设计文档。
- 当前目标：定义正式裁决层的 **角色、输入、输出、门控、边界**，先解决“谁拥有最终裁决权”。
- 当前不做：
  - 完整中台实现
  - 真实导航执行切换
  - 语音/记忆联动实现
  - 地图接入
- 当前先把“建议/候选/占位结果何时允许进入行动”钉住为统一入口。

---

## B. 为什么现在必须进入正式裁决层

- 当前系统已经积累了多类 **建议层 / 占位层 / 承接层**：
  - 视角切片与候选
  - 导航需求建议与消费占位
  - 导航执行前承接设计与 stub
- 这些层本身都 **不拥有最终执行权**，只能给出候选/建议/状态。
- 若不引入正式裁决层：
  - 真实导航执行、语音派发、记忆写入将缺少合法入口
  - 系统会被迫在各模块边缘“越权接线”
- 因此必须先有正式裁决层，把多路输入收束为：**是否允许进入下一步行动**。

---

## C. 正式裁决层的系统角色（写死）

正式裁决层不是：
- 视角前端（YOLO/OCR/Tracking）
- 解释模型
- 语音模块
- 导航执行器
- 记忆模块

它是：
- 中台主层中唯一拥有 **“正式决策权”** 的层
- 负责把各路建议/候选/承接状态，收束成可执行判断
- 负责决定（正式判定结果）：
  - 是否进入导航链
  - 是否保持在非导航主链
  - 是否阻断
  - 是否挂起/等待

并写死：
- 其他模块只能给 **建议、候选、状态、占位**，不能越权替代正式裁决层。

---

## D. 正式裁决层未来要消费的最小输入集合（只列已存在/已冻结输入面）

> 口径：只定义“可消费输入面”，不做实现细节，不扩太多未来输入。

### D1. 任务链相关（当前部分为占位）

- 当前任务语境（占位）
- 当前任务有效性状态（占位：是否挂起/被覆盖/过期）
- `proposal.task_action`（若存在）

### D2. 视角链相关

- `runtime_context.metadata["vision_consumable_slices_v0"]`
- `runtime_context.metadata["vision_interpretation_candidates_v0"]`
- 视角运行时治理分支未来状态（占位：见视角生命周期治理占位文档）

### D3. 导航建议链相关

- `result.metadata["need_navigation_routing_v0"]`
- `result.metadata["mid_platform_dispatch_consumption_stub_v0"]`（只读消费占位产物，非裁决输入的替代）

### D4. 导航执行前承接链相关

- `result.metadata["destination_bound_v0"]`
- `result.metadata["navigation_handoff_consume_bound_v0"]`
- `result.metadata["navigation_handoff_post_bound_execution_stub_v0"]`

### D5. 安全相关（占位）

- 当前安全状态/抢占状态（占位；未来作为安全门控输入）

门控输入占位与承载位（v0）：
- `docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_GATE_INPUTS_V0.md`

---

## E. 正式裁决层要输出的最小结果集合（收敛为 4 类）

> 口径：这是正式裁决层输出，不是建议层输出；也不等于真实执行器动作。

- **allow_progress**：条件满足，允许进入下一阶段链路（仍需由下游承接层接住）
- **hold_pending**：条件不足但非永久阻断，等待更多信息/条件补齐
- **block_execution**：当前明确不允许继续执行
- **switch_branch**：应切换到另一条链（例如进入导航链，或回到非导航链）

---

## F. 正式裁决前要过的最小门控类别（只写门类与原则，不做实现）

1. **安全门控**  
   - 风险过高时，其他建议不得越权放行。
2. **任务有效性门控**  
   - 任务已过期/被覆盖/挂起时，不得继续推进。
3. **分支一致性门控**  
   - 建议进入哪条链，与当前链路状态是否一致；不一致时需 pending 或阻断（占位语义）。
4. **信息充分性门控**  
   - 是否具备推进所需的最小信息；不足则 hold_pending。
5. **承接链完整性门控**  
   - 例如进入导航执行前，是否已经具备：
     - `destination_bound_v0`（bound fact）
     - `navigation_handoff_consume_bound_v0`（handoff consume bound）
     - `navigation_handoff_post_bound_execution_stub_v0`（执行前承接状态占位）

承接链完整性门控输入（v0，占位与只读承接）：
- `docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_HANDOFF_GATES_V0.md`

信息充分性门控输入（v0，最小设计/占位）：
- `docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_INFORMATION_GATES_V0.md`

allow-progress 最小放行前提（v0，设计冻结；不等于实现放行）：
- `docs/architecture/LUNA_MID_PLATFORM_FORMAL_DECISION_ALLOW_PROGRESS_PRECONDITIONS_V0.md`

---

## G. 谁不能替代正式裁决层（必须写死）

以下都不能直接替代正式裁决层：
- `need_navigation_routing_v0`
- `mid_platform_dispatch_consumption_stub_v0`
- `destination_bound_v0`
- `navigation_handoff_consume_bound_v0`
- `navigation_handoff_post_bound_execution_stub_v0`
- 视角 slice（例如 `vision_consumable_slices_v0`）
- 解释候选（例如 `vision_interpretation_candidates_v0`）
- 语音 response template
- 局部分支的建议信号（任何“看起来应该执行”的旁路信号）

---

## H. 与各模块的关系（写死）

- **与视角链**：视角链提供输入候选与状态；不拥有裁决权。  
- **与解释/纠偏层**：解释层提供更可信候选与重识别建议；不拥有裁决权。  
- **与任务链**：任务链提供任务状态/优先级/有效性；正式裁决层据此决定是否推进。  
- **与导航链**：正式裁决层决定是否允许进入导航链；导航链仍有执行前承接与执行层。  
- **与语音链**：未来可成为语音候选的上游来源；当前不直接驱动语音。  
- **与记忆链**：未来可决定哪些结果允许进入记忆消费；当前不直接写记忆。  

---

## I. 当前不做（写死）

- 不做完整中台实现
- 不做真实导航执行切换
- 不做语音联动实现
- 不做记忆联动实现
- 不做地图接入
- 不做跨会话任务缓存恢复实现
- 不做视角生命周期治理真实运行时实现
- 不做规则/模型混合裁决器实现

---

## J. 下一步边界（写死）

- 本轮之后，下一步才考虑：
  1) 正式裁决层的只读 stub  
  2) 再把某一类裁决结果接到真实链路  
- 当前不跨这两步。

---

## K. 未来最小 stub 输出位建议（仅方向说明，不落代码）

建议未来只读占位输出：
- `result.metadata["mid_platform_formal_decision_stub_v0"]`

示例结构（占位）：

```json
{
  "decision_attempted": true,
  "decision_scope": "mid_platform_formal_decision_stub_v0",
  "decision_result": "hold_pending",
  "reason": "missing_required_gate_inputs"
}
```

