# Luna Observation Lens — Copywriting Standard V1

## 品牌与标题

| 场景 | 文案 |
|------|------|
| 页面标题 | Luna Observation Lens |
| 副标题 | 查看 Luna 如何看见、标注、判断和解释当前画面 |
| 内部模块（仅开发者） | Model Test Lens |

## 默认使用（用户可见）

- 开始观察
- 选择图片或视频
- Luna 看到了什么
- 机器人视角
- 模型识别结果
- 原图
- 普通对比
- 可能漏掉
- 我不确定
- 建议补充测试
- 当前结果仅用于模型评估
- 需要人工复核
- 可测试 / 实验中 / 未接入

## 能力卡片标题

视觉：图像分割 · 目标检测 · OCR 文字识别 · SLAM / 空间定位 · 深度感知  
声音：语音识别 · 语音合成 · 说话人  
综合：表情 / 手势 · 多模态理解

## Luna 解释面板区块标题

1. 当前任务  
2. 我看到了什么  
3. 我为什么这么判断  
4. 我不确定什么  
5. 建议下一步怎么测  

## 空状态

- 主文案：把图片或视频放进这里  
- 副文案：Luna 会在这里显示它看到的内容  

## 服务未启动（轻量一行）

本地测试服务未启动。需要测试本地图片时，请运行 `bash scripts/start_local_runner_bridge.sh`

## 默认禁止出现（仅高级/开发者）

manifest · job request · runner bridge · adapter · envelope · artifact_ref · phase_ref · candidate_output · visualization_layers · semantic layer · fact layer · workflow phase · expected_envelope · panel_id · active_example_available · placeholder

## 边界声明（默认简化）

当前结果仅用于模型评估，不会写入事实层，也不会触发导航或语音输出。

## 色彩语义（HUD）

| 语义 | 颜色 |
|------|------|
| 风险 / 注意 | 橙色 |
| 不确定 | 黄色 |
| 可用 / 稳定 | 绿色 |
| 背景 HUD | 深色 |
