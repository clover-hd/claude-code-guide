# Cost & Token Management

[< Back to Guide](../README.en.md)

---

## Plans and Pricing

Claude Code is available on paid plans. Higher plans come with larger usage allowances.

Plans and prices change from time to time, so this guide doesn't list them. For the latest details and which plans include Claude Code, see the [pricing page](https://claude.com/pricing).

We recommend starting with the most affordable individual paid plan and considering a higher plan once you hit the limits often.

## Pro Plan Usage Limits

- Usage resets in a **5-hour rolling window**
- When the limit is reached, you'll see "Usage limit reached" along with the reset time. If you leave the session open, it automatically resumes after the reset (it does not wait automatically when the reset is 24 hours or more away, such as a weekly limit)
- Opus consumes more tokens, so you'll hit the limit faster

## Set Up Status Line First

The most effective token management is to **make usage visible in real-time**.

Setting up the [status line](statusline.md) displays your 5-hour and 7-day usage rates directly on the Claude Code screen. By watching this while you work, you naturally make decisions like "I'm getting close to the limit, let me switch to Sonnet" or "I still have plenty, so let me design with Opus."

See [statusline.md](statusline.md) for setup instructions.

## Tips for Saving Tokens

| Technique | Benefit | How |
|-----------|---------|------|
| **Use Sonnet** | Consumes less than Opus | `/model sonnet` (sufficient for daily use) |
| **Use `/clear` frequently** | Avoid wasting context on unnecessary information | Reset every time you change tasks |
| **Use `/compact`** | Compress context and extend session life | Run around 70% usage |
| **Delegate to sub-agents** | Reduce main context consumption | "Investigate with sub-agent" |
| **Give specific instructions** | Reduce trial-and-error iterations | Specify file names, function names, expected behavior |
| **Plan first in Plan Mode** | Doesn't edit source, so it's lighter, and rework drops | Always plan large tasks first |

For more details on model selection by workflow, see [Model Differences and Selection Guide](models.md#workflow-specific-selection-guide).

> **Tip**: When you hit the 5-hour limit, use that time to manually organize specifications and documentation for your next session. Development isn't just about writing code.
