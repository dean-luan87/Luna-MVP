# A3 / ACTIVE 测试与视频验证流程（v0）

## 一、单元测试（先跑）

在项目根目录执行：

```bash
# 1. ENGAGED 失败诊断（D）
python3 -m pytest tests/test_engaged_failure.py -v

# 2. 多任务仲裁 mock（Test 4）
python3 -m pytest tests/mock/test_multitask_arbitration_v0.py -v

# 3. Shadow 上传与聚合
python3 -m pytest tests/test_shadow_upload_v0.py -v

# 4. 一次性跑完上述
python3 -m pytest tests/test_engaged_failure.py tests/mock/test_multitask_arbitration_v0.py tests/test_shadow_upload_v0.py -v
```

---

## 二、测试视频快速验证（验证流程）

用**少量帧**跑一遍，确认无报错、trace 正常、engaged_failure 有具体原因（非全 FAIL_UNKNOWN）。

```bash
# Shadow 模式，200 帧，每 5 帧处理一次（约 1 分钟内跑完）
A3_SHADOW_MODE=1 python3 tools/run_video_a3_trace.py \
  --video test_video_complex_6m42s.mp4 \
  --simulate-active \
  --max-frames 200 \
  --frame-step 5
```

**检查：**

- 终端最后出现：`处理完成: processed=200, trace=.../logs/a3_trace.jsonl`
- 分析 trace 看 ENGAGED 失败原因分布（应出现 FAIL_ARBITRATION_LOST / FAIL_COOLDOWN_ACTIVE 等，而非全 FAIL_UNKNOWN）：

```bash
# 注意：关键词是「ENGAGED 失败回退诊断」（中间无空格）
python3 tools/analyze_a3_trace.py logs/a3_trace.jsonl 2>/dev/null | grep -A 20 "ENGAGED 失败回退诊断"
```

---

## 三、真实视频完整跑（完整 6m42s）

确认快速验证无问题后，跑**完整视频**、不限制帧数：

```bash
# Shadow 模式，完整视频，每帧都处理（约 6 分 42 秒视频，耗时视机器而定）
A3_SHADOW_MODE=1 python3 tools/run_video_a3_trace.py \
  --video test_video_complex_6m42s.mp4 \
  --simulate-active
```

若机器较慢，可加 `--frame-step 2` 或 `--frame-step 5` 降采样：

```bash
A3_SHADOW_MODE=1 python3 tools/run_video_a3_trace.py \
  --video test_video_complex_6m42s.mp4 \
  --simulate-active \
  --frame-step 5
```

---

## 四、分析 trace（完整跑之后）

```bash
# 文本报告（含 ENGAGED 失败分布、节律、仲裁等）
python3 tools/analyze_a3_trace.py logs/a3_trace.jsonl

# 若报 matplotlib 错误，可只看文本部分
python3 tools/analyze_a3_trace.py logs/a3_trace.jsonl 2>/dev/null
```

CSV 会写入 `logs/a3_metrics.csv`。

---

## 五、推荐执行顺序（一句话）

1. **单元测试** → `pytest tests/test_engaged_failure.py tests/mock/test_multitask_arbitration_v0.py tests/test_shadow_upload_v0.py -v`
2. **快速视频验证** → `A3_SHADOW_MODE=1 python3 tools/run_video_a3_trace.py --video test_video_complex_6m42s.mp4 --simulate-active --max-frames 200 --frame-step 5`
3. **看失败诊断** → `python3 tools/analyze_a3_trace.py logs/a3_trace.jsonl 2>/dev/null | grep -A 20 "ENGAGED 失败回退诊断"`（关键词中间无空格；若 200 帧内未进入 ENGAGED，本节会无输出，属正常）
4. **完整视频** → `A3_SHADOW_MODE=1 python3 tools/run_video_a3_trace.py --video test_video_complex_6m42s.mp4 --simulate-active`
5. **完整分析** → `python3 tools/analyze_a3_trace.py logs/a3_trace.jsonl`
