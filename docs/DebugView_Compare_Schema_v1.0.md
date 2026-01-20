# Risk × Authority DebugView Compare Schema v1.0

## 目的
让 Risk 与 Authority 的关系可回放、可比对、可解释。
不参与裁决，不影响行为，只做解释与分析。

## 顶层结构（冻结）
```json
{
  "run_meta": {
    "run_id": "string",
    "timestamp": "float",
    "version": {
      "code": "git_sha",
      "risk": "risk_version_id",
      "threshold": "threshold_version_id"
    }
  },
  "timeline": []
}
```

## Timeline 单帧结构（冻结）
```json
{
  "ts": 123456.78,
  "system_snapshot": {
    "perception_state": "READY",
    "calibration_state": "OK",
    "hardware_state": "OK",
    "control_distortion": false,
    "risk_level": "NORMAL"
  },
  "risk": {
    "present": true,
    "level": "MEDIUM",
    "type": ["STATIC_OBSTACLE", "RELATIVE_VELOCITY"],
    "time_to_risk": 2.4
  },
  "authority": {
    "raw": "A2",
    "effective": "A3",
    "blocked_by": "HYSTERESIS",
    "since": 123450.0
  },
  "envelope": {
    "status": "WITHIN_ENVELOPE",
    "violations": [],
    "margin": {
      "distance_m": 0.8,
      "time_s": 2.4
    }
  },
  "bc": {
    "abilities": {
      "allow_b_input": true,
      "allow_output": true
    },
    "gate": "PASS"
  },
  "c": {
    "decision": "HOLD"
  }
}
```

## 对比模式（两次运行 diff）
```json
{
  "compare": {
    "baseline_run": "run_A",
    "candidate_run": "run_B"
  },
  "diff": [
    {
      "ts": 123458.12,
      "risk.level": ["LOW", "MEDIUM"],
      "authority.effective": ["A2", "A3"],
      "envelope.status": ["WITHIN_ENVELOPE", "EDGE"]
    }
  ]
}
```

## 关键设计原则
- Risk × Authority 关系是并列解释，不是因果裁决  
- Risk 不决定 Authority，Authority 不消耗 Risk  
- DebugView 只是把两者并排展示  
- Envelope 是可接受性语言，不是动作语言

## 工程语义口径
| 术语 | 工程含义 |
| --- | --- |
| acceptable | 可接受（不最优，但允许） |
| admissible | 合规（满足规则） |
| safe enough | 足够安全（在当前 Authority 下） |
| within envelope | 在安全包络内 |

说明：`within_envelope=false` 不等价于“危险”，仅表示“不满足当前安全包络的输出条件”。  
