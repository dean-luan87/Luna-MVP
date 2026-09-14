# LUNA Evaluation — PaddleOCR Current API Model Cache Layout v0（Phase-PaddleOCR-ManifestV1-CachePrepare-001）

## 推荐 `model_root`（默认）

**绝对路径**：`/Users/luanlei/LunaRuntime/models/ocr/paddleocr_current_api_v1`（可通过 `--model-root` 覆盖）。

本目录 **不在本 phase 自动创建**为“成功态”；由操作者按需 `mkdir` 或后续工具创建。

## 布局 A — 扁平 det / rec / cls（默认 candidate）

```text
paddleocr_current_api_v1/
  det/     # det_model_ref = "det"
  rec/     # rec_model_ref = "rec"
  cls/     # cls_model_ref = "cls"
```

与 **`run_paddleocr_manifest_v1_snapshot_v0.py`** 的解析规则对齐：`model_root` + 各 ref 子目录。

## 布局 B — 官方命名式目录（仅作 route note）

若官方包使用类似：

- `PP-OCRv5_server_det/`  
- `PP-OCRv5_server_rec/`  
- `PP-OCRv5_mobile_cls/`  

则在运行 prepare 时传入：

`--det-ref PP-OCRv5_server_det --rec-ref PP-OCRv5_server_rec --cls-ref PP-OCRv5_mobile_cls`

（名称以你确认的发行物为准；**本仓库不强行固定**。）

## manifest 字段关系

| 字段 | 含义 |
|------|------|
| `model_root` | 离线缓存根（绝对路径，candidate 中写死推荐值） |
| `det_model_ref` / `rec_model_ref` / `cls_model_ref` | **相对** `model_root` 的子目录名 |
| `route_options` | candidate 内记录 flat 与命名式 **备注**，便于评审 |

## 与 Snapshot 的衔接

1. 按 **manual_copy_instructions** 放入真实模型文件。  
2. 将 **candidate** 复制到 repo 内受控路径（若需要版本管理）或直接用绝对路径指向该 JSON。  
3. 运行 **`run_paddleocr_manifest_v1_snapshot_v0.py --manifest <candidate>`**（及可选 `--cache-root`）直至 **`pinning_complete=true`**。
