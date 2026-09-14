# Luna — Better Frame Selection Runtime v1 GO/NO_GO Pack v0

## GO

- 27 deferred crop items 全部 intake
- `better_frame_candidate` 生成；`selection_planning_only=true`
- `new_video_decoded=false`；`new_frame_extracted=false`；`roi_crop_executed=false`
- `boundary_ok=true`；`verifier=GO`

## CONDITIONAL_GO

- 部分 item 为 `neighboring_frame_required` / `future_detector_required` / `unavailable`，但 routing 与 future plan 完整

## NO_GO

- 解码新视频或抽新帧；执行 crop；生成 OCRRequest；调用 provider
- 写 fact/WM/Scene Delta；benchmark claim；改 routing；audit 缺失
