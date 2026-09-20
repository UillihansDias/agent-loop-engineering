'use strict';

const assert = require('node:assert/strict');
const handler = require('./handler.js');

const REMINDER_NAME = 'AGENT_LOOP_ENGINEERING_REMINDER.md';

function event(sessionKey = 'main', bootstrapFiles = []) {
  return {
    type: 'agent',
    action: 'bootstrap',
    sessionKey,
    context: { bootstrapFiles },
  };
}

async function run() {
  const primary = event();
  await handler(primary);
  assert.equal(primary.context.bootstrapFiles.length, 1, 'injects one reminder');
  assert.equal(primary.context.bootstrapFiles[0].name, REMINDER_NAME);
  assert.equal(primary.context.bootstrapFiles[0].virtual, true);

  const subagent = event('agent:main:subagent:review');
  await handler(subagent);
  assert.deepEqual(subagent.context.bootstrapFiles, [], 'skips subagent sessions');

  const stale = {
    name: REMINDER_NAME,
    path: REMINDER_NAME,
    content: 'stale reminder',
    missing: false,
    virtual: true,
  };
  const duplicates = event('main', [stale, { ...stale }]);
  await handler(duplicates);
  assert.equal(duplicates.context.bootstrapFiles.length, 1, 'deduplicates stale reminders');
  assert.notEqual(duplicates.context.bootstrapFiles[0].content, stale.content, 'refreshes stale content');

  const collision = {
    name: 'UNRELATED_FILE.md',
    path: REMINDER_NAME,
    content: 'owned by another hook',
    missing: false,
    virtual: true,
  };
  const occupied = event('main', [collision]);
  await handler(occupied);
  assert.deepEqual(occupied.context.bootstrapFiles, [collision], 'does not overwrite a path collision');

  for (const malformed of [null, undefined, {}, { type: 'agent' }, { type: 'agent', action: 'bootstrap' }]) {
    await handler(malformed);
  }

  console.log('PASS: OpenClaw hook behavior');
}

run().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
