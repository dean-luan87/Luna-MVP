# Luna OCR Runtime Provider Adapter Selection v0

**Phase**: `Phase-OCR-Real-Provider-Adapter-Selection-001`  
**判定目标**: **GO**（本阶段完成后）表示 **adapter / registry / selection / audit / smoke** 骨架齐备，且 **默认仍只走 stub**；**不**调用真实 OCR、**不**启用 PaddleOCR runtime、**不**替换 RapidOCR、**不**改生产 routing、**不**进入 MidPlatform、**不**写 WorldModel。

## 与前置阶段的关系

- 依赖主线桥接、规范化与（可选）tile merge stub 等已 **GO** 的路径；本阶段在 `run_ocr_mainline_bridge_v0` 内于 **normalization 产出 `provider_input_pack` 之后** 执行 provider 选择，再调用所选 adapter 的 `run()`。与 **OCR Provider Runtime Governance** 的边界一致，见 [LUNA_OCR_PROVIDER_RUNTIME_GOVERNANCE_STANDARD_V0.md](./LUNA_OCR_PROVIDER_RUNTIME_GOVERNANCE_STANDARD_V0.md)。
- `Phase-OCR-Partial-Evidence-Completion-Policy-001` 仍为 **DESIGN_RECORDED / FIELD_RESERVED**（独立 verifier 未建前不宣称 GO）；与补全策略的衔接见 [LUNA_OCR_PARTIAL_EVIDENCE_COMPLETION_POLICY_V0.md](./LUNA_OCR_PARTIAL_EVIDENCE_COMPLETION_POLICY_V0.md)。

## 代码位置

| 文件 | 作用 |
|------|------|
| `capabilities/ocr_runtime/ocr_provider_adapter_contract_v0.py` | `OCRProviderAdapterV0` 统一接口（`provider_name` / `provider_level` / `supports_input_pack` / `run` / `health_check` / `estimate_cost`）。 |
| `capabilities/ocr_runtime/ocr_stub_provider_adapter_v0.py` | `StubProviderAdapter` 包装 `run_ocr_provider_stub_v0`；`DisabledCandidateAdapter` 占位禁用候选。 |
| `capabilities/ocr_runtime/ocr_provider_registry_v0.py` | 默认 registry：`ocr_stub` 启用；`rapidocr_candidate` 由 **real ∧ rapid** flag 动态启用；`paddleocr_candidate` **默认 disabled**。 |
| `capabilities/ocr_runtime/ocr_provider_selection_v0.py` | 环境变量 + `allow_heavy_ocr` + **input_pack 轻量闸门**；产出 `ocr_provider_selection_report_v0`（`phase` 字段见 Lightweight 文档）。 |
| `capabilities/ocr_runtime/ocr_mainline_bridge_v0.py` | 挂载 selection、合并 audit、误配置硬拒绝（见下）。 |
| `tools/evaluation/ocr/run_ocr_provider_selection_smoke_v0.py` | A/B/C 三用例 smoke。 |
| `tools/evaluation/ocr/verify_ocr_provider_selection_smoke_v0.py` | 本阶段 verifier。 |

## 环境变量与硬边界

| 变量 | 默认 | 语义 |
|------|------|------|
| `LUNA_ENABLE_OCR_MAINLINE_BRIDGE_V0` | `false` | 总开关。 |
| `LUNA_ENABLE_OCR_STUB_PROVIDER_V0` | `true` | stub 关闭则选择失败。 |
| `LUNA_ENABLE_OCR_REAL_PROVIDER_V0` | `false` | 为 `false` 时 registry **不**启用 Rapid；为 `true` 且 rapid flag 同开时方可选轻量真实路径（见 [LUNA_OCR_LIGHTWEIGHT_REAL_PROVIDER_ADAPTER_V0.md](./LUNA_OCR_LIGHTWEIGHT_REAL_PROVIDER_ADAPTER_V0.md)）。 |
| `LUNA_ENABLE_PADDLEOCR_RUNTIME_PROVIDER_V0` | `false` | 若为 `true` 且 `LUNA_ENABLE_OCR_REAL_PROVIDER_V0=false` → **误配置**，bridge **error** 返回（不跑 gate / 不跑 stub）。与 `true` 且 real `true` 时：**不选 Rapid**，仅 stub + reason。 |
| `LUNA_ENABLE_RAPIDOCR_RUNTIME_PROVIDER_V0` | `false` | 与 real 同时为 `true` 时 registry 启用 `rapidocr_candidate`；仍受 input_pack / health 约束。 |

**请求侧**: `allow_heavy_ocr=false` 时选择逻辑会记录 **不得**走 heavy paddle 路径的 reason code（Paddle 仍不会作为 runtime 被选中）。

## `provider_selection_report`（摘要字段）

- `phase`：当前实现为 **Phase-OCR-Lightweight-Real-Provider-Adapter-001**（选择含轻量 input_pack 闸门，见 Lightweight 文档）。
- `selected_provider` / `selected_provider_level`
- `provider_selection_reason_codes`
- `real_provider_requested` / `real_provider_allowed` / `real_provider_invoked`（在真实 adapter 实际执行成功且回填后为 **true**）
- `paddleocr_runtime_provider_enabled` / `rapidocr_runtime_provider_enabled`
- `fallback_to_stub`（例如 `allow_heavy_ocr=true` 且 real 关闭，或 Rapid **unavailable** / **input_pack 被拒**）
- `provider_registry_snapshot` / `provider_unavailable_reason`（可选）

扁平 audit 由 `merge_audit_provider_selection_v0` 同步写入同名键，便于既有 smoke 消费。

## 下一阶段建议

轻量真实路径见 **Phase-OCR-Lightweight-Real-Provider-Adapter-001**（[LUNA_OCR_LIGHTWEIGHT_REAL_PROVIDER_ADAPTER_V0.md](./LUNA_OCR_LIGHTWEIGHT_REAL_PROVIDER_ADAPTER_V0.md)）。后续 heavy（Paddle）仅在独立 phase、独立闸门与进程隔离策略就绪后评估。
