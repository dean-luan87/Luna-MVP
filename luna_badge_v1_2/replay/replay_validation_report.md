# replay_validation_report.md

## Summary
- replay_input: `luna_badge_v1_2/replay/examples/case_nav_turn_001.json`
- runs_fast: 5 (sleep_ms=0)
- runs_slow: 5 (sleep_ms=5)
- runner_version: `1.4.9-P0-2-C.1`
- git_commit: `83e8ce8c868878c7584dbcf2cb1a5ee8c238b12c`
- result: PASS

## Hashes

### fast
- 1. `525658dc08ea8c639823f7320e8d06cef00571b9e41953af6877ebbf35a2d1b4`
- 2. `525658dc08ea8c639823f7320e8d06cef00571b9e41953af6877ebbf35a2d1b4`
- 3. `525658dc08ea8c639823f7320e8d06cef00571b9e41953af6877ebbf35a2d1b4`
- 4. `525658dc08ea8c639823f7320e8d06cef00571b9e41953af6877ebbf35a2d1b4`
- 5. `525658dc08ea8c639823f7320e8d06cef00571b9e41953af6877ebbf35a2d1b4`

### slow
- 1. `525658dc08ea8c639823f7320e8d06cef00571b9e41953af6877ebbf35a2d1b4`
- 2. `525658dc08ea8c639823f7320e8d06cef00571b9e41953af6877ebbf35a2d1b4`
- 3. `525658dc08ea8c639823f7320e8d06cef00571b9e41953af6877ebbf35a2d1b4`
- 4. `525658dc08ea8c639823f7320e8d06cef00571b9e41953af6877ebbf35a2d1b4`
- 5. `525658dc08ea8c639823f7320e8d06cef00571b9e41953af6877ebbf35a2d1b4`

## Notes
- Replay 模式下禁止纳入 wall clock / uuid / thread id 等非确定性字段。
- FailSafe 资源探测（psutil CPU/MEM）在 Replay 证明口径中视为 non-deterministic，应跳过验证。

