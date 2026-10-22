# Loop Decision Guide

## Contents

- Boundedness test
- Feedback test
- Risk and authority test
- Retry design
- Terminal decisions
- Scheduling requirements

## Boundedness Test

A loop is executable when all of the following are known:

- one finite work unit can be named
- acceptance criteria distinguish success from failure
- allowed actions and protected surfaces are clear
- required context is available or discoverable
- verification can produce a concrete signal
- a stop condition exists

If any missing answer could materially change the outcome, finish safe discovery and escalate with a review packet.

## Feedback Test

Good feedback is observable and tied to the goal: test status, build result, metric threshold, reconciliation count, screenshot comparison, queue state, or acceptance-criteria result.

Weak feedback includes "looks good," "make it great," or activity counts without outcome evidence. Convert weak feedback into criteria with a human checkpoint before automating repeated execution.

## Risk and Authority Test

Check whether the current request or established authority covers:

- destructive or irreversible actions
- external messages, purchases, publication, or deployment
- credential, permission, scheduler, or global configuration changes
- decisions based on taste, policy, business judgment, or product intent
- changes that weaken security, privacy, accessibility, or error handling

Complete reversible analysis and preparation first, then ask for the smallest necessary decision.

## Retry Design

Define the retry budget before automating retries. Each retry must have new evidence or a materially changed approach. Stop retrying when:

- the same failure repeats without a new hypothesis
- the next attempt needs broader permissions or scope
- the remaining uncertainty requires human judgment
- cost or time exceeds the declared budget
- verification signals degrade

Retries are attempts within one work unit. Recursion that creates new goals requires a new bounded invocation.

## Terminal Decisions

| Decision | Use when |
|---|---|
| `close` | Required acceptance criteria and verification pass. |
| `retry` | A bounded, authorized attempt with a new hypothesis is available; continue the same unit. |
| `escalate` | A human decision, authority grant, or missing material context is required. |
| `defer` | The work is valid but blocked by current constraints or timing. |
| `reject` | The action is unsafe, prohibited, or outside the permitted system. |

## Scheduling Requirements

Before creating a recurring job, establish authority and the following details:

- trigger and cadence
- queue source and item ownership
- per-run scope and concurrency
- resource and retry limits
- idempotency and duplicate handling
- credentials and permission boundaries
- logging and notification destination
- stop, disable, and rollback procedure
- human review cadence

Do not convert a one-time request into scheduled autonomy.
