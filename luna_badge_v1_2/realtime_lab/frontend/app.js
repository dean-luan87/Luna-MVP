// 200ms 一帧
const FRAME_INTERVAL_MS = 200;

// 获取模型信息
async function fetchModelInfo() {
  try {
    const protocol = window.location.protocol;
    const host = window.location.hostname;
    const port = "5001";
    const url = `${protocol}//${host}:${port}/api/model/info`;
    
    const resp = await fetch(url);
    const data = await resp.json();
    
    const modelNameEl = document.getElementById("modelName");
    if (data.current_nav_model) {
      modelNameEl.textContent = data.current_nav_model;
      modelNameEl.style.color = "#4ade80";
    } else if (data.error) {
      modelNameEl.textContent = "error";
      modelNameEl.style.color = "#ef4444";
    } else {
      modelNameEl.textContent = "unknown";
    }
    
    console.log("[MODEL] 当前模型:", data.current_nav_model);
  } catch (e) {
    console.error("[MODEL] 获取模型信息失败:", e);
    document.getElementById("modelName").textContent = "error";
  }
}

// 页面加载时获取模型信息
window.addEventListener("load", () => {
  fetchModelInfo();
  // 每 30 秒刷新一次模型信息
  setInterval(fetchModelInfo, 30000);
});

setInterval(() => {
  if (!wsReady()) return;

  const dataUrl = captureFrame();
  if (!dataUrl) return;

  frameCount += 1;

  wsSend({
    type: "frame",
    data: dataUrl,
    ts: performance.now(),
  });
}, FRAME_INTERVAL_MS);

