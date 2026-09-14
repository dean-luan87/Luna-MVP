# LUNA Evaluation Tools — Boundary Contract v0 (Phase-EvaluationTools-Foundation-001)

## Allowed

Evaluation Tools 允许：

- 生成测试数据（synthetic / curated / imported）
- 管理 ground truth 与数据集 manifest
- 运行离线 provider benchmark（单图 / batch / stress）
- 计算指标（CER / WER / 中文召回 / 空串率 / 乱码率 / 延迟等）
- 生成 failure cases（归档、可复现、可回放）
- 生成人工复核包（contact sheet / review index / annotations template）
- 输出压力测试报告与 provider 对比报告

## Forbidden (hard boundaries)

Evaluation Tools 禁止：

- 进入 Luna runtime 主链（不得被 runtime import/执行）
- 进入 whitebox 后台（不得接入任何白盒 UI/服务）
- **自动改变**主线 provider 选择或 runtime 决策
- 写世界模型 / 触发中台 / 触发导航动作
- 触发语音输出（真实 TTS / 播报）或调用 Qwen
- 上传蜂巢、接推荐系统、作为线上决策依据直接运行

## Output policy

- Evaluation Tools 可输出报告与证据包供 **人工评审/验收** 使用
- 允许写 evaluation-only 的 `trace/replay` JSONL 以便审计
- **不得复用** runtime RequestTrace pipeline / stage namespace

