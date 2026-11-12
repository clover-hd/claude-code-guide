# Troubleshooting / FAQ

[< Back to Guide](../README.en.md)

---

## Common Issues and Solutions

### Installation & Startup

#### Claude Code won't start

```bash
# First, check version
claude --version

# If there's an issue, use the diagnostic command
claude doctor

# Reinstall
curl -fsSL https://claude.ai/install.sh | bash
```

#### "Please log in" message

On first startup, you need to log in to your Anthropic account using a browser. If the browser doesn't open automatically, copy and paste the displayed URL into your browser manually.

#### Browser won't open in WSL

In WSL environments, the browser may not open automatically. Copy the displayed URL and paste it into your browser on Windows to log in.

---

### Rate Limiting (Overuse)

#### "Usage limit reached" appears

You've reached your plan's usage limit. The message shows the time the limit resets (e.g. `Usage limit reached · limit resets 3:45pm`).

```
Solution:
1. Wait until the reset time. If you leave the session open, it automatically continues after the reset (Continue automatically at usage limit in `/config`; on by default. It does not wait automatically when the reset is more than 24 hours away, such as a weekly limit)
2. While waiting, manually organize specifications and documentation
3. Next time, be mindful of these saving techniques
```

**Prevention:**

| Technique | Benefit |
|-----------|---------|
| Use Sonnet with `/model sonnet` | Consumes less usage than Opus |
| Reset with `/clear` per task | Prevent unnecessary context accumulation |
| Give specific instructions | Fewer trial-and-error iterations |
| Plan in Plan Mode first | It only investigates and plans, so rework drops |

→ See [Cost & Token Management](cost.md) for details

---

### Claude's Output is Wrong

#### Claude is hallucinating (making things up)

Claude claims something is implemented, but the file hasn't changed or the code is wrong.

```
Solution:
1. Always have Claude run tests ("Run tests and show me the results")
2. Verify the build passes
3. Check the files yourself

Prevention:
- Include verification in your instructions
- Make it a habit to say "implement and run tests to confirm"
```

#### Claude repeats the same mistake

If fixing something twice doesn't work, **continuing in the same session won't help**.

```
Solution:
1. Use `/clear` to reset the context
2. Instruct from scratch with what you learned ("The issue was caused by X")
3. Propose an alternative approach ("The previous method didn't work,
   so let's use X instead")
```

#### Claude ignores instructions

Claude isn't following the rules or style guide in CLAUDE.md.

```
Common causes (in order):
1. CLAUDE.md is too long (well over 50 lines) → Important rules get buried
2. Instructions are vague → Rewrite more specifically
3. Context is full → Use `/compact` or `/clear`

Solution:
- Cut CLAUDE.md down to just a table of contents and promises, 50 lines or less (move the substance to docs/ and link to it)
- Put the most important rules at the top
- Explicitly tell Claude "re-read and follow the CLAUDE.md rules"
```

#### Context is getting full

You see a warning like "context window is getting full."

```
Solution:
/compact                           ← Summarize and compress the conversation
/compact Focus on API changes      ← Compress while preserving specific topics
/clear                             ← Complete reset (when moving to a different task)
/handoff → /clear                  ← Save the state, reset, then resume with the prompt it prints
```

→ See [Best Practices > Context Management](best-practices.md#2-manage-your-context-window) for details

---

### File & Code Issues

#### Claude edited the wrong file

```
Solution:
1. Press Esc + Esc to undo (return to last checkpoint)
2. Select "Restore code" → Only file changes are reverted
3. If managed by git, you can also use git checkout
```

#### "Permission denied" when creating files

```bash
# Check file permissions
ls -la

# If you're not the owner:
# → Verify you're working in the correct directory
# → In WSL, work in ~/projects/ instead of /mnt/c/
```

#### Package installation fails

```
Solution:
1. Paste the error message directly to Claude
2. Instruct: "Fix this error"
3. Your Node.js version may be old → Check with node -v
```

---

### Git-Related

#### "I accidentally committed .env"

```bash
# Remove .env from git tracking (file itself remains)
git rm --cached .env

# Add to .gitignore
echo ".env" >> .gitignore

# Commit
git add .gitignore && git commit -m "fix: exclude .env from git management"
```

> **Important**: Once committed, credentials remain in history. If you've pushed .env with API keys, immediately revoke and regenerate those keys.

#### Commit guard blocked my commit

In projects created with `/kickstart`, a hook blocks commits that contain secrets or DB files. When blocked, unstage the files it lists.

```bash
git restore --staged <file>     # before the first commit, use git rm --cached <file>
```

- **Don't bypass the hook** (don't use `--no-verify`). Even if it looks like a false positive, first consider whether you can move that file elsewhere
- If it says "the git pre-commit hook isn't enabled," run `git config core.hooksPath .githooks` (cloning alone doesn't enable it)

→ See [Security Basics](security.md#commit-guard--stop-secrets-mechanically) for how it works

#### Claude pushed unexpectedly

Claude Code starts in **auto mode** by default. In auto mode, pushes to the current repository (including the default branch) and Pull Request creation **go through without confirmation**. If you always want a confirmation before pushing, add something like `Bash(git push *)` to `permissions.ask` in `.claude/settings.json` ([Security Basics](security.md#require-confirmation-before-push-and-pull-requests)). In projects created with `/kickstart`, this is set from the start.

In manual mode and Auto-Accept, a confirmation appears before pushing. When it does, read which branch and what is being pushed before approving.

→ See [Permission Modes and Approvals](overview.md#permissions-modes-and-approval-important)

---

## What Should I Do In This Situation?

| Situation | Action |
|------|---------|
| I don't know what to build | Ask Claude "Suggest 5 interesting projects that beginners can build" |
| I can't read error messages | Copy the error and ask Claude "Explain this error in simple terms" |
| I can't read English documentation | Ask Claude "Summarize the content of this URL in simple language" |
| I forgot what I was doing | Use `claude --continue` to resume the previous session |
| I don't understand Claude's suggestion | Don't hesitate to say "Explain this in simpler terms" |
| Nothing is working | `/clear` and start from scratch. If it still doesn't work, try again another day |
