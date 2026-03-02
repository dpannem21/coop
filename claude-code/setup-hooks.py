#!/usr/bin/env python3
import json
import os

settings_path = "/root/.claude/settings.json"

new_hook = {
    "matcher": "Read|WebFetch|Bash|Grep|Task",
    "hooks": [{
        "type": "command",
        "command": "uv run .claude/hooks/prompt-injection-defender/post-tool-defender.py"
    }]
}

# load existing settings or start fresh
if os.path.exists(settings_path):
    with open(settings_path) as f:
        settings = json.load(f)
else:
    settings = {}

# safely navigate the nested structure
settings.setdefault("hooks", {})
settings["hooks"].setdefault("PostToolUse", [])

# avoid adding duplicate hooks
if new_hook not in settings["hooks"]["PostToolUse"]:
    settings["hooks"]["PostToolUse"].append(new_hook)

with open(settings_path, "w") as f:
    json.dump(settings, f, indent=2)

print("✓ Prompt injection defender hook installed")