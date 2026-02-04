# perf_baseline_1_4_9.md

## Test environment
- **git_commit**: `ef5814bd2c33a439cecbe356a0a2d51c31d7ba73`
- **os**: `macOS-26.1-arm64-arm-64bit`
- **python**: `3.9.6 (default, Aug  8 2025, 19:06:38)  [Clang 17.0.0 (clang-1700.3.19.1)]`
- **cpu**: `arm`
- **ram_bytes**: `19327352832`
- **peak_rss_bytes (process ru_maxrss)**: `19480576`

## Method
- Baseline is collected by repeatedly running replay mode (no optimization).
- Input case: `luna_badge_v1_2/replay/examples/case_nav_turn_001.json`
- Runs: `200` (set via env `PERF_RUNS`, default=200)

### Metric definitions (auditable)
- **DecisionPipeline E2E latency (replay-step)**: per-step wall time from step processing start → end (includes decision/scheduler/tts routing event generation).
- **TTS first-frame latency (queue entry)**: wall time of `facade.emit(...)` call until enqueue/suppress decision completes (no real audio).
- **RSS peak**: `resource.getrusage(...).ru_maxrss` converted to bytes (Darwin bytes, Linux KB×1024).

## Results

### DecisionPipeline E2E latency (replay-step, wall µs)
- P50: `1`
- P95: `20`
- P99: `24`

### TTS first-frame latency (enqueue, wall µs)
- P50: `7`
- P95: `10`
- P99: `32`

### Replay run total time (wall ms)
- P50: `0.134`
- P95: `0.235`

## Degradation redlines (definition only)
- **Rule**: P95 must not exceed baseline +20%.
- replay-step P95 redline (µs): `24`
- tts enqueue P95 redline (µs): `12`

## How to reproduce

### Collect baseline
```bash
PERF_RUNS=200 python3 luna_badge_v1_2/tools/perf_baseline_1_4_9.py
```

### Determinism regression gate (must stay green)
```bash
python3 luna_badge_v1_2/tools/replay_gate.py --cases luna_badge_v1_2/replay/examples/case_nav_turn_001.json --runs 5
```

## 30-minute stability (manual/assisted)
- Recommended manual procedure (no automation guarantee in CI):
  - Run the gate loop for >=30 minutes and keep logs as evidence.
  - Suggested command (shell loop):
```bash
end=$((SECONDS+1800)); while [ $SECONDS -lt $end ]; do python3 luna_badge_v1_2/tools/replay_gate.py --cases luna_badge_v1_2/replay/examples/case_nav_turn_001.json --runs 1 || break; done
```

