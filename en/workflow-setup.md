# Development Workflow Phase A: Project Initialization

[< Back to Guide](../README.en.md) | [Phase B: Daily Development Cycle >](workflow-daily.md)

---

Development with Claude Code follows a golden rule: **think before you build**. This section introduces a workflow for launching projects from scratch.

When starting a new project, jumping straight into coding leads to getting lost. Instead, we systematically lay the **foundation for Claude Code to work intelligently**, step by step.

> You can run these steps interactively with the [/kickstart skill](kickstart-skill.md). Complete templates for every file created in each step are in [skills/kickstart/SKILL.md](skills/kickstart/SKILL.md).

## Overall Flow and Dependencies

```
Phase A: Project Initialization

  A0. Initialization
      │  docs/ structure, documentation policy, .gitignore, git init
      ▼
  A1. Create Requirements Document
      │  Put "what to build", "principles to keep",
      │  and "what we won't build" into words
      ▼
  A2. Create /consult Skill
      │  Build a thinking partner who reads A1
      ▼
  A3. Bounce Ideas with /consult
      │  Lock down feature list, MVP, priorities
      ▼
  A4. Decide Base Spec                 ← Branching point
      │  Tech stack, directory structure,      Developer agent contents
      │  branch strategy, common commands      depend on this
      ▼
  A4.5. Implementation Policy
      │  Decide which way to lean when in doubt
      ▼
  A5. Create CLAUDE.md
      │  A thin file: an index and a few rules
      ▼
  A6. Create Sub-agents
      │  advisor / developer / qa-engineer / code-reviewer
      ▼
  A7. Skills, Commit Guard, Initial Commit
      │  /ask-advisor, /commit, hooks that block secrets
      ▼
  A8. Runbook Skills (optional)
      │  Irreversible operations such as deploys and migrations
      ▼
  ─────────────────────────────
  Phase B: Daily Development Cycle
```

> **Key Point**: A4 (Base Spec) must come before A6 (Sub-agents).
> Only after you decide "Backend is Express + Prisma" can you define an agent like "a developer who implements with Prisma ORM".

## Document Structure

The documents created in Phase A fall into **ones you keep** and **temporary ones**.

```
docs/
├── README.md                  ← Documentation policy (what goes where)
├── requirements.md            ← Requirements and principles to keep (A1)
├── spec.md                    ← Base spec. Only the stable skeleton (A4)
├── implementation-policy.md   ← Implementation policy. Which way to lean when in doubt (A4.5)
├── decisions/                 ← Why we decided it. One decision per file
│   └── 0001-orm-prisma.md
└── _wip/                      ← Detailed design during implementation (promote or delete when done)
```

- **The source code is the source of truth for detailed design.** Table definitions and API details live in `docs/_wip/` only while you implement. When the implementation is done, move anything that counts as requirements, base spec, or reasoning behind a decision into docs/, and delete the rest. This prevents documents and source from drifting apart
- **Record decisions in `docs/decisions/`.** The key is to write not just "what we decided" but also "rejected alternatives" and "when to revisit". Six months later you'll know why things are the way they are, and whether it's OK to change them now

---

## A0: Initialization

Create the `docs/` structure, `docs/README.md` (documentation policy), and `.gitignore`, then initialize git. `docs/README.md` describes the structure above and how to write decisions:

```markdown
# NNNN Title

- Date: YYYY-MM-DD
- Status: Accepted / Superseded (→ NNNN)
- Decided by: Human / Consulted advisor (name of the consulting agent)

## Decision
## Reasons
## Rejected alternatives and why
## Evidence
## When to revisit
```

When a decision changes, don't rewrite the old file. Create a new one and mark the old one "Superseded".

---

## A1: Create a Requirements Document

Create `docs/requirements.md`, a **Markdown file describing the project's requirements**. This becomes the foundation for everything.

What to write:

```markdown
# Requirements

## Service Name
(You can use a placeholder)

## What are we building? (One sentence)
Example: A platform for restaurant reservation and review management

## Target Users
Example: Independent restaurants and their regular customers

## Principles to Keep
- Never log personal information
- Any action on the restaurant side finishes within 3 taps
- AI never rewrites review ratings

## What We Won't Build
- Rankings like gourmet sites
- Comparison between restaurants

## Final Vision
Example: A place where small restaurants can nurture relationships with their regulars

## MVP (Minimum Viable Product)
1. User registration and login
2. Accepting and confirming reservations
3. Posting reviews

## Future features to add
- Payments
- Notifications
```

> **Why "principles to keep" and "what we won't build" matter**
> These two become the **yardstick** that the advisor and code-reviewer use in reviews later. Instead of things anyone could say, like "make it easy to use", write **what this particular service must protect**.

At this stage, you don't even need to talk with Claude. Just **write down the image in your head**.

---

## A2: Create the /consult Skill

Build a "thinking partner who always reads your A1 document before answering".

```
.claude/skills/consult/SKILL.md
```

```markdown
---
name: consult
description: Consult on service requirements and planning
---

# /consult - Service Requirements Consultation

## Load Prerequisites

Always read these documents before answering:

1. `docs/requirements.md` - Requirements and principles to keep
2. `docs/spec.md` - Base spec (if present)
3. `docs/decisions/` - Past decisions related to the topic (if present)

## How to Behave as a Thinking Partner

- Discuss as equals (not condescending)
- Acknowledge good ideas honestly
- Voice concerns directly
- Don't stop at "That sounds good" — dig deeper

## Service Core (Always Keep in Mind)

> (Copy the vision, principles to keep, and what we won't build from A1)
```

> **Why make it a skill?**
> You can bounce ideas off Claude normally. But when conversations get long and you clear context, or resume in a new session, the service's prerequisite knowledge resets. A skill ensures Claude **always reads the requirements before answering**, so discussions stay consistently high quality.

---

## A3: Bounce Ideas with /consult

Once the skill is ready, bounce ideas relentlessly:

```
You: /consult
Claude: (Reads requirements) Ready. What would you like to discuss?

You: Review the MVP feature list. Does it look right?

Claude: The MVP is well organized, but a few things stand out:
        - How will reservation changes and cancellations work?
        - How will the restaurant be notified of a reservation?
        - ...

You: Good point. Let's put cancellation in the MVP and use email-only notifications.

Claude: Great. To reorganize the MVP...
```

Reflect what you settle on in `docs/requirements.md`. **Decisions with rejected alternatives**, like "payments are not in the MVP", also go into `docs/decisions/`.

> **Important: Always persist idea bouncing to documents**
> Consult conversations disappear when the session ends. Once the discussion solidifies, instruct Claude to "reflect this in `docs/requirements.md`" to make it permanent. Without documented persistence, you'll have to explain everything from scratch in the next session. This same pattern applies in Phase B too—"planning → save as a detailed design" becomes the fundamental workflow ([see Step 2.5](workflow-daily.md#step-25-persistence--save-plan-as-detailed-design)).

---

## A4: Decide the Base Spec

Once requirements are solid, decide **"how" to build it technically**. **This is the prerequisite for creating sub-agents.**

```
You: MVP requirements are solid. Let's decide the base spec.
     Requirements are in docs/requirements.md.
     Please compare multiple options from these perspectives:
     - Frontend (Web? Mobile? Both?)
     - Backend (framework, DB)
     - Infrastructure (AWS? GCP? Vercel?)
     - Design pattern (Monolith? Microservices?)
     - Directory structure
     - Branch strategy and environments (local / staging / production)
     - Common commands (type check, tests, dev server)
```

Claude will present multiple options. Discuss and decide. Once decided, record it as **`docs/spec.md`**. Write **only the stable skeleton** (table definitions and API details go into `docs/_wip/` during implementation).

```markdown
# Base Spec

## Tech Stack
- Frontend: React Native (Expo) — mobile app
- Backend: Node.js + Express + TypeScript
- DB / ORM: MySQL + Prisma
- Infra: AWS (Lambda, API Gateway, RDS, S3)
- Design pattern: Clean Architecture

## Directory Structure
src/
├── domain/         # Entities, repository interfaces, use cases
├── infrastructure/ # DB, external APIs, storage
├── interface/      # Express routes, controllers
└── ...

## Branches and Deployment
- Work on develop; main always works
- Environments: local / staging / production

## Common Commands
- Type check: npm run typecheck
- Tests: npm test
```

> **Pick a single entry point for type checking and tests.** This stops agents from reporting "it passed" based on a partial check.

Among your technology choices, record each one that had rejected alternatives (e.g., "Prisma rather than Drizzle for the ORM") in `docs/decisions/`, one file per decision.

---

## A4.5: Decide the Implementation Policy

Create `docs/implementation-policy.md`. It's not a detailed coding standard—it only records **which way to lean when in doubt**. When agents are unsure during implementation or review, they check here first.

| Area | What to decide (examples) |
|---|---|
| Logging | What may be logged (IDs, counts, durations) and what must not (personal info, secrets). When in doubt, don't log |
| External API calls | Timeouts, when to retry, what to show users on failure |
| On failure | Stop everything, or skip only the failed items and continue |
| Input and auth | Keep auth checks in one place, closed by default |
| Tests | Whether to replace external services with fakes |
| UI | Minimums for text size and tap-target size |

Skip any area that doesn't apply. The trick is to derive each lean from the "principles to keep" in A1.

---

## A5: Create CLAUDE.md

Once the base spec is decided, create **instructions for Claude**. Keep CLAUDE.md to **an index and a few rules**.

```markdown
# Restaurant Reservation Platform

Manages reservations and reviews for independent restaurants.

- Requirements and principles to keep: docs/requirements.md (always read before working)
- Base spec: docs/spec.md
- Implementation policy (which way to lean when in doubt): docs/implementation-policy.md
- Why we decided it: docs/decisions/
- Documentation policy: docs/README.md

## Common Commands
- Type check: `npm run typecheck`
- Tests: `npm test`

## Rules
- The source is the source of truth for detailed design. If docs and source disagree, trust the source
- Never commit secrets (the pre-commit hook blocks them; don't skip the hook)
- Work on develop. Keep main always working
- Each agent's role and workflow are in its definition file under .claude/agents/
```

> **Why not write procedures here?**
> CLAUDE.md is loaded into every conversation and every agent. Procedures like "run tests and review before committing" only need to live in the definition file of the agent that performs them. The shorter CLAUDE.md is, the more reliably its rules are followed.

---

## A6: Create Sub-agents

**Because the base spec is decided, you can define each agent's area of expertise.**

Start with four agents:

| Agent | Model | Role |
|------|------|------|
| **advisor** | opus | Read-only advisor. Consulted on choices that change principles, data shape, or user experience, and does the milestone review |
| **developer** | sonnet | Implementation. Commits only after passing qa-engineer and code-reviewer |
| **qa-engineer** | sonnet | Testing. Doesn't trust the implementer's "it passed"—runs the tests itself |
| **code-reviewer** | sonnet | Light review on every commit. Looks only at the staged diff |

The key is to **separate heavy judgment (advisor) from frequent, light review (code-reviewer)**. This keeps usage of the expensive model down while maintaining the quality of decisions. See [Sub-agents](sub-agents.md) for the thinking behind each agent and how to write them.

The developer definition might contain something like this:

```markdown
---
name: developer
description: Implements the restaurant reservation platform with Express + Prisma. (← depends on base spec)
model: sonnet
---

## Read first
- docs/requirements.md, docs/spec.md, docs/implementation-policy.md

## Scope of consultation
- Consult the advisor on decisions touching principles or data shape   ← name who to consult
- Record what you decided after consulting in docs/decisions/ yourself

## Pre-commit flow
1. Pass npm run typecheck and npm test                                 ← depends on base spec
2. Ask qa-engineer to test
3. git add only the files you touched; check with git diff --cached --stat
4. Ask code-reviewer to review
5. Commit
```

> **Why must the base spec come first?**
> For example, to write "persist with Prisma" or "pass `npm run typecheck`" in the `developer` definition, those technology choices must be locked in. Creating agents before the base spec is decided means rewriting all of them later.

---

## A7: Create Skills and the Commit Guard

The final touch on your development infrastructure.

```
.claude/
├── skills/
│   ├── consult/SKILL.md      ← Created in A2
│   ├── ask-advisor/SKILL.md  ← Consult the advisor
│   └── commit/SKILL.md       ← Commit rules
├── agents/
│   ├── advisor.md
│   ├── developer.md
│   ├── qa-engineer.md
│   └── code-reviewer.md
├── hooks/
│   └── guard-bash.mjs        ← Hook that checks commits
└── settings.json             ← Hook registration
.githooks/pre-commit          ← Also checks human commits
scripts/check-staged.sh       ← Check script called by both
```

- **/ask-advisor**: A skill that sends a question to the advisor with `context: fork`. You get a decision without cluttering the main conversation (see [Skills](skills.md))
- **Commit guard**: Mechanically blocks commits of secrets and DB files. For why it's placed in two layers—a git hook and a Claude Code hook—see [Security Basics](security.md#commit-guard--stop-secrets-mechanically)

---

## A8: Runbook Skills (optional)

For **operations that can't be undone if you get them wrong**—production deploys, DB migrations, registering secrets—it's safer to turn the procedure into a skill. Write into the procedure that the "local → staging → production" order must never be skipped, and that a human must always confirm before production. See [Skills](skills.md) for the template.

If you haven't decided on these yet, it's fine to create them when you need them.

**Once you reach here, your development foundation is complete. Move on to [Phase B](workflow-daily.md).**
