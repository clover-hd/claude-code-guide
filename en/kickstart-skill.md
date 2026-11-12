# /kickstart Skill — Automate Project Setup

[< Back to Guide](../README.en.md)

---

## What Is This?

This skill automatically guides Claude Code through the steps of [Phase A: Project Setup](workflow-setup.md) (A0-A8) in a conversational manner.

You can follow the guide manually, but with `/kickstart`, **Claude Code itself understands the guide steps and builds your project foundation with you**.

### What the Skill Does Automatically

Claude Code walks through [Phase A steps](workflow-setup.md) (A0-A8) interactively. Specifically:

- Initialize project (`.gitignore`, docs/ structure and documentation policy, git init)
- Articulate requirements (principles to keep, what we won't build) and validate them
- Decide and record the base spec and implementation policy (which way to lean when in doubt)
- Decide where tasks live (`docs/tasks.md` or GitHub Issues) and create the first tasks from the MVP
- Build CLAUDE.md (an index and a few rules), four sub-agents, and skills
- Set up a commit guard that blocks commits of secrets
- Make initial commit

For details on each step, see [workflow-setup.md](workflow-setup.md).

## Setup

### Method 1: Install as Personal Skill (Available in All Projects)

```bash
# Create directory and download
mkdir -p ~/.claude/skills/kickstart
curl -fsSL https://raw.githubusercontent.com/clover-hd/claude-code-guide/main/skills/kickstart/SKILL.md \
  -o ~/.claude/skills/kickstart/SKILL.md
```

Now `/kickstart` works in **any project**.

### Method 2: Install as Project Skill (This Project Only)

```bash
# Run in project root
mkdir -p .claude/skills/kickstart
curl -fsSL https://raw.githubusercontent.com/clover-hd/claude-code-guide/main/skills/kickstart/SKILL.md \
  -o .claude/skills/kickstart/SKILL.md
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
        ✓ docs/README.md (documentation policy)
        ✓ docs/decisions/
        ✓ docs/_wip/
        ✓ git init

        Now let's create A1: Requirements document.
        What do you want to build? Tell me in one sentence.

You: A platform for managing restaurant reservations and reviews

Claude: Great. Let me dig deeper.
        - Who's the target? (Restaurant owners? Users? Both?)
        - What are the "principles to keep" specific to this service?
        - Compared to similar services, what will you deliberately not build?
        ...
```

Claude asks questions at each step and creates documents and files based on your answers.

### 4. Review each step

Claude asks for confirmation when each step is complete. **Review carefully before moving forward.**

```
Claude: Created docs/requirements.md.
        Please review. Tell me if you need changes.
        If OK, we'll move to the next step (A2: /consult skill creation).

You: I want to add search functionality to the MVP

Claude: Got it. Added search and updated.
        (Updated docs/requirements.md)
        Is this OK?

You: OK, let's move forward
```

### 5. Model switching guidance

At A4 (Base spec) and A4.5 (Implementation policy), you'll be guided to switch to Opus.

```
Claude: Next is A4: Deciding the base spec.
        Deep design decisions ahead, so I recommend switching to Opus.
        Please switch with /model opus before continuing.
```

From A5 onwards, you'll be guided back to Sonnet. Follow the guidance to save costs.

### 6. Completion

After all steps (A0-A8), you'll have these files:

```
my-new-project/
├── CLAUDE.md                              ← Instructions: an index and a few rules
├── .gitignore                             ← Security basics
├── .githooks/pre-commit                   ← Also checks human commits
├── scripts/check-staged.sh                ← Checks for secrets and DB files
├── docs/
│   ├── README.md                          ← Documentation policy (what goes where)
│   ├── requirements.md                    ← Requirements and principles to keep
│   ├── spec.md                            ← Base spec (only the stable skeleton)
│   ├── implementation-policy.md           ← Implementation policy (which way to lean when in doubt)
│   ├── decisions/                         ← Why we decided it (one decision per file)
│   ├── tasks.md                           ← Tasks (if the file was chosen)
│   └── _wip/                              ← Detailed design during implementation (promote or delete when done)
└── .claude/
    ├── settings.json                      ← Hook registration
    ├── hooks/guard-bash.mjs               ← Checks the agent's commits
    ├── skills/
    │   ├── consult/SKILL.md               ← Requirements consultation skill
    │   ├── ask-advisor/SKILL.md           ← Consult the advisor
    │   ├── commit/SKILL.md                ← Commit skill
    │   ├── task/SKILL.md                  ← View, add, and close tasks
    │   ├── overnight/SKILL.md             ← Advance tasks while you sleep
    │   └── handoff/SKILL.md               ← Leave a handoff before clearing
    └── agents/
        ├── advisor.md                     ← Advisor and milestone review (read-only)
        ├── developer.md                   ← Implementation
        ├── qa-engineer.md                 ← Testing
        └── code-reviewer.md               ← Light review on every commit
```

> **Note**: Start with 4 agents and add more as the project grows. The advisor uses Opus by default. To switch it to Fable, see [Sub-agents](sub-agents.md#using-fable-for-the-advisor).
> If you chose GitHub Issues as the task location in A4, `docs/tasks.md` is not created and the first tasks are created as Issues (you'll be asked to confirm before they are created).
> The hook is written in the language chosen in A4 (`guard-bash.mjs` for Node.js, `guard_bash.py` for Python). If you create runbook skills in A8, they are added under `.claude/skills/`.

Claude displays **Phase B Transition Guide** (daily development cycle, model selection, context management tips) and completes.

**Now you're ready to enter Phase B (daily development cycle).**

## Step Overview

For details and rationale on each step, see [Phase A: Project Setup](workflow-setup.md).

| Step | Purpose | Recommended Model |
|----------|------|-----------|
| **A0** | Auto-initialize (.gitignore, directories, git init) | — |
| **A1** | Requirements — what to build, principles to keep, what we won't build | Sonnet |
| **A2** | /consult skill — create a consultation partner | Sonnet |
| **A3** | Validate requirements — finalize MVP and priorities | Sonnet |
| **A4** | Base spec — tech stack, branch strategy, task location, commands | **Opus** |
| **A4.5** | Implementation policy — which way to lean when in doubt | **Opus** |
| **A5** | CLAUDE.md — an index and a few rules | Sonnet |
| **A6** | Sub-agents — advisor / developer / qa-engineer / code-reviewer | Sonnet |
| **A7** | Skills, commit guard, first tasks, and initial commit | Sonnet |
| **A8** | Runbook skills (optional) — irreversible operations | Sonnet |

## FAQ

### Can I stop in the middle?

Yes. Use `claude --continue` to resume the previous session and continue from where you left off. If the session is old, `/clear` first, then say "I want to resume from A5. Please read requirements.md, spec.md, and implementation-policy.md in docs/" to jump to that step.

### I want to skip A1-A3 and start from A4

If requirements are already decided:

```
> /kickstart
> Requirements are in docs/requirements.md.
  I want to start from A4: Deciding the base spec.
```

Claude will read the existing documents and proceed from A4.

### Do I need to do all steps in one session?

No. **A1-A3 on Day 1, A4-A8 on Day 2** is recommended. Sleeping on requirements often reveals what you missed.

### The generated agents or skills aren't perfect

Edit `.claude/agents/` or `.claude/skills/` files manually. Or instruct Claude Code "Add X to the developer agent's scope of consultation" and it will fix it. Project settings grow as you use them.

### Which task location should I choose?

For solo development, `docs/tasks.md`; for a team using Pull Requests, GitHub Issues. Either way, day-to-day operations go through the `/task` skill, so usage is the same. To switch later, rewrite the procedure in the `/task` skill and the task sections in the developer and advisor definitions, then record it in `docs/decisions/` as a new decision.

### Can it implement while I sleep?

Type `/overnight` before going to bed and it implements the delegated tasks in order until morning. After confirming which tasks to delegate and the limit up front, it asks no more questions; points that need a decision are left under "Awaiting Human Decision" and it moves on. Work happens on an `overnight/<date>` branch, with no push. Normally (when not using `/overnight`), it asks you on the spot when a decision is needed. See [Phase B](workflow-daily.md#advance-while-you-sleep--overnight) for details.

### I want to change .gitignore contents

The `.gitignore` created in A0 is generic. After your tech stack is decided (A4+), add project-specific entries. For example, for Python add `__pycache__/` and `.venv/`.
