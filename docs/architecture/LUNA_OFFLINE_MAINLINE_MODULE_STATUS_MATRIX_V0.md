# LUNA — Offline Mainline Module Status Matrix v0 (Phase-EngineeringFlow-001)

## 状态枚举
- **done**：已实现并在 offline/shadow scope 内通过验收证据
- **definition_only**：定义/契约已完成，但未形成可运行 gate / 可集成入口
- **runtime_needed**：需要最小 runtime 化（但仍限定在 offline runner 内，不进入真实 runtime）
- **integration_needed**：需要从分阶段工具链收敛到统一主链入口
- **test_needed**：需要纳入回归/验收体系
- **out_of_scope**：明确不在 offline engineering mainline 范围内

## 模块状态矩阵（收口版）

### 输入与数据面
- phone_local bundle/archive（FieldBatch）：**done**
- 样本扩展（更多 phone_local）：**test_needed**（后续 EF-006/增强阶段）

### Perception 与源策略
- YOLO shadow adapter：**done**
- YOLO default offline source policy：**done**
- pinned_local YOLO readiness（manifest+sha256+readiness）：**done**
- Perception replacement（作为 staged tool / 分阶段链路）：**done**
- PerceptionEval 默认入口（统一选择点）：**integration_needed**（EF-002）

### SceneContext（三道防线）
- SceneContext-001/002/003 definitions：**definition_only**
- SceneContext gates 最小 runtime 化（仅 offline runner）：**runtime_needed**（EF-003）

### SceneTask/Fusion/Output（候选链路）
- SceneTask bridge（staged tool）：**done**
- Fusion bridge（staged tool）：**done**
- Output bridge（staged tool）：**done**
- 主链集成形态（统一 runner 可调用）：**integration_needed**（EF-004）

### 语音/TTS 候选链
- Output candidate → 语音/TTS 受控候选链：**integration_needed**（但须明确“候选态/不真实播报”；排在 EF-004/005 之后）

### 可观测性与证据
- trace/replay/whitebox artifacts：**partial**（已有但缺统一入口）
- 统一总观测入口/总报告：**integration_needed**（EF-005）

### 测试与验收
- 全链路回归套件：**missing → test_needed**（EF-006）
- 模块专项测试（Perception/SceneContext/SceneTask/Fusion/Output）：**out_of_scope（当前优先级之后）**

### 实时与试验
- controlled_live_stream：**out_of_scope**
- 真实 runtime：**out_of_scope**
- full controlled trial / open user testing：**out_of_scope**

