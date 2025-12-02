// frontend/minimap.js
// MiniMap：小雷达图，显示自己 + 危险 + 节点 + 大致方向

(function () {
  "use strict";

  if (window.MiniMap) return;

  const NavLog = window.NavLog || window.TaskLogger || {
    info: console.log,
    warn: console.warn,
    error: console.error,
  };

  class MiniMap {
    constructor() {
      this.canvas = null;
      this.ctx = null;
      this.width = 220;
      this.height = 220;
      this.state = {
        routeLength: 0,
        currentStepIndex: 0,
        hazards: [],
        nodes: [],
      };

      this._initCanvas();
      this._startRenderLoop();
    }

    _initCanvas() {
      let container = document.getElementById("luna-minimap-container");
      if (!container) {
        container = document.createElement("div");
        container.id = "luna-minimap-container";
        Object.assign(container.style, {
          position: "fixed",
          right: "12px",
          bottom: "12px",
          width: this.width + "px",
          height: this.height + "px",
          background: "rgba(0,0,0,0.45)",
          borderRadius: "10px",
          border: "1px solid rgba(255,255,255,0.2)",
          zIndex: 9999,
          overflow: "hidden",
          backdropFilter: "blur(4px)",
          color: "#fff",
          fontSize: "11px",
          fontFamily: "system-ui, -apple-system, BlinkMacSystemFont",
        });
        document.body.appendChild(container);
      }

      const title = document.createElement("div");
      title.innerText = "Luna MiniMap";
      Object.assign(title.style, {
        padding: "4px 8px",
        borderBottom: "1px solid rgba(255,255,255,0.15)",
        fontSize: "11px",
        opacity: 0.8,
      });
      container.appendChild(title);

      const canvas = document.createElement("canvas");
      canvas.width = this.width;
      canvas.height = this.height - 18;
      canvas.style.display = "block";
      container.appendChild(canvas);

      this.canvas = canvas;
      this.ctx = canvas.getContext("2d");

      NavLog.info("MiniMap", "初始化完成", {});
    }

    _startRenderLoop() {
      const draw = () => {
        this._render();
        requestAnimationFrame(draw);
      };
      requestAnimationFrame(draw);
    }

    setRouteLength(len) {
      this.state.routeLength = len || 0;
      this.state.currentStepIndex = 0;
    }

    setStepIndex(idx) {
      this.state.currentStepIndex = idx;
    }

    addHazard(relativeDirection) {
      const base = { x: 0, y: 0 };

      switch (relativeDirection) {
        case "front":
          base.y = -30;
          break;
        case "back":
          base.y = 30;
          break;
        case "left":
          base.x = -30;
          break;
        case "right":
          base.x = 30;
          break;
        default:
          base.y = -30;
      }

      this.state.hazards.push({
        x: base.x + (Math.random() * 10 - 5),
        y: base.y + (Math.random() * 10 - 5),
        ts: Date.now(),
      });

      if (this.state.hazards.length > 30) {
        this.state.hazards.shift();
      }

      NavLog.info("MiniMap", "记录危险点", { dir: relativeDirection });
    }

    addNode(nodeSummary) {
      this.state.nodes.push({
        x: Math.random() * 80 - 40,
        y: Math.random() * 80 - 40,
        type: nodeSummary.type || "facility",
        label: nodeSummary.label || nodeSummary.role || "节点",
      });

      if (window.NodeMemory) {
        window.NodeMemory.addNode({
          role: nodeSummary.role,
          type: nodeSummary.type,
          label: nodeSummary.label,
        });
      }

      if (this.state.nodes.length > 40) {
        this.state.nodes.shift();
      }

      NavLog.info("MiniMap", "记录节点", nodeSummary);
    }

    _render() {
      if (!this.ctx) return;
      const ctx = this.ctx;
      const w = this.canvas.width;
      const h = this.canvas.height;

      ctx.clearRect(0, 0, w, h);
      ctx.fillStyle = "rgba(0, 0, 0, 0.4)";
      ctx.fillRect(0, 0, w, h);

      // 网格
      ctx.strokeStyle = "rgba(255,255,255,0.06)";
      ctx.lineWidth = 1;
      ctx.beginPath();
      for (let x = 0; x <= w; x += 20) {
        ctx.moveTo(x, 0);
        ctx.lineTo(x, h);
      }
      for (let y = 0; y <= h; y += 20) {
        ctx.moveTo(0, y);
        ctx.lineTo(w, y);
      }
      ctx.stroke();

      const cx = w / 2;
      const cy = h / 2;

      // 自己
      ctx.fillStyle = "#00ffcc";
      ctx.beginPath();
      ctx.arc(cx, cy, 5, 0, Math.PI * 2);
      ctx.fill();

      // 导航方向（简化：用 stepIndex / routeLength 表示）
      if (this.state.routeLength > 0) {
        const progress = this.state.currentStepIndex / this.state.routeLength;
        const arrowLen = 40 + progress * 30;
        ctx.strokeStyle = "#00ffcc";
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        ctx.lineTo(cx, cy - arrowLen);
        ctx.stroke();
      }

      // 危险点
      const now = Date.now();
      ctx.fillStyle = "#ff5555";
      this.state.hazards = this.state.hazards.filter(hz => now - hz.ts < 10000);
      for (const hz of this.state.hazards) {
        ctx.beginPath();
        ctx.arc(cx + hz.x, cy + hz.y, 4, 0, Math.PI * 2);
        ctx.fill();
      }

      // 节点
      ctx.fillStyle = "#ffdd66";
      for (const n of this.state.nodes) {
        ctx.beginPath();
        ctx.arc(cx + n.x, cy + n.y, 3, 0, Math.PI * 2);
        ctx.fill();
      }
    }
  }

  window.MiniMap = new MiniMap();
})();
