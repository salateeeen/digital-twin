from __future__ import annotations
from pathlib import Path
import sys
import pandas as pd

REQUIRED = {
    "schemaVersion", "runId", "entityId", "entityType", "observedAt",
    "status", "utilizationPct", "latencyMs", "packetLossPct",
    "throughputMbps", "source", "sequence",
}
NUMERIC = ["utilizationPct", "latencyMs", "packetLossPct", "throughputMbps", "sequence"]

def load_snapshots(path: Path) -> pd.DataFrame:
    print(f"Reading {path.resolve()}")
    frame = pd.read_csv(path, na_values=["", "NA", "null"])
    missing = REQUIRED - set(frame.columns)
    if missing:
        raise ValueError(f"missing columns: {sorted(missing)}")
    
    frame["observedAt"] = pd.to_datetime(frame["observedAt"], utc=True, errors="raise")
    for column in NUMERIC:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
        
    if not frame["schemaVersion"].astype(str).eq("1.0").all():
        raise ValueError('schemaVersion must be exactly "1.0"')
        
    if frame["sequence"].isna().any() or (frame["sequence"] < 0).any():
        raise ValueError("sequence must be a non-negative integer")
        
    allowed_status = {"healthy", "degraded", "failed", "unknown"}
    bad_status = frame["status"].notna() & ~frame["status"].isin(allowed_status)
    if frame["status"].isna().any() or bad_status.any():
        raise ValueError(f"status must be one of {sorted(allowed_status)}")
        
    for column in ["utilizationPct", "packetLossPct"]:
        bad = frame[column].notna() & ~frame[column].between(0.0, 100.0)
        if bad.any():
            raise ValueError(f"{column} must be between 0 and 100")
            
    for column in ["latencyMs", "throughputMbps"]:
        bad = frame[column].notna() & (frame[column] < 0.0)
        if bad.any():
            raise ValueError(f"{column} cannot be negative")
            
    return frame

def add_features(frame: pd.DataFrame, decision_time: pd.Timestamp) -> pd.DataFrame:
    out = frame.sort_values(["runId", "entityId", "sequence"]).copy()
    out["telemetryAgeSeconds"] = (
        decision_time - out["observedAt"]
    ).dt.total_seconds()
    
    out["deltaUtilizationPct"] = out.groupby(
        ["runId", "entityId"]
    )["utilizationPct"].diff()
    
    out["congestionSignal"] = (
        ((out["utilizationPct"].notna()) & (out["utilizationPct"] >= 80.0)) |
        ((out["latencyMs"].notna()) & (out["latencyMs"] >= 50.0)) |
        ((out["packetLossPct"].notna()) & (out["packetLossPct"] >= 2.0))
    )
    return out

if __name__ == "__main__":
    csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/raw/metric_snapshots.csv")
    decision_time = pd.Timestamp("2026-01-01T00:00:25Z")
    result = add_features(load_snapshots(csv_path), decision_time)
    print(result[[
        "sequence", "observedAt", "telemetryAgeSeconds",
        "utilizationPct", "deltaUtilizationPct", "congestionSignal",
    ]].to_string(index=False))