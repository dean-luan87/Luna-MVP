# 模型资产（外部存放）

**本仓库不存放模型权重。** 所有 `.pt` / `.onnx` / `.safetensors` / Paddle 推理文件等，统一放在外部 **Luna-Models**：

```
~/Desktop/Luna-Models/          # 默认，与 Luna-Core 同级
  vision/                     # 视觉模型
  speech/                     # 语音模型（TTS / ASR）
  ocr/                        # OCR 模型
  language/                   # 语言 / LLM
  spatial/                    # SLAM / Scene Graph
```

- 路径解析：`capabilities/model_paths_v1.py`
- 就绪检查：`python3 tools/check_models_root_v1.py`
- 环境变量：`export LUNA_MODELS_ROOT=/path/to/Luna-Models`

`configs/models/` 仅保留 **manifest / 授权 / 评估规划** JSON，不含权重文件。
