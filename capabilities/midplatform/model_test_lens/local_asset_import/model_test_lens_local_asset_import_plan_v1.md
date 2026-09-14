# Model Test Lens — Local Asset Import Plan V1

## 定位

Model Test Lens **可以是测试入口，不能是模型执行器**。

## 页面允许

- 选择本地 image / video / frame_sequence / audio / text
- 生成 `local_test_asset_manifest`
- 生成 `model_test_job_request`
- 生成 `runner_bridge_request`
- 展示 runner 输出经 adapter 后的 envelope
- 展示 TestBoard refs

## 页面禁止

- 直接调用模型 / inference
- 启动 SLAM / OCR / SAM / TTS 后端
- runtime server / output adapter / registry / fact / semantic / navigation

## 资产类型

见 `local_asset_import_types_v1.py` 中 `ASSET_TYPE_MODEL_MAP`。

## Schema

- `schemas/local_asset_import/local_test_asset_manifest_schema_v1.json`
- `schemas/local_asset_import/model_test_job_request_schema_v1.json`

## TestBoard

asset import 与 job request 均须写入 TestBoard，protected + non-deletable。

## 本阶段

**Planning only** — 不实现真实导入，不读取新媒资作为模型输入。
