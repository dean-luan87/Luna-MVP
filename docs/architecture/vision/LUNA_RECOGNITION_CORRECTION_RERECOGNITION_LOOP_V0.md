# Luna Vision — Recognition → Correction → Re-recognition Loop v0（最小占位接线）

**文件**：`docs/architecture/vision/LUNA_RECOGNITION_CORRECTION_RERECOGNITION_LOOP_V0.md`  
**性质**：P2-3 最小闭环占位设计（可运行、可观察、可回归；不进入真实执行）  

关联冻结协议：
- P2-1 解释/纠偏层候选协议：`docs/architecture/vision/LUNA_VISUAL_INTERPRETATION_AND_CORRECTION_OUTPUT_V0.md`
- P1 可消费切片 schema：`docs/architecture/vision/LUNA_VISION_CONSUMABLE_SLICE_OUTPUT_SCHEMA_V0.md`
- P1-2 中台 consume stub：`docs/architecture/vision/LUNA_VISION_MID_PLATFORM_CONSUME_STUB_V0.md`

---

## A. 文档定位（写死）

- 这是 **P2-3 的最小闭环占位设计**。
- 当前目标：让纠偏循环在主线中有正式位置与可观测输出。
- 当前不做：
  - 真实重识别执行（不触发 OCR/YOLO 重跑）
  - 中台裁决
  - 真实轻量模型代码接入

---

## B. 当前最小闭环定义（本轮打通链路）

本轮打通链路（只打一跳）：

**已有视觉候选 / slice（上游输入）**  
→ **纠偏判断占位（极保守规则）**  
→ 产出 **`needs_rerecognition_candidate`**（符合 P2-1 协议）  
→ 写入 `runtime_context.metadata["vision_interpretation_candidates_v0"]`（只读承载位）  
→ **中台 consume stub** 观测到并写入 `result.metadata["vision_mid_platform_consume_stub_v0"]`

注意：
- 这不是完整纠偏系统
- 只是一期最小闭环占位链（可观察、可回归、不可夺权）

---

## C. 本轮选定的上游输入（只选 1 种）

**选定**：`risk_slice`（来自 `runtime_context.metadata["vision_consumable_slices_v0"]`）

理由：
- 已有 P1-3 最小 wiring 可稳定产出 `risk_slice`
- 输入结构清晰、最容易收敛
- 更适合作为“高价值但可能需再确认/再识别”的占位逻辑起点

---

## D. 本轮接线边界（写死）

- 本轮只产出 `needs_rerecognition_candidate`
- 不触发真实重识别
- 不触发联网补证
- 不驱动语音
- 不写记忆
- 不激活导航
- 不改主链 route/proposal/dispatch_type
- 不把候选升格为事实

---

## E. 当前最小验证口径（写死）

- 至少一种已有输入（`risk_slice`）能转成 `needs_rerecognition_candidate`
- consume stub 能观测到它（candidate_type 可见）
- 主链其余行为不变
- `tools/verify_voice_v1_minimal_flow.py` 回归不坏

---

## 本轮硬约束（继续成立）

### No Fabrication Rule
- 不允许系统编造“需要重识别”的事实依据
- 只能基于已有上游输入产出候选
- 无有效输入就不写（relevant-only）

### 统一时空锚点原则
- 本轮不新增任何模块自造的时间/空间字段
- 如未来需要时空关联，只能引用统一锚点（本轮不展开）

