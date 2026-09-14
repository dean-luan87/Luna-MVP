# LUNA 主线 Runtime Abort / Rollback 要求 v0

**Phase**：Phase-Mainline-RuntimeReadiness-001  
**原则**：每一次「放行真实 provider / 真实播报」失败时，须有不伤害用户与系统的 **安全默认**，且 **shadow 证据可保留**。

机器可读表：`mainline_runtime_abort_rollback_requirement_matrix.json`。

---

## Voice / Qwen

| 触发 | abort | rollback / fallback | safe default | 用户影响 |
|------|-------|---------------------|--------------|----------|
| Qwen 超时 / 网络 | 熔断打开 | Piper 或 suppress | offline_only / Piper | 可能听到备用音色或静默 |
| governance 未接受 | 阻断 submit | 不调 provider | 无播报 | 无播放 |
| diff_audit 缺失/不一致 | 阻断 provider | 无合成 | 无播报 | 无播放 |
| SpeechGate / guard 缺失（若路径要求） | 阻断 submit | 无下游 | 无播报 | 无播放 |
| 过期 / 取消 | 阻断 submit | 丢弃队列项 | 无播报 | 无播放 |

**runtime_can_continue**：通常为 **true**（降级继续）。  
**shadow_evidence_retained**：**true**（与 RequestTrace 策略一致）。

---

## OCR

| 触发 | abort | rollback | safe default |
|------|-------|----------|----------------|
| provider 不可用 | 跳过或 defer | 标记 not_available | 无 OCR 输出 |
| governance / 源策略泄漏 | 阻断下游消费 | kill switch | 不向下游送证据 |
| source policy 未解析 | 不进行 runtime OCR | — | 显式空结果 |

---

## YOLO

| 触发 | abort | rollback | safe default |
|------|-------|----------|----------------|
| detector 失败 | 本 tick 跳过 | degraded observation | 无检测框 |
| frame 缺失 | 无推理 | — | 无检测 |
| confidence 坍塌（策略定义后） | guarded mode | 降低输出或抑制 | 按策略降级 |

---

## 通用要求

每条 abort 须对应：**abort condition（可判定）**、**rollback action**、**fallback path**、**safe default**、**用户是否受影响**、**runtime 是否可继续**、**shadow 是否保留**。

未定义 abort/rollback 即建议接线 → **NO_GO**。
