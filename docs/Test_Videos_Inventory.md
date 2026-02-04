# 测试视频清单

项目根目录下 6 个测试视频的清单与选用建议，供 ACTIVE×视频、风险门禁、K/L 验证等测试时选用。

---

## 清单总表

| # | 文件名 | 时长 | 帧率 | 主要内容 | 推荐用途 |
|---|--------|------|------|----------|----------|
| 1 | `test_video.mp4` | （见文件） | 30fps | 通用/早期测试 | 通用冒烟、基础流程 |
| 2 | `test_video_complex_6m42s.mp4` | 6 分 42 秒 | 30fps | 复杂场景（多目标/丰富视觉） | 复杂度高、易触发 ENGAGED / K/L、长时跑测 |
| 3 | `test_video_empty_street_1m01s_60fps.mp4` | 1 分 1 秒 | 60fps | 基本空旷的马路和街道 | 低复杂度、L0/不介入、节流与 60fps 行为 |
| 4 | `test_video_follow_crowd_crossing_6m14s_60fps.mp4` | 6 分 14 秒 | 60fps | 跟随人群前进；1 次过马路（通过）+ 1 次等红绿灯（未通过） | 人群+过马路、中等复杂度、仲裁/节律 |
| 5 | `test_video_traffic_light_crossing_1m01s_60fps.mp4` | 1 分 1 秒 | 60fps | 等红绿灯、观察车流、过马路 | 车流+过马路、短时验证 |
| 6 | `test_video_park_pond_edge_2m01s_60fps.mp4` | 2 分 1 秒 | 60fps | 公园、草地、主要在水池边行走 | **危险/水边场景，测试是否触发安全警告** |

---

## 按测试目的选用

| 测试目的 | 推荐视频 | 说明 |
|----------|----------|------|
| 验证 K/L、arbitration、ENGAGED | `test_video_complex_6m42s.mp4` 或 `test_video_follow_crowd_crossing_6m14s_60fps.mp4` | 复杂度较高，易满足 eligibility，便于出现 engagement + 仲裁 + k/l |
| ACTIVE×视频 限时跑（如 120s） | 同上，或 `test_video_traffic_light_crossing_1m01s_60fps.mp4` | 需要一定复杂度才能进 ENGAGED |
| 低复杂度 / 全程 L0 | `test_video_empty_street_1m01s_60fps.mp4` | 空旷街道，适合验证“不介入”行为 |
| 风险/安全警告（水边、危险场景） | `test_video_park_pond_edge_2m01s_60fps.mp4` | 公园水池边，用于验证是否触发警告 |
| 60fps 节流与帧率行为 | 任意 `*_60fps.mp4` | 4 个 60fps 视频均可 |
| 长时稳定 / 压力 | `test_video_complex_6m42s.mp4`、`test_video_follow_crowd_crossing_6m14s_60fps.mp4` | 时长 6 分钟以上 |

---

## 路径与命令示例

- 路径：所有视频均放在项目根目录下，即 `/Users/luanlei/Desktop/Luna-2/`（或相对路径 `./`）。
- ACTIVE×视频 测试示例：
  ```bash
  python3 tools/run_active_video_test.py --video test_video_complex_6m42s.mp4 --seconds 120
  python3 tools/run_active_video_test.py --video test_video_park_pond_edge_2m01s_60fps.mp4 --seconds 130
  ```

---

*文档维护：新增或变更测试视频时请同步更新本清单与选用建议。*
