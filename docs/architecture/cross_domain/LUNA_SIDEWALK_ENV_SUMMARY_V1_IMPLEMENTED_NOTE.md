# sidewalk_env_summary_v1 最小实现（V1）说明

## 实现了什么

根据《[LUNA_SIDEWALK_ENV_SUMMARY_STABILIZATION_PLAN_V1.md](./LUNA_SIDEWALK_ENV_SUMMARY_STABILIZATION_PLAN_V1.md)》，新增**最小可调用**的摘要构建模块（不做统一环境层、不接地图/视觉）：

- 模块：`capabilities/cross_domain/context/sidewalk_env_summary_v1.py`
- 入口：`build_sidewalk_env_summary_v1(...)`
- 包导出：`capabilities/cross_domain/context/__init__.py`

## 当前最小输入

| 参数 | 说明 |
|------|------|
| `scene_candidate` | 场景候选字符串 |
| `path_confidence` | [0,1] 路径/可通行相关置信 |
| `is_outdoor` | 是否在室外 |
| `event_timestamp` | 观测时间（秒，与 `time.time()` 同口径） |
| `now` | 可选，当前时间（秒） |
| `ttl_ms` | 可选 TTL；未传则用 `LUNA_SIDEWALK_ENV_SUMMARY_TTL_MS` 或默认 `5000` |
| `source` | 可选来源标签（默认 `sidewalk_env_summary_builder_v1`） |

## 当前最小输出（dict）

与主线已有三字段兼容，并增加稳定化字段：

| 键 | 说明 |
|----|------|
| `scene_candidate` / `path_confidence` / `is_outdoor` | 与输入一致（`path_confidence` 为**原始值**） |
| `summary_freshness` | `fresh` \| `stale` \| `ambiguous` |
| `event_timestamp` | 观测时间（秒） |
| `ttl_ms` | 本摘要使用的 TTL |
| `confidence_weight` | TTL 内线性衰减 × 路径置信；`stale` 为 0；`ambiguous` 再 ×0.5 |
| `summary_schema_version` | `sidewalk_env_summary_v1/1` |
| `source` | 来源标记 |
| `age_ms` | 相对 `now` 的年龄（毫秒） |
| `inference_notes` | 短枚举列表（如 `ttl_expired`、`low_path_confidence`） |

**与 risk 的关系**：本模块**不**读取、不写入 `risk_summary_v1`；与 risk 零耦合。

## 怎么验证

```bash
python3 tools/test_sidewalk_env_summary_v1.py
```

覆盖：新鲜 / 过期 stale / 低证据 ambiguous / 输出不含 risk 键 / 默认 TTL。

## 主线接入

- 已接入 `dispatch_voice_final_text` 入口稳定化，见《[LUNA_SIDEWALK_ENV_SUMMARY_V1_INTEGRATED_NOTE.md](./LUNA_SIDEWALK_ENV_SUMMARY_V1_INTEGRATED_NOTE.md)》。

## 哪些还没做

- ~~未接入 `voice_final_text_dispatcher`~~（已完成，见上）
- 无统一环境层、无多源合并、无地图/OCR
- TTL 未按「感知 vs 地图」分档（V1 单一 TTL + env 覆盖）

## 一句话收束

先把 **sidewalk_env_summary_v1** 做成可调用、可判 fresh/stale/ambiguous、可衰减权重的最小输入层；接入主链与上游生产管线留待下一步。
