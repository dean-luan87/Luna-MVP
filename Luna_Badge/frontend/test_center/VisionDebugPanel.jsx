import React, { useState } from "react";

export default function VisionDebugPanel() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  async function testYOLO() {
    setLoading(true);
    try {
      const res = await fetch("/api/test/feature/yolo", {
        method: "POST",
        body: createFormDataFromCamera()
      });
      const data = await res.json();
      setResult(data);
    } catch (error) {
      setResult({ error: error.message });
    } finally {
      setLoading(false);
    }
  }

  async function testOCR() {
    setLoading(true);
    try {
      const res = await fetch("/api/test/feature/ocr", {
        method: "POST",
        body: createFormDataFromCamera()
      });
      const data = await res.json();
      setResult(data);
    } catch (error) {
      setResult({ error: error.message });
    } finally {
      setLoading(false);
    }
  }

  async function testHazard() {
    setLoading(true);
    try {
      const res = await fetch("/api/test/feature/hazard", {
        method: "POST",
        body: createFormDataFromCamera()
      });
      const data = await res.json();
      setResult(data);
    } catch (error) {
      setResult({ error: error.message });
    } finally {
      setLoading(false);
    }
  }

  async function testStep() {
    setLoading(true);
    try {
      const res = await fetch("/api/test/feature/step", {
        method: "POST",
        body: createFormDataFromCamera()
      });
      const data = await res.json();
      setResult(data);
    } catch (error) {
      setResult({ error: error.message });
    } finally {
      setLoading(false);
    }
  }

  async function visionDebug() {
    setLoading(true);
    try {
      const res = await fetch("/api/test/vision/debug", {
        method: "POST",
        body: createFormDataFromCamera()
      });
      const data = await res.json();
      setResult(data);
    } catch (error) {
      setResult({ error: error.message });
    } finally {
      setLoading(false);
    }
  }

  function createFormDataFromCamera() {
    // 如果有摄像头，从video元素捕获帧
    const video = document.getElementById("test_video");
    if (video && video.videoWidth > 0) {
      const canvas = document.createElement("canvas");
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(video, 0, 0);
      return new Promise((resolve) => {
        canvas.toBlob((blob) => {
          const formData = new FormData();
          formData.append("image", blob);
          resolve(formData);
        });
      });
    }
    // 否则返回空FormData（需要用户上传图片）
    return new FormData();
  }

  return (
    <div>
      <h3>👁 视觉功能调试</h3>

      <div style={{ marginBottom: 20 }}>
        <button onClick={testYOLO} disabled={loading} style={btnStyle}>
          {loading ? "测试中..." : "测试 YOLO 检测"}
        </button>
        <button onClick={testOCR} disabled={loading} style={btnStyle}>
          测试 OCR 识别
        </button>
        <button onClick={testHazard} disabled={loading} style={btnStyle}>
          测试 危险检测
        </button>
        <button onClick={testStep} disabled={loading} style={btnStyle}>
          测试 台阶检测
        </button>
        <button onClick={visionDebug} disabled={loading} style={btnStyle}>
          🔍 完整视觉调试
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

const btnStyle = {
  padding: "10px 18px",
  marginRight: 10,
  marginTop: 10,
  borderRadius: 6,
  background: "#444",
  border: "none",
  cursor: "pointer",
  color: "white"
};



