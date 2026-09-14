# 5 分钟以上测试视频 · 测试指令

两条视频均在**项目根目录**：

| 视频 | 时长 | 用途建议 |
|------|------|----------|
| `test_video_complex_6m42s.mp4` | 6 分 42 秒 | 标准 A3/vision trace、复杂度场景 |
| `test_video_follow_crowd_crossing_6m14s_60fps.mp4` | 6 分 14 秒 60fps | 跟车/人群过街、高帧率 |

---

## 1. A3 Trace（生成 + 分析）

**视频 1：6 分 42 秒**

```bash
cd /Users/luanlei/Desktop/Luna-2

python3 tools/run_video_a3_trace.py --video test_video_complex_6m42s.mp4
python3 tools/analyze_a3_trace.py logs/a3_trace.jsonl
```

**视频 2：6 分 14 秒**

```bash
cd /Users/luanlei/Desktop/Luna-2

python3 tools/run_video_a3_trace.py --video test_video_follow_crowd_crossing_6m14s_60fps.mp4
python3 tools/analyze_a3_trace.py logs/a3_trace.jsonl
```

可选：
- `--max-frames N`：只处理前 N 帧（快速试跑）
- `--frame-step N`：每隔 N 帧处理一帧
- `--simulate-active`：模拟 ACTIVE 任务态
- `--force-engaged`：强制 L1 engagement，仲裁与 P 层写入 trace

---

## 2. 主流程（main.py 视频模式）

**视频 1**

```bash
cd /Users/luanlei/Desktop/Luna-2
python3 main.py --video test_video_complex_6m42s.mp4
```

**视频 2**

```bash
cd /Users/luanlei/Desktop/Luna-2
python3 main.py --video test_video_follow_crowd_crossing_6m14s_60fps.mp4
```

带 L1/L2 测试时：

```bash
python3 main.py --video test_video_complex_6m42s.mp4 --force-engaged-test
python3 main.py --video test_video_complex_6m42s.mp4 --force-engaged-test --force-engaged-test-l2
```

---

## 3. Active 视频测试（LunaBadgeMVP 整链）

**视频 1**

```bash
cd /Users/luanlei/Desktop/Luna-2
python3 tools/run_active_video_test.py --video test_video_complex_6m42s.mp4 --seconds 120
```

**视频 2**

```bash
cd /Users/luanlei/Desktop/Luna-2
python3 tools/run_active_video_test.py --video test_video_follow_crowd_crossing_6m14s_60fps.mp4 --seconds 120
```

---

## 4. B2 v0.5 视频 Trace

**视频 1**

```bash
cd /Users/luanlei/Desktop/Luna-2
python3 tools/run_v05_video_test.py test_video_complex_6m42s.mp4
```

**视频 2**

```bash
cd /Users/luanlei/Desktop/Luna-2
python3 tools/run_v05_video_test.py test_video_follow_crowd_crossing_6m14s_60fps.mp4
```

---

## 5. PQRS 链验证（需先有 trace）

```bash
cd /Users/luanlei/Desktop/Luna-2
python3 main.py --video test_video_complex_6m42s.mp4 --force-engaged-test
python3 tools/verify_chain_pqrs_v0.py
```

---

## 6. D0.1 Headless Parity（需已有 episode）

Headless 重放依赖 `library_store/.../records.jsonl`。若 episode 由**真实视频跑 main 并落盘**得到，则用对应 episode 路径：

```bash
# 假设 episode 路径为 v1.1/episodes/YYYYMMDD/session-id/EPISODE_ID
EPISODE_PATH="v1.1/episodes/YYYYMMDD/session-id/EPISODE_ID"

python3 tools/run_a3_headless_replay.py --base-dir library_store --version-tag v1.1 \
  --episode "$EPISODE_PATH" --patch patches/empty_patch.json --out-dir outputs

python3 tools/test_a3_headless_parity.py --episode "$EPISODE_PATH" --base-dir library_store \
  --candidate outputs/v1.1/headless_parity/EPISODE_ID/empty_patch/candidate_decisions.jsonl \
  --out-dir outputs/v1.1/headless_parity/EPISODE_ID/empty_patch
```

当前两条长视频若尚未接入「视频 → episode 落盘」流水线，可先用 `library_store` 里已有 episode（如 SPEECH_12）做 D0.1 验收；待流水线打通后再用这两条视频生成的 episode 跑上述命令。
