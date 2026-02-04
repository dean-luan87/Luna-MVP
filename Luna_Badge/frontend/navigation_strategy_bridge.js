// frontend/navigation_strategy_bridge.js
// 策略事件 → NavigationFSM 行为映射
// 收到策略事件后，根据内容去调用 NavigationFSM.handleEvent(...)

(function () {
  "use strict";
  if (window.NavigationStrategyBridge) return;

  const Hooks = window.Hooks || { onActionSuggest: [] };
  const EventDispatcher = window.EventDispatcher || { subscribe: () => {} };

  function mapStrategyToNavEvent(strategy) {
    const severity = strategy.severity || "info";
    const type = strategy.type || "hazard";
    const code = strategy.code || "";

    // 根据策略代码和严重程度映射导航事件
    // critical级别 → 建议停下
    if (severity === "critical") {
      return {
        type: "nav_progress",
        action: "GUIDANCE_STOP",
        reason: "critical_hazard",
      };
    }

    // 危险策略且距离很近 → 放慢速度
    if (
      (type === "hazard" || code.includes("HAZARD") || code.includes("WATER") || code.includes("SHADOW")) &&
      strategy.distance &&
      strategy.distance < 1.0
    ) {
      return {
        type: "nav_progress",
        action: "GUIDANCE_SLOW",
        reason: "near_hazard",
      };
    }

    // 弱光/反光等环境策略 → 仅提示，不改变导航状态
    if (
      code.includes("LOW_LIGHT") ||
      code.includes("REFLECTIVE") ||
      code.includes("BACKLIGHT") ||
      code.includes("MULTI_LIGHT")
    ) {
      return null; // 不改变导航状态
    }

    // 其他情况不改变状态，仅作为提示
    return null;
  }

  function handleStrategy(strategy) {
    const fsm = window.NavigationFSM;
    if (!fsm) {
      console.warn("[NavigationStrategyBridge] NavigationFSM 未找到");
      return;
    }

    const navEvent = mapStrategyToNavEvent(strategy);
    if (!navEvent) {
      // 不改变导航状态，仅作为提示
      return;
    }

    try {
      // 尝试调用 handleEvent 方法
      if (typeof fsm.handleEvent === "function") {
        fsm.handleEvent({
          type: navEvent.type,
          action: navEvent.action,
          reason: navEvent.reason,
          source: "Strategy",
          code: strategy.code || "NAV_STRATEGY",
          severity: strategy.severity,
          distance: strategy.distance,
          direction: strategy.direction,
        });

        if (window.__debugPanel) {
          if (typeof window.__debugPanel.logNav === "function") {
            window.__debugPanel.logNav(
              `🎛 策略触发导航事件: ${navEvent.action} (code=${strategy.code || "NAV_STRATEGY"})`
            );
          } else if (typeof window.__debugPanel.logTask === "function") {
            window.__debugPanel.logTask(
              `🎛 策略触发导航事件: ${navEvent.action} (code=${strategy.code || "NAV_STRATEGY"})`
            );
          }
        }

        console.log(
          `[NavigationStrategyBridge] 策略触发导航事件: ${navEvent.action}`,
          strategy
        );
      } else if (typeof fsm.onHazard === "function") {
        // 降级：使用onHazard方法
        fsm.onHazard({
          type: strategy.code || "NAV_STRATEGY",
          distance_m: strategy.distance || 0,
          risk: strategy.severity || "warning",
          text: strategy.message || null,
        });
      } else {
        console.warn("[NavigationStrategyBridge] NavigationFSM 没有 handleEvent 或 onHazard 方法");
      }
    } catch (e) {
      console.error("[NavigationStrategyBridge] 调用 NavigationFSM 出错:", e);
    }
  }

  // 处理策略事件的函数
  function handleStrategyEvent(data) {
    handleStrategy({
      severity: data.severity || (data.distance && data.distance < 0.5 ? "critical" : "warning"),
      type: data.type || "hazard",
      code: data.code || "NAV_STRATEGY",
      message: data.message,
      distance: data.distance,
      direction: data.direction,
      ...data,
    });
  }

  // 绑定 Hooks.onActionSuggest
  if (Hooks.onActionSuggest && Array.isArray(Hooks.onActionSuggest)) {
    Hooks.onActionSuggest.push(handleStrategyEvent);
  }

  // 同时监听EventDispatcher的NAV_GUIDANCE事件
  if (EventDispatcher.subscribe) {
    EventDispatcher.subscribe(function (event) {
      if (event.type === "NAV_GUIDANCE") {
        handleStrategy({
          severity: event.severity || "info",
          type: "guidance",
          code: event.code || "NAV_STRATEGY",
          message: event.message,
          distance: event.extra?.distance,
          direction: event.extra?.direction,
          ...event,
        });
      }
    });
  }

  window.NavigationStrategyBridge = {
    handleStrategy: handleStrategy,
    mapStrategyToNavEvent: mapStrategyToNavEvent,
  };

  console.log("[NavigationStrategyBridge] 策略→导航联动桥接已加载");
})();



