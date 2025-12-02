// web/app.js

const API_BASE = window.location.origin; // 比如 http://127.0.0.1:5001

const videoEl = document.getElementById("video");
const overlay = document.getElementById("overlay");
const statusEl = document.getElementById("status");
const latencyEl = document.getElementById("latency");
const avgLatencyEl = document.getElementById("avgLatency");
const fpsEl = document.getElementById("fps");
const frameCountEl = document.getElementById("frameCount");
const boxCountEl = document.getElementById("boxCount");
const logEl = document.getElementById("log");
const startBtn = document.getElementById("startBtn");
const stopBtn = document.getElementById("stopBtn");
const intervalInput = document.getElementById("intervalInput");

let sendingTimer = null;
let heartbeatTimer = null;
let lastFrameTime = null;
let frameCount = 0;
let latencySum = 0;

function appendLog(msg) {
  const ts = new Date().toISOString().split("T")[1].replace("Z", "");
  logEl.textContent += `[${ts}] ${msg}\n`;
  logEl.scrollTop = logEl.scrollHeight;
}

function setStatus(text, level) {
  statusEl.textContent = text;
  statusEl.classList.remove("status-ok", "status-warn", "status-error");
  if (level === "ok") statusEl.classList.add("status-ok");
  else if (level === "warn") statusEl.classList.add("status-warn");
  else if (level === "error") statusEl.classList.add("status-error");
}

async function initCamera() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: "environment" },
      audio: false,
    });
    videoEl.srcObject = stream;
    await videoEl.play();

    // 设置 overlay 尺寸
    overlay.width = videoEl.videoWidth || 640;
    overlay.height = videoEl.videoHeight || 480;

    setStatus("摄像头已就绪", "ok");
    appendLog("摄像头初始化成功");
  } catch (err) {
    console.error(err);
    
    // 详细的错误提示
    let errorMsg = "摄像头初始化失败: " + err.message;
    
    if (err.name === "NotAllowedError" || err.name === "PermissionDeniedError") {
      errorMsg = "摄像头权限被拒绝，请在设置中允许访问";
    } else if (err.name === "NotFoundError" || err.name === "DevicesNotFoundError") {
      errorMsg = "未找到摄像头设备";
    } else if (err.name === "NotReadableError" || err.name === "TrackStartError") {
      errorMsg = "摄像头被其他应用占用";
    } else if (location.protocol === "http:" && location.hostname !== "localhost" && location.hostname !== "127.0.0.1") {
      errorMsg = "iOS Safari 需要 HTTPS 才能访问摄像头。当前使用 HTTP，请使用 HTTPS 访问";
      appendLog("⚠️  提示: 请使用 https:// 访问（首次需要接受证书）");
    }
    
    setStatus("摄像头初始化失败", "error");
    appendLog(errorMsg);
  }
}

async function heartbeat() {
  try {
    const resp = await fetch(`${API_BASE}/health`, { method: "GET" });
    if (!resp.ok) {
      appendLog(`心跳失败: HTTP ${resp.status}`);
      setStatus("后端异常", "warn");
      return;
    }
    const data = await resp.json();
    if (data.status === "ok") {
      setStatus("后端正常", "ok");
    } else {
      setStatus("后端状态异常", "warn");
    }
  } catch (err) {
    appendLog("心跳请求错误: " + err.message);
    setStatus("后端不可达", "error");
  }
}

function drawBoxes(boxes) {
  const ctx = overlay.getContext("2d");
  const w = overlay.width;
  const h = overlay.height;
  ctx.clearRect(0, 0, w, h);

  ctx.lineWidth = 2;
  ctx.font = "12px -apple-system, BlinkMacSystemFont, sans-serif";

  boxes.forEach((b) => {
    const x1 = b.x1;
    const y1 = b.y1;
    const x2 = b.x2;
    const y2 = b.y2;
    const conf = b.conf != null ? b.conf.toFixed(2) : "";

    ctx.strokeStyle = "#00ff88";
    ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);

    const label = conf ? `${b.cls || 'obj'} ${conf}` : "obj";
    const textW = ctx.measureText(label).width;
    const textH = 14;

    ctx.fillStyle = "rgba(0, 0, 0, 0.6)";
    ctx.fillRect(x1, y1 - textH, textW + 6, textH);

    ctx.fillStyle = "#00ff88";
    ctx.fillText(label, x1 + 3, y1 - 3);
  });
}

// 抓帧并发给后端
async function captureAndSendFrame() {
  if (videoEl.readyState < 2) {
    return;
  }

  const canvas = document.createElement("canvas");
  canvas.width = overlay.width;
  canvas.height = overlay.height;

  const ctx = canvas.getContext("2d");
  ctx.drawImage(videoEl, 0, 0, canvas.width, canvas.height);

  const startTs = performance.now();

  canvas.toBlob(
    async (blob) => {
      if (!blob) {
        return;
      }

      try {
        const formData = new FormData();
        formData.append("frame", blob, "frame.jpg");

        const resp = await fetch(`${API_BASE}/api/frame`, {
          method: "POST",
          body: formData,
        });

        const endTs = performance.now();
        const rtt = endTs - startTs; // 往返时间

        if (!resp.ok) {
          appendLog(`后端返回错误: ${resp.status}`);
          return;
        }

        const data = await resp.json();
        const boxes = data.boxes || [];
        const latencyMs =
          typeof data.latency_ms === "number" ? data.latency_ms : rtt;

        frameCount += 1;
        latencySum += latencyMs;
        const avg = latencySum / frameCount;

        const now = performance.now();
        let fps = "-";
        if (lastFrameTime != null) {
          const dt = now - lastFrameTime;
          fps = (1000.0 / dt).toFixed(1);
        }
        lastFrameTime = now;

        // 更新 UI
        drawBoxes(boxes);
        latencyEl.textContent = latencyMs.toFixed(1);
        avgLatencyEl.textContent = avg.toFixed(1);
        fpsEl.textContent = fps;
        frameCountEl.textContent = String(frameCount);
        boxCountEl.textContent = String(boxes.length);

        appendLog(
          `frame=${frameCount}, boxes=${boxes.length}, latency=${latencyMs.toFixed(
            1
          )}ms, fps=${fps}`
        );
      } catch (err) {
        appendLog("请求失败: " + err.message);
        console.error(err);
      }
    },
    "image/jpeg",
    0.7
  );
}

function startSending() {
  const interval = Math.max(
    100,
    parseInt(intervalInput.value || "300", 10)
  );

  if (sendingTimer) {
    clearInterval(sendingTimer);
  }

  frameCount = 0;
  latencySum = 0;
  lastFrameTime = null;
  fpsEl.textContent = "-";
  frameCountEl.textContent = "0";
  avgLatencyEl.textContent = "-";
  boxCountEl.textContent = "0";

  sendingTimer = setInterval(captureAndSendFrame, interval);
  setStatus(`运行中 (间隔 ${interval}ms)`, "ok");
  appendLog(`开始发送图像, 间隔=${interval}ms`);

  startBtn.disabled = true;
  stopBtn.disabled = false;
}

function stopSending() {
  if (sendingTimer) {
    clearInterval(sendingTimer);
    sendingTimer = null;
  }
  setStatus("已停止", "warn");
  appendLog("停止发送图像");

  startBtn.disabled = false;
  stopBtn.disabled = true;
}

// 事件绑定
startBtn.addEventListener("click", startSending);
stopBtn.addEventListener("click", stopSending);

window.addEventListener("load", () => {
  setStatus("初始化摄像头...", "warn");
  initCamera();
  // 每 5 秒做一次心跳
  heartbeat();
  heartbeatTimer = setInterval(heartbeat, 5000);
});

