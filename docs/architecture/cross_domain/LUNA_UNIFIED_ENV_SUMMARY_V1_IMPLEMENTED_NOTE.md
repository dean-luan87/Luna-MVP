# unified_env_summary_v1 实现说明（V1）

## 实现了什么

- 新增模块 `capabilities/cross_domain/context/unified_env_summary_v1.py`。
- 提供 `build_unified_env_summary_v1(...)`：从最小原始环境信号生成 **统一环境摘要** `dict`，带 `summary_schema_version: unified_env_summary_v1/1`。
- **scene_family** 第一版仅支持：`walkway` | `retail` | `unknown`（基于 `raw_scene_candidate` 关键词与可选 `raw_family_hint` 弱提示）。
- **TTL**：默认读 `LUNA_UNIFIED_ENV_SUMMARY_TTL_MS`，未设置时为 **6000 ms**（`default_unified_ttl_ms_v1()`）。
- **summary_freshness**：`fresh` / `stale` / `ambiguous`；超 TTL 为 `stale`；低置信或 unknown 家族偏低置信等为 `ambiguous`；含 `confidence_weight` 与 `age_ms`、`inference_notes`。

## 当前最小输入 / 输出

**输入（必填 / 常用）**

| 参数 | 说明 |
|------|------|
| `raw_scene_candidate` | 原始场景候选字符串 |
| `raw_environment_confidence` | 原始环境整体置信 0–1 |
| `event_timestamp` | 观测时间（秒，与 `time.time()` 同口径） |
| `source` | 来源标记 |

**可选**

| 参数 | 说明 |
|------|------|
| `raw_family_hint` | `walkway` / `retail`，仅在无法从 scene 判定家族时作弱提示 |
| `ttl_override_ms` | 覆盖默认 TTL |
| `now` | 当前时间（秒），默认 `time.time()` |

**输出（至少）**

`scene_family`、`scene_candidate`、`environment_confidence`、`event_timestamp`、`summary_freshness`、`ttl_ms`、`confidence_weight`、`source`、`summary_schema_version`、`age_ms`、`inference_notes`。

**本模块不产出、不读取**：`risk_summary_v1`、`find_item_intent_summary_v1`、`ocr_summary_v1` 任意字段。

## 怎么验证

```bash
python3 tools/test_unified_env_summary_v1.py
```

覆盖：walkway / retail / unknown 家族、超 TTL stale、低置信 ambiguous、输出键不含 risk/intent/OCR 语义、默认 TTL。

## 哪些还没做（按设计）

- **不接主线**：未在 `dispatch_voice_final_text` 写入 metadata。
- **不替换** `build_sidewalk_env_summary_v1` / `build_retail_env_summary_v1`，不做派生迁移。
- **不并入** risk / 意图 / OCR。
- **不做** 地图/知识接入与更多 `scene_family` 扩张。

## 一句话收束

`unified_env_summary_v1` 已是可运行的最小 builder，用于验证统一环境抽象；后续再定 sidewalk/retail 派生映射与是否接线主线。
