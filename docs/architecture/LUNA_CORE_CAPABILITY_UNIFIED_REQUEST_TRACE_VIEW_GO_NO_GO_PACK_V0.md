# Phase-CoreCapability-TRW-Unified-003
# Unified Core RequestTrace View Go/No-Go Pack v0

**阶段目标**：把 YOLO / OCR / Voice 三条 shadow chains 合并为统一核心能力 RequestTrace shadow view（只读合并视图）。

**硬边界**：不接 runtime、不重构目录、不接真实播放、不执行真实 TTS、不执行导航动作、不写真实世界模型、不进入 SceneTask/Fusion/Output、不接地图/GPS/点云。

---

## GO 条件（全部满足）

- core shadow root 可读（YOLO/OCR chains 可加载）
- voice shadow root 可读（Voice chains 可加载）
- unified view 产物生成（summary/index/timeline/matrix/jsonl）
- capability index 包含 yolo/ocr/voice
- stage namespace 保留（不强制迁移）
- source_root refs 保留（不丢失关键 refs 键）
- hard audit 不变量保持（YOLO/OCR/Voice）
- unified trace/replay/whitebox JSONL 非空
- verifier 通过

---

## CONDITIONAL_GO（允许但必须明确）

- 无法跨能力统一 request_id（本阶段允许且必须明确“不伪造跨能力 link”）
- timestamp 缺失（必须 null + missing_fields，不伪造）

---

## NO_GO（任一触发即失败）

- 强行伪造跨能力 request link（把 YOLO/OCR/Voice 硬拼成同一个 request_id）
- 伪造 trace_id/session_id
- 丢失 source refs 或补假路径
- hard audit 字段缺失或出现禁止值（如 `real_tts_invoked=true` / `provider_invoked=true` / `navigation_action` 非空）
- 本阶段接入 runtime 或修改原始链路
- 目录级重构

