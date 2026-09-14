# LUNA — MidPlatform OCR Bridge Upstream Input GO/NO-GO Pack v0

## Phase

- **Phase-ModelOCR-MidPlatform-Bridge-002-Fix**

## GO conditions（离线上游输入验证通过）

对给定的 `yolo_ocr_bridge_root` 或 `ocr_benchmark_root`：
1) `tools/evaluate_midplatform_ocr_bridge_v0.py` 能成功生成全部 Bridge-002 输出文件集
2) `tools/verify_midplatform_ocr_bridge_v0.py` verdict=GO
3) `trace/replay/whitebox` 三份 JSONL 均非空
4) 禁止项保持：
   - 不生成 `semantic_summary`
   - 不生成 `navigation_action`
   - 不执行任何导航动作
   - 不写入真实世界模型

## NO-GO conditions

- 任一输出文件缺失
- 禁止项出现（semantic_summary / navigation_action 非 null 或 runtime 写入迹象）
- trace/replay/whitebox 任意缺失或为空

