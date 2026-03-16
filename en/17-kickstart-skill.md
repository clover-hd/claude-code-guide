# /kickstart Skill — Automate Project Setup

[< Back to Guide](README.en.md)

---

## What Is This?

This skill automatically guides Claude Code through the steps of [Phase A: Project Setup](05-workflow-setup.md) (A0-A7) in a conversational manner.

You can follow the guide manually, but with `/kickstart`, **Claude Code itself understands the guide steps and builds your project foundation with you**.

### What the Skill Does Automatically

Claude Code walks through [Phase A steps](05-workflow-setup.md) (A0-A7) interactively. Specifically:

- Initialize project (`.gitignore`, directory structure, git init)
- Articulate service overview and validate requirements
- Decide on architecture and document it
- Build CLAUDE.md, skills, and sub-agents
- Make initial commit

For details on each step, see [05-workflow-setup.md](05-workflow-setup.md).

## Setup

### Method 1: Install as Personal Skill (Available in All Projects)

```bash
# Create skills directory
mkdir -p ~/.claude/skills/kickstart

# Copy SKILL.md
cp /path/to/claude-code-guide/skills/kickstart/SKILL.md ~/.claude/skills/kickstart/SKILL.md
```

Now `/kickstart` works in **any project**.

### Method 2: Install as Project Skill (This Project Only)

```bash
# Run in project root
mkdir -p .claude/skills/kickstart

# Copy SKILL.md
cp /path/to/claude-code-guide/skills/kickstart/SKILL.md .claude/skills/kickstart/SKILL.md
```

> **We recommend Method 1**. Since kickstart is used every time you start a new project, it's convenient to have it always available as a personal skill.

## Usage

### 1. Create and start new project

```bash
mkdir my-new-project && cd my-new-project
claude
```

> `git init` is not needed. The skill initializes it automatically.

### 2. Run /kickstart

```
> /kickstart
```

Claude will first auto-initialize (A0) by creating `.gitignore`, directory structure, etc., then start the conversation from A1.

### 3. Work through interactively

```
Claude: Created initial project files.
        ✓ .gitignore
        ✓ docs/specs/
        ✓ docs/architecture-decisions/
        ✓ git init

        Now let's create A1: Service overview.
        What do you want to build? Tell me in one sentence.

You: A platform for managing restaurant reservations and reviews

Claude: Great. Let me dig deeper.
        - Who's the target? (Restaurant owners? Users? Both?)
        - What do you want to prioritize?
        ...
```

Claude asks questions at each step and creates documents and files based on your answers.

### 4. Review each step

Claude asks for confirmation when each step is complete. **Review carefully before moving forward.**

```
Claude: Created docs/service-overview.md.
        Please review. Tell me if you need changes.
        If OK, we'll move to the next step (A2: /consult skill creation).

You: I want to add search functionality to the MVP

Claude: Got it. Added search and updated.
        (Updated docs/service-overview.md)
        Is this OK?

You: OK, let's move forward
```

### 5. Model switching guidance

At A4 (Architecture Decision), you'll be guided to switch to Opus 4.6.

```
Claude: Next is A4: Architecture Decision.
        Deep design decisions ahead, so I recommend switching to Opus 4.6.
        Please switch with /model opus before continuing.
```

From A5 onwards, you'll be guided back to Sonnet 4.6. Follow the guidance to save costs.

### 6. Completion

After all steps (A0-A7), you'll have these files:

```
my-new-project/
├── CLAUDE.md                              ← Instructions for Claude (max 200 lines)
├── .gitignore                             ← Security basics
├── docs/
│   ├── service-overview.md                ← Service overview
│   ├── architecture.md                    ← Architecture & tech stack
│   ├── specs/                             ← Specs storage (used in Phase B)
│   └── architecture-decisions/            ← ADR (Architecture Decision Record)
└── .claude/
    ├── skills/
    │   ├── consult/SKILL.md               ← Requirements consultation skill
    │   └── commit/SKILL.md                ← Commit skill
    └── agents/
        ├── system_architect.md            ← System architect
        ├── developer.md                   ← Implementation (e.g., backend_developer)
        └── qa_engineer.md                 ← QA
```

> **Note**: Start with 3 agents (architect, developer, qa) and add more as the project grows. See [Sub-agents](07-sub-agents.md) for details.

Claude displays **Phase B Transition Guide** (daily development cycle, model selection, context management tips) and completes.

**Now you're ready to enter Phase B (daily development cycle).**

## Step Overview

For details and rationale on each step, see [Phase A: Project Setup](05-workflow-setup.md).

| Step | Purpose | Recommended Model |
|----------|------|-----------|
| **A0** | Auto-initialize (.gitignore, directories, git init) | — |
| **A1** | Service overview — articulate what you're building | Sonnet |
| **A2** | /consult skill — create a consultation partner | Sonnet |
| **A3** | Validate requirements — finalize MVP and priorities | Sonnet |
| **A4** | Architecture decision — tech stack and design patterns | **Opus** |
| **A5** | CLAUDE.md — define project rules | Sonnet |
| **A6** | Sub-agents — start with minimal setup | Sonnet |
| **A7** | Skills, Hooks, and initial commit | Sonnet |

## FAQ

### Can I stop in the middle?

Yes. Use `claude --continue` to resume the previous session and continue from where you left off. If the session is old, `/clear` first, then say "I want to resume from A4. Please read docs/service-overview.md and docs/architecture.md" to jump to that step.

### I want to skip A1-A3 and start from A4

If service overview and requirements are already decided:

```
> /kickstart
> Service overview is in docs/service-overview.md.
  I want to start from A4: Architecture Decision.
```

Claude will read the existing documents and proceed from A4.

### Do I need to do all steps in one session?

No. **A1-A3 on Day 1, A4-A7 on Day 2** is recommended. Sleeping on requirements often reveals what you missed.

### The generated agents or skills aren't perfect

Edit `.claude/agents/` or `.claude/skills/` files manually. Or instruct Claude Code "Add X to the backend_developer agent's Constraints" and it will fix it. Project settings grow as you use them.

### I want to change .gitignore contents

The `.gitignore` created in A0 is generic. After your tech stack is decided (A4+), add project-specific entries. For example, for Python add `__pycache__/` and `.venv/`.
