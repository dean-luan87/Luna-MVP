// frontend/components/GuidanceBubble.js
// UI标准组件：策略提示卡片
// 支持React和IIFE两种模式

(function () {
  "use strict";
  if (window.GuidanceBubble) return;

  /**
   * GuidanceBubble组件（IIFE版本）
   * 用于非React环境
   */
  class GuidanceBubbleClass {
    /**
     * 创建并显示提示气泡
     * @param {Object} options - 选项
     * @param {string} options.message - 提示消息
     * @param {string} options.severity - 严重程度: critical/warning/info/success
     * @param {number} options.duration - 显示时长（毫秒），默认4000
     * @param {string} options.position - 位置: top-right/top-left/bottom-right/bottom-left，默认bottom-right
     */
    static show(options) {
      const {
        message,
        severity = "info",
        duration = 4000,
        position = "bottom-right",
      } = options;

      if (!message) {
        console.warn("[GuidanceBubble] message is required");
        return;
      }

      // 移除旧的bubble（如果存在）
      const oldBubble = document.getElementById("guidance-bubble");
      if (oldBubble) {
        oldBubble.remove();
      }

      // 创建bubble元素
      const bubble = document.createElement("div");
      bubble.id = "guidance-bubble";
      bubble.className = `guidance-bubble guidance-bubble-${severity}`;

      // 设置样式
      const styles = {
        position: "fixed",
        zIndex: "10000",
        padding: "12px 16px",
        borderRadius: "8px",
        boxShadow: "0 4px 12px rgba(0,0,0,0.15)",
        display: "flex",
        alignItems: "center",
        gap: "8px",
        fontFamily: "system-ui, -apple-system, sans-serif",
        fontSize: "14px",
        lineHeight: "1.5",
        maxWidth: "320px",
        animation: "guidanceBubbleSlideIn 0.3s ease-out",
        pointerEvents: "none",
      };

      // 根据severity设置颜色
      const colorMap = {
        critical: { bg: "rgba(220,53,69,0.95)", text: "#fff", icon: "🛑" },
        warning: { bg: "rgba(255,193,7,0.95)", text: "#000", icon: "⚠️" },
        info: { bg: "rgba(0,123,255,0.95)", text: "#fff", icon: "ℹ️" },
        success: { bg: "rgba(40,167,69,0.95)", text: "#fff", icon: "✅" },
      };

      const colors = colorMap[severity] || colorMap.info;
      styles.background = colors.bg;
      styles.color = colors.text;

      // 设置位置
      const positionMap = {
        "top-right": { top: "20px", right: "20px" },
        "top-left": { top: "20px", left: "20px" },
        "bottom-right": { bottom: "20px", right: "20px" },
        "bottom-left": { bottom: "20px", left: "20px" },
      };

      const pos = positionMap[position] || positionMap["bottom-right"];
      Object.assign(styles, pos);

      // 应用样式
      Object.assign(bubble.style, styles);

      // 创建图标
      const icon = document.createElement("span");
      icon.className = "guidance-bubble-icon";
      icon.textContent = colors.icon + " ";
      icon.style.fontSize = "16px";

      // 创建文本
      const text = document.createElement("span");
      text.className = "guidance-bubble-text";
      text.textContent = message;

      // 组装
      bubble.appendChild(icon);
      bubble.appendChild(text);
      document.body.appendChild(bubble);

      // 添加CSS动画（如果还没有）
      if (!document.getElementById("guidance-bubble-styles")) {
        const styleSheet = document.createElement("style");
        styleSheet.id = "guidance-bubble-styles";
        styleSheet.textContent = `
          @keyframes guidanceBubbleSlideIn {
            from {
              opacity: 0;
              transform: translateY(20px);
            }
            to {
              opacity: 1;
              transform: translateY(0);
            }
          }
          @keyframes guidanceBubbleSlideOut {
            from {
              opacity: 1;
              transform: translateY(0);
            }
            to {
              opacity: 0;
              transform: translateY(-20px);
            }
          }
        `;
        document.head.appendChild(styleSheet);
      }

      // 自动隐藏
      setTimeout(() => {
        bubble.style.animation = "guidanceBubbleSlideOut 0.3s ease-in";
        setTimeout(() => {
          if (bubble.parentNode) {
            bubble.remove();
          }
        }, 300);
      }, duration);
    }

    /**
     * 隐藏当前bubble
     */
    static hide() {
      const bubble = document.getElementById("guidance-bubble");
      if (bubble) {
        bubble.style.animation = "guidanceBubbleSlideOut 0.3s ease-in";
        setTimeout(() => {
          if (bubble.parentNode) {
            bubble.remove();
          }
        }, 300);
      }
    }
  }

  // React版本（如果React可用）
  if (typeof window !== "undefined" && window.React) {
    const React = window.React;
    const { useState, useEffect } = React;

    /**
     * React版本的GuidanceBubble组件
     */
    const GuidanceBubbleReact = ({ message, severity = "info", duration = 4000, position = "bottom-right" }) => {
      const [visible, setVisible] = useState(false);

      useEffect(() => {
        if (message) {
          setVisible(true);
          const timer = setTimeout(() => {
            setVisible(false);
          }, duration);
          return () => clearTimeout(timer);
        }
      }, [message, duration]);

      if (!visible || !message) return null;

      const colorMap = {
        critical: { bg: "rgba(220,53,69,0.95)", text: "#fff", icon: "🛑" },
        warning: { bg: "rgba(255,193,7,0.95)", text: "#000", icon: "⚠️" },
        info: { bg: "rgba(0,123,255,0.95)", text: "#fff", icon: "ℹ️" },
        success: { bg: "rgba(40,167,69,0.95)", text: "#fff", icon: "✅" },
      };

      const colors = colorMap[severity] || colorMap.info;

      const positionMap = {
        "top-right": { top: "20px", right: "20px" },
        "top-left": { top: "20px", left: "20px" },
        "bottom-right": { bottom: "20px", right: "20px" },
        "bottom-left": { bottom: "20px", left: "20px" },
      };

      const pos = positionMap[position] || positionMap["bottom-right"];

      return React.createElement(
        "div",
        {
          className: `guidance-bubble guidance-bubble-${severity}`,
          style: {
            position: "fixed",
            ...pos,
            zIndex: 10000,
            padding: "12px 16px",
            borderRadius: "8px",
            boxShadow: "0 4px 12px rgba(0,0,0,0.15)",
            display: "flex",
            alignItems: "center",
            gap: "8px",
            fontFamily: "system-ui, -apple-system, sans-serif",
            fontSize: "14px",
            lineHeight: "1.5",
            maxWidth: "320px",
            background: colors.bg,
            color: colors.text,
            animation: "guidanceBubbleSlideIn 0.3s ease-out",
          },
        },
        React.createElement("span", { className: "guidance-bubble-icon", style: { fontSize: "16px" } }, colors.icon + " "),
        React.createElement("span", { className: "guidance-bubble-text" }, message)
      );
    };

    window.GuidanceBubbleReact = GuidanceBubbleReact;
  }

  // 挂载到全局
  window.GuidanceBubble = GuidanceBubbleClass;

  console.log("[GuidanceBubble] 策略提示卡片组件已加载");
})();



