# LUNA OCR Independent Capability Definition v0

## Phase

- Phase-ModelOCR-001（OCR Independent Capability Definition v0）

## Goal (definition-only)

本阶段只做 OCR 独立能力定义与冻结：

- 定义 OCR 在 Luna 感知层的职责与非目标
- 冻结输入边界、输出结构（candidate-only）、控制方案、禁止项
- 冻结 trace / replay / whitebox 记录要求（只定义，不实现 runtime）
- 冻结 fallback / not_available 规则（fail-closed）
- 冻结验收指标（为后续实现阶段提供合同）
- 明确后续阶段路线，但 **本阶段不实现** YOLO 联动/中台仲裁/下游接入

## Non-goals (hard)

本阶段明确不做：

- 不接 YOLO（不做 YOLO+OCR 联动）
- 不接中台（不做 Scene Belief / Evidence Arbitration 实现）
- 不接 SceneTask / Fusion / Output
- 不进入 controlled_live_stream
- 不进入 full controlled trial
- 不开放真实用户测试
- 不执行导航动作
- 不真实播报（real TTS）
- 不做 tracking / depth / OCR(dynamic) 能力增强（实现层面）
- 不新增任何真实 runtime 默认路径

## OCR responsibilities (what OCR does)

OCR 只负责输出“文字候选证据”：

- 从图像/视频帧中读取文字候选（text candidates）
- 给出文字位置 bbox
- 给出置信度 confidence
- 给出文本类型候选（方向指示/门牌/设施/警示/广告/屏幕等）
- 给出导航相关性候选（仅候选，不是结论）
- 标记不确定/遮挡/低置信/不可用（honesty）

## OCR non-responsibilities (what OCR must NOT do)

OCR 不负责也不得输出/推断：

- 用户应该往哪里走（不可产生 final navigation instruction）
- 某个文字是否一定是真实标识（不得“盖章真实”）
- macro_scene 判断（不得决定 scene）
- 触发 SceneTask / Fusion / Output
- 触发真实 TTS
- 执行导航动作/side effects

## Scope (where OCR lives in the stack)

OCR 独立能力只写入感知层信号：

- `ocr_navigation_signal`（candidate-only）

可选仅定义（不实现联动）：

- `visual_text_region_candidate`（用于后续 YOLO×OCR 协同时的区域文字候选组合）

## Stop condition (for Phase-ModelOCR-001)

满足以下即本阶段 GO 并停止（不进入实现）：

- 职责边界清楚（do / not-do）
- 输入输出合同清楚（含禁止项与 fail-closed 规则）
- 观察控制方案清楚（full_frame / region_focused / task_hint_guided）
- trace / replay / whitebox 要求清楚（字段与产物）
- 验收指标清楚（后续实现阶段可直接用作门槛）
- 后续主线分段（A/B/C）与阶段路线冻结清楚

