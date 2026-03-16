# Project Configuration with CLAUDE.md and Hooks

[< Back to Guide](README.en.md)

---

## What is CLAUDE.md?

When you place `CLAUDE.md` in the project root, Claude Code **automatically reads it every time** as project-specific instructions.

## What to Write

```markdown
# CLAUDE.md

## Project Overview
- This project is for ○○
- Tech stack: React, Express, MySQL

## Important Rules
- Always run backend commands inside Docker
- Tests must pass before committing

## Directory Structure
- src/domain/ - Domain logic
- src/interface/ - API endpoints

## Coding Standards
- Variable names in camelCase
- Function names start with a verb
```

## Hierarchical Structure

CLAUDE.md can be placed in a directory hierarchy. You can place CLAUDE.md in subdirectories as well.

```
my-project/
├── CLAUDE.md                 ← Rules for entire project
├── frontend/
│   └── CLAUDE.md             ← Frontend-specific rules
└── backend/
    └── CLAUDE.md             ← Backend-specific rules
```

---

## Hooks (Automation)

### What are Hooks?

A mechanism that **automatically executes shell commands** before and after tool execution.

### Example: Hooks Configuration

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write \"$CLAUDE_TOOL_INPUT_FILE_PATH\""
          }
        ]
      }
    ]
  }
}
```

With this configuration, **Prettier automatically formats files every time Claude edits them**. No manual formatting work needed.
