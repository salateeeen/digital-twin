import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from features import load_snapshots, add_features
from decision_engine import RuleConfig, decide

def run_integrated_system():
    print("Initializing System...")
    print("1. Training Random Forest Predictive Model on historical data...")
    csv_path = Path("data/raw/metric_snapshots.csv")
    decision_time = pd.Timestamp("2026-01-01T00:00:25Z")
    
    df = load_snapshots(csv_path)
    features_df = add_features(df, decision_time)
    
    feature_columns = ["utilizationPct", "latencyMs", "packetLossPct", "telemetryAgeSeconds"]
    X_train = features_df[feature_columns]
    y_train = features_df["congestionSignal"].map({True: "congested", False: "normal"})
    
    model = Pipeline([
        ('imputer', SimpleImputer(strategy='constant', fill_value=0)),
        ('rf', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    model.fit(X_train, y_train)
    
    print("\n2. Starting Integrated System (RF Predictor + Rule-Based Safety Guard)\n")
    
    live_stream = [
        {"entityId": "link-1", "status": "healthy", "utilizationPct": 60.0, "latencyMs": 20.0, "packetLossPct": 0.0, "telemetryAgeSeconds": 1.0, "observedAt": "2026-01-01T00:00:30Z"},
        {"entityId": "link-1", "status": "degraded", "utilizationPct": 85.0, "latencyMs": 55.0, "packetLossPct": 2.5, "telemetryAgeSeconds": 1.0, "observedAt": "2026-01-01T00:00:35Z"},
        {"entityId": "link-1", "status": "unknown", "utilizationPct": None, "latencyMs": None, "packetLossPct": None, "telemetryAgeSeconds": 15.0, "observedAt": "2026-01-01T00:00:40Z"},
    ]
    
    cfg = RuleConfig(cooldownSeconds=0) 
    rule_state = {}
    
    for i, snapshot in enumerate(live_stream):
        print(f"--- Timestep {i+1} ---")
        
        current_features = pd.DataFrame([{
            "utilizationPct": snapshot.get("utilizationPct"),
            "latencyMs": snapshot.get("latencyMs"),
            "packetLossPct": snapshot.get("packetLossPct"),
            "telemetryAgeSeconds": snapshot.get("telemetryAgeSeconds")
        }])
        
        prediction = model.predict(current_features)[0]
        ai_suggestion = "REROUTE_REQUEST" if prediction == "congested" else "NOOP"
        
        rule_decision, rule_state = decide(snapshot, rule_state, now_s=float(i * 10), cfg=cfg)
        
        final_solution = ai_suggestion
        if rule_decision["solutionId"] == "HOLD" and ai_suggestion != "NOOP":
            final_solution = "HOLD (AI Overridden by Safety Rules)"
            rule_decision["reasonCodes"].append("AI_OVERRIDDEN_BY_SAFETY_RULES")
            
        print(f"RF Prediction   : {prediction.upper()} -> Suggests: {ai_suggestion}")
        print(f"Rule Engine     : {rule_decision['solutionId']} (Guard Baseline)")
        print(f"Final Action    : {final_solution}")
        print(f"Safety Reasons  : {rule_decision['reasonCodes']}\n")

if __name__ == "__main__":
    run_integrated_system()