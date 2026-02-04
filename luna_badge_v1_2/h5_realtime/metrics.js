// metrics.js - 性能监控模块

const PROTOCOL_VERSION = "1.0.0";

let frameCount = 0;
let uploadKB = 0;
let downloadKB = 0;
let totalFramesSent = 0;

// DOM 元素
const fpsEl = document.getElementById("fps");
const latencyEl = document.getElementById("latency");
const inferTimeEl = document.getElementById("inferTime");
const navTimeEl = document.getElementById("navTime");
const rttEl = document.getElementById("rtt");
const uploadRateEl = document.getElementById("uploadRate");
const downloadRateEl = document.getElementById("downloadRate");
const frameCountEl = document.getElementById("frameCount");

/**
 * 更新 FPS
 */
function updateFPS() {
    fpsEl.textContent = frameCount;
    frameCount = 0;
}

/**
 * 更新流量统计
 */
function updateTraffic() {
    uploadRateEl.textContent = uploadKB.toFixed(1);
    downloadRateEl.textContent = downloadKB.toFixed(1);
    uploadKB = 0;
    downloadKB = 0;
}

/**
 * 更新延迟指标
 * @param {Object} metrics - 性能指标
 */
function updateMetrics(metrics) {
    if (metrics.latency !== undefined) {
        latencyEl.textContent = metrics.latency.toFixed(1);
    }
    if (metrics.infer_ms !== undefined) {
        inferTimeEl.textContent = metrics.infer_ms.toFixed(1);
    }
    if (metrics.nav_ms !== undefined) {
        navTimeEl.textContent = metrics.nav_ms.toFixed(1);
    }
    if (metrics.rtt_ms !== undefined) {
        rttEl.textContent = metrics.rtt_ms.toFixed(1);
    }
}

/**
 * 记录发送的帧
 */
function recordFrameSent(sizeKB) {
    frameCount++;
    totalFramesSent++;
    uploadKB += sizeKB;
    frameCountEl.textContent = totalFramesSent;
}

/**
 * 记录接收的数据
 */
function recordDataReceived(sizeKB) {
    downloadKB += sizeKB;
}

/**
 * 每秒更新统计
 */
setInterval(() => {
    updateFPS();
    updateTraffic();
}, 1000);
















