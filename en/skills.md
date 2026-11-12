# Skills

[< Back to Guide](../README.en.md)

---

## What Are Skills?

**Skills** are a feature that allows you to give Claude specialized knowledge or procedures as templates that can be invoked with `/skill-name`.

> **Note**: Older versions used Markdown files in `.claude/commands/`, but the latest version **recommends placing `SKILL.md` in the `.claude/skills/` directory**. The old format still works for backward compatibility, but new skills should be created in the skills format.

## How to Set Up

Place files in the structure `.claude/skills/<skill-name>/SKILL.md`.

```
.claude/
└── skills/
    ├── commit/
    │   └── SKILL.md         ← Invoked with /commit
    └── consult/
        ├── SKILL.md         ← Invoked with /consult
        └── examples.md      ← Supporting file (optional)
```

Comparison with old format:

| | Old format (commands) | New format (skills) - Recommended |
|--|-------------------|---------------------|
| **Location** | `.claude/commands/commit.md` | `.claude/skills/commit/SKILL.md` |
| **Supporting files** | Not possible | Possible (templates, scripts, etc. included) |
| **Invocation control** | Limited | Flexible control via frontmatter |
| **Auto-invocation** | Claude decides | Controllable with `disable-model-invocation` |

## How to Write Skill Definitions (SKILL.md)

```markdown
---
name: commit
description: Execute git commits following project rules
disable-model-invocation: true   # Only user can invoke (due to side effects)
---

# /commit - Project-specific commit skill

## Rules
1. 1 commit = 1 logical change
2. Conventional Commits format: feat:, fix:, chore:, refactor:, docs:
...
```

Key frontmatter fields:

| Field | Description |
|-----------|------|
| `name` | Skill name (invoked with `/name`) |
| `description` | Description for Claude to decide when to use it |
| `disable-model-invocation: true` | Only users can invoke (for operations with side effects like deployments) |
| `user-invocable: false` | Claude only (for providing background knowledge) |
| `argument-hint` | Hint for the argument typed after `/name`. Received in the body as `$ARGUMENTS` |
| `context: fork` | Run in a context separate from the main conversation |
| `agent` | The sub-agent to use with `context: fork` |
| `background` | Used only with `context: fork`. Defaults to `true`: it runs in the background and the result arrives later. Set it to `false` to wait for the result on the spot |

## Skill Placement Scope

| Scope | Location | Effect |
|---------|---------|---------|
| **Personal** | `~/.claude/skills/<name>/SKILL.md` | All your projects |
| **Project** | `.claude/skills/<name>/SKILL.md` | This project only |

Personal skills are for your own shortcuts, while project skills are for team-shared rules.

## Example 1: /commit (Project-specific commits)

An example of defining commit rules as a skill.

```markdown
---
name: commit
description: Execute git commits following project rules
disable-model-invocation: true
---

# /commit - Project-specific commit skill

## Rules
1. 1 commit = 1 logical change
2. Conventional Commits format: feat:, fix:, chore:, refactor:, docs:
3. Add Co-Authored-By
4. Avoid git add -A, explicitly specify files

## Procedure
### 1. Check changes
git status / git diff --stat / git log --oneline -5

### 2. Group changes
Group changes in logical units

### 3. Commit per group
Stage related files → Use HEREDOC to commit
```

**Usage**: Just type `/commit` in the terminal. Claude automatically executes commits following the rules.

## Example 2: /consult (Service requirements consultation)

```markdown
---
name: consult
description: Consult on service requirements and planning
---

# /consult - Service requirements consultation

## Loading prerequisite knowledge
1. Read docs/requirements.md (requirements and principles to keep)
2. Understand feature implementation status

## Behavior as a consultant
- Discuss from an equal perspective
- Honestly recognize good ideas
- Frankly communicate concerns
```

**Usage**: Type `/consult` and Claude will load the service specification and serve as a planning partner for consultation.

## Example 3: /ask-advisor (Send a question to a sub-agent)

Combining `context: fork` with `agent:` lets **the specified sub-agent run the skill in a separate context**. The main conversation doesn't fill up with the consultation process.

A `context: fork` skill runs in the background by default, and the result arrives later. Because we want to see the answer to the consultation before moving on, we add `background: false` so it waits on the spot.

```markdown
---
name: ask-advisor
description: Consult the advisor. Use when unsure about principles, data shape, screen flow, or choices that change the user experience. Also use to request a milestone review.
argument-hint: <what you want to consult on, or "milestone review">
context: fork
agent: advisor
background: false
---

Answer the following consultation.

$ARGUMENTS

- For a consultation, answer in the form: conclusion, reasons, rejected alternatives, when to revisit, draft record
- If it says "milestone review", review overall changes since the last milestone
```

**Usage**: Type something like `/ask-advisor Should cancellation deadlines be configurable per user?`. For the advisor agent, see [Sub-agents](sub-agents.md).

## Example 4: Runbook skill (Irreversible operations)

For **operations that can't be undone if you get them wrong**—production deploys, DB migrations, registering secrets—turn the procedure into a skill. The key is to write into the procedure that the order must never be skipped and that a human must confirm before production.

```markdown
---
name: db-migrate
description: Apply DB migrations in order: local → staging → production. Use when the schema changes. Always get human confirmation before applying to production.
argument-hint: "[local|staging|production]"
---

# DB Migration

Database changes can't be undone. Don't skip steps.

## Prerequisites
- Treat <config file> as the source of truth for environment names and connection targets
- First, check that staging and production don't point to the same DB

## 1. Create the migration and read the SQL (if it deletes data, stop and tell a human)
## 2. Apply locally and pass the tests
## 3. Apply to staging and verify
## 4. Apply to production (always get human confirmation)
Show the human the files to apply, whether any change deletes data, and the staging results; run only after getting approval

## When things go wrong
- <How to roll back. If you can't, say so>
```

Beyond writing it in the runbook, also make the same commands targets of the `PreToolUse` hook's "ask for confirmation (ask)", so a human confirmation is inserted even if they're run without going through the runbook (see [Hooks](project-config.md#hooks-automation)).

## Skills strength: Supporting files

The biggest difference from commands format is the ability to **include supporting files**.

```
.claude/skills/review/
├── SKILL.md           ← Main instructions
├── checklist.md       ← Review checklist
├── examples.md        ← Examples of good/bad reviews
└── scripts/
    └── lint-check.sh  ← Auto-run script
```

You can keep `SKILL.md` concise while separating detailed information into files.

## Skill usage ideas

| Skill name | Purpose | `disable-model-invocation` |
|----------|------|---------------------------|
| `/commit` | Commits following project rules | `true` (has side effects) |
| `/review` | Code review | `false` |
| `/test` | Test generation & execution | `false` |
| `/deploy` | Execute deployment procedure | `true` (has side effects) |
| `/consult` | Brainstorm service planning | `false` |
| `/ask-advisor` | Consult the advisor agent, milestone review | `false` |
