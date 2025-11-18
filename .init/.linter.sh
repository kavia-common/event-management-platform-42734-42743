#!/bin/bash
cd /home/kavia/workspace/code-generation/event-management-platform-42734-42743/event_management_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

