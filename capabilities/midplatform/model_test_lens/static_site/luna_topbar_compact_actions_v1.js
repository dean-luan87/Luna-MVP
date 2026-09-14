/**
 * Luna Topbar Compact Actions V1 — single-line toolbar with "更多" menu.
 */
(function (global) {
  "use strict";

  var Copy = function () { return global.LunaObservationCopy || {}; };

  function hide(el) {
    if (el) el.hidden = true;
  }

  function init(callbacks) {
    callbacks = callbacks || {};
    var actions = document.getElementById("lol-top-actions");
    if (!actions) return null;

    var jsonBtn = actions.querySelector(".lol-json-btn");
    var advBtn = document.getElementById("lol-advanced-btn");
    var devBtn = document.getElementById("lol-developer-btn");
    hide(jsonBtn);
    hide(advBtn);
    hide(devBtn);

    var existing = document.getElementById("lol-more-menu");
    if (existing) existing.remove();

    var menu = document.createElement("div");
    menu.id = "lol-more-menu";
    menu.className = "lol-more-menu";
    menu.innerHTML =
      "<button type='button' class='btn btn-ghost' id='lol-more-btn' aria-haspopup='true' aria-expanded='false'>更多</button>" +
      "<div class='lol-more-dropdown' id='lol-more-dropdown' hidden role='menu'>" +
      "<button type='button' class='lol-more-item' data-action='import' role='menuitem'>" +
      escapeHtml(Copy().importJson || "导入结果") + "</button>" +
      "<button type='button' class='lol-more-item' data-action='advanced' role='menuitem'>" +
      escapeHtml(Copy().advanced || "高级流程") + "</button>" +
      "<button type='button' class='lol-more-item' data-action='developer' role='menuitem'>" +
      escapeHtml(Copy().developer || "开发者") + "</button>" +
      "<button type='button' class='lol-more-item' data-action='testboard' role='menuitem'>测试记录</button>" +
      "<button type='button' class='lol-more-item' data-action='whitebox' role='menuitem'>白盒链路</button>" +
      "</div>";
    actions.appendChild(menu);

    var moreBtn = menu.querySelector("#lol-more-btn");
    var dropdown = menu.querySelector("#lol-more-dropdown");
    var jsonInput = document.getElementById("lol-json-input");

    function closeMenu() {
      dropdown.hidden = true;
      moreBtn.setAttribute("aria-expanded", "false");
    }

    moreBtn.addEventListener("click", function (ev) {
      ev.stopPropagation();
      var open = dropdown.hidden;
      dropdown.hidden = !open;
      moreBtn.setAttribute("aria-expanded", open ? "true" : "false");
    });

    document.addEventListener("click", closeMenu);

    menu.querySelectorAll(".lol-more-item").forEach(function (item) {
      item.addEventListener("click", function (ev) {
        ev.stopPropagation();
        closeMenu();
        var action = item.dataset.action;
        if (action === "import" && jsonInput) jsonInput.click();
        else if (action === "advanced" && callbacks.onAdvanced) callbacks.onAdvanced();
        else if (action === "developer" && callbacks.onDeveloper) callbacks.onDeveloper();
        else if (action === "testboard" && callbacks.onTestBoard) callbacks.onTestBoard();
        else if (action === "whitebox" && callbacks.onWhitebox) callbacks.onWhitebox();
      });
    });

    return { closeMenu: closeMenu };
  }

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  global.LunaTopbarCompactActions = {
    version: "luna_topbar_compact_actions_v1",
    init: init
  };
})(typeof window !== "undefined" ? window : this);
