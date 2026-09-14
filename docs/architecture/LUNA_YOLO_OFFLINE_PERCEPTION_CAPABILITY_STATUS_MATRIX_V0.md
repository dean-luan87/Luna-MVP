# LUNA — YOLO Offline Perception Capability Status Matrix v0 (Phase-ModelPerception-Closure-001)

## 状态枚举
- **done**：已实现并通过离线/影子证据链验收（在既定 scope 内）
- **offline-only**：只允许在 offline evaluation 中作为 candidate 信号使用
- **shadow-only**：只允许影子/候选态产出，不得触发执行面
- **blocked**：明确阻断（需要单独阶段与治理入口才能解除）
- **not-claimed**：明确不声称具备该能力/已验证
- **prohibited**：当前明确禁止（无条件禁止，除非另开阶段治理变更）

## 能力矩阵

### done
- YOLO inventory / mapping / gap register（002A）
- YOLO shadow adapter implementation & verifier（002B）
- disable_yolo / fail-closed fallback baseline/mock（贯穿链路要求）
- enabled smoke（004 + Fix-002 闭环）
- YOLO enabled vs baseline comparison（005）
- Perception replacement trial（006）
- SceneTask bridge evaluation（007）
- Fusion bridge evaluation（008）
- Output bridge evaluation（009）
- E2E offline evaluation（010）
- baseline replacement review（011）
- default offline source policy（012）
- pinned weights reproducibility definition（013）
- readiness minimal implementation（014：torch_hub_dev conditional）
- pinned_local weights hardening + readiness（015：GO）

### offline-only
- YOLO 作为 **offline evaluation** 默认 perception candidate source（012 + 011）
- YOLO replacement chain outputs（Perception/SceneTask/Fusion/Output）：仅离线候选态
- E2E offline candidate outputs（无执行、无 TTS）

### shadow-only
- YOLO detection 输出作为 perception candidate 信号源（不授予执行权）
- object/passability/risk 等候选信号（仅供离线评测与审计）

### blocked
- runtime 默认感知源接入（blocked：必须另开阶段，且需 runtime gates + governance）
- controlled_live_stream 接入（blocked：必须另开阶段）
- full controlled trial / open user testing（blocked：必须另开阶段）

### not-claimed（明确不声称）
- OCR
- depth
- dynamic event（可靠的动态事件识别/预测）
- collision risk（可执行级别的碰撞风险判定）
- stable multi-object tracking（稳定跟踪）
- real navigation correctness（真实导航正确性）
- real-time performance / latency SLO
- user-facing reliability（用户可用性、长期稳定性）

### prohibited（必须写死）
- runtime default-on
- controlled_live_stream default-on
- execute/navigation action
- real TTS emit
- 关闭 `pending_real_sidewalk_run`
- 绕过 SceneContext gates / governance
- 扩大 side effects 面

