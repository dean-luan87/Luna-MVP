# 📦 批量图片下载工具集成方案

## 🎯 集成到 v1.3.0 测试体系

### 1. 后端集成

#### 1.1 创建批量下载路由

在 `routes/auto_test_routes.py` 中添加：

```python
from backend.auto_test.batch_image_downloader import (
    BatchImageDownloader,
    download_images_from_keywords,
    download_images_from_file
)

@auto_test_api.route("/batch_download/keywords", methods=["POST"])
def batch_download_keywords():
    """
    批量下载：关键词搜索模式
    body: {
        "keywords": ["人行道", "斑马线"],
        "max_per_keyword": 20,
        "output_dir": "downloads"
    }
    """
    data = request.get_json() or {}
    keywords = data.get("keywords", [])
    max_per_keyword = data.get("max_per_keyword", 20)
    output_dir = data.get("output_dir", "downloads")
    
    if not keywords:
        return jsonify({"success": False, "error": "keywords 不能为空"}), 400
    
    try:
        summary = download_images_from_keywords(
            keywords=keywords,
            output_dir=output_dir,
            max_per_keyword=max_per_keyword
        )
        return jsonify(summary)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@auto_test_api.route("/batch_download/file", methods=["POST"])
def batch_download_file():
    """
    批量下载：文件解析模式
    form-data: file (文件)
    """
    if "file" not in request.files:
        return jsonify({"success": False, "error": "未上传文件"}), 400
    
    file = request.files["file"]
    output_dir = request.form.get("output_dir", "downloads")
    
    # 保存临时文件
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        file.save(tmp.name)
        filepath = tmp.name
    
    try:
        summary = download_images_from_file(
            filepath=filepath,
            output_dir=output_dir
        )
        return jsonify(summary)
    finally:
        try:
            os.unlink(filepath)
        except:
            pass
```

#### 1.2 更新配置

在 `config/auto_test_config.py` 中添加：

```python
class AutoTestConfig:
    # ... 现有配置 ...
    
    # 批量下载配置
    BATCH_DOWNLOAD_OUTPUT_DIR = os.getenv("BATCH_DOWNLOAD_OUTPUT_DIR", "downloads")
    BATCH_DOWNLOAD_MAX_WORKERS = int(os.getenv("BATCH_DOWNLOAD_MAX_WORKERS", "5"))
    BATCH_DOWNLOAD_MAX_PER_KEYWORD = int(os.getenv("BATCH_DOWNLOAD_MAX_PER_KEYWORD", "20"))
    BATCH_DOWNLOAD_TIMEOUT = int(os.getenv("BATCH_DOWNLOAD_TIMEOUT", "10"))
    BATCH_DOWNLOAD_RETRY_TIMES = int(os.getenv("BATCH_DOWNLOAD_RETRY_TIMES", "3"))
```

### 2. 前端集成

#### 2.1 在 `/auto_test` 页面添加批量下载功能

在 `frontend/auto_test/index.html` 中添加：

```html
<hr />
<h2>📥 批量图片下载（v1.3.0）</h2>

<div class="card mt-2">
    <div class="card-body">
        <h5>模式1: 关键词搜索</h5>
        <div class="mb-2">
            <label>关键词（逗号分隔）：</label>
            <input type="text" id="downloadKeywords" class="form-control" 
                   placeholder="例如: 人行道, 斑马线, 台阶" />
        </div>
        <div class="mb-2">
            <label>每个关键词下载数量：</label>
            <input type="number" id="downloadCount" class="form-control" value="20" min="1" max="100" />
        </div>
        <button id="btnDownloadKeywords" class="btn btn-primary">开始下载</button>
    </div>
</div>

<div class="card mt-2">
    <div class="card-body">
        <h5>模式2: 文件解析</h5>
        <div class="mb-2">
            <label>上传文件（.txt / .json / .csv / .md）：</label>
            <input type="file" id="downloadFile" class="form-control" accept=".txt,.json,.csv,.md" />
        </div>
        <button id="btnDownloadFile" class="btn btn-primary">开始下载</button>
    </div>
</div>

<div id="downloadProgress" class="mt-3"></div>
<div id="downloadSummary" class="mt-3"></div>
```

#### 2.2 添加 JavaScript 逻辑

在 `frontend/auto_test/auto_test.js` 中添加：

```javascript
// 批量下载：关键词搜索
async function downloadFromKeywords() {
    const keywordsInput = document.getElementById("downloadKeywords");
    const countInput = document.getElementById("downloadCount");
    const keywords = keywordsInput.value.split(",").map(k => k.trim()).filter(k => k);
    
    if (keywords.length === 0) {
        alert("请输入关键词");
        return;
    }
    
    const progress = document.getElementById("downloadProgress");
    const summary = document.getElementById("downloadSummary");
    
    progress.innerHTML = `<div class="result-item"><h3>正在下载...</h3><p>关键词: ${keywords.join(", ")}</p></div>`;
    
    try {
        const resp = await fetch("/api/auto/batch_download/keywords", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                keywords: keywords,
                max_per_keyword: parseInt(countInput.value) || 20
            })
        });
        
        const data = await resp.json();
        
        if (data.success) {
            summary.innerHTML = `
                <div class="result-item pass">
                    <h3>下载完成</h3>
                    <p>成功: ${data.success_count} 张</p>
                    <p>失败: ${data.fail_count} 张</p>
                    <p>成功率: ${(data.success_rate * 100).toFixed(1)}%</p>
                    <p>输出目录: ${data.output_dir}</p>
                </div>
            `;
        } else {
            summary.innerHTML = `<div class="result-item fail"><h3>下载失败</h3><p>${data.error}</p></div>`;
        }
    } catch (error) {
        summary.innerHTML = `<div class="result-item fail"><h3>下载失败</h3><p>${error.message}</p></div>`;
    }
}

// 批量下载：文件解析
async function downloadFromFile() {
    const fileInput = document.getElementById("downloadFile");
    const file = fileInput.files[0];
    
    if (!file) {
        alert("请选择文件");
        return;
    }
    
    const formData = new FormData();
    formData.append("file", file);
    
    const progress = document.getElementById("downloadProgress");
    const summary = document.getElementById("downloadSummary");
    
    progress.innerHTML = `<div class="result-item"><h3>正在解析并下载...</h3><p>文件: ${file.name}</p></div>`;
    
    try {
        const resp = await fetch("/api/auto/batch_download/file", {
            method: "POST",
            body: formData
        });
        
        const data = await resp.json();
        
        if (data.success) {
            summary.innerHTML = `
                <div class="result-item pass">
                    <h3>下载完成</h3>
                    <p>成功: ${data.success_count} 张</p>
                    <p>失败: ${data.fail_count} 张</p>
                    <p>成功率: ${(data.success_rate * 100).toFixed(1)}%</p>
                </div>
            `;
        } else {
            summary.innerHTML = `<div class="result-item fail"><h3>下载失败</h3><p>${data.error}</p></div>`;
        }
    } catch (error) {
        summary.innerHTML = `<div class="result-item fail"><h3>下载失败</h3><p>${error.message}</p></div>`;
    }
}

// 绑定事件
document.getElementById("btnDownloadKeywords").onclick = downloadFromKeywords;
document.getElementById("btnDownloadFile").onclick = downloadFromFile;
```

### 3. 使用示例

#### 3.1 命令行使用

```bash
# 从关键词下载
python3 scripts/batch_download_images.py \
    --mode keywords \
    --input "人行道,斑马线,台阶" \
    --output downloads \
    --max-per-keyword 20 \
    --save-summary

# 从 URL 列表下载
python3 scripts/batch_download_images.py \
    --mode urls \
    --input "https://example.com/image1.jpg,https://example.com/image2.jpg" \
    --output downloads

# 从文件下载
python3 scripts/batch_download_images.py \
    --mode file \
    --input urls.txt \
    --output downloads
```

#### 3.2 API 调用

```bash
# 关键词搜索下载
curl -X POST http://localhost:9001/api/auto/batch_download/keywords \
    -H "Content-Type: application/json" \
    -d '{
        "keywords": ["人行道", "斑马线"],
        "max_per_keyword": 20
    }'

# 文件解析下载
curl -X POST http://localhost:9001/api/auto/batch_download/file \
    -F "file=@urls.txt"
```

### 4. 集成步骤

1. ✅ 创建 `backend/auto_test/batch_image_downloader.py`
2. ✅ 创建 `scripts/batch_download_images.py`
3. ⏳ 在 `routes/auto_test_routes.py` 中添加批量下载路由
4. ⏳ 在 `config/auto_test_config.py` 中添加配置
5. ⏳ 在 `frontend/auto_test` 中添加 UI
6. ⏳ 测试验证

### 5. 依赖安装

```bash
pip install duckduckgo-search requests
```

---

## 📝 总结

### ✅ 已完成
- 批量下载模块实现
- 命令行脚本实现
- 文档编写

### ⏳ 待完成
- 后端路由集成
- 前端 UI 集成
- 测试验证


