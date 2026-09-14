# LUNA Mainline Runtime Readiness Boundary Register v0（Phase-006）

**Phase**：Phase-Mainline-RuntimeReadiness-006  
**作用**：登记 RuntimeReadiness 闭包 **允许 / 禁止** 事项，防止与本阶段结论混淆。

---

## 1. 冻结字段（与 `boundary_summary.json` 一致）

| 字段 | 值 |
|------|-----|
| `runtime_readiness_status` | `closed_v0` |
| `scope` | `guarded_trial_readiness_layer` |
| `real_runtime_activation_allowed` | `false` |
| `real_qwen_invocation_allowed` | `false` |
| `real_tts_invocation_allowed` | `false` |
| `real_playback_allowed` | `false` |
| `default_trial_enabled` | `false` |
| `global_kill_switch_required` | `true`（语义：必须在治理模型中保留并可审计） |
| `whitebox_scope` | `minimal_observability_only` |

---

## 2. 禁止（本阶段及闭包默认）

- 接地图 / GPS / 点云；SceneTask / Fusion / Output；导航动作；世界模型写入；蜂巢上传；推荐系统。  
- 白盒后台、白盒 UI、复杂查询系统的产品化实现。  
- 修改 YOLO/OCR/Voice **主链业务语义**（004 hook 仅为默认关闭旁路）。

---

## 3. 允许（最小）

- RequestTrace shadow stage、side-effect 审计字段、reason/no-op/kill 可见性、004/005 工具链产出的 trace/replay/whitebox jsonl。
