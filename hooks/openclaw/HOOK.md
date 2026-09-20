---
name: agent-loop-engineering
description: Injects a bounded-loop safety reminder during OpenClaw agent bootstrap.
metadata: {"openclaw":{"emoji":"🔄","events":["agent:bootstrap"]}}
---

# Agent Loop Engineering Hook

Inject a concise reminder that autonomous work must have a bounded goal, verification signal, stop condition, record, and escalation path.

## Behavior

- Run on `agent:bootstrap`.
- Add one virtual reminder file to primary sessions.
- Skip subagent sessions to prevent recursive amplification.
- Avoid filesystem writes and network access.

## Enable

```bash
openclaw hooks enable agent-loop-engineering
```

## Test

```bash
node handler.test.js
```
