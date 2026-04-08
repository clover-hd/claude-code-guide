# Development Workflow Phase A: Project Initialization

[< Back to Guide](../README.en.md) | [Phase B: Daily Development Cycle >](workflow-daily.md)

---

Development with Claude Code follows a golden rule: **think before you build**. This section introduces a workflow for launching projects from scratch.

When starting a new project, jumping straight into coding leads to getting lost. Instead, we systematically lay the **foundation for Claude Code to work intelligently**, step by step.

## Overall Flow and Dependencies

```
Phase A: Project Initialization

  A1. Create Service Overview Document
      │  Express your vision in writing
      ▼
  A2. Create /consult Skill
      │  Build a thinking partner who reads A1
      ▼
  A3. Bounce Ideas with /consult
      │  Lock down feature list, MVP, priorities
      ▼
  A4. Decide Architecture              ← Branching point
      │  Technology stack, design patterns,      Sub-agent contents
      │  directory structure                    depend on this
      ▼
  A5. Create CLAUDE.md
      │  Define project rules, structure, conventions
      ▼
  A6. Create Sub-agents
      │  Assemble specialist team aligned with architecture
      ▼
  A7. Create Additional Skills & Hooks
      │  Development tools like /commit, /review
      ▼
  ─────────────────────────────
  Phase B: Daily Development Cycle
```

> **Key Point**: A4 (Architecture Decision) must come before A6 (Sub-agents).
> Only after you decide "Backend is Express + Prisma" can you define an agent like "Prisma ORM specialist".

---

## A1: Create a Service Overview Document

Create a **Markdown file describing the entire service vision** at your project root. This becomes the foundation for everything.

What to write:

```markdown
# Service Overview

## Service Name
(You can use a placeholder)

## What are we building? (One sentence)
Example: A platform for restaurant reservation and review management

## What we value most
- User experience first (simple and intuitive)
- Security (we handle personal information)
- Small start, fast market entry

## Final Vision
Example: Provide peace of mind that "help is always just a moment away" anywhere in the world

## MVP (Minimum Viable Product)
1. User registration and login
2. Profile creation
3. Matching feature
4. Chat functionality
5. Payment processing

## Future features to add
- Video calling
- Review and rating system
- AI recommendations
```

At this stage, you don't even need to talk to Claude. **Just write down the vision in your head**. That's enough.

---

## A2: Create /consult Skill

Create a "thinking partner" that always reads the document you created in A1 before responding.

```
.claude/skills/consult/SKILL.md
```

```markdown
---
name: consult
description: Discuss service requirements and planning decisions
---

# /consult - Service Requirements Discussion

## Prerequisites

Read the following document before answering:

1. `docs/service-overview.md` - Service Overview

## Behavior as a thinking partner

- Engage as an equal (don't be condescending)
- Acknowledge good ideas genuinely
- Voice concerns frankly if you have them
- Don't stop at "that's good" — dig deeper

## Core of the Service (always keep in mind)

> (Copy vision and values from A1 document here)
```

> **Why turn it into a skill?**
> You can bounce ideas with Claude directly, but as conversations grow long and you clear context or restart in a new session, the service background knowledge resets. By making it a skill, **it reads the service overview before responding every single time**, ensuring consistent discussion quality.

---

## A3: Bounce Ideas with /consult

Once the skill is ready, start bouncing ideas.

```
You: /consult
Claude: I'm ready. What would you like to discuss?

You: I want feedback on the MVP feature list. Does it seem complete?

Claude: A few things stand out:
        - Is payment processing really needed for MVP? You could validate
          without it first, then add it after confirming PMF.
        - I don't see notifications. How will you notify users after matching?
        - ...

You: You're right. Let's move payments to Phase 2 and add push notifications.

Claude: Good call. So the revised MVP would be...
```

Keep the outcomes of idea bouncing in `docs/service-overview.md`. As the consult skill's reference documents become richer, it gets smarter.

> **Critical: Always save discussion results in documents**
> Consult conversations disappear when the session ends. Once the discussion solidifies, instruct Claude to "save this to `docs/service-overview.md`" to make it permanent. Without documented persistence, you'll have to explain everything from scratch in the next session. This same pattern applies in Phase B too—"planning → save as specification document" becomes the fundamental workflow ([see Step 2.5](workflow-daily.md#step-25-persistence--save-plan-as-specification-document)).

---

## A4: Decide on Architecture

Once requirements are solid, decide the technical **"how to build it"**. **This is a prerequisite for creating sub-agents**.

```
You: Requirements are locked in, so I want to decide architecture.
     Check docs/service-overview.md for the requirements.
     Please propose from these angles:
     - Frontend (Web? Mobile? Both?)
     - Backend (framework, DB)
     - Infrastructure (AWS? GCP? Vercel?)
     - Design pattern (Monolith? Microservices?)
     - Directory structure
```

Claude will present multiple options. Discuss and decide. Once decided, record as **`docs/architecture.md`**:

```markdown
# Architecture

## Technology Stack
- Frontend: React Native (Expo) — Mobile app
- Backend: Node.js + Express + TypeScript
- DB: MySQL + Prisma ORM
- Infra: AWS (Lambda, API Gateway, RDS, S3)
- Design: Clean Architecture + DDD

## Directory Structure
src/
├── domain/        # Entities, Repository IF, Use Cases
├── infrastructure/ # DB, external APIs, storage
├── interface/      # Express routes, controllers
└── ...
```

---

## A5: Create CLAUDE.md

Once architecture is decided, create an **instruction manual for Claude**.

```markdown
# CLAUDE.md

## Project Overview
Platform for managing restaurant reservations and customer reviews.

## Technology Stack
- Backend: Node.js + Express + TypeScript + Prisma
- Frontend: React Native (Expo)
- DB: MySQL

## Important Rules
- Always execute backend commands inside Docker
- Tests must pass before committing
- Refer to specs in docs/ directory

## Directory Structure
(Copy from A4)

## Reference Documents
- docs/service-overview.md — Service overview
- docs/architecture.md — Architecture
```

---

## A6: Create Sub-agents

**Because architecture is decided, you can define each agent's specialty.**

Start with a minimum of three agents:

| Order | Agent | Reason |
|-------|-------|--------|
| 1 | **system_architect** | Keeper of overall design. Source of truth for other agents' rules |
| 2 | **developer** | Full-stack implementation specialist per architecture |
| 3 | **qa_engineer** | Test creation, quality management |

As the project grows and requires division of labor, add tech_researcher, frontend_developer, ui_ux_designer, etc. See [Sub-agents](sub-agents.md) for details.

What each agent should contain:

```markdown
---
name: developer
description: Full-stack specialist using React + Express + SQLite. (← Architecture-dependent)
---

# Role
Full-stack specialist in React, Node.js (Express), SQLite.

# Goals
1. Implement features following specs in docs/
2. Maintain Clean Architecture patterns    ← Architecture-dependent

# Constraints
- If spec changes needed, defer to architect ← Architect dependency
```

> **Why architecture first?**
> To write "SQLite for persistence" and "Clean Architecture follower" in `developer`'s definition, those technology choices must already be confirmed. Without decided architecture, you'll end up rewriting all agents later.

---

## A7: Create Additional Skills & Hooks

Final infrastructure setup.

```
.claude/
├── skills/
│   ├── consult/SKILL.md     ← Created in A2
│   ├── commit/SKILL.md      ← Commit rules
│   └── review/SKILL.md      ← Code review
├── agents/
│   ├── system_architect.md  ← Created in A6
│   ├── developer.md         ← Full-stack implementation
│   └── qa_engineer.md       ← Quality management
└── settings.json            ← Hooks (auto-format, etc.)
```

> Add tech_researcher, frontend_developer, etc. as needed. See [Sub-agents](sub-agents.md) for details.

**Now the foundation is complete. Let's move to [Phase B](workflow-daily.md).**
