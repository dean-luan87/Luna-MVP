# Luna Vision — Mid-Platform Consume Stub v0（中台消费占位：只读承载与观测）

**文件**：`docs/architecture/vision/LUNA_VISION_MID_PLATFORM_CONSUME_STUB_V0.md`  
**性质**：P1-2 中台消费占位设计（只读接住切片；不裁决、不派发、不夺权）  

基于已完成冻结/规范：
- `docs/architecture/vision/LUNA_VISION_CONSUMABLE_SLICE_OUTPUT_SCHEMA_V0.md`
- `docs/architecture/vision/LUNA_VISION_MODULE_ARCHITECTURE_V0.md`
- `docs/architecture/LUNA_PHASE1_EXECUTION_PLAN_V0.md`

---

## A. 文档定位（写死）

- 这是 **P1 的中台消费占位设计**（Vision Mid-Platform Consume Stub v0）。
- 当前只让“中台侧”**接住视角切片**并形成观测结果。
- 当前不做：
  - 中台裁决（不决定该说/该记/该导航）
  - 语音/记忆/导航执行联动
  - Need-Navigation Routing
- 当前只做：**只读承载与观测**（接住、记录、保留、可观察）。

---

## B. 当前问题定义

- 视角模块已经有统一的 Consumable Slice 输出 schema（v0）。
- 但当前缺一个正式的“中台消费入口”来接住这些 slice。
- 如果没有入口：
  - 解释层输出无法稳定接线
  - 中台调度无法落地
  - 快/慢链分流无法形成可回归的接口面

---

## C. consume stub 的最小定义（写死）

consume stub 不是：
- 裁决器
- 任务执行器
- 语音驱动器

consume stub 只是：
- 中台侧的正式接收位
- 作用是：**接住、记录、保留、可观察**

---

## D. consume stub 当前允许接收什么（写死）

- 只接收 **符合 `LUNA_VISION_CONSUMABLE_SLICE_OUTPUT_SCHEMA_V0`** 的：
  - 单个 slice（dict）
  - slice 集合（list[dict]）
- 不接：
  - 原始视频流
  - YOLO/OCR 原始结果（框/原始文本块）
  - 自然语言解释结论

---

## E. consume stub 当前不允许做什么（写死）

- 不允许直接驱动语音
- 不允许直接写记忆
- 不允许直接触发导航
- 不允许修改主链裁决（route/proposal/dispatch_type）
- 不允许把 slice 升格为事实

---

## F. 当前最小输出/观测位（建议）

建议写入：
- `result.metadata["vision_mid_platform_consume_stub_v0"]`

最小结构建议：

```json
{
  "consume_attempted": true,
  "consume_scope": "vision_mid_platform_consume_stub_v0",
  "slice_count": 2,
  "slice_types": ["risk_slice", "ocr_related_slice"],
  "consume_mode": "read_only"
}
```

约束（写死）：
- 不加时间/空间字段
- 不膨胀成复杂调度对象
- 只做中台占位观测

---

## G. 下一步边界（写死）

- 本轮之后，下一步才考虑中台如何基于这些 slice 做真正调度
- 当前先不做 Need-Navigation Routing
- 当前先不做语音候选派发
- 当前先不做记忆候选派发

