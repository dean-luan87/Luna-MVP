# Model Test Lens Static Site Plan V1

## 1. 页面定位

**Model Test Lens / 模型测试镜头页** — 本地静态模型测试可视化，非白盒产品页。

- 导入测试内容 → 选择单个模型 → 读取或展示测试结果 → 可视化工作过程与 candidate 输出 → 对照 TestBoard
- 不承载最终产品参数、不承载 runtime、不承载用户侧输出

## 2. 布局（四区）

| 区域 | 模块 |
|------|------|
| 左 | Model selector（OCR / SLAM / Segmentation / …） |
| 中 | Input preview（图/视频帧/音频/文本/轨迹） |
| 右 | Result visualization（按 panel 类型） |
| 底 | Trace / Metrics / Failure mode / TestBoard refs / Boundary |

## 3. 页面模块（9）

1. Model selector
2. Test case importer（本地 JSON manifest / _tmp_eval_out / TestBoard refs）
3. Input preview panel
4. Process trace panel
5. Result visualization panel
6. Metrics panel
7. Failure mode panel
8. TestBoard refs panel
9. Boundary panel（candidate_only、readiness 全 false）

## 4. 模型面板（10）

见 `model_panels/` 与 `model_test_lens_model_panel_registry_v1.json`。

MobileSAM 当前接入 **vision_segmentation** panel。

## 5. 统一 Result Envelope

见 `schemas/model_test_result_envelope_schema_v1.json`。

## 6. 与治理的关系

- 引用 `governance_standards_manifest_v1.json`、`legacy_reusable_governance_rules_inventory_v1.json`
- 引用 Model Asset Onboarding Standard
- 不绕过 approval gate；不把 candidate 升级为 fact
- readiness 只读 registry/review artifact，页面不生成 readiness

## 7. 本阶段边界

- `planning_only = true`
- 不实现完整 UI；仅目录、schema、规划产物、skeleton 占位

## 8. Skeleton 阶段预告

生成 `index.html` / `app.js` / `styles.css`、示例 envelope、MobileSAM 示例面板、其他 panel 占位。
