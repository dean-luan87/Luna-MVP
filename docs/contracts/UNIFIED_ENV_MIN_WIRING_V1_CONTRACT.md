# unified_env_min_wiring_v1 — 最小链路契约（Freeze）

**文件**：`docs/contracts/UNIFIED_ENV_MIN_WIRING_V1_CONTRACT.md`  
**性质**：工程基线（冻结当前**可运行**的 min wiring 观测链路）；**不是**完整架构说明。  
**关联实现**：`capabilities/voice/runtime/voice_final_text_dispatcher.py`、`tools/analyze_unified_env_min_wiring_v1.py`、`tools/smoke_compare_unified_env_min_wiring_v1.py`

---

## 1. 文档目的

- 将 **unified_env_min_wiring_v1** 已确认的最小输入、输出、兼容规则与验收方式写成**可回归**的契约，供后续改动对照。
- 读者预期：改 snapshot、analyzer 或 smoke 前，先对照本文；破坏性变更须同步更新本文与回归命令。

---

## 2. 主链 snapshot 输出契约

| 项 | 内容 |
|----|------|
| **开关** | `LUNA_ENABLE_UNIFIED_ENV_MIN_WIRING_SNAPSHOT_V1`（默认关闭；`1` / `true` / `yes` 开启） |
| **输出路径** | 环境变量 `LUNA_UNIFIED_ENV_MIN_WIRING_SNAPSHOT_V1_JSONL`；未设置时默认 **`logs/unified_env_min_wiring_snapshot_v1.jsonl`**（相对当前工作目录） |
| **写盘时机** | `dispatch_voice_final_text` 内，在 **`_maybe_attach_unified_env_fill_shadow_v1` 之后**（与既有 `unified_env_shadow_snapshot` 写盘时机独立，不得混用） |

**每行 JSON（envelope）结构：**

```json
{
  "type": "unified_env_min_wiring_snapshot",
  "data": {
    "timestamp": "<float, host wall>",
    "event_timestamp": "<float, 事件时间>",
    "related_request_id": "<string>",
    "metadata": { }
  }
}
```

- **`data.metadata`**：按白名单从 `runtime_context.metadata` 拷贝**已存在且为 dict** 的键（当前至少覆盖）：`sidewalk_env_summary_v1`、`retail_env_summary_v1`、`unified_env_summary_shadow_v1`、`unified_env_fill_shadow_v1`。
- **关键观测目标**：**`metadata.unified_env_fill_shadow_v1`**（`fill_applied`、`filled_fields`、`fill_blocked_reason` 等离线分析依赖此项；缺 fill 则 min wiring 窗口不完整）。

---

## 3. analyzer 输入契约

**工具**：`tools/analyze_unified_env_min_wiring_v1.py`

须**同时兼容**下列两种**单行**格式（不改变统计口径与 JSON/MD 输出结构）。

### 3.1 Flat row

```json
{
  "id": "...",
  "event_timestamp": 123.0,
  "metadata": { }
}
```

### 3.2 Envelope row（与主链 snapshot 一致）

```json
{
  "type": "unified_env_min_wiring_snapshot",
  "data": {
    "related_request_id": "...",
    "event_timestamp": 123.0,
    "metadata": { }
  }
}
```

（`data` 内亦可含 `timestamp`；主链当前使用 **`related_request_id`** 作为请求关联 id。）

### 3.3 归一化规则（加载后内部统一）

| 字段 | 规则 |
|------|------|
| `id` | `row.id` **或** `row.related_request_id`（envelope 时 `row` = `data`） |
| `event_timestamp` | `row.event_timestamp` |
| `metadata` | `row.metadata`（须为 dict，否则该行跳过） |

### 3.4 坏行处理

以下情况**整行跳过**、不中断进程：非法 JSON、解析结果非 dict、`type` 为 `unified_env_min_wiring_snapshot` 但 `data` 非 dict、缺失 `metadata` 或 `metadata` 非 dict。

---

## 4. 当前已验证的业务闭环（本地）

以下链路已在真实执行中跑通（含 fill 写入 snapshot 与 analyzer 消费）：

- **`unified_env_fill_shadow_v1`** 由 `voice_final_text_dispatcher.py` 在开启相应实验开关时写入 metadata，并在 **fill 之后** 由 min wiring snapshot 落盘。
- 产出 **`logs/unified_env_min_wiring_snapshot_v1.jsonl`**（envelope 行）。
- **analyzer 可直接读取 envelope**，无需手工扁平化。
- **envelope 与手工 flat 窗口**对同一语义内容的**关键统计一致**（见第 5 节 smoke）。
- **回归脚本**：`tools/smoke_compare_unified_env_min_wiring_v1.py`（对比两次 analyzer 的 JSON 结果）。

---

## 5. 最小验收命令

在 **Luna-Core 仓库根目录**执行：

```bash
python3 tools/smoke_compare_unified_env_min_wiring_v1.py \
  --envelope-jsonl logs/unified_env_min_wiring_snapshot_v1.jsonl \
  --flat-jsonl logs/window_real_unified_env_min_wiring_round02.jsonl
```

**通过标准**：

- 进程 **exit code 0**；
- 标准输出包含：**`OK: envelope and flat results match`**。

（`flat` 文件须与 envelope 表示**同一语义窗口**的扁平对照样例；路径可按环境调整，但命令形态保持不变。）

---

## 6. Freeze 边界

以下内容视为**当前冻结**；若改动须**同步更新本文档**并跑通第 5 节 smoke，禁止静默破坏：

- snapshot 行的 **`type`** 字符串：`unified_env_min_wiring_snapshot`；
- **`data.metadata`** 作为分析载荷的承载方式（白名单键集合的演进须在本文或附录中可追溯）；
- **analyzer 对 flat + envelope 双格式**的兼容与归一化规则；
- **smoke 脚本**对「两次 analyzer JSON 关键字段一致」的最小验收职责。

---

## 7. 依赖开关备忘（非本文 freeze 对象，仅便于复现）

主链要出现完整 fill 再落 snapshot，通常还需与现有实验一致地开启 **unified shadow** 与 **min wiring fill** 相关开关（以代码与环境变量为准）；本文不展开业务默认值，以免与实现漂移。
