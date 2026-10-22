from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import pandas as pd

# ----------------------------------------------------
# 1. إعدادات محرك القرارات (Rule Config)
# ----------------------------------------------------
@dataclass(frozen=True)
class RuleConfig:
    staleAfterSeconds: float = 12.0
    highUtilizationPct: float = 80.0
    clearUtilizationPct: float = 70.0
    highLatencyMs: float = 50.0
    clearLatencyMs: float = 35.0
    highPacketLossPct: float = 2.0
    clearPacketLossPct: float = 1.0
    requiredWindows: int = 3
    cooldownSeconds: float = 15.0
    policyVersion: str = "rules-1.0"

# ----------------------------------------------------
# 2. دالة استخراج الميزات (Add Features)
# ----------------------------------------------------
def add_features(frame: pd.DataFrame, decision_time: pd.Timestamp) -> pd.DataFrame:
    out = frame.sort_values(["runId", "entityId", "sequence"]).copy()
    
    # حساب عمر القراءة بالثواني
    out["telemetryAgeSeconds"] = (
        decision_time - out["observedAt"]
    ).dt.total_seconds()
    
    # حساب التغير في الاستهلاك
    out["deltaUtilizationPct"] = out.groupby(
        ["runId", "entityId"]
    )["utilizationPct"].diff()
    
    # تحديد إشارة الازدحام
    out["congestionSignal"] = (
        ((out["utilizationPct"].notna()) & (out["utilizationPct"] >= 80.0)) |
        ((out["latencyMs"].notna()) & (out["latencyMs"] >= 50.0)) |
        ((out["packetLossPct"].notna()) & (out["packetLossPct"] >= 2.0))
    )
    return out

# ----------------------------------------------------
# 3. دالة اتخاذ القرار (Decide)
# ----------------------------------------------------
def decide(
    snapshot: dict[str, Any],
    state: dict[str, Any],
    now_s: float,
    cfg: RuleConfig = RuleConfig(),
) -> tuple[dict[str, Any], dict[str, Any]]:
    entity_id = snapshot["entityId"]
    state = {
        "highCount": 0,
        "clearCount": 0,
        "engineStatus": "normal",
        **state,
    }
    reasons: list[str] = []
    
    age = snapshot.get("telemetryAgeSeconds")
    values = [
        snapshot.get("utilizationPct"),
        snapshot.get("latencyMs"),
        snapshot.get("packetLossPct"),
    ]
    
    stale = age is None or age > cfg.staleAfterSeconds
    failed = snapshot.get("status") == "failed"
    
    if failed:
        state["engineStatus"] = "failureSuspected"
        solution_id = "RECOVERY_REQUEST"
        reasons.append("STATUS_FAILED")
    elif stale or all(value is None for value in values):
        state["engineStatus"] = "unknown"
        solution_id = "HOLD"
        reasons.append("STALE_OR_INCOMPLETE_TELEMETRY")
    else:
        high = (
            (values[0] is not None and values[0] >= cfg.highUtilizationPct)
            or (values[1] is not None and values[1] >= cfg.highLatencyMs)
            or (values[2] is not None and values[2] >= cfg.highPacketLossPct)
        )
        clear = (
            all(value is not None for value in values)
            and values[0] < cfg.clearUtilizationPct
            and values[1] < cfg.clearLatencyMs
            and values[2] < cfg.clearPacketLossPct
        )
        
        state["highCount"] = state["highCount"] + 1 if high else 0
        state["clearCount"] = state["clearCount"] + 1 if clear else 0
        
        if state["engineStatus"] == "congested" and state["clearCount"] >= cfg.requiredWindows:
            state["engineStatus"] = "normal"
            solution_id = "NOOP"
            reasons.append("CONGESTION_CLEARED")
        elif state["highCount"] >= cfg.requiredWindows:
            state["engineStatus"] = "congested"
            solution_id = "REROUTE_REQUEST"
            reasons.append("HIGH_CONGESTION_FEATURE")
        elif state["engineStatus"] == "congested":
            solution_id = "HOLD"
            reasons.append("WAIT_FOR_HYSTERESIS_CLEAR")
        elif state["highCount"] > 0:
            solution_id = "HOLD"
            reasons.append("WAIT_FOR_CONGESTION_CONFIRMATION")
        else:
            state["engineStatus"] = "normal"
            solution_id = "NOOP"
            reasons.append("NO_TRIGGER")
            
    last_action = state.get("lastActionTime")
    if (
        solution_id not in {"NOOP", "HOLD"}
        and last_action is not None
        and now_s - last_action < cfg.cooldownSeconds
    ):
        solution_id = "HOLD"
        reasons.append("COOLDOWN")
        
    if solution_id not in {"NOOP", "HOLD"}:
        state["lastActionTime"] = now_s
        
    decision = {
        "schemaVersion": "1.0",
        "entityId": entity_id,
        "solutionId": solution_id,
        "engineStatus": state["engineStatus"],
        "reasonCodes": sorted(set(reasons)),
        "policyVersion": cfg.policyVersion,
        "observedAt": str(snapshot.get("observedAt", "")),
    }
    return decision, state