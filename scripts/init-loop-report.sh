#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATE="$SKILL_ROOT/assets/loop-report-template.json"
OUTPUT_PATH="${1:-./agent-loop-report.json}"

if [[ ! -f "$TEMPLATE" ]]; then
  echo "Report template not found: $TEMPLATE" >&2
  exit 1
fi

if [[ -e "$OUTPUT_PATH" ]]; then
  echo "Refusing to overwrite existing file: $OUTPUT_PATH" >&2
  exit 1
fi

cp "$TEMPLATE" "$OUTPUT_PATH"
"$SKILL_ROOT/scripts/validate-loop-report.py" --template "$OUTPUT_PATH"
echo "Created agent loop report: $OUTPUT_PATH"
