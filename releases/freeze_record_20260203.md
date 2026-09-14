# Luna-2 工程封版记录

**封版日期**：2026-02-03  
**封版级别**：工程级冻结  
**状态**：✅ 已封版

---

## 一、封版范围

本封版针对 **Luna-2 工程根目录** 当前状态（main.py 驱动之 MVP、视觉流水线、Freeze 测试、run/视频模式等），不包含子工程 luna_badge_v1_2 / Luna_Badge 等独立版本的版本号与发布策略。

---

## 二、封版前验证

| 项目 | 结果 | 说明 |
|------|------|------|
| Freeze 测试套件 | ✅ 56 passed | `python3 -m pytest tests/freeze -v` |
| 视频输入源确认 | ✅ 已验证 | `--video` 使用视频帧，首帧/每 30 帧有日志确认 |
| 运行流程 | ✅ 正常 | 视觉流水线、语音、日志、退出与资源释放均正常 |

---

## 三、本封版包含的变更要点（近期）

- **run.py**：`--video` 支持；以项目根为 cwd 启动 main.py；相对路径视频自动解析为绝对路径。
- **main.py**：`--video` 传入 `LunaBadgeMVP(video_path=...)`；为 `utils.camera_handler` 配置 logger，便于确认视频帧来源。
- **utils/camera_handler.py**：视频模式首帧与每 30 帧打日志；首帧增加 `[视频确认]` 打印，便于终端确认。
- **vision_pipeline / PipelineController**：接受 `video_path`，创建 `CameraHandler(video_path=...)` 从视频读帧。

---

## 四、封版后约定

- 本封版**不**对子工程（如 luna_badge_v1_2）的版本号或发布流程做约束。
- 封版后如需修改上述已冻结行为，应在变更说明中引用本记录并说明原因。
- 新增功能或重构不影响本封版所记录之“视频模式 + Freeze 测试通过”的基线即可。

---

## 五、封版声明

**Luna-2 工程于 2026-02-03 完成本次冻结封版。**

- 冻结内容：当前 main/run/视觉流水线/视频输入/Freeze 测试行为及上述文档记录。
- 验证依据：`tests/freeze` 全绿、视频帧来源日志确认、人工运行验证。

**封版记录人**：系统  
**封版记录文件**：`releases/freeze_record_20260203.md`、`releases/freeze_confirmation_20260203.md`

---

## 六、Git 标签（建议）

封版完成后，建议先提交本次封版相关变更（含 `releases/` 下两文档），再打标签以固定当前工程状态：

```bash
# 1. 提交封版文档与当前修改（按需 add/commit）
git add releases/freeze_record_20260203.md releases/freeze_confirmation_20260203.md
git commit -m "chore: Luna-2 工程封版 2026-02-03（Freeze 测试通过、视频模式确认）"

# 2. 打封版标签
git tag -a freeze-2026-02-03 -m "Luna-2 工程封版 2026-02-03"
```

若仅对当前 HEAD 打标签（不包含未提交的封版文档），可直接执行：

```bash
git tag -a freeze-2026-02-03 -m "Luna-2 工程封版 2026-02-03"
```
