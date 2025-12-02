// overlay.js - 检测框绘制模块

const overlay = document.getElementById("overlay");
let overlayCtx = null;

/**
 * 初始化 overlay canvas
 */
function initOverlay() {
    const camera = document.getElementById("camera");
    overlay.width = camera.videoWidth || 640;
    overlay.height = camera.videoHeight || 480;
    overlayCtx = overlay.getContext("2d");
}

/**
 * 绘制检测框
 * @param {Array} objects - 检测到的对象列表
 */
function drawDetections(objects) {
    if (!overlayCtx) {
        initOverlay();
    }
    
    const camera = document.getElementById("camera");
    overlay.width = camera.videoWidth || 640;
    overlay.height = camera.videoHeight || 480;
    
    // 清空画布
    overlayCtx.clearRect(0, 0, overlay.width, overlay.height);
    
    if (!objects || objects.length === 0) {
        return;
    }
    
    objects.forEach(obj => {
        // 解析边界框
        let x1, y1, x2, y2;
        if (Array.isArray(obj.bbox)) {
            [x1, y1, x2, y2] = obj.bbox;
        } else if (obj.x1 !== undefined) {
            x1 = obj.x1;
            y1 = obj.y1;
            x2 = obj.x2;
            y2 = obj.y2;
        } else {
            return; // 跳过无效对象
        }
        
        const width = x2 - x1;
        const height = y2 - y1;
        
        // 绘制边界框
        overlayCtx.strokeStyle = "#4ade80";
        overlayCtx.lineWidth = 2;
        overlayCtx.strokeRect(x1, y1, width, height);
        
        // 绘制标签背景
        const label = `${obj.cls || "unknown"} ${(obj.conf || 0).toFixed(2)}`;
        overlayCtx.font = "12px Arial";
        const textWidth = overlayCtx.measureText(label).width;
        
        overlayCtx.fillStyle = "rgba(74, 222, 128, 0.8)";
        overlayCtx.fillRect(x1, y1 - 18, textWidth + 4, 16);
        
        // 绘制标签文字
        overlayCtx.fillStyle = "#0b1020";
        overlayCtx.fillText(label, x1 + 2, y1 - 4);
    });
}

/**
 * 清空检测框
 */
function clearOverlay() {
    if (!overlayCtx) {
        initOverlay();
    }
    overlayCtx.clearRect(0, 0, overlay.width, overlay.height);
}

