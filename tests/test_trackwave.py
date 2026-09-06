"""Behavior checks runnable outside any project, using only Python's stdlib."""

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/codex-trackwave/scripts/trackwave.py"
MODULE = importlib.util.spec_from_file_location("trackwave", SCRIPT)
tw = importlib.util.module_from_spec(MODULE)
MODULE.loader.exec_module(tw)


class TrackWaveTests(unittest.TestCase):
    def setUp(self):
        self.spec = tw.read_json(
            ROOT / "skills/codex-trackwave/assets/plan.example.json"
        )
        self.state = tw.new_state(self.spec)
        self.counter = 0

    def event(self, item, action, **kwargs):
        self.counter += 1
        payload = dict(
            event_id=f"event-{self.counter}",
            item=item,
            action=action,
            model="",
            run_id="",
            evidence="",
            note="",
            run_resolved=False,
        )
        payload.update(kwargs)
        return payload

    def record(self, item, action, **kwargs):
        self.state = tw.record_event(
            self.state, self.state["revision"], self.event(item, action, **kwargs)
        )

    def complete(self, item):
        self.record(item, "reserve", model="observed-configured-model")
        self.record(item, "bind", run_id=f"actual-host-run-{item}")
        self.record(item, "return", evidence=f"artifact:{item}")
        self.record(item, "accept", evidence=f"host-check:{item}")

    def test_wave_join_and_full_completion(self):
        self.assertEqual(tw.status(self.state)["ready"], ["parser", "test-design"])
        self.complete("parser")
        self.assertEqual(tw.status(self.state)["active_wave"], "implementation")
        with self.assertRaises(ValueError):
            self.record("join", "reserve", model="Sol")
        self.complete("test-design")
        self.assertEqual(tw.status(self.state)["ready"], ["join"])
        self.complete("join")
        self.assertTrue(tw.status(self.state)["complete"])
        self.assertEqual(len(self.state["events"]), 12)

    def test_same_wave_dependency_waits_for_acceptance(self):
        self.spec["items"][1]["depends_on"] = ["parser"]
        self.state = tw.new_state(self.spec)
        self.record("parser", "reserve", model="Luna")
        self.record("parser", "bind", run_id="run")
        self.record("parser", "return", evidence="patch")
        self.assertEqual(tw.status(self.state)["ready"], [])
        self.record("parser", "accept", evidence="checks")
        self.assertEqual(tw.status(self.state)["ready"], ["test-design"])

    def test_reservation_limits_concurrency_before_dispatch(self):
        self.spec["limits"]["max_parallel"] = 1
        self.state = tw.new_state(self.spec)
        self.record("parser", "reserve", model="Luna")
        before = copy.deepcopy(self.state)
        with self.assertRaisesRegex(ValueError, "parallel limit"):
            self.record("test-design", "reserve", model="Spark")
        self.assertEqual(self.state, before)

    def test_fail_requires_run_resolution_and_retries_are_bounded(self):
        for _ in range(2):
            self.record("parser", "reserve", model="Luna")
            with self.assertRaises(ValueError):
                self.record("parser", "fail", note="watch timed out")
            self.record(
                "parser",
                "fail",
                note="dispatch confirmed not started",
                run_resolved=True,
            )
        with self.assertRaisesRegex(ValueError, "attempts exhausted"):
            self.record("parser", "reserve", model="Sol")
        self.assertEqual(self.state["items"]["parser"]["attempts"], 2)
        self.assertEqual(len(self.state["events"]), 4)

    def test_evidence_and_transition_requirements(self):
        with self.assertRaises(ValueError):
            self.record("parser", "accept", evidence="invented")
        self.record("parser", "reserve", model="Luna")
        with self.assertRaises(ValueError):
            self.record("parser", "bind")
        self.record("parser", "bind", run_id="observed")
        with self.assertRaises(ValueError):
            self.record("parser", "return")
        self.record("parser", "return", evidence="artifact")
        with self.assertRaises(ValueError):
            self.record("parser", "accept")

    def test_idempotent_event_and_conflicting_id(self):
        event = self.event("parser", "reserve", model="Luna")
        self.state = tw.record_event(self.state, 0, event)
        self.record("test-design", "reserve", model="Spark")
        repeated = tw.record_event(self.state, 0, event)
        self.assertEqual(repeated, self.state)
        with self.assertRaisesRegex(ValueError, "different content"):
            tw.record_event(self.state, 0, dict(event, model="Sol"))

    def test_stale_revision_is_rejected(self):
        self.record("parser", "reserve", model="Luna")
        with self.assertRaisesRegex(ValueError, "stale revision"):
            tw.record_event(
                self.state, 0, self.event("test-design", "reserve", model="Spark")
            )

    def test_graph_and_limit_validation(self):
        for change in (
            "cycle",
            "missing",
            "future",
            "duplicate",
            "boolean-limit",
            "empty-wave",
        ):
            spec = copy.deepcopy(self.spec)
            if change == "cycle":
                spec["items"][0]["depends_on"] = ["test-design"]
                spec["items"][1]["depends_on"] = ["parser"]
            elif change == "missing":
                spec["items"][0]["depends_on"] = ["missing"]
            elif change == "future":
                spec["items"][0]["depends_on"] = ["join"]
            elif change == "duplicate":
                spec["items"][1]["id"] = "parser"
            elif change == "boolean-limit":
                spec["limits"]["max_attempts"] = True
            else:
                spec["waves"].append("unused")
            with self.subTest(change=change), self.assertRaises(ValueError):
                tw.new_state(spec)

    def test_event_replay_detects_state_corruption(self):
        self.complete("parser")
        self.state["items"]["test-design"]["state"] = "accepted"
        with self.assertRaisesRegex(ValueError, "event history"):
            tw.validate_state(self.state)

    def test_locked_and_failed_writes_preserve_state(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "plan.json"
            tw.save_locked(target, lambda: self.state)
            before = target.read_bytes()
            lock = target.with_suffix(".json.lock")
            lock.write_text('{"pid": 123}', encoding="utf-8")
            with self.assertRaises(FileExistsError):
                tw.save_locked(target, lambda: {})
            self.assertTrue(lock.exists())
            lock.unlink()
            with patch.object(
                tw.os, "replace", side_effect=OSError("simulated failure")
            ):
                with self.assertRaises(OSError):
                    tw.save_locked(target, lambda: {"new": "data"})
            self.assertEqual(target.read_bytes(), before)
            self.assertEqual(list(Path(directory).iterdir()), [target])

    def test_cli_works_in_isolated_directory_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            spec = Path(directory) / "spec.json"
            spec.write_text(json.dumps(self.spec), encoding="utf-8")
            plan = Path(directory) / "plan.json"

            def cli(*args):
                return subprocess.run(
                    [sys.executable, "-I", "-B", str(SCRIPT), *args],
                    cwd=directory,
                    capture_output=True,
                    text=True,
                    timeout=10,
                )

            result = cli("init", "--spec", str(spec), "--plan", str(plan))
            self.assertEqual(result.returncode, 0, result.stderr)
            initial = plan.read_bytes()
            self.assertEqual(
                cli("init", "--spec", str(spec), "--plan", str(plan)).returncode, 2
            )
            self.assertEqual(plan.read_bytes(), initial)
            result = cli(
                "record",
                "--plan",
                str(plan),
                "--revision",
                "0",
                "--event-id",
                "r1",
                "--item",
                "parser",
                "--action",
                "reserve",
                "--model",
                "Luna",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            result = cli("status", "--plan", str(plan))
            self.assertEqual(
                json.loads(result.stdout)["items"]["parser"]["state"], "reserved"
            )


if __name__ == "__main__":
    unittest.main()
