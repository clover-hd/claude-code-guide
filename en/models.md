# Model Differences and Selection

[< Back to Guide](../README.en.md)

---

## Model Differences and Selection

You can switch models with the `/model` command in Claude Code.

> This guide doesn't list model version numbers or prices, because they change with every new release. For the latest models, prices, and context windows, see the [official models overview](https://platform.claude.com/docs/en/about-claude/models/overview); for how to specify models in Claude Code, see [Model configuration](https://code.claude.com/docs/en/model-config).

### Model Families

Claude models come in four families with different capability and cost. Passing a family name (alias) to `/model` uses the latest model in that family.

| Family | Alias | Positioning | Good for |
|--------|-------|-------------|----------|
| **Fable** | `fable` | Top tier. For the hardest, longest-running work | Consultations that shape direction, long autonomous runs |
| **Opus** | `opus` | High capability. For complex reasoning | Design, tech selection, complex refactoring |
| **Sonnet** | `sonnet` | Balanced capability and cost. For everyday coding | Implementation, bug fixes, tests |
| **Haiku** | `haiku` | Fastest and cheapest. For simple work | Quick questions, file search, routine tasks |

> **Note on Fable**: On some plans, Fable usage is drawn from **usage credits** rather than your plan's allowance (the `/model` picker shows "Requires usage credits"). For where to use it, see [Sub-agents](sub-agents.md#using-fable-for-the-advisor).

### How to Choose?

```
Daily coding, bug fixes, feature additions
  → Sonnet (start here. Lighter than Opus, so your usage allowance lasts longer)

Large-scale architecture design, complex refactoring
  → Opus (shines where deep reasoning is needed)

Hard decisions that shape direction, work you leave running for a long time
  → Fable (save it for when it matters, keeping an eye on usage)

Quick questions, file search, routine tasks
  → Haiku (fast & cheap)
```

Higher families are more capable and also consume more usage. Rather than "go one tier up when in doubt," "try Sonnet first and move up if it falls short" is the way to make your allowance last.

### How to Switch Models

```
/model            ← Opens the model picker
/model sonnet     ← Switch to the latest Sonnet
/model opus       ← Switch to the latest Opus
/model fable      ← Switch to the latest Fable
/model haiku      ← Switch to the latest Haiku
/model opusplan   ← Use Opus in Plan Mode and Sonnet for implementation
```

You can also specify it at launch, e.g. `claude --model sonnet`.

---

## Workflow-Specific Selection Guide

The same basic approach applies to both Phase A (project setup) and Phase B (daily development).

| Phase | Recommended Model | Reason |
|-------|-------------------|--------|
| Ideation & brainstorming (/consult) | Sonnet | Sufficient for interactive discussion |
| Planning & design (Plan Mode) | **Opus** | Deep reasoning pays off in large design decisions |
| Architecture decisions (Phase A4) | **Opus** | Tech stack selection is a critical branching point |
| Implementation & coding | Sonnet | Plenty capable for everyday coding |
| Writing & running tests | Sonnet | Sufficient accuracy for test code generation |
| Commits & routine tasks | Sonnet / Haiku | A light model is fine |

Sub-agents specify the family with `model:` in their definition file (e.g., `opus` for the advisor, `sonnet` for the developer). Putting only the advisor, which makes the heavy decisions, on a higher family keeps usage down while preserving decision quality. To use Fable for the advisor, see [Sub-agents](sub-agents.md#using-fable-for-the-advisor).

> **Tip**: Planning with Opus and implementing with Sonnet is a "best of both worlds" strategy that keeps cost down while maximizing quality. `/model opusplan` does this switch automatically.

### Monitor Token Usage in Real-Time

The best way to stay mindful of model selection is to make your current token consumption visible. Set up the [status line](statusline.md) to display your 5-hour / 7-day usage in real time in Claude Code. Watching what's left, you can decide "Sonnet is enough here" or "switch to Opus just for this part."
