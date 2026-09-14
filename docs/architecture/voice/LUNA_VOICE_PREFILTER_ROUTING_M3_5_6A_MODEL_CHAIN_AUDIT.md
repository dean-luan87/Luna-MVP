# LUNA Voice Prefilter Routing M3.5.6a Model-Chain Audit（识别链归因）

## 背景

M3.5.6 扩灰到更高样本量后出现少量 **model routes 非绿**，表现为：

- 失败只审计 `route_to_turbo/route_to_plus`（明确剔除 `route_to_rule_or_reject` 正常样本）
- 在部分 `day` 样本里出现：
  - `used_model_chain = false`
  - `validator_ok = None`
  - `fallback = true`

## 本轮目标（只做归因，不做修复）

对 M3.5.6 中那 12 条 model routes 非绿样本做定点归因，判断问题到底是：

- **A. 模型真失败为主**（没有返回可用结构化/JSON）
- **B. model_chain 识别 / success tagging 口径问题为主**（模型已返回，但识别/打标没命中）
- **C. 两者混合，但以某一类为主**

## 本轮原则（冻结项）

- 不扩灰
- 不改骨架 / 路由策略
- 不改 prefilter / prompt
- 不改 schema / validator / builder
- 只允许：归因、对照、最小观测补充（如确有必要）

## 固定输入

- 源日志：`logs/benchmark_prefilter_routing_m3_5_6_20260407T025835Z.json`

## 失败集合口径（必须固定）

仅审计满足以下条件的 rows：

1. `routing_suggestion in {route_to_turbo, route_to_plus}`
2. 且满足任一：
   - `used_model_chain == false`
   - `validator_ok != true`
   - `fallback == true`

禁止把 `route_to_rule_or_reject` 的正常样本混入失败集合。

## 工具脚本

新增脚本：

- `tools/audit_model_chain_failures_m3_5_6a.py`

职责：

1. 读取 M3.5.6 日志
2. 只抽取上述 failure 口径的失败样本
3. 额外抽取 3～5 条成功对照样本（同为 turbo/plus；优先与失败 case 同类）
4. 输出 audit JSON + Markdown 表，便于贴附录

运行：

```bash
python3 tools/audit_model_chain_failures_m3_5_6a.py \
  --src-log logs/benchmark_prefilter_routing_m3_5_6_20260407T025835Z.json
```

输出（默认写到当前目录的 `logs/`）：

- `logs/audit_model_chain_failures_m3_5_6a_<UTC>.json`
- `logs/audit_model_chain_failures_m3_5_6a_<UTC>.md`

## 需要回答的问题（逐条）

对每条失败样本回答：

1. 模型原始返回体是否存在？
2. 原始 JSON 是否存在？
3. 原始 JSON 是否满足结构化要求？
4. 若有结果，为什么没被识别为 `used_model_chain=true`？
5. notes / metadata / route 标记是否与成功样本不同？
6. 是否存在 day 段特有的返回形态差异？
7. 12 条是否可归为同一种失败模式？

## 观测字段缺口与最小补充（如确有必要）

若仅凭 M3.5.6 `rows` 无法回答 1～4，则允许做最小 instrumentation（只加观测，不改逻辑，不默认开启，仅用于复现实验）：

- `raw_model_payload_present`
- `raw_json_present`
- `raw_json_top_level_keys`
- `model_chain_detection_reason`
- `model_chain_detection_failed_reason`

## 结果填写区（执行后补齐）

- audit 产物：`logs/audit_model_chain_failures_m3_5_6a_<UTC>.{json,md}`
- 失败样本是否都集中在 day：**待填**
- 是否可归为同一种失败模式：**待填**
- 失败更像 A 还是 B：**待填**

## 最终结论（只给一个明确结论）

### 结论（暂定）

**B（暂定）：现有证据更倾向于 model_chain 识别 / success tagging 口径问题为主，而非模型真失败为主。**

### 依据（来自 M3.5.6a 审计产物）

- **失败 12 条全部集中在 day**，night 段仍可全绿
- **失败分散于 11 个 case**，不集中在某一任务类型
- **同类 case 存在成功对照样本**（例如 `C1_mixed_nav`、`C2_mixed_health_nav`、`C3_ordered_itinerary_multistep`、`S4_simple_nav_longer`、`S5_simple_poi_longer`）
- 失败样本共同特征高度一致：
  - `used_model_chain=false`
  - `validator_ok=None`（validator 未被执行/未到达）
  - `fallback=true`
  - `backup_provider_used=false`
  - `provider_switch_reason` 为空
- 当前日志 **缺少** raw payload / raw json / detection reason 等关键证据字段，因此该结论仍需最小观测补证，不能 100% 排除 A 或混合态

### 下一步（M3.5.6b 最小观测补证；只加观测，不做修复）

目标只回答两个问题：

1. 失败时模型是否返回 payload / JSON？
2. 若返回了，为什么没有被识别为 `model_chain` 成功（`used_model_chain=true`）？

必补字段（仅用于复现实验，不进默认主链、只做 debug）：

- `raw_model_payload_present`
- `raw_json_present`
- `raw_json_top_level_keys`
- `model_chain_detection_reason`
- `model_chain_detection_failed_reason`

### 结论格式（补证完成后更新为最终版）

- 结论：**A / B / C（只选一个）**
- 下一步建议修哪一层：**待补证后填写**（识别/打标 vs provider/原始输出形态）
- 为什么：**待补证后填写**

