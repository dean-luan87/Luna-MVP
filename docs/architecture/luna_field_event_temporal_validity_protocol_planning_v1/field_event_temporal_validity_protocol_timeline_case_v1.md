# Field Event and Temporal Validity Timeline Case: 小北门

## 1. 白天
- road active
- entrance_exit active
- night_market inactive

## 2. 傍晚
- recurrence_window_opened
- vendor evidence observed
- night_market candidate activated

## 3. 城管检查
- enforcement overlay started
- night_market suspended
- road and entrance remain active

## 4. 检查结束
- overlay ended
- 不自动恢复夜市
- request refresh evidence

## 5. 用户命名
- personal_name_asserted = 小北门
- valid until revoked
- personal scope only

## 6. 打车
- internet ride-hailing uses institutional/map naming
- local taxi conversation may use social/personal naming candidate

## Notes
- 同一 SpaceAnchor 在不同时间和任务下产生不同 Active Projection。
- 临时覆盖、周期规则和个人命名共存时，必须使用治理规则决定当前投影。
- 事件历史应保留完整 lineage，而不是删除旧候选。
