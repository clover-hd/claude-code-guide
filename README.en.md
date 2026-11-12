[🇯🇵 日本語](README.md)

# Claude Code Practical Guide

A comprehensive, workflow-driven guide for real-world software development with Claude Code — written by a CTO actively using AI-driven development in production projects at a Japanese software company ([Clover Holding](https://www.clover-hd.jp/)).

> **Full English translation available in the [`en/`](en/) directory.** This page provides an overview; click through to read each chapter in English.

---

## What Makes This Guide Different

Most Claude Code resources are either reference docs, scattered tips, or collections of templates. This guide takes a different approach: it's structured around **how development actually flows** — from project setup to daily coding cycles — based on hands-on experience building real applications with Claude Code.

**End-to-end workflow coverage** — Not just "what each feature does," but "how to wire them together into a working development process." Phase A (project setup) flows into Phase B (daily development cycle) with clear, repeatable steps.

**Sub-agent team architecture** — Start with a 4-agent starter team (advisor, developer, QA engineer, code reviewer) and scale up as your project grows, with practical guidance on when and how to delegate.

**Task management and overnight runs** — Keep a task list that outlives sessions, pick and close tasks with `/task`, and let `/overnight` work through delegated tasks while you sleep — leaving decisions that need a human for the morning instead of guessing.

**Battle-tested patterns** — Anti-patterns, debugging strategies, cost management, and context window optimization learned from actual production use.

---

## Guide Structure

### Getting Started
| Section | Covers |
|---------|--------|
| [Installation & Setup](en/setup.md) | macOS / Linux / Windows (WSL) setup |
| [First 30 Minutes Tutorial](en/tutorial.md) | Hands-on tutorial to experience your first "wow" moment |
| [Walkthrough: Build an Outing Planner](en/walkthrough.md) | Full walkthrough: /kickstart → Phase A → Phase B on a real project |

### Claude Code Fundamentals
| Section | Covers |
|---------|--------|
| [Overview & Basic Operations](en/overview.md) | Capabilities, **permission modes & approval safety**, common commands |
| [Model Selection](en/models.md) | Fable / Opus / Sonnet / Haiku comparison, choosing the right model per task |

### Development Workflow
| Section | Covers |
|---------|--------|
| [Phase A: Project Setup](en/workflow-setup.md) | Building foundations from scratch (steps A0–A8 with dependencies, including where tasks live) |
| [Phase B: Daily Development Cycle](en/workflow-daily.md) | pick a task → consult → Plan → persist → implement → test → commit → milestone; `/overnight` while you sleep |

### Extending Claude Code
| Section | Covers |
|---------|--------|
| [Sub-Agents](en/sub-agents.md) | Start with 4 agents, scale up as needed |
| [Skills](en/skills.md) | Reusable prompt templates (`/commit`, `/consult`, `/task`, `/overnight`, etc.) |
| [MCP Servers](en/mcp.md) | External tool integration (Sequential Thinking, Serena, Context7) |
| [CLAUDE.md & Hooks](en/project-config.md) | Project-specific config and automation |

### Practical Guide
| Section | Covers |
|---------|--------|
| [Best Practices](en/best-practices.md) | Verification, context management, session handling, anti-patterns (12 topics) |
| [Security Basics](en/security.md) | Files to never commit, sensitive data handling, .gitignore |
| [Debugging](en/debugging.md) | Error investigation patterns, log analysis, test-driven reproduction |
| [Cost & Token Management](en/cost.md) | Pricing, usage limits, token-saving techniques |

### Customization
| Section | Covers |
|---------|--------|
| [Status Line](en/statusline.md) | Real-time usage rate, context remaining, and branch display |
| [/kickstart Skill](en/kickstart-skill.md) | Interactive project scaffolding — automates Phase A (A0–A8) |

### More
| Section | Covers |
|---------|--------|
| [Agent Team Quick Demo](en/examples/team-demo-quick.md) | 10-minute demo of parallel AI team development |
| [Troubleshooting / FAQ](en/troubleshooting.md) | Rate limits, hallucinations, repetitive errors |
| [Glossary](en/glossary.md) | Context window, tokens, hallucination, and other key terms |

---

## Daily Development Cycle (Quick Reference)

```
0. /task           → Pick the next task (add new ideas with /task add)
1. /consult        → Brainstorm requirements
2. Shift+Tab       → Plan Mode — design the approach
2.5. Persist       → Save the plan to docs/_wip/ as a detailed design
3. Shift+Tab       → Normal Mode — implement
3.5. Test          → Unit tests & E2E tests
4. /commit         → Commit after review
5. Milestone       → /ask-advisor milestone review, clean up docs/_wip/, /task done

Before bed        → /overnight works through delegated tasks until morning,
                    leaving points that need a human decision and moving on
```

---

## About

This guide is maintained as part of an AI-driven development initiative at [Clover Holding](https://www.clover-hd.jp/), a software company based in Tokyo. We're actively exploring how AI agents can transform the way engineering teams build software — and sharing what we learn along the way.

If you find this guide useful, a ⭐ would be appreciated.
