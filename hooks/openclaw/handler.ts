/** Inject a bounded-loop reminder during OpenClaw bootstrap. */

import type { HookHandler } from 'openclaw/hooks';

const REMINDER_NAME = 'AGENT_LOOP_ENGINEERING_REMINDER.md';
const REMINDER_PATH = REMINDER_NAME;
const REMINDER_CONTENT = `## Agent Loop Engineering Reminder

For autonomous or repeated work:
- Define one bounded goal, acceptance criteria, scope, verification signal, budget, and stop condition.
- Treat work as finite queue items; finish one unit cleanly.
- Do not guess through product, security, business, taste, or authority decisions.
- Retry only with new evidence or a materially changed approach.
- Verify with a concrete signal before claiming success.
- Record the outcome and choose close, retry, escalate, defer, or reject.
- Do not create schedules, persistence, or broader permissions without explicit approval.`;

function isObject(value: unknown): value is Record<string, unknown> {
  return Boolean(value) && typeof value === 'object';
}

function isOurReminder(value: unknown): boolean {
  if (!isObject(value) || value.path !== REMINDER_PATH) return false;
  return value.content === REMINDER_CONTENT || (
    value.name === REMINDER_NAME && value.virtual === true
  );
}

const handler: HookHandler = async (event) => {
  if (!isObject(event) || event.type !== 'agent' || event.action !== 'bootstrap') return;
  if (!isObject(event.context)) return;
  if (String(event.sessionKey || '').includes(':subagent:')) return;
  if (!Array.isArray(event.context.bootstrapFiles)) return;

  const occupied = event.context.bootstrapFiles.some(
    (file) => isObject(file) && file.path === REMINDER_PATH && !isOurReminder(file),
  );
  if (occupied) return;

  const files = event.context.bootstrapFiles.filter(
    (file, index, all) => !isOurReminder(file) || all.findIndex(isOurReminder) === index,
  );
  const reminder = {
    name: REMINDER_NAME,
    path: REMINDER_PATH,
    content: REMINDER_CONTENT,
    missing: false,
    virtual: true,
  };
  const index = files.findIndex(isOurReminder);
  if (index === -1) files.push(reminder);
  else files[index] = reminder;
  event.context.bootstrapFiles = files;
};

export default handler;
