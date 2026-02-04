import React, { useState } from "react";

export default function SceneDescribePanel() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  async function describe() {
    setLoading(true);
    try {
      // 从摄像头捕获当前帧
      const video = document.getElementById("test_video");
      if (!video || video.videoWidth === 0) {
        setResult({ error: "请先启动摄像头" });
        setLoading(false);
        return;
      }

      const canvas = document.createElement("canvas");
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(video, 0, 0);

      const blob = await new Promise((resolve) => {
        canvas.toBlob(resolve);
      });

      const formData = new FormData();
      formData.append("image", blob);

      const res = await fetch("/api/navigation/describe_scene", {
        method: "POST",
        body: formData
      });
      const data = await res.json();
      setResult(data);
    } catch (error) {
      setResult({ error: error.message });
    } finally {
      setLoading(false);
    }
  }

  async function queryScene(query) {
    setLoading(true);
    try {
      const res = await fetch("/api/navigation/scene_query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query })
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
      <h3>🌍 场景描述（Scene Description Engine）</h3>

      <div style={{ marginBottom: 20 }}>
        <button onClick={describe} disabled={loading} style={btn}>
          {loading ? "分析中..." : "📷 描述当前场景"}
        </button>
        <button onClick={() => queryScene("你看到什么")} disabled={loading} style={btn}>
          ❓ 你看到什么
        </button>
        <button onClick={() => queryScene("前面有没有人")} disabled={loading} style={btn}>
          ❓ 前面有没有人
        </button>
        <button onClick={() => queryScene("有没有台阶")} disabled={loading} style={btn}>
          ❓ 有没有台阶
        </button>
      </div>

      {result && (
        <div style={{ marginTop: 20 }}>
          {result.success && result.data && result.data.description && (
            <div style={{ 
              background: "#222", 
              padding: 20, 
              borderRadius: 8,
              marginBottom: 10
            }}>
              <h4 style={{ marginTop: 0 }}>场景描述：</h4>
              <p style={{ lineHeight: 1.6 }}>{result.data.description.summary || result.data.description}</p>
              {result.data.description.scene_type && (
                <p><strong>场景类型：</strong>{result.data.description.scene_type}</p>
              )}
            </div>
          )}
          <pre style={{ background: "#222", padding: 20, overflow: "auto", maxHeight: "400px" }}>
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}

const btn = {
  padding: "10px 20px",
  marginRight: 10,
  borderRadius: 6,
  background: "#444",
  border: "none",
  color: "white",
  cursor: "pointer",
  marginTop: 10
};



