# Phase-Voice-OutputGovernance-008

# Governed Submit RequestTrace Test Matrix v0

## A. 输入可读

- A1：submit shadow root 可读（含 decisions）
- A2：voice request trace root 可读（含 chains）

## B. 产物

- B1：enhanced chains 生成
- B2：`governed_submit_shadow_gate` stage 出现
- B3：两种 gate position 均有记录（跨全量 matrix）
- B4：trace/replay/whitebox JSONL 非空

## C. Join

- C1：`request_id` join 成功数 > 0
- C2：无法 join 的 decision 记入 unmatched（如有）

## D. Hard audit

- `real_submit_invoked` 为 false 或缺失视为 shadow 安全边界内可接受
- `real_tts_invoked=false`、`playback_invoked=false`、`provider_invoked=false`
- `navigation_action=null`、`downstream_invocation_count=0`

## E. 禁止项

- 不接真实 submit、不改 Phase-005 磁盘文件、不删旧 stage
