# LUNA — PaddleOCR Pinned Weights Result Matrix v0

## Phase

- Phase: **Phase-ModelOCR-003-Fix**
- Focus: PaddleOCR lightweight（ppocrv5 pipeline）det/rec/cls pinned readiness

## Result matrix（模板）

> 本文件是**结果矩阵模板**。实际运行后，将 readiness report 与 file-manifest 摘要填入。

| Item | det | rec | cls |
|---|---:|---:|---:|
| assets present | TBD | TBD | TBD |
| pinned status | TBD | TBD | TBD |
| file_count | TBD | TBD | TBD |
| total_file_size_bytes | TBD | TBD | TBD |
| hash recorded | TBD | TBD | TBD |
| hash verified (readiness) | TBD | TBD | TBD |
| source provenance recorded | TBD | TBD | TBD |

## Produced artifacts（应产出）

- File-manifest: `models/ocr/paddleocr_ppocrv5/model_files_manifest_v0.json`
- OCR manifest: `configs/models/ocr/paddleocr_ppocrv5_model_manifest_v0.json`
- Readiness report: `logs/ocr_model_readiness_paddleocr_ppocrv5_lightweight_zh_en_v0_*.json`

## Notes

- 本阶段不跑 OCR 推理；不输出识别结果样例；只做“权重固定+hash/size 可复现”。

