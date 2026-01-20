// app.js - 主应用逻辑

const FRAME_INTERVAL_MS = 200;  // 每 200ms 发送一帧
const HEARTBEAT_INTERVAL_MS = 3000;  // 每 3 秒发送心跳

let frameId = 0;
let frameTimer = null;
let heartbeatTimer = null;

// DOM 元素
const btnConnect = document.getElementById("btnConnect");
const btnStartCamera = document.getElementById("btnStartCamera");
const resultTextEl = document.getElementById("resultText");
const navResultEl = document.getElementById("navResult");

/**
 * 启动自动帧发送
 */
function startFrameLoop() {
    if (frameTimer) {
        return;
    }
    
    frameTimer = setInterval(() => {
        if (!wsConnected) {
            return;
        }
        
        const frame = captureFrame();
        if (!frame) {
            console.warn("[APP] 无法捕获帧");
            return;
        }
        
        const clientTs = performance.now();
        frameId++;
        
        sendFrame(frame, frameId, clientTs);
    }, FRAME_INTERVAL_MS);
    
    console.log("[APP] 启动自动帧发送");
}

/**
 * 停止自动帧发送
 */
function stopFrameLoop() {
    if (frameTimer) {
        clearInterval(frameTimer);
        frameTimer = null;
        console.log("[APP] 停止自动帧发送");
    }
}

/**
 * 启动心跳
 */
function startHeartbeat() {
    if (heartbeatTimer) {
        return;
    }
    
    heartbeatTimer = setInterval(() => {
        if (wsConnected) {
            sendHeartbeat();
        }
    }, HEARTBEAT_INTERVAL_MS);
    
    console.log("[APP] 启动心跳");
}

/**
 * 停止心跳
 */
function stopHeartbeat() {
    if (heartbeatTimer) {
        clearInterval(heartbeatTimer);
        heartbeatTimer = null;
        console.log("[APP] 停止心跳");
    }
}

/**
 * 处理推理结果
 */
window.onInferResult = (data) => {
    // 显示检测结果
    if (data.objects && data.objects.length > 0) {
        drawDetections(data.objects);
        resultTextEl.textContent = JSON.stringify(data.objects, null, 2);
    } else {
        clearOverlay();
        resultTextEl.textContent = "未检测到对象";
    }
    
    // 显示导航结果
    if (data.nav) {
        const nav = data.nav;
        navResultEl.innerHTML = `
            <div><strong>决策:</strong> ${nav.decision || "未知"}</div>
            <div><strong>危险等级:</strong> ${nav.danger_level || 0}</div>
            <div><strong>提示:</strong> ${nav.text || ""}</div>
        `;
    } else {
        navResultEl.textContent = "";
    }
};

/**
 * WebSocket 连接成功回调
 */
window.onWSConnected = () => {
    startFrameLoop();
    startHeartbeat();
    btnConnect.textContent = "断开连接";
};

/**
 * WebSocket 断开回调
 */
window.onWSDisconnected = () => {
    stopFrameLoop();
    stopHeartbeat();
    btnConnect.textContent = "连接服务器";
};

/**
 * 连接按钮点击
 */
btnConnect.addEventListener("click", () => {
    if (!wsConnected) {
        connectWS();
    } else {
        disconnectWS();
    }
});

/**
 * 启动相机按钮点击
 */
btnStartCamera.addEventListener("click", async () => {
    const success = await startCamera();
    if (success) {
        initOverlay();
        btnStartCamera.disabled = true;
        btnStartCamera.textContent = "相机已启动";
    }
});

/**
 * 页面加载完成后自动启动相机
 */
window.addEventListener("load", async () => {
    console.log("[APP] 页面加载完成");
    
    // 自动启动相机
    const success = await startCamera();
    if (success) {
        initOverlay();
        btnStartCamera.disabled = true;
        btnStartCamera.textContent = "相机已启动";
    }
});

/**
 * 页面隐藏时暂停，显示时恢复
 */
document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
        stopFrameLoop();
        stopHeartbeat();
    } else {
        if (wsConnected) {
            startFrameLoop();
            startHeartbeat();
        }
    }
});
















