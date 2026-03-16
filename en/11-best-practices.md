# Practical Know-How

[< Back to Guide](README.en.md)

---

## 1. Always Provide Validation Methods (Most Important)

**The official team states this is "the highest-leverage practice"**. Claude's output quality improves dramatically when it can validate its own work.

```
❌ "Implement an email authentication function"
✅ "Implement an email authentication function.
    Test cases: user@example.com → true, invalid → false, user@.com → false
    Run tests after implementation to confirm"
```

| Method | How |
|------|--------|
| **Test-driven** | Have it write tests first, then implement code to pass them |
| **Screenshots** | For UI changes, say "take a screenshot and compare with the original" |
| **Build verification** | Say "verify the build passes after implementation" |
| **Linter** | Say "verify eslint passes" |

Without validation methods, Claude might produce "code that looks right but doesn't work."

---

## 2. Manage Your Context Window

**Claude Code's performance is directly tied to how full your context window is.** This is your most important resource.

### What is Context?

Your conversations with Claude, files read, command output...everything accumulates in the context window. As it fills up, Claude's accuracy begins to decline.

### Management Rules

| Command | Timing | Effect |
|----------|-----------|------|
| `/clear` | **When switching to unrelated tasks** | Completely reset context |
| `/compact` | **Around 70% context fill** | Summarize and compress conversation (CLAUDE.md is re-read) |
| `/compact Focusing on API changes` | When you want to retain specific topics | Control summary content with instructions |
| `Esc + Esc` → "Summarize from here" | When you want to summarize from a point | Compress only from selection onward |

> **Tip**: If you set up [the status line](18-statusline.md), remaining context is always displayed, so you won't miss the right time for `/compact`.

### Common Mistakes

```
❌ Mixed-up session
   Task A → Unrelated question → Back to Task A → Context wasted and full

✅ Reset per task
   Task A → /clear → Task B → /clear → Task C
```

### Protect Context with Sub-agents

Delegating investigation work to a sub-agent prevents large file reads from polluting your main context.

```
You: Use a sub-agent to investigate token refresh mechanisms in the
     authentication system and whether existing OAuth utilities exist

Claude: (Sub-agent investigates in separate context → reports only results)
```

---

## 3. Auto-generate CLAUDE.md with `/init`

For new projects, running `/init` has Claude analyze the codebase and **auto-generate CLAUDE.md**.

```bash
cd my-project
claude
> /init
```

It detects the build system, test framework, and code conventions to create a foundation. Then manually refine it from there.

---

## 4. Keep CLAUDE.md Short and Specific

CLAUDE.md should target **200 lines or less**. If it's too long, important rules get buried and Claude starts ignoring them.

| Should write | Should NOT write |
|-------------|-------------|
| Commands Claude can't infer | Things obvious from reading code |
| Code style different from default | Standard language conventions |
| How to run tests | Detailed API documentation (links are enough) |
| Branch naming rules, PR conventions | Frequently changing information |
| Project-specific architecture decisions | Self-evident instructions like "write clean code" |

**When Claude doesn't follow instructions**: Often caused by CLAUDE.md being too long. Review periodically and cut unnecessary lines.

---

## 5. Master Session Management

| Operation | Command | Purpose |
|------|----------|------|
| **Resume session** | `claude --continue` | Continue from previous session |
| **Select session** | `claude --resume` | Choose from past sessions list |
| **Rename session** | `/rename oauth-migration` | Give descriptive name for later |
| **Rewind** | `Esc + Esc` or `/rewind` | Restore code and conversation to any point |

> **Tip**: Treat sessions like git branches. Maintaining separate sessions per work stream keeps contexts from mixing.

---

## 6. Be Specific in Instructions: "What, Where, How"

```
❌ "Fix the bug"
✅ "In src/controllers/user.ts, the getUser function returns a 500 error
    when user is not found. Fix it to return 404 instead"

❌ "Add a calendar widget"
✅ "On the homepage, create a new calendar widget following the existing
    widget pattern (reference HotDogWidget.php), with month selection
    and pagination"
```

**Reference files directly with `@`**:

```
@src/auth/login.ts - explain the session management mechanism
```

---

## 7. Have Claude Interview You

When building large features, you'll always miss considerations. **Having Claude ask you questions** is highly effective.

```
You: I want to build a chat feature. Interview me in detail.
     Cover technical implementation, UI/UX, edge cases, and tradeoffs.
     Deep-dive into difficult parts I might miss. Once we've covered
     everything, write the spec to SPEC.md.

Claude: I'd like to ask some questions.
        1. How real-time does this need to be? (instant vs. few-second delay OK?)
        2. Message persistence? (how long to keep history?)
        3. File attachments needed?
        4. Group chat support?
        ...
```

Once the spec is done, **start implementation in a new session** for a clean context to focus.

---

## 8. Leverage Rewind

All of Claude's actions are recorded as **checkpoints**. Use `Esc + Esc` or `/rewind` to return to any point.

```
Restore conversation    → Rewind conversation only
Restore code           → Rewind file changes only
Restore both           → Rewind both conversation and code
```

Since you can rewind, you can freely try risky implementations. Checkpoints persist across sessions.

> **Note**: Checkpoints only track changes made by Claude Code. They don't replace git.

---

## 9. Avoid Common Anti-patterns

| Anti-pattern | Symptom | Solution |
|---------------|------|------|
| **Mixed-up session** | Running unrelated tasks one after another in one session | Use `/clear` to reset per task |
| **Fix loop** | Same problem needs fixing 2+ times despite instructions | `/clear` and restart with better initial prompt including what you learned |
| **Bloated CLAUDE.md** | Claude not following rules | Reduce to 200 lines. Don't write what Claude can figure out |
| **Unvalidated trust** | Looks like it works but actually missing edge cases | Always require validation: tests, builds, linters, etc. |
| **Endless investigation** | Vague "research" requests lead to reading tons of files | Narrow scope or delegate to sub-agent |

---

## 10. Leverage Auto Memory

Claude **automatically saves notes** from conversations. They persist across sessions, so you don't need to repeat yourself.

```
You: Use pnpm for this project, not npm.
Claude: Understood. (Automatically saved to memory)

# Next session
You: Add a package
Claude: (Reads pnpm from memory)
        pnpm add ...
```

| Command | Description |
|----------|------|
| `/memory` | Display/edit current memory files |
| "Remember this" | Explicitly have Claude save to memory |
| "Forget" | Have Claude delete from memory |

Memory is stored as plaintext in `~/.claude/projects/<project>/memory/`, so you can edit or delete anytime.

---

## 11. Project Configuration is Something You "Grow"

CLAUDE.md, agents, skills, and hooks are **not a one-time creation**.

```
Use → Claude makes mistake → Add/fix rule → Accuracy improves
                                  ↑
                           Grows through iteration
```

Commit CLAUDE.md to git and edit collaboratively with your team. Value grows exponentially over time.

---

## 12. Other Helpful Features

| Feature | Description |
|------|------|
| **`/fast`** | Faster output with same model. For simple tasks |
| **`claude -p "prompt"`** | Non-interactive mode. Call Claude Code from CI/scripts |
| **Paste images** | Paste screenshots or designs directly and say "implement this" |
| **Pipe input** | `cat error.log \| claude` to pass logs directly |
| **Parallel sessions** | Run Claude Code simultaneously in multiple terminals. Writer/Reviewer pattern is powerful |
