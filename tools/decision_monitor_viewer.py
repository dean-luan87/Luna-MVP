#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Decision Monitor JSONL Viewer（最小版）

目标：
- 左侧：帧列表（seq / ts / decision_owner / action_summary）
- 右侧：单帧 6 层责任链展开（goal/inputs/state/decision/outputs/consequence）
- 顶部：拍板者、目标、动作摘要
- 支持过滤：decision_owner / goal_type / action_summary（子串匹配）

不做复杂前端：一个 python 脚本 + 内置 HTML/JS，本地启动即可用。

用法：
  python3 tools/decision_monitor_viewer.py --jsonl logs/decision_monitor.jsonl
  python3 tools/decision_monitor_viewer.py --jsonl logs/decision_monitor.jsonl --host 127.0.0.1 --port 8765
"""

from __future__ import annotations

import argparse
import html
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse


INDEX_HTML = r"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Decision Monitor Viewer (M0)</title>
  <style>
    body { margin: 0; font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei"; }
    header { padding: 10px 12px; border-bottom: 1px solid #ddd; display:flex; gap:10px; align-items:center; flex-wrap:wrap; }
    header .pill { padding: 2px 8px; border: 1px solid #ccc; border-radius: 999px; font-size: 12px; }
    #app { display:flex; height: calc(100vh - 56px); }
    #left { width: 360px; border-right: 1px solid #ddd; overflow:auto; }
    #right { flex:1; overflow:auto; padding: 10px 12px; }
    .row { padding: 8px 10px; border-bottom: 1px solid #f0f0f0; cursor:pointer; }
    .row:hover { background:#fafafa; }
    .row.active { background:#eef6ff; }
    .meta { color:#666; font-size: 12px; margin-top: 2px; }
    .titleLine { display:flex; gap:8px; align-items:center; flex-wrap:wrap; }
    .badge { padding: 2px 8px; border-radius: 999px; font-size: 12px; border:1px solid #ccc; background:#fff; }
    .badge.owner { border-color:#99b; }
    .badge.action { border-color:#9b9; }
    .badge.goal { border-color:#bb9; }
    .tag { padding: 2px 8px; border-radius: 999px; font-size: 12px; color:#fff; }
    .tag.green { background:#1f883d; }
    .tag.yellow { background:#b78103; }
    .tag.red { background:#cf222e; }
    .tag.blue { background:#0969da; }
    .filters { display:flex; gap:8px; align-items:center; flex-wrap:wrap; }
    input { padding: 6px 8px; border:1px solid #ccc; border-radius:6px; }
    button { padding: 6px 10px; border:1px solid #ccc; border-radius:6px; background:#fff; cursor:pointer; }
    button:hover { background:#f7f7f7; }
    .toggle { display:flex; align-items:center; gap:6px; font-size:12px; color:#444; user-select:none; }
    .toggle input { transform: translateY(1px); }
    pre { white-space: pre-wrap; word-break: break-word; background:#0b1020; color:#e6edf3; padding:10px; border-radius:8px; }
    h2 { margin: 8px 0 6px; font-size: 16px; }
    .kv { display:grid; grid-template-columns: 220px 1fr; gap:6px 10px; font-size: 13px; }
    .kv div.k { color:#444; }
    .kv div.v { color:#111; }
    .cards { display:grid; grid-template-columns: repeat(3, minmax(240px, 1fr)); gap:10px; margin: 6px 0 10px; }
    .card { border:1px solid #e6e6e6; border-radius:10px; padding:10px 12px; background:#fff; }
    .card h3 { margin:0 0 6px; font-size: 13px; color:#333; }
    .big { font-size: 15px; font-weight: 600; }
    .small { font-size: 12px; color:#666; margin-top: 4px; }
    details { border:1px solid #e6e6e6; border-radius:10px; padding: 8px 10px; margin: 8px 0; background:#fff; }
    summary { cursor:pointer; font-weight:600; }
    .storyline { margin: 10px 0 10px; padding: 12px 12px; border:1px solid #e6e6e6; border-radius:12px; background:#fff; }
    .storyline .headline { font-size: 18px; font-weight: 800; line-height: 1.25; }
    .storyline .sub { margin-top:6px; font-size: 12px; color:#666; }
    .continuity { margin: 6px 0 8px; padding: 8px 10px; background:#f8f9fa; border-radius:8px; font-size: 13px; }
    .continuity .k { font-weight:600; color:#333; margin-bottom:4px; }
    .continuity .v { color:#444; line-height:1.4; }
    .view-guard-alert { margin: 8px 0; padding: 10px 12px; background:#fff3cd; border: 1px solid #ffc107; border-radius:8px; font-size: 13px; color:#856404; }
    .domain-alert { background:#f8d7da; border-color:#dc3545; color:#721c24; }
    .view-guard .view-alert { color:#cf222e; font-weight:600; }
  </style>
</head>
<body>
  <header>
    <strong>Decision Monitor Viewer (M0.5)</strong>
    <span id="status" class="pill">loading…</span>
    <div class="filters">
      <input id="f_owner" placeholder="filter decision_owner (e.g. sampling_gate)" size="32"/>
      <input id="f_goal" placeholder="filter goal_type (e.g. observe_navigate)" size="30"/>
      <input id="f_action" placeholder="filter action_summary (e.g. sample)" size="26"/>
      <label class="toggle"><input id="mode_toggle" type="checkbox" /> 专家模式</label>
      <button id="btn_reload">Reload</button>
    </div>
  </header>
  <div id="app">
    <div id="left"></div>
    <div id="right">
      <div class="meta">从左侧选择一帧查看详情。</div>
    </div>
  </div>

<script>
let frames = [];
let activeIndex = -1;
let expertMode = false;

function qs() {
  const owner = document.getElementById('f_owner').value.trim();
  const goal = document.getElementById('f_goal').value.trim();
  const action = document.getElementById('f_action').value.trim();
  const params = new URLSearchParams();
  if (owner) params.set('owner', owner);
  if (goal) params.set('goal', goal);
  if (action) params.set('action', action);
  return params.toString();
}

function safe(v) {
  if (v === null || v === undefined) return '';
  return String(v);
}

function humanOwner(owner) {
  const o = safe(owner);
  const m = {
    'controller': '系统主控',
    'sampling_gate': '采样控制',
    'module_gate': '模块执行控制',
    'floor_guard': '安全底线保护',
    'b2_impact': '谨慎提醒（B2）',
  };
  return m[o] || (o ? o : '未知');
}

function humanAction(action) {
  const a = safe(action);
  const m = {
    'sample_and_run': '继续观察并执行',
    'skip': '跳过本轮采样',
    'floor_forced': '强制采样确认',
    'run_detector': '运行检测器',
    'run_ocr': '运行文字识别',
  };
  if (m[a]) return m[a];
  if (a.includes('skip')) return '跳过本轮采样';
  if (a.includes('run_detector') && a.includes('run_ocr')) return '继续观察并执行（检测 + OCR）';
  if (a.includes('run_detector')) return '继续观察并执行（检测）';
  if (a.includes('run_ocr')) return '继续观察并执行（OCR）';
  return a || '未定义动作';
}

function humanSafety(safety, risk) {
  const s = safe(safety).toUpperCase();
  const r = Number(risk);
  if (s === 'SAFE') return '安全';
  if (s === 'CAUTION') return '需要谨慎';
  if (s === 'DANGER') return '危险';
  if (Number.isFinite(r)) {
    if (r >= 0.7) return '危险';
    if (r >= 0.4) return '需要谨慎';
    return '安全';
  }
  return s ? s : '未知';
}

function fmtTime(ts) {
  const n = Number(ts);
  if (!Number.isFinite(n) || n <= 0) return 'N/A';
  const d = new Date(n * 1000);
  const hh = String(d.getHours()).padStart(2,'0');
  const mm = String(d.getMinutes()).padStart(2,'0');
  const ss = String(d.getSeconds()).padStart(2,'0');
  return `${hh}:${mm}:${ss}`;
}

function statusTag(f) {
  const owner = safe(f?.decision?.decision_owner);
  const forced = !!(f?.decision?.floor_forced || f?.decision?.escape_hatch_triggered);
  const safety = safe(f?.state?.safety_level).toUpperCase();
  const risk = Number(f?.state?.risk_score);
  const sampled = f?.inputs?.sampled;
  const b2Applied = !!(f?.decision?.b2_impact_applied || f?.inputs?.active_b2_impact);
  const action = safe(f?.outputs?.action_summary || f?.decision?.decision_type);
  const modeAfter = safe(f?.decision?.policy_mode_after || f?.outputs?.policy_intent_summary).toUpperCase();

  // 叙事优先级：守底 > 节流 > B2 上调 > 风险态 > 正常
  if (forced || owner === 'floor_guard') {
    return {text:'守底触发：强制执行', cls:'red'};
  }
  if (owner === 'sampling_gate' || action.includes('skip') || sampled === false) {
    return {text:'节流：本轮跳过采样', cls:'blue'};
  }
  if (b2Applied) {
    return {text:'B2 介入：调度上调', cls:'yellow'};
  }
  if (safety === 'DANGER' || (Number.isFinite(risk) && risk >= 0.7)) {
    return {text:'风险态：高风险', cls:'red'};
  }
  if (safety === 'CAUTION' || (Number.isFinite(risk) && risk >= 0.4)) {
    return {text:'风险态：谨慎', cls:'yellow'};
  }
  if (modeAfter === 'FULL') {
    return {text:'推进：高频观察', cls:'green'};
  }
  if (modeAfter === 'CONSERVE') {
    return {text:'推进：省算观察', cls:'green'};
  }
  return {text:'推进：正常', cls:'green'};
}

function trendLabel(trend) {
  const t = safe(trend);
  if (t === 'stable') return '稳定';
  if (t === 'improving') return '好转';
  if (t === 'worsening') return '转入谨慎';
  if (t === 'shifting') return '切换中';
  if (t === 'recovering') return '恢复正常';
  return t || '—';
}

function buildStoryline(f) {
  const goal = safe(f?.goal?.goal_description || f?.goal?.goal_type);
  const actionRaw = safe(f?.outputs?.action_summary || f?.decision?.decision_type);
  const action = humanAction(actionRaw);
  const safety = humanSafety(f?.state?.safety_level, f?.state?.risk_score);
  const tag = statusTag(f).text;
  const gain = safe(f?.consequence?.expected_gain);
  const cost = safe(f?.consequence?.expected_cost);
  const why = safe(f?.decision?.decision_reason);
  const deltaSummary = safe(f?.state?.state_delta_summary);
  const prevSummary = safe(f?.state?.prev_state_summary);
  const viewCorrectionNeeded = f?.state?.view_correction_needed === true;
  const visionDegraded = f?.state?.vision_degraded === true;
  const holdActive = f?.state?.predictive_hold_active === true;
  const holdExpired = f?.state?.predictive_hold_expired === true;
  const holdRemaining = f?.state?.predictive_hold_remaining_ms;
  const recoveryAction = safe(f?.state?.predictive_recovery_action);
  const domainMismatch = f?.state?.domain_mismatch_detected === true;
  const domainState = safe(f?.state?.runtime_domain_state);
  const degradeAction = safe(f?.state?.degrade_action);
  const sceneSupported = f?.state?.scene_supported === true;
  const sceneGateState = safe(f?.state?.scene_gate_state);
  const sceneGateAction = safe(f?.state?.scene_gate_action);

  // 关键状态（人话）；Scene Gate 挂起最优先，再运行域失配，再短时容错
  let keyState = safety;
  if (!sceneSupported && sceneGateState === 'suspended') keyState = '当前场景不在支持域内，已挂起高层理解';
  else if (domainState === 'frozen') keyState = '当前场景超出正常理解范围，已进入认知冻结';
  else if (domainState === 'degraded' || domainMismatch) keyState = '当前场景部分超出正常理解范围，认知降级';
  else if (holdActive) keyState = '当前画面短时退化，但最近状态稳定';
  else if (holdExpired) keyState = '短时容错已到期，需重新确认环境';
  else if (viewCorrectionNeeded && visionDegraded) keyState = '镜头偏航且视觉质量下降';
  else if (viewCorrectionNeeded) keyState = '镜头偏航，需纠正观察方向';
  else if (visionDegraded) keyState = '当前视觉可信度下降';
  else if (tag.includes('节流')) keyState = '当前需要节流';
  else if (tag.includes('守底')) keyState = '已经接近安全底线';
  else if (tag.includes('B2 介入')) keyState = '存在弱证据变化';
  else if (deltaSummary && deltaSummary !== '—' && deltaSummary !== '与上一时刻相比，变化不大') {
    keyState = '相较上一时刻' + deltaSummary;
  } else if (deltaSummary === '与上一时刻相比，变化不大') {
    keyState = '当前风险没有明显变化';
  }

  // 目标/后果（人话）；hold 激活时强调“暂时维持并准备重确认”
  let effect = gain || (goal ? `维持${goal}` : '维持目标推进');
  if (holdActive && holdRemaining != null && holdRemaining > 0) {
    effect = `暂时维持当前判断，并在 ${Math.round(holdRemaining)}ms 内${recoveryAction ? recoveryAction.replace(/_/g, ' ') : '重新确认环境'}`;
  } else if (holdExpired) {
    effect = recoveryAction ? (recoveryAction.replace(/_/g, ' ') + '（已触发）') : '重新确认环境';
  }

  // 解释句模板
  const sentence = `因为${keyState}，所以系统决定「${action}」，以达到「${effect}」。`;
  const sub = [];
  if (prevSummary && prevSummary !== '首帧，无上一时刻') sub.push(`上一时刻：${prevSummary}`);
  if (!sceneSupported && sceneGateState === 'suspended') sub.push('场景：非支持域，' + (sceneGateAction ? sceneGateAction.replace(/_/g, ' ') : '挂起'));
  if (domainMismatch) sub.push('运行域：' + domainState + (degradeAction ? '，降级动作：' + degradeAction : ''));
  if (holdActive) sub.push('短时容错：开启，剩余 ' + (holdRemaining != null ? Math.round(holdRemaining) + 'ms' : '—') + (recoveryAction ? '，恢复：' + recoveryAction : ''));
  if (f?.state?.view_correction_needed) sub.push('视线：需纠正镜头');
  if (f?.state?.vision_degraded) sub.push('视觉：' + (safe(f?.state?.vision_degrade_reason) || '退化') + (f?.state?.vision_recovery_eta_ms > 0 ? `，约${Math.round(f.state.vision_recovery_eta_ms)}ms可恢复` : ''));
  if (goal) sub.push(`目标：${goal}`);
  if (cost) sub.push(`代价：${cost}`);
  if (why) sub.push(`原因：${why}`);
  return {sentence, sub: sub.join(' · ')};
}

function renderList() {
  const left = document.getElementById('left');
  left.innerHTML = '';
  frames.forEach((f, idx) => {
    const row = document.createElement('div');
    row.className = 'row' + (idx === activeIndex ? ' active' : '');
    const owner = safe(f?.decision?.decision_owner);
    const seq = safe(f?.inputs?.frame_seq);
    const ts = safe(f?.inputs?.current_ts);
    const action = safe(f?.outputs?.action_summary || f?.decision?.decision_type);
    const goal = safe(f?.goal?.goal_description || f?.goal?.goal_type);
    const tag = statusTag(f);
    row.innerHTML = `
      <div class="titleLine">
        <strong>${fmtTime(ts)}</strong>
        <span class="badge goal">${htmlEscape(goal || '目标N/A')}</span>
      </div>
      <div class="titleLine" style="margin-top:6px;">
        <span class="badge action">${htmlEscape(humanAction(action) || '动作N/A')}</span>
        <span class="badge owner">${htmlEscape(humanOwner(owner))}</span>
        <span class="tag ${tag.cls}">${tag.text}</span>
      </div>
      <div class="meta">#${seq}  ts=${ts}</div>
    `;
    row.onclick = () => { activeIndex = idx; renderList(); renderDetail(); };
    left.appendChild(row);
  });
  document.getElementById('status').textContent = `frames=${frames.length}`;
}

function htmlEscape(s) {
  return safe(s)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function kvTable(obj, keys) {
  const div = document.createElement('div');
  div.className = 'kv';
  keys.forEach(k => {
    const kk = document.createElement('div'); kk.className='k'; kk.textContent = k;
    const vv = document.createElement('div'); vv.className='v'; vv.textContent = safe(obj?.[k]);
    div.appendChild(kk); div.appendChild(vv);
  });
  return div;
}

function renderDetail() {
  const right = document.getElementById('right');
  if (activeIndex < 0 || activeIndex >= frames.length) {
    right.innerHTML = '<div class="meta">从左侧选择一帧查看详情。</div>';
    return;
  }
  const f = frames[activeIndex];
  const owner = safe(f?.decision?.decision_owner);
  const goalTitle = safe(f?.goal?.goal_description || f?.goal?.goal_type);
  const subgoal = safe(f?.goal?.subgoal_description);
  const action = safe(f?.outputs?.action_summary || f?.decision?.decision_type);
  const safety = safe(f?.state?.safety_level);
  const risk = f?.state?.risk_score;
  const tag = statusTag(f);
  right.innerHTML = '';
  // Scene Gate 轻量控制 + 人工沟通校准：提前读取，供顶部横幅与卡片使用
  const sceneGateAction = safe(f?.state?.scene_gate_action);
  const sceneGateControlApplied = f?.state?.scene_gate_control_applied === true;
  const humanCheckPending = f?.state?.human_check_pending === true;
  const humanCheckResolved = f?.state?.human_check_resolved === true;
  const humanCheckNeeded = f?.state?.human_check_needed === true;
  const humanCheckTimeoutTriggered = f?.state?.human_check_timeout_triggered === true;
  // 顶部一句话：人工确认优先于 Scene Gate 文案
  let topBannerText = '';
  if (humanCheckPending) {
    topBannerText = '系统正在等待人工确认，已暂缓高代价动作。';
  } else if (humanCheckTimeoutTriggered) {
    topBannerText = '用户未在规定时间内确认，系统已按默认策略处理。';
  } else if (humanCheckResolved && humanCheckNeeded) {
    topBannerText = '已根据人工确认调整策略。';
  } else if (sceneGateControlApplied && sceneGateAction === 'freeze_to_minimum_mode') {
    topBannerText = '当前场景不在支持域内，系统已冻结到最低运行模式。';
  } else if (sceneGateControlApplied && sceneGateAction === 'pause_goal_progress') {
    topBannerText = '当前场景不适合继续推进目标，系统已暂停目标推进并保持观察。';
  } else if (sceneGateControlApplied && (sceneGateAction === 'continue_normal' || sceneGateAction === 'continue_cautious')) {
    topBannerText = '当前场景正常，系统继续推进目标。';
  }
  if (topBannerText) {
    const bannerDiv = document.createElement('div');
    bannerDiv.className = 'storyline scene-gate-banner' + (humanCheckPending ? ' human-check-pending' : '');
    bannerDiv.style.marginBottom = '10px';
    bannerDiv.innerHTML = `<div class="headline">${htmlEscape(topBannerText)}</div>`;
    right.appendChild(bannerDiv);
  }
  // 第一段：一句话总览（新手模式核心）
  const story = buildStoryline(f);
  const storyDiv = document.createElement('div');
  storyDiv.className = 'storyline';
  storyDiv.innerHTML = `
    <div class="headline">${htmlEscape(story.sentence)}</div>
    <div class="sub">${htmlEscape(story.sub)}</div>
  `;
  right.appendChild(storyDiv);

  // 第二段：5 张核心卡片（新手默认）
  // 说明：不强依赖数字；数字降级到详情区
  const cards = document.createElement('div');
  cards.className = 'cards';

  const cGoal = `
    <div class="card">
      <h3>现在要做什么？</h3>
      <div class="big">${htmlEscape(goalTitle || 'N/A')}</div>
      <div class="small">${subgoal ? ('子目标：' + htmlEscape(subgoal)) : '子目标：—'}</div>
    </div>`;

  const trend = trendLabel(f?.state?.state_trend);
  const cSafe = `
    <div class="card">
      <h3>现在安全吗？</h3>
      <div class="big">${htmlEscape(humanSafety(safety, risk))}</div>
      <div class="small">趋势：${htmlEscape(trend)}${htmlEscape(tag.text) ? (' · ' + htmlEscape(tag.text)) : ''}${expertMode ? (` · risk=${htmlEscape(String(risk ?? 'N/A'))}`) : ''}</div>
    </div>`;

  const seen = safe(f?.inputs?.raw_observation_summary) || '';
  const seenHuman = seen ? `关键观测：${seen}` : '关键观测：暂无明显信号';
  const cSeen = `
    <div class="card">
      <h3>系统看到了什么关键东西？</h3>
      <div class="big">${htmlEscape(seen ? '有输入信号' : '无明显新信号')}</div>
      <div class="small">${htmlEscape(seenHuman)}</div>
    </div>`;

  const modsRun = JSON.stringify(f?.outputs?.modules_run ?? []);
  const modsSkip = JSON.stringify(f?.outputs?.modules_skipped ?? []);
  const cDo = `
    <div class="card">
      <h3>系统决定怎么做？</h3>
      <div class="big">${htmlEscape(humanAction(action))}</div>
      <div class="small">执行：${htmlEscape(modsRun)} · 跳过：${htmlEscape(modsSkip)}</div>
    </div>`;

  const why = safe(f?.decision?.decision_reason);
  const cWhy = `
    <div class="card">
      <h3>为什么这么做？</h3>
      <div class="big">${htmlEscape(why ? '有明确理由' : '默认策略')}</div>
      <div class="small">${htmlEscape(why || '因为当前局面稳定且风险低，所以继续正常执行。')}</div>
    </div>`;

  const viewAlign = safe(f?.state?.view_alignment_state);
  const viewAlignHuman = viewAlign === 'aligned' ? '对准' : (viewAlign === 'misaligned' ? '偏航' : (viewAlign === 'assumed_ok' ? '假定正常' : viewAlign || '—'));
  const visionQual = safe(f?.state?.vision_quality_state);
  const visionQualHuman = visionQual === 'good' ? '可靠' : (visionQual === 'degraded' ? '退化' : (visionQual === 'invalid' ? '无效' : visionQual || '—'));
  const needCorrect = f?.state?.view_correction_needed === true;
  const visionDegraded = f?.state?.vision_degraded === true;
  const correctionHint = safe(f?.state?.view_correction_hint);
  const degradeReason = safe(f?.state?.vision_degrade_reason);
  const recoveryEta = f?.state?.vision_recovery_eta_ms;
  const recoveryEtaStr = recoveryEta != null && recoveryEta > 0 ? `约 ${Math.round(recoveryEta)}ms 内可恢复` : '';
  let viewSmall = '';
  if (needCorrect && correctionHint) viewSmall += '<span class="view-alert">需纠正：' + htmlEscape(correctionHint) + '</span>';
  if (visionDegraded) viewSmall += (viewSmall ? '；' : '') + (degradeReason ? '退化原因：' + htmlEscape(degradeReason) : '') + (recoveryEtaStr ? '；' + htmlEscape(recoveryEtaStr) : '');
  if (!viewSmall) viewSmall = '当前视觉输入可信度正常';
  const cView = `
    <div class="card view-guard">
      <h3>视线与视觉</h3>
      <div class="big">视线：${htmlEscape(viewAlignHuman)} · 视觉质量：${htmlEscape(visionQualHuman)}</div>
      <div class="small">${viewSmall}</div>
    </div>`;

  const holdAllowed = f?.state?.predictive_hold_allowed === true;
  const holdActive = f?.state?.predictive_hold_active === true;
  const holdRemaining = f?.state?.predictive_hold_remaining_ms;
  const holdReason = safe(f?.state?.predictive_hold_reason);
  const recoveryAction = safe(f?.state?.predictive_recovery_action);
  const holdExpired = f?.state?.predictive_hold_expired === true;
  const cHold = `
    <div class="card predictive-hold">
      <h3>短时容错</h3>
      <div class="big">${holdActive ? '开启' : (holdExpired ? '已到期' : '关闭')}</div>
      <div class="small">${holdActive && holdRemaining != null ? '剩余：' + Math.round(holdRemaining) + ' ms' : ''}${recoveryAction ? ' · 恢复动作：' + htmlEscape(recoveryAction) : ''}${holdReason ? ' · 原因：' + htmlEscape(holdReason) : ''}</div>
    </div>`;

  const domainState = safe(f?.state?.runtime_domain_state);
  const domainStateHuman = domainState === 'normal' ? '正常' : (domainState === 'degraded' ? '降级' : (domainState === 'frozen' ? '冻结' : domainState || '—'));
  const domainMismatch = f?.state?.domain_mismatch_detected === true;
  const domainReason = safe(f?.state?.domain_mismatch_reason);
  const degradeAction = safe(f?.state?.degrade_action);
  const recoveryCond = safe(f?.state?.recovery_condition);
  const cognitiveAllowed = f?.state?.cognitive_output_allowed;
  const cDomain = `
    <div class="card runtime-domain">
      <h3>运行域状态</h3>
      <div class="big">${htmlEscape(domainStateHuman)}</div>
      <div class="small">${domainMismatch ? ('失配：' + htmlEscape(domainReason || '—') + (degradeAction ? ' · 降级：' + htmlEscape(degradeAction) : '') + (recoveryCond ? ' · 恢复条件：' + htmlEscape(recoveryCond) : '')) : '当前在正常理解范围内'}${cognitiveAllowed === false ? ' · 认知输出已关闭' : ''}</div>
    </div>`;

  const sceneType = safe(f?.state?.scene_type);
  const sceneSupported = f?.state?.scene_supported === true;
  const sceneGateState = safe(f?.state?.scene_gate_state);
  const sceneGateStateHuman = sceneGateState === 'open' ? '开放' : (sceneGateState === 'cautious' ? '谨慎' : (sceneGateState === 'suspended' ? '挂起' : sceneGateState || '—'));
  const sceneGateReason = safe(f?.state?.scene_gate_reason);
  const sceneGateAction = safe(f?.state?.scene_gate_action);
  const sceneTypeHuman = sceneType ? sceneType.replace(/_/g, ' ') : '—';
  const goalProgressPausedCard = f?.state?.goal_progress_paused === true;
  const minimumModeActiveCard = f?.state?.minimum_mode_active === true;
  const highLevelSuppressedCard = f?.state?.high_level_output_suppressed === true;
  const sceneGateControlAppliedCard = f?.state?.scene_gate_control_applied === true;
  const sceneControlLines = [];
  if (sceneGateControlAppliedCard) sceneControlLines.push('控制已生效');
  if (goalProgressPausedCard) sceneControlLines.push('已暂停 goal');
  if (highLevelSuppressedCard) sceneControlLines.push('高层输出已抑制');
  if (minimumModeActiveCard) sceneControlLines.push('最低运行模式');
  if (goalProgressPausedCard) sceneControlLines.push('当前 goal 推进已被 Scene Gate 阻断');
  const sceneControlStr = sceneControlLines.length ? sceneControlLines.join('；') : '—';
  const cSceneGate = `
    <div class="card scene-gate">
      <h3>场景 / Scene Gate</h3>
      <div class="big">${htmlEscape(sceneTypeHuman)} · ${htmlEscape(sceneGateStateHuman)}</div>
      <div class="small">${sceneSupported ? '支持域内' : '非支持域，已挂起'}${sceneGateAction ? ' · 动作：' + htmlEscape(sceneGateAction.replace(/_/g, ' ')) : ''}${sceneGateReason ? ' · ' + htmlEscape(sceneGateReason) : ''}</div>
      <div class="small" style="margin-top:6px;">控制落地：${htmlEscape(sceneControlStr)}</div>
    </div>`;

  const humanCheckNeededCard = f?.state?.human_check_needed === true;
  const humanCheckPendingCard = f?.state?.human_check_pending === true;
  const humanCheckQuestion = safe(f?.state?.human_check_question);
  const humanCheckReason = safe(f?.state?.human_check_reason);
  const humanCheckBlocking = safe(f?.state?.human_check_blocking_level);
  const humanCheckTimeout = f?.state?.human_check_timeout_ms;
  const humanCheckDefault = safe(f?.state?.human_check_default_action);
  const humanCheckResponse = safe(f?.state?.human_check_response);
  const humanCheckResolvedCard = f?.state?.human_check_resolved === true;
  const humanCheckTimeoutTriggeredCard = f?.state?.human_check_timeout_triggered === true;
  const humanCheckStatus = humanCheckPendingCard ? '等待确认' : (humanCheckResolvedCard ? (humanCheckTimeoutTriggeredCard ? '已超时默认' : '已确认') : (humanCheckNeededCard ? '需确认' : '—'));
  const humanCheckDetail = [];
  if (humanCheckTimeoutTriggeredCard) humanCheckDetail.push('用户未在规定时间内确认，已按默认策略处理');
  if (humanCheckQuestion) humanCheckDetail.push('问：' + htmlEscape(humanCheckQuestion));
  if (humanCheckReason) humanCheckDetail.push('原因：' + htmlEscape(humanCheckReason));
  if (humanCheckBlocking) humanCheckDetail.push('级别：' + htmlEscape(humanCheckBlocking));
  if (humanCheckTimeout != null) humanCheckDetail.push('超时：' + Math.round(humanCheckTimeout) + 'ms');
  if (humanCheckDefault) humanCheckDetail.push('默认：' + htmlEscape(humanCheckDefault.replace(/_/g, ' ')));
  if (humanCheckResponse) humanCheckDetail.push('回复：' + htmlEscape(humanCheckResponse));
  const cHumanCheck = `
    <div class="card human-check">
      <h3>人工沟通校准</h3>
      <div class="big">${htmlEscape(humanCheckStatus)}</div>
      <div class="small">${humanCheckDetail.length ? humanCheckDetail.join(' · ') : '未触发'}</div>
    </div>`;

  const lgs = f?.local_goal_state;
  const lgsFocus = safe(lgs?.goal_focus_region);
  const lgsProgress = safe(lgs?.goal_progress_state);
  const lgsView = safe(lgs?.primary_view_direction);
  const lgsTraversable = safe(lgs?.traversable_region_summary);
  const lgsNext = safe(lgs?.next_best_action);
  const lgsConf = lgs?.state_confidence;
  const lgsStale = lgs?.state_staleness_ms;
  const lgsRecheck = lgs?.recheck_required === true;
  const lgsRisk = safe(lgs?.local_risk_summary);
  const lgsNextHuman = lgsNext ? lgsNext.replace(/_/g, ' ') : '—';
  const lgsLines = [];
  if (lgsFocus) lgsLines.push('关注区：' + htmlEscape(lgsFocus));
  if (lgsProgress) lgsLines.push('进度：' + htmlEscape(lgsProgress));
  if (lgsView) lgsLines.push('主视向：' + htmlEscape(lgsView));
  if (lgsTraversable) lgsLines.push('通行：' + htmlEscape(lgsTraversable));
  if (lgsRecheck) lgsLines.push('需复核');
  if (lgsRisk) lgsLines.push(htmlEscape(lgsRisk));
  const lgsActionApplied = f?.state?.local_goal_action_applied === true;
  const lgsFocusApplied = f?.state?.local_goal_focus_applied === true;
  const lgsRecheckApplied = f?.state?.local_goal_recheck_applied === true;
  const lgsAppliedStr = (lgsActionApplied || lgsFocusApplied || lgsRecheckApplied)
    ? `已接管：${lgsActionApplied ? '动作' : ''}${lgsFocusApplied ? (lgsActionApplied ? '+关注' : '关注') : ''}${lgsRecheckApplied ? '+复核' : ''}`
    : '未接管行为';
  const recheckMode = safe(f?.state?.local_goal_recheck_mode);
  const recheckType = safe(f?.state?.local_goal_recheck_type);
  const recheckExecuted = f?.state?.local_goal_recheck_executed === true;
  if (recheckMode && recheckMode !== 'none') {
    lgsLines.push('主动复核：' + htmlEscape(recheckMode) + (recheckType ? ('/' + htmlEscape(recheckType)) : '') + (recheckExecuted ? '（已执行）' : ''));
  }
  const viewPriority = safe(f?.state?.local_goal_view_priority);
  const viewPriorityApplied = f?.state?.local_goal_view_priority_applied === true;
  if (viewPriority) {
    lgsLines.push('观察优先级：' + htmlEscape(viewPriority) + (viewPriorityApplied ? '（已接管）' : ''));
  }
  const cLocalGoalState = `
    <div class="card local-goal-state">
      <h3>当前局部世界状态 / Local Goal State</h3>
      <div class="big">${htmlEscape(lgsFocus || '—')} · ${htmlEscape(lgsNextHuman)}</div>
      <div class="small">${htmlEscape(lgsAppliedStr)} · ${lgsLines.length ? lgsLines.join(' · ') : '—'}${lgsConf != null ? ' · 置信度=' + lgsConf : ''}${lgsStale != null ? ' · 陈旧=' + Math.round(lgsStale) + 'ms' : ''}</div>
    </div>`;

  // 主线 2 第二阶段 M0/M1.5：Local Goal Spatial Map（含标尺字段）
  const sm = f?.local_goal_spatial_map;
  function regionLine(regionName, regions) {
    if (!regions || !regions.length) return `${regionName}：—`;
    const parts = regions.map(r => {
      const rank = r?.priority_rank;
      const sec = safe(r?.sector);
      const conf = r?.confidence;
      const stab = r?.stability_score;
      const reason = safe(r?.reason);
      const ttl = r?.ttl_ms;
      const bearing = r?.relative_bearing_deg;
      const distCm = r?.distance_cm;
      const dBand = safe(r?.distance_band);
      const oBand = safe(r?.offset_band);
      const head = `#${rank != null ? rank : '—'} ${sec || '—'}`;
      const tail = [
        conf != null ? ('conf=' + conf) : null,
        stab != null ? ('stability=' + stab) : null,
        ttl != null ? ('ttl=' + Math.round(ttl) + 'ms') : null,
        bearing != null ? (bearing + '°') : null,
        distCm != null ? (distCm + 'cm') : null,
        dBand ? ('band=' + dBand) : null,
        oBand ? ('offset=' + oBand) : null,
        reason ? reason : null,
      ].filter(Boolean).join(', ');
      return head + (tail ? (' (' + tail + ')') : '');
    });
    return `${regionName}：` + parts.join(' · ');
  }
  const spatialLines = [];
  spatialLines.push(regionLine('focus_region', sm?.focus_region));
  spatialLines.push(regionLine('traversable_region', sm?.traversable_region));
  spatialLines.push(regionLine('risk_region', sm?.risk_region));
  spatialLines.push(regionLine('confirm_region', sm?.confirm_region));
  const profileStr = sm?.scene_profile ? ` · profile=${sm.scene_profile}` : '';
  const cLocalGoalSpatialMap = `
    <div class="card local-goal-spatial-map">
      <h3>当前局部空间图 / Local Goal Spatial Map</h3>
      <div class="big">${htmlEscape(safe(sm?.summary) || '—')}${htmlEscape(profileStr)}</div>
      <div class="small">${htmlEscape(spatialLines.join(' · '))}</div>
    </div>`;

  // M1.5 标尺层卡片：场景/包络/速度
  const scale = f?.spatial_scale;
  const scaleParts = [];
  if (scale) {
    if (scale.scene_profile) scaleParts.push('场景=' + scale.scene_profile);
    if (scale.effective_body_width_cm != null) scaleParts.push('体宽=' + scale.effective_body_width_cm + 'cm');
    if (scale.effective_body_height_cm != null) scaleParts.push('体高=' + scale.effective_body_height_cm + 'cm');
    if (scale.clearance_required_cm != null) scaleParts.push('需间隙=' + scale.clearance_required_cm + 'cm');
    if (scale.forward_speed_cm_s != null) scaleParts.push('速度=' + scale.forward_speed_cm_s + 'cm/s');
    if (scale.speed_band) scaleParts.push('速度带=' + scale.speed_band);
    if (scale.reaction_horizon_ms != null) scaleParts.push('反应horizon=' + Math.round(scale.reaction_horizon_ms) + 'ms');
  }
  const cSpatialScale = `
    <div class="card spatial-scale">
      <h3>标尺层 / Spatial Scale (M1.5)</h3>
      <div class="big">${scaleParts.length ? htmlEscape(scaleParts.join(' · ')) : '—'}</div>
      <div class="small">scene_profile / 用户包络 / forward_speed / speed_band / reaction_horizon_ms</div>
    </div>`;

  // M2 局部空间关系
  const relList = f?.local_goal_spatial_relations || [];
  const relLines = relList.map(r => {
    const src = (r?.source_region_type || '—') + '#' + (r?.source_priority_rank ?? '—');
    const tgt = (r?.target_region_type || '—') + '#' + (r?.target_priority_rank ?? '—');
    const type = r?.relation_type || '—';
    const conf = r?.confidence != null ? ('conf=' + r.confidence) : '';
    const reason = safe(r?.reason);
    return src + ' → ' + tgt + ' [' + type + ']' + (conf ? ' ' + conf : '') + (reason ? ' ' + reason : '');
  });
  const cLocalGoalSpatialRelations = `
    <div class="card local-goal-spatial-relations">
      <h3>局部空间关系 / Local Goal Spatial Relations (M2)</h3>
      <div class="big">${relLines.length ? relLines.map(l => htmlEscape(l)).join(' · ') : '—'}</div>
      <div class="small">source → target · relation_type · confidence · reason</div>
    </div>`;

  // Skeleton Mix M0：当前帧骨架配比
  const mix = f?.skeleton_mix;
  const mixWeights = mix ? [mix.navigation_weight, mix.fine_interaction_weight, mix.observation_weight, mix.safety_weight] : [];
  const mixFloors = mix ? [mix.navigation_floor, mix.fine_interaction_floor, mix.observation_floor, mix.safety_floor] : [];
  const mixWeightStr = mixWeights.length ? mixWeights.map((w, i) => ['nav','fine','obs','safe'][i] + '=' + (w != null ? w.toFixed(2) : '—')).join(' ') : '—';
  const mixFloorStr = mixFloors.length ? mixFloors.map((fl, i) => ['nav','fine','obs','safe'][i] + '_fl=' + (fl != null ? fl.toFixed(2) : '—')).join(' ') : '—';
  const dominantStr = mix?.dominant_skeleton ? mix.dominant_skeleton.replace(/_/g, ' ') : '—';
  const reasonStr = safe(mix?.mix_reason) || '—';
  const cSkeletonMix = `
    <div class="card skeleton-mix">
      <h3>骨架配比 / Skeleton Mix (M0)</h3>
      <div class="big">主导：${htmlEscape(dominantStr)} · ${htmlEscape(reasonStr)}</div>
      <div class="small">weight: ${htmlEscape(mixWeightStr)}</div>
      <div class="small">floor: ${htmlEscape(mixFloorStr)}</div>
    </div>`;

  // 骨架过滤 M0
  const filt = f?.skeleton_filter;
  const keepStr = filt?.keep_region_types?.length ? filt.keep_region_types.join(', ') : '—';
  const suppStr = filt?.suppress_region_types?.length ? filt.suppress_region_types.join(', ') : '—';
  const granStr = safe(filt?.granularity_bias) || '—';
  const filtReasonStr = safe(filt?.filter_reason) || '—';
  const anchorPriStr = safe(filt?.keep_anchor_priority) || '—';
  const cSkeletonFilter = `
    <div class="card skeleton-filter">
      <h3>骨架过滤 / Skeleton Filter (M0)</h3>
      <div class="big">保留：${htmlEscape(keepStr)} · 压低：${htmlEscape(suppStr)}</div>
      <div class="small">粒度：${htmlEscape(granStr)} · 锚点优先：${htmlEscape(anchorPriStr)} · ${htmlEscape(filtReasonStr)}</div>
    </div>`;

  // 骨架记忆分池 M0：四层空间记忆池
  const pools = f?.spatial_memory_pools;
  const workingItems = pools?.working_memory_items || [];
  const episodeItems = pools?.episode_memory_items || [];
  const stableItems = pools?.stable_memory_items || [];
  const anchorItems = pools?.anchor_memory_items || [];
  const poolDominant = pools?.dominant_skeleton ? pools.dominant_skeleton.replace(/_/g, ' ') : '—';
  const poolReason = safe(pools?.pool_reason) || '—';
  const workingSummaries = workingItems.slice(0, 5).map(it => htmlEscape(it.payload_summary || '—')).join(' · ') || '—';
  const episodeSummaries = episodeItems.slice(0, 5).map(it => htmlEscape(it.payload_summary || '—')).join(' · ') || '—';
  const stablePlaceholder = stableItems.length ? (stableItems[0].payload_summary === '(stable placeholder M0)' ? '占位' : stableItems.length + ' 项') : '空';
  const anchorPlaceholder = anchorItems.length ? (anchorItems[0].payload_summary === '(anchor placeholder M0)' ? '占位' : anchorItems.length + ' 项') : '空';
  const cSpatialMemoryPools = `
    <div class="card spatial-memory-pools">
      <h3>空间记忆分池 / Spatial Memory Pools (M0)</h3>
      <div class="big">主导：${htmlEscape(poolDominant)} · ${htmlEscape(poolReason)}</div>
      <div class="small">working (${workingItems.length})：${workingSummaries}</div>
      <div class="small">episode (${episodeItems.length})：${episodeSummaries}</div>
      <div class="small">stable：${stablePlaceholder} · anchor：${anchorPlaceholder}</div>
    </div>`;

  // 空间遗忘 M0
  const fg = f?.spatial_forgetting;
  const fgWork = fg?.working_expired_count ?? 0;
  const fgColl = fg?.episode_collapsed_count ?? 0;
  const fgExp = fg?.episode_expired_count ?? 0;
  const fgReason = safe(fg?.forgetting_reason_summary) || '—';
  const fgActions = fg?.forgetting_actions_applied?.length ? fg.forgetting_actions_applied.join(', ') : '无';
  const cSpatialForgetting = `
    <div class="card spatial-forgetting">
      <h3>空间遗忘 / Spatial Forgetting (M0)</h3>
      <div class="big">working 过期：${fgWork} · episode 塌缩：${fgColl} · episode 过期：${fgExp}</div>
      <div class="small">原因：${htmlEscape(fgReason)}</div>
      <div class="small">已应用：${htmlEscape(fgActions)}</div>
    </div>`;

  // 证据账本 M0
  const ledger = f?.evidence_ledger;
  const entries = ledger?.entries || [];
  const first = entries[0];
  const claimStr = first ? htmlEscape(first.claim_summary || '—') : '—';
  const supN = first ? (first.supporting_evidence?.length ?? 0) : 0;
  const confN = first ? (first.conflicting_evidence?.length ?? 0) : 0;
  const missN = first ? (first.missing_evidence?.length ?? 0) : 0;
  const confVal = first?.evidence_confidence != null ? (first.evidence_confidence * 100).toFixed(0) + '%' : '—';
  const riskStr = first ? htmlEscape(first.risk_if_wrong || '—') : '—';
  const sugStr = first ? htmlEscape(first.suggested_next_check || '—') : '—';
  const cEvidenceLedger = `
    <div class="card evidence-ledger">
      <h3>证据账本 / Evidence Ledger (M0)</h3>
      <div class="big">${claimStr}</div>
      <div class="small">支持：${supN} · 冲突：${confN} · 缺失：${missN} · 置信度：${confVal}</div>
      <div class="small">误判风险：${riskStr}</div>
      <div class="small">建议补证：${sugStr}</div>
    </div>`;

  // 假设层 M0
  const hypLayer = f?.hypothesis_layer;
  const hypList = hypLayer?.hypotheses || [];
  const firstHyp = hypList[0];
  const hypSum = firstHyp ? htmlEscape(firstHyp.hypothesis_summary || '—') : '—';
  const hypType = firstHyp ? htmlEscape((firstHyp.hypothesis_type || '—').replace(/_/g, ' ')) : '—';
  const hypConf = firstHyp?.hypothesis_confidence != null ? (firstHyp.hypothesis_confidence * 100).toFixed(0) + '%' : '—';
  const hypRisk = firstHyp ? htmlEscape(firstHyp.risk_if_wrong || '—') : '—';
  const hypHint = firstHyp ? htmlEscape(firstHyp.verification_hint || '—') : '—';
  const hypStatus = firstHyp ? htmlEscape(firstHyp.hypothesis_status || '—') : '—';
  const hypReason = safe(hypLayer?.hypothesis_reason_summary) || '—';
  const cHypothesisLayer = `
    <div class="card hypothesis-layer">
      <h3>假设层 / Hypothesis Layer (M0)</h3>
      <div class="big">${hypSum}</div>
      <div class="small">类型：${hypType} · 置信度：${hypConf} · 状态：${hypStatus}</div>
      <div class="small">误判风险：${hypRisk} · 验证建议：${hypHint}</div>
      <div class="small">${hypList.length} 条假设 · ${htmlEscape(hypReason)}</div>
    </div>`;

  // 补证规划 M0
  const rp = f?.recheck_planner;
  const rpAction = rp ? htmlEscape(rp.recheck_action || '—') : '—';
  const rpReason = safe(rp?.recheck_reason) || '—';
  const rpTarget = safe(rp?.recheck_target) || '—';
  const rpPriority = safe(rp?.recheck_priority) || '—';
  const rpBlocked = rp?.recheck_blocked === true;
  const rpBlockReason = safe(rp?.recheck_block_reason) || '—';
  const rpApplied = rp?.recheck_applied === true;
  const cRecheckPlanner = `
    <div class="card recheck-planner">
      <h3>补证规划 / Recheck Planner (M0)</h3>
      <div class="big">动作：${rpAction} · 已执行：${rpApplied ? '是' : '否'} · 阻断：${rpBlocked ? '是' : '否'}</div>
      <div class="small">原因：${rpReason}</div>
      <div class="small">目标：${rpTarget} · 优先级：${rpPriority}${rpBlocked ? ' · 阻断原因：' + htmlEscape(rpBlockReason) : ''}</div>
    </div>`;

  // Recheck Whitebox Trace M0：补证白盒轨迹（仅解释）
  const rwb = f?.recheck_whitebox_trace;
  const rwbApplied = rwb?.whitebox_applied === true;
  const rwbSummary = safe(rwb?.whitebox_summary) || '—';
  const rwbSteps = Array.isArray(rwb?.reasoning_steps) ? rwb.reasoning_steps : [];
  const rwbWeights = Array.isArray(rwb?.weight_allocation) ? rwb.weight_allocation : [];
  const rwbExcl = Array.isArray(rwb?.exclusion_log) ? rwb.exclusion_log : [];
  const rwbInter = Array.isArray(rwb?.interaction_trace) ? rwb.interaction_trace : [];
  const rwbStepLines = rwbSteps.length ? rwbSteps.map(s => `${s.step_index}. ${safe(s.step_name) || '—'} | in=${safe(s.step_input_summary) || '—'} | out=${safe(s.step_output_summary) || '—'}`).join('\\n') : '—';
  const rwbWeightLines = rwbWeights.slice(0, 6).map(w => {
    const aid = safe(w?.action_id) || '—';
    const ah = safe(w?.action_human_label) || '—';
    const tot = w?.weight_total != null ? String(w.weight_total) : '—';
    const comps = w?.weight_components ? JSON.stringify(w.weight_components) : '{}';
    const rs = safe(w?.weight_reason) || '—';
    return `${aid}（${ah}） total=${tot} comps=${comps} reason=${rs}`;
  }).join('\\n') || '—';
  const rwbExclLines = rwbExcl.slice(0, 6).map(e => {
    const aid = safe(e?.excluded_action_id) || '—';
    const ah = safe(e?.excluded_action_human_label) || '—';
    const rs = safe(e?.excluded_reason) || '—';
    const st = safe(e?.excluded_at_stage) || '—';
    return `${aid}（${ah}） stage=${st} reason=${rs}`;
  }).join('\\n') || '—';
  const rwbInterLines = rwbInter.length ? rwbInter.map(i => {
    const sp = safe(i?.system_prompt_summary) || '—';
    const ur = safe(i?.user_feedback_raw) || '—';
    const mt = safe(i?.mapped_confirmation_type) || '—';
    const ne = safe(i?.next_effect) || '—';
    const ef = safe(i?.interaction_effect_on_recheck) || '—';
    return `sys=${sp}\\nuser_raw=${ur}\\nmapped=${mt} next=${ne}\\neffect=${ef}`;
  }).join('\\n\\n') : 'no_interaction_this_frame';
  const cRecheckWhiteboxTrace = `
    <div class="card recheck-whitebox-trace">
      <h3>补证白盒轨迹 / Recheck Whitebox Trace (M0)</h3>
      <div class="big">applied：${rwbApplied ? '是' : '否'} · summary：${htmlEscape(rwbSummary)}</div>
      <div class="small"><pre style="margin:6px 0 0; background:#0b1020; color:#e6edf3; padding:8px; border-radius:8px;">${htmlEscape(rwbStepLines)}</pre></div>
      <div class="small"><pre style="margin:6px 0 0; background:#0b1020; color:#e6edf3; padding:8px; border-radius:8px;">${htmlEscape(rwbWeightLines)}</pre></div>
      <div class="small"><pre style="margin:6px 0 0; background:#0b1020; color:#e6edf3; padding:8px; border-radius:8px;">${htmlEscape(rwbExclLines)}</pre></div>
      <div class="small"><pre style="margin:6px 0 0; background:#0b1020; color:#e6edf3; padding:8px; border-radius:8px;">${htmlEscape(rwbInterLines)}</pre></div>
    </div>`;

  // 对象时空账本 M1.5：容器逻辑增强（最后可信 vs 当前候选分离 + 容器状态）
  const otl = f?.object_temporal_ledger;
  const objEntry = otl?.focus_object_entry;
  const objLabel = objEntry ? htmlEscape(objEntry.object_label || '—') : '—';
  const lastConfLoc = objEntry ? htmlEscape(objEntry.last_confirmed_location || '—') : '—';
  const lastConfTs = objEntry?.last_confirmed_ts != null ? objEntry.last_confirmed_ts.toFixed(2) : '—';
  const candLoc = objEntry ? htmlEscape(objEntry.current_candidate_location || '—') : '—';
  const candTs = objEntry?.current_candidate_ts != null ? objEntry.current_candidate_ts.toFixed(2) : '—';
  const candType = objEntry ? htmlEscape(objEntry.candidate_location_type || '—') : '—';
  const objVis = objEntry ? htmlEscape(objEntry.visibility_status || '—') : '—';
  const objConf = objEntry?.ledger_confidence != null ? (objEntry.ledger_confidence * 100).toFixed(0) + '%' : '—';
  const objContainer = objEntry ? htmlEscape((objEntry.current_container_candidate || '').slice(0, 36)) : '—';
  const containerConf = objEntry?.current_container_confidence != null ? (objEntry.current_container_confidence * 100).toFixed(0) + '%' : '—';
  const containerState = objEntry ? htmlEscape(objEntry.container_state || '—') : '—';
  const otlReason = safe(otl?.ledger_reason) || '—';
  const stateSummary = safe(otl?.ledger_state_summary) || '—';
  const evList = (otl?.events ?? []).slice(-5).map(ev => `${ev.event_type || '?'}@${ev.timestamp != null ? ev.timestamp.toFixed(1) : '?'} ${safe(ev.summary) || ''}`).join(' | ');
  const cObjectTemporalLedger = `
    <div class="card object-temporal-ledger">
      <h3>对象时空账本 / Object Temporal Ledger (M1.5)</h3>
      <div class="big">关注对象：${objLabel} · 可见性：${objVis} · 账本置信度：${objConf}</div>
      <div class="small"><strong>最后可信位置</strong>：${lastConfLoc} @ ${lastConfTs} · <strong>当前候选位置</strong>：${candLoc} @ ${candTs}</div>
      <div class="small">候选类型：${candType} · 容器状态：${containerState}</div>
      <div class="small">容器候选：${objContainer}（置信度 ${containerConf}）</div>
      <div class="small">状态摘要：${htmlEscape(stateSummary)}</div>
      <div class="small">最近事件：${evList || '—'}</div>
      <div class="small">${htmlEscape(otlReason)}</div>
    </div>`;

  // 交互式寻物 M0/M1
  const osi = f?.object_search_interaction;
  const osiTarget = osi ? htmlEscape(osi.search_target_label || '—') : '—';
  const osiSubtask = osi ? htmlEscape(osi.search_subtask_state || '—') : '—';
  const osiState = osi ? htmlEscape(osi.search_state || '—') : '—';
  const osiAction = osi ? htmlEscape(osi.interaction_action || '—') : '—';
  const osiReason = safe(osi?.interaction_reason) || '—';
  const osiPrompt = safe(osi?.interaction_prompt) || '—';
  const osiZone = safe(osi?.suggested_search_zone) || '—';
  const osiResultLevel = osi ? htmlEscape(osi.search_result_level || '—') : '—';
  const osiWaiting = osi?.search_waiting_user_input === true;
  const osiTerminal = osi ? htmlEscape(osi.search_terminal_status || '—') : '—';
  const osiCanResume = osi?.search_can_resume_main_task === true;
  const osiBlock = safe(osi?.blocking_issue) || '—';
  const osiApplied = osi?.interaction_applied === true;
  // M1.5：任务流增强
  const osiFlow = osi ? htmlEscape(osi.interaction_flow_type || '—') : '—';
  const osiStepIdx = osi?.interaction_step_index ?? '—';
  const osiExpectedInput = safe(osi?.interaction_expected_user_input) || '—';
  const osiTimeoutMs = osi?.interaction_timeout_ms ?? '—';
  const osiTimeoutTriggered = osi?.interaction_timeout_triggered === true;
  const osiFallbackAction = safe(osi?.fallback_action) || '—';
  const osiFallbackReason = safe(osi?.fallback_reason) || '—';
  const osiNextStep = safe(osi?.next_search_step_summary) || '—';
  const osiPath = osi?.search_resolution_path?.length ? osi.search_resolution_path.join(' → ') : '—';
  const osiRetry = osi?.interaction_retry_count ?? '—';
  // M0.5：Spatial Expression → Search 文案接入；Level 2 口语化行动表达 M0
  const osiFromSidecar = osi?.search_zone_from_sidecar === true ? 'yes' : 'no';
  const sidecarForOsi = f?.spatial_expression_sidecar;
  const osiLevel2 = sidecarForOsi?.focus_target_actionable_expression ? '是' : '否';
  const cObjectSearchInteraction = `
    <div class="card object-search-interaction">
      <h3>交互式寻物 / Object Search Interaction (M1.5)</h3>
      <div class="big">目标：${osiTarget} · 子任务状态：${osiSubtask} · 动作：${osiAction}</div>
      <div class="small">结果分级：${osiResultLevel} · 等待用户输入：${osiWaiting ? '是' : '否'} · 终端状态：${osiTerminal} · 可恢复主任务：${osiCanResume ? '是' : '否'}</div>
      <div class="small">flow：${osiFlow} · 步骤：${osiStepIdx} · 期待输入：${htmlEscape(osiExpectedInput)} · 超时：${osiTimeoutMs}ms ${osiTimeoutTriggered ? '已触发' : ''}</div>
      <div class="small">回退：${htmlEscape(osiFallbackAction)} · 原因：${htmlEscape(osiFallbackReason)} · 重试：${osiRetry}</div>
      <div class="small">位置/搜索区：${htmlEscape(osiZone)} · from sidecar：${osiFromSidecar} · Level 2 行动表达：${osiLevel2}</div>
      <div class="small">下一步建议：${htmlEscape(osiNextStep)}</div>
      <div class="small">路径：${htmlEscape(osiPath)}</div>
      <div class="small">原因：${htmlEscape(osiReason)} · 提示：${htmlEscape(osiPrompt)}</div>
      <div class="small">阻断：${htmlEscape(osiBlock)} · 已执行：${osiApplied ? '是' : '否'}</div>
    </div>`;

  // Action Hint Copy M0：推理→引导→确认
  const ah = f?.action_hint_copy;
  const ahStage = safe(ah?.action_hint_stage) || '—';
  const ahPrimary = safe(ah?.action_hint_primary) || '—';
  const ahFollowup = safe(ah?.action_hint_followup) || '—';
  const ahConfirmation = safe(ah?.action_hint_confirmation) || '—';
  const ahReason = safe(ah?.action_hint_reason) || '—';
  const ahApplied = ah?.action_hint_applied === true;
  const cActionHintCopy = `
    <div class="card action-hint-copy">
      <h3>动作提示 / Action Hint Copy (M0)</h3>
      <div class="big">stage：${htmlEscape(ahStage)} · 已应用：${ahApplied ? '是' : '否'}</div>
      <div class="small">主提示：${htmlEscape(ahPrimary)}</div>
      <div class="small">后续提示：${htmlEscape(ahFollowup)}</div>
      <div class="small">确认提示：${htmlEscape(ahConfirmation)}</div>
      <div class="small">reason：${htmlEscape(ahReason)}</div>
    </div>`;

  // Action Hint Whitebox Trace M0：引导话术白盒轨迹（含用户可见解释层）
  const ahwb = f?.action_hint_whitebox_trace;
  const ahwbApplied = ahwb?.whitebox_applied === true;
  const ahwbSummary = safe(ahwb?.whitebox_summary) || '—';
  const ahwbSteps = Array.isArray(ahwb?.reasoning_steps) ? ahwb.reasoning_steps : [];
  const ahwbWeights = Array.isArray(ahwb?.weight_allocation) ? ahwb.weight_allocation : [];
  const ahwbExcl = Array.isArray(ahwb?.exclusion_log) ? ahwb.exclusion_log : [];
  const ahwbInter = Array.isArray(ahwb?.interaction_trace) ? ahwb.interaction_trace : [];
  const ahwbStepLines = ahwbSteps.length ? ahwbSteps.map(s => `${s.step_index}. ${safe(s.step_name) || '—'} | in=${safe(s.step_input_summary) || '—'} | out=${safe(s.step_output_summary) || '—'}`).join('\\n') : '—';
  const ahwbWeightLines = ahwbWeights.slice(0, 6).map(w => {
    const hid = safe(w?.hint_id) || '—';
    const hh = safe(w?.hint_human_label) || '—';
    const tot = w?.weight_total != null ? String(w.weight_total) : '—';
    const rs = safe(w?.weight_reason) || '—';
    return `${hid}（${hh}） total=${tot} reason=${rs}`;
  }).join('\\n') || '—';
  const ahwbExclLines = ahwbExcl.slice(0, 6).map(e => {
    const hid = safe(e?.excluded_hint_id) || '—';
    const hh = safe(e?.excluded_hint_human_label) || '—';
    const rs = safe(e?.excluded_reason) || '—';
    const st = safe(e?.excluded_at_stage) || '—';
    return `${hid}（${hh}） stage=${st} reason=${rs}`;
  }).join('\\n') || '—';
  const ahwbInterLines = ahwbInter.length ? ahwbInter.map(i => {
    const sp = safe(i?.system_prompt_summary) || '—';
    const ur = safe(i?.user_feedback_raw) || '—';
    const mt = safe(i?.mapped_confirmation_type) || '—';
    const ne = safe(i?.next_effect) || '—';
    const ef = safe(i?.interaction_effect_on_hint) || '—';
    return `sys=${sp}\\nuser_raw=${ur}\\nmapped=${mt} next=${ne}\\neffect=${ef}`;
  }).join('\\n\\n') : 'no_interaction_this_frame';
  const uv = ahwb?.user_visible_explanation;
  const uvPrimary = safe(uv?.user_visible_reason_primary) || '—';
  const uvFollowup = safe(uv?.user_visible_reason_followup) || '—';
  const uvConfirm = safe(uv?.user_visible_reason_confirmation) || '—';
  const uvChanged = safe(uv?.user_visible_changed_by_feedback) || '—';
  const uvExcluded = safe(uv?.user_visible_excluded_alternative) || '—';
  const cActionHintWhiteboxTrace = `
    <div class="card action-hint-whitebox-trace">
      <h3>引导话术白盒轨迹 / Action Hint Whitebox Trace (M0)</h3>
      <div class="big">applied：${ahwbApplied ? '是' : '否'} · summary：${htmlEscape(ahwbSummary)}</div>
      <div class="small"><strong>用户可见解释</strong> 主提示：${htmlEscape(uvPrimary)}</div>
      <div class="small">后续：${htmlEscape(uvFollowup)} · 确认：${htmlEscape(uvConfirm)}</div>
      <div class="small">反馈影响：${htmlEscape(uvChanged)} · 未选路径：${htmlEscape(uvExcluded)}</div>
      <details><summary>专家：reasoning / weights / exclusion / interaction</summary>
      <div class="small"><pre style="margin:6px 0 0; background:#0b1020; color:#e6edf3; padding:8px; border-radius:8px;">${htmlEscape(ahwbStepLines)}</pre></div>
      <div class="small"><pre style="margin:6px 0 0; background:#0b1020; color:#e6edf3; padding:8px; border-radius:8px;">${htmlEscape(ahwbWeightLines)}</pre></div>
      <div class="small"><pre style="margin:6px 0 0; background:#0b1020; color:#e6edf3; padding:8px; border-radius:8px;">${htmlEscape(ahwbExclLines)}</pre></div>
      <div class="small"><pre style="margin:6px 0 0; background:#0b1020; color:#e6edf3; padding:8px; border-radius:8px;">${htmlEscape(ahwbInterLines)}</pre></div>
      </details>
    </div>`;

  // Confirmation Input Bridge M0：用户反馈→系统推进
  const cib = f?.confirmation_input_bridge;
  const cibType = safe(cib?.confirmation_input_type) || '—';
  const cibRaw = safe(cib?.confirmation_input_raw_text) || '—';
  const cibSource = safe(cib?.confirmation_input_source) || '—';
  const cibTargetFlow = safe(cib?.confirmation_bridge_target_flow) || '—';
  const cibNextEffect = safe(cib?.confirmation_bridge_next_effect) || '—';
  const cibReason = safe(cib?.confirmation_bridge_reason) || '—';
  const cibApplied = cib?.confirmation_bridge_applied === true;
  const cConfirmationInputBridge = `
    <div class="card confirmation-input-bridge">
      <h3>确认输入桥 / Confirmation Input Bridge (M0)</h3>
      <div class="big">input_type：${htmlEscape(cibType)} · source：${htmlEscape(cibSource)} · 已应用：${cibApplied ? '是' : '否'}</div>
      <div class="small">raw_text：${htmlEscape(cibRaw)}</div>
      <div class="small">target_flow：${htmlEscape(cibTargetFlow)} · next_effect：${htmlEscape(cibNextEffect)}</div>
      <div class="small">reason：${htmlEscape(cibReason)}</div>
    </div>`;

  // Confirmation Whitebox Trace M0：确认输入白盒轨迹（解释映射与推进，含用户可见解释层）
  const cwb = f?.confirmation_whitebox_trace;
  const cwbApplied = cwb?.whitebox_applied === true;
  const cwbSummary = safe(cwb?.whitebox_summary) || '—';
  const cwbSteps = Array.isArray(cwb?.reasoning_steps) ? cwb.reasoning_steps : [];
  const cwbWeights = Array.isArray(cwb?.weight_allocation) ? cwb.weight_allocation : [];
  const cwbExcl = Array.isArray(cwb?.exclusion_log) ? cwb.exclusion_log : [];
  const cwbInter = Array.isArray(cwb?.interaction_trace) ? cwb.interaction_trace : [];
  const cwbStepLines = cwbSteps.length ? cwbSteps.map(s => `${s.step_index}. ${safe(s.step_name) || '—'} | in=${safe(s.step_input_summary) || '—'} | out=${safe(s.step_output_summary) || '—'}`).join('\\n') : '—';
  const cwbWeightLines = cwbWeights.slice(0, 6).map(w => {
    const tid = safe(w?.candidate_type_id) || '—';
    const hh = safe(w?.candidate_human_label) || '—';
    const tot = w?.weight_total != null ? String(w.weight_total) : '—';
    const rs = safe(w?.weight_reason) || '—';
    return `${tid}（${hh}） total=${tot} reason=${rs}`;
  }).join('\\n') || '—';
  const cwbExclLines = cwbExcl.slice(0, 6).map(e => {
    const tid = safe(e?.excluded_type_id) || '—';
    const hh = safe(e?.excluded_type_human_label) || '—';
    const rs = safe(e?.excluded_reason) || '—';
    const st = safe(e?.excluded_at_stage) || '—';
    return `${tid}（${hh}） stage=${st} reason=${rs}`;
  }).join('\\n') || '—';
  const cwbInterLines = cwbInter.length ? cwbInter.map(i => {
    const sp = safe(i?.system_prompt_summary) || '—';
    const ur = safe(i?.user_feedback_raw) || '—';
    const mt = safe(i?.mapped_confirmation_type) || '—';
    const ne = safe(i?.next_effect) || '—';
    const ef = safe(i?.interaction_effect_on_confirmation) || '—';
    return `sys=${sp}\\nuser_raw=${ur}\\nmapped=${mt} next=${ne}\\neffect=${ef}`;
  }).join('\\n\\n') : 'no_confirmation_input_this_frame';
  const cuv = cwb?.user_visible_explanation;
  const cuvMap = safe(cuv?.user_visible_reason_mapping) || '—';
  const cuvNext = safe(cuv?.user_visible_reason_next_effect) || '—';
  const cuvChanged = safe(cuv?.user_visible_changed_search_direction) || '—';
  const cuvExcluded = safe(cuv?.user_visible_excluded_alternative) || '—';
  const cConfirmationWhiteboxTrace = `
    <div class="card confirmation-whitebox-trace">
      <h3>确认输入白盒轨迹 / Confirmation Whitebox Trace (M0)</h3>
      <div class="big">applied：${cwbApplied ? '是' : '否'} · summary：${htmlEscape(cwbSummary)}</div>
      <div class="small"><strong>用户可见解释</strong> 映射：${htmlEscape(cuvMap)}</div>
      <div class="small">推进：${htmlEscape(cuvNext)}</div>
      <div class="small">影响：${htmlEscape(cuvChanged)} · 未选路径：${htmlEscape(cuvExcluded)}</div>
      <details><summary>专家：reasoning / weights / exclusion / interaction</summary>
      <div class="small"><pre style="margin:6px 0 0; background:#0b1020; color:#e6edf3; padding:8px; border-radius:8px;">${htmlEscape(cwbStepLines)}</pre></div>
      <div class="small"><pre style="margin:6px 0 0; background:#0b1020; color:#e6edf3; padding:8px; border-radius:8px;">${htmlEscape(cwbWeightLines)}</pre></div>
      <div class="small"><pre style="margin:6px 0 0; background:#0b1020; color:#e6edf3; padding:8px; border-radius:8px;">${htmlEscape(cwbExclLines)}</pre></div>
      <div class="small"><pre style="margin:6px 0 0; background:#0b1020; color:#e6edf3; padding:8px; border-radius:8px;">${htmlEscape(cwbInterLines)}</pre></div>
      </details>
    </div>`;

  // Local Task Space Grid M0：局部任务二维空间格（组织层）
  const tg = f?.local_task_space_grid;
  const tgFocus = safe(tg?.focus_target_cell_id) || '—';
  const tgContainer = safe(tg?.container_candidate_cell_id) || '—';
  const tgOcc = Array.isArray(tg?.occlusion_cell_ids) && tg.occlusion_cell_ids.length ? tg.occlusion_cell_ids.join(', ') : '—';
  const tgRec = safe(tg?.recommended_search_cell_id) || '—';
  const tgFocusH = safe(tg?.focus_target_cell_human_label) || '—';
  const tgContainerH = safe(tg?.container_candidate_cell_human_label) || '—';
  const tgRecH = safe(tg?.recommended_search_cell_human_label) || '—';
  const tgAdj = Array.isArray(tg?.recommended_search_adjacent_cells) && tg.recommended_search_adjacent_cells.length ? tg.recommended_search_adjacent_cells.join(', ') : '—';
  const tgFollow = safe(tg?.grid_followup_hint) || '—';
  const tgSummary = safe(tg?.grid_summary) || '—';
  const tgApplied = tg?.grid_applied === true;
  const tgCells = Array.isArray(tg?.cells) ? tg.cells : [];
  const tgLines = tgCells.length ? tgCells.map(c => {
    const cid = safe(c?.cell_id) || '—';
    const sem = safe(c?.dominant_semantic) || '—';
    const cnt = c?.candidate_count ?? 0;
    const labs = Array.isArray(c?.candidate_labels) && c.candidate_labels.length ? c.candidate_labels.join(',') : '';
    const flags = [
      c?.focus_target_present === true ? 'focus' : null,
      c?.container_candidate_present === true ? 'container' : null,
      c?.occlusion_present === true ? 'occlusion' : null,
    ].filter(Boolean).join('|');
    return `${cid}: ${sem} c=${cnt}${flags ? ' [' + flags + ']' : ''}${labs ? ' {' + labs + '}' : ''}`;
  }).join('\\n') : '';
  const cLocalTaskSpaceGrid = `
    <div class="card local-task-space-grid">
      <h3>局部任务空间格 / Local Task Space Grid (M0)</h3>
      <div class="big">focus：${htmlEscape(tgFocus)}（${htmlEscape(tgFocusH)}） · container：${htmlEscape(tgContainer)}（${htmlEscape(tgContainerH)}） · occlusion：${htmlEscape(tgOcc)}</div>
      <div class="small">recommended_search：${htmlEscape(tgRec)}（${htmlEscape(tgRecH)}） · adjacent：${htmlEscape(tgAdj)} · applied：${tgApplied ? '是' : '否'}</div>
      <div class="small">summary：${htmlEscape(tgSummary)}</div>
      <div class="small">followup_hint：${htmlEscape(tgFollow)}</div>
      <div class="small"><pre style="margin:6px 0 0; background:#0b1020; color:#e6edf3; padding:8px; border-radius:8px;">${htmlEscape(tgLines || '—')}</pre></div>
    </div>`;

  // Grid Search Expansion M0：最小扩搜建议（建议层）
  const gse = f?.grid_search_expansion;
  const gsePrimary = safe(gse?.primary_search_cell_id) || '—';
  const gsePrimaryH = safe(gse?.primary_search_cell_human_label) || '—';
  const gseSecondary = Array.isArray(gse?.secondary_search_cell_ids) && gse.secondary_search_cell_ids.length ? gse.secondary_search_cell_ids.join(', ') : '—';
  const gseSecondaryH = Array.isArray(gse?.secondary_search_cell_human_labels) && gse.secondary_search_cell_human_labels.length ? gse.secondary_search_cell_human_labels.join(' / ') : '—';
  const gseStrategy = safe(gse?.expansion_strategy_type) || '—';
  const gseFlow = safe(gse?.expansion_flow_type) || '—';
  const gseReason = safe(gse?.expansion_reason) || '—';
  const gseSummary = safe(gse?.expansion_summary) || '—';
  const gseHint = safe(gse?.grid_search_expansion_hint) || '—';
  const gseApplied = gse?.expansion_applied === true;
  const cGridSearchExpansion = `
    <div class="card grid-search-expansion">
      <h3>搜索扩展建议 / Grid Search Expansion (M0)</h3>
      <div class="big">primary：${htmlEscape(gsePrimary)}（${htmlEscape(gsePrimaryH)}） · secondary：${htmlEscape(gseSecondary)}</div>
      <div class="small">secondary_human：${htmlEscape(gseSecondaryH)}</div>
      <div class="small">flow：${htmlEscape(gseFlow)} · strategy：${htmlEscape(gseStrategy)} · applied：${gseApplied ? '是' : '否'}</div>
      <div class="small">hint：${htmlEscape(gseHint)}</div>
      <div class="small">reason：${htmlEscape(gseReason)}</div>
      <div class="small">summary：${htmlEscape(gseSummary)}</div>
    </div>`;

  // Grid Search Whitebox Trace M0：白盒轨迹
  const wb = f?.grid_search_whitebox_trace;
  const wbApplied = wb?.whitebox_applied === true;
  const wbSummary = safe(wb?.whitebox_summary) || '—';
  const wbSteps = Array.isArray(wb?.reasoning_steps) ? wb.reasoning_steps : [];
  const wbWeights = Array.isArray(wb?.weight_allocation) ? wb.weight_allocation : [];
  const wbExcl = Array.isArray(wb?.exclusion_log) ? wb.exclusion_log : [];
  const wbInter = Array.isArray(wb?.interaction_trace) ? wb.interaction_trace : [];
  const wbStepLines = wbSteps.length ? wbSteps.map(s => `${s.step_index}. ${safe(s.step_name) || '—'} | in=${safe(s.step_input_summary) || '—'} | out=${safe(s.step_output_summary) || '—'}`).join('\\n') : '—';
  const wbWeightLines = wbWeights.slice(0, 6).map(w => {
    const cid = safe(w?.cell_id) || '—';
    const ch = safe(w?.cell_human_label) || '—';
    const tot = w?.weight_total != null ? String(w.weight_total) : '—';
    const comps = w?.weight_components ? JSON.stringify(w.weight_components) : '{}';
    const rs = safe(w?.weight_reason) || '—';
    return `${cid}（${ch}） total=${tot} comps=${comps} reason=${rs}`;
  }).join('\\n') || '—';
  const wbExclLines = wbExcl.slice(0, 6).map(e => {
    const cid = safe(e?.excluded_cell_id) || '—';
    const ch = safe(e?.excluded_cell_human_label) || '—';
    const rs = safe(e?.excluded_reason) || '—';
    const st = safe(e?.excluded_at_stage) || '—';
    return `${cid}（${ch}） stage=${st} reason=${rs}`;
  }).join('\\n') || '—';
  const wbInterLines = wbInter.length ? wbInter.map(i => {
    const sp = safe(i?.system_prompt_summary) || '—';
    const sf = safe(i?.system_followup_summary) || '—';
    const ur = safe(i?.user_feedback_raw) || '—';
    const mt = safe(i?.mapped_confirmation_type) || '—';
    const ne = safe(i?.next_effect) || '—';
    const ef = safe(i?.interaction_effect_on_search) || '—';
    return `sys_primary=${sp}\\nsys_followup=${sf}\\nuser_raw=${ur}\\nmapped=${mt} next=${ne}\\neffect=${ef}`;
  }).join('\\n\\n') : 'no_interaction_this_frame';
  const cGridSearchWhiteboxTrace = `
    <div class="card grid-search-whitebox-trace">
      <h3>搜索扩展白盒轨迹 / Grid Search Whitebox Trace (M0)</h3>
      <div class="big">applied：${wbApplied ? '是' : '否'} · summary：${htmlEscape(wbSummary)}</div>
      <div class="small"><pre style="margin:6px 0 0; background:#0b1020; color:#e6edf3; padding:8px; border-radius:8px;">${htmlEscape(wbStepLines)}</pre></div>
      <div class="small"><pre style="margin:6px 0 0; background:#0b1020; color:#e6edf3; padding:8px; border-radius:8px;">${htmlEscape(wbWeightLines)}</pre></div>
      <div class="small"><pre style="margin:6px 0 0; background:#0b1020; color:#e6edf3; padding:8px; border-radius:8px;">${htmlEscape(wbExclLines)}</pre></div>
      <div class="small"><pre style="margin:6px 0 0; background:#0b1020; color:#e6edf3; padding:8px; border-radius:8px;">${htmlEscape(wbInterLines)}</pre></div>
    </div>`;

  // 任务仲裁 M0
  const arb = f?.task_arbitration;
  const arbForeground = arb ? htmlEscape(arb.foreground_task_type || '—') : '—';
  const arbCandidates = arb?.candidate_task_types?.length ? arb.candidate_task_types.join(', ') : '—';
  const arbAction = arb ? htmlEscape(arb.arbitration_action || '—') : '—';
  const arbReason = safe(arb?.arbitration_reason) || '—';
  const arbRisk = arb ? htmlEscape(arb.risk_priority_level || '—') : '—';
  const arbOverlap = arb ? htmlEscape(arb.environment_overlap_level || '—') : '—';
  const arbConflict = arb ? htmlEscape(arb.resource_conflict_level || '—') : '—';
  const arbUserCost = arb ? htmlEscape(arb.user_interruption_cost || '—') : '—';
  const arbApplied = arb?.arbitration_applied === true;
  const cTaskArbitration = `
    <div class="card task-arbitration">
      <h3>任务仲裁 / Task Arbitration (M0)</h3>
      <div class="big">当前主任务：${arbForeground} · 仲裁动作：${arbAction}</div>
      <div class="small">候选任务类型：${htmlEscape(arbCandidates)}</div>
      <div class="small">原因：${htmlEscape(arbReason)}</div>
      <div class="small">风险等级：${arbRisk} · 环境重合：${arbOverlap} · 资源冲突：${arbConflict} · 用户打扰成本：${arbUserCost}</div>
      <div class="small">已应用：${arbApplied ? '是' : '否'}</div>
    </div>`;

  // 联合任务包 M0
  const tb = f?.task_bundle;
  const tbId = tb ? htmlEscape(tb.bundle_id || '—') : '—';
  const tbZone = safe(tb?.bundle_zone) || '—';
  const tbTasks = tb?.bundle_task_types?.length ? tb.bundle_task_types.join(', ') : '—';
  const tbSkel = tb ? htmlEscape(tb.bundle_dominant_skeleton || '—') : '—';
  const tbFocus = safe(tb?.bundle_shared_focus) || '—';
  const tbReason = safe(tb?.bundle_reason) || '—';
  const tbStatus = tb ? htmlEscape(tb.bundle_status || '—') : '—';
  const tbCreated = tb?.bundle_created === true;
  const tbApplied = tb?.bundle_applied === true;
  const tbBlock = safe(tb?.bundle_block_reason) || '—';
  const cTaskBundle = `
    <div class="card task-bundle">
      <h3>联合任务包 / Task Bundle (M0)</h3>
      <div class="big">ID：${tbId} · 状态：${tbStatus} · 已创建：${tbCreated ? '是' : '否'} · 已应用：${tbApplied ? '是' : '否'}</div>
      <div class="small">区域：${htmlEscape(tbZone)} · 任务类型：${htmlEscape(tbTasks)}</div>
      <div class="small">主导骨架：${tbSkel} · 共享焦点：${htmlEscape(tbFocus)}</div>
      <div class="small">原因：${htmlEscape(tbReason)}</div>
      <div class="small">阻断：${htmlEscape(tbBlock)}</div>
    </div>`;

  // 任务链桥接 M0
  const br = f?.task_chain_bridge;
  const brForeground = safe(br?.task_chain_foreground_summary) || '—';
  const brState = br ? htmlEscape(br.task_chain_state || '—') : '—';
  const brSubstate = safe(br?.task_chain_substate) || '—';
  const brBundleState = br ? htmlEscape(br.task_chain_bundle_state || '—') : '—';
  const brCanResume = br?.task_chain_can_resume === true;
  const brBlocked = br?.task_chain_blocked === true;
  const brBlockReason = safe(br?.task_chain_block_reason) || '—';
  const brSummaryText = safe(br?.task_chain_summary_text) || '—';
  const brSources = br?.task_chain_source_modules?.length ? br.task_chain_source_modules.join(', ') : '—';
  const brApplied = br?.task_chain_bridge_applied === true;
  const cTaskChainBridge = `
    <div class="card task-chain-bridge">
      <h3>任务链桥接 / Task Chain Bridge (M0)</h3>
      <div class="big">前台：${htmlEscape(brForeground)} · 状态：${brState} · 子状态：${htmlEscape(brSubstate)} · bundle：${brBundleState}</div>
      <div class="small">可恢复：${brCanResume ? '是' : '否'} · 阻断：${brBlocked ? '是' : '否'} · 原因：${htmlEscape(brBlockReason)}</div>
      <div class="small">摘要：${htmlEscape(brSummaryText)}</div>
      <div class="small">来源：${htmlEscape(brSources)} · 已应用：${brApplied ? '是' : '否'}</div>
    </div>`;

  // 经验演化 M0/M1
  const evo = f?.experience_evolution;
  const evoCands = evo?.candidates || [];
  const evoFirst = evoCands[0];
  const evoType = evoFirst ? htmlEscape(evoFirst.experience_type || '—') : '—';
  const evoGroup = safe(evoFirst?.experience_group_key) || '—';
  const evoSource = safe(evoFirst?.source_summary) || safe(evoFirst?.source_path) || '—';
  const evoSupport = evoFirst?.supporting_events_count ?? '—';
  const evoContra = evoFirst?.contradiction_count ?? '—';
  const evoContraSrc = evoFirst?.contradiction_sources?.length ? evoFirst.contradiction_sources.join(', ') : '—';
  const evoConfirm = evoFirst?.user_confirmed_count ?? '—';
  const evoFallback = evoFirst?.fallback_count ?? '—';
  const evoRepeat = evoFirst?.repeated_pattern_count ?? '—';
  const evoTrend = evoFirst ? htmlEscape(evoFirst.confidence_trend || '—') : '—';
  const evoBand = evoFirst ? htmlEscape(evoFirst.evolution_confidence_band || '—') : '—';
  const evoStatus = evoFirst ? htmlEscape(evoFirst.evolution_status || '—') : '—';
  const evoScore = evoFirst?.promotable_score ?? '—';
  const evoScope = safe(evoFirst?.future_use_scope) || '—';
  const evoWatchReason = safe(evoFirst?.watchlist_reason) || '—';
  const evoReason = safe(evoFirst?.evolution_reason) || '—';
  const evoBlocked = evoFirst?.promotion_blocked === true;
  const evoBlockReason = safe(evoFirst?.promotion_block_reason) || '—';
  const cExperienceEvolution = `
    <div class="card experience-evolution">
      <h3>经验演化 / Experience Evolution (M1)</h3>
      <div class="big">类型：${evoType} · 组：${htmlEscape(evoGroup)} · 状态：${evoStatus} · 趋势：${evoTrend} · 置信带：${evoBand}</div>
      <div class="small">重复：${evoRepeat} · 支撑：${evoSupport} · 冲突：${evoContra}（${htmlEscape(evoContraSrc)}）· 确认：${evoConfirm} · 回退：${evoFallback}</div>
      <div class="small">升格分：${evoScore} · 适用范围：${htmlEscape(evoScope)} · 观察原因：${htmlEscape(evoWatchReason)}</div>
      <div class="small">来源：${htmlEscape(evoSource)}</div>
      <div class="small">原因：${htmlEscape(evoReason)} · 阻断：${htmlEscape(evoBlockReason)}</div>
      <div class="small">共 ${evoCands.length} 条候选</div>
    </div>`;

  const mi = f?.mainline_integration;
  const miEnabled = mi?.integration_enabled === true;
  const miSummary = safe(mi?.integration_summary) || '—';
  const miModules = mi?.integration_observed_modules?.length ? mi.integration_observed_modules.join(', ') : (mi?.integration_consumed_modules?.length ? mi.integration_consumed_modules.join(', ') : '—');
  const miEffective = mi?.integration_effective_modules?.length ? mi.integration_effective_modules.join(', ') : '—';
  const miSoft = mi?.integration_soft_actions?.length ? mi.integration_soft_actions.join(', ') : '—';
  const miBlocked = mi?.integration_blocked_actions?.length ? mi.integration_blocked_actions.join(', ') : '—';
  const miNotes = mi?.integration_observation_notes?.length ? mi.integration_observation_notes.join('; ') : '—';
  const miApplied = mi?.integration_applied === true;
  const miFrameNote = safe(mi?.integration_observation_frame_note) || '—';
  const miPillar = mi?.integration_pillar_effective ? Object.entries(mi.integration_pillar_effective).map(([k,v]) => v ? k + ':Y' : k + ':N').join(' ') : '—';
  const cMainlineIntegration = `
    <div class="card mainline-integration">
      <h3>主线接入 / Mainline Integration (M0 / M0.6)</h3>
      <div class="big">启用：${miEnabled ? '是' : '否'} · 已应用：${miApplied ? '是' : '否'}</div>
      <div class="small">M0.5 观察：${htmlEscape(miFrameNote)}</div>
      <div class="small">摘要：${htmlEscape(miSummary)}</div>
      <div class="small">observed：${htmlEscape(miModules)}</div>
      <div class="small">effective：${htmlEscape(miEffective)}</div>
      <div class="small">软动作：${htmlEscape(miSoft)}</div>
      <div class="small">阻断动作：${htmlEscape(miBlocked)}</div>
      <div class="small">pillar有效：${htmlEscape(miPillar)}</div>
      <div class="small">观察备注：${htmlEscape(miNotes)}</div>
    </div>`;

  const vca = f?.visual_candidate_audit;
  const vcaSrc = safe(vca?.input_source_type) || '—';
  const vcaPath = safe(vca?.input_source_path) || '—';
  const vcaDetMode = safe(vca?.detector_mode) || '—';
  const vcaDetModel = safe(vca?.detector_model_name) || '—';
  const vcaDetCount = vca?.detector_candidate_count ?? '—';
  const vcaDetLabels = Array.isArray(vca?.detector_candidate_labels) ? vca.detector_candidate_labels.join(', ') : (vca?.detector_candidate_labels ?? '—');
  const vcaProbeCount = vca?.detector_probe_candidate_count ?? '—';
  const vcaProbeLabels = Array.isArray(vca?.detector_probe_candidate_labels) ? vca.detector_probe_candidate_labels.join(', ') : (vca?.detector_probe_candidate_labels ?? '—');
  const vcaOcrCount = vca?.ocr_candidate_count ?? '—';
  const vcaOcrTexts = Array.isArray(vca?.ocr_texts) ? vca.ocr_texts.join(', ') : (vca?.ocr_texts ?? '—');
  const vcaScene = vca?.scene_description_present === true ? '是' : (vca?.scene_description_present === false ? '否' : '—');
  const vcaTarget = safe(vca?.search_target_label) || '—';
  const vcaMapped = Array.isArray(vca?.mapped_candidate_labels) ? vca.mapped_candidate_labels.join(', ') : (vca?.mapped_candidate_labels ?? '—');
  const vcaStatus = safe(vca?.candidate_audit_status) || '—';
  const vcaReason = safe(vca?.candidate_audit_reason) || '—';
  const cVisualCandidateAudit = `
    <div class="card visual-candidate-audit">
      <h3>静态图候选审计 / Visual Candidate Audit (M0)</h3>
      <div class="big">输入：${htmlEscape(vcaSrc)} · 状态：${htmlEscape(vcaStatus)}</div>
      <div class="small">路径：${htmlEscape(vcaPath)}</div>
      <div class="small">detector_mode：${htmlEscape(vcaDetMode)} · 模型：${htmlEscape(vcaDetModel)}</div>
      <div class="small">detector 数量：${vcaDetCount} · 标签：${htmlEscape(vcaDetLabels)}</div>
      <div class="small">probe(弱扫描) 数量：${vcaProbeCount} · 标签：${htmlEscape(vcaProbeLabels)}</div>
      <div class="small">OCR 数量：${vcaOcrCount} · 文本：${htmlEscape(vcaOcrTexts)}</div>
      <div class="small">scene_description：${vcaScene}</div>
      <div class="small">search_target：${htmlEscape(vcaTarget)} · 映射上的候选：${htmlEscape(vcaMapped)}</div>
      <div class="small">原因：${htmlEscape(vcaReason)}</div>
    </div>`;

  const ses = f?.spatial_expression_sidecar;
  const sesFocusLabel = safe(ses?.focus_target_label) || '—';
  const sesFocusExpr = safe(ses?.focus_target_expression) || '—';
  const sesFocusDbg = safe(ses?.focus_target_debug_expression) || '—';
  const sesActionable = safe(ses?.focus_target_actionable_expression) || '—';
  const sesActionableReason = safe(ses?.focus_target_actionable_debug_reason) || '—';
  const sesCount = ses?.candidate_count ?? '—';
  const sesReason = safe(ses?.sidecar_reason) || '—';
  const sesCands = Array.isArray(ses?.candidates) ? ses.candidates : [];
  const sesLines = sesCands.slice(0, 5).map(c => {
    const lab = safe(c?.candidate_label) || '—';
    const conf = c?.candidate_confidence != null ? Number(c.candidate_confidence).toFixed(2) : '—';
    const human = safe(c?.candidate_human_location_text) || '—';
    const dbg = safe(c?.candidate_debug_location_text) || '—';
    const isFocus = c?.candidate_is_focus_target === true;
    const src = safe(c?.candidate_source_mode) || '—';
    return `${isFocus ? '[focus] ' : ''}${lab} (${conf}) @ ${human} · ${src}\\n  ${dbg}`;
  }).join('\\n');
  const cSpatialExpressionSidecar = `
    <div class="card spatial-expression-sidecar">
      <h3>坐标/方位表达旁路 / Spatial Expression Sidecar (M0)</h3>
      <div class="big">focus：${htmlEscape(sesFocusLabel)} · Level 1 表达：${htmlEscape(sesFocusExpr)}</div>
      <div class="small">focus_debug（精确/日志层）：${htmlEscape(sesFocusDbg)}</div>
      <div class="small">Level 2 口语化行动表达：${htmlEscape(sesActionable)}</div>
      <div class="small">Level 2 debug_reason：${htmlEscape(sesActionableReason)}</div>
      <div class="small">候选数：${sesCount} · reason：${htmlEscape(sesReason)}</div>
      <div class="small"><pre style="margin:6px 0 0; background:#0b1020; color:#e6edf3; padding:8px; border-radius:8px;">${htmlEscape(sesLines || '—')}</pre></div>
    </div>`;

  cards.innerHTML = cGoal + cSafe + cSeen + cDo + cWhy + cView + cHold + cDomain + cSceneGate + cHumanCheck + cLocalGoalState + cLocalGoalSpatialMap + cLocalGoalSpatialRelations + cSkeletonMix + cSkeletonFilter + cSpatialMemoryPools + cSpatialForgetting + cEvidenceLedger + cHypothesisLayer + cRecheckPlanner + cRecheckWhiteboxTrace + cObjectTemporalLedger + cObjectSearchInteraction + cActionHintCopy + cActionHintWhiteboxTrace + cConfirmationInputBridge + cConfirmationWhiteboxTrace + cLocalTaskSpaceGrid + cGridSearchExpansion + cGridSearchWhiteboxTrace + cTaskArbitration + cTaskBundle + cTaskChainBridge + cExperienceEvolution + cMainlineIntegration + cVisualCandidateAudit + cSpatialExpressionSidecar + cSpatialScale;
  right.appendChild(cards);

  if (domainMismatch) {
    const domainAlert = document.createElement('div');
    domainAlert.className = 'view-guard-alert domain-alert';
    domainAlert.appendChild(document.createTextNode('运行域失配：' + (domainReason || '—') + (degradeAction ? '，建议：' + degradeAction.replace(/_/g, ' ') : '') + (recoveryCond ? '；恢复需：' + recoveryCond : '')));
    right.insertBefore(domainAlert, right.children[1]);
  }
  if (!sceneSupported && sceneGateState === 'suspended') {
    const sceneAlert = document.createElement('div');
    sceneAlert.className = 'view-guard-alert domain-alert';
    sceneAlert.appendChild(document.createTextNode('Scene Gate 挂起：当前场景不在支持域内（' + (sceneTypeHuman || '—') + '），动作：' + (sceneGateAction ? sceneGateAction.replace(/_/g, ' ') : '—')));
    right.insertBefore(sceneAlert, right.children[1]);
  }
  if (humanCheckPending && humanCheckQuestion) {
    const humanAlert = document.createElement('div');
    humanAlert.className = 'view-guard-alert';
    humanAlert.style.background = '#e7f3ff';
    humanAlert.style.borderColor = '#0969da';
    humanAlert.appendChild(document.createTextNode('人工确认：' + humanCheckQuestion + (humanCheckTimeout != null ? '（超时 ' + Math.round(humanCheckTimeout) + 'ms 后按默认动作执行）' : '')));
    right.insertBefore(humanAlert, right.children[1]);
  }
  if ((needCorrect || visionDegraded) && !domainMismatch) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'view-guard-alert';
    if (needCorrect) alertDiv.appendChild(document.createTextNode('⚠ 镜头偏航：' + (correctionHint || '建议纠正镜头方向')));
    if (visionDegraded) alertDiv.appendChild(document.createTextNode((needCorrect ? '；' : '') + '视觉退化：' + (degradeReason || '质量下降') + (recoveryEtaStr ? '，' + recoveryEtaStr : '')));
    right.insertBefore(alertDiv, right.children[1]);
  }

  // 第三段：详细展开（专家模式保留工程深度）
  const expertTop = document.createElement('details');
  expertTop.open = expertMode;
  const expertTopSum = document.createElement('summary');
  expertTopSum.textContent = expertMode ? '展开更多（专家信息）' : '展开更多（点击查看详情）';
  expertTop.appendChild(expertTopSum);
  const expertMeta = document.createElement('div');
  expertMeta.className = 'kv';
  const ownerHuman = humanOwner(owner);
  const actionHuman = humanAction(action);
  expertMeta.innerHTML = `
    <div class="k">谁拍板</div><div class="v">${htmlEscape(ownerHuman)}（${htmlEscape(owner || 'N/A')}）</div>
    <div class="k">正在做什么</div><div class="v">${htmlEscape(actionHuman)}（${htmlEscape(action || 'N/A')}）</div>
    <div class="k">预期后果</div><div class="v">收益：${htmlEscape(f?.consequence?.expected_gain || 'N/A')} · 代价：${htmlEscape(f?.consequence?.expected_cost || 'N/A')} · 风险：${htmlEscape(f?.consequence?.expected_risk || 'N/A')}</div>
  `;
  expertTop.appendChild(expertMeta);
  right.appendChild(expertTop);

  // 责任链：折叠面板（专家模式默认展开更多）
  const sections = [
    ['goal', f.goal, ['goal_id','goal_type','goal_description','goal_source','goal_priority','goal_confidence','goal_status','subgoal_description','goal_switch_reason']],
    ['inputs', f.inputs, ['frame_seq','produced_ts','current_ts','delta_t_ms','sampled','route','active_b2_impact','raw_observation_summary','goal_relevant_observations','sensor_notes']],
    ['state', f.state, ['prev_state_summary','state_delta_summary','state_trend','goal_progress_delta','view_alignment_state','view_alignment_score','view_misaligned','view_correction_needed','view_correction_hint','vision_quality_state','vision_reliability_score','vision_degraded','vision_degrade_reason','vision_recovery_eta_ms','predictive_hold_allowed','predictive_hold_active','predictive_hold_remaining_ms','predictive_hold_reason','predictive_hold_confidence','predictive_hold_expired','predictive_recovery_action','runtime_domain_state','runtime_domain_confidence','domain_mismatch_detected','domain_mismatch_reason','cognitive_degrade_level','cognitive_output_allowed','degrade_action','recovery_condition','scene_type','scene_supported','scene_gate_state','scene_gate_reason','scene_gate_action','goal_progress_paused','minimum_mode_active','high_level_output_suppressed','scene_gate_control_applied','human_check_needed','human_check_reason','human_check_question','human_check_blocking_level','human_check_timeout_ms','human_check_default_action','human_check_response','human_check_resolved','human_check_pending','human_check_timeout_triggered','focus_region_hint','view_behavior_hint','local_goal_action_applied','local_goal_focus_applied','local_goal_recheck_applied','local_goal_recheck_mode','local_goal_recheck_type','local_goal_recheck_executed','local_goal_view_priority','local_goal_view_priority_applied','c1_state','motion','diff','risk_score','safety_level','weak_evidence_level','traversability_state','local_risk_summary','goal_progress_state','state_confidence','state_notes']],
    ['decision', f.decision, ['decision_id','for_goal_id','decision_owner','decision_type','decision_reason','policy_mode_before','policy_mode_after','b2_impact_applied','escape_hatch_triggered','floor_forced','decision_confidence']],
    ['outputs', f.outputs, ['policy_intent_summary','sampling_target_fps','detector_stride','ocr_stride','modules_run','modules_skipped','action_summary','user_facing_output','output_notes']],
    ['consequence', f.consequence, ['expected_gain','expected_cost','expected_risk','consequence_confidence','evaluation_horizon_ms','rollback_hint','post_action_check_needed']],
    ['local_goal_state', f.local_goal_state, ['goal_id','goal_type','goal_focus_region','goal_progress_state','primary_view_direction','traversable_region_summary','critical_objects','state_confidence','state_staleness_ms','recheck_required','local_risk_summary','next_best_action']],
    ['local_goal_spatial_map', f.local_goal_spatial_map, ['goal_id','goal_type','produced_ts','staleness_ms','scene_profile','focus_region','traversable_region','risk_region','confirm_region','summary']],
    ['local_goal_spatial_relations', f.local_goal_spatial_relations, []],
    ['skeleton_mix', f.skeleton_mix, ['navigation_weight','fine_interaction_weight','observation_weight','safety_weight','navigation_floor','fine_interaction_floor','observation_floor','safety_floor','dominant_skeleton','mix_reason']],
    ['skeleton_filter', f.skeleton_filter, ['keep_region_types','suppress_region_types','keep_anchor_priority','suppress_detail_level','granularity_bias','filter_reason']],
    ['spatial_memory_pools', f.spatial_memory_pools, ['working_memory_items','episode_memory_items','stable_memory_items','anchor_memory_items','dominant_skeleton','pool_reason']],
    ['spatial_forgetting', f.spatial_forgetting, ['working_expired_count','episode_collapsed_count','episode_expired_count','forgetting_reason_summary','forgetting_actions_applied']],
    ['evidence_ledger', f.evidence_ledger, ['entries']],
    ['hypothesis_layer', f.hypothesis_layer, ['hypotheses','dominant_hypothesis_type','hypothesis_reason_summary']],
    ['recheck_planner', f.recheck_planner, ['recheck_action','recheck_reason','recheck_target','recheck_priority','recheck_blocked','recheck_block_reason','recheck_applied']],
    ['recheck_whitebox_trace', f.recheck_whitebox_trace, ['whitebox_summary','whitebox_applied','reasoning_steps','weight_allocation','exclusion_log','interaction_trace']],
    ['action_hint_whitebox_trace', f.action_hint_whitebox_trace, ['whitebox_summary','whitebox_applied','reasoning_steps','weight_allocation','exclusion_log','interaction_trace','user_visible_explanation']],
    ['object_temporal_ledger', f.object_temporal_ledger, ['focus_object_entry','events','ledger_reason','ledger_state_summary']],
    ['object_search_interaction', f.object_search_interaction, ['search_target_label','search_state','search_subtask_state','search_waiting_user_input','search_terminal_status','search_can_resume_main_task','search_summary_for_task_chain','search_result_level','interaction_action','interaction_reason','interaction_prompt','suggested_search_zone','search_zone_from_sidecar','last_interaction_action','last_user_response_type','last_user_response_value','candidate_confidence_level','blocking_issue','interaction_applied','interaction_flow_type','interaction_step_index','interaction_expected_user_input','interaction_timeout_ms','interaction_timeout_triggered','fallback_action','fallback_reason','next_search_step_summary','search_resolution_path','interaction_retry_count']],
    ['action_hint_copy', f.action_hint_copy, ['action_hint_stage','action_hint_summary','action_hint_primary','action_hint_followup','action_hint_confirmation','action_hint_reason','action_hint_applied']],
    ['confirmation_input_bridge', f.confirmation_input_bridge, ['confirmation_input_type','confirmation_input_raw_text','confirmation_input_source','confirmation_bridge_reason','confirmation_bridge_applied','confirmation_bridge_target_flow','confirmation_bridge_next_effect']],
    ['local_task_space_grid', f.local_task_space_grid, ['grid_rows','grid_cols','focus_target_cell_id','container_candidate_cell_id','occlusion_cell_ids','recommended_search_cell_id','focus_target_cell_human_label','container_candidate_cell_human_label','recommended_search_cell_human_label','recommended_search_adjacent_cells','grid_followup_hint','grid_summary','grid_applied','cells']],
    ['grid_search_expansion', f.grid_search_expansion, ['primary_search_cell_id','primary_search_cell_human_label','secondary_search_cell_ids','secondary_search_cell_human_labels','expansion_flow_type','expansion_strategy_type','expansion_reason','expansion_summary','expansion_applied','grid_search_expansion_hint']],
    ['grid_search_whitebox_trace', f.grid_search_whitebox_trace, ['whitebox_summary','whitebox_applied','reasoning_steps','weight_allocation','exclusion_log','interaction_trace']],
    ['task_arbitration', f.task_arbitration, ['foreground_task_type','candidate_task_types','arbitration_action','arbitration_reason','risk_priority_level','environment_overlap_level','resource_conflict_level','user_interruption_cost','arbitration_applied']],
    ['task_bundle', f.task_bundle, ['bundle_id','bundle_zone','bundle_task_types','bundle_dominant_skeleton','bundle_shared_focus','bundle_reason','bundle_status','bundle_created','bundle_applied','bundle_block_reason']],
    ['task_chain_bridge', f.task_chain_bridge, ['task_chain_foreground_summary','task_chain_state','task_chain_substate','task_chain_blocked','task_chain_block_reason','task_chain_can_resume','task_chain_bundle_state','task_chain_source_modules','task_chain_summary_text','task_chain_bridge_applied']],
    ['experience_evolution', f.experience_evolution, ['candidates']],
    ['mainline_integration', f.mainline_integration, ['integration_enabled','integration_summary','integration_consumed_modules','integration_observed_modules','integration_effective_modules','integration_soft_actions','integration_blocked_actions','integration_observation_notes','integration_applied','integration_observation_frame_note','integration_pillar_effective']],
    ['visual_candidate_audit', f.visual_candidate_audit, ['input_source_type','input_source_path','detector_mode','detector_model_name','detector_candidate_count','detector_candidate_labels','detector_probe_candidate_count','detector_probe_candidate_labels','ocr_candidate_count','ocr_texts','scene_description_present','search_target_label','mapped_candidate_labels','candidate_audit_status','candidate_audit_reason']],
    ['spatial_expression_sidecar', f.spatial_expression_sidecar, ['focus_target_label','focus_target_expression','focus_target_debug_expression','focus_target_actionable_expression','focus_target_actionable_debug_reason','candidate_count','candidates','sidecar_reason']],
    ['spatial_scale', f.spatial_scale, ['scene_profile','effective_body_width_cm','effective_body_height_cm','clearance_required_cm','forward_speed_cm_s','speed_band','reaction_horizon_ms']],
  ];

  const labelMap = new Map([
    ['goal', '我现在要做什么'],
    ['inputs', '我看到了什么'],
    ['state', '我怎么理解现在的情况'],
    ['decision', '我为什么这么决定'],
    ['outputs', '我实际做了什么'],
    ['consequence', '这样做会有什么结果'],
  ]);
  const openByDefault = expertMode ? new Set(['goal','inputs','state','decision','outputs','consequence']) : new Set([]);
  sections.forEach(([name, obj, keys]) => {
    const det = document.createElement('details');
    if (openByDefault.has(name)) det.open = true;
    const sum = document.createElement('summary');
    sum.textContent = labelMap.get(name) || name;
    det.appendChild(sum);
    if (name === 'state' && (f?.state?.prev_state_summary || f?.state?.state_delta_summary || f?.state?.state_trend || f?.state?.goal_progress_delta)) {
      const continuity = document.createElement('div');
      continuity.className = 'continuity';
      continuity.innerHTML = `
        <div class="k">与上一时刻相比</div>
        <div class="v">
          上一时刻：${htmlEscape(safe(f?.state?.prev_state_summary) || '—')}；
          本次变化：${htmlEscape(safe(f?.state?.state_delta_summary) || '—')}；
          当前趋势：${htmlEscape(trendLabel(f?.state?.state_trend))}；
          对目标推进的影响：${htmlEscape(safe(f?.state?.goal_progress_delta) || '—')}
        </div>`;
      det.appendChild(continuity);
    }
    det.appendChild(kvTable(obj, keys));
    right.appendChild(det);
  });

  // raw JSON：底部折叠，不抢主信息位置
  const raw = document.createElement('details');
  const rawSum = document.createElement('summary');
  rawSum.textContent = 'raw JSON / debug';
  raw.appendChild(rawSum);
  const pre = document.createElement('pre');
  pre.textContent = JSON.stringify(f, null, 2);
  raw.appendChild(pre);
  right.appendChild(raw);
}

async function load() {
  document.getElementById('status').textContent = 'loading…';
  const resp = await fetch('/api/frames?' + qs(), { cache: 'no-store' });
  if (!resp.ok) throw new Error('load failed: ' + resp.status);
  frames = await resp.json();
  activeIndex = frames.length ? 0 : -1;
  renderList();
  renderDetail();
}

document.getElementById('btn_reload').onclick = () => load();
['f_owner','f_goal','f_action'].forEach(id => {
  document.getElementById(id).addEventListener('input', () => load());
});
document.getElementById('mode_toggle').addEventListener('change', (e) => {
  expertMode = !!e.target.checked;
  renderList();
  renderDetail();
});

load().catch(e => {
  document.getElementById('status').textContent = 'error';
  document.getElementById('right').innerHTML = '<pre>' + safe(e) + '</pre>';
});
</script>
</body>
</html>
"""


def _read_jsonl(path: str) -> list[dict]:
    out: list[dict] = []
    if not path or not os.path.exists(path):
        return out
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except Exception:
                continue
    return out


def _contains(v: object, needle: str) -> bool:
    if not needle:
        return True
    if v is None:
        return False
    return needle.lower() in str(v).lower()


class _Handler(BaseHTTPRequestHandler):
    jsonl_path: str = ""

    def _send(self, code: int, body: bytes, content_type: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):  # noqa: N802
        u = urlparse(self.path)
        if u.path == "/" or u.path == "/index.html":
            self._send(200, INDEX_HTML.encode("utf-8"), "text/html; charset=utf-8")
            return

        if u.path == "/api/frames":
            qs = parse_qs(u.query)
            owner = (qs.get("owner") or [""])[0].strip()
            goal = (qs.get("goal") or [""])[0].strip()
            action = (qs.get("action") or [""])[0].strip()

            frames = _read_jsonl(self.jsonl_path)
            filtered: list[dict] = []
            for f in frames:
                if not _contains(((f.get("decision") or {}).get("decision_owner")), owner):
                    continue
                if not _contains(((f.get("goal") or {}).get("goal_type")), goal):
                    continue
                act_v = ((f.get("outputs") or {}).get("action_summary")) or ((f.get("decision") or {}).get("decision_type"))
                if not _contains(act_v, action):
                    continue
                filtered.append(f)

            body = json.dumps(filtered, ensure_ascii=False).encode("utf-8")
            self._send(200, body, "application/json; charset=utf-8")
            return

        self._send(404, b"not found", "text/plain; charset=utf-8")

    def log_message(self, fmt: str, *args):  # noqa: N802
        # 安静模式：不刷屏
        return


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jsonl", required=True, help="Decision Monitor JSONL 路径（如 logs/decision_monitor.jsonl）")
    ap.add_argument("--host", default="127.0.0.1", help="监听地址（默认 127.0.0.1）")
    ap.add_argument("--port", type=int, default=8765, help="端口（默认 8765）；若被占用会自动尝试 +1")
    args = ap.parse_args()

    _Handler.jsonl_path = args.jsonl
    port = args.port
    for _ in range(20):
        try:
            httpd = HTTPServer((args.host, port), _Handler)
            break
        except OSError as e:
            if e.errno != 48:  # 48 = Address already in use
                raise
            port += 1
    else:
        print("错误：连续 20 个端口均被占用，请先关闭其他 viewer 或换 --port", file=__import__("sys").stderr)
        return 1
    print(f"Decision Monitor Viewer: http://{args.host}:{port}  (jsonl={args.jsonl})")
    if port != args.port:
        print(f"（端口 {args.port} 已被占用，已改用 {port}）")
    print("按 Ctrl+C 退出")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())

