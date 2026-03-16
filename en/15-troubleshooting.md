# Troubleshooting / FAQ

[< Back to Guide](README.en.md)

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

#### "Try again in X hours" appears

You've reached your Pro plan usage limit.

```
Solution:
1. Wait the specified time (5-hour rolling window)
2. While waiting, manually organize specifications and documentation
3. Next time, be mindful of these saving techniques
```

**Prevention:**

| Technique | Benefit |
|-----------|---------|
| Use Sonnet with `/model sonnet` | 1/5 token consumption of Opus |
| Reset with `/clear` per task | Prevent unnecessary context accumulation |
| Give specific instructions | Fewer trial-and-error iterations |
| Plan in Plan Mode first | Read-only mode uses fewer tokens than implementation |

→ See [Cost & Token Management](14-cost.md) for details

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
1. CLAUDE.md is too long (over 200 lines) → Important rules get buried
2. Instructions are vague → Rewrite more specifically
3. Context is full → Use `/compact` or `/clear`

Solution:
- Reduce CLAUDE.md to 200 lines or less
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
```

→ See [Best Practices > Context Management](11-best-practices.md#2-manage-your-context-window) for details

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

#### Claude pushed unexpectedly

In the default Claude Code configuration, there's always a confirmation before pushing. Even in Auto-Accept mode, pushes are confirmed. If you push unintentionally, get in the habit of reading approval prompts carefully.

→ See [Permission Modes and Approvals](03-overview.md#permission-modes-and-approvals-important)

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
