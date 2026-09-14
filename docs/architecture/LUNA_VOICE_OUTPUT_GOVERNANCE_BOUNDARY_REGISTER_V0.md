# Phase-Voice-OutputGovernance-006
# Voice Output Governance Boundary Register v0（边界登记）

**目的**：把 Voice Output Governance 的“禁止项”登记为 closure 硬边界，防止回归/增强时误触真实副作用。

---

## 1. 永久边界（本阶段与 closed_v0 都必须遵守）

- 不真实播报（no real playback）
- 不执行真实 TTS（no provider runtime invocation）
- 不接新 provider
- 不删除 legacy voice
- 不改现有 env 开关语义/默认值
- 不把 Phase-002 skeleton 接入真实 submit 链
- 不进入导航/SceneTask/Fusion/Output 新链路
- 不执行导航动作
- 不写世界模型
- 不上传蜂巢
- 不接推荐系统

---

## 2. 硬审计不变量（必须为 false/null）

- `real_tts_invoked=false`
- `playback_invoked=false`
- `provider_invoked=false`
- `navigation_action=null`
- `downstream_invocation_count=0`

