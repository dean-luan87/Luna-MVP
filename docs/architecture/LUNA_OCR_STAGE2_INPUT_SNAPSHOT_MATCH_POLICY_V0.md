# LUNA — OCR Stage-2 Input Snapshot Match Policy v0

## Phase

- **Phase-Mainline-GuardedTrial-011**

## Rule

Phase-011 只允许使用 Phase-010 approval root 冻结的 input image：

- path（resolved）一致
- sha256 一致
- size_bytes 一致

若不一致：

- `trial_verdict = NO_GO`
- **不得调用** OCR provider

