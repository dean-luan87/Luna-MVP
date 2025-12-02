// frontend/ui/TestPanel.js
// 新版测试界面

(function () {
  "use strict";
  if (window.TestPanel) return;

  class TestPanelClass {
    constructor(rootId = "luna_test_panel") {
      this.root = null;
      this.rootId = rootId;
      this.data = {};
      this._init();
    }

    _init() {
      this.root = document.getElementById(this.rootId);
      if (!this.root) {
        this.root = document.createElement("div");
        this.root.id = this.rootId;
        document.body.appendChild(this.root);
      }

      this.root.style.cssText = `
        position: fixed;
        right: 0;
        top: 0;
        width: 360px;
        height: 100vh;
        overflow-y: auto;
        background: rgba(0,0,0,0.85);
        color: #00ffa2;
        font-size: 13px;
        padding: 10px;
        z-index: 99999;
        font-family: 'Monaco', 'Menlo', 'Courier New', monospace;
        box-shadow: -2px 0 10px rgba(0,0,0,0.5);
      `;

      this.update({ message: "TestPanel initialized" });
    }

    update(data) {
      if (!this.root) return;

      // 合并数据
      this.data = { ...this.data, ...data };

      // 格式化显示
      const html = `
        <div style="border-bottom: 1px solid #00ffa2; padding-bottom: 8px; margin-bottom: 8px;">
          <h2 style="margin: 0; color: #00ffa2;">Luna Test Panel</h2>
          <div style="font-size: 11px; color: #888; margin-top: 4px;">
            ${new Date().toLocaleTimeString()}
          </div>
        </div>
        <pre style="margin: 0; white-space: pre-wrap; word-wrap: break-word; font-size: 11px;">${JSON.stringify(
          this.data,
          null,
          2
        )}</pre>
      `;

      this.root.innerHTML = html;
    }

    // 追加数据（不覆盖）
    append(key, value) {
      this.data[key] = value;
      this.update({});
    }

    // 清除数据
    clear() {
      this.data = {};
      this.update({ message: "Panel cleared" });
    }
  }

  window.TestPanel = TestPanelClass;
  console.log("[TestPanel] 新版测试界面已加载");
})();

