// Luna Auto Test Panel v1.1 - JavaScript

// =============================
// 批量场景测试逻辑（BatchTester）
// =============================
(function () {
  "use strict";

  // 避免重复注入
  if (window.BatchTester) return;

  const API_RECOGNIZE = "/api/recognize";
  const API_HAZARD = "/api/detect/hazard";
  const API_DESCRIBE = "/api/navigation/describe_scene";
  const API_REPORT = "/api/auto/batch/report";

  // 简单的"关键字 → 匹配词"映射，用来做一个初版的自动判断（可以人工复核）
  const MATCH_RULES = {
    stairs_up: ["楼梯", "台阶", "上楼", "下楼"],
    community_walk: ["小区", "居民楼", "绿化带", "步行道"],
    bus_station: ["公交站", "站牌", "候车亭", "上车", "下车"],
    cross_road: ["斑马线", "路口", "红绿灯", "过马路"],
    subway_station: ["地铁", "地铁站", "地铁口", "metro", "subway"],
    mall_entrance: ["商场", "入口", "大厅", "shopping mall"],
    hospital_hall: ["医院", "挂号", "候诊", "就诊", "导诊台"],
  };

  function autoJudge(sceneTag, description, hazardSummary) {
    if (!description && !hazardSummary) {
      return { match: false, reason: "没有返回描述" };
    }
    const descLower = (description || "").toLowerCase();
    const hazLower = (hazardSummary || "").toLowerCase();

    const rules = MATCH_RULES[sceneTag] || [];
    for (const w of rules) {
      if (descLower.includes(w.toLowerCase()) || hazLower.includes(w.toLowerCase())) {
        return { match: true, reason: `命中关键词：${w}` };
      }
    }
    // 没有匹配到就标为"不匹配待人工复核"
    return { match: false, reason: "未命中预设关键词（需要人工检查）" };
  }

  class BatchTester {
    constructor() {
      this.files = [];
      this.sceneTag = "unknown";
      this.results = [];
      this.index = 0;
      this.running = false;

      this.$files = document.getElementById("batchFilesInput");
      this.$tag = document.getElementById("batchSceneTag");
      this.$tagCustom = document.getElementById("batchSceneTagCustom");
      this.$btnStart = document.getElementById("btnBatchStart");
      this.$btnStop = document.getElementById("btnBatchStop");
      this.$btnExport = document.getElementById("btnBatchExport");
      this.$btnReport = document.getElementById("btnBatchReport");
      this.$status = document.getElementById("batchStatusText");
      this.$tbody = document.getElementById("batchResultTbody");
      this.$metrics = document.getElementById("batchMetrics");

      this.bindEvents();
    }

    bindEvents() {
      if (this.$btnStart) {
        this.$btnStart.addEventListener("click", () => this.start());
      }
      if (this.$btnStop) {
        this.$btnStop.addEventListener("click", () => this.stop());
      }
      if (this.$btnExport) {
        this.$btnExport.addEventListener("click", () => this.exportCSV());
      }
      if (this.$btnReport) {
        this.$btnReport.addEventListener("click", () => this.reportToServer());
      }
    }

    start() {
      if (!this.$files || this.$files.files.length === 0) {
        alert("请先选择一批图片（可以多选）");
        return;
      }
      // 处理场景标签
      const preTag = this.$tag ? this.$tag.value : "unknown";
      const custom = (this.$tagCustom && this.$tagCustom.value.trim()) || "";
      this.sceneTag = custom || preTag || "unknown";

      this.files = Array.from(this.$files.files);
      this.results = [];
      this.index = 0;
      this.running = true;
      if (this.$tbody) {
        this.$tbody.innerHTML = "";
      }
      this.updateStatus(`运行中：0 / ${this.files.length}`);

      this.runNext();
    }

    stop() {
      this.running = false;
      this.updateStatus("已停止");
    }

    updateStatus(text) {
      if (this.$status) {
        this.$status.textContent = "当前状态：" + text;
      }
    }

    runNext() {
      if (!this.running) return;
      if (this.index >= this.files.length) {
        this.running = false;
        this.updateStatus("已完成全部图片测试");
        this.updateMetrics();
        return;
      }

      const file = this.files[this.index];
      const currentIndex = this.index + 1;
      this.updateStatus(`运行中：${currentIndex} / ${this.files.length}`);

      this.processSingleFile(file)
        .then((result) => {
          this.results.push(result);
          this.appendResultRow(result, this.results.length);
          this.updateMetrics();
        })
        .catch((err) => {
          console.error("批量测试单张失败:", err);
          const result = {
            fileName: file.name,
            sceneTag: this.sceneTag,
            description: "",
            hazardSummary: "",
            hazardCount: 0,
            match: false,
            reason: "接口调用错误",
          };
          this.results.push(result);
          this.appendResultRow(result, this.results.length);
          this.updateMetrics();
        })
        .finally(() => {
          this.index += 1;
          setTimeout(() => this.runNext(), 300); // 避免连环打爆后端
        });
    }

    async processSingleFile(file) {
      // 1) 调 /api/recognize
      const formData = new FormData();
      formData.append("image", file);

      let recognizeData = null;
      try {
        const resp = await fetch(API_RECOGNIZE, { method: "POST", body: formData });
        recognizeData = await resp.json();
      } catch (e) {
        console.warn("调用 /api/recognize 失败", e);
      }

      // 2) 调 /api/detect/hazard
      let hazardData = null;
      try {
        const fd2 = new FormData();
        fd2.append("image", file);
        const resp2 = await fetch(API_HAZARD, { method: "POST", body: fd2 });
        hazardData = await resp2.json();
      } catch (e) {
        console.warn("调用 /api/detect/hazard 失败", e);
      }

      // 3) 提取 base64 传给 /api/navigation/describe_scene
      const fileBase64 = await this.fileToBase64(file);
      let descData = null;
      try {
        const resp3 = await fetch(API_DESCRIBE, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ image_base64: fileBase64, scene_tag: this.sceneTag }),
        });
        descData = await resp3.json();
      } catch (e) {
        console.warn("调用 /api/navigation/describe_scene 失败", e);
      }

      const description =
        (descData && descData.data && descData.data.description) ||
        (descData && descData.description) ||
        "";
      const hazards = (hazardData && hazardData.data && hazardData.data.hazards) ||
        hazardData?.hazards ||
        [];
      const hazardCount = Array.isArray(hazards) ? hazards.length : 0;

      let hazardSummary = "";
      if (Array.isArray(hazards) && hazards.length > 0) {
        hazardSummary = hazards
          .slice(0, 3)
          .map((h) => (h.type || h.hazard_type || "未知") + (h.severity ? `(${h.severity})` : ""))
          .join("，");
      }

      const judge = autoJudge(this.sceneTag, description, hazardSummary);

      return {
        fileName: file.name,
        sceneTag: this.sceneTag,
        description,
        hazardSummary,
        hazardCount,
        match: judge.match,
        reason: judge.reason,
      };
    }

    fileToBase64(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = function (e) {
          const result = e.target.result || "";
          const base64 = result.toString().split(",").pop();
          resolve(base64);
        };
        reader.onerror = reject;
        reader.readAsDataURL(file);
      });
    }

    appendResultRow(result, idx) {
      if (!this.$tbody) return;
      const tr = document.createElement("tr");

      const tdIndex = document.createElement("td");
      tdIndex.textContent = idx;
      tdIndex.style.padding = "8px";
      tdIndex.style.border = "1px solid #ddd";

      const tdFile = document.createElement("td");
      tdFile.textContent = result.fileName;
      tdFile.style.padding = "8px";
      tdFile.style.border = "1px solid #ddd";

      const tdTag = document.createElement("td");
      tdTag.textContent = result.sceneTag;
      tdTag.style.padding = "8px";
      tdTag.style.border = "1px solid #ddd";

      const tdDesc = document.createElement("td");
      tdDesc.textContent = result.description || "(无返回)";
      tdDesc.style.padding = "8px";
      tdDesc.style.border = "1px solid #ddd";
      tdDesc.style.maxWidth = "200px";
      tdDesc.style.overflow = "hidden";
      tdDesc.style.textOverflow = "ellipsis";

      const tdHaz = document.createElement("td");
      tdHaz.textContent =
        result.hazardCount > 0
          ? `发现 ${result.hazardCount} 个危险：${result.hazardSummary}`
          : "未发现明显危险";
      tdHaz.style.padding = "8px";
      tdHaz.style.border = "1px solid #ddd";

      const tdMatch = document.createElement("td");
      tdMatch.textContent = result.match
        ? "✅ 初步匹配：" + result.reason
        : "❌ 待人工检查：" + result.reason;
      tdMatch.style.whiteSpace = "pre-wrap";
      tdMatch.style.padding = "8px";
      tdMatch.style.border = "1px solid #ddd";

      tr.appendChild(tdIndex);
      tr.appendChild(tdFile);
      tr.appendChild(tdTag);
      tr.appendChild(tdDesc);
      tr.appendChild(tdHaz);
      tr.appendChild(tdMatch);

      this.$tbody.appendChild(tr);
    }

    updateMetrics() {
      if (!this.$metrics) return;
      const total = this.results.length;
      if (total === 0) {
        this.$metrics.textContent = "暂无数据";
        return;
      }
      let pass = 0;
      let fail = 0;
      for (const r of this.results) {
        if (r.match) pass += 1;
        else fail += 1;
      }
      const rate = total > 0 ? ((pass / total) * 100).toFixed(1) : "0.0";

      const text =
        `总图片数：${total}\n` +
        `自动判断通过：${pass}\n` +
        `自动判断未通过（待人工复核）：${fail}\n` +
        `通过率（仅供参考）：${rate}%\n\n` +
        `当前场景标签：${this.sceneTag}\n` +
        `说明：这里的"通过/未通过"只是根据关键词做的粗判，\n` +
        `真正的结果需要你人工抽查。`;

      this.$metrics.textContent = text;
    }

    exportCSV() {
      if (!this.results || this.results.length === 0) {
        alert("没有结果可以导出");
        return;
      }
      const rows = [];
      rows.push(
        ["fileName", "sceneTag", "description", "hazardSummary", "hazardCount", "match", "reason"].join(
          ","
        )
      );
      for (const r of this.results) {
        const line = [
          r.fileName.replace(/,/g, ";"),
          r.sceneTag.replace(/,/g, ";"),
          (r.description || "").replace(/[\r\n,]/g, " "),
          (r.hazardSummary || "").replace(/[\r\n,]/g, " "),
          r.hazardCount,
          r.match ? "1" : "0",
          (r.reason || "").replace(/[\r\n,]/g, " "),
        ].join(",");
        rows.push(line);
      }
      const csv = rows.join("\n");
      const blob = new Blob([csv], { type: "text/csv" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      const ts = new Date().toISOString().replace(/[:.]/g, "-");
      a.download = `luna_batch_test_${this.sceneTag}_${ts}.csv`;
      a.click();
      URL.revokeObjectURL(url);
    }

    async reportToServer() {
      if (!this.results || this.results.length === 0) {
        alert("没有结果可以上报");
        return;
      }
      try {
        const payload = {
          scene_tag: this.sceneTag,
          total: this.results.length,
          pass: this.results.filter((r) => r.match).length,
          fail: this.results.filter((r) => !r.match).length,
          items: this.results.slice(0, 200), // 避免一次性太大
        };
        const resp = await fetch(API_REPORT, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        const data = await resp.json();
        if (data && data.success) {
          alert("已上报本次批量测试结果（后端会记一条日志）");
        } else {
          alert("上报失败：" + (data && data.error || "未知错误"));
        }
      } catch (e) {
        console.error("上报失败", e);
        alert("上报失败：" + e.message);
      }
    }
  }

  // 页面加载后自动初始化
  window.addEventListener("DOMContentLoaded", () => {
    try {
      window.BatchTester = new BatchTester();
      console.log("[BatchTester] 批量场景测试已初始化");
    } catch (e) {
      console.error("[BatchTester] 初始化失败", e);
    }
  });
})();

const KEYWORDS = [
    "人行道",
    "斑马线",
    "台阶",
    "地铁入口",
    "公交站牌",
    "电梯",
    "扶梯",
    "路口",
    "障碍物"
];

/**
 * 加载关键字列表
 */
function loadKeywords() {
    const box = document.getElementById("keyword-list");
    box.innerHTML = ""; // 清空
    
    KEYWORDS.forEach(kw => {
        const btn = document.createElement("button");
        btn.innerText = "🔍 " + kw;
        btn.onclick = () => runSingleTest(kw);
        box.appendChild(btn);
    });
}

/**
 * 运行单个测试
 */
async function runSingleTest(kw) {
    const resultBox = document.getElementById("result-box");
    resultBox.innerHTML = `<div class="result-item"><h3>${kw} — 测试中...</h3><p>正在抓取图片并调用场景描述接口...</p></div>`;

    try {
        const resp = await fetch(`/api/auto/run_full_test/${encodeURIComponent(kw)}`);
        const data = await resp.json();

        if (!data.success) {
            renderError(kw, data.error || "未知错误");
            return;
        }

        renderResult(data);
    } catch (error) {
        renderError(kw, `请求失败: ${error.message}`);
    }
}

/**
 * 渲染测试结果
 */
function renderResult(data) {
    const box = document.getElementById("result-box");
    
    // 如果已有结果，追加；否则替换
    const div = document.createElement("div");
    div.className = "result-item " + (data.match ? "pass" : "fail");

    const statusText = data.match ? "✔ 通过" : "✘ 未通过";
    const hitText = data.hit || "无";

    div.innerHTML = `
        <h3>${data.keyword} — ${statusText}</h3>
        <p><b>描述：</b> ${data.description || "(空)"}</p>
        <p><b>命中关键词：</b> ${hitText}</p>
        ${data.image_base64 ? `<img src="data:image/jpeg;base64,${data.image_base64}" alt="测试图片" />` : ""}
    `;

    box.appendChild(div);
    
    // 滚动到底部
    box.scrollTop = box.scrollHeight;
}

/**
 * 渲染错误信息
 */
function renderError(keyword, errorMsg) {
    const box = document.getElementById("result-box");
    const div = document.createElement("div");
    div.className = "result-item fail";
    div.innerHTML = `
        <h3>${keyword} — ✘ 测试失败</h3>
        <p><b>错误：</b> ${errorMsg}</p>
    `;
    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
}

/**
 * 运行全部测试
 */
async function runAllTests() {
    const resultBox = document.getElementById("result-box");
    resultBox.innerHTML = `<div class="placeholder">正在运行全部测试，请稍候...</div>`;

    const runAllBtn = document.getElementById("run-all");
    runAllBtn.disabled = true;
    runAllBtn.textContent = "⏳ 测试中...";

    try {
        for (let i = 0; i < KEYWORDS.length; i++) {
            const kw = KEYWORDS[i];
            const resp = await fetch(`/api/auto/run_full_test/${encodeURIComponent(kw)}`);
            const data = await resp.json();

            if (data.success) {
                renderResult(data);
            } else {
                renderError(kw, data.error || "未知错误");
            }

            // 添加小延迟，避免请求过快
            if (i < KEYWORDS.length - 1) {
                await new Promise(resolve => setTimeout(resolve, 500));
            }
        }
    } catch (error) {
        renderError("批量测试", `批量测试失败: ${error.message}`);
    } finally {
        runAllBtn.disabled = false;
        runAllBtn.textContent = "▶ 运行全部测试";
    }
}

// ====== v1.2: 视频测试 ======
async function runVideoTest() {
    const input = document.getElementById("videoInput");
    const file = input.files[0];
    if (!file) {
        alert("请先选择视频文件");
        return;
    }

    const formData = new FormData();
    formData.append("video", file);

    const box = document.getElementById("videoResult");
    box.innerHTML = `<div class="result-item"><h3>视频分析中...</h3></div>`;

    try {
        const resp = await fetch("/api/auto/video_describe", {
            method: "POST",
            body: formData,
        });

        const data = await resp.json();
        if (!data.success) {
            box.innerHTML = `<div class="result-item fail"><h3>视频分析失败：${data.error || "未知错误"}</h3></div>`;
            return;
        }

        box.innerHTML = "";
        const frames = data.frames || [];
        frames.forEach((f) => {
            const div = document.createElement("div");
            div.className = "result-item";
            div.innerHTML = `
                <h3>帧 #${f.frame_index}</h3>
                <p><b>描述：</b> ${f.description || "(空)"}</p>
                <img src="data:image/jpeg;base64,${f.image_base64}" alt="帧 ${f.frame_index}" />
            `;
            box.appendChild(div);
        });
    } catch (error) {
        box.innerHTML = `<div class="result-item fail"><h3>视频分析失败：${error.message}</h3></div>`;
    }
}

// ====== v1.3: Playlist 多场景测试 ======
async function loadPlaylists() {
    try {
        const resp = await fetch("/api/auto/playlists");
        const data = await resp.json();
        if (!data.success) return;

        const sel = document.getElementById("playlistSelect");
        (data.data || []).forEach(p => {
            const opt = document.createElement("option");
            opt.value = p.name;
            opt.textContent = `${p.name} (${p.keywords.length} 个场景)`;
            sel.appendChild(opt);
        });
    } catch (error) {
        console.error("加载 Playlist 失败:", error);
    }
}

async function runPlaylist() {
    const sel = document.getElementById("playlistSelect");
    const name = sel.value;
    if (!name) {
        alert("请选择一个场景组");
        return;
    }

    const resultBox = document.getElementById("result-box");
    resultBox.innerHTML = `<div class="result-item"><h3>${name} 场景组执行中...</h3></div>`;

    try {
        const resp = await fetch(`/api/auto/run_playlist/${encodeURIComponent(name)}`, {
            method: "POST"
        });
        const data = await resp.json();
        
        if (!data.success) {
            resultBox.innerHTML = `<div class="result-item fail"><h3>执行失败：${data.error || "未知错误"}</h3></div>`;
            return;
        }

        resultBox.innerHTML = "";
        (data.results || []).forEach(r => {
            const div = document.createElement("div");
            div.className = "result-item " + (r.match ? "pass" : "fail");
            div.innerHTML = `
                <h3>${r.keyword} — ${r.match ? "✔ 通过" : "✘ 未通过"}</h3>
                <p><b>描述：</b> ${r.description || "(空)"} </p>
                <p><b>命中关键词：</b> ${r.hit || "无"}</p>
                ${r.image_base64 ? `<img src="data:image/jpeg;base64,${r.image_base64}" alt="${r.keyword}" />` : ""}
            `;
            resultBox.appendChild(div);
        });
    } catch (error) {
        resultBox.innerHTML = `<div class="result-item fail"><h3>执行失败：${error.message}</h3></div>`;
    }
}

// ====== v2.0: 测试统计 ======
async function loadMetrics() {
    const box = document.getElementById("metricsBox");
    box.innerHTML = `<div class="result-item"><h3>统计加载中...</h3></div>`;

    try {
        const resp = await fetch("/api/auto/metrics_summary");
        const data = await resp.json();
        
        if (!data.success) {
            box.innerHTML = `<div class="result-item fail"><h3>统计加载失败：${data.error || "未知错误"}</h3></div>`;
            return;
        }

        const s = data.data;
        const total = s.total || { total: 0, pass: 0 };

        let html = `
            <div class="result-item">
              <h3>整体情况</h3>
              <p>总测试次数：${total.total}</p>
              <p>通过次数：${total.pass}</p>
              <p>整体通过率：${total.total ? ((total.pass / total.total * 100).toFixed(1) + "%") : "-"}</p>
            </div>
        `;

        html += `<div class="result-item"><h3>按关键字统计</h3>`;
        html += `<ul style="list-style:none;padding-left:0;">`;
        (s.keywords || []).forEach(k => {
            html += `<li style="margin:8px 0;">${k.name}: ${k.pass}/${k.total} （${(k.pass_rate * 100).toFixed(1)}%）</li>`;
        });
        html += `</ul></div>`;

        html += `<div class="result-item"><h3>按场景组统计</h3>`;
        html += `<ul style="list-style:none;padding-left:0;">`;
        (s.playlists || []).forEach(p => {
            html += `<li style="margin:8px 0;">${p.name}: ${p.pass}/${p.total} （${(p.pass_rate * 100).toFixed(1)}%）</li>`;
        });
        html += `</ul></div>`;

        box.innerHTML = html;
    } catch (error) {
        box.innerHTML = `<div class="result-item fail"><h3>统计加载失败：${error.message}</h3></div>`;
    }
}

// ====== v1.4: 自动识别与分类 ======
(function () {
    const btn = document.getElementById("btnRunAutoSort");
    if (!btn) return;

    btn.addEventListener("click", async () => {
        const dirInput = document.getElementById("autoSortInputDir");
        const dir = dirInput ? (dirInput.value || "test_images") : "test_images";
        const resultBox = document.getElementById("autoSortResult");
        if (resultBox) {
            resultBox.textContent = "⏳ 正在扫描并分类，请稍候...";
        }

        // 禁用按钮
        btn.disabled = true;
        btn.textContent = "⏳ 分类中...";

        try {
            const resp = await fetch("/api/auto/auto_sort", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ input_dir: dir })
            });
            const data = await resp.json();

            if (!data.success) {
                if (resultBox) {
                    resultBox.textContent = "❌ 自动分类失败：" + (data.error || "未知错误");
                }
                return;
            }

            const stats = data.data || {};
            const per = stats.per_category || {};
            let lines = [];

            lines.push(`📊 总图片数：${stats.total || 0}`);
            lines.push(`❓ 未能识别类别：${stats.unknown || 0}`);
            lines.push("");

            lines.push("按类别统计：");
            Object.keys(per).forEach(k => {
                if (per[k] > 0) {
                    lines.push(`- ${k}: ${per[k]} 张`);
                }
            });

            if (stats.errors && stats.errors.length) {
                lines.push("");
                lines.push(`⚠️ 处理失败：${stats.errors.length} 张（详见后台日志）`);
            }

            lines.push("");
            lines.push("✅ 输出目录：auto_sorted/（按类别自动创建子目录）");

            if (resultBox) {
                resultBox.textContent = lines.join("\n");
            }
        } catch (e) {
            console.error(e);
            if (resultBox) {
                resultBox.textContent = "❌ 请求失败：" + e.message;
            }
        } finally {
            btn.disabled = false;
            btn.textContent = "运行自动分类";
        }
    });
})();

// 初始化
document.getElementById("run-all").onclick = runAllTests;
document.getElementById("btnVideoTest").onclick = runVideoTest;
document.getElementById("btnRunPlaylist").onclick = runPlaylist;
document.getElementById("btnLoadMetrics").onclick = loadMetrics;

window.onload = function () {
    loadKeywords();
    loadPlaylists();
};

