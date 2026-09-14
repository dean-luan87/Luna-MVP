# Phase-CoreCapability-TRW-Unified-001
# Unified RequestTrace Stage Namespace Go/No-Go Pack v0

**目标**：完成 YOLO/OCR/Voice 三条核心能力线的统一 RequestTrace stage namespace 定义与映射原则（definition-only）。  
**边界**：不实现 runtime、不做 adapter、不重构目录、不接真实播放、不执行真实 TTS。

---

## GO 条件

- unified namespace 定义完整（`core_capability_request_trace_v0` + 一级分组）
- YOLO stages 定义完整（stage list + 字段要求 + 边界）
- OCR stages 定义完整（stage list + 字段要求 + 边界）
- Voice 兼容现有 `voice_output_governance_v0`（兼容映射 + 硬审计字段不丢失）
- ID 规范完整（request_id/trace_id/session_id/source_run_id 等）
- local TRW → RequestTrace 映射原则完整（保留 refs、missing 规则、禁止伪造）
- MidPlatform/SceneDelta/WorldContext/WriteReadiness 的后续 stage 位置已占位（在 unified namespace 文档中）
- 未实现 runtime、未重构、未触碰真实播放链

---

## CONDITIONAL_GO

- 某些 YOLO/OCR 历史字段无法完全对应，但已明确 missing/future adapter（不得伪造）。

---

## NO_GO

- 把 shadow mapping 当 runtime 接入
- 伪造 trace_id/session_id
- 丢失 local TRW refs
- 重构目录或接入真实播放/TTS/地图/GPS/点云
- 进入 SceneTask/Fusion/Output

