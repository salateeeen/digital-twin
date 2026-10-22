from __future__ import annotations
from typing import Any

def explain_decision(decision: dict[str, Any]) -> str:
    """
    Transforms decision engine outputs into a clear and transparent text report
    for UI display or academic defense.
    """
    solution_id = decision.get("solutionId", "UNKNOWN")
    engine_status = decision.get("engineStatus", "unknown")
    reasons = decision.get("reasonCodes", [])
    
    reason_descriptions = {
        "STATUS_FAILED": "Entity status failed, immediate recovery intervention required.",
        "STALE_OR_INCOMPLETE_TELEMETRY": "Stale or incomplete telemetry forced the engine to hold the decision (HOLD).",
        "HIGH_CONGESTION_FEATURE": "Sustained high congestion detected across multiple consecutive windows, requiring rerouting.",
        "WAIT_FOR_HYSTERESIS_CLEAR": "Waiting for congestion metrics to drop completely according to hysteresis safety rules.",
        "WAIT_FOR_CONGESTION_CONFIRMATION": "Initial congestion detected, waiting for required consecutive confirmation windows.",
        "CONGESTION_CLEARED": "Congestion indicators cleared and network returned to normal state.",
        "NO_TRIGGER": "Network state is normal and no corrective action is required.",
        "COOLDOWN": "Action repetition temporarily blocked to protect network routers during the cooldown period."
    }
    
    explanations = [
        reason_descriptions.get(code, f"Unrecognized reason code: {code}") 
        for code in reasons
    ]
    
    explanation_text = " | ".join(explanations) if explanations else "No reasons recorded."
    
    report = (
        f"--- Explainability Report ---\n"
        f"• Solution ID: {solution_id}\n"
        f"• Engine Status: {engine_status}\n"
        f"• Rationale & Evidence: [{explanation_text}]\n"
        f"------------------------------"
    )
    
    return report

if __name__ == "__main__":
    sample_decision = {
        "solutionId": "REROUTE_REQUEST",
        "engineStatus": "congested",
        "reasonCodes": ["HIGH_CONGESTION_FEATURE"]
    }
    print(explain_decision(sample_decision))