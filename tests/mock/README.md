# Test 4 · 多任务并行仲裁 v0（Mock）

A–O 全链路测试验证方案中 **Test 4** 的可直接运行 mock 脚本。

## 覆盖层

- **G**：多任务并行仲裁（只选一个）
- **I**：跨 tick 公平性（长期不饿死）
- **J** / **O**：本 mock 不测（需 trace）

## 运行方式

```bash
# 直接运行（人工可读输出）
python3 tests/mock/test_multitask_arbitration_v0.py

# pytest
python3 -m pytest tests/mock/test_multitask_arbitration_v0.py -v

# 带 print 输出
python3 -m pytest tests/mock/test_multitask_arbitration_v0.py -v -s
```

## 通过 / 不通过判定

| 检查项 | 判定 |
|--------|------|
| SAFETY 出现必胜 | ❌ 否则不通过 |
| 同一 tick 多个 winner | ❌ 不通过 |
| TASK 60s 内一次都没赢 | ❌ 不通过 |
| winner 全是同一类型 | ❌ 不通过 |

## 正确结果特征

1. **Winner 分布**：NAVIGATION ≈ ENV_AWARENESS ≈ TASK_STATE，SAFETY 在 t=0,20,40 必赢
2. **TASK 至少赢 1 次**：Fairness 生效
3. **每 tick 只有一个 winner**：无多 winner
