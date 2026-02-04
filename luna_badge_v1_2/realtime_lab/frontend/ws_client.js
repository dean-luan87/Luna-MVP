let ws = null;
let lastPingTs = 0;
let reconnectTimer = null;

function getWsUrl() {
  // 根据当前页面协议自动选择 WebSocket 协议
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const host = window.location.hostname;
  const port = "5001";  // 使用 5001 避免与 AirPlay 冲突
  const wsUrl = `${protocol}//${host}:${port}/ws`;
  console.log(`[WS] WebSocket URL: ${wsUrl}`);
  return wsUrl;
}

function connectWS() {
  const url = getWsUrl();
  console.log("[WS] connect to", url);

  ws = new WebSocket(url);

  ws.onopen = () => {
    console.log("[WS] open");
    setConnStatus("Connected");
    // 清理重连timer
    if (reconnectTimer) {
      clearTimeout(reconnectTimer);
      reconnectTimer = null;
    }
  };

  ws.onclose = (event) => {
    console.log("[WS] close", event.code, event.reason);
    setConnStatus("Disconnected");
    // 延迟重连
    if (!event.wasClean) {
      console.warn("[WS] 非正常关闭，将在 2 秒后重连...");
    }
    reconnectTimer = setTimeout(connectWS, 2000);
  };

  ws.onerror = (err) => {
    console.error("[WS] error", err);
    console.error("[WS] 连接失败，请检查：");
    console.error("  1. 后端服务器是否运行");
    console.error("  2. WebSocket URL 是否正确:", url);
    console.error("  3. SSL 证书是否已接受");
    setConnStatus("Error");
  };

  ws.onmessage = (event) => {
    addDownloadBytes(event.data.length);

    let data;
    try {
      data = JSON.parse(event.data);
    } catch (e) {
      console.warn("invalid json:", e);
      return;
    }

    if (data.type === "result") {
      setLatency(data.latency);
      setResultText(data);
      if (Array.isArray(data.objects)) {
        drawDetections(data.objects);
      }
    } else if (data.type === "pong") {
      // 可以在这里算网络 RTT
    } else if (data.type === "error") {
      setResultText(data);
    }
  };
}

// 心跳（可选）
setInterval(() => {
  if (!ws || ws.readyState !== WebSocket.OPEN) return;
  ws.send(JSON.stringify({ type: "ping", ts: performance.now() }));
}, 5000);

connectWS();

// 供 app.js 判断
function wsReady() {
  return ws && ws.readyState === WebSocket.OPEN;
}

function wsSend(obj) {
  if (!wsReady()) return;
  const text = JSON.stringify(obj);
  addUploadBytes(text.length);
  ws.send(text);
}

