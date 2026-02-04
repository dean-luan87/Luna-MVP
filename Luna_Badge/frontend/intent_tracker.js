// frontend/intent_tracker.js
// "cancel" | "resume" | "insert" | "replace" | "continue"

(function () {
  "use strict";

  if (window.IntentTracker) return;

  const logger = window.TaskLogger || {
    info: console.log,
    warn: console.warn,
    error: console.error,
  };

  class IntentTracker {
    constructor() {
      this.lastUtterance = null;
    }

    updateIntent(text) {
      this.lastUtterance = text;
      logger.info("Intent", "收到用户语句", { text });

      if (/(停|不要了|算了|取消|先这样)/.test(text)) {
        return "cancel";
      }
      if (/(继续|接着|刚才|恢复导航)/.test(text)) {
        return "resume";
      }
      if (/(顺便|先去|顺路|路过)/.test(text)) {
        return "insert";
      }
      if (/(我要去|带我去|导航到|帮我去)/.test(text)) {
        return "replace";
      }
      return "continue";
    }
  }

  window.IntentTracker = new IntentTracker();
})();
