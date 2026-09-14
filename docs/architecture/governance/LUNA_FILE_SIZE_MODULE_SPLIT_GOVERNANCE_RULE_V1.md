# Luna File Size & Module Split Governance Rule v1

**File Size & Module Split Governance Rule** / **工程文件大小与模块拆分治理规则**

## 与 Reuse-First 的关系

本规则与 **Reuse-First Protocol Engineering Rule** 并列执行，本质相同：减少重复、减少臃肿、降低维护成本。

严谨不能靠堆文件和堆检查实现，应靠**标准化、复用、分层、边界清楚**来实现。

## 核心原则

- 单个工程文件不得承载过多职责
- 大常量、大矩阵、大协议表、大模板白名单、大 error code map、大 classification registry → 拆到 shared module 或独立数据产物
- `capability` / `runner` / `verifier` 不得变成 monolithic file
- 文件过大不仅影响维护，还会影响 Cursor 读取、diff、验证和排查（533s 超时即为例证）

## 阈值（Python）

| 级别 | 行数 | 动作 |
|------|------|------|
| 建议 | ≤ 600 | 默认目标 |
| Warning | > 800 | 必须在 summary 说明拆分理由 |
| Blocker candidate | > 1200 | 必须拆分或记录正式豁免理由 |

## 阈值（Markdown）

| 级别 | 行数 | 动作 |
|------|------|------|
| 建议 | ≤ 800 | 默认目标 |
| Warning | > 1200 | 考虑拆分 appendix |
| Blocker candidate | > 1800 | 建议主文档 + appendix |

## JSON 产物

- 不按行数硬卡
- 大 registry / matrix 必须 **index + detail files**
- verifier 默认优先读 `summary.json` / `verifier_report.json` / manifest / index

## 拆分规则

### capability

- 只保留阶段构建逻辑
- 大型 protocol / matrix / constants → shared module

### runner

- 只负责编排和写产物
- 不内嵌大量 schema / registry / 文档正文

### verifier

- 只做检查逻辑
- 不内嵌大型白名单、错误码全集、协议全集
- 大规则从 shared helper 或 registry/index 读取
- **禁止全库扫描**；历史大文件只读 index/summary

### template_lineage

- 不无限增长；按 family / domain / phase group 拆分
- 保留统一入口聚合

### protocol registry

- L1 / L2 / L3 分文件
- input / output / traceability / error-code 分文件
- index 只存摘要与引用

## 阶段指令默认附录（工程简洁约束）

```
工程简洁约束：
- 能复用 shared helper 就不复制
- 能 registry patch 就不新开长链
- 能轻量引用就不完整重验
- 能拆分文件就不堆进单文件
- verifier 读取 summary/index，不读超大文件
```

## 阶段产物

每阶段应生成 `file_size_governance_review_v1.json`。

## Verifier GO 键

- `file_size_governance_review_exists=true`
- `monolithic_file_absent=true`
- `large_file_read_avoidance_ok=true`
- `summary_index_first_reading_ok=true`
- `template_lineage_growth_controlled=true`
- `shared_constants_split_ok=true`
- `verifier_large_file_scan_absent=true`

## 机器可读定义

- `capabilities/midplatform/protocols/file_size_module_split_governance_rule_v1.py`
- `capabilities/midplatform/file_size_governance_v1.py`（限定目录扫描 helper，禁止全库 rglob）

## 不合规清单（待整改）

见 `LUNA_FILE_SIZE_GOVERNANCE_INVENTORY_V0.md`（仅记录，本阶段不修改代码）。
