# Claude Code Basics and Core Operations

[< Back to Guide](../README.en.md)

---

## What is Claude Code?

Claude Code is an AI agent that lives in your terminal. It's not just a chatbot — it can **autonomously** execute:

- File reading, writing, and editing
- Command execution (building, testing, git operations, etc.)
- Web searches for latest information
- Understanding your entire project structure

```bash
# Launch
claude

# Basics: launch from your project directory
cd my-project && claude
```

---

## Permissions Modes and Approval (Important)

Claude Code performs operations that **affect your system**, like editing files and running commands. Being asked for approval before execution is a safety feature. **Don't approve everything carelessly.**

### Three Operation Modes

Press `Shift + Tab` to cycle through modes:

```
Normal Mode → Auto-Accept Mode → Plan Mode → Normal Mode → ...
```

| Mode | Display | Behavior | Safety |
|--------|------|------|--------|
| **Normal Mode** | (no indicator) | Requests approval each time before editing files or running commands | Most safe |
| **Auto-Accept** | `⏵⏵ accept edits on` | Auto-approves file edits. Bash commands still require confirmation | Medium |
| **Plan Mode** | `⏸ plan mode on` | Read-only. Makes no changes at all | Completely safe |

### Reading Approval Prompts

In normal mode, Claude shows a confirmation before acting:

```
Claude wants to edit src/app.ts
Allow? [y/n/a]

  y = Allow this time only
  n = Deny
  a = Allow all similar operations in this session
```

**Pay special attention with Bash commands**:

```
Claude wants to run: rm -rf dist/
Allow? [y/n/a]
```

**Always read the command before approving**. Check that it doesn't contain destructive operations like `rm`, `git push --force`, `DROP TABLE`, etc.

### Rules to Prevent Accidents

| Rule | Reason |
|--------|------|
| **Start in normal mode** | Until you're comfortable, verify what Claude is about to do each time |
| **Auto-Accept only for trusted tasks** | Use it for "write tests" or "refactor" — tasks with clear scope |
| **Always read Bash commands** | File deletion, package addition/removal, and git operations need extra care |
| **Use Plan Mode when unsure** | It's read-only, so nothing can break. Perfect for investigation and planning |
| **Don't use `--dangerously-skip-permissions`** | This bypasses all safety guards. Never use except in CI/CD |

### Real-World Accident Examples

```
❌ Auto-Accept mode with vague instruction "clean up the project"
   → Claude deletes files it deems unnecessary

❌ Approve Bash command without reading
   → git push --force overwrites teammates' changes

❌ Vague instruction "clean the environment"
   → node_modules/ deleted, but so is .env
```

> **Golden Rule: Claude is capable, but the final decision on destructive operations is always yours.**
> Approval prompts aren't annoying confirmations — they're your safety net.

---

## Basic Operations

### Frequently Used Commands

| Command | Description |
|----------|------|
| `/model` | Switch models |
| `/fast` | Fast Mode (faster output with the same model) |
| `/help` | Show help |
| `/clear` | Clear context |
| `/compact` | Summarize conversation to save context |
| `Esc` | Cancel the current task |

### How to Give Effective Instructions

```
❌ Bad: "Create a login feature"
✅ Good: "Create a login API with Express + JWT.
          POST /api/auth/login accepts email and password,
          returns a JWT token. Reference users table with Prisma"

❌ Bad: "Fix the bug"
✅ Good: "The getUser function in src/controllers/user.ts
          returns 500 error when a user isn't found.
          Change it to return 404 instead"
```

Key: **Be specific about what, where, and how.**
