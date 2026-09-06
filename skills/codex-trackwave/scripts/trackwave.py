#!/usr/bin/env python3
"""Local TrackWave state recorder. Standard library only; never executes work."""

import argparse
import copy
import json
import os
import socket
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def strings(value):
    return isinstance(value, list) and all(nonempty(v) for v in value)


def validate_spec(spec):
    require(isinstance(spec, dict), "spec must be an object")
    require(spec.get("format") == "codex-trackwave/v1", "unsupported format")
    allowed = {
        "format",
        "id",
        "goal",
        "source",
        "authorization",
        "deadline",
        "limits",
        "waves",
        "items",
        "predecessor",
    }
    require(not set(spec) - allowed, "unknown spec fields; resume state with status")
    for field in ("id", "goal", "source", "authorization", "deadline"):
        require(nonempty(spec.get(field)), f"missing text: {field}")
    if "predecessor" in spec:
        require(nonempty(spec["predecessor"]), "predecessor must be text")
    limits = spec.get("limits")
    require(isinstance(limits, dict), "limits must be an object")
    require(set(limits) == {"max_parallel", "max_attempts"}, "invalid limits")
    for key in limits:
        require(type(limits[key]) is int and limits[key] > 0, f"invalid {key}")
    waves = spec.get("waves")
    require(strings(waves) and waves, "waves must be nonempty text IDs")
    require(len(waves) == len(set(waves)), "duplicate wave IDs")
    items = spec.get("items")
    require(isinstance(items, list) and items, "items must be nonempty")
    by_id = {}
    for item in items:
        require(isinstance(item, dict), "item must be an object")
        for field in ("id", "wave", "title", "route", "acceptance"):
            require(nonempty(item.get(field)), f"invalid item {field}")
        require(item["id"] not in by_id, "duplicate item IDs")
        require(item["wave"] in waves, "unknown wave")
        for field in ("depends_on", "read_set", "write_set"):
            require(strings(item.get(field)), f"invalid item {field}")
        require(
            len(item["depends_on"]) == len(set(item["depends_on"])),
            "duplicate dependency",
        )
        by_id[item["id"]] = item
    require(set(waves) == {i["wave"] for i in items}, "empty wave")
    for item in items:
        for dep in item["depends_on"]:
            require(dep in by_id, f"unknown dependency: {dep}")
            require(
                waves.index(by_id[dep]["wave"]) <= waves.index(item["wave"]),
                "dependency points into a later wave",
            )
    # Iterative DAG check avoids recursion depth depending on plan size.
    remaining = {key: set(item["depends_on"]) for key, item in by_id.items()}
    while remaining:
        roots = {key for key, deps in remaining.items() if not deps}
        require(roots, "cyclic dependencies")
        remaining = {
            key: deps - roots for key, deps in remaining.items() if key not in roots
        }


def new_state(spec):
    validate_spec(spec)
    return {
        "spec": copy.deepcopy(spec),
        "revision": 0,
        "events": [],
        "items": {i["id"]: {"state": "pending", "attempts": 0} for i in spec["items"]},
    }


def status(state):
    spec, records = state["spec"], state["items"]
    active = next(
        (
            wave
            for wave in spec["waves"]
            if any(
                records[i["id"]]["state"] != "accepted"
                for i in spec["items"]
                if i["wave"] == wave
            )
        ),
        None,
    )
    ready = [
        i["id"]
        for i in spec["items"]
        if i["wave"] == active
        and records[i["id"]]["state"] in {"pending", "failed"}
        and records[i["id"]]["attempts"] < spec["limits"]["max_attempts"]
        and all(records[d]["state"] == "accepted" for d in i["depends_on"])
    ]
    occupied = sum(r["state"] in {"reserved", "running"} for r in records.values())
    return {
        "plan_id": spec["id"],
        "revision": state["revision"],
        "active_wave": active,
        "complete": active is None,
        "ready": ready,
        "available_slots": max(0, spec["limits"]["max_parallel"] - occupied),
        "accepted": sum(r["state"] == "accepted" for r in records.values()),
        "total": len(records),
        "items": records,
    }


def apply_event(state, event):
    require(event["item"] in state["items"], "unknown item")
    record = state["items"][event["item"]]
    action, old = event["action"], record["state"]
    if action == "reserve":
        view = status(state)
        require(
            event["item"] in view["ready"], "item is not ready or attempts exhausted"
        )
        require(view["available_slots"] > 0, "parallel limit reached")
        require(nonempty(event["model"]), "reserve requires model")
        record.clear()
        record.update(state="reserved", attempts=event["attempt"], model=event["model"])
    elif action == "bind":
        require(old == "reserved", "bind requires reserved item")
        require(nonempty(event["run_id"]), "bind requires observed run ID")
        record.update(state="running", run_id=event["run_id"])
    elif action in {"return", "accept"}:
        require(
            old == ("running" if action == "return" else "returned"),
            f"invalid transition: {old} -> {action}",
        )
        require(nonempty(event["evidence"]), f"{action} requires evidence")
        record["state"] = "returned" if action == "return" else "accepted"
        record["artifact" if action == "return" else "validation"] = event["evidence"]
    elif action == "fail":
        require(old in {"reserved", "running", "returned"}, "invalid failure state")
        require(
            nonempty(event["note"]) and event["run_resolved"] is True,
            "failure requires note and resolved prior run",
        )
        record.update(state="failed", failure=event["note"])
    else:
        raise ValueError("unknown action")


def validate_state(state):
    require(isinstance(state, dict), "state must be an object")
    require(
        set(state) == {"spec", "revision", "events", "items"}, "invalid state fields"
    )
    rebuilt = new_state(state["spec"])
    require(type(state["revision"]) is int, "invalid revision")
    require(isinstance(state["events"], list), "events must be a list")
    seen = set()
    for event in state["events"]:
        require(isinstance(event, dict), "invalid event")
        require(
            nonempty(event.get("event_id")) and event["event_id"] not in seen,
            "invalid or duplicate event ID",
        )
        seen.add(event["event_id"])
        require(event["revision"] == rebuilt["revision"] + 1, "event revision mismatch")
        previous = rebuilt["items"].get(event["item"], {})
        expected = previous.get("attempts", 0) + (event["action"] == "reserve")
        require(
            type(event["attempt"]) is int and event["attempt"] == expected,
            "attempt lineage mismatch",
        )
        apply_event(rebuilt, event)
        rebuilt["revision"] += 1
    require(
        state["revision"] == rebuilt["revision"] and state["items"] == rebuilt["items"],
        "state differs from event history",
    )


def record_event(state, revision, payload):
    validate_state(state)
    require(nonempty(payload.get("event_id")), "event ID required")
    for previous in state["events"]:
        if previous["event_id"] == payload["event_id"]:
            require(
                all(previous.get(k) == v for k, v in payload.items()),
                "event ID already used with different content",
            )
            return state
    require(state["revision"] == revision, "stale revision; inspect status and retry")
    require(payload["item"] in state["items"], "unknown item")
    updated = copy.deepcopy(state)
    event = dict(
        payload,
        revision=revision + 1,
        timestamp=datetime.now(timezone.utc).isoformat(),
        attempt=updated["items"][payload["item"]]["attempts"]
        + (payload["action"] == "reserve"),
    )
    apply_event(updated, event)
    updated["events"].append(event)
    updated["revision"] += 1
    validate_state(updated)
    return updated


def read_json(path):
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def save_locked(path, operation):
    """Serialize cooperative writers, retaining the previous state on failure."""
    path = path.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    lock = path.with_name(path.name + ".lock")
    descriptor = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    temporary = None
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump({"pid": os.getpid(), "hostname": socket.gethostname()}, stream)
        result = operation()
        with tempfile.NamedTemporaryFile(
            mode="w",
            dir=path.parent,
            prefix=path.name + ".",
            delete=False,
            encoding="utf-8",
        ) as stream:
            temporary = stream.name
            json.dump(result, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        temporary = None
        return result
    finally:
        if temporary is not None:
            Path(temporary).unlink(missing_ok=True)
        lock.unlink()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("init", "status", "record"):
        command = sub.add_parser(name)
        command.add_argument("--plan", required=True, type=Path)
        if name == "init":
            command.add_argument("--spec", required=True, type=Path)
        if name == "record":
            command.add_argument("--revision", type=int, required=True)
            command.add_argument("--event-id", required=True)
            command.add_argument("--item", required=True)
            command.add_argument(
                "--action",
                required=True,
                choices=["reserve", "bind", "return", "accept", "fail"],
            )
            for field in ("model", "run-id", "evidence", "note"):
                command.add_argument("--" + field, default="")
            command.add_argument("--run-resolved", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            spec = read_json(args.spec)

            def initialize():
                require(not args.plan.exists(), "plan already exists; use status")
                return new_state(spec)

            state = save_locked(args.plan, initialize)
        elif args.command == "record":
            payload = {
                key: getattr(args, key)
                for key in (
                    "event_id",
                    "item",
                    "action",
                    "model",
                    "run_id",
                    "evidence",
                    "note",
                    "run_resolved",
                )
            }
            state = save_locked(
                args.plan,
                lambda: record_event(read_json(args.plan), args.revision, payload),
            )
        else:
            state = read_json(args.plan)
            validate_state(state)
        print(json.dumps(status(state), indent=2, ensure_ascii=False))
        return 0
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(json.dumps({"error": str(error)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
