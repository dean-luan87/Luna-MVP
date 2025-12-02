import React, { useState } from "react";

export default function AudioDebugPanel() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [ttsText, setTtsText] = useState("这是一次TTS测试。");

  async function testTTS() {
    setLoading(true);
    try {
      const res = await fetch("/api/test/feature/tts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          text: ttsText,
          voice: "zh-CN-XiaoxiaoNeural",
          rate: "+0%"
        })
      });
      const data = await res.json();
      setResult(data);
      
      // 如果成功，播放音频
      if (data.success && data.data && data.data.audio) {
        const audio = new Audio(`data:audio/mpeg;base64,${data.data.audio}`);
        audio.play().catch(e => console.error("播放失败:", e));
      }
    } catch (error) {
      setResult({ error: error.message });
    } finally {
      setLoading(false);
    }
  }

  async function testWakeup() {
    setLoading(true);
    try {
      // 模拟唤醒词测试
      const res = await fetch("/api/test/audio/test_wakeup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: "Luna你在吗" })
      });
      const data = await res.json();
      setResult(data);
    } catch (error) {
      // 如果接口不存在，使用CommandParser
      if (window.CommandParser) {
        window.CommandParser.handleASR("Luna你在吗");
        setResult({ 
          success: true, 
          message: "已通过CommandParser处理唤醒词",
          note: "后端接口未实现，使用前端CommandParser"
        });
      } else {
        setResult({ error: error.message });
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h3>🔊 音频系统检测</h3>

      <div style={{ marginBottom: 20 }}>
        <div style={{ marginBottom: 10 }}>
          <label style={{ display: "block", marginBottom: 5 }}>TTS测试文本：</label>
          <textarea
            value={ttsText}
            onChange={(e) => setTtsText(e.target.value)}
            style={{
              width: "100%",
              minHeight: "60px",
              padding: "8px",
              background: "#222",
              color: "white",
              border: "1px solid #444",
              borderRadius: 4
            }}
          />
        </div>
        <button onClick={testTTS} disabled={loading} style={btn}>
          {loading ? "测试中..." : "测试 TTS"}
        </button>
        <button onClick={testWakeup} disabled={loading} style={btn}>
          测试 唤醒词
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



