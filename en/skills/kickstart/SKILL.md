---
name: kickstart
description: Start a new project from scratch. Follow Phase A procedures, building the foundation from service overview to CLAUDE.md, agents, and skills step by step.
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

## Model Selection

- A1-A3 (concept and requirement brainstorming): Sonnet 4.6 is sufficient
- A4 (architecture decision): **Opus 4.6 recommended** (deep design judgment needed)
- A5-A7 (file creation): Sonnet 4.6 is sufficient

If the recommended model differs from current at step start, guide the user to switch with `/model`.

---

## A0: Project Initialization (Automatic)

Run automatically at the start. User confirmation not needed.

### Create Directory Structure

```
docs/
├── specs/                ← Save feature specs here (used in Phase B)
└── architecture-decisions/ ← Record technical decisions
```

### Create .gitignore

Create `.gitignore` in project root with common items (tech-stack independent):

```gitignore
# Environment variables and secrets
.env
.env.*

# Credentials
credentials.json
*.pem
*.key
service-account.json

# OS and editors
.DS_Store
Thumbs.db
*.swp
.vscode/settings.json
.idea/
```

> **Note**: Tech-specific items (`node_modules/`, `__pycache__/`, `vendor/` etc.) are added after A4 architecture decision.

### Verify git Initialization

If `.git/` doesn't exist, run `git init`.

**Completion criteria**: Directory structure and .gitignore created.

---

## A1: Service Overview Document

Ask the user the following questions to create `docs/service-overview.md`:

### What to Ask

- **What are you building** (in one sentence)
- **Who is the target** (user demographics)
- **What matters most** (priorities, non-negotiables)
- **Long-term vision (final goal)**
- **MVP (minimum viable features)** — each feature in one specific line
- **Future features to add**

### How to Ask

- Don't ask all at once; naturally explore in conversation
- For vague answers, dig deeper: "What would that look like specifically?"
- If MVP exceeds 5 features, check: "Do you really need all for MVP? Anything deferrable?"
- If the user seems uncertain, offer specific choices

### Document Template

```markdown
# Service Overview

## Service Name
(Tentative is fine)

## What Are You Building
(One sentence)

## Target Users
(Who's it for)

## What Matters Most
- ...
- ...

## Vision (Final Goal)
...

## MVP (Minimum Viable Features)
1. ...
2. ...

## Future Features to Add
- ...
- ...
```

**Completion criteria**: `docs/service-overview.md` created and user confirmed the content with "OK."

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

## Load Required Knowledge

Before answering, always read:

1. `docs/service-overview.md` - Service overview
2. `docs/specs/` - Existing feature specs (if any)

## Behavior as Discussion Partner

- Discuss on equal footing (not top-down)
- Acknowledge good ideas genuinely
- Share concerns frankly
- Don't just say "that's good" — dig deeper
- Reference implementation status if needed, sharing "what's possible now"

## Things to Avoid

- Don't jump straight to implementation (organize requirements first)
- Avoid excessive optimism or pessimism
- Don't uncritically agree with everything the user says

## Service Core (Always Keep in Mind)

> (Transfer vision and values from A1's `docs/service-overview.md`)
```

Transfer the **actual content** of vision and values from A1's `docs/service-overview.md` — don't leave template placeholders.

**Completion criteria**: `.claude/skills/consult/SKILL.md` created with project-specific content.

---

## A3: Brainstorm Requirements with /consult

Guide the user:

```
The consult skill is ready.
Let's start brainstorming. We'll explore these angles:

- Are MVP features appropriate?
- Priorities correct?
- Missing features? (auth, notifications, error handling, search, etc.)
- User experience flow (key interactions)?

Results will update docs/service-overview.md.
Let's start by revisiting the MVP features.
```

### Brainstorming Points

- **User Flow**: Main operations (signup → login → main feature → ...)
- **Permissions**: Need admin/user distinction?
- **Notifications**: Email, push notifications needed?
- **Search/Filtering**: How to search when data grows?
- **Error Cases**: How do major operations fail?
- **Data Lifecycle**: Logical or physical delete?

### Important: Persist Brainstorming Results

Once discussion settles, always update `docs/service-overview.md`. Conversations disappear when sessions end, but documents remain.

**Completion criteria**: User agrees on MVP requirements, `docs/service-overview.md` updated.

---

## A4: Architecture Decision ← Branching Point

> **This step is recommended with Opus 4.6.** Switch with `/model opus`.

**Can't make A6 agents without deciding this.**

### Points to Discuss

Discuss each one-by-one with the user, present multiple options with comparison tables, let the user choose:

1. **Platform**: Web / mobile / desktop / multiple
2. **Language**: TypeScript, Python, Go, Rust, Ruby, Java, etc.
3. **Frontend**: React, Next.js, Vue, Svelte, Flutter, etc. (if applicable)
4. **Backend**: Express, Hono, Django, FastAPI, Rails, Gin, Echo, etc.
5. **Database**: PostgreSQL, MySQL, SQLite, MongoDB, etc.
6. **ORM/Data Access**: Prisma, SQLAlchemy, GORM, ActiveRecord, etc.
7. **Infrastructure**: AWS, GCP, Vercel, Cloudflare, self-hosted, etc.
8. **Design Pattern**: Monolith, microservices, Clean Architecture, etc.
9. **Directory Structure**: Propose structure suited to chosen tech stack

### Decision Criteria (Explain to User)

- **Team Experience**: Prioritize familiar technologies
- **MVP Speed**: Prioritize quick building
- **Learning Goal**: If wanting to try new tech, that counts too
- **Scalability**: Future extensibility

### Proposal Format (Example)

```
| Angle | Option A | Option B | Option C |
|-------|----------|----------|----------|
| Frontend | Next.js | React + Vite | React Native |
| Why | SSR support, Vercel compat ◎ | Simple, low learning curve | Mobile apps |
| Good for | SEO-needed web apps | SPA | iOS/Android |
```

### Record Decisions

Write `docs/architecture.md`:

```markdown
# Architecture

## Tech Stack
- Frontend: ...
- Backend: ...
- DB: ...
- ORM: ...
- Infra: ...
- Design Pattern: ...

## Selection Reasoning
(Why these technologies)

## Directory Structure
(Tree format)
```

### Record Technical Decisions

For important choices, create individual files in `docs/architecture-decisions/`:

```markdown
# ADR-001: Why Prisma

## Situation
ORM selection needed

## Options
- Prisma: type-safe, easy migration management
- Drizzle: lightweight, close to SQL
- TypeORM: proven, but maintenance stalled

## Decision
Prisma

## Reasoning
Prioritize type safety and migration convenience.
```

### Update .gitignore

Now that tech is chosen, add tech-specific items to A0's `.gitignore`:

Example:
- Node.js: `node_modules/`, `dist/`, `build/`
- Python: `__pycache__/`, `.venv/`, `*.pyc`
- Go: basically none (specify binary name)
- Ruby: `vendor/bundle/`, `.bundle/`

**Completion criteria**: `docs/architecture.md` created, tech stack finalized, directory structure confirmed, `.gitignore` updated for tech stack.

---

## A5: Create CLAUDE.md

After **actually reading A1-A4 outputs**, create `CLAUDE.md` in project root.

### Content to Include

1. **Project Overview** (1-2 lines)
2. **Tech Stack** (transfer from A4)
3. **Important Rules**
   - Command execution environment (Docker? Local?)
   - Test policy (tests must pass before committing)
   - Code style (naming, formatter)
4. **Directory Structure** (transfer from A4)
5. **Reference Documents**
   - `docs/service-overview.md`
   - `docs/architecture.md`
   - `docs/specs/` — feature specs
6. **Security Rules**
   - Never commit `.env` files
   - Never hardcode API keys or passwords
   - Get credentials via environment variables

### Strict Rules

- **Keep under 200 lines** (Claude ignores longer files)
- Don't document what code already shows
- Avoid obvious instructions like "write clean code"

**Completion criteria**: `CLAUDE.md` created, under 200 lines, project-specific.

---

## A6: Create Sub-agents

> **Switch back to Sonnet 4.6.** `/model sonnet` is fine.

Create `.claude/agents/` based on A4 architecture.

### Start with 3 Agents

| Order | Agent | Why |
|-------|-------|-----|
| 1 | **system_architect** | Guardian of design. Source of rules others reference |
| 2 | **developer** | Implementation per architecture (e.g., `backend_developer`) |
| 3 | **qa_engineer** | Testing and quality |

> **Key**: Add tech_researcher, frontend_developer, etc. as needed. No need to create everything upfront.

### Required Items for Each Agent

```markdown
---
name: (agent name)
description: (Specific: what expert does this project need; include tech stack names)
---

# Role
(Specific expertise in this project)

# Goals
1. (Include spec file paths)
2. (Include design patterns to maintain)
3. (Include test rules)

# Constraints
- (Directories/files to avoid)
- (Things not to do)
- (When to escalate decisions)

# References
- docs/architecture.md
- docs/specs/ (relevant specs)
- (Other agent-specific refs)
```

### Important

- **Description must include actual tech stack names** ("Express + Prisma API builder" not "backend person")
- **Constraints must clarify boundaries** with other agents
- Reference OSS agent definitions but override with project specifics

**Completion criteria**: All needed agents in `.claude/agents/`, each reflecting project tech and rules.

---

## A7: Skills, Hooks, and Initial Commit

### Create /commit Skill

Create `.claude/skills/commit/SKILL.md`:

```markdown
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
Organize by logical unit:
- New feature → `feat:`
- Bug fix → `fix:`
- Refactoring → `refactor:`
- Docs → `docs:`
- Misc → `chore:`

### 3. Commit Per Group
```bash
git add <related-files>
git commit -m "$(cat <<'EOF'
<type>: <concise description>

<detailed explanation if needed>

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

## Notes
- Avoid `git add -A` or `git add .` — specify files explicitly
- Never commit `.env` or credential files
- Push only with explicit user instruction
```

### Optional: Setup Hooks

Ask the user: "Set up code auto-formatting?"

If YES, create `.claude/settings.json` with formatter for chosen tech stack:

Examples:
- JavaScript/TypeScript: `npx prettier --write`
- Python: `ruff format`
- Go: `gofmt -w`
- Rust: `rustfmt`

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "<tech-stack formatter> \"$CLAUDE_TOOL_INPUT_FILE_PATH\""
          }
        ]
      }
    ]
  }
}
```

### Confirm Test Strategy

Ask the user:

- Test framework choice (Jest / Vitest / etc.)
- E2E testing needed? (Playwright, etc.)
- Test directory structure?

Add results to `CLAUDE.md`'s test policy section.

### Make Initial Commit

Once all files are ready, confirm with user and commit:

```
docs: Create initial project documentation

- docs/service-overview.md (service overview)
- docs/architecture.md (architecture)

chore: Build development foundation

- CLAUDE.md (project config)
- .claude/agents/ (sub-agents)
- .claude/skills/ (consult, commit skills)
- .gitignore
```

**Completion criteria**: `/commit` skill created, initial commit done.

---

## Complete: Bridge to Phase B

Once all steps are done, show:

```
Project foundation is ready!

■ Created Files
  docs/service-overview.md       — Service overview
  docs/architecture.md           — Architecture
  docs/specs/                    — Feature specs (used in Phase B)
  docs/architecture-decisions/   — Technical decisions
  CLAUDE.md                      — Project config
  .claude/skills/consult/        — Requirements discussion skill
  .claude/skills/commit/         — Commit skill
  .claude/agents/                — Sub-agents (minimum 3)
  .gitignore                     — Security basics

■ How to Develop Going Forward (Phase B)

  1. /consult     → Brainstorm desired feature with Claude
  2. Shift+Tab    → Make implementation plan in Plan Mode
  2.5. Persistence → Save plan to docs/specs/ as spec
  3. Shift+Tab    → Return to normal mode and implement
  3.5. Testing    → Run unit tests & E2E tests
  4. /commit      → Commit following rules

  ※ Always save plans and brainstorms to docs.
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
