# Practical Example: Building a Git Commit History Visualizer

This document is a practical guide for getting your project up and running from scratch using the [/kickstart skill](../17-kickstart-skill.md) and advancing development through Phase B.

By actually following these steps, you'll experience the entire guide workflow firsthand.

---

## Prerequisites

1. Claude Code is installed ([installation instructions](../01-setup.md))
2. The `/kickstart` skill is installed ([setup instructions](../17-kickstart-skill.md#setup))
3. Demo repositories are prepared in advance (see below)

### Preparing Demo Repositories

Prepare repositories for the visualizer to display by cloning them in advance.

```bash
mkdir -p ~/demo-repos && cd ~/demo-repos

# Recommended: small and fast to clone & lots of contributors
git clone --bare https://github.com/honojs/hono.git
git clone --bare https://github.com/colinhacks/zod.git

# This guide's own repository ("We built this together with AI")
git clone --bare https://github.com/clover-hd/claude-code-guide.git
```

> Using `--bare` retrieves just the git history without source code, making it faster and more storage-efficient.

| Repository | Features | Demo Highlights |
|-----------|----------|-----------------|
| **honojs/hono** | Lightweight web framework | Many contributors, active development patterns |
| **colinhacks/zod** | TS validation library | Growing commit frequency during growth phase |
| **clover-hd/claude-code-guide** | This guide itself | Story: "A repository built with AI" |

---

## Phase A: Project Setup

### Step 0: Create Project → Run /kickstart

```bash
mkdir git-visualizer && cd git-visualizer
claude
```

Once Claude Code starts:

```
> /kickstart
```

A0 (automatic initialization) runs, creating `.gitignore` and directories.

---

### Step 1 (A1): Service Overview — Tell Claude

Claude will ask "What would you like to build?" Answer with something like:

```
I want to build a web app that visualizes commit history in a Git repository.
```

Claude will dive deeper, so communicate these key points:

| Question | Reference Answer |
|----------|----------|
| Who's the target? | Individual engineers to small teams |
| What matters most? | Visual appeal and ease of use |
| Vision? | A dashboard where you just specify a repository and instantly see your team's development activity |
| MVP features? | See below |

**Example MVP features (narrow down to about 4):**

1. Load a local git repository by specifying its path
2. Display commit history as a timeline
3. Show contributor contributions as a graph
4. Display commit frequency by day and time of day

**Example future features:**
- Visualize branch branching and merging
- Heatmap of file changes
- GitHub API integration (remote repository support)
- Team comparison dashboard

> **Key Point**: Keep the MVP to "the minimum that would make it fun." If there's too much, Claude will ask "Which can we defer?"

Once Claude creates `docs/service-overview.md`, review it and say "OK."

---

### Step 2 (A2): Create /consult Skill

Claude automatically creates the `/consult` skill. Verify that the service's vision and values are reflected.

No special instructions needed — Claude will proceed. Review and say "OK."

---

### Step 3 (A3): Requirement Brainstorming

Claude uses `/consult` to dive deeper into requirements. Discussion progresses from perspectives like:

- **User Flow**: Specify repository → analyze → display dashboard
- **Error Cases**: What if the path specified isn't a git repository?
- **Data Volume**: What happens with huge repositories (tens of thousands of commits)?
- **Authentication**: Not needed (local tool, no login)

```
Thinking hints:
- "Should repository specification be text input or drag-and-drop?"
- "Do we need loading indicators during analysis?"
- "Should date range filtering be available?" → Is this MVP or future?
```

Once brainstorming is complete, `docs/service-overview.md` is updated. Review and say "OK."

> **Tip**: Sleeping on this overnight helps — next day you'll realize "Oh, we need that too."

---

### Step 4 (A4): Architecture Decision ← Most Important

> **Switch to Opus here.** Claude will prompt you.
> ```
> /model opus
> ```

Claude will present technology options in a comparison table. Here's guidance for decision-making.

#### Decision-Making Points

Since this project is "a local web app":

| Perspective | Recommended Direction | Reason |
|------------|------------------|--------|
| Frontend | React or Vue + chart library | Visualization is primary, charting library richness matters |
| Backend | Lightweight framework | Mainly git command execution and JSON conversion; no heavy framework needed |
| DB | None or SQLite | MVP just reads directly from git; SQLite available for caching |
| Infrastructure | Local execution | MVP on localhost, set up for future deployment |

```
You can tell Claude:
"I want visually appealing chart libraries.
For MVP, no DB — just read directly from git.
Choose the tech stack and show me a comparison table."
```

Claude creates `docs/architecture.md` and records important decisions as ADRs in `docs/architecture-decisions/`.

Review and say "OK."

---

### Step 5 (A5): Create CLAUDE.md

> **Switch back to Sonnet.**
> ```
> /model sonnet
> ```

Claude creates the project configuration file `CLAUDE.md`.

Verification points:
- Tech stack matches the A4 decision
- Security rules are included
- Stays under 200 lines

Say "OK" and move forward.

---

### Step 6 (A6): Create Sub-agents

Claude creates an agent team matching the architecture.

For this project, you'll likely get a team like:

| Agent | Role |
|-------|------|
| system_architect | Guardian of overall design |
| tech_researcher | Technology investigation (chart library comparison, etc.) |
| frontend_developer | UI and chart implementation |
| backend_developer | Git analysis logic and API |
| qa_engineer | Testing |
| technical_writer | Documentation |

Verify that each agent's description includes **specific technology stack names** (not just "frontend developer" but "build dashboard with React + Recharts").

---

### Step 7 (A7): Skills, Hooks, and Initial Commit

Claude creates and executes:

1. `/commit` skill
2. Hooks configuration (formatter, optional)
3. Test strategy confirmation
4. Initial commit

When asked about test strategy:
```
Reference:
- Unit tests: git analysis logic tests (commit count, etc.)
- E2E: Can defer for MVP
```

Once initial commit completes, **Phase B transition guide** appears.

---

## Phase B: Development Cycle

Once Phase A is complete, implement features one by one using this cycle:

### Cycle Flow

```
1. /consult                            → Brainstorm feature requirements
2. Shift+Tab                           → Make implementation plan in Plan Mode
2.5. Persistence                       → Save specification to docs/specs/
3. @.claude/agents/xxx.md for implementation → Instruct specialized agent to implement
3.5. Testing                           → Run tests after implementation
4. /commit                             → Commit following rules
```

### Using Sub-agents

In Phase B's development cycle, utilize the agents created in Phase A's Step 6.

#### How to Call Agents

When you type `@` in Claude Code's prompt, file path completion works. Specify the agent file path:

```
> @.claude/agents/backend_developer.md
> (write your instructions here)
```

> **Completion tip**: Type `@.cl` and `.claude/` appears as an option. Then select `agents/` → filename.

#### Agent Usage Map

```
/consult (requirement brainstorming)
  ↓
Plan Mode (implementation planning)
  ↓ Here, ask @.claude/agents/system_architect.md for design review
  ↓
Persistence (save to docs/specs/)
  ↓
Implementation ← Agents shine here
  ↓
Testing ← Ask @.claude/agents/qa_engineer.md to create and run tests
  ↓
/commit
```

#### Information Handoff Between Agents

Sub-agents can reference current context (conversation flow). There are two patterns for information handoff:

**Pattern A: Consecutive calls in same session (without /clear)**

```
@.claude/agents/tech_researcher.md investigates
  ↓ context remains
@.claude/agents/backend_developer.md is called
  → Can see previous investigation results and start work immediately
```

- Information passes without file saving
- But consumes context (longer conversations degrade quality)
- Without `/clear`, next agent might act on previous context

**Pattern B: Reset session, then call (using /clear)**

```
@.claude/agents/tech_researcher.md investigates → saves to docs/research/
  ↓
/clear to reset context
  ↓
@.claude/agents/backend_developer.md is called
  → Tell it to "read docs/research/xxx.md and implement" — share info via files
```

- Documentation remains for future reference
- Conserves context
- Info must be saved to file or it disappears

**Pattern B is recommended** because:

1. **Reusability**: Investigation results remain in files, referenced from other sessions/agents
2. **Context Savings**: Context margin is crucial for long feature development
3. **Best Practice**: "Always save deliverables" is fundamental to project management where knowledge persists even when sessions disappear

> Pattern A is handy for "quick questions, immediate handoff" type short tasks. Use what fits your situation.

#### Example Agent Calls

**tech_researcher — Pre-implementation investigation**

```
> @.claude/agents/tech_researcher.md
> Research libraries for parsing git log output into JSON.
  Compare pros/cons of building a parser vs. using libraries.
  Save results to docs/research/git-log-parsing.md.
```

```
> @.claude/agents/tech_researcher.md
> Compare 3 chart libraries good for rendering commit frequency heatmaps.
  Look at performance, customizability, and bundle size.
  Save results to docs/research/chart-libraries.md.
```

> Investigation tasks are efficiently delegated to tech_researcher. Read-only and safe, plus doesn't consume main context.
>
> **Important**: Always have research results saved to `docs/research/`. Sub-agent context ends with the session, so without saving, the next agent can't reference it.

**backend_developer — Git analysis logic**

```
> @.claude/agents/backend_developer.md
> Following the investigation results in docs/research/git-log-parsing.md and
  the specification in docs/specs/feature-git-reader.md,
  implement the module that retrieves commit information from git repositories.
  Write unit tests too.
```

**frontend_developer — UI and chart implementation**

```
> @.claude/agents/frontend_developer.md
> Following the spec in docs/specs/feature-timeline.md,
  implement the timeline chart component.
  Set it up so it can be tested with sample data.
```

**system_architect — Design review**

```
> @.claude/agents/system_architect.md
> Review the current implementation from these perspectives:
  - Is the separation of concerns between backend and frontend appropriate?
  - Is there any waste in data flow?
  - Is the structure set up for future GitHub API integration?
```

> Getting system_architect to review after 2-3 features are done helps find design issues early.

**qa_engineer — Testing**

```
> @.claude/agents/qa_engineer.md
> Enhance unit tests for the git analysis module.
  Cover these edge cases:
  - Repository with 0 commits
  - Handling of merge commits
  - Commit messages containing Japanese characters
```

**technical_writer — Documentation**

```
> @.claude/agents/technical_writer.md
> Create README.md. Include:
  - Project overview and where to place screenshots
  - Setup instructions
  - How to use it
  - Development method (for contributors)
```

#### Agent Usage Tips

| Tip | Explanation |
|------|-----------|
| **Pass specifications** | When you say "follow the spec in docs/specs/xxx.md", agent reads spec then implements |
| **Save investigation results** | Always have tech_researcher save to `docs/research/`. Without saving, next agent can't reference |
| **One agent, one task** | Don't say "build UI and API too" — delegate by responsibility |
| **Investigate → Save → Implement order** | tech_researcher investigates → save to `docs/research/` → pass both investigation and spec to implementation agent |
| **Include reviews** | Have system_architect review once implementation hits a milestone to maintain quality |
| **Separate testing** | Have implementer write tests too, but having qa_engineer write additional edge case tests improves coverage |

---

### Recommended Implementation Order

Implementing the 4 MVP features in this order shows progress at each stage:

#### First Cycle: Load git Repository and Fetch Data

```
> /consult
> As the first feature, I want to load a local git repository and
  retrieve commit information in JSON format.
  Save the spec to docs/specs/feature-git-reader.md.
```

Once spec is saved, investigate → implement:

```
> /clear
> @.claude/agents/tech_researcher.md
> Research git log output format and parsing methods.
  Summarize what information you can get with the --format option.
  Save results to docs/research/git-log-parsing.md.
```

After reviewing investigation results, `/clear` then implement:

```
> /clear
> @.claude/agents/backend_developer.md
> Following the investigation results in docs/research/git-log-parsing.md and
  the spec in docs/specs/feature-git-reader.md, implement it.
  Write unit tests too.
```

What you're building:
- Repository path input UI
- git log execution and parsing logic
- Commit data structure (datetime, author, message, changed lines, etc.)

```
Completion image: Input path → commit data displays as JSON in console or screen
```

#### Second Cycle: Timeline Display

```
> /consult
> I want to visualize retrieved commit data as a timeline.
  Think of it like horizontal axis for date, vertical for commit count.
  Save spec to docs/specs/feature-timeline.md.
```

Once spec is saved, investigate → implement:

```
> /clear
> @.claude/agents/tech_researcher.md
> Compare timeline chart libraries.
  Consider compatibility with the tech stack from A4.
  Save results to docs/research/chart-libraries.md.
```

After reviewing, `/clear` then implement:

```
> /clear
> @.claude/agents/frontend_developer.md
> Following the investigation in docs/research/chart-libraries.md and
  the spec in docs/specs/feature-timeline.md,
  implement the timeline chart. Make it work with sample data.
```

What you're building:
- Group commit data by date
- Render timeline with chart library
- Basic dashboard layout

```
Completion image: Load repository → timeline chart displays
```

**Recommended: Have system_architect review once here:**

```
> @.claude/agents/system_architect.md
> Review the first and second cycles of implementation.
  Is data flow and component separation appropriate?
  Any issues that might come up adding the remaining 2 features?
```

#### Third Cycle: Contributor Contributions

```
> /consult
> I want to add a feature to visualize contributor contributions.
  Pie chart or bar chart showing who committed how much.
  Save spec to docs/specs/feature-contributors.md.
```

Once spec is saved, `/clear` then implement:

```
> /clear
> @.claude/agents/frontend_developer.md
> Following the spec in docs/specs/feature-contributors.md, implement it.
```

#### Fourth Cycle: Time-of-Day Analysis

```
> /consult
> I want to add time-of-day analysis of commits.
  Want to see which day of week and what time commits happen most in a heatmap.
  Save spec to docs/specs/feature-heatmap.md.
```

Once spec is saved, `/clear` then implement:

```
> /clear
> @.claude/agents/frontend_developer.md
> Following the spec in docs/specs/feature-heatmap.md, implement it.
```

**Wrapping up after MVP completion:**

```
> @.claude/agents/qa_engineer.md
> Test all features end-to-end. If any areas lack coverage, add tests.
```

```
> @.claude/agents/technical_writer.md
> Create README.md. Write setup instructions and usage guide.
```

---

## What to Keep in Mind Each Cycle

### After /consult

- After Plan Mode planning, **always save specs to `docs/specs/`**
- Be explicit: "Save the spec to docs/specs/feature-timeline.md"

### During Implementation

- Say "write tests too"
- Once it works, validate with "run tests and show results"

### Committing

```
> /commit
```

That's it — it creates rule-following commits.

### Before Next Cycle

```
> /clear
```

Reset context before tackling the next feature.

---

## When You Get Stuck

| Situation | Solution |
|-----------|----------|
| Claude's implementation doesn't work | "Run tests" to verify. Paste errors as-is for fix instructions |
| Still broken after 2 fixes | `/clear` then re-instruct from scratch including what you learned |
| Context is full | `/compact` to compress, or `/clear` to reset |
| Want to undo | `Esc + Esc` to rewind to checkpoint |
| Unsure about design | Switch with `/model opus` to discuss |

---

## Advanced: Parallel Development with Agent Teams

> **This is an experimental feature.** We recommend completing the MVP with the sub-agent method described above first.

### What This Is, in a Sentence

**One PC, one terminal — AI forms a team, communicates with each other, and develops in parallel.**

The same teamwork humans do happens on your single PC.

### Contrast with Human Teamwork

```
Human teamwork                    AI agent team
─────────────────────────         ─────────────────────────
PM assigns tasks via Slack        → Leader assigns via task list
Backend developer implements      → backend session implements
Frontend developer implements in parallel → frontend session implements in parallel
Code review when done              → architect reviews and points out issues
QA tests                           → qa writes and runs tests
Slack: "Ready to merge?"           → Message: "Implemented, review please"
Everyone works on same git repo    → Everyone works on same git repo
```

The difference: **this all happens in one terminal in minutes to tens of minutes.**

### Setup

Add to `~/.claude/settings.json` (if not already set):

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

### Demo: Second Cycle Parallel Development with Team

Example of doing the second cycle (timeline display) with the team, starting from where the first cycle (git loading) is done.

#### 1. Instruct the Leader

```
> I want to parallelize the second cycle's "timeline chart" with the team.
  Based on the spec in docs/specs/feature-timeline.md,
  form these teams and proceed in parallel:

  - researcher: Research and compare chart libraries
  - backend: Date-grouped commit data API
  - frontend: Timeline chart UI implementation
  - qa: Test creation
```

#### 2. Leader Forms Team and Starts

The leader auto-forms the team and assigns tasks. The following happens **simultaneously before your eyes:**

```
┌─────────────────────────────────────────────────────────┐
│ Leader                                                   │
│ > Forming team. Creating task list...                   │
│ > Launched researcher, backend, frontend, qa            │
└─────────────────────────────────────────────────────────┘
     │
     ├── researcher launches
     │   "Researching chart libraries...
     │    Comparing Recharts, Chart.js, D3.js"
     │
     ├── backend launches
     │   "Implementing commit data grouping logic...
     │    Creating src/services/commit-grouper.ts"
     │
     ├── frontend launches
     │   "Implementing dashboard layout...
     │    Creating src/components/Timeline.tsx"
     │
     └── qa launches
         "Considering test strategy...
          Inventorying test cases"
```

#### 3. Team Members Communicate

```
researcher → Leader:
  "Research complete. Recommending Recharts. Reasons:
   High React compatibility, abundant timeline chart samples.
   Saved comparison to docs/"

Leader → frontend:
  "Decided on Recharts.
   Refer to researcher's investigation results and continue"

backend → Leader:
  "Date grouping API implementation done.
   Tests passing."

Leader → qa:
  "Backend implementation complete. Write tests."

frontend → Leader:
  "Timeline component done.
   Want to wire up to backend API.
   What's the endpoint spec?"

Leader → frontend:
  "Refer to backend's src/services/commit-grouper.ts.
   Interface is like this..."

qa → Leader:
  "All tests created. 15/15 passing.
   Edge cases (empty repo, single commit) covered"
```

#### 4. Leader Integrates and Commits

Once all members complete, leader integrates and commits:

```
Leader:
  "All members complete.
   - Library research ✓
   - Backend API ✓
   - Frontend UI ✓
   - Tests 15/15 pass ✓
   Committing now."
```

#### 5. Terminal View

Use `Shift + ↓` to switch between team members and see **in real-time what each is doing**.

```
┌─ Leader ──────────────────────────────────────────┐
│ Task progress:                                    │
│ ✓ researcher: library research complete           │
│ ✓ backend: API implementation complete            │
│ ● frontend: UI implementation... (80%)            │
│ ✓ qa: test creation complete                      │
│                                                   │
│ [Shift+↓ to switch to other members]              │
└───────────────────────────────────────────────────┘
```

### More Boldly: Parallelize All 4 MVP Features

Once comfortable, you can let the team handle the entire MVP:

```
> Based on the 4 spec files in docs/specs/,
  parallelize development of all MVP features.

  Team composition:
  - backend: git loading + data conversion API
  - frontend-timeline: timeline chart
  - frontend-contrib: contributor contributions graph
  - frontend-heatmap: time-of-day heatmap
  - qa: tests for each feature (sequential as members complete)

  Once backend finishes, share with frontend members.
  Once all done, qa tests everything, then commit together.
```

**What takes a human team days happens in tens of minutes before your eyes** — this is the impact of agent teams.

### Cautions

| Item | Details |
|------|---------|
| **Token consumption** | Uses context per member. 4-person team ≈ 4 session costs |
| **Experimental** | Unexpected errors or member stalling can happen |
| **Specs are essential** | Team members read `docs/specs/`. Ambiguous specs → scattered implementations |
| **Conflicts** | Multiple members touching same file → git conflicts. Keep responsibilities clear |
| **Start small** | Don't jump to all features. Try 2-3 people on 1 feature first |

### Choosing Between Sub-agent and Team Methods

```
Sub-agent method (@.claude/agents/xxx.md calls)
  → "Pair programming" style: instruct one by one
  → Stable, low cost
  → Start here

Agent teams
  → "Team development" style: multiple people at once
  → Parallel and fast, but costly and experimental stage
  → Level up after getting comfortable with sub-agents
```

---

## Summary

```
Phase A (/kickstart) builds foundation              → About 1-2 sessions
Phase B implements features one by one              → 1 feature = 1 cycle
  ├─ Sub-agent method (basic)                       → Instruct one by one
  └─ Agent team method (advanced)                   → AI team develops in parallel
4 features complete → MVP done                      → Days to ~1 week
```

The key is "don't try to build everything at once." Verify working features after each cycle.

Agent teams give a glimpse of the future of development. Master the sub-agent basics first, then explore the world of team development.
