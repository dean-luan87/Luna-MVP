# -*- coding: utf-8 -*-
"""
Luna Reasoning Console M0（本地推理控制台）

启动：
  python3 tools/reasoning_console_server.py --jsonl logs/decision_monitor.jsonl

说明：
- 不做复杂前端：一个脚本 + 内置 HTML/JS
- API 由 tools/reasoning_console_api.py 提供
"""

from __future__ import annotations

import argparse
import html
import os
from http.server import HTTPServer

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.append(str(_ROOT))

from tools.reasoning_console_api import ReasoningConsoleAPIHandler  # noqa: E402


INDEX_HTML = r"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Luna Reasoning Console (M0.5)</title>
  <style>
    body { margin: 0; font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei"; }
    header { padding: 10px 12px; border-bottom: 1px solid #ddd; display:flex; gap:10px; align-items:center; flex-wrap:wrap; }
    #app { display:flex; height: calc(100vh - 56px); }
    #left { width: 380px; border-right: 1px solid #ddd; overflow:auto; }
    #right { flex:1; overflow:auto; padding: 10px 12px; }
    .row { padding: 8px 10px; border-bottom: 1px solid #f0f0f0; cursor:pointer; }
    .row:hover { background:#fafafa; }
    .row.active { background:#eef6ff; }
    .meta { color:#666; font-size: 12px; margin-top: 2px; }
    .pill { padding: 2px 8px; border: 1px solid #ccc; border-radius: 999px; font-size: 12px; }
    .tag { padding: 2px 8px; border-radius: 999px; font-size: 12px; color:#fff; }
    .tag.red { background:#cf222e; }
    .tag.blue { background:#0969da; }
    .tag.yellow { background:#b78103; }
    .filters { display:flex; gap:8px; align-items:center; flex-wrap:wrap; }
    button { padding: 6px 10px; border:1px solid #ccc; border-radius:6px; background:#fff; cursor:pointer; }
    button:hover { background:#f7f7f7; }
    pre { white-space: pre-wrap; word-break: break-word; background:#0b1020; color:#e6edf3; padding:10px; border-radius:8px; }
    h2 { margin: 8px 0 6px; font-size: 16px; }
    h3 { margin: 10px 0 6px; font-size: 13px; color:#333; }
    .grid { display:grid; grid-template-columns: repeat(3, 1fr); gap:6px; }
    .cell { border:1px solid #e6e6e6; border-radius:10px; padding:8px; background:#fff; min-height: 54px; }
    .cell.rec-bg { background:#fff1f1; border-color:#ffccd0; }
    .cell .name { font-weight:700; font-size:12px; }
    .cell .flags { margin-top:4px; font-size:12px; color:#666; }
    .flag { display:inline-block; padding:1px 6px; border-radius:999px; font-size:12px; margin-right:4px; border:1px solid #ddd; }
    .flag.focus { border-color:#0969da; color:#0969da; }
    .flag.container { border-color:#1f883d; color:#1f883d; }
    .flag.occlusion { border-color:#b78103; color:#b78103; }
    .flag.rec { border-color:#cf222e; color:#cf222e; }
    .tabs { display:flex; gap:8px; margin: 8px 0; flex-wrap:wrap; }
    .tabs button.active { border-color:#0969da; }
    .box { border:1px solid #e6e6e6; border-radius:12px; background:#fff; padding:10px 12px; margin: 10px 0; }
    .kv { display:grid; grid-template-columns: 220px 1fr; gap:6px 10px; font-size: 13px; }
    .kv .k { color:#444; }
    .kv .v { color:#111; }
    .overview { display:grid; grid-template-columns: repeat(4, minmax(220px, 1fr)); gap:10px; margin: 6px 0 10px; }
    .card { border:1px solid #e6e6e6; border-radius:12px; background:#fff; padding:10px 12px; }
    .card .t { font-size:12px; color:#666; }
    .card .v { margin-top:6px; font-size:14px; font-weight:800; color:#111; line-height:1.25; }
    .card .s { margin-top:6px; font-size:12px; color:#444; line-height:1.35; }
    .diag { border-left: 4px solid #0969da; }
    .diag.none { border-left-color:#1f883d; }
    details { border:1px solid #e6e6e6; border-radius:12px; background:#fff; padding:10px 12px; margin: 10px 0; }
    summary { cursor:pointer; font-weight:800; }
    /* Reasoning Structure Tree M0.5 (view only) */
    .tree { font-size: 13px; line-height: 1.35; }
    .tree .n { margin: 6px 0; }
    .tree .indent { margin-left: 14px; border-left: 2px solid #f0f0f0; padding-left: 10px; }
    .tree .nodeCard { border:1px solid #e6e6e6; border-radius:12px; background:#fff; padding:8px 10px; }
    .tree .nodeCard.active { border-color:#0969da; box-shadow: 0 0 0 2px rgba(9,105,218,0.10); }
    .tree .nodeCard.pruned { opacity: 0.62; }
    .tree .nodeCard.blocked { border-color:#cf222e; box-shadow: 0 0 0 2px rgba(207,34,46,0.10); }
    .tree .nodeCard.resolved { border-color:#1f883d; box-shadow: 0 0 0 2px rgba(31,136,61,0.10); }
    .tree .hdr { display:flex; gap:8px; align-items:center; flex-wrap:wrap; }
    .tree .hdr .tt { font-weight: 900; }
    .tree .sub { margin-top: 6px; color:#444; }
    .tree .mini { margin-left: auto; display:flex; gap:6px; flex-wrap:wrap; }
    .badge { display:inline-block; padding: 1px 8px; border-radius: 999px; border:1px solid #ddd; font-size: 12px; color:#333; background:#fff; }
    .badge.active { border-color:#0969da; color:#0969da; }
    .badge.pruned { border-color:#999; color:#666; }
    .badge.blocked { border-color:#cf222e; color:#cf222e; }
    .badge.resolved { border-color:#1f883d; color:#1f883d; }
    .badge.watchlist { border-color:#b78103; color:#b78103; }
    .badge.feedback { border-color:#8250df; color:#8250df; }
    .badge.type { border-color:#ddd; color:#111; background:#f6f8fa; }
  </style>
</head>
<body>
  <header>
    <div class="pill"><strong>Reasoning Console (M0.5)</strong></div>
    <div class="filters">
      <button id="btnAll">all</button>
      <button id="btnBlocked">blocked</button>
      <button id="btnIssue">issue</button>
      <button id="btnFeedback">with_feedback</button>
      <span class="pill" id="jsonlPath">jsonl: —</span>
    </div>
  </header>
  <div id="app">
    <div id="left"></div>
    <div id="right">
      <div class="box">
        <div class="kv">
          <div class="k">状态</div><div class="v" id="status">选择左侧快照</div>
        </div>
      </div>
    </div>
  </div>

<script>
const left = document.getElementById('left');
const right = document.getElementById('right');
const jsonlPath = document.getElementById('jsonlPath');
let currentView = 'all';
let activeId = null;

function esc(s){ return (s==null?'':String(s)).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;'); }
function tagHtml(s){
  if(!s) return '';
  return `<span class="tag yellow">${esc(s)}</span>`;
}
function boolTag(label, on, color){
  if(!on) return '';
  return `<span class="tag ${color}">${esc(label)}</span>`;
}

async function loadList(){
  const res = await fetch(`/api/reasoning/snapshots?view=${encodeURIComponent(currentView)}`);
  const data = await res.json();
  jsonlPath.textContent = `jsonl: ${data.jsonl_path || '—'}`;
  const items = data.items || [];
  left.innerHTML = items.map(it => {
    const id = it.id;
    const active = (id === activeId) ? 'active' : '';
    const blocked = boolTag('blocked', it.blocked, 'red');
    const issue = it.possible_issue_type ? `<span class="tag blue">${esc(it.possible_issue_type)}</span>` : '';
    const meta = `seq=${it.seq ?? '—'} ts=${it.ts ?? '—'} flow=${it.flow ?? '—'}`;
    const title = `${it.goal ?? '—'} · ${it.terminal_status ?? '—'}`;
    return `<div class="row ${active}" onclick="selectSnap('${esc(id)}')">
      <div><strong>${esc(title)}</strong></div>
      <div class="meta">${esc(meta)}</div>
      <div class="meta">${blocked} ${issue}</div>
      <div class="meta">${esc(it.integration_summary || '')}</div>
    </div>`;
  }).join('');
}

function gridCellLabel(cellId){
  const map = {
    'left_back':'左后', 'center_back':'中后', 'right_back':'右后',
    'left_mid':'左中', 'center_mid':'中间', 'right_mid':'右中',
    'left_front':'左前', 'center_front':'中前', 'right_front':'右前'
  };
  return map[cellId] || cellId || '—';
}

function renderGrid(snapshot){
  const focus = snapshot.focus_target_cell_id;
  const container = null; // M0.5：不做新推断，避免误导
  const rec = snapshot.recommended_search_cell_id;
  const cells = ['left_back','center_back','right_back','left_mid','center_mid','right_mid','left_front','center_front','right_front'];
  return `<div class="grid">` + cells.map(cid => {
    const isRec = (cid && rec && cid === rec);
    const flags = [];
    if(cid && focus && cid === focus) flags.push('<span class="flag focus">focus</span>');
    if(cid && container && cid === container) flags.push('<span class="flag container">container</span>');
    if(cid && rec && cid === rec) flags.push('<span class="flag rec">recommended</span>');
    return `<div class="cell ${isRec ? 'rec-bg' : ''}">
      <div class="name">${esc(gridCellLabel(cid))}</div>
      <div class="flags">${flags.join(' ') || '<span class="flag">—</span>'}</div>
    </div>`;
  }).join('') + `</div>`;
}

function firstLine(s){ if(!s) return '—'; const t=String(s); return t.length>120 ? (t.slice(0,120)+'...') : t; }
function wbSummaryLines(wb){
  if(!wb) return ['—'];
  const sum = wb.whitebox_summary ? `summary: ${firstLine(wb.whitebox_summary)}` : `applied: ${String(wb.whitebox_applied||false)}`;
  const steps = Array.isArray(wb.reasoning_steps) ? wb.reasoning_steps : [];
  const weights = Array.isArray(wb.weight_allocation) ? wb.weight_allocation : [];
  const excl = Array.isArray(wb.exclusion_log) ? wb.exclusion_log : [];
  const inter = Array.isArray(wb.interaction_trace) ? wb.interaction_trace : [];
  const topStep = steps[1]?.step_output_summary ? `key: ${firstLine(steps[1].step_output_summary)}` : (steps[0]?.step_output_summary ? `key: ${firstLine(steps[0].step_output_summary)}` : null);
  const topW = weights[0] ? `top_weight: ${firstLine(JSON.stringify(weights[0]))}` : null;
  const topEx = excl[0] ? `top_excl: ${firstLine(JSON.stringify(excl[0]))}` : null;
  const fb = inter[0] ? `feedback: ${firstLine(JSON.stringify(inter[0]))}` : null;
  return [sum, topStep, topW, topEx, fb].filter(Boolean);
}

function wbSummaryBlock(title, wb){
  const lines = wbSummaryLines(wb);
  return `<div class="card">
    <div class="t">${esc(title)}（摘要）</div>
    <div class="s"><pre style="margin:8px 0 0;">${esc(lines.join('\\n'))}</pre></div>
    <details style="margin-top:8px;"><summary>展开完整白盒</summary><pre>${esc(wbToText(wb))}</pre></details>
  </div>`;
}

function wbToText(wb){
  if(!wb) return '—';
  const steps = Array.isArray(wb.reasoning_steps) ? wb.reasoning_steps.map(s => `${s.step_index}. ${s.step_name} | in=${s.step_input_summary} | out=${s.step_output_summary}`).join('\\n') : '';
  const w = Array.isArray(wb.weight_allocation) ? wb.weight_allocation.slice(0,6).map(x => JSON.stringify(x)).join('\\n') : '';
  const ex = Array.isArray(wb.exclusion_log) ? wb.exclusion_log.slice(0,6).map(x => JSON.stringify(x)).join('\\n') : '';
  const it = Array.isArray(wb.interaction_trace) ? wb.interaction_trace.slice(0,3).map(x => JSON.stringify(x)).join('\\n') : '';
  const sum = wb.whitebox_summary || wb.whitebox_applied || '';
  return `summary=${sum}\\n\\n[reasoning_steps]\\n${steps||'—'}\\n\\n[weight_allocation]\\n${w||'—'}\\n\\n[exclusion_log]\\n${ex||'—'}\\n\\n[interaction_trace]\\n${it||'—'}`;
}

function bandFromScore(x){
  if(x==null || x==='') return null;
  const v = Number(x);
  if(Number.isNaN(v)) return null;
  if(v >= 0.80) return 'high';
  if(v >= 0.55) return 'mid';
  return 'low';
}

function nodeBadgeHtml(label, cls){
  if(!label) return '';
  return `<span class="badge ${esc(cls||'')}">${esc(label)}</span>`;
}

function nodeStatusClass(st){
  const s = (st||'').toLowerCase();
  if(s === 'blocked') return 'blocked';
  if(s === 'resolved') return 'resolved';
  if(s === 'pruned' || s === 'rejected') return 'pruned';
  if(s === 'watchlist') return 'watchlist';
  return '';
}

function nodeCardHtml(n, sets){
  const id = n.node_id || '';
  const st = (n.status || '—');
  const ty = (n.node_type || '—');
  const title = (n.node_title || '—');
  const summ = n.node_summary ? firstLine(n.node_summary) : '—';
  const src = n.source_module || '—';
  const conf = (n.confidence_score!=null) ? Number(n.confidence_score) : null;
  const band = n.confidence_band || bandFromScore(conf);
  const isActive = sets.active.has(id);
  const isPruned = sets.pruned.has(id) || (String(st).toLowerCase() === 'pruned') || (String(st).toLowerCase() === 'rejected');
  const isResolved = (String(st).toLowerCase() === 'resolved');
  const isBlocked = (String(st).toLowerCase() === 'blocked');
  const feedback = !!n.is_user_feedback_driven;
  const cls = ['nodeCard', isActive?'active':'', isPruned?'pruned':'', isResolved?'resolved':'', isBlocked?'blocked':''].filter(Boolean).join(' ');
  const mini = [
    nodeBadgeHtml(ty, 'type'),
    nodeBadgeHtml(st, nodeStatusClass(st)),
    isActive ? nodeBadgeHtml('active_path','active') : '',
    feedback ? nodeBadgeHtml('feedback','feedback') : '',
    (conf!=null) ? nodeBadgeHtml(`conf=${conf.toFixed(2)}${band?('·'+band):''}`, '') : (band ? nodeBadgeHtml(`conf·${band}`, '') : ''),
  ].filter(Boolean).join('');

  const detailLines = [
    n.exclusion_reason ? `exclusion_reason: ${n.exclusion_reason}` : null,
    n.next_effect ? `next_effect: ${n.next_effect}` : null,
    n.related_raw_text ? `related_raw_text: ${firstLine(n.related_raw_text)}` : null,
    `source_module: ${src}`,
    `node_id: ${id}`,
    n.parent_node_id ? `parent_node_id: ${n.parent_node_id}` : null,
  ].filter(Boolean);

  return `
    <div class="${cls}">
      <div class="hdr">
        <div class="tt">${esc(title)}</div>
        <div class="mini">${mini}</div>
      </div>
      <div class="sub">${esc(summ)}</div>
      <details style="margin-top:8px;">
        <summary>展开细节</summary>
        <pre>${esc(detailLines.join('\\n') || '—')}</pre>
      </details>
    </div>
  `;
}

function buildTreeIndex(t){
  const nodes = Array.isArray(t?.nodes) ? t.nodes : [];
  const byId = new Map();
  const children = new Map();
  const roots = [];
  for(const n of nodes){
    const id = n?.node_id;
    if(!id) continue;
    byId.set(id, n);
  }
  for(const n of nodes){
    const id = n?.node_id;
    if(!id) continue;
    const pid = n?.parent_node_id;
    if(pid && byId.has(pid)){
      if(!children.has(pid)) children.set(pid, []);
      children.get(pid).push(id);
    }else{
      roots.push(id);
    }
  }
  // stable ordering: type, then title
  const sortIds = (ids) => (ids||[]).slice().sort((a,b)=>{
    const na = byId.get(a)||{}, nb = byId.get(b)||{};
    const ta = String(na.node_type||''), tb = String(nb.node_type||'');
    if(ta !== tb) return ta.localeCompare(tb);
    const sa = String(na.node_title||''), sb = String(nb.node_title||'');
    return sa.localeCompare(sb);
  });
  for(const [pid, ids] of children.entries()){
    children.set(pid, sortIds(ids));
  }
  return {nodes, byId, children, roots: sortIds(roots)};
}

function renderTreeView(t){
  const idx = buildTreeIndex(t);
  const byId = idx.byId;
  const children = idx.children;
  const roots = idx.roots;
  const active = new Set(Array.isArray(t?.active_path_node_ids) ? t.active_path_node_ids : []);
  const pruned = new Set(Array.isArray(t?.pruned_node_ids) ? t.pruned_node_ids : []);
  const resolvedId = t?.resolved_node_id || null;
  const sets = {active, pruned, resolvedId};

  const rootId = t?.root_node_id;
  const mainRoot = (rootId && byId.has(rootId)) ? rootId : (roots[0] || null);
  const orphans = roots.filter(x => x !== mainRoot);

  const shouldOpen = (id) => {
    if(!id) return false;
    if(id === mainRoot) return true;
    if(active.has(id)) return true;
    if(resolvedId && id === resolvedId) return true;
    // if any descendant in active path, keep open
    const st = [id];
    const seen = new Set();
    while(st.length){
      const cur = st.pop();
      if(seen.has(cur)) continue;
      seen.add(cur);
      const kids = children.get(cur) || [];
      for(const k of kids){
        if(active.has(k) || (resolvedId && k === resolvedId)) return true;
        st.push(k);
      }
    }
    return false;
  };

  const renderNode = (id) => {
    const n = byId.get(id);
    if(!n) return '';
    const kids = children.get(id) || [];
    const open = shouldOpen(id);
    const wrapStart = `<div class="n">`;
    const wrapEnd = `</div>`;
    const card = nodeCardHtml(n, sets);
    if(!kids.length) return `${wrapStart}${card}${wrapEnd}`;
    return `${wrapStart}
      <details ${open?'open':''} style="border:none; padding:0; margin:0;">
        <summary style="list-style:none; display:none;"></summary>
        ${card}
        <div class="indent">${kids.map(renderNode).join('')}</div>
      </details>
    ${wrapEnd}`;
  };

  if(!mainRoot) return `<div class="tree"><div class="meta">—</div></div>`;
  const metrics = `metrics: depth=${esc(t?.tree_depth ?? '—')} branch=${esc(t?.branch_count ?? '—')} dead=${esc(t?.dead_branch_count ?? '—')}`;
  const main = renderNode(mainRoot);
  const orphanHtml = orphans.length ? `
    <details style="margin-top:10px;">
      <summary>orphan / detached nodes（兜底）</summary>
      <div class="tree">${orphans.map(renderNode).join('')}</div>
    </details>
  ` : '';
  return `
    <div class="tree">
      <div class="meta">${metrics}</div>
      ${main}
      ${orphanHtml}
    </div>
  `;
}

function renderTabs(snapshot){
  const tabs = [
    ['grid_search','Search / Grid', snapshot.grid_search_whitebox_trace],
    ['recheck','Recheck', snapshot.recheck_whitebox_trace],
    ['action_hint','Action Hint', snapshot.action_hint_whitebox_trace],
    ['confirmation','Confirmation', snapshot.confirmation_whitebox_trace],
    ['evidence_hypothesis','Evidence / Hypothesis', snapshot.evidence_hypothesis_whitebox_trace],
    ['experience_governance','Experience Governance', snapshot.experience_governance_whitebox_trace],
  ];
  const btns = tabs.map(([k,label,wb]) => {
    const badge = wb ? `<span class="pill">${esc(snapshot.confirmation_input_raw_text ? 'feedback' : 'ok')}</span>` : `<span class="pill">—</span>`;
    return `<button onclick="selectTab('${k}')">${esc(label)} ${badge}</button>`;
  }).join('');
  return `<div class="tabs">${btns}</div>
    <div class="box">
      <h3 id="tabTitle">白盒详情（默认摘要，可展开）</h3>
      <div id="tabBody"></div>
    </div>`;
}

function fillTab(snapshot, key){
  const title = document.getElementById('tabTitle');
  const body = document.getElementById('tabBody');
  const map = {
    'grid_search': ['Search / Grid Whitebox', snapshot.grid_search_whitebox_trace],
    'recheck': ['Recheck Whitebox', snapshot.recheck_whitebox_trace],
    'action_hint': ['Action Hint Whitebox', snapshot.action_hint_whitebox_trace],
    'confirmation': ['Confirmation Whitebox', snapshot.confirmation_whitebox_trace],
    'evidence_hypothesis': ['Evidence / Hypothesis Whitebox', snapshot.evidence_hypothesis_whitebox_trace],
    'experience_governance': ['Experience Governance Whitebox', snapshot.experience_governance_whitebox_trace],
  };
  const x = map[key] || ['Whitebox', null];
  title.textContent = x[0];
  body.innerHTML = wbSummaryBlock(x[0], x[1]);
}

window.selectTab = (key) => {
  if(!window.__snapshot) return;
  fillTab(window.__snapshot, key);
};

window.selectSnap = async (id) => {
  activeId = id;
  await loadList();
  const res = await fetch(`/api/reasoning/snapshots/${encodeURIComponent(id)}`);
  const s = await res.json();
  window.__snapshot = s;
  const blocked = s.blocked ? `<span class="tag red">blocked</span>` : '';
  const issue = s.possible_issue_type ? `<span class="tag blue">${esc(s.possible_issue_type)}</span>` : `<span class="tag blue">none</span>`;
  const issueReason = s.possible_issue_reason || '暂无明显异常';
  const statusLine = `${esc(s.terminal_status||'—')} · can_resume=${esc(s.can_resume)} · blocked=${esc(s.blocked)}${s.blocked_reason ? (' · '+esc(s.blocked_reason)) : ''}`;
  right.innerHTML = `
    <div class="overview">
      <div class="card">
        <div class="t">当前目标</div>
        <div class="v">${esc(s.current_goal||'—')}</div>
        <div class="s">focus：${esc(s.focus_target_label||'—')} · flow：${esc(s.current_flow_type||'—')}</div>
      </div>
      <div class="card">
        <div class="t">当前主判断</div>
        <div class="v">${esc(s.suggested_search_zone||'—')}</div>
        <div class="s">next_effect：${esc(s.confirmation_bridge_next_effect||'—')}</div>
      </div>
      <div class="card diag ${s.possible_issue_type ? '' : 'none'}">
        <div class="t">当前最可能问题</div>
        <div class="v">${issue} ${blocked}</div>
        <div class="s">${esc(issueReason)} · debug=${esc(s.suggested_debug_module||'—')}</div>
      </div>
      <div class="card">
        <div class="t">当前状态</div>
        <div class="v">${esc(s.terminal_status||'—')}</div>
        <div class="s">${statusLine}</div>
      </div>
    </div>

    <div class="box">
      <h3>空间与搜索</h3>
      ${renderGrid(s)}
      <div class="meta">grid：${esc(s.grid_summary||'—')} · rec=${esc(s.recommended_search_cell_human_label||'—')}</div>
      <div class="kv" style="margin-top:8px;">
        <div class="k">L1/L2 表达</div><div class="v">L1=${esc(s.focus_target_expression||'—')} · L2=${esc(s.focus_target_actionable_expression||'—')}</div>
        <div class="k">主建议</div><div class="v">${esc(s.suggested_search_zone||'—')}</div>
        <div class="k">下一步</div><div class="v">${esc(s.next_search_step_summary||'—')}</div>
      </div>
    </div>

    <div class="box">
      <h3>当前行动建议</h3>
      <div class="kv">
        <div class="k">primary</div><div class="v">${esc(s.action_hint_primary||'—')}</div>
        <div class="k">followup</div><div class="v">${esc(s.action_hint_followup||'—')}</div>
        <div class="k">confirmation</div><div class="v">${esc(s.action_hint_confirmation||'—')}</div>
      </div>
    </div>

    <div class="box">
      <h3>当前反馈与推进</h3>
      <div class="kv">
        <div class="k">raw feedback</div><div class="v">${esc(s.confirmation_input_raw_text||'—')}</div>
        <div class="k">mapped type</div><div class="v">${esc(s.confirmation_input_type||'—')}</div>
        <div class="k">next_effect</div><div class="v">${esc(s.confirmation_bridge_next_effect||'—')}</div>
        <div class="k">recheck</div><div class="v">${esc(s.recheck_action||'—')} · blocked=${esc(s.recheck_blocked)}</div>
      </div>
    </div>

    <div class="box">
      <h3>用户可见解释（对话口径）</h3>
      <div class="kv">
        <div class="k">我为什么先这么判断</div><div class="v">${esc(s.user_visible_explanation_primary||'—')}</div>
        <div class="k">我为什么没有先选别的方向</div><div class="v">${esc(s.user_visible_excluded_alternative||'—')}</div>
        <div class="k">你刚才那句反馈改变了什么</div><div class="v">${esc(s.user_visible_feedback_impact||'—')}</div>
        <div class="k">我为什么没有把它理解成别的意思</div><div class="v">${esc(s.user_visible_explanation_confirmation||'—')}</div>
      </div>
    </div>

    <div class="box">
      <h3>白盒详情（默认摘要）</h3>
      <div class="meta">Search / Grid → Recheck → Action Hint → Confirmation</div>
      ${renderTabs(s)}
    </div>

    <div class="box">
      <h3>推理结构树 / Reasoning Structure Tree（M0.5）</h3>
      <div class="meta">仅展示升级：按 parent_node_id 渲染层级树；默认展开 root + active/resolved 路径；pruned 弱化但可见。</div>
      <div id="treeBox">loading...</div>
    </div>
  `;
  fillTab(s, 'grid_search');
  // render tree
  try{
    const t = s.reasoning_structure_tree;
    const tb = document.getElementById('treeBox');
    if(tb) tb.innerHTML = renderTreeView(t);
  }catch(e){
    const tb = document.getElementById('treeBox');
    if(tb) tb.textContent = '—';
  }
};

function setView(v){
  currentView = v;
  activeId = null;
  window.__snapshot = null;
  loadList();
}
document.getElementById('btnAll').onclick = () => setView('all');
document.getElementById('btnBlocked').onclick = () => setView('blocked');
document.getElementById('btnIssue').onclick = () => setView('issue');
document.getElementById('btnFeedback').onclick = () => setView('with_feedback');

loadList();
</script>
</body>
</html>"""


class _Handler(ReasoningConsoleAPIHandler):
    def do_GET(self):  # noqa: N802
        if self.path == "/" or self.path.startswith("/?"):
            body = INDEX_HTML.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        return super().do_GET()

    # quiet default logs (avoid spam)
    def log_message(self, fmt, *args):  # noqa: A003
        return


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jsonl", default=None, help="DecisionMonitor JSONL 路径（默认 logs/decision_monitor.jsonl 或 env）")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8777)
    args = ap.parse_args()

    if args.jsonl:
        os.environ["REASONING_CONSOLE_JSONL_PATH"] = args.jsonl

    httpd = HTTPServer((args.host, int(args.port)), _Handler)
    print(f"Reasoning Console M0.5: http://{html.escape(args.host)}:{int(args.port)}/")
    httpd.serve_forever()


if __name__ == "__main__":
    main()

