# retail_env_summary_v1 最小实现（V1）说明

## 实现了什么

根据《[LUNA_RETAIL_ENV_SUMMARY_STABILIZATION_PLAN_V1.md](./LUNA_RETAIL_ENV_SUMMARY_STABILIZATION_PLAN_V1.md)》，新增**最小可调用**的零售环境摘要构建模块：

- `capabilities/cross_domain/context/retail_env_summary_v1.py`
- 入口：`build_retail_env_summary_v1(...)`
- 包导出：`capabilities/cross_domain/context/__init__.py`

## 当前最小输入

| 参数 | 说明 |
|------|------|
| `scene_type` 或 `scene_type_candidate` | 规范化为 `retail_shelf` / `retail_aisle` / `unknown` |
| `retail_context_confidence` | [0,1] |
| `shelf_visible` | bool |
| `gating_passed` | 可选 bool；`None` 表示交由下游规则推断 |
| `event_timestamp` | 秒（与 `time.time()` 同口径） |
| `now` / `ttl_ms` / `source` | 可选 |

## 当前最小输出（dict）

| 键 | 说明 |
|----|------|
| `scene_type` / `scene_type_candidate` | 规范场景（主线可读 `scene_type` 或 `scene_type_candidate`） |
| `retail_context_confidence` | 原始输入值 |
| `shelf_visible` / `gating_passed` | 与输入一致 |
| `summary_freshness` | `fresh` \| `stale` \| `ambiguous` |
| `event_timestamp` / `ttl_ms` / `confidence_weight` / `age_ms` | 时效与衰减 |
| `summary_schema_version` | `retail_env_summary_v1/1` |
| `source` / `inference_notes` | 来源与短枚举备注 |

**不包含**：OCR、找货意图、risk 任意字段；本模块不 import 上述域。

## TTL 默认

- 环境变量：`LUNA_RETAIL_ENV_SUMMARY_TTL_MS`，缺省 **8000** ms（零售场景略长于 sidewalk 默认）。

## 怎么验证

```bash
python3 tools/test_retail_env_summary_v1.py
```

## 哪些还没做

- 已接入 `dispatch_voice_final_text` 入口稳定化，见《[LUNA_RETAIL_ENV_SUMMARY_V1_INTEGRATED_NOTE.md](./LUNA_RETAIL_ENV_SUMMARY_V1_INTEGRATED_NOTE.md)》。
- 多级 TTL（货架 vs 门店）仍为单 TTL + env 覆盖
- 统一环境层派生视图未接

## 一句话收束

**retail_env_summary_v1** 已具备与 sidewalk 同风格的稳定化 builder；主线接入与 `retail_find_item_v1` 优先消费留待下一步。
