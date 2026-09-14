/**
 * Luna Agent Planning — browser state / package builder (dry-run explainability).
 * Builds L2 UI package from situationPkg + envelope; does not execute tools.
 */
(function (global) {
  "use strict";

  function uid(prefix) {
    return prefix + "_" + Math.random().toString(36).slice(2, 10);
  }

  function toolCaps(plan, key) {
    return ((plan && plan[key]) || []).map(function (t) {
      return t.capability_type || t;
    });
  }

  function scorePlan(plan, userGoal, situation) {
    var breakdown = {
      user_goal_alignment: 0,
      missing_info_fit: 0,
      survival_risk_fit: 0,
      cost_penalty: 0,
      noop_discipline: 0
    };
    var ug = (userGoal && userGoal.goal_type) || "unknown";
    var ugText = ((userGoal && userGoal.goal_text_optional) || "").toLowerCase();
    var planGoal = ((plan && plan.plan_goal_candidate) || {}).goal_type || "unknown";
    var tools = toolCaps(plan, "tool_plan_candidates");
    var noops = toolCaps(plan, "noop_tool_plan_candidates");

    if (ug !== "unknown") {
      if (planGoal === ug || (ug === "navigate" && planGoal === "navigate") ||
          (ugText.indexOf("entrance") >= 0 && planGoal === "navigate")) {
        breakdown.user_goal_alignment = 0.45;
      } else if ((planGoal === "read_text" || planGoal === "identify_place") &&
          (ug === "identify" || ug === "read" || ug === "find")) {
        breakdown.user_goal_alignment = 0.3;
      } else {
        breakdown.user_goal_alignment = 0.05;
      }
    } else {
      var tasks = ((situation && situation.task_clue_candidates) || []).map(function (t) {
        return t.task_type;
      });
      breakdown.user_goal_alignment =
        (tasks.indexOf(planGoal) >= 0 || planGoal === "identify_place" || planGoal === "find_direction") ? 0.35 : 0.15;
    }

    var missing = ((situation && situation.missing_information_candidates) || []).map(function (m) {
      return m.info_type;
    });
    var fit = 0;
    if (missing.indexOf("text_content") >= 0 && tools.indexOf("ocr") >= 0) fit += 0.12;
    if (missing.indexOf("place_identity") >= 0 && tools.indexOf("ocr") >= 0) fit += 0.08;
    if (missing.indexOf("direction_info") >= 0 && tools.indexOf("ocr") >= 0) fit += 0.12;
    if (missing.indexOf("walkable_area") >= 0 &&
        (tools.indexOf("detection") >= 0 || tools.indexOf("depth") >= 0 || tools.indexOf("tracking") >= 0)) fit += 0.15;
    breakdown.missing_info_fit = Math.min(fit, 0.25);

    var cost = 0.02 * tools.length;
    if (tools.indexOf("slam") >= 0 && planGoal !== "navigate" && planGoal !== "assess_walkable") cost += 0.15;
    breakdown.cost_penalty = -Math.min(cost, 0.25);

    if (planGoal === "read_text" || planGoal === "identify_place" || planGoal === "find_direction") {
      if (noops.indexOf("slam") >= 0 && noops.indexOf("tracking") >= 0 && noops.indexOf("depth") >= 0) {
        breakdown.noop_discipline = 0.12;
      } else if (tools.indexOf("slam") >= 0) {
        breakdown.noop_discipline = -0.15;
      }
    }

    var total = breakdown.user_goal_alignment + breakdown.missing_info_fit +
      breakdown.survival_risk_fit + breakdown.cost_penalty + breakdown.noop_discipline;
    return { score: Math.round(total * 10000) / 10000, breakdown: breakdown };
  }

  function buildSelectionReason(pkg) {
    var selected = pkg.selected_plan || {};
    var goal = selected.goal_type || "unknown";
    var tools = ((pkg.tool_plan || {}).active || []).map(function (t) { return t.capability_type; });
    var noops = ((pkg.tool_plan || {}).noop || []).map(function (t) { return t.capability_type; });
    var missing = (pkg.situation_summary && pkg.situation_summary.missing_information) || [];
    var positives = [];
    var negatives = [];

    if (goal === "navigate") positives.push("用户目标明确为导航 / 寻找入口");
    if (goal === "identify_place" || goal === "read_text") {
      positives.push("用户当前未提出导航需求");
      if (missing.indexOf("text_content") >= 0 || missing.indexOf("place_identity") >= 0) {
        positives.push("当前缺失信息是文字/地点内容");
        positives.push("OCR 成本低，适合 information gathering");
      }
    }
    if (goal === "ask_user") {
      positives.push("场景不确定，优先向用户澄清");
      negatives.push("不 blanket 激活全部模型");
    }
    if (noops.indexOf("slam") >= 0) negatives.push("无需空间建模（SLAM noop）");
    if (noops.indexOf("tracking") >= 0) negatives.push("无需动态目标分析（Tracking noop）");
    if (noops.indexOf("depth") >= 0 && tools.indexOf("detection") < 0) {
      negatives.push("无需深度测距（Depth noop）");
    }

    var finals = {
      identify_place: "OCR-first information gathering",
      read_text: "OCR-first information gathering",
      find_direction: "OCR-first direction finding",
      navigate: "navigation-support plan candidate",
      assess_walkable: "risk-assessment plan candidate",
      ask_user: "ask-user-first (no blanket activation)"
    };
    return {
      positives: positives,
      negatives: negatives,
      final_label: finals[goal] || "selected plan candidate",
      selected_goal: goal,
      candidate_only: true,
      not_fact: true
    };
  }

  function synthesizePlanFromSituation(situationPkg, userGoal) {
    if (!global.LunaSituationUnderstandingState && !situationPkg) return null;
    // Prefer calling through agent planning if dry-run payload injected
    var scene = (situationPkg.scene_profile_candidate || {}).scene_type || "unknown_scene";
    var tasks = (situationPkg.task_clue_candidates || []).map(function (t) { return t.task_type; });
    var missing = (situationPkg.missing_information_candidates || []).map(function (m) { return m.info_type; });
    var likely = ((situationPkg.model_need_hints || {}).likely_needed || []).map(function (h) {
      return h.capability_type;
    });
    var notNeeded = ((situationPkg.model_need_hints || {}).not_needed || []).map(function (h) {
      return h.capability_type;
    });
    var ug = (userGoal && userGoal.goal_type) || "unknown";
    var ugText = ((userGoal && userGoal.goal_text_optional) || "").toLowerCase();

    var goalType = "unknown";
    if (ug === "navigate" || ugText.indexOf("entrance") >= 0 || ugText.indexOf("导航") >= 0 || ugText.indexOf("入口") >= 0) {
      goalType = "navigate";
    } else if (scene === "unknown_scene") {
      goalType = "ask_user";
    } else if (tasks.indexOf("find_direction") >= 0 || scene === "subway_platform") {
      goalType = "find_direction";
    } else if (tasks.indexOf("assess_walkable") >= 0 || scene === "street_crossing") {
      goalType = "assess_walkable";
    } else if (tasks.indexOf("identify_place") >= 0) {
      goalType = "identify_place";
    } else if (tasks.indexOf("read_text") >= 0) {
      goalType = "read_text";
    }

    var tools = [];
    var noops = notNeeded.slice();
    var strategy = "information_gathering";
    if (goalType === "navigate") {
      strategy = "navigation_support";
      tools = scene === "corridor" ? ["depth", "slam"] : ["detection", "depth"];
      if (likely.indexOf("ocr") >= 0) tools.push("ocr");
      noops = noops.filter(function (n) { return tools.indexOf(n) < 0; });
    } else if (goalType === "ask_user") {
      strategy = "ask_user_first";
      tools = [];
      noops = ["slam", "detection", "ocr", "tracking", "depth"];
    } else if (goalType === "assess_walkable") {
      strategy = "risk_assessment";
      tools = ["detection", "depth", "tracking"];
      noops = ["ocr"];
    } else {
      strategy = goalType === "identify_place" ? "place_identification" : "information_gathering";
      tools = ["ocr"];
      noops = ["slam", "tracking", "depth"];
    }

    var plan = {
      plan_id: uid("plan"),
      plan_goal_candidate: {
        goal_type: goalType,
        interpreted_goal: goalType + " for " + scene,
        source: ug !== "unknown" ? "user_goal" : "situation_task_clue",
        confidence: ug !== "unknown" ? 0.88 : 0.8,
        candidate_only: true,
        not_fact: true,
        trace_refs: ug !== "unknown" && goalType === "navigate" ? [{
          stage: "user_goal_overrides_task_clue",
          resolution: "plan_goal_navigate"
        }] : []
      },
      plan_strategy: { strategy_type: strategy, reason: "deterministic ui stub", candidate_only: true, not_fact: true },
      plan_steps: goalType === "ask_user" ? [
        { step_order: 1, step_type: "ask_user", step_goal: "clarify user goal" },
        { step_order: 2, step_type: "stop", step_goal: "await clarification" }
      ] : [
        { step_order: 1, step_type: "observe", step_goal: "observe context" },
        { step_order: 2, step_type: "request_tool", step_goal: "request tools via Tool OS" },
        { step_order: 3, step_type: "evaluate_result", step_goal: "evaluate sufficiency" },
        { step_order: 4, step_type: "fallback", step_goal: "low confidence fallback" },
        { step_order: 5, step_type: "stop", step_goal: "apply stop conditions" }
      ],
      tool_plan_candidates: tools.map(function (c) {
        return {
          capability_type: c,
          tool_purpose: c + " evidence",
          execution_mode: "request_tool_os_admission",
          priority: "P0",
          reason: "plan candidate",
          candidate_only: true,
          not_fact: true
        };
      }),
      noop_tool_plan_candidates: noops.map(function (c) {
        return {
          capability_type: c,
          noop_reason: "not required for selected plan candidate",
          policy_ref: "noop_plan_required",
          candidate_only: true,
          not_fact: true
        };
      }),
      handoff_to_tool_os_candidate: {
        should_handoff: tools.length > 0,
        handoff_reason: tools.length ? "handoff tool plans to Tool OS" : "no executable tool plan",
        required_tool_os_checks: ["permission check", "resource check", "runner admission"],
        runner_admission_required: tools.length > 0,
        fact_admission_required_after_result: true,
        candidate_only: true,
        not_fact: true
      },
      no_runner_invocation: true,
      no_tool_execution: true,
      candidate_only: true,
      not_fact: true
    };
    return plan;
  }

  function buildCompetition(situationPkg, userGoal) {
    var situation = situationPkg || {};
    var scene = (situation.scene_profile_candidate || {}).scene_type || "unknown_scene";
    var competing = [];

    // Plan A — OCR / identify
    var planA = synthesizePlanFromSituation(situation, { goal_type: "identify", goal_text_optional: "identify place" });
    competing.push({ competition_slot: "plan_a_read_identify", label: "识别地点 / OCR", plan: planA, driver: "scene_default_text_task" });

    // Plan primary from actual goal
    var planPrimary = synthesizePlanFromSituation(situation, userGoal || { goal_type: "unknown" });
    competing.push({
      competition_slot: "plan_primary_user_or_situation",
      label: "primary:" + ((planPrimary.plan_goal_candidate || {}).goal_type),
      plan: planPrimary,
      driver: (userGoal && userGoal.goal_type && userGoal.goal_type !== "unknown") ? "user_goal" : "situation_task_clue"
    });

    // Plan B — entrance / navigate
    var planB = synthesizePlanFromSituation(situation, {
      goal_type: "navigate",
      goal_text_optional: "navigate_to_entrance"
    });
    competing.push({ competition_slot: "plan_b_find_entrance", label: "寻找入口 / Detection+Depth", plan: planB, driver: "navigation_or_entrance" });

    // Plan C — VLM / ask / understand
    var planCGoal = scene === "unknown_scene" ? { goal_type: "unknown" } : { goal_type: "understand", goal_text_optional: "understand environment" };
    var planC = synthesizePlanFromSituation(
      scene === "unknown_scene" ? Object.assign({}, situation, {
        scene_profile_candidate: Object.assign({}, situation.scene_profile_candidate || {}, { scene_type: "unknown_scene" })
      }) : situation,
      planCGoal
    );
    if (scene === "unknown_scene") {
      competing.push({ competition_slot: "plan_c_ask_user", label: "询问用户 / Ask user", plan: planC, driver: "ask_user_first" });
    } else {
      competing.push({ competition_slot: "plan_c_environment_vlm", label: "了解环境 / VLM", plan: planC, driver: "environment_understanding" });
    }

    var scored = competing.map(function (item) {
      var sc = scorePlan(item.plan, userGoal || { goal_type: "unknown" }, situation);
      return Object.assign({}, item, { score: sc.score, score_breakdown: sc.breakdown, candidate_only: true, not_fact: true });
    });
    scored.sort(function (a, b) { return b.score - a.score; });
    return {
      competition_id: uid("pcomp"),
      competing_plans: scored,
      selected_plan_candidate: scored[0].plan,
      selected_slot: scored[0].competition_slot,
      selection_trace: {
        stage: "plan_competition_select",
        selected_slot: scored[0].competition_slot,
        selected_goal: (scored[0].plan.plan_goal_candidate || {}).goal_type,
        score: scored[0].score,
        reason: (userGoal && userGoal.goal_type && userGoal.goal_type !== "unknown")
          ? "user_goal_dominates_scene_default"
          : "situation_and_missing_info_drive_selection"
      },
      candidate_only: true,
      not_fact: true
    };
  }

  function toUiPayload(situationPkg, competition, options) {
    options = options || {};
    var plan = competition.selected_plan_candidate;
    var cards = competition.competing_plans.map(function (item) {
      return {
        slot: item.competition_slot,
        label: item.label,
        goal_type: (item.plan.plan_goal_candidate || {}).goal_type,
        strategy_type: (item.plan.plan_strategy || {}).strategy_type,
        tools: toolCaps(item.plan, "tool_plan_candidates"),
        noops: toolCaps(item.plan, "noop_tool_plan_candidates"),
        score: item.score,
        status: item.competition_slot === competition.selected_slot ? "selected" : "candidate",
        driver: item.driver,
        candidate_only: true,
        not_fact: true
      };
    });
    var goalCandidates = [];
    var seen = {};
    competition.competing_plans.forEach(function (item) {
      var g = item.plan.plan_goal_candidate || {};
      var gt = g.goal_type || "unknown";
      if (seen[gt]) return;
      seen[gt] = true;
      goalCandidates.push({
        goal_type: gt,
        interpreted_goal: g.interpreted_goal || gt,
        confidence: Math.round((g.confidence || item.score || 0.5) * 100) / 100,
        source: g.source || item.driver,
        candidate_only: true,
        not_fact: true
      });
    });
    goalCandidates.sort(function (a, b) { return b.confidence - a.confidence; });

    var sitSummary = {
      scene_type: (situationPkg.scene_profile_candidate || {}).scene_type,
      confidence: (situationPkg.scene_profile_candidate || {}).confidence,
      task_clues: (situationPkg.task_clue_candidates || []).map(function (t) {
        return { task_type: t.task_type, priority: t.priority };
      }),
      missing_information: (situationPkg.missing_information_candidates || []).map(function (m) {
        return m.info_type;
      }),
      owned_by: (situationPkg.scene_profile_candidate || {}).owned_by || "situation_understanding_layer",
      candidate_only: true,
      not_fact: true,
      wording: "当前证据支持这是一个场景候选，不是已确认事实"
    };

    var pkg = {
      job_id: options.job_id || situationPkg.job_id || "",
      situation_summary: sitSummary,
      goal_candidates: goalCandidates,
      plan_competition_cards: cards,
      selected_plan: {
        plan_id: plan.plan_id,
        goal_type: (plan.plan_goal_candidate || {}).goal_type,
        strategy_type: (plan.plan_strategy || {}).strategy_type,
        steps: (plan.plan_steps || []).map(function (s) {
          return { step_order: s.step_order, step_type: s.step_type, step_goal: s.step_goal };
        }),
        candidate_only: true,
        not_fact: true
      },
      tool_plan: {
        active: (plan.tool_plan_candidates || []).map(function (t) {
          return {
            capability_type: t.capability_type,
            purpose: t.tool_purpose,
            execution_mode: t.execution_mode,
            reason: t.reason,
            candidate_only: true,
            not_fact: true
          };
        }),
        noop: (plan.noop_tool_plan_candidates || []).map(function (n) {
          return {
            capability_type: n.capability_type,
            noop_reason: n.noop_reason,
            policy_ref: n.policy_ref,
            candidate_only: true,
            not_fact: true
          };
        }),
        not_executed: true,
        candidate_only: true,
        not_fact: true
      },
      tool_os_handoff: {
        should_handoff: (plan.handoff_to_tool_os_candidate || {}).should_handoff,
        request_capabilities: toolCaps(plan, "tool_plan_candidates"),
        required_checks: (plan.handoff_to_tool_os_candidate || {}).required_tool_os_checks || [
          "permission check", "resource check", "runner admission"
        ],
        runner_admission_required: (plan.handoff_to_tool_os_candidate || {}).runner_admission_required,
        fact_admission_required_after_result: true,
        status: "candidate_only",
        not_executed: true,
        candidate_only: true,
        not_fact: true
      },
      badges: ["candidate_only", "not_fact", "selected_plan_candidate", "no_tool_execution", "no_runner_invocation"],
      candidate_only: true,
      not_fact: true,
      ui_execution_only: true
    };
    pkg.selection_reason = buildSelectionReason(pkg);
    pkg.chain_trace = [
      { stage: "L1_Situation", summary: "scene=" + (sitSummary.scene_type || "unknown") + " candidate" },
      { stage: "L2_Goal", summary: "goal=" + (pkg.selected_plan.goal_type || "unknown") + " candidate" },
      { stage: "L2_PlanCompetition", summary: "competing plans scored" },
      { stage: "L2_SelectedPlan", summary: "selected_goal=" + (pkg.selected_plan.goal_type || "unknown") },
      { stage: "L2_ToolPlan", summary: "active=" + JSON.stringify(toolCaps(plan, "tool_plan_candidates")) },
      { stage: "L3_ToolOSHandoff", summary: "handoff candidate_only · not executed" }
    ];
    return pkg;
  }

  function buildPackage(envelope, options) {
    options = options || {};
    if (options.ui_payload) return options.ui_payload;
    var situationPkg = options.situationPkg;
    if (!situationPkg) return null;

    var userGoal = options.user_goal_candidate || envelope.user_goal_candidate || {
      goal_type: "unknown",
      goal_text_optional: "",
      confidence: 0.2,
      source: "unknown"
    };

    // Detect shopfront + navigate override from envelope filename/context if present
    var fname = (envelope._source_file_name || envelope.test_case_id || "").toLowerCase();
    if ((options.force_user_goal) ) {
      userGoal = options.force_user_goal;
    }

    var competition = buildCompetition(situationPkg, userGoal);
    return toUiPayload(situationPkg, competition, {
      job_id: envelope.job_id || envelope.envelope_id || ""
    });
  }

  global.LunaAgentPlanningState = {
    version: "luna_agent_planning_state_v1",
    buildPackage: buildPackage,
    buildCompetition: buildCompetition,
    synthesizePlanFromSituation: synthesizePlanFromSituation
  };
})(typeof window !== "undefined" ? window : this);
