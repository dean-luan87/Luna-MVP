// frontend/navigation_executors.js
// 把 NAV_* 任务转成语音行为

(function () {
  "use strict";

  if (window.NavigationExecutors) return;

  const TTS = window.speakText || (txt => Promise.resolve(console.log("[TTS]", txt)));
  const NavLog = window.NavLog || window.TaskLogger || {
    info: console.log,
    warn: console.warn,
    error: console.error,
  };

  async function execStart(payload) {
    const { eta } = payload || {};
    const text = eta ? `路线规划完成，预计需要 ${eta} 分钟。` : "路线规划完成，开始导航。";
    NavLog.info("Executor", "开始执行 NAV_START", payload);
    await TTS(text);
    NavLog.info("Executor", "NAV_START 执行完成", {});
  }

  async function execTurn(payload) {
    const { direction, distance } = payload || {};
    let text;
    if (direction === "left") {
      text = distance ? `前方 ${distance} 米左转` : "请在前方左转";
    } else if (direction === "right") {
      text = distance ? `前方 ${distance} 米右转` : "请在前方右转";
    } else {
      text = "请按提示转弯";
    }

    NavLog.info("Executor", "开始执行 NAV_TURN", payload);
    await TTS(text);
    NavLog.info("Executor", "NAV_TURN 执行完成", {});
  }

  async function execStraight(payload) {
    const { distance } = payload || {};
    const text = distance ? `请直行 ${distance} 米` : "请继续直行";
    NavLog.info("Executor", "开始执行 NAV_STRAIGHT", payload);
    await TTS(text);
    NavLog.info("Executor", "NAV_STRAIGHT 执行完成", {});
  }

  async function execPOI(payload) {
    const { name } = payload || {};
    const text = name ? `您已到达 ${name}` : "您已到达关键位置";
    NavLog.info("Executor", "开始执行 NAV_POI", payload);
    await TTS(text);
    NavLog.info("Executor", "NAV_POI 执行完成", {});
  }

  async function execEnd() {
    const text = "已到达目的地。导航结束。";
    NavLog.info("Executor", "开始执行 NAV_END", {});
    await TTS(text);
    NavLog.info("Executor", "NAV_END 执行完成", {});
  }

  async function execError(payload) {
    const { reason } = payload || {};
    const text = reason ? `导航出错：${reason}` : "导航出错，请稍后重试。";
    NavLog.error("Executor", "开始执行 NAV_ERROR", payload);
    await TTS(text);
    NavLog.error("Executor", "NAV_ERROR 执行完成", {});
  }

  window.NavigationExecutors = {
    execStart,
    execTurn,
    execStraight,
    execPOI,
    execEnd,
    execError,
  };

  console.log("[NavigationExecutors] 已加载");
})();



