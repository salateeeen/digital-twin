import unittest
from src.rules import RuleConfig, decide

BASE = {
    "entityId": "s1-s2",
    "observedAt": "2026-01-01T00:00:00Z",
    "status": "degraded",
    "utilizationPct": 85.0,
    "latencyMs": 60.0,
    "packetLossPct": 3.0,
    "telemetryAgeSeconds": 0.1,
}

class RuleTests(unittest.TestCase):
    def test_third_high_window_requests_reroute(self):
        state = {}
        cfg = RuleConfig(cooldownSeconds=0)
        for i in range(2):
            decision, state = decide(BASE, state, float(i), cfg)
            self.assertEqual(decision["solutionId"], "HOLD")
        decision, state = decide(BASE, state, 2.0, cfg)
        self.assertEqual(decision["solutionId"], "REROUTE_REQUEST")
        self.assertEqual(decision["engineStatus"], "congested")

    def test_one_clear_window_does_not_clear(self):
        state = {}
        cfg = RuleConfig(cooldownSeconds=0)
        for i in range(3):
            _, state = decide(BASE, state, float(i), cfg)
        low = {**BASE, "utilizationPct": 60.0, "latencyMs": 20.0, "packetLossPct": 0.0}
        decision, state = decide(low, state, 3.0, cfg)
        self.assertEqual(decision["solutionId"], "HOLD")
        self.assertIn("WAIT_FOR_HYSTERESIS_CLEAR", decision["reasonCodes"])

    def test_three_clear_windows_return_to_normal(self):
        state = {}
        cfg = RuleConfig(cooldownSeconds=0)
        for i in range(3):
            _, state = decide(BASE, state, float(i), cfg)
        low = {**BASE, "utilizationPct": 60.0, "latencyMs": 20.0, "packetLossPct": 0.0}
        for i in range(2):
            _, state = decide(low, state, float(i+3), cfg)
        decision, state = decide(low, state, 5.0, cfg)
        self.assertEqual(decision["solutionId"], "NOOP")
        self.assertEqual(decision["engineStatus"], "normal")

    def test_stale_telemetry_holds(self):
        stale = {**BASE, "status": "healthy", "telemetryAgeSeconds": 99.0}
        decision, _ = decide(stale, {}, 0.0)
        self.assertEqual(decision["solutionId"], "HOLD")
        self.assertIn("STALE_OR_INCOMPLETE_TELEMETRY", decision["reasonCodes"])

    def test_cooldown_holds_repeated_request(self):
        state = {}
        cfg = RuleConfig(cooldownSeconds=15)
        for i in range(3):
            decision, state = decide(BASE, state, float(i), cfg)
        self.assertEqual(decision["solutionId"], "REROUTE_REQUEST")
        decision, _ = decide(BASE, state, 3.0, cfg)
        self.assertEqual(decision["solutionId"], "HOLD")
        self.assertIn("COOLDOWN", decision["reasonCodes"])

    def test_incomplete_telemetry_holds(self):
        incomplete = {
            **BASE,
            "status": "unknown",
            "utilizationPct": None,
            "latencyMs": None,
            "packetLossPct": None,
            "telemetryAgeSeconds": 0.1,
        }
        decision, _ = decide(incomplete, {}, 0.0)
        self.assertEqual(decision["solutionId"], "HOLD")
        self.assertIn("STALE_OR_INCOMPLETE_TELEMETRY", decision["reasonCodes"])

    def test_failed_status_requests_recovery(self):
        failed = {**BASE, "status": "failed"}
        decision, _ = decide(failed, {}, 0.0)
        self.assertEqual(decision["solutionId"], "RECOVERY_REQUEST")

if __name__ == "__main__":
    unittest.main(verbosity=2)