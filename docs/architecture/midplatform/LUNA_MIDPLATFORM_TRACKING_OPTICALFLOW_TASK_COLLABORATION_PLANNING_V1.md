# Luna Midplatform — Tracking / Optical Flow Task Collaboration Planning v1

## Scope

Task collaboration planning only. Defines how Tracking / Optical Flow participates in 2–3 model task groups under midplatform control.

## Task Model Groups

1. road_crossing_safety — YOLO + Depth + Tracking
2. moving_obstacle_avoidance — YOLO + Depth + Tracking
3. find_moving_object — YOLO + Tracking + Depth optional
4. return_to_location_context — SLAM + YOLO + Tracking optional

## Prohibited

- Task Reasoning execution
- Action / navigation output
- World model assembly
- Real tracker / optical flow execution
