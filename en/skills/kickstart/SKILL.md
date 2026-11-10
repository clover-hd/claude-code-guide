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

**Completion criteria**: `docs/spec.md` created; tech stack, directory structure, branch workflow, and commands settled; `.gitignore` updated for the stack.

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
  - Is it in a state that can be merged into main and run?
- Return format: "Must fix (most serious first)," "Think about before next milestone," "What got better." Keep each short

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

### Recording Consulted Decisions

**You yourself** record decisions made through consultation in `docs/decisions/NNNN-short-name.md`, following `docs/README.md`. Write "Consulted advisor (developer)" in the "Decided by" field. Put the record in the same commit as the implementation that uses the decision.

## Detailed Design

- When starting implementation, write the detailed design (tables, API shapes, screen components, etc.) in `docs/_wip/<topic>.md`
- Clean up when done. Move requirements, base spec, and decision reasons into `docs/`; delete the rest

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

Finally, briefly report: what you did, test and review results, commit hash, decisions consulted and recorded, what remains.

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

```markdown
---
name: ask-advisor
description: Consult advisor. Use when unsure about principles, data shape, screen flow, or choices that change the user experience. Also use to request a milestone full review.
argument-hint: <what to consult about, or "milestone review">
context: fork
agent: advisor
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

### Set Up the Commit Guard (Standard)

Put a two-layer mechanism in place that **mechanically blocks** commits of secrets and DB files. Both layers call the same check script.

| Layer | What it blocks | Why |
|---|---|---|
| git pre-commit hook (`.githooks/`) | Blocks commits including human ones | Claude Code hooks alone can't stop human commits |
| Claude Code PreToolUse hook | Agents' `git commit`, bypassing hooks with `--no-verify`, environments where git hooks aren't enabled | git hooks aren't enabled just by cloning, and `--no-verify` skips them |

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
// - Commands that could break production: ask a human to confirm (add them to ASK_RULES)
import { execFileSync, spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { join } from "node:path";

const input = JSON.parse(readFileSync(0, "utf8"));
const cmd = String(input?.tool_input?.command ?? "");
const projectDir = process.env.CLAUDE_PROJECT_DIR || input.cwd || process.cwd();

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
const isCommit = /\bgit\s+(?:-[cC]\s+\S+\s+|--?[\w-]+(?:=\S+)?\s+)*commit\b/.test(cmd);
if (isCommit) {
  if (/--no-verify\b/.test(cmd) || /\bcommit\b[^;&|\n]*\s-[A-Za-z]*n[A-Za-z]*(\s|$)/.test(cmd)) {
    deny("Flags that skip commit hooks (--no-verify / -n) are not allowed.");
  }
  if (/core\.hooksPath/.test(cmd)) {
    deny("You can't change core.hooksPath while committing.");
  }

  let hooksPath = "";
  try {
    hooksPath = execFileSync("git", ["config", "--get", "core.hooksPath"], { cwd: projectDir, encoding: "utf8" }).trim();
  } catch {}
  if (hooksPath !== ".githooks") {
    deny("The git pre-commit hook is not enabled. Run `git config core.hooksPath .githooks` first.");
  }

  const r = spawnSync("bash", [join(projectDir, "scripts/check-staged.sh")], { cwd: projectDir, encoding: "utf8" });
  if (r.status !== 0) {
    deny((r.stderr || "") + (r.stdout || "") || "scripts/check-staged.sh failed.");
  }
}

// ---- Commands that could break production: ask a human to confirm ----
// Add rules matching the infrastructure chosen in A4. Examples:
//   [/\bprisma\s+migrate\s+deploy\b/, "This command applies migrations to the production DB."],
//   [/\bterraform\s+(apply|destroy)\b/, "This command changes infrastructure."],
const ASK_RULES = [];
for (const [re, reason] of ASK_RULES) {
  if (re.test(cmd)) ask(reason + " Check the impact before allowing it.");
}

process.exit(0);
```

In `ASK_RULES`, put — after discussing with the user — the commands that **could break production** for the infrastructure and DB chosen in A4 (leaving it empty is fine if there are none).

`.claude/settings.json`:

```json
{
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

After creating it, stage `.env`, try `git commit`, and confirm it's blocked (this is before the initial commit, so unstage it afterward with `git rm --cached .env`).

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

chore: set up development foundation

- CLAUDE.md (index and promises)
- .claude/agents/ (advisor, developer, qa-engineer, code-reviewer)
- .claude/skills/ (consult, ask-advisor, commit)
- .claude/settings.json, .claude/hooks/, .githooks/, scripts/check-staged.sh (commit guard)
- .gitignore
```

**Completion criteria**: Skills and the commit guard created, the guard confirmed to block committing `.env`, initial commit done.

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
  CLAUDE.md                       — Index and promises
  .claude/agents/                 — advisor, developer, qa-engineer, code-reviewer
  .claude/skills/                 — consult, ask-advisor, commit
  .claude/settings.json etc.      — Commit guard
  .gitignore                      — Security basics

■ How to Develop Going Forward (Phase B)

  1. /consult              → Brainstorm desired feature with Claude (requirements go to requirements.md)
  2. Shift+Tab             → Make implementation plan in Plan Mode
  2.5. Persistence         → Save plan to docs/_wip/<topic>.md as a detailed design
  3. Ask developer         → Implement → qa-engineer → code-reviewer → commit
  4. /ask-advisor milestone review → Get a full review when a chunk of features is done
  5. Clean up              → Move docs/_wip/ content into docs/ or delete it

  ※ Consult /ask-advisor on uncertain decisions and record them in docs/decisions/.
    Sessions end, but documents remain.

■ Model Selection
  Daily coding        → /model sonnet (best bang for buck)
  Complex design      → /model opus (deep reasoning)
  Quick tasks         → /model haiku (fastest and cheapest)

■ Context Management
  Task changes        → /clear (reset)
  70% full            → /compact (compress)

■ Stuck?
  Esc+Esc → Rewind to checkpoint
  /clear → Start over (include what you learned)
```
