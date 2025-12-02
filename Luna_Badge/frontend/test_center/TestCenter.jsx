import React, { useEffect, useState } from "react";
import VisionDebugPanel from "./VisionDebugPanel";
import NavigationDebugPanel from "./NavigationDebugPanel";
import AudioDebugPanel from "./AudioDebugPanel";
import SceneDescribePanel from "./SceneDescribePanel";

export default function TestCenter() {
  const [activeTab, setActiveTab] = useState("vision");

  return (
    <div style={{ padding: "20px", background: "#111", color: "white" }}>
      <h2 style={{ marginBottom: 20 }}>Luna Badge v1.2.0 — 调试中心</h2>

      <div style={{ marginBottom: 20 }}>
        {["vision", "navigation", "audio", "scene"].map(tab => (
          <button
            key={tab}
            style={{
              padding: "10px 20px",
              marginRight: 8,
              borderRadius: 6,
              border: "none",
              background: activeTab === tab ? "#3b82f6" : "#333",
              color: "white",
              cursor: "pointer",
            }}
            onClick={() => setActiveTab(tab)}
          >
            {tab === "vision" && "👁 视觉测试"}
            {tab === "navigation" && "🧭 导航测试"}
            {tab === "audio" && "🔊 音频测试"}
            {tab === "scene" && "🌍 场景描述"}
          </button>
        ))}
      </div>

      {activeTab === "vision" && <VisionDebugPanel />}
      {activeTab === "navigation" && <NavigationDebugPanel />}
      {activeTab === "audio" && <AudioDebugPanel />}
      {activeTab === "scene" && <SceneDescribePanel />}
    </div>
  );
}



