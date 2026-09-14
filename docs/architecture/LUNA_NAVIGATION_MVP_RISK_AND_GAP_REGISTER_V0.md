# Phase-Productization-000 — Navigation MVP Risk & Gap Register v0（风险与缺口登记冻结）

**目的**：在进入“受控真实场景试验前置开发”之前，把风险/缺口显式登记并分级，防止未登记风险直接带入真实环境。  

---

## 字段要求（写死）

每条风险必须包含：
- `risk_id`
- `risk_name`
- `risk_level`（low/medium/high/critical）
- `blocker_level`（hard_blocker / soft_followup / industrial_placeholder）
- `planned_phase`
- `mitigation_direction`
- `blocking_current_phase`（bool；Productization-000 默认 false，除非 hard blocker）

---

## 风险清单（v0）

| risk_id | risk_name | risk_level | blocker_level | planned_phase | mitigation_direction | blocking_current_phase |
|---|---|---|---|---|---|---|
| R-001 | Model-003 仍为 conditional_go（候选质量/稳定性仍需提升） | high | soft_followup | Phase-RealScenePrep-001 | 在受控真实输入下做 shadow 质量回归矩阵与观测指标 | false |
| R-002 | Perception-001 为 baseline，不等于产品级感知覆盖 | high | industrial_placeholder | Phase-Device-001 / Phase-Device-002 | 弱光/抖动/隐私/长时等按占位推进，不得误判已完成 | false |
| R-003 | Fusion-001 的地图/记忆仍可为 mock/minimal | medium | industrial_placeholder | Phase-Fusion-002（future） | 明确真实地图更新/离线/记忆污染治理后置，不在当前扩展 | false |
| R-004 | Device-001 主要 fixture/replay/受控输入，不等于开放真实环境 | high | soft_followup | Phase-RealScenePrep-001 | 明确 controlled live 的护栏、短时窗口与中止策略；仍不开放用户 | false |
| R-005 | 工业级性能/功耗/发热/弱光/隐私/长时间运行仍为 placeholder | high | industrial_placeholder | Phase-Device-001 / Phase-Device-002 / Phase-Model-004 | 保持占位登记与 planned_phase；只要求“可记录可观察” | false |
| R-006 | 真机连续摄像头输入的专项验证仍不足 | high | soft_followup | Phase-RealScenePrep-001 | 受控真实输入专项：显式入口、可回放、可中止、可降级 | false |
| R-007 | 真实 TTS 延迟与声学环境未做产品级验收 | medium | industrial_placeholder | Phase-Device-001 / Phase-Voice-002 | 仅记录与观测；不作为进入前置开发阻断 | false |
| R-008 | 真实路线/真实场景中的用户行为不确定性尚未验证 | high | soft_followup | Phase-RealScenePrep-001 | 受控真实场景前置定义中写死“非开放测试”边界与人类监督条件 | false |
| R-009 | “Device-001 GO”被误解为产品可发布资格 | critical | soft_followup | Phase-Productization-000（本阶段） | 文档与 pack 明确声明：GO≠发布；fixture≠真实充分验证 | false |

---

## 当前 hard blockers（v0）

无。  
说明：若出现 execute 泄漏、default-on、side effects expansion、trace/replay 缺失、fallback 不成立，则必须升级为 hard blocker 并停止进入真实场景前置。

---

## 当前 soft follow-ups（v0 摘要）

- Model-003 质量与稳定性仍需在受控真实输入下回归
- controlled live input 的护栏/中止/回放需要在下一阶段前置定义中写死

---

## 当前 industrial placeholders（v0 摘要）

参见：`docs/architecture/LUNA_INDUSTRIAL_GRADE_PLACEHOLDER_REGISTER_V0.md`（IG-001…）  
本表不复制全部占位，仅保证风险层面不误判已完成。

