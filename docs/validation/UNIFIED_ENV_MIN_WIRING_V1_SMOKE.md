# unified_env_min_wiring_v1 — Smoke 验收入口

## 目的

本 smoke 用于验证 **unified_env_min_wiring_v1** 的 **analyzer 双格式兼容**未被破坏：

- **flat row**（扁平行）
- **envelope**（`type="unified_env_min_wiring_snapshot"` 的包裹行）

若该 smoke 失败，通常意味着：

- flat / envelope 的统计口径可能发生漂移，或
- `tools/analyze_unified_env_min_wiring_v1.py` 的双格式兼容被破坏，或
- snapshot 结构（`type` / `data` / `metadata` 承载方式）被改动但未同步更新 analyzer。

## 输入

- **envelope**：`logs/unified_env_min_wiring_snapshot_v1.jsonl`
- **flat**：`logs/window_real_unified_env_min_wiring_round02.jsonl`

## 固定验收命令

```bash
python3 tools/smoke_compare_unified_env_min_wiring_v1.py \
  --envelope-jsonl logs/unified_env_min_wiring_snapshot_v1.jsonl \
  --flat-jsonl logs/window_real_unified_env_min_wiring_round02.jsonl
```

## 通过标准

- 进程 **exit 0**
- 输出包含：

```text
OK: envelope and flat results match
```

