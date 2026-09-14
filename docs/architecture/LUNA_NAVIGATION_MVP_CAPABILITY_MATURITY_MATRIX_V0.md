# Phase-Productization-000 — Navigation MVP Capability Maturity Matrix v0（能力成熟度矩阵冻结）

**目的**：把“已完成 v0”与“placeholder/mock/未开始”严格区分，防止 v0 能力被误判为产品级完成。  

---

## 状态枚举（写死）

- `completed_v0`
- `conditional`
- `placeholder_only`
- `blocked`
- `not_started`

---

## 能力域矩阵（v0）

| capability_domain | maturity_status | evidence_source | remaining_gap | next_phase_action | blocker_level |
|---|---|---|---|---|---|
| Governance | completed_v0 | Phase-Closure-001 收口文档链 | 不等于“真实执行放权已进入”；仍需维持闭合安全态 | 进入 RealScenePrep-001 前保持边界不变 | soft_followup |
| Model Shadow Integration | completed_v0 | Phase-Model-002 实现+验证 | 仅 shadow/candidate-only；不等于可执行模型 | 保持 shadow；补充真实输入下的观测覆盖 | soft_followup |
| Model Admission Baseline | conditional | Phase-Model-003 = conditional_go | 候选质量仍需提升；抗探针/稳定性需继续评估 | 受控真实场景前置阶段追加质量回归矩阵 | soft_followup |
| Perception Baseline | completed_v0 | Phase-Perception-001 = go | baseline 不等于产品级；弱光/抖动/隐私等未覆盖 | 受控真实场景前置补充“受控真实输入”验证计划 | soft_followup |
| SceneTask Chain | completed_v0 | Phase-SceneTask-001 = go | 仅 4 核心场景；不扩长尾 | RealScenePrep-001 仅做前置定义与护栏，不扩场景 | soft_followup |
| Map × Vision × Memory Fusion | completed_v0 | Phase-Fusion-001 = go | 地图/记忆可为 mock/minimal；真实更新/污染治理后置 | 保持 conflict policy；补充真实定位漂移观测占位 | soft_followup |
| Navigation Output Timing | completed_v0 | Phase-Expression-001 = go | 文案/模板为 v0；非产品级 TTS/声学 | RealScenePrep-001 仅定义受控输出策略，不做产品化 TTS | soft_followup |
| On-Device Closed Loop | completed_v0 | Phase-Device-001 = go | 主要 fixture/replay/受控输入；非开放环境 | RealScenePrep-001 明确 controlled live 的显式入口与护栏 | soft_followup |
| Industrial Placeholder Register | completed_v0 | `LUNA_INDUSTRIAL_GRADE_PLACEHOLDER_REGISTER_V0.md` | placeholder 不可被忽略；需持续维护 planned_phase | RealScenePrep-001 前补齐新增占位（如出现） | soft_followup |
| Logging / Trace / Replay / Whitebox | completed_v0 | Device-001 requirements + validator | 真机长时/高频落盘策略未产品化 | RealScenePrep-001 明确采样/压缩/脱敏方向（仅定义） | soft_followup |
| Fallback / Degraded Mode | completed_v0 | Device-001 matrix+validator 覆盖 | 复杂真实环境下的降级策略仍需细化 | RealScenePrep-001 仅追加触发条件清单与中止策略 | soft_followup |
| Default Path Control | completed_v0 | 多阶段硬声明：default path disabled | 需要防止未来阶段误开 default-on | RealScenePrep-001 强制显式入口与审计字段 | soft_followup |
| Side Effects Control | completed_v0 | 全链 candidate-only + no execute leakage | 未来真实动作仍需独立治理链（不在此阶段） | RealScenePrep-001 明确“不扩大 side effects 面” | soft_followup |

---

## 总结（矩阵级）

- **允许进入下一阶段**：是（见 readiness review：`conditional_go`）  
- **核心原因**：链路闭环已完成 v0，但模型准入仍 conditional 且设备验证仍非开放真实环境覆盖。  

