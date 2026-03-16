# Cost & Token Management

[< Back to Guide](README.en.md)

---

## Plans and Pricing

| Plan | Monthly Cost | Claude Code | Notes |
|------|------|-------------|------|
| **Free** | Free | Not available | — |
| **Pro** | $20 | Available | This project uses this |
| **Max 5x** | $100 | 5x Pro's limit | For heavy users |
| **Max 20x** | $200 | 20x Pro's limit | For all-day users |

## Pro Plan Usage Limits

- Usage resets in a **5-hour rolling window**
- When the limit is reached, you'll see "Try again in X hours"
- Opus consumes more tokens, so you'll hit the limit faster

## Set Up Status Line First

The most effective token management is to **make usage visible in real-time**.

Setting up the [status line](18-statusline.md) displays your 5-hour and 7-day usage rates directly on the Claude Code screen. By watching this while you work, you naturally make decisions like "I'm getting close to the limit, let me switch to Sonnet" or "I still have plenty, so let me design with Opus."

See [18-statusline.md](18-statusline.md) for setup instructions.

## Tips for Saving Tokens

| Technique | Benefit | How |
|-----------|---------|------|
| **Use Sonnet 4.6** | 1/5 the cost of Opus | `/model sonnet` (sufficient for daily use) |
| **Use `/clear` frequently** | Avoid wasting context on unnecessary information | Reset every time you change tasks |
| **Use `/compact`** | Compress context and extend session life | Run around 70% usage |
| **Delegate to sub-agents** | Reduce main context consumption | "Investigate with sub-agent" |
| **Give specific instructions** | Reduce trial-and-error iterations | Specify file names, function names, expected behavior |
| **Plan first in Plan Mode** | Read-only mode is lighter than implementation | Always plan large tasks first |

For more details on model selection by workflow, see [Model Differences and Selection Guide](04-models.md#workflow-specific-usage-guide).

> **Tip**: When you hit the 5-hour limit, use that time to manually organize specifications and documentation for your next session. Development isn't just about writing code.
