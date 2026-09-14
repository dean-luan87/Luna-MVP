# LUNA YOLO Stage-1 Multi-Window Test Matrix v0

**Phase**：Phase-Mainline-GuardedTrial-006

---

## 1. CLI / 闸门

| ID | `--windows` | 期望 |
|----|-------------|------|
| M-006-01 | `50` | 合法前缀 |
| M-006-02 | `50,100` | 合法前缀 |
| M-006-03 | `50,100,200` | 全长链 |
| M-006-04 | `100` | **拒绝**（非前缀） |
| M-006-05 | `50,200` | **拒绝**（跳过 100） |

---

## 2. 运行时行为

| ID | 条件 | 期望 |
|----|------|------|
| M-006-10 | baseline 非 GO | 不执行任意扩展窗；`stop_reason` 明示 baseline |
| M-006-11 | `--input-video` 与 baseline 摘要路径不一致（resolve） | 不执行；视频 mismatch |
| M-006-12 | 50 → NO_GO | 100/200 **skipped**，立即停止 |
| M-006-13 | 50 → CONDITIONAL | 不得跑 100/200 |
| M-006-14 | 50/100 GO，100 后 eof 导致 CONDITIONAL | 200 **不跑**，最终 CONDITIONAL |

---

## 3. Verifier（`tools/verify_yolo_stage1_multi_window_offline_trial_v0.py`）

覆盖：`A-U`（产物齐备）、baseline 可读且状态 GO、离线视频 gate、执行顺序、gating (`F/G`)、帧数上界、`hard_audit`、`TRW` 非空、**`final_recommendation`** 存在等。
