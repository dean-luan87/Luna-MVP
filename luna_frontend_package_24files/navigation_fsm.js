// frontend/navigation_fsm.js
// 一期步行导航 FSM：YOLO → FSM → taskChain

(function () {
  "use strict";

  if (window.NavigationFSM) return;

  const logger = window.TaskLogger || {
    info: console.log,
    warn: console.warn,
    error: console.error,
  };

  class NavigationFSMClass {
    constructor() {
      this.state = "IDLE"; 
      this.currentRoute = null;
      this.currentStepIndex = 0;
      this.lastAnnouncement = 0;
      this.minInterval = 2500;
    }

    getState() {
      return this.state;
    }

    getCurrentStep() {
      if (!this.currentRoute) return null;
      return this.currentRoute[this.currentStepIndex] || null;
    }

    now() {
      return Date.now();
    }

    start(route) {
      if (!Array.isArray(route) || route.length === 0) {
        return this._dispatchError("路线为空");
      }

      this.currentRoute = route;
      this.currentStepIndex = 0;
      this.state = "NAVIGATING";

      if (window.taskChain) {
        window.taskChain.enqueue({
          type: "NAV_START",
          priority: "HIGH",
          payload: {
            route: this.currentRoute,
            eta: Math.ceil(route.length * 0.5)
          }
        });
      }

      if (window.MiniMap) {
        window.MiniMap.setRouteLength(route.length || 0);
      }

      logger.info("NavigationFSM", "导航开始", {});
    }

    finish() {
      this.state = "ARRIVED";

      if (window.taskChain) {
        window.taskChain.enqueue({
          type: "NAV_END",
          priority: "HIGH",
          payload: {}
        });
      }

      logger.info("NavigationFSM", "已到达终点", {});
    }

    onVisionUpdate(data) {
      if (this.state !== "NAVIGATING") return;
      const { direction, distance } = data || {};
      if (!direction) return;

      // 节流
      if (this.now() - this.lastAnnouncement < this.minInterval) return;
      this.lastAnnouncement = this.now();

      if (direction === "left" || direction === "right") {
        this._dispatchTurn(direction, distance);
      } else if (direction === "straight") {
        this._dispatchStraight(distance);
      }

      if (window.MiniMap) {
        const dir = direction === "straight" ? "front" : direction;
        window.MiniMap.addHazard(dir);
      }

      logger.info("NavigationFSM", "收到视觉更新", data);
    }

    nextStep() {
      if (!this.currentRoute) return;
      if (this.currentStepIndex < this.currentRoute.length - 1) {
        this.currentStepIndex++;
      } else {
        this.finish();
      }

      if (window.MiniMap) {
        window.MiniMap.setStepIndex(this.currentStepIndex);
      }
    }

    _dispatchTurn(direction, distance) {
      if (window.taskChain) {
        window.taskChain.enqueue({
          type: "NAV_TURN",
          priority: "HIGH",
          payload: { direction, distance }
        });
      }
      logger.info("NavigationFSM", "触发转弯", { direction, distance });
    }

    _dispatchStraight(distance) {
      if (window.taskChain) {
        window.taskChain.enqueue({
          type: "NAV_STRAIGHT",
          priority: "MEDIUM",
          payload: { distance }
        });
      }
      logger.info("NavigationFSM", "直行", { distance });
    }

    _dispatchPOI(name) {
      if (window.taskChain) {
        window.taskChain.enqueue({
          type: "NAV_POI",
          priority: "LOW",
          payload: { name }
        });
      }
      logger.info("NavigationFSM", "进入关键节点", { name });
    }

    _dispatchError(reason) {
      if (window.taskChain) {
        window.taskChain.enqueue({
          type: "NAV_ERROR",
          priority: "HIGH",
          payload: { reason }
        });
      }
      logger.error("NavigationFSM", "错误", { reason });
    }
  }

  window.NavigationFSM = new NavigationFSMClass();
  logger.info("NavigationFSM", "已加载", {});

})();
