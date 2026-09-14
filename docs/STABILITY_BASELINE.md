# 稳定基线（Stability Baseline）

建立标准：两次同视频 A3 trace 经 `tools/determinism_guard.py` 对比 **0 差异**、输出 **PASS** 后，记录本文件并执行 `git add . && git commit -m "stability baseline established"`。

---

## 基线记录（维护者填写）

| 项 | 值 |
|---|-----|
| **Baseline Date** | （完成 determinism_guard PASS 的日期） |
| **Python Version** | Python 3.9.6 |
| **Commit Hash** | 8701c43be2d16db7bc9585dd426df30c97250692 |
| **File Count** | 2500 |
| **Determinism** | PENDING → 需在项目根放入 `test_video_complex_6m42s.mp4` 后执行下方流程并改为 PASS |
| **Test Video** | test_video_complex_6m42s.mp4 |

---

## 建立流程（执行顺序）

1. **放入视频**  
   将 `test_video_complex_6m42s.mp4` 置于项目根目录。

2. **生成两次 trace**  
   ```bash
   python3 tools/run_video_a3_trace.py \
     --video test_video_complex_6m42s.mp4 \
     --output trace_run1.jsonl
   ```
   再执行一次，输出改为 `trace_run2.jsonl`：
   ```bash
   python3 tools/run_video_a3_trace.py \
     --video test_video_complex_6m42s.mp4 \
     --output trace_run2.jsonl
   ```

3. **确定性验证（必须 0 差异）**  
   ```bash
   python3 tools/determinism_guard.py trace_run1.jsonl trace_run2.jsonl
   ```  
   验收：无 decision/safety_level/control_mode 差异，输出 PASS 或等价成功信息。若有 diff，立即停止，不提交基线。

4. **更新本文件**  
   将 **Determinism** 改为 `PASS`，**Baseline Date** 填当日，**Commit Hash** 改为执行 commit 后的 hash。

5. **提交基线**  
   ```bash
   git add .
   git commit -m "stability baseline established"
   ```

---

## 成功标志

- 两次 trace 完全一致  
- determinism_guard PASS  
- 基线已 commit  
- 文件数 < 3000（当前 2500）
