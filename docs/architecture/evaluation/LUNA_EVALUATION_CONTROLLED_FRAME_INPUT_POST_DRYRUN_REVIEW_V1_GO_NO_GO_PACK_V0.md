# Luna Evaluation — Controlled Frame Input Post-DryRun Review v1 GO / NO-GO Pack

对应 phase：`Phase-Controlled-Frame-Input-Post-DryRun-Review-v1-001`

## GO Conditions

- required roots 全部成功加载
- input root review 已生成
- scenario coverage review 已生成且 `reviewed_scenario_count>=14`
- `accepted_candidate_count>=5`
- `rejected_candidate_count>=6`
- `restricted_candidate_count>=1`
- `stale_archive_only_candidate_count>=1`
- `source_chain / timestamp / privacy_tags` 硬门槛全部验证通过
- `frame_to_ocr_requires_visual_focus=true`
- `frame_to_tracking_requires_visual_focus=true`
- `frame_to_world_observation_requires_policy=true`
- `live_camera / device_camera / external_stream` 当前全部仍被拒绝
- `dual_device / dual_model / failover / multi_input_fusion` 当前全部 runtime 禁止
- 不存在 runtime / write / action / speech 越权
- closure readiness 明确指向 `Phase-Controlled-Frame-Input-Closure-v1-001`

## NO_GO Conditions

- 任一 required root 缺失
- 任一 required review 产物缺失
- `reviewed_scenario_count<14`
- 缺少指定 14 个 dry-run 场景中的任意一个
- `accepted_candidate_count<5`
- `rejected_candidate_count<6`
- `restricted_candidate_count<1`
- `stale_archive_only_candidate_count<1`
- `source_chain / timestamp / privacy_tags` 其中任一不再是硬门槛
- frame 可直接进入 OCR provider / tracking runtime / NavigationAction / SpeechOutput
- frame 可写 `WorldModel / Memory / Fact`
- dual-device placeholder 被误放开到 runtime
- 建议下一阶段不是 `Closure`

## GO Meaning

本阶段 `GO` 的语义仅表示：

- Luna 已正式完成 `Controlled Frame Input Planning + DryRun` 的 post-dryrun 审查
- Luna 已确认 metadata dry-run 的候选链与边界是稳定的
- Luna 已确认下一步应先进入 `Closure` 收口，而不是扩大到 controlled sample planning

本阶段 `GO` 不表示：

- 真实图像内容已读取
- `live camera` 已开放
- 视觉模型已调用
- OCR provider 已调用
- tracking runtime 已调用
- dual-device runtime 已开放
- failover 已实现
- multi-input fusion 已实现
- `WorldModel / Memory / Fact / Library` 已开放写入

## Next Phase

本阶段通过后，只允许推荐：

- `Phase-Controlled-Frame-Input-Closure-v1-001`

Closure 也必须继续保持：

- no real image content read
- no live camera
- no device camera
- no external stream
- no model runtime
- no dual-device runtime
- no failover
- no write
