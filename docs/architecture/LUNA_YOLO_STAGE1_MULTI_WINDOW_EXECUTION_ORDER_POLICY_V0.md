# LUNA YOLO Stage-1 Multi-Window Execution Order Policy v0

**Phase**：Phase-Mainline-GuardedTrial-006

---

## 1. 允许的窗口序列

只允许 **`[50]`、`[50,100]`、`[50,100,200]`** 或其前缀（必须为 **50→100→200** 的单调前缀）。例如禁止单独请求 **`100`** 或 **`50,200` 跳过 100**。

实现：`validate_yolo_multi_window_input_v0`。

---

## 2. 串行与闸门

执行顺序：**50 → 100 → 200**（按请求的子序列）。禁止并发窗口。

| 规则 | 行为 |
|------|------|
| 50 非 `GO_next_window` | 不得启动 100；后续窗口记入 **skipped**，**立即停止**序列化扩展 |
| 100 非 `GO_next_window` | 不得启动 200；同上 |
| 任一 **`NO_GO_rollback_and_fix`** 或 **`abort_triggered`** | **停止**，更大窗口一律不跑 |
| 任一 **`CONDITIONAL_GO_repeat`** | **停止**；只允许人工 **重复当前窗口**，**禁止**引擎自动升级到更大窗口 |

---

## 3. 与 Phase-005 的关系

每一窗格独立调用 Phase-005 执行核（可变 `max_frames`），从零时刻顺序读取离线文件的前 **N** 帧；每窗重建 detector（v0 实现，后续可优化为单加载多窗）。
