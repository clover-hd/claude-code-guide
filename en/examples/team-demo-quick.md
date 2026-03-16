# Quick Demo: Seeing Agent Teams Work

Estimated time: **10-15 minutes**

A procedure for demoing parallel agent team development right after Phase A completion. Focus on showing **how one feature is divided among the team** without needing to fully implement all features.

---

## Prerequisites

- Phase A (/kickstart) is complete
- At least one spec file in `docs/specs/`
- Team feature enabled in `~/.claude/settings.json`

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

---

## Pre-Demo Setup (2 minutes)

### 1. Prepare one spec

Use an existing spec from Phase A `/consult` brainstorming in `docs/specs/`.

If none exists, you can create one manually with this content:

```markdown
# Commit Timeline Display

## Overview
Display the commit history from a local git repository as a timeline chart grouped by date.

## Input
- Local git repository path (e.g.: ~/demo-repos/hono.git)

## Output
- Bar or line chart with date on horizontal axis, commit count on vertical axis
- Filterable by committer name

## Technical constraints (Important)
- Data retrieval only via `git log` command execution (no GitHub API)
- No external API network requests
- Parse git log with custom implementation (use `--format` option to fetch needed info)
- No database (convert git log output directly to JSON)

## How to Get Data
Backend parses output from:
  git log --format="%H|%an|%ae|%ad|%s" --date=iso <repo-path>

Fields to retrieve:
- Commit hash
- Author name
- Author email
- Datetime (ISO format)
- Commit message

## Work Division
- Backend: Execute the above git log command, parse it, and create date-grouping API
- Frontend: Render timeline with chart library
- Testing: Unit tests for backend data transformation logic (using sample git log output)
```

Save this as `docs/specs/feature-timeline.md`.

### 2. Confirm Demo Repositories

Verify that pre-cloned repositories exist for visualizer testing:

```bash
ls ~/demo-repos/
# hono.git  zod.git  claude-code-guide.git etc.
```

---

## Demo Time (10 minutes)

### Step 1: Say This First

> "I'm now going to **have Claude Code form a team**. A leader, backend developer, frontend developer, and test engineer AI will **work simultaneously on one PC, communicating with each other as they develop**. Watch as the same teamwork humans do unfolds."

### Step 2: Instruct the Team

```
> Based on the spec in docs/specs/feature-timeline.md,
  develop it with the team in parallel. Must follow the spec's "technical constraints".

  Team:
  - researcher: Research chart libraries suitable for timelines
  - backend: Execute git log, parse it, create date-grouped API
             (No GitHub API. git log only)
  - frontend: Render timeline with chart
  - qa: Unit tests for backend

  Once researcher's investigation is done, share with frontend.
  When everyone's done, run tests and report results.
```

### Step 3: Explain as You Watch

As the team works, use `Shift + ↓` to switch between members and explain.

**What to highlight:**

```
① Team formation moment
  "Leader just created the task list and launched 4 members"

② Working in parallel
  "Shift+↓ to switch. See? Backend's writing API while
   researcher's investigating libraries. Simultaneous."

③ Member communication
  "Researcher finished, leader shared with frontend.
   Same as human Slack coordination, fully automatic."

④ Test execution
  "Everyone's done implementing, qa's running tests now.
   Same flow as human QA."

⑤ Complete
  "All members done, leader integrates.
   All happened on this one PC."
```

### Step 4: Show Results

When the team finishes:

```bash
# Start dev server (depends on tech stack)
npm run dev  # or yarn dev, etc.
```

Open browser, specify the path to `~/demo-repos/hono.git`, and if the timeline displays, perfect.

> Even if the team's implementation doesn't work perfectly, that's fine. The demo's goal is **showing AI teams collaborating** — not perfect code.

---

## Post-Demo Notes (Good to Mention)

```
"What you just saw is experimental, but this is where AI development is headed.

 For everyday development, there's a slightly more stable approach called "sub-agents" —
 not parallel like a team, but more of a pair-programming style, one instruction at a time.

 Start with sub-agents to build the habit,
 then try team development once you're comfortable."
```

---

## If Things Don't Work

| Situation | Workaround |
|-----------|-----------|
| Team doesn't form | Check `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` in `settings.json` |
| Member stalls | Tell the leader session "re-instruct the stalled member" |
| Code won't build | Explain: "Demo goal is showing team collaboration. Polish code later." |
| Takes too long | Reduce team to 2 (backend + frontend) and retry |
