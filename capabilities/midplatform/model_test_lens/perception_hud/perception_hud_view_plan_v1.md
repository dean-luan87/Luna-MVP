# Perception HUD View — Planning V1

Phase: `Phase-P1-Midplatform-Model-Test-Lens-Perception-HUD-View-Planning-v1-001`  
Status: **Planning only** — no page implementation, no model execution.

## 1. 核心定义

**Perception HUD View**（机器人视觉 HUD / 第一视角感知解释层）是 Model Test Lens 的**解释型展示层**。

它回答五个问题：

1. 画面里有什么？
2. 每个东西在哪里？
3. 和当前任务有什么关系？
4. 系统哪里不确定？
5. 系统建议下一步做什么（补测方向）？

**不是**：模型执行层、事实层、runtime 层、导航指令层。

## 2. 与现有视图关系

```
Simple Mode
  → Visual Compare View（左原图 / 右模型结果）
  → Perception HUD View（机器人视角 + 推理面板）  ← 本规划
  → Insight / Metrics
  → Advanced / Developer
```

- Visual Compare View **保留**
- HUD 作为「**机器人视角**」模式，用户可在「普通对比 / 机器人视角 HUD」间切换
- 不得删除 Simple Mode、Overlay、Compare、Insight、Debug

## 3. 默认布局

### Desktop 三栏（优先）

| 左 | 中 | 右 |
|----|----|-----|
| 原图 | 机器人视觉 HUD 图 | 系统观察 / 推理 / 建议 |

### Desktop 双栏

- 左：原图
- 右：HUD 图 + 浮动推理面板

### 小屏

- 上：HUD 图
- 下：观察 / 推理 / 建议面板

## 4. HUD 主画面要素

底图 + 叠加层：

- Object boxes / Segmentation masks / OCR text boxes
- Keypoints / Trajectory hints
- 空间标签：left / right / front / near / far / on_path / off_path
- 任务相关性：relevant / possible_risk / background / needs_confirmation
- 不确定性：low_confidence / boundary_uncertain / occluded / missing_depth / missing_tracking / missing_ocr
- 风险标记：watch / caution / blocked / unknown

## 5. Reasoning Panel（五块）

1. **当前任务** — task_name, task_goal, test_mode=true
2. **系统观察** — observed_entities, detected_regions, scene_context
3. **系统推理** — reasoning_steps, evidence_refs, missing_inputs
4. **主要风险 / 缺失** — missing_objects, low_confidence, false positive/negative, model_limitations
5. **建议** — next_observation, recommended_model, recommended_followup_test, human_review_required

**文案约束**：使用「测试观察 / 候选判断 / 需要确认 / 建议补充测试」，禁止写成事实、导航指令、行动命令。

## 6. Schema

| Schema | 路径 |
|--------|------|
| Scene Annotation | `schemas/perception_hud/perception_hud_scene_annotation_schema_v1.json` |
| Reasoning Panel | `schemas/perception_hud/perception_hud_reasoning_panel_schema_v1.json` |
| Overlay Layer | `schemas/perception_hud/perception_hud_overlay_layer_schema_v1.json` |

## 7. MobileSAM 适配

MobileSAM 仅提供 **segmentation mask + prompt label**：

- 显示「识别区域 / 分割区域」
- **不能**独立证明语义类别
- label 标注为 `prompt_label`，**不得**升级为 fact label
- 置信低 → 显示「需要确认」
- 建议补充 detection / OCR / depth runner

示例观察：

- 建筑区域：较稳定
- 道路区域：边界需复核
- 车辆候选：置信较低，需 detection 复核
- 路牌候选：需 OCR/detection 辅助

## 8. 未来模型适配（规划预留）

| 模型 | HUD 能力 |
|------|----------|
| Detection / YOLO | box, class, confidence, missed object warning |
| OCR | text box, recognized text, reading order, unclear warning |
| SLAM | keypoints, tracking lost, trajectory minimap, drift risk |
| Depth | heatmap, near/far legend, uncertainty |
| ASR/TTS/Speaker/VLM | 见 UI Standardization 文档 |

## 9. Task Context（第一版）

- `general_scene_understanding`
- `street_navigation_test`
- `crossing_road_test`
- `find_object_test`
- `find_text_test`
- `indoor_navigation_test`
- `model_quality_review`

本阶段只规划 task_context 对 relevance / risk 标记的影响规则，不做真实任务推理。

## 10. 边界

| 允许 | 禁止 |
|------|------|
| 读取 envelope / annotations | 执行模型 / inference |
| Canvas 展示 / 本地 8787 读图 | 写 fact / semantic / registry |
| 透明度 / 图层开关 | 导航 / 语音 / output adapter |
| 测试观察文案 | external URL / live camera / mic |

默认文案：「当前结果仅用于模型评估，不会写入事实层，也不会触发导航或语音输出。」

## 11. 后续执行路线

1. Visual Compare View（已完成）
2. **Perception HUD View Execution**（下一执行阶段）
3. Task-aware HUD
4. Luna Runtime HUD（未来，非本测试系统）
