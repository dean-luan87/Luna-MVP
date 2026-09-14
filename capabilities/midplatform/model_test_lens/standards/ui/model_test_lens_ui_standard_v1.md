# Model Test Lens UI Standard V1

Phase: `Phase-P1-Midplatform-Model-Test-Lens-Perception-HUD-UI-Standardization-Planning-v1-001`  
Status: **Planning only** — standard definition, no page changes.

## 统一目标

所有 Model Test Lens 模型测试页面的默认目标：

> **让人看懂模型如何看世界、如何判断、哪里不确定、下一步怎么补测。**

禁止退回到：指标表优先、JSON 优先、artifact path 优先、manifest/job/bridge 优先。

## 信息层级（Level 1–6）

| Level | 名称 | 内容 |
|-------|------|------|
| L1 | Simple Mode | 选文件、选类型、开始测试、进度、结论 |
| L2 | Visual Compare View | 左原图 / 右模型结果 |
| L3 | Perception HUD View | 机器人视角标注 + 推理面板 |
| L4 | Metrics | ATE / IoU / WER / confidence 等（排在 HUD 之后） |
| L5 | Advanced Mode | manifest / job / runner bridge / TestBoard refs |
| L6 | Developer Mode | raw JSON / paths / phase_ref |

## 默认展示顺序

1. 测试结论
2. 原图 / 模型结果对比
3. Robot Vision HUD
4. 系统观察
5. 系统推理
6. 不确定性 / 可能漏检
7. 建议补测
8. 指标
9. 高级流程
10. 开发者信息

## 模式切换

- 简洁模式（默认）
- 机器人视角 HUD（有图像/视频结果时推荐）
- 指标模式
- 高级模式
- 开发者模式

## 统一文案

**使用**：我看到了 · 我判断 · 我不确定 · 可能漏掉 · 建议补充测试 · 需要人工复核

**避免（默认）**：envelope · artifact_ref · adapter · phase_ref · semantic layer · fact layer

## 统一边界声明

「当前结果仅用于模型测试，不会写入事实层，也不会触发导航或语音输出。」

## 后续页面强制引用

新模型测试页面必须先检查：

1. Model Test Lens UI Standard V1
2. **Luna Observation Lens V1 Template Standard**（默认 UI 壳）
3. Perception HUD UI Template Standard V1
4. Per-model HUD Adapter Requirements V1
5. `luna_observation_lens_v1_model_adapter_slot_contract.json`

不得重新设计一套独立页面。V1 Closure 后 UI 主体不再推倒重来；新模型仅扩展 adapter slot。
