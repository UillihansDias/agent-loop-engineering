# OpenClaw Integration

## Contents

- Install the skill
- Use the skill
- Enable the optional hook
- Verify the hook
- Disable or remove
- Safety notes

## Install the Skill

Copy the folder into the OpenClaw workspace skills directory:

```bash
cp -R agent-loop-engineering ~/.openclaw/workspace/skills/
```

Restart or reload OpenClaw so it discovers `SKILL.md`.

## Use the Skill

Invoke `agent-loop-engineering` for bounded autonomous work, queues, retries, verification loops, stop-rule design, or escalation packets. The skill itself does not create schedules or persistent jobs.

## Enable the Optional Hook

The bundled bootstrap hook injects a short loop-safety reminder into primary agent sessions. It skips subagent sessions to avoid reminder amplification.

```bash
cp -R hooks/openclaw ~/.openclaw/hooks/agent-loop-engineering
openclaw hooks enable agent-loop-engineering
```

The hook is optional. Enable it only when a persistent reminder is desirable.

## Verify the Hook

Start a new primary agent session and inspect its bootstrap context for `AGENT_LOOP_ENGINEERING_REMINDER.md`. Start a subagent session and confirm the reminder is absent.

## Disable or Remove

```bash
openclaw hooks disable agent-loop-engineering
rm -rf ~/.openclaw/hooks/agent-loop-engineering
```

Remove the copied skill folder separately if it is no longer needed.

## Safety Notes

- The hook only adds virtual bootstrap context; it does not write files or use the network.
- Installing the skill does not authorize scheduling, external side effects, or expanded permissions.
- Keep report artifacts free of credentials and unnecessary raw command output.
