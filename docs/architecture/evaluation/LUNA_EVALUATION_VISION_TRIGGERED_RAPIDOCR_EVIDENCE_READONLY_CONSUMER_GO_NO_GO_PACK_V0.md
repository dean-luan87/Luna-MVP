# Luna — GO / NO_GO: Vision-triggered RapidOCR ReadOnly Consumer v0

## GO

- 只读消费 RapidOCR submission collection；`rapidocr_success_count > 0`；`provider=rapidocr_candidate`。
- `empty_text_count` 可为 10，**不得**因空 `text_joined` 判 NO_GO。
- 无融合、无事实写入；verifier = **GO**。

## NO_GO

- 把空文本当运行失败；重新调用 OCR；融合/事实/导航/AI；audit 缺失。
