#!/usr/bin/env python3
"""Validate an Agent Loop Engineering JSON report."""

import json
import sys
from pathlib import Path


TOP_LEVEL = {
    "trigger": str,
    "goal": dict,
    "context": dict,
    "execution": dict,
    "verification": dict,
    "decision": dict,
    "human_checkpoint": dict,
    "harness_improvements": list,
    "uncertainties": list,
}

SECTIONS = {
    "goal": {
        "objective": str,
        "acceptance_criteria": list,
        "in_scope": list,
        "out_of_scope": list,
        "constraints": list,
    },
    "context": {
        "sources_consulted": list,
        "assumptions": list,
        "authority_limits": list,
    },
    "execution": {
        "work_unit": str,
        "actions_completed": list,
        "changes_made": list,
        "failed_attempts": list,
        "retry_budget": str,
    },
    "verification": {"status": str, "checks": list},
    "decision": {
        "outcome": str,
        "reason": str,
        "stop_condition_met": str,
        "next_action": str,
    },
    "human_checkpoint": {
        "required": bool,
        "decision_needed": str,
        "risks": list,
        "recommendation": str,
    },
}

OUTCOMES = {"close", "retry", "escalate", "defer", "reject"}
VERIFICATION_STATUSES = {"pass", "fail", "partial", "not_run"}
CHECK_STATUSES = {"pass", "fail", "not_run"}


def fail(message: str) -> None:
    print(f"INVALID: {message}", file=sys.stderr)
    raise SystemExit(1)


def require_fields(data: dict, fields: dict, prefix: str = "") -> None:
    for key, expected_type in fields.items():
        label = f"{prefix}.{key}" if prefix else key
        if key not in data:
            fail(f"missing field: {label}")
        if not isinstance(data[key], expected_type):
            fail(f"{label} must be {expected_type.__name__}")


def require_text(value: str, label: str) -> None:
    if not value.strip():
        fail(f"{label} must not be empty in a completed report")


def parse_args() -> tuple[Path, bool]:
    if len(sys.argv) == 2:
        return Path(sys.argv[1]), False
    if len(sys.argv) == 3 and sys.argv[1] == "--template":
        return Path(sys.argv[2]), True
    fail("usage: validate-loop-report.py [--template] <report.json>")


def main() -> None:
    path, template_mode = parse_args()
    if not path.is_file():
        fail(f"file does not exist: {path}")

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"cannot read valid UTF-8 JSON: {exc}")

    if not isinstance(data, dict):
        fail("report root must be an object")

    require_fields(data, TOP_LEVEL)
    for section, fields in SECTIONS.items():
        require_fields(data[section], fields, section)

    verification = data["verification"]
    decision = data["decision"]
    checkpoint = data["human_checkpoint"]

    if verification["status"] not in VERIFICATION_STATUSES:
        fail("verification.status must be pass, fail, partial, or not_run")
    if decision["outcome"] not in OUTCOMES:
        fail("decision.outcome must be close, retry, escalate, defer, or reject")

    for index, check in enumerate(verification["checks"]):
        if not isinstance(check, dict):
            fail(f"verification.checks[{index}] must be an object")
        prefix = f"verification.checks[{index}]"
        require_fields(check, {"name": str, "status": str, "evidence": str}, prefix)
        if check["status"] not in CHECK_STATUSES:
            fail(f"{prefix}.status must be pass, fail, or not_run")
        if not template_mode:
            require_text(check["name"], f"{prefix}.name")
            if check["status"] != "not_run":
                require_text(check["evidence"], f"{prefix}.evidence")

    if template_mode:
        print("VALID: agent loop report template schema passed")
        return

    require_text(data["goal"]["objective"], "goal.objective")
    require_text(data["execution"]["work_unit"], "execution.work_unit")
    require_text(decision["reason"], "decision.reason")
    require_text(decision["stop_condition_met"], "decision.stop_condition_met")

    checks = verification["checks"]
    if verification["status"] != "not_run" and not checks:
        fail("verification.checks must contain at least one check unless status is not_run")
    if verification["status"] == "pass" and any(check["status"] != "pass" for check in checks):
        fail("verification.status pass requires every check to pass")
    if verification["status"] == "pass" and not checks:
        fail("verification.status pass requires at least one check")
    if decision["outcome"] == "close" and verification["status"] != "pass":
        fail("decision.outcome close requires verification.status pass")
    if checkpoint["required"]:
        require_text(checkpoint["decision_needed"], "human_checkpoint.decision_needed")
        if decision["outcome"] not in {"escalate", "defer"}:
            fail("a required human checkpoint requires decision.outcome escalate or defer")

    print("VALID: completed agent loop report passed")


if __name__ == "__main__":
    main()
