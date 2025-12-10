// 性能统计全局变量
let frameCount = 0;
let uploadKB = 0;
let downloadKB = 0;

// DOM
const fpsEl = document.getElementById("fps");
const latencyEl = document.getElementById("latency");
const uploadRateEl = document.getElementById("uploadRate");
const downloadRateEl = document.getElementById("downloadRate");
const resultTextEl = document.getElementById("resultText");
const connStatusEl = document.getElementById("connStatus");

// 每秒刷新一次 FPS / 带宽
setInterval(() => {
  fpsEl.textContent = frameCount;
  frameCount = 0;

  uploadRateEl.textContent = uploadKB.toFixed(1);
  downloadRateEl.textContent = downloadKB.toFixed(1);
  uploadKB = 0;
  downloadKB = 0;
}, 1000);

function addUploadBytes(bytes) {
  uploadKB += bytes / 1024.0;
}

function addDownloadBytes(bytes) {
  downloadKB += bytes / 1024.0;
}

function setLatency(latencyMs) {
  latencyEl.textContent = latencyMs;
}

function setResultText(obj) {
  resultTextEl.innerText = JSON.stringify(obj, null, 2);
}

function setConnStatus(status) {
  connStatusEl.textContent = status;
}





