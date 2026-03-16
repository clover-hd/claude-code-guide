# Model Differences and Selection / Sonnet 4.6's Major Leap

[< Back to Guide](README.en.md)

---

## Model Differences and Selection

You can switch models with the `/model` command in Claude Code.

### Model List (As of March 2026)

| Model | Model ID | Characteristics | Input/Output Cost |
|--------|----------|------|----------------|
| **Opus 4.6** | `claude-opus-4-6` | Top performance. Best for complex reasoning and large-scale design | $15 / $75 per 1M tokens |
| **Sonnet 4.6** | `claude-sonnet-4-6` | **Best value. Nearly matches Opus for coding** | $3 / $15 per 1M tokens |
| **Haiku 4.5** | `claude-haiku-4-5` | Fastest and cheapest. Best for simple tasks | Most affordable |

### How to Choose?

```
Daily coding, bug fixes, feature additions
  → Sonnet 4.6 (sufficient for all. 1/5 the cost of Opus)

Large-scale architecture design, complex refactoring
  → Opus 4.6 (deep reasoning shines here)

Simple questions, file searches, routine tasks
  → Haiku 4.5 (fast & cheap)
```

### How to Switch Models

```
/model          ← Shows model selection menu
/model opus     ← Switch to Opus 4.6
/model sonnet   ← Switch to Sonnet 4.6
/model haiku    ← Switch to Haiku 4.5
```

---

## Sonnet 4.6's Major Breakthrough

**Sonnet 4.6, released in February 2026, is a game-changer.**

### Benchmark Comparison

| Benchmark | Sonnet 4.6 | Opus 4.6 | Gap |
|-------------|-----------|----------|-----|
| **SWE-bench** (Coding) | **79.6%** | 80.8% | Only 1.2pt difference |
| **OSWorld** (PC Operations) | **72.5%** | 72.7% | Nearly equivalent |
| **Math & Reasoning** | **89%** | — | High score |

### Real-World Performance in Claude Code

In Anthropic's internal testing, developer preference for Sonnet 4.6:

- **vs Sonnet 4.5** (previous generation): **70%** chose Sonnet 4.6
- **vs Opus 4.5** (previous flagship): **59%** chose Sonnet 4.6

In other words, **it surpassed the previous flagship model.**

### What Improved

| Improvement | Details |
|--------|------|
| **Context Understanding** | Now reads existing code thoroughly before making changes |
| **Logic Consolidation** | Properly abstracts shared logic instead of copy-pasting |
| **Avoiding Overdesign** | Unnecessary abstraction and over-engineering greatly reduced |
| **Following Instructions** | Follows directions precisely. Less likely to go off track on its own |
| **Honesty** | Reduced false claims of completion. Less hallucination |
| **Multi-step Tasks** | Better at completing multi-step tasks to the end |

### Context Window

Sonnet 4.6 supports a **1 million token** context window (beta). You can understand your entire project codebase at once.

### Bottom Line: Sonnet 4.6 is Sufficient for Daily Use

At **1/5 the cost of Opus**, with nearly equivalent coding performance, Sonnet 4.6 should be your default. Only switch to Opus for truly complex design decisions.

---

## Model Selection Guide by Workflow

Whether you're in Phase A (project setup) or Phase B (daily development), the thinking is the same.

| Phase | Recommended Model | Reason |
|---------|-----------|------|
| Brainstorming & discussion (/consult) | Sonnet 4.6 | Sufficient for interactive discussion |
| Planning & design (Plan Mode) | **Opus 4.6** | Deep reasoning helps with large design decisions |
| Architecture decisions (Phase A4) | **Opus 4.6** | Tech stack selection is an important branching point |
| Implementation & coding | Sonnet 4.6 | Coding performance nearly matches Opus |
| Test writing & execution | Sonnet 4.6 | Sufficient accuracy for generating test code |
| Commits & routine tasks | Sonnet 4.6 / Haiku 4.5 | Lighter models work fine |

> **Tip**: Planning with Opus and implementing with Sonnet is a cost-effective "best of both worlds" strategy that maintains quality while reducing costs.

### Monitor Token Usage in Real-Time

To make model selection a habit, visibility into current token consumption is key. Setting up the [status line](18-statusline.md) displays your 5-hour and 7-day usage rate in real-time on your Claude Code screen. You can then make judgments like "Sonnet is enough here" or "Let me switch to Opus just for this part" based on remaining quota.
