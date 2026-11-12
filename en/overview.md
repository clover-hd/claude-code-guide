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

Claude Code performs operations that **affect your system**, like editing files and running commands. In manual mode it asks for approval before acting, and in auto mode a classifier blocks dangerous operations. Both are safety features. **Don't approve everything carelessly.**

### Operation Modes

Claude Code **starts in auto mode**. Each press of `Shift + Tab` cycles through the modes like this:

```
auto mode → manual mode → Auto-Accept → Plan Mode → auto mode → ...
```

| Mode | Display | Runs without asking | Good for |
|--------|------|------|--------|
| **auto mode** | `⏵⏵ auto mode on` | Almost everything. Instead, a separate model (the classifier) watches for dangerous operations and blocks them | Long tasks, or when you're tired of constant confirmations |
| **manual mode** | `⏸ manual mode on` | File reads only. Asks every time before editing or running commands | When you want to verify each step yourself, or for critical work |
| **Auto-Accept** | `⏵⏵ accept edits on` | Reads, file edits, and common file-operation commands (`mkdir`, `mv`, `cp`, `rm`, etc., only inside the working directory) | When you're fixing code while watching |
| **Plan Mode** | `⏸ plan mode on` | Reads and commands for investigating. Does not edit source | Investigating and planning before making changes |

- You can also enter Plan Mode directly with `/plan`
- There are also `dontAsk` (denies everything not explicitly allowed) for CI, and `bypassPermissions` (skips all confirmations), to be used only in isolated environments
- To start in manual mode, write `{"permissions": {"defaultMode": "manual"}}` in `~/.claude/settings.json`
- Claude Code starts in auto mode when auto mode is available on v2.1.283 or later (if it's disabled by your organization, for example, it starts in manual mode)

### Things to Watch for in Auto Mode

In auto mode, a classifier watches operations in place of a human and blocks dangerous ones (sending secret values outside, deleting unrelated locations, etc.). It's convenient with fewer confirmations, but it's important to **decide for yourself what should be stopped**.

- **Pushes to the current repository and Pull Request creation go through without confirmation** (including pushes to the default branch). If you always want confirmation before a push, add it to `permissions.ask` ([Security Basics](security.md#require-confirmation-before-push-and-pull-requests))
- If you tell it "don't push" in the conversation, the classifier will respect that, but it can disappear when the conversation is compacted. Put anything that must hold into settings
- Rules in `permissions.ask` and hooks that explicitly ask for confirmation always prompt, even in auto mode

### Reading Approval Prompts

For operations that need confirmation, options like these are shown:

```
Bash command
  npm test
  Do you want to proceed?
  ❯ 1. Yes
    2. Yes, and don't ask again for: npm test *
    3. Yes, and switch to auto mode
    4. No
```

| Option | Meaning |
|---|---|
| **Yes** | Allow this time only |
| **Yes, and don't ask again** | Stop asking for the same kind of operation. For Bash commands this is saved to `.claude/settings.local.json`, so it goes through without confirmation **in future sessions too** |
| **Yes, and switch to auto mode** | Allow and switch to auto mode (sometimes not shown) |
| **No** | Deny |

**Always read the command before approving**. Check that it doesn't contain destructive operations like `rm`, `git push --force`, `DROP TABLE`, etc. "Don't ask again" is saved and persists, so also check that you aren't allowing an overly broad pattern.

### Rules to Prevent Accidents

| Rule | Reason |
|--------|------|
| **Use manual mode too until you're comfortable** | Seeing what Claude is about to do each time helps you grasp what kinds of operations it performs |
| **Write operations you want stopped into settings** | Put push, production deploys, etc. in `permissions.ask`. A request in conversation can disappear |
| **Always read Bash command confirmations** | File deletion, package addition/removal, and git operations need extra care |
| **Use Plan Mode when unsure** | It doesn't edit source, so it's perfect for investigation and planning |
| **Don't use `--dangerously-skip-permissions`** | This bypasses all safety guards. Don't use it except in isolated containers or VMs |

### Real-World Accident Examples

```
❌ auto mode or Auto-Accept with vague instruction "clean up the project"
   → Claude deletes files it deems unnecessary

❌ Approve Bash command without reading
   → git push --force overwrites teammates' changes

❌ Vague instruction "clean the environment"
   → node_modules/ deleted, but so is .env
```

> **Golden Rule: Claude is capable, but the final decision on destructive operations is always yours.**
> Approval confirmations and `permissions.ask` settings aren't annoying confirmations — they're your safety net. When using auto mode, especially, write the operations you want stopped into settings.

---

## Basic Operations

### Frequently Used Commands

| Command | Description |
|----------|------|
| `/model` | Switch models |
| `/fast` | Fast Mode (faster output on Opus and Fable. Higher cost; on subscription plans it's deducted from usage credits) |
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
