---
name: kickstart
description: Start a new project from scratch. Follow Phase A procedures, building the foundation step by step — requirements, base spec, and implementation policy through CLAUDE.md, agents, skills, and a commit guard.
disable-model-invocation: true
---

# /kickstart - Project Startup Guide

Build the foundation for a new project following Phase A procedures. Proceed through each step, **confirming completion before moving to the next one.**

## How to Proceed

- Show the user the current step number and name, progressing through dialogue
- Advance **one step at a time with confirmation**, not all at once
- Ensure all **completion criteria** for each step are met before proceeding
- Wait for the user to say "OK," "next," etc. before moving to the next step
- If uncertain, **offer choices and let the user decide** (don't decide alone)
- For any decision made during a step that **had rejected alternatives**, record it in `docs/decisions/` (format in A0's `docs/README.md`)

## Model Selection

- A1-A3 (concept and requirement brainstorming): Sonnet is sufficient
- A4-A4.5 (base spec and implementation policy): **Opus recommended** (deep design judgment needed)
- A5-A8 (file creation): Sonnet is sufficient

If the recommended model differs from current at step start, guide the user to switch with `/model`.

---

## A0: Project Initialization (Automatic)

Run automatically at the start. User confirmation not needed.

### Create Directory Structure

```
docs/
├── README.md     ← Documentation policy (what goes where)
├── decisions/    ← Why we decided things (one decision per file)
└── _wip/         ← Detailed designs in progress (promote or delete when done)
```

Place a `.gitkeep` in `docs/_wip/` and `docs/decisions/`.

### Create docs/README.md

Create it with the following content.

````markdown
# Documentation Policy

## What we keep (directly under docs/)

| Kind | Location | Contents |
|---|---|---|
| Requirements | requirements.md | Purpose, principles to keep, what we won't build, what must be satisfied |
| Base spec | spec.md | Tech stack, high-level data flow, directory structure, branches and deployment. Only the skeleton that rarely changes |
| Implementation policy | implementation-policy.md | Which way to lean when in doubt. Don't write what can be read from the source |
| Why we decided | decisions/ | What was decided, rejected alternatives, evidence, conditions for revisiting |

Tasks (things to do) are not managed here; they live where spec.md's "Task Management" section says. Finished tasks are not kept (git history and the source record what was done).

## Detailed designs (docs/_wip/)

- Write `docs/_wip/<topic>.md` when starting implementation. Table definitions, API shapes, screen details, etc. go here
- Clean up when implementation is done
  - Move anything that is requirements, base spec, or a reason for a decision into docs/
  - Delete the rest (the source holds that content)
- The source is the truth for detailed design. If docs/ and the source disagree, trust the source

## How to write "why we decided"

Write one decision per file in `decisions/NNNN-short-name.md`. Number sequentially.

```markdown
# NNNN Title

- Date: YYYY-MM-DD
- Status: Adopted / Superseded (→ NNNN)
- Decided by: Human / Consulted advisor (name of consulting agent)

## Decision
## Reasons
## Rejected alternatives and why
## Evidence (doc URLs, measurements, commits, etc.)
## Conditions for revisiting (what would make us reconsider)
```

When a decision changes, don't rewrite the old file. Create a new file and set the old file's status to "Superseded."
````

### Create .gitignore

Create `.gitignore` in project root with common items (tech-stack independent):

```gitignore
# Environment variables and secrets
.env
.env.*
!.env.example

# Credentials
credentials.json
*.pem
*.key
service-account.json

# Claude Code personal settings
.claude/settings.local.json

# OS and editors
.DS_Store
Thumbs.db
*.swp
.vscode/settings.json
.idea/
```

> **Note**: Tech-specific items (`node_modules/`, `__pycache__/`, `vendor/` etc.) are added after the A4 base spec decision.

### Verify git Initialization

If `.git/` doesn't exist, run `git init`.

**Completion criteria**: Directory structure, `docs/README.md`, and `.gitignore` created.

---

## A1: Requirements Document

Ask the user the following questions to create `docs/requirements.md`:

### What to Ask

- **What are you building** (in one sentence)
- **Who is the target** (user demographics)
- **Principles to keep** (non-negotiables; the yardstick for decisions when in doubt)
- **What we won't build** (similar things we don't aim for, things we won't do)
- **Long-term vision (final goal)**
- **MVP (minimum viable features)** — each feature in one specific line
- **Future features to add**

### How to Ask

- Don't ask all at once; naturally explore in conversation
- For vague answers, dig deeper: "What would that look like specifically?"
- Agents will later use "principles to keep" as a review yardstick. Draw out **what this particular service must protect**, not generic things like "easy to use" (e.g., "never log personal information," "don't push decisions onto the user")
- If "what we won't build" doesn't come up, ask: "Compared to similar services, what will you deliberately not do?"
- If MVP exceeds 5 features, check: "Do you really need all for MVP? Anything deferrable?"
- If the user seems uncertain, offer specific choices

### Document Template

```markdown
# Requirements

## Service Name
(Tentative is fine)

## What Are You Building
(One sentence)

## Target Users
(Who's it for)

## Principles to Keep
- ...
- ...

## What We Won't Build
- ...

## Vision (Final Goal)
...

## MVP (Minimum Viable Features)
1. ...
2. ...

## Future Features to Add
- ...
```

**Completion criteria**: `docs/requirements.md` created and user confirmed the content with "OK."

---

## A2: Create /consult Skill

Create `.claude/skills/consult/SKILL.md` based on the A1 document.

### Content to Include

```markdown
---
name: consult
description: Discuss service requirements and planning
---

# /consult - Service Requirements Discussion

## Load Prerequisites

Always read these documents before answering.

1. `docs/requirements.md` - Requirements and principles to keep
2. `docs/spec.md` - Base spec (if it exists)
3. `docs/decisions/` - Past decisions relevant to the discussion (if any)

## Behavior as a Sounding Board

- Discuss as equals (don't talk down)
- Acknowledge good ideas honestly
- Raise concerns frankly
- Don't stop at "that's nice" — dig deeper
- When useful, check the implementation status and say what's possible now

## Avoid

- Jumping straight into implementation (sort out requirements first)
- Being overly optimistic or pessimistic
- Agreeing with the user uncritically

## Core of the Service (always keep in mind)

> (Copy the vision, principles to keep, and what we won't build from the A1 document)
```

Copy the **actual content** of the vision, principles to keep, and what we won't build from `docs/requirements.md` created in A1. Don't leave the template as-is.

**Completion criteria**: `.claude/skills/consult/SKILL.md` created with service-specific content.

---

## A3: Brainstorm Requirements with /consult

Guide the user as follows:

```
The consult skill is ready.
Let's start brainstorming. We'll dig into requirements from these angles:

- Are the MVP features complete, with nothing extra?
- Are priorities right?
- Are any features missing (auth, notifications, error handling, search, etc.)?
- User experience flow (main operation flows)
- Are the principles to keep and what we won't build sufficient?

Results will be reflected in docs/requirements.md.
Let's start by reviewing the MVP feature list.
```

### Angles to Check While Brainstorming

- **User flow**: Flow of main operations (sign up → log in → main feature → ...)
- **Permissions**: Is a distinction between admins and users needed?
- **Notifications**: Are email or push notifications needed?
- **Search/filter**: How to find things as data grows
- **Error cases**: Behavior when main operations fail
- **Data lifecycle**: Soft delete or hard delete? What happens when a user asks to be deleted?

### Important: Persist Brainstorming Results

Once the discussion settles, always update `docs/requirements.md`.
Decisions that had rejected alternatives (e.g., "payments are not in the MVP") also go in `docs/decisions/`.
Conversations disappear when the session ends; documents remain.

**Completion criteria**: User is satisfied with the MVP requirements and `docs/requirements.md` is updated.

---

## A4: Base Spec Decision ← The Turning Point

> **Opus is recommended for this step.** Switch with `/model opus`.

**A6 agents can't be created until this is decided.**

### Angles to Discuss

Discuss these **one at a time** with the user. For each, present multiple options, build a comparison table, and let the user choose.

1. **Platform**: Web / mobile / desktop / both
2. **Language**: TypeScript, Python, Go, Rust, Ruby, Java, etc.
3. **Frontend**: React, Next.js, Vue, Svelte, Flutter, etc. (if applicable)
4. **Backend**: Express, Hono, Django, FastAPI, Rails, Gin, Echo, etc.
5. **Database**: PostgreSQL, MySQL, SQLite, MongoDB, etc.
6. **ORM/data access**: Prisma, Drizzle, SQLAlchemy, GORM, ActiveRecord, etc.
7. **Infrastructure**: AWS, GCP, Vercel, Cloudflare, self-hosted, etc.
8. **Design pattern**: Monolith, microservices, Clean Architecture, etc.
9. **Directory structure**: Propose a structure suited to the chosen stack
10. **Branches and deployment**: Working branch (e.g., work on `develop`, keep `main` always working), whether to use Pull Requests, environments (local / staging / production)
11. **Common commands**: Test, type check (static analysis), dev server, build. **Settle on a single entry point each for type checking and tests** (e.g., `npm run typecheck`, `npm test`)
12. **Where tasks live**: Where to keep the list of things to do. Present these two options in a comparison table and let the user choose

| Aspect | File in the repo (`docs/tasks.md`) | GitHub Issues (operated via `gh`) |
|---|---|---|
| Good fit | Solo development, not using GitHub | Team development, using Pull Requests |
| Strengths | No extra tools. Status changes in the same commit as the code | No conflicts from simultaneous edits. Links to PRs and comments |
| Watch out for | Conflicts easily when several people edit at once | Needs `gh` authentication. Writes outside the repo, so get human confirmation before creating |

If the user is unsure, recommend the file for solo work and GitHub Issues for teams. If they want another tool (Linear, Jira, etc.), confirm it can be read and written via MCP, then build it along the same lines as the GitHub Issues option.

### Decision Criteria (explain to the user)

- **Team experience**: Prefer technologies you've used
- **MVP speed**: Prefer what's quick to build
- **Learning goals**: Consider new technologies if you want to try them
- **Scalability**: Future extensibility
- **Ease of switching**: Can parts that depend heavily on a specific service sit behind a swappable layer?

### Proposal Format (example)

```
| Angle | Option A | Option B | Option C |
|------|-----|-----|-----|
| Frontend | Next.js | React + Vite | React Native |
| Why | SSR, great with Vercel | Simple, low learning cost | Mobile app |
| Best for | Web apps needing SEO | SPA | iOS/Android |
```

### Recording the Decision

Record it in `docs/spec.md` with the following structure. Write **only the skeleton that rarely changes** (no table definitions or API details — those go in `docs/_wip/` during implementation).

```markdown
# Base Spec

## Tech Stack
- Frontend: ...
- Backend: ...
- DB / ORM: ...
- Infra: ...
- Design pattern: ...

## High-Level Data Flow
(Where main data comes in, where it's stored, where it goes out)

## Directory Structure
(Tree format)

## Branches and Deployment
- Working branch: ...
- Environments: local / staging / production
- Deployment method: ...

## Task Management
- Location: docs/tasks.md / GitHub Issues (<owner>/<repo>)
- Add and close tasks with the /task skill

## Common Commands
- Type check: ...
- Test: ...
- Dev server: ...
```

### Recording Decisions

For tech choices **with rejected alternatives**, record one decision per file in `docs/decisions/` using the format from A0's `docs/README.md`.

```markdown
# 0001 Choose Prisma as the ORM

- Date: YYYY-MM-DD
- Status: Adopted
- Decided by: Human

## Decision
Use Prisma as the ORM.

## Reasons
Prioritized type safety and convenient migration management.

## Rejected alternatives and why
- Drizzle: Lightweight and close to SQL, but nobody on the team has experience with it
- TypeORM: Proven, but maintenance has stalled

## Evidence
- (Official doc URLs, etc.)

## Conditions for revisiting
- When we need to run on an Edge runtime
```

### Update .gitignore

Now that the stack is settled, append tech-specific items to the `.gitignore` created in A0.

Examples:
- Node.js: `node_modules/`, `dist/`, `build/`
- Python: `__pycache__/`, `.venv/`, `*.pyc`
- Go: Usually nothing to add (specify the binary name)
- Ruby: `vendor/bundle/`, `.bundle/`
- If using a local DB file (SQLite, etc.): that file

The choice of where tasks live also has a rejected alternative, so record it in `docs/decisions/`.

**Completion criteria**: `docs/spec.md` created; tech stack, directory structure, branch workflow, task location, and commands settled; `.gitignore` updated for the stack.

---

## A4.5: Decide the Implementation Policy

> Opus still recommended.

Create `docs/implementation-policy.md`. This is not a detailed coding standard; it only states **which way to lean when in doubt**. When agents are unsure during implementation or review, they check here first.

### How to Proceed

Present the following angles one at a time and decide with the user how this service should lean. **Skip angles that don't apply.** For each angle, first propose the leaning that follows from the requirements' "principles to keep."

| Angle | What to decide (examples) |
|---|---|
| Logging | What may be logged (IDs, counts, durations, error types) and what may not (personal info, content bodies, tokens, secrets). **When in doubt, don't log it** |
| External API calls | Timeouts, when to retry and when not to, what the user sees on failure |
| On failure | Stop the whole process, or skip only what failed and continue? Does running twice give the same result (idempotency)? |
| Input and auth | Centralize auth checks in one place and close by default (list the entry points that skip checks) |
| Data | Keep what users entered separate from what the system inferred or generated |
| Testing | Replace external services with fakes? When do we call the real thing? |
| UI (if applicable) | Minimums for font size, tap target size, contrast ratio, etc. |
| If calling an LLM | Receive structured output and validate its contents, keep a single model-per-use-case table, compare before/after outputs side by side when changing prompts |

### Template

```markdown
# Implementation Policy (which way to lean when in doubt)

Not detailed rules — only which way to lean when in doubt. The source is the truth for how things were implemented.

## Logging
- OK to log: ...
- Don't log: ...
- When in doubt, don't log it

## External API Calls
- ...

## On Failure
- ...

(Then only the angles you decided)
```

Record the reasons for leanings that had rejected alternatives in `docs/decisions/`.

**Completion criteria**: `docs/implementation-policy.md` created and the user said OK.

---

## A5: Create CLAUDE.md

> **Switch back to Sonnet.** `/model sonnet` is fine.

**Actually read** the A1-A4.5 outputs, then create `CLAUDE.md` in the project root.

Keep CLAUDE.md to **an index and promises only**. Content goes in docs/, and each agent's workflow goes in its own definition file in `.claude/agents/`. Every conversation and agent loads CLAUDE.md, so procedures written there get ignored more as the file grows.

### Template

```markdown
# <Service Name>

<What you're building (one sentence)>

- Requirements and principles: [docs/requirements.md](docs/requirements.md) (always read before working)
- Base spec: [docs/spec.md](docs/spec.md)
- Implementation policy (which way to lean when in doubt): [docs/implementation-policy.md](docs/implementation-policy.md)
- Why we decided: [docs/decisions/](docs/decisions/)
- Tasks: <[docs/tasks.md](docs/tasks.md) or GitHub Issues (<owner>/<repo>)>. Add and close them with `/task`
- Documentation policy (what goes where): [docs/README.md](docs/README.md)

## Common Commands

- Type check: `...`
- Test: `...`
- Dev server: `...`

## Promises

- The source is the truth for detailed design. If docs and source disagree, trust the source
- Never commit secrets (.env, API keys, credentials) — the pre-commit hook blocks them. Don't bypass the hook
- Work on `<working branch>`. (One line on the branch workflow decided in A4)
- Each agent's role and workflow is written in its definition file under `.claude/agents/`
```

### Must-Follow

- Aim for **50 lines or fewer** (Claude starts ignoring long files)
- Don't write what can be learned by reading the code
- Don't write obvious instructions like "write clean code"
- Put procedures (like the pre-commit flow) in agent definitions, not CLAUDE.md

**Completion criteria**: `CLAUDE.md` created with project-specific info and no procedures written into it.

---

## A6: Create Sub-agents

Create agents in `.claude/agents/` based on the A1-A4.5 outputs.

### Start with 4 Agents

| Agent | Model | Role |
|---|---|---|
| **advisor** | opus | Read-only consultant. Consulted on principles, data shape, screen flow, and choices that change the user experience; does a full review at milestones (when a chunk of features is done). Writes no code |
| **developer** | sonnet | Implementer. Passes qa-engineer and code-reviewer before committing |
| **qa-engineer** | sonnet | Tester. Doesn't trust the implementer's "it passed" — runs the tests itself. Doesn't fix app source |
| **code-reviewer** | sonnet | Light review on every commit. Looks only at the staged diff. Read-only |

> **Key**: Separating heavy judgment (advisor) from frequent light reviews (code-reviewer) keeps judgment quality high while limiting usage of expensive models. When the project grows and needs division of labor, add more — e.g., split developer into frontend-developer / backend-developer.

> **Using Fable**: Changing advisor's `model:` to `fable` improves the quality of consultations and milestone reviews. However, depending on your plan it may draw from usage credits (the `/model` picker shows "Requires usage credits"), so watch usage. Don't use it for the frequently-run code-reviewer. Ask the user "Use Fable for advisor?" and, if yes, record that decision in `docs/decisions/`.

### Template for Each Agent

**Actually fill in** each `<...>` from the A1-A4.5 content. Don't leave the template as-is.

#### advisor.md

````markdown
---
name: advisor
description: Advisor for all of <service name>. Use for consultations on principles (principles to keep, distance from what we won't build), data shape, screen flow, and choices that change the user experience. Also use for full reviews at milestones (when a chunk of features is done). Not for per-commit reviews (that's code-reviewer).
model: opus
tools: Read, Grep, Glob, Bash
---

You are the advisor for "<service name>". You don't write code. You return decisions and their reasons.

## Read First

- `docs/requirements.md` (principles to keep — this is the yardstick for decisions)
- `docs/spec.md`
- Relevant files in `docs/decisions/`
- The source is the truth for details. If docs and source disagree, trust the source and point out the discrepancy

## Job 1: Answer Consultations

1. **Conclusion**: Which to choose. Narrow it to one
2. **Reasons**: Which principle in requirements.md you checked against
3. **Rejected alternatives and why**
4. **Conditions for revisiting**
5. **Draft record**: A short text the consulting agent can copy straight into `docs/decisions/`

The consulting agent writes the record file. You don't.

### Watch Especially For

- <Bullets: from requirements.md's "principles to keep" and "what we won't build," things easy to overlook in decisions>

### When You Can't Decide

Say so when only a human can decide (changing the service's core idea, choices that cost money, operations involving production data). In that case, return the question to ask the human as a single sentence.

## Job 2: Milestone Full Review

Only when asked (when a chunk of features is done, end of day, etc.).

- Use `git log` and `git diff <previous milestone>..HEAD` to grasp changes since last time. If you don't know the previous milestone, ask the requester
- Check
  - Has anything strayed from the requirements and principles to keep?
  - Has anything strayed from the leanings in `docs/implementation-policy.md`?
  - Anything left uncleaned in `docs/_wip/` (to move or delete)?
  - Any unrecorded decisions missing from `docs/decisions/`?
  - Does the task list (<docs/tasks.md or GitHub Issues>) match reality? Tasks that are done but not closed, tasks stuck in progress for a long time
  - Is it in a state that can be merged into main and run?
- Return format: "Must fix (most serious first)," "Think about before next milestone," "What got better." Keep each short
- Mark items in "Must fix" and "Think about before next milestone" that would make good tasks with `→task`. The requester creates the tasks; you don't

## Don't

- Don't modify files
- Don't weigh in on fine implementation choices (how to split functions, details of library usage). If asked, reply "the implementation side can decide"
````

#### developer.md

````markdown
---
name: developer
description: Implements <service name> with <tech stack names, specifically (e.g., React + Hono + Drizzle)>. Use when asking for feature implementation or fixes.
model: sonnet
---

You implement "<service name>".

## Read First

- `docs/requirements.md` (principles to keep — always read)
- `docs/spec.md`
- `docs/implementation-policy.md` (which way to lean when in doubt — check implementation decisions here first)
- Relevant files in `docs/decisions/`
- The source is the truth for details. Don't trust the docs; read the source each time

## Tech Stack and Constraints

- <Tech stack from spec.md>
- <Constraints easy to trip over in this stack (runtime limits, unavailable APIs, etc.)>

## What to Consult On

Don't decide the following yourself; consult advisor (call `advisor` with the Agent tool).

- Anything involving principles to keep or what we won't build
- Data shape, screen flow, wording shown to users
- Choices with multiple options where the choice changes the user experience or the service's philosophy

You may decide fine implementation choices yourself (how to split functions, details of library usage, etc.).

When consulting, tell advisor: what you want to decide, the options you considered (two or more), pros and cons of each, and the relevant files.

### When a Human Decision Is Needed

If advisor replies that only a human can decide, don't decide it yourself. Stop there without committing and return: the question to ask the human (one sentence), the options you considered, advisor's assessment, and the files with uncommitted changes. How to ask the human is up to whoever called you.

### Recording Consulted Decisions

**You yourself** record decisions made through consultation in `docs/decisions/NNNN-short-name.md`, following `docs/README.md`. Write "Consulted advisor (developer)" in the "Decided by" field. Put the record in the same commit as the implementation that uses the decision.

## Detailed Design

- When starting implementation, write the detailed design (tables, API shapes, screen components, etc.) in `docs/_wip/<topic>.md`
- Clean up when done. Move requirements, base spec, and decision reasons into `docs/`; delete the rest

## Tasks

<Write only one of the following, matching the location chosen in A4>

(For docs/tasks.md)
- If `docs/tasks.md` has a task matching the requested work, confirm its ID before starting
- When done, move that task to "Done." Include this change in the same commit as the implementation

(For GitHub Issues)
- If there is an Issue matching the requested work, check its content with `gh issue view <number>` before starting
- Put `#<number>` in the commit message. Closing the Issue is done by a human or `/task done` (or a PR's `Closes #<number>`), not by you

Either way, don't create new tasks yourself. Write "things worth doing" you found during the work under "Task candidates" in your report.

## Don't Work in Parallel

- Only one implementing agent commits in the same working tree at a time. If asked to work in parallel, create a separate working tree with `git worktree` and work there (a shared staging area lets other work's files slip into your commit)

## Pre-commit Flow

1. Implement, then pass `<type check command>` and `<test command>` locally. Don't settle for a partial check
2. Call **qa-engineer** to request testing. Tell it what changed, the expected behavior, and the relevant files. If it fails, fix and ask again
3. `git add` only the files you touched, by explicit path. Don't use `git add -A` or `git add .`. Check `git diff --cached --stat` against the list of files you touched
4. Call **code-reviewer** to review the staged diff. Fix "must fix" items. After fixing, ask for review again
5. Commit (working branch is `<working branch>`)
   - The commit hook checks for secrets and the like. If it stops you, unstage that file. Don't bypass the hook (don't use `--no-verify`)

## What to Return

Finally, briefly report: what you did, test and review results, commit hash, decisions consulted and recorded, tasks handled, task candidates (things not done this time but worth doing; one line each).

- When you write "passed," paste the tail of the last type check and test output (counts, errors or not). Don't just say "passed" in words
````

#### qa-engineer.md

````markdown
---
name: qa-engineer
description: Handles testing for <service name>. Use when developer requests pre-commit testing. Writes and runs unit tests with <test framework name>.
model: sonnet
---

You handle testing for "<service name>".

## Read First

- `docs/requirements.md` (principles to keep — the basis for what tests should verify)
- `docs/spec.md`
- `docs/implementation-policy.md`
- The source is the truth for details. Don't trust the docs; read the source each time

## Pre-commit Testing

1. Read the requested change and the relevant source
2. Add missing tests. Run existing tests
3. Run `<type check command>` and `<test command>` **yourself**. Don't trust the implementer's "it passed"
4. Return results: whether it passed (paste the commands you ran and the tail of their output), what failed (which test and why), what tests couldn't verify

### Always Verify (when the change is relevant)

- <Bullets: from requirements.md's principles and implementation-policy.md, what tests can verify (e.g., can't be fetched without auth, no personal info in logs)>

### Test Data

- Use only fictional data. Never use real user data
- Replace external services with fakes (follow "Testing" in implementation-policy.md)

## What to Consult On

If unsure about a testing decision that involves the principles to keep, consult advisor. **You yourself** record consulted decisions in `docs/decisions/` ("Decided by": "Consulted advisor (qa-engineer)").

## Don't

- Don't modify app source to make tests pass. If you find something to fix, return it to the implementer who asked
- Don't commit. The implementer who asked commits
````

#### code-reviewer.md

````markdown
---
name: code-reviewer
description: Light review done on every commit. Looks only at the staged diff (git diff --staged). Call before the implementer commits. Not for heavy whole-project reviews (that's advisor).
model: sonnet
tools: Read, Grep, Glob, Bash
---

You handle per-commit reviews for "<service name>". Keep them light and fast.

## What to Do

1. Look at the diff with `git diff --staged`. If there's no diff, say so and stop
2. Check that the file list in `git diff --staged --stat` matches the requested change. If files from other work are mixed in, mark it "fix first"
3. Read only as much surrounding source as needed to understand the diff. Don't read the whole repository
4. Check the diff against the "principles to keep" in `docs/requirements.md` and the leanings in `docs/implementation-policy.md`

## What to Look For

- **Bugs**: Doesn't work, breaks on boundary values, swallows errors
- **Straying from principles**: <Bullets: principles to keep that are easy to spot in a diff>
- **Security**: Missing auth checks, personal info or secrets in logs, hard-coded keys
- **Docs**: A change that involves a decision but has no record in `docs/decisions/`

## Return Format

```
Verdict: OK to pass / Fix first
Must fix:
- file:line — what's wrong — how to fix
Worth noting (optional to fix):
- …
```

- Keep findings within the diff. For problems found outside the diff, write one line under "Worth noting" only
- Don't flag matters of taste (fine details of style)
- If you can't judge something about principles, write "Consult advisor." Don't decide yourself

## Don't

- Don't modify files. Don't commit
````

### Important

- **Description must include actual tech stack names** ("Builds the API with Express + Prisma" not "backend person")
- Fill the `<...>` bullets with **what is specific to this service** from requirements.md and implementation-policy.md. Don't fill them with generalities
- Use kebab-case agent names (`code-reviewer`)

**Completion criteria**: The 4 agents are in `.claude/agents/`, each reflecting the project's tech stack, commands, and principles.

---

## A7: Skills, Commit Guard, and Initial Commit

### Create /ask-advisor Skill

Create `.claude/skills/ask-advisor/SKILL.md` with the following content. With `context: fork` and `agent: advisor`, you can send a consultation to advisor without cluttering the main conversation.

A `context: fork` skill runs in the background by default, and the answer arrives later. Because we want to see the answer to the consultation before moving on, add `background: false` so it waits for the answer on the spot.

```markdown
---
name: ask-advisor
description: Consult advisor. Use when unsure about principles, data shape, screen flow, or choices that change the user experience. Also use to request a milestone full review.
argument-hint: <what to consult about, or "milestone review">
context: fork
agent: advisor
background: false
---

Answer the following consultation.

$ARGUMENTS

- For a consultation, answer in the "Job 1" format from your definition (conclusion, reasons, rejected alternatives, conditions for revisiting, draft record)
- If it says "milestone review," do "Job 2"
- If the consultation is too short to judge, return a list of the information missing to decide
```

### Create /commit Skill

Create `.claude/skills/commit/SKILL.md` with the following content. Use it when a human asks for a commit directly (when going through the developer agent, follow the "Pre-commit Flow" in its definition).

````markdown
---
name: commit
description: Execute git commits following project rules
disable-model-invocation: true
---

# /commit - Project Commit Skill

## Rules

1. **Separate by change**: One commit = one logical change
2. **Conventional Commits format**: `feat:`, `fix:`, `chore:`, `refactor:`, `docs:` etc.
3. **Add Co-Authored-By**: Always include
   ```
   Co-Authored-By: Claude <noreply@anthropic.com>
   ```
4. **Use HEREDOC for message**: Maintains format

## Steps

### 1. Check Changes
```bash
git status
git diff --stat
git log --oneline -5
```

### 2. Group Changes
Group changes into logical units.
- New features: `feat:`
- Bug fixes: `fix:`
- Refactoring: `refactor:`
- Docs: `docs:`
- Other chores: `chore:`

### 3. Commit Each Group
```bash
git add <related files by explicit path>
git diff --cached --stat   # confirm only the intended files are staged
git commit -m "$(cat <<'EOF'
<type>: <brief description>

<details (if needed)>

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

## Notes
- Don't use `git add -A` or `git add .`; specify files explicitly
- If the commit hook stops you, unstage that file. Don't use `--no-verify`
- Push only when the user explicitly asks
````

### Create /task Skill

Create `.claude/skills/task/SKILL.md`. It is the single entry point for viewing, adding, and closing tasks. **For the procedure part, write only the one for the location chosen in A4** (don't keep both).

````markdown
---
name: task
description: View the task list and pick what to do next, add tasks, close finished tasks. Use when starting work, or when "things to do" come up during work or a milestone review.
argument-hint: [add <content> | done <ID> | no argument for the list and next candidate]
---

# /task - Task Management

Location: <docs/tasks.md or GitHub Issues (<owner>/<repo>)>

## No argument: list and next candidate

1. If there are items "Awaiting Human Decision," show them first (left by `/overnight`)
2. List tasks in progress and not started
3. Against the MVP and principles in `docs/requirements.md`, recommend one to do next, with a one-line reason
4. When the human picks one, mark it in progress

## Answering items awaiting decision

When the human answers an item "Awaiting Human Decision":

1. If there were rejected alternatives, record it in `docs/decisions/` (Decided by: human)
2. If something was provisionally implemented ("provisionally did X") and the answer differs, add a task to fix it
3. Move the waiting tasks back to "Next" and remove the item

## add <content>

1. Split the content into "what to do" and "done when (how we know it's finished)." If it's too vague to write a done-when, ask the human
2. Check it doesn't overlap with existing tasks
3. Add it. When there are several (developer's task candidates, advisor's `→task`, etc.), list them and confirm with the human before adding

## done <ID>

1. Confirm the done-when is met, using commits and test results. If not, return what's missing and don't close it
2. Close it

## Procedure (for docs/tasks.md)

- Follow the format at the top of `docs/tasks.md`. IDs are `T-` followed by a sequential number (e.g., `T-012`). Never reuse an ID
- Move to "In Progress" when starting, and to "Done" when closing
- Delete "Done" items after the milestone review (history stays in git)
- After changes, commit with `/commit` (starting with `docs:`)

## Procedure (for GitHub Issues)

- List: `gh issue list --state open`
- Add: `gh issue create --title "<what to do>" --body "<done when>"`. **Show the title and body to the human and get confirmation before creating** (it writes outside the repo; the commit guard's hook and settings also prompt for confirmation)
- Mark in progress: `gh issue edit <number> --add-assignee @me`
- Close: `gh issue close <number> --comment "<commits that handled it>"`
````

#### Create docs/tasks.md (if the file was chosen)

````markdown
# Tasks

Format: `- [ ] T-001 What to do — Done when: … — Design: docs/_wip/<topic>.md (if any)`
Add and close tasks with `/task`. Delete "Done" items after the milestone review.
Format for items awaiting decision: `- Question — Options: … — From: T-003 — Waiting tasks: T-005 (or "none")`

## Awaiting Human Decision

## In Progress

## Next (top to bottom)

## Someday

## Done
````

### Create the First Tasks

Create the first tasks from the MVP in `docs/requirements.md`.

- One MVP feature becomes one task. Split features that are too big (ones that won't finish in a single request)
- Order them by the priority decided in A3. Put "features to add later" under "Someday" (for GitHub Issues, don't create them)
- Show the list to the human and write it only after getting OK. For GitHub Issues, check authentication with `gh auth status` at this point

### Create /overnight Skill

Create `.claude/skills/overnight/SKILL.md`. Typed before going to bed, it implements the delegated tasks in order until morning.

Normally (while the human is awake), when a decision is needed, the human is asked on the spot. That already happens through developer's "When a Human Decision Is Needed" and the main conversation's flow. **Keep the rules for while the human sleeps inside this skill; don't write them into agent definitions.** Set `disable-model-invocation: true` so the overnight behavior starts only when the human types it.

Fill in `<...>` from A4–A7. As with `/task`, keep only the variant matching the chosen task location.

````markdown
---
name: overnight
description: Implements delegated tasks in order while the human sleeps. After the up-front confirmation, never asks the human; leaves points needing a decision in the list and moves on.
argument-hint: [limit (e.g., 3 tasks, 6 hours; omit for no limit)]
disable-model-invocation: true
---

# /overnight - Advance Tasks While You Sleep

## Before Starting (the only time to ask the human)

1. Check with `git status` that the working tree is clean. If not, say so and stop
2. Show the task list and have the human choose which tasks to delegate. Recommend every task in "Next" that has a done-when (worked from the top). Don't delegate tasks without a done-when
3. Decide the limit: number of tasks or time (use $ARGUMENTS if given; otherwise no limit — work through all the delegated tasks)
4. Check the setting that continues automatically after a usage limit resets (`autoContinueAtUsageLimit`; in `/config`, **Continue automatically at usage limit**; on by default)
   - Read `~/.claude/settings.json`. If it's `false`, it's off
   - If the user settings don't have this key but `.claude/settings.json` or `.claude/settings.local.json` does, it's off regardless of the value (this key is read only from user and managed settings; setting it in a project turns it off)
   - Managed settings may override it, so finally ask the human to check in `/config`
   - If it's off, ask the human whether to turn it on. The human turns it on in the `/config` panel (the `/config autoContinueAtUsageLimit=true` form can't turn it on). If it stays off, tell them work will stop at the usage limit until morning
5. Create and switch to `overnight/YYYY-MM-DD` from `<working branch>`
6. Tell the human the following and get OK
   - No more questions until morning
   - To avoid stalling on permission prompts, it has to run in auto mode. Ask them to check that `auto mode on` is shown at the bottom of the screen
   - If it isn't, ask them to press `Shift+Tab` a few times to switch to auto mode (Claude Code normally starts in auto mode, but they may have set a different mode in settings)
   - No push or deploy. In the morning, review `overnight/YYYY-MM-DD` before merging (on `overnight/` branches, the hook rejects push and creating PRs and Issues)
   - If work stops at a usage limit, it continues automatically only when: Claude Code stays open (closing it ends the wait), they're signed in with a claude.ai subscription, the reset is within 24 hours (it won't wait for a weekly limit), and it has continued automatically no more than 3 times
   - Don't let the computer sleep. If the limit resets during a sleep of more than about 30 minutes, it stops until someone presses Enter (on macOS, run `caffeinate -i` in another terminal)

Once you have OK, don't ask the human anything after that.

## How to Proceed

Work through the delegated tasks from the top, one at a time.

1. Mark the task in progress
2. Call a fresh developer. Tell it:
   - The task ID and done-when
   - This is overnight work and the human can't be asked. If a point needing a human decision comes up, stop and return per "When a Human Decision Is Needed" in its definition
   - Commit to `overnight/YYYY-MM-DD`
3. Branch on developer's report
   - Done: next task
   - Human decision needed: go to "When a Human Decision Is Needed" below
   - Tests or review still fail after fixing: stash the uncommitted changes with `git stash push -m "<ID> failing"`, move the task to awaiting decision with what fails, and go to the next task
4. When the limit is reached (with no limit, when the delegated tasks are done) or no task can proceed, write the "Morning Report" and finish

## When a Human Decision Is Needed

1. Add it to awaiting decision: the question (one sentence), options considered, the originating task
2. Decide what to do with that task by asking advisor: "Is this decision easy to change later? If so, which option should we provisionally go with?"
   - **Easy to change later**: have developer continue with advisor's recommended option and finish the task. Append "provisionally did X (commit <hash>)" to the item
   - **Involves data shape, wording or flows users see, or principles to keep**: don't decide provisionally. Stash the uncommitted changes with `git stash push -m "<ID> awaiting decision"` and take the task out of in progress
3. Find remaining tasks that depend on this decision. Skip them and list them under "Waiting tasks" in the item
4. Move on to the next task

## Where Items Awaiting Decision Go

<For docs/tasks.md>
- Write them under "Awaiting Human Decision" in `docs/tasks.md` and commit to `overnight/YYYY-MM-DD`

<For GitHub Issues>
- Don't create Issues (creating them needs human confirmation; the hook also rejects it on `overnight/` branches). Write them only in the morning report; the human adds them with `/task add` in the morning

## Morning Report

When finishing, write it to `docs/_wip/overnight-YYYY-MM-DD.md`, commit it, and also print the same content as the final message.

```markdown
# Overnight Work YYYY-MM-DD

Branch: overnight/YYYY-MM-DD (from <hash> of <working branch>)

## Awaiting Human Decision (answer these first)
- Question — Options — From — Provisional choice (if any) — Waiting tasks

## Finished Tasks
- T-003 … — commit <hash>

## Skipped or Stopped Tasks
- T-005 … — reason — stashed changes (stash name)

## Task Candidates (from developer and advisor)
- …

## Last Type Check and Test Run
(paste the tail of the output)
```

After the human reads this file in the morning and answers the items awaiting decision, delete it.

## Don't

- Ask the human anything after the up-front confirmation
- Do irreversible operations such as push, deploy, or DB migrations (don't use runbook skills even if they exist)
- Commit to any branch other than `overnight/YYYY-MM-DD`
- Add new tasks (only write them as task candidates in the morning report)
- Decide and close items awaiting decision yourself
- Bypass the commit hook (use `--no-verify`)
````

### Create /handoff Skill

Create `.claude/skills/handoff/SKILL.md`. Typed when the context is running low, it saves the current state and prints a prompt for continuing the work after clearing.

What's needed to continue is **first saved in the harness's usual places (tasks, detailed design, decisions, commits)**, and only the in-progress state that fits nowhere else goes into a short handoff note. The note is throwaway, deleted on resume, so that stale content doesn't linger.

Fill in `<...>` with the contents of A4 to A7.

````markdown
---
name: handoff
description: Before clearing the context, save the current state and print a prompt for continuing the work after the clear.
disable-model-invocation: true
---

# /handoff - Leave a Handoff Before Clearing

## 1. Bring the Usual Places Up to Date

Before writing the handoff note, first bring the following in line with the current state. Don't repeat in the note what you write here.

- Tasks (<docs/tasks.md or GitHub Issues>): the state of the task in progress. Close finished ones using the `/task done` procedure
- Detailed design (`docs/_wip/<topic>.md`): design or steps that changed during the conversation
- Decisions (`docs/decisions/`): anything decided in the conversation that has a rejected alternative and isn't recorded yet
- Commits: if there's a clean break point in the changes, ask the human whether to commit. Don't do it on your own

## 2. Write the Handoff Note

Write only the in-progress state that fits nowhere else to `docs/_wip/handoff.md` (overwrite it if it already exists).

```markdown
# Handoff (YYYY-MM-DD HH:MM)

## What I'm Working On
- Task: T-003 ... (detailed design: docs/_wip/...)
- Current stage: (e.g., finished 2 of 3 implementation steps; 1 test is failing)

## Uncommitted Changes
- File — what the change is for (check with `git status` before writing)

## Next Steps
1. ...

## Findings and Pitfalls
- (what was tried and didn't work, things to watch out for)

## What the Human Said / Decisions Pending
- (preferences or instructions the human gave in the conversation, questions asked that are still unanswered)
```

- Keep it short. For anything already in docs/ or the tasks, just point to where it is
- Prioritize what exists only in the conversation (what was tried, the human's instructions and preferences)
- Don't write secret values (API keys, etc.)

## 3. Print the Prompt for Resuming

Finally, print it in this form. The human pastes it after `/clear`.

```
After /clear, paste the following prompt:

Read docs/_wip/handoff.md and continue the work. Once you start, delete handoff.md.
```

If the next step is clear, add one line such as "Start from X."

## Don'ts

- Type `/clear` yourself (the human types it)
- Commit without asking the human
- Write only in the handoff note what belongs in the usual places
````

### Set Up the Commit Guard (Standard)

Put a two-layer mechanism in place that **mechanically blocks** commits of secrets and DB files. Both layers call the same check script.

| Layer | What it blocks | Why |
|---|---|---|
| git pre-commit hook (`.githooks/`) | Blocks commits including human ones | Claude Code hooks alone can't stop human commits |
| Claude Code PreToolUse hook | Agents' `git commit`, bypassing hooks with `--no-verify`, environments where git hooks aren't enabled | git hooks aren't enabled just by cloning, and `--no-verify` skips them |

In addition, **get human confirmation before a push, a Pull Request, or an Issue is created**. Claude Code starts in auto mode by default, and in auto mode a push to the current repository (including the default branch) and creating a PR go through without confirmation. Put them in both `permissions.ask` in `.claude/settings.json` and `REMOTE_RULES` in the PreToolUse hook (`permissions.ask` can't catch forms such as `git -C <dir> push`, so the hook, which looks at the whole command, fills the gap). During `/overnight` work (on an `overnight/` branch), a confirmation would stall everything until morning, so the hook returns a rejection instead of a confirmation.

#### 1. Check script `scripts/check-staged.sh`

Write it in bash regardless of tech stack. Adjust DB file extensions etc. for the stack chosen in A4. If the service has files that must never enter the repository (e.g., users' photos or audio), discuss with the user and add those extensions too.

```bash
#!/usr/bin/env bash
# Checks staged changes for secrets, credentials, and database files.
# Called from both the git pre-commit hook (.githooks/pre-commit) and the Claude Code hook (.claude/hooks/).
# Returns 1 if anything is found.
set -uo pipefail

cd "$(git rev-parse --show-toplevel)" || exit 1

fail=0
report() { echo "  ✗ $1" >&2; fail=1; }

db_ext='sqlite|sqlite3|db|db3|db-wal|db-shm|db-journal'

while IFS= read -r -d '' f; do
  lower=$(printf '%s' "$f" | tr '[:upper:]' '[:lower:]')
  base=${lower##*/}

  case "$base" in
    .env.example | .env.sample) ;;
    .env | .env.*) report "$f — secrets file (.env)"; continue ;;
    *.pem | *.key | credentials.json | service-account*.json) report "$f — credentials file"; continue ;;
  esac

  if [[ "$base" =~ \.(${db_ext})$ ]]; then
    report "$f — database file"; continue
  fi
done < <(git diff --cached --name-only --diff-filter=ACMR -z)

# Check added lines for strings that look like API keys
secret_patterns=(
  'sk-ant-[A-Za-z0-9_-]{20,}'                     # Anthropic
  'sk-(proj-|svcacct-|admin-)?[A-Za-z0-9_-]{32,}' # OpenAI
  'AKIA[0-9A-Z]{16}'                              # AWS access key
  'gh[pousr]_[A-Za-z0-9]{36,}'                    # GitHub token
  '-----BEGIN [A-Z ]*PRIVATE KEY-----'            # Private key
  '(api[_-]?key|secret|token|password|access[_-]?key)["'"'"']?[[:space:]]*[:=][[:space:]]*["'"'"']?[A-Za-z0-9_/+=-]{20,}'
)
pattern=$(IFS='|'; echo "${secret_patterns[*]}")

while IFS= read -r -d '' f; do
  [[ "$f" == "scripts/check-staged.sh" ]] && continue
  hits=$(git diff --cached -U0 --no-color -- "$f" | grep -E '^\+' | grep -vE '^\+\+\+' | grep -ainE -e "$pattern" | head -n 3)
  if [[ -n "$hits" ]]; then
    report "$f — string that looks like an API key"
    while IFS= read -r line; do echo "      ${line:0:120}" >&2; done <<<"$hits"
  fi
done < <(git diff --cached --name-only --diff-filter=ACMR -z)

if [[ $fail -ne 0 ]]; then
  cat >&2 <<'EOF'

Commit blocked. Unstage the files above with `git restore --staged <file>` (before the first commit, use `git rm --cached <file>`).
Even for false positives, don't bypass the hook — ask a human.
EOF
  exit 1
fi
exit 0
```

#### 2. git pre-commit hook `.githooks/pre-commit`

```bash
#!/usr/bin/env bash
# To enable: git config core.hooksPath .githooks
exec "$(git rev-parse --show-toplevel)/scripts/check-staged.sh"
```

After creating it, run:

```bash
chmod +x scripts/check-staged.sh .githooks/pre-commit
git config core.hooksPath .githooks
```

> `core.hooksPath` isn't enabled just by cloning. If a team uses the repo, tell the user to add `git config core.hooksPath .githooks` to the setup instructions in the README.

#### 3. Claude Code PreToolUse hook

Write the hook itself **in the language chosen in A4** (`.claude/hooks/guard-bash.mjs` for Node.js, `.claude/hooks/guard_bash.py` for Python). Input to the hook is passed as **JSON on standard input** (`tool_input.command` holds the command about to run).

- Block (deny): exit with code 2 and write the reason to standard error
- Ask a human to confirm (ask): write JSON with `permissionDecision: "ask"` to standard output and exit with code 0

Node.js example:

```js
// Claude Code PreToolUse hook (Bash).
// - git commit: block hook-skipping flags and check staged changes with scripts/check-staged.sh
// - Pushes, PR and Issue creation, and commands that could break production: ask a human to confirm (REMOTE_RULES / ASK_RULES)
// - During /overnight work (an overnight/ branch), reject them instead of asking
import { execFileSync, spawnSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";

let input = {};
try { input = JSON.parse(readFileSync(0, "utf8")) ?? {}; } catch {}
const cmd = String(input?.tool_input?.command ?? "").replace(/\\\r?\n/g, "");
const projectDir = process.env.CLAUDE_PROJECT_DIR || input.cwd || process.cwd();
const workDir = input.cwd && existsSync(input.cwd) ? input.cwd : projectDir; // look at the worktree / directory Claude is working in
// Match against the command with quoted strings and heredoc bodies removed (so that a commit message
// or a grep argument that merely contains "git push" or "-n" doesn't trigger anything).
const QUOTED = String.raw`\$'(?:[^'\\]|\\.)*'|"(?:[^"\\]|\\.)*"|'[^']*'`;
function strip(s) {
  return s
    .replace(/<<-?\s*(['"]?)(\w+)\1([^\n]*)\n(?:[\s\S]*?\n)??[ \t]*\2(?=\s|\)|$)/g, "$3")
    .replace(new RegExp(QUOTED, "g"), '""');
}
// Treat the contents of bash -c "..." / sh -c '...' / eval "..." as commands
const inner = [...cmd.matchAll(new RegExp(String.raw`\b(?:(?:ba|z|da)?sh\s+(?:-\w+\s+)*-\w*c|eval)\s+(` + QUOTED + ")", "g"))]
  .map((m) => m[1].replace(/^\$?['"]|['"]$/g, ""));
const bare = [cmd, ...inner].map(strip).join("\n");

function deny(reason) {
  process.stderr.write(reason + "\n");
  process.exit(2);
}

function ask(reason) {
  process.stdout.write(
    JSON.stringify({
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "ask",
        permissionDecisionReason: reason,
      },
    }),
  );
  process.exit(0);
}

// ---- git commit ----
const isCommit = /\bgit\s+(?:-[cC]\s+\S+\s+|--?[\w-]+(?:=\S+)?\s+)*commit\b/.test(bare);
if (isCommit) {
  if (/--no-veri\w*/.test(bare) || /\bcommit\b[^;&|\n]*\s-[aeiopqsvz]*n/.test(bare)) {
    deny("Flags that skip commit hooks (--no-verify / -n) are not allowed.");
  }
  if (/core\.hookspath|GIT_CONFIG_/i.test(bare) || /(?:-c\s*|--config-env[=\s])["']?core\.hookspath/i.test(cmd)) {
    deny("You can't change core.hooksPath while committing.");
  }

  let hooksPath = "";
  try {
    hooksPath = execFileSync("git", ["config", "--get", "core.hooksPath"], { cwd: workDir, encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] }).trim();
  } catch {}
  if (hooksPath !== ".githooks") {
    deny("The git pre-commit hook is not enabled. Run `git config core.hooksPath .githooks` first.");
  }

  const r = spawnSync("bash", [join(projectDir, "scripts/check-staged.sh")], { cwd: workDir, encoding: "utf8" });
  if (r.status !== 0) {
    deny((r.stderr || "") + (r.stdout || "") || "scripts/check-staged.sh failed.");
  }
}

// ---- Pushes, PR and Issue creation, and commands that could break production: ask a human to confirm ----
// During /overnight work (an overnight/ branch), a confirmation would stall everything until morning,
// so reject push, PR creation, Issue creation, and ASK_RULES commands instead of asking. Claude takes the reason and moves on.
function branchOf(dir) {
  const git = (...a) => {
    try { return execFileSync("git", a, { cwd: dir, encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] }).trim(); } catch { return ""; }
  };
  const b = git("symbolic-ref", "--short", "-q", "HEAD"); // works even on a branch with no commits yet
  if (b) return b;
  for (const p of ["rebase-merge/head-name", "rebase-apply/head-name"]) { // during a rebase (detached HEAD)
    try { return readFileSync(git("rev-parse", "--path-format=absolute", "--git-path", p), "utf8").trim().replace(/^refs\/heads\//, ""); } catch {}
  }
  return "";
}
// Check both the working directory and the project, for work done in a worktree
const overnight = [workDir, projectDir].some((d) => branchOf(d).startsWith("overnight/"));

// Push, PR creation, and Issue creation are included by default (auto mode lets them through without confirmation).
const GH = String.raw`\bgh\s+(?:(?:-R|--repo)[=\s]\S+\s+)?`;
const REMOTE_RULES = [
  [/\bgit\s+(?:-[cC]\s+\S+\s+|--?[\w-]+(?:=\S+)?\s+)*(?:(?:subtree|lfs)\s+)?push(?![\w-])(?![^;&|\n]*\s(?:--dry-run|--help|-h)\b)/, "This pushes to a remote."],
  [new RegExp(GH + String.raw`pr\s+(create|merge)\b`), "This creates or merges a Pull Request."],
  [new RegExp(GH + String.raw`issue\s+create\b`), "This creates an Issue."],
];
for (const [re, reason] of REMOTE_RULES) {
  if (!re.test(bare)) continue;
  if (overnight) deny(reason + " This is not done during overnight work (overnight/ branch). Note it in the morning report and move on.");
  ask(reason + " Check the content before allowing it.");
}

// Add rules for commands that could break production, matching the infrastructure chosen in A4. Examples:
//   [/\bprisma\s+migrate\s+deploy\b/, "This command applies migrations to the production DB."],
//   [/\bterraform\s+(apply|destroy)\b/, "This command changes infrastructure."],
const ASK_RULES = [];
for (const [re, reason] of ASK_RULES) {
  if (!re.test(bare)) continue;
  if (overnight) deny(reason + " This is not done during overnight work (overnight/ branch). Note it in the morning report and move on.");
  ask(reason + " Check the impact before allowing it.");
}

process.exit(0);

```

Keep `REMOTE_RULES` (push, PR, and Issue creation) as is. In `ASK_RULES`, put — after discussing with the user — the commands that **could break production** for the infrastructure and DB chosen in A4 (leaving it empty is fine if there are none). On `overnight/` branches, both are rejected instead of asking.

`.claude/settings.json`:

```json
{
  "permissions": {
    "ask": [
      "Bash(git push *)",
      "Bash(gh pr create *)",
      "Bash(gh pr merge *)",
      "Bash(gh issue create *)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "node \"$CLAUDE_PROJECT_DIR/.claude/hooks/guard-bash.mjs\""
          }
        ]
      }
    ]
  }
}
```

After creating it, confirm the following two things.

- Stage `.env` with `git add -f .env`, try `git commit`, and confirm it's blocked (`-f` is needed because `.env` is in `.gitignore`; this is before the initial commit, so unstage it afterward with `git rm --cached .env`)
- The hook recognizes a push. Use the Write tool to create a file (e.g., `/tmp/push-test.json`) containing `{"tool_input":{"command":"git -C . push"}}`, run `node .claude/hooks/guard-bash.mjs < /tmp/push-test.json`, and confirm that `permissionDecision: "ask"` is returned (if you wrote the push text directly in the command, the hook would react to the verification command itself, so pass it via a file. This works even if no remote exists yet)

When writing it in Python or another language, include the same behavior:

- `REMOTE_RULES` (push, PR, and Issue creation) and rejection on `overnight/` branches (checking the branch of both the working directory and the project)
- Matching against the command with quoted strings and heredoc bodies removed, while still treating the contents of `bash -c "..."`, `sh -c '...'`, and `eval "..."` as commands
- Applying the same removal to the commit checks (`--no-verify` / `-n`, changing `core.hooksPath`), so a commit message that merely contains `-n` isn't blocked

> With this hook and `permissions.ask`, confirmation appears for push, PR, and Issue creation written in the ordinary way. However, some forms slip through, such as creating one directly with `gh api`, running it inside quotes like `echo "$(git push)"`, or using a git alias. Don't treat confirmation as a sure defense; combine it with a human checking at natural breakpoints in the work.
>
> The commit check (`scripts/check-staged.sh`) runs in the directory Claude is working in. If Claude moves to another worktree with `cd` or `git -C` and commits there, the hook may not catch it, but the git pre-commit hook (`.githooks/pre-commit`) still blocks it.

### Auto-formatting Hook (Optional)

Ask the user: "Set up automatic code formatting?"
If YES, add a formatter matching the A4 stack to `PostToolUse` in `.claude/settings.json`. The edited file's path is in `tool_input.file_path` of the JSON on standard input (requires `jq`).

Formatter examples:
- JavaScript/TypeScript: `npx prettier --write`
- Python: `ruff format`
- Go: `gofmt -w`
- Rust: `rustfmt`

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs <tech-stack formatter>"
          }
        ]
      }
    ]
  }
}
```

### Confirm Testing Strategy

Confirm with the user:

- Test framework choice (Jest / Vitest / pytest, etc.)
- Whether E2E tests are needed (Playwright, etc.)
- Test directory structure

Reflect the results in "Testing" in `docs/implementation-policy.md`, "Common Commands" in `CLAUDE.md`, and the qa-engineer definition.

### Initial Commit

Once all files are in place, make the initial commit after confirming with the user.

```
docs: create initial project documents

- docs/requirements.md (requirements and principles to keep)
- docs/spec.md (base spec)
- docs/implementation-policy.md (implementation policy)
- docs/decisions/ (why we decided)
- docs/README.md (documentation policy)
- docs/tasks.md (first tasks, if the file was chosen)

chore: set up development foundation

- CLAUDE.md (index and promises)
- .claude/agents/ (advisor, developer, qa-engineer, code-reviewer)
- .claude/skills/ (consult, ask-advisor, commit, task, overnight, handoff)
- .claude/settings.json, .claude/hooks/, .githooks/, scripts/check-staged.sh (commit guard)
- .gitignore
```

**Completion criteria**: Skills and the commit guard created, the guard confirmed to block committing `.env`, first tasks created, initial commit done.

---

## A8: Runbook Skills for Irreversible Operations (Optional)

Ask the user: "Do you want to turn operations that are irreversible if done wrong — production deploys, DB migrations, registering secrets, etc. — into runbook skills?" If nothing is decided yet, tell them they can create these when needed and skip.

If creating them, make `.claude/skills/<operation-name>/SKILL.md` for each operation using this template.

```markdown
---
name: <operation name (e.g., db-migrate)>
description: <What to do, in what order>. <When to use>. Always get human confirmation before applying to production.
argument-hint: "[local|staging|production]"
---

# <Operation Name>

<Why to be careful (1-2 lines)>. Don't skip steps.

## Prerequisites

- <Config file> is the source of truth for environment names and settings
- <First confirm staging and production don't point to the same resource, etc.>

## 1. Do it locally
## 2. Do it on staging and verify
## 3. Do it on production (always get human confirmation)

**Do not proceed past here without human confirmation.**

1. Show the human the following and ask whether to proceed: what will be applied, whether any change destroys data, the results verified on staging
2. Run it only after getting approval

## When Things Go Wrong

- <How to roll back. If it can't be rolled back, say so>
```

Also add the commands handled by runbook skills to `ASK_RULES` in A7, so the hook also inserts a human confirmation.

**Completion criteria**: The runbook skills the user decided on are created (skip if none).

---

## Complete: Bridge to Phase B

Once all steps are done, show:

```
Project foundation is ready!

■ Created Files
  docs/requirements.md            — Requirements and principles to keep
  docs/spec.md                    — Base spec
  docs/implementation-policy.md   — Implementation policy (which way to lean)
  docs/decisions/                 — Why we decided
  docs/_wip/                      — Detailed designs in progress (promote or delete when done)
  docs/README.md                  — Documentation policy
  docs/tasks.md / GitHub Issues   — Tasks (first list created from the MVP)
  CLAUDE.md                       — Index and promises
  .claude/agents/                 — advisor, developer, qa-engineer, code-reviewer
  .claude/skills/                 — consult, ask-advisor, commit, task, overnight, handoff
  .claude/settings.json etc.      — Commit guard
  .gitignore                      — Security basics

■ How to Develop Going Forward (Phase B)

  0. /task                 → Pick the next task (add new ideas with /task add)
  1. /consult              → Brainstorm desired feature with Claude (requirements go to requirements.md)
  2. /plan                 → Make implementation plan in Plan Mode
  2.5. Persistence         → Save plan to docs/_wip/<topic>.md as a detailed design
  3. Ask developer         → Implement → qa-engineer → code-reviewer → commit
  4. /ask-advisor milestone review → Get a full review when a chunk of features is done
  5. Clean up              → Move docs/_wip/ content into docs/ or delete it
                             Close with /task done; /task add the review's "→task" items and developer's task candidates

  ※ Before bed, /overnight → advances delegated tasks until morning, leaving points that need a decision and moving on
    In the morning, read docs/_wip/overnight-<date>.md, answer the items awaiting decision, then merge the branch

  ※ Consult /ask-advisor on uncertain decisions and record them in docs/decisions/.
    Sessions end, but documents remain.

■ Model Selection
  Daily coding        → /model sonnet (best bang for buck)
  Complex design      → /model opus (deep reasoning)
  Quick tasks         → /model haiku (fastest and cheapest)

■ Context Management
  Task changes        → /clear (reset)
  Running low         → /handoff to save state → /clear → paste the prompt it prints
  Need to continue fast → /compact (compress; nothing is saved to files)

■ Stuck?
  Esc+Esc → Rewind to checkpoint
  /clear → Start over (include what you learned)
```
