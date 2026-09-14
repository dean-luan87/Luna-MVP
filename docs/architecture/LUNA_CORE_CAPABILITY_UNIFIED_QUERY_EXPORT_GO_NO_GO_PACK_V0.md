# Phase-CoreCapability-TRW-Unified-004
# Unified Query / Export Go/No-Go Pack v0

**阶段目标**：为 Phase-003 unified shadow view 提供离线查询、过滤、导出能力（含字段级映射表）。

---

## GO 条件（全部满足）

- Phase-003 input root 可读
- query tool 可运行并生成 summary + results（json/jsonl/md）
- export tool 可运行并生成 capability/stage/hard_audit/missing_fields 表
- field-level mapping report 生成且为字段级（非结构统计）
- verifier 通过
- 不接 runtime、不重构、不修改 YOLO/OCR/Voice 原始链路

---

## CONDITIONAL_GO（允许但必须记录）

- 某些字段只能标记 missing/not_applicable，但 mapping report 披露完整

---

## NO_GO（任一触发即失败）

- 查询结果丢失 source refs / source_root
- field-level mapping 只做结构统计（缺字段级条目）
- hard audit 字段丢失或异常值出现
- 本阶段接 runtime 或修改原始链路或重构目录

