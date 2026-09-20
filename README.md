# Agent Loop Engineering Skill

An OpenClaw agent skill to run disciplined, bounded operational loops for autonomous systems, background tasks, queues, retries, and remediation workflows.

Turns open-ended "keep going" or "handle this queue" tasks into discrete, finite, reviewable units with explicit stop conditions, escalation boundaries, and verified outcomes.

---

## Core Purpose

- **Prevent Runaway Loops**: Constrain automated iterations with hard step budgets, circuit breakers, and explicit stop triggers.
- **Reviewable Work Units**: Complete one coherent task slice at a time with observable runtime evidence.
- **Disciplined Recovery**: Inspect failures before retrying; eliminate identical repeat attempts or blind brute-forcing.
- **Escalate Deliberately**: Halt and ask the operator when reaching product, security, or authorization boundaries.

---

## Directory Structure

```text
agent-loop-engineering/
├── README.md                              # Repository overview and operational guide
├── SKILL.md                               # Canonical skill specification and loop rules
├── agents/
│   └── openai.yaml                        # Agent manifest
├── assets/
│   ├── loop-report-template.json          # Machine-readable loop state & telemetry template
│   ├── example-github-queue-report.json   # Worked queue execution report
│   └── review-packet.md                   # Operator review & handoff artifact
├── hooks/
│   └── openclaw/
│       ├── HOOK.md                        # Hook trigger specifications
│       ├── handler.ts                     # TypeScript hook logic
│       ├── handler.js                     # Compiled runtime hook
│       └── handler.test.js                # Hook unit tests
├── references/
│   ├── decision-guide.md                  # Loop vs. one-shot classification & failure criteria
│   ├── examples.md                        # Queue processing, retry, and issue triage patterns
│   └── openclaw-integration.md            # OpenClaw event and runtime integration
└── scripts/
    ├── init-loop-report.sh                # Initialize a structured loop report
    └── validate-loop-report.py            # Validate report schema and completion invariants
```

---

## Tooling & Verification

```bash
# Initialize a loop tracking report
bash scripts/init-loop-report.sh /path/to/loop-report.json

# Validate that the loop report satisfies schema and termination invariants
python3 scripts/validate-loop-report.py /path/to/loop-report.json
```

---

## Operating Invariants

1. **One Slice at a Time**: Never attempt an unbounded sequence without recording evidence for each completed unit.
2. **Runtime Verification**: Every loop completion requires runtime observation (tests, CLI exits, API responses)—never plausible output alone.
3. **Fail Fast on Repeat Failures**: If a step fails twice without changing environmental conditions, escalate rather than retry.
4. **Preserve State**: Persist reviewable artifacts (`assets/review-packet.md`) before yielding or terminating.

---

## Installation in OpenClaw

```bash
openclaw skills install ./agent-loop-engineering --as agent-loop-engineering
```

Skill entry point: [`SKILL.md`](SKILL.md).
