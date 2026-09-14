# Luna Observation Lens — UI Redesign Plan V1

Phase: `Phase-P1-Midplatform-Model-Test-Lens-Luna-Observation-UI-Redesign-Planning-v1-001`  
Status: **Planning only** — no page implementation, no model execution.

## 1. 核心目标

将 Model Test Lens 默认 UI 从**工程化表单/后台工具**改造为 **Luna Observation Lens / Luna 运行观察窗口**：

> 用户进入后第一感觉是「我要看 Luna 怎么看世界」，而不是「我要配置什么」。

**内部模块名**保留 `Model Test Lens`；**默认用户界面**使用 `Luna Observation Lens`。

| 维度 | 现在（待改） | 目标 |
|------|-------------|------|
| 首屏感受 | 配置 manifest / job / bridge | 观察画面 + HUD + Luna 解释 |
| 主视觉 | 表单居中 | 中央观察画面最大化 |
| 右侧 | 说明 / 工程 badge | Luna 观察 / 推理 / 建议 |
| 左侧 | 模型目录（工程词） | 能力卡片（可测试 / 实验中 / 未接入） |
| 底部 | 散落指标 | 折叠：指标 / 高级流程 / 开发者 |

## 2. 重新命名

| 元素 | 文案 |
|------|------|
| 页面标题 | **Luna Observation Lens** |
| 副标题 | 查看 Luna 如何看见、标注、判断和解释当前画面 |
| 状态条 | Candidate-only · 非 Runtime（简化一行） |

## 3. 默认四区布局

```
┌────────────────────────────────────────────────────────────┐
│ Luna Observation Lens     Candidate-only · 非 Runtime       │
│ [选择图片/视频] [开始观察] [原图|对比|机器人视角] [高级][开发者]│
├──────────────┬──────────────────────────────┬──────────────┤
│ 能力卡片      │      中央观察画面（最大）      │ Luna 解释面板  │
├──────────────┴──────────────────────────────┴──────────────┤
│ 进度时间线 · [评估指标] [高级流程] [开发者信息]（默认折叠）   │
└────────────────────────────────────────────────────────────┘
```

详见 `luna_observation_lens_layout_spec_v1.json`、`luna_observation_lens_component_spec_v1.json`。

## 4. 中央观察区 — 三种模式

默认优先：**机器人视角 HUD**。

| 模式 | 说明 |
|------|------|
| 原图 | 只看输入画面 |
| 普通对比 | 左原图 / 右模型结果 |
| 机器人视角 | 大图 + 框/mask/标签/风险/气泡 + 右侧推理 |

无文件时占位：「选择图片或视频，Luna 会在这里显示它看到的内容。」

## 5. 右侧 Luna 解释面板（固定五块）

1. 当前任务  
2. 我看到了什么  
3. 我为什么这么判断  
4. 我不确定什么  
5. 建议下一步怎么测  

复用 Perception HUD Reasoning Panel 语义；UI 品牌改为「Luna 观察面板」。

## 6. 左侧能力卡片

分组：**视觉能力** · **声音能力** · **综合理解**

状态仅三种：**可测试** · **实验中** · **未接入**

禁止默认显示：`placeholder` · `active_example_available` · `model_category` · `runner_type` · `adapter`

## 7. 底部折叠区

| 折叠页 | 内容 |
|--------|------|
| 评估指标 | 结论、分数、主要问题、失败模式 |
| 高级流程 | manifest、job、runner bridge、TestBoard、candidate boundary |
| 开发者信息 | raw envelope、JSON、artifact path、phase_ref、trace |

默认全部折叠。

## 8. 默认用户流程

1. 选择图片或视频  
2. 选择能力  
3. 点击「开始观察」  
4. 查看机器人视角 HUD  
5. 查看 Luna 解释  
6. 按需展开指标或开发者信息  

内部仍通过 8787 runner bridge 执行；用户**不得**手动 manifest / job / bridge。

## 9. 默认隐藏词

manifest · job request · runner bridge · candidate_output · visualization_layers · adapter · artifact_ref · phase_ref · workflow phase · expected_envelope · semantic layer · fact layer

仅出现在**高级流程**或**开发者模式**。

## 10. 视觉风格

- 深色 HUD / 科幻观察窗口  
- 中央画面最大化  
- 风险：橙色 · 不确定：黄色 · 可用：绿色  
- 禁止默认大面积 JSON  

## 11. 与白盒窗口关系（占位）

本阶段只规划 UI slot，不接 runtime：

- 白盒链路 · 证据链 · 决策链 · trace · TestBoard  

## 12. 与现有实现关系

| 保留（折叠或高级） | 提升为默认主视觉 |
|-------------------|-----------------|
| Simple Mode 一键流程 | 顶部「开始观察」 |
| Visual Compare | 普通对比模式 |
| Perception HUD | 机器人视角（默认） |
| Insight / Metrics | 底部评估指标折叠 |
| Runner Bridge / Import | 高级流程折叠 |
| Debug Mode | 开发者信息折叠 |

## 13. 治理边界

- 页面不执行模型；执行仅由 `127.0.0.1:8787` local runner bridge  
- 不写 fact / semantic / registry  
- 不触发 navigation / action / speech  
- 不调 output adapter  
- 不访问外部网络 / live camera / microphone  
- 不删除 artifact / TestBoard  

## 14. 后续执行阶段

`Phase-P1-Midplatform-Model-Test-Lens-Luna-Observation-UI-Redesign-Execution-And-Post-Review-v1-001`

目标：真正替换当前 `static_site/` 工程化布局，而非在表单上打补丁。
