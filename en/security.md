# Security Basics

[< Back to Guide](../README.en.md)

---

For company projects, you need at least a basic security awareness.

## Things That Should Never Be Committed

| File | Content | Mitigation |
|---------|------|------|
| `.env` | API keys, DB connection info, secrets | Add to `.gitignore` |
| `credentials.json` | Service account keys | Add to `.gitignore` |
| `*.pem`, `*.key` | SSL certificates, private keys | Add to `.gitignore` |
| `node_modules/` | Dependency packages | Add to `.gitignore` |

**Write rules in CLAUDE.md** and Claude automatically avoids them:

```markdown
# CLAUDE.md (excerpt)

## Security Rules
- Never commit .env files
- Never hardcode API keys or passwords in code
- Retrieve authentication info via environment variables
```

> However, rules in CLAUDE.md are "requests". If you need to block things reliably, set up the [commit guard](#commit-guard--stop-secrets-mechanically) described below.

## Information Not to Pass to Claude

Claude Code communicates with AI in the cloud. Do not enter:

- Production database connection info
- Customer personal information (names, email addresses, etc.)
- Production API keys or secrets

> Development dummy data or test environment info is fine.

## .gitignore Template

When starting a new project, include at least this:

```gitignore
# Environment variables and secrets
.env
.env.local
.env.production

# Authentication info
credentials.json
*.pem
*.key
service-account.json

# Dependency packages
node_modules/

# Build artifacts
dist/
build/

# OS and editor
.DS_Store
.vscode/settings.json
```

## Commit Guard — Stop Secrets Mechanically

With only `.gitignore` and CLAUDE.md rules, secrets can still get committed through `git add -f` or an agent's oversight. Anything once committed is **hard to remove completely from history**, so set up a mechanism that **mechanically** checks and blocks before committing.

### Block in two layers

Call the same check script, `scripts/check-staged.sh`, from two entry points.

| Layer | What it blocks | Why it's not enough on its own |
|---|---|---|
| git pre-commit hook (`.githooks/pre-commit`) | Blocks commits, including human ones | Not enabled just by cloning. Can be skipped with `--no-verify` |
| Claude Code PreToolUse hook (`.claude/settings.json`) | The agent's `git commit`. Also blocks bypassing hooks with `--no-verify` | Can't block human commits |

Either one alone leaves a hole, so use both layers.

### What the check script looks at

- Secret and credential files such as `.env`, `*.pem`, `*.key`, and `credentials.json`
- Database files such as `*.sqlite` and `*.db`
- API-key-like strings in added lines (`sk-ant-...`, `AKIA...`, `-----BEGIN ... PRIVATE KEY-----`, etc.)

```bash
# Excerpt: look at each staged file
while IFS= read -r -d '' f; do
  base=$(basename "$f" | tr '[:upper:]' '[:lower:]')
  case "$base" in
    .env.example) ;;
    .env | .env.*) report "$f — secrets file (.env)" ;;
  esac
done < <(git diff --cached --name-only --diff-filter=ACMR -z)
```

### What the PreToolUse hook does

- **Blocks** `git commit --no-verify` / `-n` (options that skip git hooks)
- **Blocks** if the git hook (`core.hooksPath`) isn't enabled, and says to enable it
- Runs the check script and **blocks** on a hit (the reason is passed to Claude, which then unstages the file)
- **Asks a human to confirm** pushes, creating Pull Requests and Issues, and commands that could break production (such as migrating the production DB)

### Require Confirmation Before Push and Pull Requests

Claude Code starts in **auto mode** by default. In auto mode, pushes to the current repository (including the default branch) and creating Pull Requests **go through without confirmation**. The classifier also reads instructions in CLAUDE.md, but that doesn't guarantee a confirmation will appear. An instruction given only in conversation, such as "don't push," can disappear when the conversation is compacted.

If you want a human to confirm before a push, put it in `permissions.ask` in `.claude/settings.json`. Operations matching these rules always prompt for confirmation, even in auto mode.

```json
{
  "permissions": {
    "ask": [
      "Bash(git push *)",
      "Bash(gh pr create *)",
      "Bash(gh pr merge *)",
      "Bash(gh issue create *)"
    ]
  }
}
```

These rules match commands written as `git push` (including a part chained with `&&`). They don't catch other forms such as `git -C <dir> push`, so the PreToolUse hook above also looks at the whole command and asks for confirmation. `/kickstart` sets up both.

Even so, some things slip through depending on how they're written, such as creating one directly with `gh api`. Treat the confirmation setup not as a sure defense but as something that "stops the ordinary way of writing it," and combine it with a human checking at natural breakpoints in the work.

For how to write hooks, see [CLAUDE.md and Hooks](project-config.md#hooks-automation). The full script and hook are in A7 of the [kickstart skill](skills/kickstart/SKILL.md). With `/kickstart`, this is set up automatically when the project is created.

> **Even when blocked by a false positive**, don't skip the hook. Before adding an exception, first consider whether the file can live somewhere else.

> **For teams**: `core.hooksPath` isn't enabled just by cloning, so add `git config core.hooksPath .githooks` to the setup steps in your README.
