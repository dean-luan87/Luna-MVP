# Phase-Voice-OutputGovernance-006
# Voice Output Governance Future Branches v0（后续分支清单）

**目的**：列出 closure 后的合理分支，避免在 closed_v0 上直接接入真实播放或破坏边界。

---

## 1. Observability / IDs

- trace_id/session_id 注入与贯通（从主链 `SpeechRequest.trace_id` / voice session anchor 注入）
- candidate_text_hash 标准化（统一算法与落点）

---

## 2. Wiring / Runtime modes (仍需分阶段)

- governed_submit shadow（不影响输出，只给出“若治理接入会如何”）
- real submit wiring trial（严格受控：必须满足 003 wiring contract，且审计字段全链可观测）
- provider health runtime（latency/failure/circuit breaker 的真实统计与 readiness gate）

---

## 3. Controlled real playback（严格受控）

- real playback controlled trial（必须建立 operator runbook、kill switch、回滚策略与回归门槛）

---

## 4. Cross-domain trace unification

- unified YOLO/OCR/Voice request trace mapping（统一链路视图，但不得污染事实层/世界模型）

