#!/bin/bash
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

pip install -q -r "$CLAUDE_PROJECT_DIR/requirements.txt"

# Configure git auth using GH_PAT environment variable (set in Claude Code project settings)
if [ -n "${GH_PAT:-}" ]; then
  git -C "$CLAUDE_PROJECT_DIR" remote set-url origin \
    "https://dakaredriveuniraid-code:${GH_PAT}@github.com/dakaredriveuniraid-code/Investments.git"
fi

git -C "$CLAUDE_PROJECT_DIR" config user.email "djimagem@gmail.com"
git -C "$CLAUDE_PROJECT_DIR" config user.name "Djimagem Finance"
