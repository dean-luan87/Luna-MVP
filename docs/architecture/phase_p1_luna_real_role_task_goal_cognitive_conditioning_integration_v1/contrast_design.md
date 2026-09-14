# Contrast Design

三组对照均使用同一个既有真实车站图片。每个 side 由现有
`RealOCRProviderExecutionEngineV1` 在 `LIVE_RUNTIME` 下独立取得真实 native OCR 结果，
再由 native content projection/fingerprint 检查等价性。独立执行是为了保留现有
Provider Request、Runtime Observation 与 Gateway execution identity 的完整性；不使用
recorded result。

## Goal

共同 Task 为既有回归 vocabulary `task:assess-target`。左侧目标是
`goal:locate-current-station`，需要 station location；右侧目标是
`goal:identify-platform-exit`，需要 platform direction。相同 OCR observation 因 active
Goal/Information Need 不同而具有不同 required information 与 sufficiency 结果。

## Task

共同 Goal/Information Need/Evidence 不变，使用既有回归 vocabulary：
`task:find-document` 与 `task:identify-exit`。预期差异出现在 hypothesis、relation
interpretation 或 attention-conditioned projection，不进入 Task Manager execution。

## Role

复用已有 `role:workspace-owner` 与 `role:visitor`。共同 Goal、Task、Information Need
和真实 OCR Evidence 不变；预期差异出现在 perspective/relation interpretation 或
relevance。Role 不得修改 provider native output、RuntimeObservation 或 Evidence payload。
