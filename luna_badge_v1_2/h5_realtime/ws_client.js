// ws_client.js - WebSocket 客户端模块（符合协议规范）

const PROTOCOL_VERSION = "1.0.0";

// 自动检测服务器地址
const SERVER_HOST = window.location.hostname || "10.183.232.224";
const SERVER_PORT = window.location.port || "8899";
const WS_PATH = "/ws";  // 也可以使用 /ws_json
const protocol = window.location.protocol === "https:" ? "wss" : "ws";
const WS_URL = `${protocol}://${SERVER_HOST}:${SERVER_PORT}${WS_PATH}`;

let ws = null;
let wsConnected = false;
let reconnectTimer = null;
let reconnectAttempts = 0;
const MAX_RECONNECT_DELAY = 10000;

// DOM 元素
const connStatusEl = document.getElementById("connStatus");

/**
 * 连接 WebSocket
 */
function connectWS() {
    if (wsConnected || ws) {
        return;
    }
    
    console.log(`[WS] 连接服务器: ${WS_URL}`);
    connStatusEl.textContent = "连接中...";
    connStatusEl.className = "status connecting";
    
    try {
        ws = new WebSocket(WS_URL);
    } catch (e) {
        console.error("[WS] 创建连接失败:", e);
        scheduleReconnect();
        return;
    }
    
    ws.onopen = () => {
        wsConnected = true;
        reconnectAttempts = 0;
        connStatusEl.textContent = "已连接";
        connStatusEl.className = "status connected";
        console.log("[WS] 连接成功");
        
        // 触发连接事件
        if (window.onWSConnected) {
            window.onWSConnected();
        }
    };
    
    ws.onclose = () => {
        wsConnected = false;
        connStatusEl.textContent = "已断开";
        connStatusEl.className = "status disconnected";
        console.log("[WS] 连接已关闭");
        
        // 触发断开事件
        if (window.onWSDisconnected) {
            window.onWSDisconnected();
        }
        
        scheduleReconnect();
    };
    
    ws.onerror = (err) => {
        console.error("[WS] 连接错误:", err);
        connStatusEl.textContent = "连接错误";
        connStatusEl.className = "status disconnected";
    };
    
    ws.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            handleMessage(data, event.data.length);
        } catch (e) {
            console.error("[WS] 消息解析失败:", e);
        }
    };
}

/**
 * 处理收到的消息（符合协议规范）
 */
function handleMessage(data, dataSize) {
    // 记录接收的数据量
    recordDataReceived(dataSize / 1024);
    
    // HeartbeatSpec: heartbeat_ack
    if (data.type === "heartbeat_ack") {
        const now = performance.now();
        const rtt = now - (data.client_ts || now);
        console.log(`[WS] 心跳确认: seq=${data.seq}, RTT=${rtt.toFixed(1)}ms`);
        return;
    }
    
    // InferSpec: infer_result
    if (data.type === "infer_result") {
        const tClientRecv = performance.now();
        const clientSendTs = data.client_ts;
        const endToEndMs = tClientRecv - clientSendTs;
        
        // 计算 RTT
        const uploadMs = data.server_ts - clientSendTs;
        const downloadMs = tClientRecv - (data.ts_server_send || tClientRecv);
        const rttMs = uploadMs + downloadMs;
        
        // 更新性能指标
        updateMetrics({
            latency: endToEndMs,
            infer_ms: data.infer_ms,
            nav_ms: data.nav_ms,
            rtt_ms: rttMs
        });
        
        // 显示推理结果
        if (window.onInferResult) {
            window.onInferResult(data);
        }
        
        return;
    }
    
    // ErrorSpec: error
    if (data.type === "error") {
        console.error(`[WS] 错误: ${data.code} - ${data.message}`);
        if (data.detail) {
            console.error(`[WS] 详情: ${data.detail}`);
        }
        alert(`错误: ${data.message}`);
        return;
    }
    
    // 兼容旧版格式
    if (data.type === "result") {
        updateMetrics({
            latency: data.latency,
            infer_ms: data.det_ms,
            nav_ms: data.nav_ms
        });
        
        if (window.onInferResult) {
            window.onInferResult(data);
        }
    }
}

/**
 * 发送消息
 */
function sendMessage(message) {
    if (!wsConnected || !ws || ws.readyState !== WebSocket.OPEN) {
        console.warn("[WS] 连接未就绪，无法发送消息");
        return false;
    }
    
    try {
        const jsonStr = JSON.stringify(message);
        ws.send(jsonStr);
        return true;
    } catch (e) {
        console.error("[WS] 发送消息失败:", e);
        return false;
    }
}

/**
 * 发送帧数据（符合 FrameSpec）
 */
function sendFrame(base64Image, frameId, clientTs) {
    const resolution = getCameraResolution();
    
    // 移除 data URL 前缀
    const imageBase64 = base64Image.includes(",") 
        ? base64Image.split(",")[1] 
        : base64Image;
    
    // FrameSpec 规范
    const frame = {
        type: "frame",
        protocol_version: PROTOCOL_VERSION,
        frame_id: frameId,
        client_ts: clientTs,
        width: resolution.width,
        height: resolution.height,
        image_base64: imageBase64,
        meta: {
            platform: /iPhone|iPad|iPod/.test(navigator.userAgent) ? "ios" : 
                     /Android/.test(navigator.userAgent) ? "android" : "web",
            user_agent: navigator.userAgent,
            auto_mode: true,
            camera_facing: "rear",
            network: getNetworkType()
        }
    };
    
    const sent = sendMessage(frame);
    if (sent) {
        recordFrameSent((JSON.stringify(frame).length) / 1024);
    }
    
    return sent;
}

/**
 * 发送心跳（符合 HeartbeatSpec）
 */
let hbSeq = 0;
function sendHeartbeat() {
    const heartbeat = {
        type: "heartbeat",
        protocol_version: PROTOCOL_VERSION,
        seq: ++hbSeq,
        client_ts: performance.now()
    };
    
    sendMessage(heartbeat);
}

/**
 * 获取网络类型
 */
function getNetworkType() {
    if (navigator.connection) {
        const conn = navigator.connection;
        if (conn.effectiveType === "4g") return "4g";
        if (conn.effectiveType === "5g" || (conn.type === "cellular" && conn.downlink > 10)) return "5g";
        if (conn.type === "wifi") return "wifi";
    }
    return "other";
}

/**
 * 断开连接
 */
function disconnectWS() {
    if (reconnectTimer) {
        clearTimeout(reconnectTimer);
        reconnectTimer = null;
    }
    
    if (ws) {
        ws.close();
        ws = null;
    }
    
    wsConnected = false;
}

/**
 * 计划重连
 */
function scheduleReconnect() {
    if (reconnectTimer) {
        return;
    }
    
    reconnectAttempts++;
    const delay = Math.min(MAX_RECONNECT_DELAY, 1000 * reconnectAttempts);
    
    console.log(`[WS] 计划重连，延迟 ${delay}ms (尝试 ${reconnectAttempts})`);
    
    reconnectTimer = setTimeout(() => {
        reconnectTimer = null;
        if (!wsConnected) {
            connectWS();
        }
    }, delay);
}

