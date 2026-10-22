from pathlib import Path
import sys
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/processed/toy_evaluation.csv")
df = pd.read_csv(path)
labels = ["normal", "congested"]

accuracy = accuracy_score(df.actual, df.predicted)
precision = precision_score(df.actual, df.predicted, labels=labels, pos_label="congested")
recall = recall_score(df.actual, df.predicted, labels=labels, pos_label="congested")
f1 = f1_score(df.actual, df.predicted, labels=labels, pos_label="congested", zero_division=0)

print(f"rows={len(df)}")
print(f"accuracy={accuracy:.3f}")
print(f"precision_congested={precision:.3f}")
print(f"recall_congested={recall:.3f}")
print(f"f1_congested={f1:.3f}")