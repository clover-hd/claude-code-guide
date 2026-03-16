# Skills

[< Back to Guide](README.en.md)

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
1. Read service requirements document
2. Understand feature implementation status

## Behavior as a consultant
- Discuss from an equal perspective
- Honestly recognize good ideas
- Frankly communicate concerns
```

**Usage**: Type `/consult` and Claude will load the service specification and serve as a planning partner for consultation.

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
