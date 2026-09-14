# Luna Evaluation — Controlled Frame Sample Closure v1

**Phase**：`Phase-Controlled-Frame-Sample-Closure-v1-001`  
**性质**：closure-only（不读内容、不打开文件、不进入 runtime）  
**输出目录**：`_eval_out/controlled_frame_sample_closure_v1_smoke_v0/`

## 运行命令（smoke）

runner：

```bash
python3 tools/evaluation/vision/run_controlled_frame_sample_closure_v1.py
```

verifier：

```bash
python3 tools/evaluation/vision/verify_controlled_frame_sample_closure_v1.py
```

## 通过标准

通过 verifier（GO）时：

- `final_decision=CONTROLLED_FRAME_SAMPLE_CLOSED_FOR_CURRENT_MAINLINE`
- `recommended_next_phase=Phase-Post-Controlled-Frame-Sample-Roadmap-Decision-v1-001`

本阶段强制保证：

- closure 仅关账，不新增能力
- 仍为 manifest-level governance；不等于真实图像读取，不等于视觉 runtime，不等于 production readiness

