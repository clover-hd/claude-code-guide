[🇯🇵 日本語](README.md)

# Claude Code Practical Guide

A comprehensive, workflow-driven guide for real-world software development with Claude Code — written by a CTO actively using AI-driven development in production projects at a Japanese software company ([Clover Holding](https://www.clover-hd.jp/)).

> **Full English translation available in the [`en/`](en/) directory.** This page provides an overview; click through to read each chapter in English.

---

## What Makes This Guide Different

Most Claude Code resources are either reference docs, scattered tips, or collections of templates. This guide takes a different approach: it's structured around **how development actually flows** — from project setup to daily coding cycles — based on hands-on experience building real applications with Claude Code.

**End-to-end workflow coverage** — Not just "what each feature does," but "how to wire them together into a working development process." Phase A (project setup) flows into Phase B (daily development cycle) with clear, repeatable steps.

**Sub-agent team architecture** — Start with a 3-agent starter team (architect, developer, QA) and scale up as your project grows, with practical guidance on when and how to delegate.

**Battle-tested patterns** — Anti-patterns, debugging strategies, cost management, and context window optimization learned from actual production use.

---

## Guide Structure

### Getting Started
| # | Section | Covers |
|---|---------|--------|
| 1 | [Installation & Setup](en/01-setup.md) | macOS / Linux / Windows (WSL) setup |
| 2 | [First 30 Minutes Tutorial](en/02-first-session.md) | Hands-on tutorial to experience your first "wow" moment |

### Claude Code Fundamentals
| # | Section | Covers |
|---|---------|--------|
| 3 | [Overview & Basic Operations](en/03-overview.md) | Capabilities, **permission modes & approval safety**, common commands |
| 4 | [Model Selection](en/04-models.md) | Opus / Sonnet / Haiku comparison, choosing the right model per task |

### Development Workflow
| # | Section | Covers |
|---|---------|--------|
| 5 | [Phase A: Project Setup](en/05-workflow-setup.md) | Building foundations from scratch (steps A1–A7 with dependencies) |
| 6 | [Phase B: Daily Development Cycle](en/06-workflow-daily.md) | consult → Plan → persist → implement → test → commit |

### Extending Claude Code
| # | Section | Covers |
|---|---------|--------|
| 7 | [Sub-Agents](en/07-sub-agents.md) | Start with 3 agents, scale up as needed |
| 8 | [Skills](en/08-skills.md) | Reusable prompt templates (`/commit`, `/consult`, etc.) |
| 9 | [MCP Servers](en/09-mcp.md) | External tool integration (Sequential Thinking, Serena, Context7) |
| 10 | [CLAUDE.md & Hooks](en/10-project-config.md) | Project-specific config and automation |

### Practical Guide
| # | Section | Covers |
|---|---------|--------|
| 11 | [Best Practices](en/11-best-practices.md) | Verification, context management, session handling, anti-patterns (12 topics) |
| 12 | [Security Basics](en/12-security.md) | Files to never commit, sensitive data handling, .gitignore |
| 13 | [Debugging](en/13-debugging.md) | Error investigation patterns, log analysis, test-driven reproduction |
| 14 | [Cost & Token Management](en/14-cost.md) | Pricing, usage limits, token-saving techniques |

### Customization
| # | Section | Covers |
|---|---------|--------|
| 18 | [Status Line](en/18-statusline.md) | Real-time usage rate, context remaining, and branch display |

### Included Skills
| # | Section | Covers |
|---|---------|--------|
| 17 | [/kickstart Skill](en/17-kickstart-skill.md) | Interactive project scaffolding — automates Phase A (A1–A7) |

### Walkthroughs
| Section | Covers |
|---------|--------|
| [Outing Planner](en/examples/walkthrough.md) | Full walkthrough: /kickstart → Phase A → Phase B on a real project |
| [Agent Team Quick Demo](en/examples/team-demo-quick.md) | 10-minute demo of parallel AI team development |

### Troubleshooting
| # | Section | Covers |
|---|---------|--------|
| 15 | [Troubleshooting / FAQ](en/15-troubleshooting.md) | Rate limits, hallucinations, repetitive errors |
| 16 | [Glossary](en/16-glossary.md) | Context window, tokens, hallucination, and other key terms |

---

## Daily Development Cycle (Quick Reference)

```
1. /consult        → Brainstorm requirements
2. Shift+Tab       → Plan Mode — design the approach
2.5. Persist       → Save spec to docs/specs/
3. Shift+Tab       → Normal Mode — implement
3.5. Test          → Unit tests & E2E tests
4. /commit         → Commit following conventions
```

---

## About

This guide is maintained as part of an AI-driven development initiative at [Clover Holding](https://www.clover-hd.jp/), a software company based in Tokyo. We're actively exploring how AI agents can transform the way engineering teams build software — and sharing what we learn along the way.

If you find this guide useful, a ⭐ would be appreciated.
