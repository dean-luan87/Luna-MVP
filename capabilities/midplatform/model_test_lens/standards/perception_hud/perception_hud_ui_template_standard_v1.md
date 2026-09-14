# Perception HUD UI Template Standard V1

## 模板组成

### 1. 主画面（HUD Canvas）

- 底图：原图 / 视频帧 / 音频波形 / 文本输入视图
- 叠加：boxes · masks · OCR boxes · keypoints · trajectories
- 标注：置信度 · 空间关系 · 任务相关性 · 不确定性 · 风险/注意力标记

### 2. Reasoning Panel（右侧或下方）

| 区块 | 用户文案标题 |
|------|-------------|
| current_task | 当前测试任务 |
| system_observations | 我看到了什么 |
| reasoning_steps | 我为什么这么判断 |
| uncertainty_summary | 我不确定什么 |
| missing_information | 可能漏了什么 |
| recommended_next_steps | 建议下一步怎么测 |

### 3. 控件

- 显示/隐藏识别层
- 显示/隐藏标签
- 透明度 slider
- 只看原图 / 只看模型结果 / 机器人视角 HUD
- 高级信息（折叠）

## 布局规格

见 `perception_hud_default_layout_spec_v1.json`。

## 与 Compare View 关系

- Compare View：**左原图 | 右模型结果**（已完成）
- HUD View：在 Compare 之上增加**解释层**，不是替代
- 切换：「普通对比」↔「机器人视角 HUD」

## 与 Luna Observation Lens V1 关系

Perception HUD 是 Luna Observation Lens V1 **中央画布**的核心子系统。V1 Closure 后：

- HUD 线框 / 编号 / 短标签 / HiDPI 渲染为冻结行为
- 对象详情默认进入 **对象胶囊条** + drawer，不挤压主画面
- Reasoning Panel 并入右侧 **Luna 观察面板**（结论优先）

完整布局见 `luna_observation_lens_v1_template_standard.md`。

## 治理

- 只读 · candidate-only · 非 fact · 非 runtime · 非导航 · 非语音
