# Project Configuration with CLAUDE.md and Hooks

[< Back to Guide](../README.en.md)

---

## What is CLAUDE.md?

When you place `CLAUDE.md` in the project root, Claude Code **automatically reads it every time** as project-specific instructions.

## What to Write

We recommend keeping CLAUDE.md to **an index and a few rules**. Put the substance of requirements and specs in `docs/`, and each agent's workflow in its definition file under `.claude/agents/`; CLAUDE.md just links to them.

```markdown
# Restaurant Reservation Platform

Manages reservations and reviews for independent restaurants.

- Requirements and principles to keep: docs/requirements.md (always read before working)
- Base spec: docs/spec.md
- Implementation policy (which way to lean when in doubt): docs/implementation-policy.md
- Why we decided it: docs/decisions/
- Documentation policy: docs/README.md

## Common Commands
- Type check: `npm run typecheck`
- Tests: `npm test`
- Dev server: `npm run dev`

## Rules
- The source is the source of truth for detailed design. If docs and source disagree, trust the source
- Always run backend commands inside Docker
- Never commit secrets (the pre-commit hook blocks them; don't skip the hook)
- Work on develop. Keep main always working
- Each agent's role and workflow are in its definition file under .claude/agents/
```

> **Why keep it short?**
> CLAUDE.md is loaded into every conversation and every sub-agent. The longer it gets, the more likely its rules are ignored. Procedures like "run tests and review before committing" only need to live in the definition file of the agent that performs them. You also don't need to write things that are clear from reading the code (like naming conventions, which a formatter or linter can enforce).

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

A mechanism that **automatically executes shell commands** before and after tool execution. Configure them in `.claude/settings.json`.

The tool's input is passed to the hook command as **JSON on standard input** (e.g., the edited file's path is `tool_input.file_path`, and a Bash command is `tool_input.command`).

### Example 1: Auto-format edited files (PostToolUse)

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
          }
        ]
      }
    ]
  }
}
```

With this configuration, **Prettier automatically formats files every time Claude edits or creates them**. No manual formatting work needed (requires `jq`).

### Example 2: Block or ask for confirmation on dangerous commands (PreToolUse)

A `PreToolUse` hook runs **before** a tool executes, and can block the execution or insert a human confirmation.

| What you want | How the hook responds |
|---|---|
| Block (deny) | Exit with code **2** and write the reason to standard error. The reason is passed to Claude |
| Ask a human to confirm (ask) | Write the following JSON to standard output and exit with code 0 |
| Let it through | Write nothing and exit with code 0 |

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "ask",
    "permissionDecisionReason": "This command applies a migration to the production DB."
  }
}
```

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "node \"$CLAUDE_PROJECT_DIR/.claude/hooks/guard-bash.mjs\""
          }
        ]
      }
    ]
  }
}
```

For example, you can "block `git commit --no-verify`" or "ask for confirmation before migrating production". For an example that checks for secrets before committing, see [Security Basics](security.md#commit-guard--stop-secrets-mechanically).

> **How this differs from writing it in CLAUDE.md**: A "don't do X" in CLAUDE.md is a request that Claude tries to follow. Hooks run **mechanically, every time**. Use hooks to block anything that must never happen.
