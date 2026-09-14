# 暂停期完整校验包（Runbook v1.0）

**状态：** Frozen / Execute-Only  
**用途：** 暂停期架构完整性校验（不改代码，只执行）

---

## 0. 环境自检
```bash
python3 -V
```

---

## 1. B / C / Risk / Explain 单层不变式
```bash
python3 -m pytest tests/invariants -v
```

---

## 2. Explain 层无害性
```bash
python3 -m pytest tests/explain_layer -v
```

---

## 3. Risk → 决策隔离
```bash
python3 -m pytest tests/test_risk_bc_integration.py -v
```

---

## 4. Freeze 世界回放一致性
```bash
python3 -m pytest tests/freeze -v
```

---

## 5. RA-View 后视性
```bash
python3 -m pytest tests/observe -v
```

---

## 6. 人工审查（DebugView 导出）
说明：
- `dump_debug_view.py` 使用 **位置参数** `path`，不是 `--input`
- `run_from_fixtures.py` 支持 `--fixtures` 目录或单文件
- 若需包含 `debug_view`，必须加 `--enable-debug-view`

### 6.1 生成样本（单个 fixture）
```bash
python3 tools/run_from_fixtures.py \
  --fixtures tests/freeze/fixtures/F-02_static_obstacle_approaching.json \
  --enable-debug-view \
  --out runs/debug_sample.jsonl
```

### 6.2 导出 DebugView
```bash
python3 tools/debug/dump_debug_view.py runs/debug_sample.jsonl
```

---

## 判定标准（简表）
- 全部 pytest 通过 → ✅
- DebugView 输出中无控制语义 → ✅
- 如果输出容易被误解为“决策” → 需要进一步瘦身
