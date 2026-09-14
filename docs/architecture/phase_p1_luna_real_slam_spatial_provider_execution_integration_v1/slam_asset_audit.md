# SLAM / Spatial Asset Audit

## 审计分类

| 资产 | 静态分类 | 依据 |
|---|---|---|
| `capabilities/midplatform/model_test_lens/local_runner_bridge/runners/slam_video_limited_runner_v1.py` | `CONTROLLED_ONLY` | 明确标注 no real ORB-SLAM backend；只读取 video metadata，返回 `trajectory=None` |
| `slam_limited_runner_to_envelope_adapter_v1.py` | `CONTROLLED_ONLY` | 只把 limited runner 结果包装成 envelope；`suitable_for_runtime_admission=false` |
| `slam_spatial_mapping_model_smoke_runner_v1.py` | `CONTROLLED_ONLY` | smoke / blocked classification；源码明确 no production runtime、no camera、no download |
| `slam_spatial_mapping_adapter_core_v1.py` | `CONTROLLED_ONLY` | 使用 mock frame、smoke inspection artifact 和 candidate builder；不是 native backend |
| `spatial_mapping_output_normalizer_v1.py` | `CONTROLLED_ONLY` | inspection-based candidate normalizer，可读取 cached/stub payload；不能证明真实 SLAM 输出 |
| `slam_adapter_contract/` | `SCHEMA_ONLY` / `CONTROLLED_ONLY` | adapter contract 与静态 validator；不启动 backend |
| `slam_spatial_evidence_adapter/` | `CONTROLLED_ONLY` | candidate mapping；validator 明确 mock backend / no real SLAM |
| `rtab_map_*_real_file_loader*` | `RECORDED_ONLY` | 离线 export/file parser；明确不读 RTAB database、不接 ROS、不启动 live runtime |
| `generic_tum_*`、`generic_json_spatial_trace_*` | `RECORDED_ONLY` | TUM/JSON trajectory 或 spatial trace 文件解析、replay |
| `slam_backend_integrated_output_replay_dryrun/` | `RECORDED_ONLY` | ORB-SLAM3/OpenVINS/Kimera 等均为 output replay sample 或 stub |
| `model_test_lens/standards/slam/` | `SCHEMA_ONLY` | input/output schema、ATE/漂移/稳定性指标和评分标准 |
| `model_test_lens/examples/slam_orb_luna_street_scene_*` | `SCHEMA_ONLY` | envelope example，不是 backend output execution |
| `capabilities/midplatform/core/.../fixtures_v1.py` SLAM cases | `RECORDED_ONLY` | provider-result / RuntimeObservation fixture；不调用 Provider |
| `Observation Gateway` `SLAM_SPATIAL` path | `SCHEMA_ONLY` / `CONTROLLED_ONLY` | Gateway 支持 spatial ingress，但没有 real SLAM source |
| `_eval_out` 历史结果 | `RECORDED_ONLY` | 仅历史运行证据参考，不作为 canonical source |
| 本地真实 SLAM/VIO backend | `UNAVAILABLE` | 未发现 ORB-SLAM、RTAB-Map、OpenVINS、VINS、Kimera 等可调用实现 |

## 关键发现

1. `slam_spatial_mapping_model_smoke_io_inspection_items_v1.py` 的默认矩阵明确为：
   `local_slam_runner_available=false`、`local_slam_weights_available=false`、
   `slam_dependencies_available=false`、`camera_runtime_authorized=false`、
   `video_stream_authorized=false`。cached output 和 adapter stub 可用，但二者都
   明确不是 real run。
2. `slam_video_limited_runner_v1.py` 只读取文件统计信息，不处理视频帧，也不产生
   trajectory；其消息明确 real ORB-SLAM/VINS/Kimera 未连接。
3. RTAB-Map 资产主要是 real file loader / export parser。其治理字段明确
   `no_rtabmap_runtime`、`no_ros_runtime`、`no_live_camera`、`no_live_imu` 和
   `no_provider_runtime_activation`。
4. ORB-SLAM3、OpenVINS、Kimera 和 Hydra 只以 sample/stub/replay 形式出现，未发现
   native library、binary、process launcher 或真实输入 dispatcher。
5. 仓库没有发现 SLAM 专用视频、RGB-D、stereo、bag、database 或 sensor sequence
   asset；现有真实图片是单帧 Vision/OCR 资产，不能替代 SLAM 时序输入。

## 结论

`REAL_EXECUTABLE`：0。
`CONTROLLED_ONLY`：存在。
`RECORDED_ONLY`：存在。
`SCHEMA_ONLY`：存在。
`UNAVAILABLE`：真实 SLAM/VIO execution path。
