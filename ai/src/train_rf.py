import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from features import load_snapshots, add_features

def train_and_evaluate_rf():
    csv_path = Path("data/raw/metric_snapshots.csv")
    decision_time = pd.Timestamp("2026-01-01T00:00:25Z")
    
    print("Loading data and extracting features...")
    df = load_snapshots(csv_path)
    features_df = add_features(df, decision_time)
    
    feature_columns = ["utilizationPct", "latencyMs", "packetLossPct", "telemetryAgeSeconds"]
    X = features_df[feature_columns]
    
    y = features_df["congestionSignal"].map({True: "congested", False: "normal"})
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42, shuffle=False)
    
    pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='constant', fill_value=0)),
        ('rf', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    print("\nTraining Random Forest model...")
    pipeline.fit(X_train, y_train)
    
    y_pred = pipeline.predict(X_test)
    
    labels = ["normal", "congested"]
    print("\n--- Evaluation Results ---")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
    print(f"Precision (congested): {precision_score(y_test, y_pred, labels=labels, pos_label='congested', zero_division=0):.3f}")
    print(f"Recall (congested): {recall_score(y_test, y_pred, labels=labels, pos_label='congested', zero_division=0):.3f}")
    print(f"F1 Score (congested): {f1_score(y_test, y_pred, labels=labels, pos_label='congested', zero_division=0):.3f}")

if __name__ == "__main__":
    train_and_evaluate_rf()