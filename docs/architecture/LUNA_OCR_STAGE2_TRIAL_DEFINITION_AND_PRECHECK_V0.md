# LUNA — OCR Stage-2 Trial Definition & Dry-run Precheck v0

## Phase

- **Phase-Mainline-GuardedTrial-008** — *OCR Stage-2 Definition & Dry-run Precheck v0*

## Goal

在 **YOLO Stage-1 已 `closed_v0`** 的前提下，仅完成：

- OCR Stage-2 的 **范围定义（definition）**
- OCR Stage-2 的 **dry-run precheck**（只做静态/路径/合同检查；不调用真实 OCR provider）
- OCR Stage-2 的 **runner skeleton**（默认不执行 provider）

## Allowed scope（允许）

- 读取/引用 OCR source policy（离线 raw_text source policy）
- 静态检查 provider readiness（配置/manifest/文件存在与可解析）
- 检查 fallback / not_available 策略存在（policy/selector 层）
- 校验 raw_text candidate schema（仅 schema 合同，不取真实输出）
- 检查 output_root / RequestTrace / trace-replay-whitebox 写入路径可写
- 生成 precheck report、runner skeleton、abort/rollback plan

## Forbidden scope（禁止）

- **执行真实 OCR provider**（任何推理/网络/SDK 调用）
- `semantic_interpretation_enabled=true`
- 自动进入 **MidPlatform / SceneDelta / WorldContextEvidence**
- 进入 **SceneTask / Fusion / Output**
- 导航动作、真实播报、真实 TTS、播放
- 调用 Qwen
- 写世界模型
- 蜂巢上传 / 推荐系统
- 读取实时 camera / 连接在线 runtime
- 修改 provider 默认策略
- 修改 env 语义（本阶段只登记、默认关闭）

## GO / CONDITIONAL_GO / NO_GO

### GO

- `yolo_stage1_closed_v0_confirmed=true`
- source policy ready
- provider readiness static checked
- fallback policy ready
- raw_text candidate schema ready
- rollback plan ready
- abort conditions registered
- output paths writable
- trace/replay/whitebox 非空
- hard audit 全 false
- verifier 通过

### CONDITIONAL_GO

- 静态 readiness 已确认，但 credentials / runtime 依赖仍待后续阶段（本阶段不要求真实调用）

### NO_GO

- 缺失 `closed_v0` 确认 / policy / schema / rollback / abort / 可写路径
- 任意 forbidden scope 被触发（例如 `provider_invoked=true` / semantic=true / midplatform=true 等）

