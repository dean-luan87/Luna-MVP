# LUNA — PaddleOCR Latency Breakdown Review v0

## Phase

- **Phase-ModelOCR-006C**

## Review scope

- provider init latency
- per-frame preprocess / inference / postprocess / normalization breakdown
- whether init-once is effective
- realtime-default eligibility guard (`realtime_default_not_allowed=true` if avg latency remains high)
