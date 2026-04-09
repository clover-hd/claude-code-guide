# Sub-agents

[< Back to Guide](../README.en.md)

---

## What are Sub-agents?

One of Claude Code's most powerful features: **define multiple specialized AI assistants**, each with different roles, permissions, and constraints.

Each sub-agent runs in its **own context window**, allowing independent work without polluting the main conversation.

## Configuration

Place Markdown files in the `.claude/agents/` directory:

```
.claude/
└── agents/
    ├── system_architect.md     ← Design lead
    ├── developer.md            ← Full-stack implementation
    ├── qa_engineer.md          ← Quality management
    └── ...                     ← Add as needed
```

## How to Invoke

Once agents are defined, there are three ways to call them. Choose based on your use case.

### 1. @-mention (recommended)

Type `@` to bring up the typeahead. Select the agent, then **continue typing your instructions** before pressing Enter.

```
> @.claude/agents/developer.md Following the spec in docs/specs/feature-crud.md, implement this feature.
```

> **Note**: The agent path and your instructions must be sent as **a single message**. If you press Enter after just the path, the agent will start running without any instructions.

This is the most reliable method. You have explicit control over which agent runs.

### 2. Natural language

Mention the agent's name in your prompt and Claude will decide whether to delegate.

```
> Use the developer agent to implement this feature
> Have the system_architect review this design
```

Convenient, but Claude may or may not delegate based on its judgment. Use @-mention when you need certainty.

### 3. `--agent` flag for session-wide use

Use this when you want the entire session to run as a single agent.

```bash
claude --agent .claude/agents/developer.md
```

In this mode, all interactions in the session use that agent's system prompt, tool restrictions, and model settings.

---

## Start with Three — Starter Configuration

More agents don't automatically mean better. **Start with three agents**, then expand as needed.

| Agent | Role | Can Do | Can't Do |
|-------|------|--------|----------|
| **system_architect** | Design lead | Design, API specs, DB design | Code implementation |
| **developer** | Implementation specialist | Coding, testing | Design decisions (defer to architect) |
| **qa_engineer** | Quality manager | Test creation, bug reports | Edit product code |

These three create the "design → implement → verify" cycle. Perfect for solo work or small teams.

> **Key Point**: Write specific tech stack names in `developer`'s description. For example, "full-stack development with React + Express + SQLite." When you need division of labor, see "Scale Up" below.

## Scale Up — For Larger Projects

When frontend/backend split, mobile apps exist, or scale grows, expand division of labor:

| Agent | Add When |
|-------|----------|
| **tech_researcher** | Library selection and research grow. Read-only, so safe |
| **frontend_developer** | Front and back use different tech stacks |
| **mobile_developer** | Mobile app development begins |
| **ui_ux_designer** | Design system management needed |
| **technical_writer** | Serious documentation phase begins |

Add agents when you need them. No need to have all nine from day one.

## How to Write Agent Definition Files

```markdown
---
name: tech-researcher
description: Technical research, library selection, bug root cause analysis.
             Proposes solutions only, makes no code changes.
---

# Role
You are a **Senior Technical Researcher**.
Your job is not "to implement"
but "to find how to implement."

# Goals
1. Library selection: Research and compare optimal libraries
2. Bug identification: Find root causes
3. Technical verification: Answer technical questions

# Available Tools
- WebSearch, WebFetch, Grep, Glob, Read

# Constraints
- **Read-Only**: Never modify code
- **Summarize**: Keep conclusions and reference links brief
```

## Why Sub-agents Are Powerful

1. **Specialization**: Each agent focuses on their domain
2. **Safety**: Limited permissions prevent unintended changes
3. **Parallel Execution**: Multiple agents work independently simultaneously
4. **Context Protection**: Main conversation doesn't get flooded with research results

---

## Generic Agents vs. Project-Specific Agents

Open-source agent definitions are published widely on GitHub. These are useful references, but **copying them as-is isn't recommended**.

### Why Build Project-Specific Agents

A generic "developer" agent knows only general development patterns. It doesn't know your project's unique rules — tech stack, design patterns, directory structure. It must guess from scratch every time.

```
Generic agent:
  "I can implement backends"
  → But doesn't know if your project uses Clean Architecture,
    Prisma, or Docker command execution requirements
  → Spends every task figuring out your project structure

Project-specific agent:
  "I implement APIs with Prisma ORM + Clean Architecture in domain/"
  → Works within your project context immediately
  → Knows which spec paths to reference, directories to avoid
```

This difference compounds the more you use them.

### Reference: OSS Agent Definition Collections

GitHub hosts many sub-agent definition collections. Use them as templates for role patterns and Constraints syntax, but customize for your project.

#### Official Agent/Skill Definitions from Companies

Major companies publish official agent/skill definitions for their frameworks. These show "how professionals actually write them."

| Repository | Content |
|-----------|---------|
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | **Vercel official** agent skill collection |
| [vercel/next.js AGENTS.md](https://github.com/vercel/next.js/blob/canary/AGENTS.md) | Next.js official AI agent instructions (CLAUDE.md example) |
| [awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | **Official skills from Anthropic, Vercel, Stripe, Cloudflare, Sentry, Expo** + community — 380+ collected |

> **Tip**: In Next.js projects, running `npx @next/codemod agents-md` auto-generates a document index in CLAUDE.md matching your Next.js version.

#### Community Agent Definition Collections

| Repository | Content |
|-----------|---------|
| [awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) | 100+ specialist agents organized by category. Includes install scripts |
| [claude-code-subagents](https://github.com/0xfurai/claude-code-subagents) | 100+ production-ready agents |
| [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | Agents, skills, Hooks, MCP plugins — curated list |
| [awesome-claude-agents](https://github.com/rahulvrane/awesome-claude-agents) | Community-submitted agents and frameworks |
| [agents (wshobson)](https://github.com/wshobson/agents) | Serious multi-agent system: 112 agents + 16 orchestrators |

> **Critical**: These are **structure and syntax references only**. Copying directly produces agents that don't understand *your* project. Customize using the process below.

### Recommended: Use OSS as Reference, Have Claude Generate Project-Specific Versions

Don't write from scratch. **Give Claude OSS agent definitions as templates and generate project-specific versions**.

Claude reads your actual codebase and creates accurate agents, catching architecture details you'd miss.

### Practical Process

```
Step 1: Find and read OSS agent definitions
        → Learn "what role divisions and Constraints look like"

Step 2: Decide your project architecture (Phase A4)
        → Tech stack, design patterns, directories all confirmed

Step 3: Instruct Claude Code to generate agents (↓ see below)
        → Claude reads codebase and creates project-specific versions
```

### Example Instruction to Claude Code

```
You: I want to create sub-agents.
     Using the OSS agent definitions below as reference,
     create a developer agent for this project.

     【Reference OSS definitions】
     (paste OSS agent definitions here)

     Check docs/architecture.md for project architecture.
     Reflect CLAUDE.md rules too.
     Save to .claude/agents/developer.md.

Claude: Examined codebase.
        - Tech Stack: React + Express + SQLite + TypeScript
        - Design Pattern: Clean Architecture
        - Directories: src/domain/, src/infrastructure/, src/interface/
        - Tests: Jest, tests/unit/

        Creating agent reflecting these...
        (.claude/agents/developer.md generated)
```

Claude automatically incorporates:

- Project-specific technology names
- Division of labor based on actual directory structure
- Reference spec and design document paths
- Alignment with rules in CLAUDE.md

### Example Transformation (Generic → Project-Specific)

```markdown
# Generic (from OSS)
---
name: backend-developer
description: Build backend APIs
---
# Role
Backend development expert.
# Constraints
- Never touch frontend code

# ↓ Claude Code generates project-specific version ↓

---
name: backend-developer
description: Build APIs with Express + Prisma. Follows Clean Architecture.
---
# Role
Specialist in Node.js (Express), MySQL, Prisma ORM.

# Goals
1. Implement APIs per specs in docs/specs/
2. Maintain Clean Architecture patterns in src/domain/
3. Create tests in tests/unit/ using Jest

# Constraints
- Never touch src/mobile/ code
- For DB schema changes, defer to system_architect
- Use .env.example for env vars, no hardcoding

# References
- docs/architecture.md — Overall architecture
- docs/specs/api/ — API endpoint specifications
```

The three-line generic version becomes a detailed, project-aware agent after Claude reads your codebase.

> **Key Point**: After generation, review and add missing pieces with simple follow-ups. No need for perfection—you develop them as you use them.
