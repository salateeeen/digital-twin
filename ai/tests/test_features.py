import unittest
import pandas as pd
from pathlib import Path
import tempfile
from src.features import load_snapshots, add_features

class TestFeatures(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.csv_path = Path(self.test_dir.name) / "test.csv"
        self.valid_csv = """schemaVersion,runId,entityId,entityType,observedAt,status,utilizationPct,latencyMs,packetLossPct,throughputMbps,source,sequence
1.0,test-run,link-1,link,2026-01-01T00:00:00Z,healthy,50.0,20.0,0.0,10.0,mininet,1
1.0,test-run,link-1,link,2026-01-01T00:00:05Z,degraded,85.0,55.0,2.5,8.0,mininet,2"""

    def tearDown(self):
        self.test_dir.cleanup()

    def write_csv(self, content):
        with open(self.csv_path, "w", encoding="utf-8") as f:
            f.write(content)

    def test_valid_snapshots_and_utc(self):
        self.write_csv(self.valid_csv)
        df = load_snapshots(self.csv_path)
        self.assertEqual(len(df), 2)
        # التأكد من الاحتفاظ بتوقيت UTC
        self.assertEqual(str(df["observedAt"].dt.tz), "UTC")

    def test_missing_column_raises_error(self):
        bad_csv = self.valid_csv.replace(",sequence", "")
        self.write_csv(bad_csv)
        with self.assertRaises(ValueError) as context:
            load_snapshots(self.csv_path)
        self.assertIn("missing columns", str(context.exception))

    def test_wrong_schema_version(self):
        bad_csv = self.valid_csv.replace("1.0,", "2.0,")
        self.write_csv(bad_csv)
        with self.assertRaises(ValueError) as context:
            load_snapshots(self.csv_path)
        self.assertIn("schemaVersion must be exactly", str(context.exception))

    def test_invalid_percentage(self):
        bad_csv = self.valid_csv.replace("50.0", "150.0")
        self.write_csv(bad_csv)
        with self.assertRaises(ValueError) as context:
            load_snapshots(self.csv_path)
        self.assertIn("must be between 0 and 100", str(context.exception))

    def test_negative_latency(self):
        bad_csv = self.valid_csv.replace("20.0", "-5.0")
        self.write_csv(bad_csv)
        with self.assertRaises(ValueError) as context:
            load_snapshots(self.csv_path)
        self.assertIn("cannot be negative", str(context.exception))

    def test_add_features_logic(self):
        self.write_csv(self.valid_csv)
        df = load_snapshots(self.csv_path)
        decision_time = pd.Timestamp("2026-01-01T00:00:10Z")
        features_df = add_features(df, decision_time)
        
        # التأكد من حساب الفرق في الاستهلاك (85.0 - 50.0 = 35.0)
        self.assertEqual(features_df["deltaUtilizationPct"].iloc[1], 35.0)
        
        # التأكد من حساب عمر البيانات بالثواني
        self.assertEqual(features_df["telemetryAgeSeconds"].iloc[1], 5.0)
        
        # التأكد من إشارة الازدحام
        self.assertTrue(features_df["congestionSignal"].iloc[1])

if __name__ == "__main__":
    unittest.main(verbosity=2)