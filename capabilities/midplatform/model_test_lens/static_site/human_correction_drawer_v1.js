/**
 * Human Correction Layer V1 — bottom drawer correction list.
 */
(function (global) {
  "use strict";

  var Copy = function () { return global.HumanCorrectionCopy || {}; };
  var Store = function () { return global.HumanCorrectionStore; };

  var _filters = { all: true };

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function typeLabel(id) {
    var types = Copy().correctionTypes || [];
    for (var i = 0; i < types.length; i++) {
      if (types[i].id === id) return types[i].label;
    }
    return id;
  }

  function severityLabel(id) {
    var levels = Copy().severityLevels || [];
    for (var i = 0; i < levels.length; i++) {
      if (levels[i].id === id) return levels[i].label;
    }
    return id;
  }

  function recordTypes(r) {
    if (r.correction_types && r.correction_types.length) return r.correction_types;
    return r.correction_type ? [r.correction_type] : [];
  }

  function recordDomains(r) {
    if (r.problem_domains && r.problem_domains.length) return r.problem_domains;
    var domains = [];
    var typeMap = {};
    (Copy().correctionTypes || []).forEach(function (t) { typeMap[t.id] = t.group; });
    recordTypes(r).forEach(function (id) {
      var g = typeMap[id];
      if (g && domains.indexOf(g) < 0) domains.push(g);
    });
    return domains;
  }

  function matchesFilter(r, filterId) {
    if (filterId === "high") {
      return r.severity === "high" || r.severity === "blocker";
    }
    if (filterId === "model") {
      return recordDomains(r).indexOf("model") >= 0;
    }
    if (filterId === "environment") {
      return recordDomains(r).indexOf("environment") >= 0;
    }
    if (filterId === "other_custom") {
      return recordTypes(r).indexOf("other_custom") >= 0 || !!(r.manual_annotation && r.manual_annotation.trim());
    }
    return recordTypes(r).indexOf(filterId) >= 0;
  }

  function filterRecords(records) {
    if (_filters.all) return records;
    var active = Object.keys(_filters).filter(function (k) { return k !== "all" && _filters[k]; });
    if (!active.length) return records;
    return records.filter(function (r) {
      for (var i = 0; i < active.length; i++) {
        if (matchesFilter(r, active[i])) return true;
      }
      return false;
    });
  }

  function toggleFilter(filterId) {
    if (filterId === "all") {
      _filters = { all: true };
      return;
    }
    delete _filters.all;
    _filters[filterId] = !_filters[filterId];
    var hasAny = Object.keys(_filters).some(function (k) { return _filters[k]; });
    if (!hasAny) _filters = { all: true };
  }

  function isFilterActive(filterId) {
    if (filterId === "all") return !!_filters.all;
    return !!_filters[filterId];
  }

  function copyToClipboard(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text);
    }
    var ta = document.createElement("textarea");
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand("copy");
    document.body.removeChild(ta);
    return Promise.resolve();
  }

  function typeBadges(r) {
    return recordTypes(r).map(function (id) {
      return "<span class='hc-badge'>" + escapeHtml(typeLabel(id)) + "</span>";
    }).join("");
  }

  function render(panel, options) {
    options = options || {};
    var c = Copy();
    var records = filterRecords(Store().list());

    var filterTabs = (c.filterTabs || []).map(function (tab) {
      var active = isFilterActive(tab.id) ? " active" : "";
      return "<button type='button' class='hc-filter-tab" + active + "' data-filter='" +
        escapeHtml(tab.id) + "'>" + escapeHtml(tab.label) + "</button>";
    }).join("");

    var listHtml;
    if (!records.length) {
      listHtml = "<p class='hc-drawer-empty muted'>" + escapeHtml(c.drawerEmpty || "") + "</p>";
    } else {
      listHtml = "<ul class='hc-correction-list'>" + records.map(function (r, idx) {
        var target = r.correction_target || {};
        var note = r.manual_annotation || r.user_note || "";
        return (
          "<li class='hc-correction-item' data-id='" + escapeHtml(r.correction_id) + "'>" +
          "<div class='hc-correction-head'>" +
          "<span class='hc-correction-num'>#" + (records.length - idx) + "</span>" +
          "<strong>" + escapeHtml(target.target_display_name || target.target_id || "—") + "</strong>" +
          typeBadges(r) +
          "<span class='hc-badge hc-sev-" + escapeHtml(r.severity) + "'>" +
          escapeHtml(severityLabel(r.severity)) + "</span>" +
          "</div>" +
          "<p class='hc-correction-note'>" + escapeHtml(note) + "</p>" +
          "<div class='hc-correction-meta muted'>" + escapeHtml(c.statusPending || "待复核") + "</div>" +
          "<div class='hc-correction-actions'>" +
          "<button type='button' class='btn btn-ghost btn-sm hc-view-detail'>查看详情</button>" +
          "<button type='button' class='btn btn-ghost btn-sm hc-copy-one'>复制 JSON</button>" +
          "<button type='button' class='btn btn-ghost btn-sm' disabled title='第一版占位'>已复核</button>" +
          "<button type='button' class='btn btn-ghost btn-sm' disabled title='第一版占位'>生成复测候选</button>" +
          "</div>" +
          "<pre class='hc-detail-json' hidden></pre>" +
          "</li>"
        );
      }).join("") + "</ul>";
    }

    panel.innerHTML =
      "<div class='hc-drawer-inner'>" +
      "<p class='hc-boundary-notice'>" + escapeHtml(c.boundaryNotice || "") + "</p>" +
      "<p class='hc-boundary-notice muted'>" + escapeHtml(c.drawerFilterHint || "") + "</p>" +
      "<div class='hc-drawer-toolbar'>" +
      "<div class='hc-filter-tabs' role='tablist'>" + filterTabs + "</div>" +
      "<div class='hc-drawer-btns'>" +
      "<button type='button' class='btn btn-ghost btn-sm hc-export'>" + escapeHtml(c.buttons.exportJson) + "</button>" +
      "<button type='button' class='btn btn-ghost btn-sm hc-clear-local'>" + escapeHtml(c.buttons.clearLocal) + "</button>" +
      "</div></div>" + listHtml + "</div>";

    panel.querySelectorAll(".hc-filter-tab").forEach(function (btn) {
      btn.addEventListener("click", function () {
        toggleFilter(btn.dataset.filter);
        render(panel, options);
      });
    });

    panel.querySelector(".hc-export").addEventListener("click", function () {
      var blob = new Blob([Store().exportJSON()], { type: "application/json" });
      var a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = "luna_human_corrections_v1.json";
      a.click();
      URL.revokeObjectURL(a.href);
    });

    panel.querySelector(".hc-clear-local").addEventListener("click", function () {
      if (confirm("仅清空浏览器本地纠错草稿，不会删除 TestBoard 受保护记录。确认？")) {
        Store().clearLocalDrafts();
        render(panel, options);
      }
    });

    panel.querySelectorAll(".hc-view-detail").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var li = btn.closest(".hc-correction-item");
        var pre = li.querySelector(".hc-detail-json");
        var id = li.dataset.id;
        var rec = Store().list().find(function (r) { return r.correction_id === id; });
        if (pre && rec) {
          pre.hidden = !pre.hidden;
          pre.textContent = JSON.stringify(rec, null, 2);
        }
      });
    });

    panel.querySelectorAll(".hc-copy-one").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var li = btn.closest(".hc-correction-item");
        var id = li.dataset.id;
        var rec = Store().list().find(function (r) { return r.correction_id === id; });
        if (rec) copyToClipboard(JSON.stringify(rec, null, 2));
      });
    });
  }

  global.HumanCorrectionDrawer = {
    version: "human_correction_drawer_v1",
    render: render,
    setFilter: function (f) { _filters = { all: false }; _filters[f] = true; },
    resetFilters: function () { _filters = { all: true }; }
  };
})(typeof window !== "undefined" ? window : this);
