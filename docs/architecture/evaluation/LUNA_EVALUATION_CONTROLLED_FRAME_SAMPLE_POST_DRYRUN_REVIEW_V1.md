# Luna Evaluation — Controlled Frame Sample Post-DryRun Review v1

**Phase**：`Phase-Controlled-Frame-Sample-Post-DryRun-Review-v1-001`  
**性质**：review-only（不读内容、不打开文件、不进入 runtime）  
**输出目录**：`_eval_out/controlled_frame_sample_post_dryrun_review_v1_smoke_v0/`

## 运行命令（smoke）

runner：

```bash
python3 tools/evaluation/vision/run_controlled_frame_sample_post_dryrun_review_v1.py
```

verifier：

```bash
python3 tools/evaluation/vision/verify_controlled_frame_sample_post_dryrun_review_v1.py
```

## 通过标准

通过 verifier（GO）时：

- `final_decision=CONTROLLED_FRAME_SAMPLE_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE`
- `recommended_next_phase=Phase-Controlled-Frame-Sample-Closure-v1-001`

本阶段必须保持：

- review-only；不读取真实图像/视频内容；不打开文件；不解码/不抽帧；不计算真实 hash
- 不触发 runtime/write/action/speech

