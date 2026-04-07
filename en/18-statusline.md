# Status Line

[< Back to Guide](README.en.md)

---

Claude Code's terminal can display **usage rates, context remaining, and branch info in real-time** at the bottom. This prevents accidents where you hit rate limits or run out of context without realizing it.

## What's Displayed

```
ai:main ↑2 | Claude Opus 4.6 | 5h:32% | 7d all:18% / opus:25% / sonnet:12% | ctx:85%
```

| Section | Content |
|-----------|------|
| **repo:branch** | Repository name, branch name, ↑↓ shows push/pull status |
| **Model name** | Currently used model |
| **5h** | 5-hour rolling window usage rate (from OAuth Usage API) |
| **7d** | 7-day usage rate (by all/opus/sonnet) |
| **ctx** | Context window remaining |

### Color Coding

- Usage rate (5h/7d): Green <50% → Yellow 50-80% → Red 80%+
- Context remaining: Green 50%+ → Yellow 20-50% → Red <20%
- Also displays time until reset (e.g., `3h24m`)

## Other Status Line Tools

Status line is a standard Claude Code feature, and display content can be customized via script. This guide uses `statusline.py`, but various implementations are available as open source.

| Tool | Features |
|--------|------|
| This guide's `statusline.py` | Displays usage, context, and git info simply |
| [claude-code-power-pack](https://github.com/nicobailon/claude-code-power-pack) | Comprehensive toolkit including status line |
| Community implementations | Search "claude code statusline" on GitHub |

You can use any tool. What matters is **keeping usage visible at all times**.

## Setup (statusline.py)

### 1. Place the script

Download [`tools/statusline.py`](tools/statusline.py) from this repository to `~/.claude/`.

```bash
curl -fsSL https://raw.githubusercontent.com/clover-hd/claude-code-guide/main/tools/statusline.py \
  -o ~/.claude/statusline.py
```

### 2. Add to settings.json

Add `statusLine` to `~/.claude/settings.json`.

```json
{
  "statusLine": {
    "type": "command",
    "command": "python3 ~/.claude/statusline.py",
    "padding": 0
  }
}
```

> If `settings.json` already has other settings, just append the `statusLine` key.

### 3. Restart Claude Code

Restart Claude Code to apply the settings. You'll see the status line at the terminal bottom if successful.

## How It Works

### Data Sources

| Data | Source |
|--------|--------|
| repo/branch/ahead-behind | `git` command |
| Model name | JSON passed to stdin from Claude Code |
| Context remaining | JSON passed to stdin from Claude Code |
| Usage rates (5h/7d) | [OAuth Usage API](https://docs.anthropic.com/) + OAuth token |

### Getting OAuth Token

- **macOS**: Auto-retrieved from macOS Keychain (no setup needed if Claude Code is logged in)
- **Linux/WSL**: Read from `~/.claude/.credentials.json`

### API Cache

To prevent excessive Usage API calls, responses are **cached for 10 minutes** in `~/.claude/statusline-usage-cache.json`. If the API fails, cached data is displayed.

## Troubleshooting

| Symptom | Cause & Solution |
|------|-----------|
| Status line not showing | Check if `python3` is in PATH. Try running `python3 ~/.claude/statusline.py` manually to see errors |
| Usage rate shows `--` | OAuth token couldn't be retrieved. Try logging in to Claude Code again |
| Usage rate not updating | Cache TTL is 10 minutes. Delete `~/.claude/statusline-usage-cache.json` to immediately re-fetch |
| Branch not showing | Claude Code is running outside a git repository |
