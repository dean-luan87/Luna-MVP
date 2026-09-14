# Real Observation Binding

当前唯一 Provider 是 canonical `text_recognition` → `ocr_v1`，native
implementation 是 RapidOCR / ONNXRuntime。两轮输入均为仓库已有 local PNG：

| Binding | Source | Information contribution |
|---|---|---|
| station | `capabilities/test_assets/p1/ocr/ocr_real_image_subway_station_longtan_temple_v1_001.png` | `information:station-location-text:v1` |
| platform | `capabilities/test_assets/p1/ocr/ocr_real_image_subway_platform_jiahuihu_v1_001.png` | `information:platform-location-text:v1` |

source path 在 Runner 中解析为 repository-local absolute path；binding ref、
source region ref 和 Provider request/source lineage 一并保留。没有网络下载、
人工 crop 文件、硬编码 OCR 文本或 recorded result。
