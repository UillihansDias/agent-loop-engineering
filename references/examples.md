# Examples and Edge Cases

## Contents

- CI failure
- Issue queue
- Vague product request
- Recurring inbox processing
- Repeated failure
- Harness improvement

## CI Failure

Request: "Fix CI and keep trying until it passes."

Bound the unit to the current failing revision. Inspect the failure, identify acceptance criteria, make the smallest authorized fix, run targeted checks, then run the relevant CI-equivalent check. Retry only with a new hypothesis. Close when checks pass; escalate if the fix changes public behavior or needs unavailable secrets.

## Issue Queue

Request: "Work through these bugs."

Treat each issue as a separate unit. Classify, scope, implement, verify, and close or escalate it before selecting the next. Do not leave several partially modified issues in one unreviewable change.

## Vague Product Request

Request: "Keep improving the onboarding flow until it is excellent."

Do not start an open-ended build loop. Gather existing goals and evidence, prepare bounded candidate outcomes, and request product criteria or a checkpoint. Taste and product intent require human judgment.

## Recurring Inbox Processing

Request: "Handle this inbox every day."

Define message classes, allowed responses, prohibited topics, deduplication, logging, scheduling, failure notifications, and escalation rules before enabling recurrence. Drafting may be safe while sending requires separate authority.

## Repeated Failure

Condition: the same test fails after two revisions with no new diagnostic evidence.

Stop retrying. Record both attempts, the common failure, remaining hypotheses, and the exact missing context or decision. Choose `escalate` or `defer` rather than looping.

## Harness Improvement

Condition: a regression escaped because no test covered a stable requirement.

Fix the bounded task first. Then propose or add the smallest regression test within scope. Record the harness change separately and verify that it fails on the old behavior and passes on the corrected behavior when practical.

## GitHub Issue Queue

Request: "Work through these 12 GitHub bugs."

Order confirmed regressions and security-impacting defects before cosmetic issues, then respect explicit priority labels and dependencies. Treat each issue as its own work unit: reproduce, scope, patch, test, and choose a terminal decision before selecting the next issue. Avoid mixing unrelated fixes in one branch or pull request.

Reading issues and preparing local patches are normally reversible. Posting comments, opening or merging pull requests, changing labels, closing issues, or triggering deployments are external actions and require the authority established for the run. Escalate when acceptance criteria are unclear, reproduction needs unavailable access, or a fix changes public behavior.

See `../assets/example-github-queue-report.json` for a canonical completed report covering one issue from such a queue.
