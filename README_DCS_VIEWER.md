# B2 Trace Viewer v0.4.3 - DCS 审判视图

## 快速开始

### 1. 准备 trace 文件

把 `trace.jsonl` 放在仓库根目录。

### 2. 运行 DCS 评估

```bash
python3 tools/dcs_eval.py trace.jsonl
```

这会生成：
- `artifacts/dcs_report.json` - DCS 报告
- `artifacts/trace_enriched.jsonl` - 带 DCS 字段的 trace

### 3. 打开 Viewer

用浏览器打开：
```
viewer/trace_viewer_v043.html?src=../artifacts/trace_enriched.jsonl
```

或者直接打开 `viewer/trace_viewer_v043.html`（会使用默认路径）。

### 4. 查看 Console

点击任意一条记录，Console 会输出：
```javascript
jump_request { t_video_s: ..., frame_id: ..., human_time: ... }
```

## 功能

- ✅ 红黄绿仪表盘（RED/YELLOW/GREEN 数量）
- ✅ Grade 筛选（ALL/RED/YELLOW/GREEN）
- ✅ 全文搜索（搜索任意 JSON 字段）
- ✅ RED 记录自动置顶
- ✅ 点击记录输出 jump_request（用于视频联动）
- ✅ 详情面板显示完整 JSON

## 自检

运行自检脚本生成示例 trace：

```bash
python3 tools/_selftest_make_sample_trace.py
python3 tools/dcs_eval.py trace.jsonl
```

然后打开 Viewer 查看结果。

---

**版本：** v0.4.3  
**状态：** ✅ 已完成
