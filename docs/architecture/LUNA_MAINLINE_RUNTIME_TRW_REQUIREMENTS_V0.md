# LUNA 主线 Runtime TRW / RequestTrace / Whitebox 要求 v0

**Phase**：Phase-Mainline-RuntimeReadiness-001  
**目标**：真实 runtime 接入前，每条主链必须能回答：**谁在什么 request 下、走了哪条 provider 路径、为何阻断或降级**。

---

## 1. 标识注入（硬要求）

| 字段 | 说明 |
|------|------|
| `request_id` | 跨 YOLO/OCR/Voice 一致关联 |
| `trace_id` | 分布式追踪根 |
| `session_id` | 会话边界 |
| `source_run_id` | 离线/回放来源 |
| `runtime_run_id` | 在线运行实例 |
| `trace_ref` | 外部追踪引用 |
| `replay_ref` | 回放复现钉扎 |
| `whitebox_ref` | 白盒实验钉扎 |

身份策略见：`LUNA_CORE_CAPABILITY_REQUEST_TRACE_IDENTITY_POLICY_V0.md`。

---

## 2. 审计与观测（硬要求）

| 字段 | 说明 |
|------|------|
| hard_audit fields | 与 Voice governance / Qwen Phase-009 导出一致 |
| provider_health | 与 MidPlatform / TTS policy 模式对齐 |
| latency_ms | 分段耗时 |
| timeout_ms | 配置与实测 |
| fallback | 实际选用的 fallback 链 |
| suppression_or_block_reason | 阻断 / 抑制原因枚举 |

---

## 3. Voice / Qwen 附加（governed entry）

在通用字段之外，真实链验收至少还需：

- `provider_input_text` / `spoken_text`（口径与 diff_audit schema 一致）
- `text_diff_audit`（Phase-Qianwen-001 schema）

Shadow 侧已闭合；runtime 侧须保证 **real_qwen_invoked / real_tts_invoked** 等硬审计与代码路径一致。

---

## 4. 保留字段（禁止静默删减）

Unified Core View 与 query/export 路径已定义的 stage / 字段名，接线时 **不得** 侧写私有副本替代；若扩展须在 **namespace 政策**下评审。

---

机器可读清单：`mainline_runtime_trw_requirement_matrix.json`。
