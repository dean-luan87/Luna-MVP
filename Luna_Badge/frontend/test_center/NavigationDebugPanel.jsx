import React, { useState } from "react";

export default function NavigationDebugPanel() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  async function simulateStep(step) {
    setLoading(true);
    try {
      const res = await fetch("/api/test/navigation/simulate_step", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ step })
      });
      const data = await res.json();
      setResult(data);
    } catch (error) {
      setResult({ error: error.message });
    } finally {
      setLoading(false);
    }
  }

  async function getNavStatus() {
    setLoading(true);
    try {
      const res = await fetch("/api/test/feature/navigation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: "status" })
      });
      const data = await res.json();
      setResult(data);
    } catch (error) {
      setResult({ error: error.message });
    } finally {
      setLoading(false);
    }
  }

  async function startNav() {
    setLoading(true);
    try {
      const res = await fetch("/api/test/feature/navigation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          action: "start",
          destination: "测试目的地",
          route_segments: []
        })
      });
      const data = await res.json();
      setResult(data);
    } catch (error) {
      setResult({ error: error.message });
    } finally {
      setLoading(false);
    }
  }

  async function stopNav() {
    setLoading(true);
    try {
      const res = await fetch("/api/test/feature/navigation", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: "stop" })
      });
      const data = await res.json();
      setResult(data);
    } catch (error) {
      setResult({ error: error.message });
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h3>🧭 导航调试面板</h3>

      <div style={{ marginBottom: 20 }}>
        <button onClick={() => simulateStep("turn_left")} disabled={loading} style={btn}>
          ← 左转
        </button>
        <button onClick={() => simulateStep("turn_right")} disabled={loading} style={btn}>
          → 右转
        </button>
        <button onClick={() => simulateStep("go_straight")} disabled={loading} style={btn}>
          ↑ 直行
        </button>
        <button onClick={() => simulateStep("turn_around")} disabled={loading} style={btn}>
          ↻ 掉头
        </button>
      </div>

      <div style={{ marginBottom: 20 }}>
        <button onClick={getNavStatus} disabled={loading} style={btn}>
          📊 获取状态
        </button>
        <button onClick={startNav} disabled={loading} style={btn}>
          ▶ 启动导航
        </button>
        <button onClick={stopNav} disabled={loading} style={btn}>
          ⏹ 停止导航
        </button>
      </div>

      {result && (
        <pre style={{ marginTop: 20, background: "#222", padding: 20, overflow: "auto", maxHeight: "400px" }}>
          {JSON.stringify(result, null, 2)}
        </pre>
      )}
    </div>
  );
}

const btn = {
  padding: "10px 20px",
  marginRight: 10,
  marginTop: 10,
  borderRadius: 6,
  background: "#444",
  border: "none",
  color: "white",
  cursor: "pointer"
};



