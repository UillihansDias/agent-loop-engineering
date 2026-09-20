---
name: agent-loop-engineering
description: Run disciplined, bounded operational loops for agents and automations. Use when a request involves autonomous or repeated execution, queued work, retries, background tasks, issue or alert handling, CI remediation, inbox processing, verification-driven iteration, human checkpoints, stop conditions, escalation, or outcome recording. Apply it to turn "keep going" or "handle these items" into finite, reviewable units without guessing through product, security, business, or taste decisions.
---

# Agent Loop Engineering

## Objective

Operate as a reliable worker inside a bounded system. Complete one reviewable unit at a time, verify it with concrete evidence, record the outcome, and stop or escalate deliberately.

## Load Supporting Resources

- Read `references/decision-guide.md` before designing an automated, recurring, or high-risk loop.
- Read `references/examples.md` when mapping vague requests, queues, retries, or human checkpoints into a bounded run.
- Use `assets/loop-report-template.json` for a machine-readable run record and validate it with `scripts/validate-loop-report.py`.
- Read `assets/example-github-queue-report.json` when a canonical completed report is useful.
- Use `assets/review-packet.md` when the result needs a human decision.
- Read `references/openclaw-integration.md` only when installing or enabling the optional OpenClaw hook.

## Run the Loop

### 1. Establish the Envelope

Identify before acting:

- trigger or queue item
- bounded goal and acceptance criteria
- in-scope and out-of-scope surfaces
- required context and authoritative sources
- permissions, risk, and rollback needs
- verification signals
- retry or resource budget
- stop and escalation conditions

Gather only context that can affect the current unit. Check indirect consumers and lifecycle-sensitive behavior before changing code or automation.

If the goal, authority, or verification signal is materially ambiguous, prepare a human checkpoint instead of guessing.

### 2. Select One Work Unit

Treat incoming work as a queue. Classify and scope one item, then finish it cleanly before selecting another.

Do not turn a queue into infinite recursion. Additional work remaining is not a reason to keep the current unit open.

### 3. Plan and Execute

Break the unit into the smallest useful parts. Prefer removing redundant work and failure paths over adding machinery. Preserve public behavior, security boundaries, accessibility, determinism, state propagation, and error semantics unless the user explicitly authorizes a change.

Keep actions within the established envelope. Do not broaden permissions because the loop is autonomous.

### 4. Critique and Revise

Compare the result with the goal, acceptance criteria, constraints, and likely failure modes. Revise only while attempts are producing meaningful progress and remain within budget.

Do not hide failed attempts. Record relevant failure evidence without copying secrets or unnecessary raw output.

### 5. Verify

Use a concrete signal such as:

- tests, lint, typecheck, build, or CI status
- logs, traces, metrics, or benchmark results
- screenshot or source comparison
- reconciliation counts or queue state
- explicit acceptance-criteria review

Never infer success solely from having performed the action. Label unrun or incomplete verification clearly.

### 6. Decide and Record

Choose exactly one terminal decision:

- `close`: goal achieved and required verification passed
- `retry`: a bounded next attempt is likely to improve the result
- `escalate`: human judgment, authority, or missing context is required
- `defer`: the unit is valid but cannot proceed within the current constraints
- `reject`: the requested action is unsafe or outside authority

Record what was requested, found, changed, verified, failed, assumed, and left uncertain. Return the delivered result rather than a transcript of internal iteration.

## Human Checkpoints

Escalate for product intent, business judgment, security risk, user preference, destructive action, unclear requirements with materially different outcomes, or any authority expansion.

Return a useful review packet containing:

1. requested outcome
2. findings and completed work
3. verification evidence
4. risks and assumptions
5. exact decision needed
6. recommended next action

Move the checkpoint as late as safely possible, after completing all reversible, unambiguous work.

## Self-Improvement

When a failure reveals a recurring system weakness, propose the smallest reversible harness improvement:

- add a regression test for an escaped bug
- add a checklist for a missed review condition
- add observability for an invisible failure
- add a guardrail for a risky action
- add or revise a skill for a repeated workflow
- retain memory only for durable, future-useful facts

Do not modify global prompts, credentials, memory, scheduler state, or runtime configuration without explicit approval. Do not schedule recurring execution merely because one run succeeded.

## Mandatory Stop Rules

Stop when the goal is achieved and verification passes, the budget is reached, the task becomes unbounded, context is insufficient, risk exceeds authority, attempts stop improving the result, or human judgment is required.

A clear stopped-loop report is a valid outcome. Never claim completion, permanent improvement, or successful verification without evidence.

## Output Contract

Return:

1. goal and work unit
2. completed actions or delivered artifact
3. verification evidence and status
4. terminal decision
5. risks, assumptions, and uncertainties
6. human decision or next action, only when needed
