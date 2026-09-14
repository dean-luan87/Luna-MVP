# LUNA 主线 Runtime Readiness Level Policy v0

**Phase**：Phase-Mainline-RuntimeReadiness-001  
**用途**：统一 `runtime_readiness_level` 语义；本 Phase **禁止** 评定 R4/R5。

---

## 定义

| Level | 含义 |
|-------|------|
| **R0_not_ready** | 仅有定义、骨架或零散 shadow，无接入条件清单。 |
| **R1_contract_ready** | 合同与字段口径完整，缺 runtime adapter 或总闸 env。 |
| **R2_shadow_ready** | Shadow/offline 闭环，具备 verifier 与回归基线；观测面可用。 |
| **R3_guarded_wiring_ready** | 可进入 **受控接线准备**：接线点、kill switch、TRW、abort/rollback 已登记；**默认全部关闭**。 |
| **R4_controlled_trial_ready** | **本 Phase 禁止给出**。短窗口真实试运行 + abort/rollback。 |
| **R5_production_ready** | **本 Phase 禁止给出**。长期生产运行。 |

---

## 本 Phase 上限

- 矩阵与文档中 **最高只能写到 R3**。
- 任何声明「可上线 / 生产默认开启」等均视为 **超出 Phase 范围**，须在 blocker register 中标注。

---

## 与 capability 的对照（v0 盘点）

当前主线三条（YOLO / OCR / Qwen Voice）在 shadow 与观测面已达 **R2**；真实 runtime 主链未闭合，整体 **未到 R3**，直至：

- 各域 trial **flag 名称冻结**（默认 false）。
- **request_id / trace_id / session_id** 注入路径写死且无旁路。
- **abort/rollback** 与 TRW 字段在真实链上可验收。

详见生成矩阵：`mainline_runtime_readiness_matrix.json`。
