// frontend/strategy_ui.js
// 策略 UI 展示条（右下角浮层）
// 在页面右下角显示一个"导航提示条"，展示最近一次策略提示（弱光 / 反光 / 积水等）

(function () {
  "use strict";
  if (window.StrategyUI) return;

  const Hooks = window.Hooks || { onActionSuggest: [], emit: () => {} };
  const EventDispatcher = window.EventDispatcher || { subscribe: () => {} };

  function createBar() {
    let bar = document.getElementById("luna_strategy_bar");
    if (bar) return bar;

    bar = document.createElement("div");
    bar.id = "luna_strategy_bar";
    bar.style.position = "fixed";
    bar.style.right = "12px";
    bar.style.bottom = "12px";
    bar.style.maxWidth = "80vw";
    bar.style.zIndex = "9999";
    bar.style.padding = "8px 12px";
    bar.style.borderRadius = "999px";
    bar.style.background = "rgba(0,0,0,0.75)";
    bar.style.color = "#fff";
    bar.style.fontSize = "14px";
    bar.style.lineHeight = "1.4";
    bar.style.display = "none";
    bar.style.boxShadow = "0 2px 8px rgba(0,0,0,0.4)";
    bar.style.pointerEvents = "none";
    bar.style.transition = "opacity 0.25s ease";
    bar.style.fontFamily = "system-ui, -apple-system, sans-serif";

    const icon = document.createElement("span");
    icon.id = "luna_strategy_bar_icon";
    icon.style.marginRight = "6px";

    const text = document.createElement("span");
    text.id = "luna_strategy_bar_text";

    bar.appendChild(icon);
    bar.appendChild(text);
    document.body.appendChild(bar);
    return bar;
  }

  function updateBar(event) {
    const bar = createBar();
    const icon = document.getElementById("luna_strategy_bar_icon");
    const text = document.getElementById("luna_strategy_bar_text");

    if (!icon || !text) return;

    const severity = event.severity || "info";
    let emo = "ℹ️";
    let bg = "rgba(0,0,0,0.75)";

    if (severity === "critical") {
      emo = "🛑";
      bg = "rgba(220,53,69,0.9)";
    } else if (severity === "warning") {
      emo = "⚠️";
      bg = "rgba(255,193,7,0.95)";
    } else if (severity === "success") {
      emo = "✅";
      bg = "rgba(40,167,69,0.9)";
    }

    icon.textContent = emo + " ";
    text.textContent = event.message || "导航提示";

    bar.style.background = bg;
    bar.style.display = "block";
    bar.style.opacity = "1";

    // 播放声音（如果SoundPack可用）
    if (window.SoundPack && typeof window.SoundPack.play === "function") {
      window.SoundPack.play(severity);
    }

    // 自动淡出
    clearTimeout(bar._hideTimer);
    bar._hideTimer = setTimeout(function () {
      bar.style.opacity = "0";
      setTimeout(function () {
        bar.style.display = "none";
      }, 300);
    }, event.durationMs || 3500);
  }

  // 注册到 Hooks.onActionSuggest
  function register() {
    if (Hooks.onActionSuggest && Array.isArray(Hooks.onActionSuggest)) {
      Hooks.onActionSuggest.push(function (data) {
        // data 形如：{ type, direction, distance, message, severity, code, ... }
        const event = {
          severity: data.severity || (data.distance && data.distance < 0.5 ? "critical" : "warning"),
          message:
            data.message ||
            (window.SpeechPolicy && typeof window.SpeechPolicy.getHazardSentence === "function"
              ? window.SpeechPolicy.getHazardSentence(data)
              : "请注意前方情况。"),
          durationMs: 4000,
          code: data.code || "NAV_STRATEGY",
        };
        updateBar(event);
      });
    }

    // 同时监听EventDispatcher的NAV_GUIDANCE事件
    if (EventDispatcher.subscribe) {
      EventDispatcher.subscribe(function (event) {
        if (event.type === "NAV_GUIDANCE") {
          updateBar({
            severity: event.severity || "info",
            message: event.message || "导航提示",
            code: event.code || "NAV_STRATEGY",
            durationMs: 4000,
          });
        }
      });
    }
  }

  // 延迟注册，确保Hooks已加载
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", register);
  } else {
    setTimeout(register, 100);
  }

  window.StrategyUI = {
    show: updateBar,
    update: updateBar,
  };

  console.log("[StrategyUI] 导航策略浮层已加载");
})();



