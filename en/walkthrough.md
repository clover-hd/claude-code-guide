# Practical Example: Building an Outing Planner

This document is a practical guide for getting your project up and running from scratch using the [/kickstart skill](kickstart-skill.md) and advancing development through Phase B.

By actually following these steps, you'll experience the entire guide workflow firsthand.

> **Note**: This project uses the [Open-Meteo API](https://open-meteo.com/) to retrieve weather data. It's free for non-commercial and learning purposes, but please check the [terms of service](https://open-meteo.com/en/terms) before running.

---

## Prerequisites

1. Claude Code is installed ([installation instructions](setup.md))
2. The `/kickstart` skill is installed ([setup instructions](kickstart-skill.md#setup))

No special data preparation is needed. Location data is CRUD that you'll register within the app itself, so you can get started right away.

---

## Phase A: Project Setup

### Step 0: Create Project → Run /kickstart

```bash
mkdir outing-planner && cd outing-planner
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
I want to build a web app that lets you register your favorite outing spots
and combines them with weather forecasts to help you decide where to go today.
```

Claude will dive deeper, so communicate these key points:

| Question | Reference Answer |
|----------|----------|
| Who's the target? | Individuals to families |
| What matters most? | Visual appeal and ease of use |
| Vision? | An app where you register spots in advance, then get today's recommendations based on the weather |
| MVP features? | See below |

**Example MVP features (narrow down to about 4):**

1. Register, edit, and delete favorite outing spots (CRUD)
2. Fetch and display weather forecasts for current location and registered spots via weather API
3. Display weekly weather as graphs (temperature trends and precipitation probability)
4. Suggest "today's recommended spots" based on weather and category

**Example future features:**
- Map display (Leaflet + OpenStreetMap)
- Photo uploads for spots
- Sharing with family and friends
- Visit history logging and reflection

> **Key Point**: Keep the MVP to "the minimum that would make it fun." If there's too much, Claude will ask "Which can we defer?"

Once Claude creates `docs/service-overview.md`, review it and say "OK."

---

### Step 2 (A2): Create /consult Skill

Claude automatically creates the `/consult` skill. Verify that the service's vision and values are reflected.

No special instructions needed — Claude will proceed. Review and say "OK."

---

### Step 3 (A3): Requirement Brainstorming

Claude uses `/consult` to dive deeper into requirements. Discussion progresses from perspectives like:

- **User Flow**: Register spot → check weather → see recommendations
- **Error Cases**: What if the weather API is down? What if location isn't available?
- **Data Volume**: How does performance scale as more spots are added?
- **Authentication**: Not needed (local tool, no login required)

```
Thinking hints:
- "How should we categorize spots? (parks, cafes, museums, shopping...)"
- "What's the weather threshold? What precipitation % triggers indoor recommendations?"
- "Should the recommendation logic be simple? (Sunny → outdoor, rainy → indoor)"
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

Since this project is "a local web app + external API integration":

| Perspective | Recommended Direction | Reason |
|------------|------------------|--------|
| Frontend | React or Vue + charting library | Weather graphs and card displays are central; charting library richness matters |
| Backend | Lightweight framework | Focused on CRUD and API relay; no heavy framework needed |
| DB | SQLite | Necessary for persisting location data; lightweight is sufficient |
| External API | Open-Meteo (no API key) | Free, no authentication, and permissive limits for non-commercial use |
| Infrastructure | Local execution | MVP runs on localhost; set up for future deployment |

```
You can tell Claude:
"I want visually appealing weather cards and graphs.
Use SQLite for the DB and Open-Meteo for the weather API.
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
| developer | Full-stack implementation (CRUD API, weather API integration, UI, charts) |
| qa_engineer | Testing |

Verify that each agent's description includes **specific technology stack names** (not just "developer" but "build full-stack with backend framework, SQLite, React + Recharts").

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
- Unit tests: CRUD operations, weather API integration mocking, recommendation logic
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

### Recommended Implementation Order

Implementing the 4 MVP features in this order shows progress at each stage:

#### First Cycle: Spot CRUD

```
> /consult
> As the first feature, I want to register, edit, and delete outing spots.
  Each spot has a name, address (or latitude/longitude), and category
  (park, cafe, museum, etc.). Save the spec to docs/specs/feature-spot-crud.md.
```

Once spec is saved, `/clear` then implement:

```
> /clear
> @.claude/agents/developer.md
> Following the spec in docs/specs/feature-spot-crud.md, implement the full-stack feature.
  Implement the CRUD API with SQLite persistence, and build the spot list display,
  registration form, edit, and delete UI. Use category-specific icons to make it visually appealing.
  Write unit tests too.
```

What you're building:
- Spot CRUD API with SQLite persistence
- Spot registration form (name, address, category)
- Spot list (card display)
- Edit and delete functionality
- Unit tests

```
Completion image: Register spot → displays as a card in the list
```

#### Second Cycle: Weather Display

```
> /consult
> I want to display weather forecasts for registered spots.
  Use the Open-Meteo API to fetch weather for spot latitude/longitude.
  Show weather icons, temperature, and precipitation probability in an easy-to-read card.
  Save the spec to docs/specs/feature-weather.md.
```

Once spec is saved, `/clear` then implement:

```
> /clear
> @.claude/agents/developer.md
> Following the spec in docs/specs/feature-weather.md, implement the full-stack feature.
  Implement the module that fetches weather forecasts from Open-Meteo API with caching (about 30 minutes).
  Build the weather forecast card component displaying weather icons, temperature, and precipitation probability.
  Include unit tests with mocked API responses.
```

What you're building:
- Open-Meteo API integration module
- API response caching
- Weather forecast card (weather icons, temperature, precipitation)
- Unit tests

```
Completion image: Select a spot → weather forecast card displays
```

**Recommended: Have system_architect review once here:**

```
> @.claude/agents/system_architect.md
> Review the first and second cycles of implementation.
  Is data flow and component separation appropriate?
  Any issues that might come up adding the remaining 2 features?
```

#### Third Cycle: Weekly Weather Graph

```
> /consult
> I want to visualize a spot's weekly weather as a graph.
  Display temperature trends as a line graph and precipitation probability as a bar chart.
  Save the spec to docs/specs/feature-weather-chart.md.
```

Once spec is saved, `/clear` then implement:

```
> /clear
> @.claude/agents/developer.md
> Following the spec in docs/specs/feature-weather-chart.md, implement it.
  Build the weekly weather graph components using a chart library to make visually appealing graphs
  for temperature trends and precipitation probability.
```

#### Fourth Cycle: Recommended Spots

```
> /consult
> I want to add a feature that suggests "today's recommended spots" based on weather.
  Recommend outdoor spots like parks if it's sunny, and indoor spots like museums and cafes if it's rainy.
  Save the spec to docs/specs/feature-recommend.md.
```

Once spec is saved, `/clear` then implement:

```
> /clear
> @.claude/agents/developer.md
> Following the spec in docs/specs/feature-recommend.md, implement the full-stack feature.
  Implement the recommendation logic with tests, and build the "today's recommended" spot card UI.
  Make the card background color and icons change based on the weather.
```

**Wrapping up after MVP completion:**

```
> @.claude/agents/qa_engineer.md
> Test all features end-to-end. If any areas lack coverage, add tests.
```


---

### Using Sub-agents

In Phase B's development cycle, utilize the agents created in Phase A's Step 6.

#### How to Call Agents

When you type `@` in Claude Code's prompt, file path completion works. Specify the agent file path:

```
> @.claude/agents/developer.md
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
Implementation ← Ask @.claude/agents/developer.md to implement full-stack
  ↓
Testing ← Ask @.claude/agents/qa_engineer.md to create and run tests
  ↓
/commit
```

#### Information Handoff Between Agents

Sub-agents can reference current context (conversation flow). When working with a single developer agent and other agents, this pattern works well:

**Reset session, then call (using /clear)**

```
/consult brainstorms feature → saves to docs/specs/
  ↓
/clear to reset context
  ↓
@.claude/agents/developer.md is called
  → Tell it to "read docs/specs/xxx.md and implement" — share info via files
  ↓
After implementation, /clear again if needed
  ↓
@.claude/agents/qa_engineer.md is called
  → References spec and implementation files
```

- Documentation remains for future reference
- Conserves context
- Info must be saved to file or it disappears

**This pattern is recommended** because:

1. **Reusability**: Implementation results remain in files, referenced from other sessions/agents
2. **Context Savings**: Context margin is crucial for long feature development
3. **Best Practice**: "Always save deliverables" is fundamental to project management where knowledge persists even when sessions disappear
4. **Clear handoff**: Developer agent reads the spec and implements based on documented requirements

#### Example Agent Calls

**developer — Spot CRUD (full-stack)**

```
> @.claude/agents/developer.md
> Following the spec in docs/specs/feature-spot-crud.md,
  implement the full-stack CRUD feature for outing spots.
  Build the API with SQLite persistence and the UI components.
  Write unit tests for both backend and frontend.
```

**developer — Weather display (full-stack)**

```
> @.claude/agents/developer.md
> Following the spec in docs/specs/feature-weather.md,
  implement the full-stack weather feature.
  Build the module that fetches forecasts from Open-Meteo API with caching (about 30 minutes),
  and implement the weather forecast card component.
  Include unit tests with mocked API responses.
```

**system_architect — Design review**

```
> @.claude/agents/system_architect.md
> Review the current implementation from these perspectives:
  - Is the architecture appropriate for adding the remaining features?
  - Is the weather API caching strategy sound?
  - Is the structure set up for future map display?
```

> Getting system_architect to review after 2-3 features are done helps find design issues early.

**qa_engineer — Testing**

```
> @.claude/agents/qa_engineer.md
> Enhance unit tests for spot CRUD and recommendation logic.
  Cover these edge cases:
  - No spots registered
  - Weather API returns an error
  - Spot category is unset
```

#### Agent Usage Tips

| Tip | Explanation |
|------|-----------|
| **Pass specifications** | When you say "follow the spec in docs/specs/xxx.md", agent reads spec then implements |
| **Save investigation results** | Always save research to `docs/research/`. Without saving, next agent can't reference |
| **Focus per agent** | developer handles full-stack implementation; system_architect handles design review; qa_engineer handles testing |
| **Review intermediate results** | Have system_architect review once implementation hits a milestone to maintain quality |
| **Separate testing** | Have developer write tests too, but having qa_engineer write additional edge case tests improves coverage |

---

## What to Keep in Mind Each Cycle

### After /consult

- After Plan Mode planning, **always save specs to `docs/specs/`**
- Be explicit: "Save the spec to docs/specs/feature-weather.md"

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
| Weather API is erroring | Check Open-Meteo status page. If you have cached data, the app works with older data |

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

Example of doing the second cycle (weather display) with the team, starting from where the first cycle (spot CRUD) is done.

#### 1. Instruct the Leader

```
> I want to parallelize the second cycle's "weather display" with the team.
  Based on the spec in docs/specs/feature-weather.md,
  form these teams and proceed in parallel:

  - backend: Open-Meteo API integration + caching
  - frontend: Weather forecast card UI
  - qa: Test creation
```

#### 2. Leader Forms Team and Starts

The leader auto-forms the team and assigns tasks. The following happens **simultaneously before your eyes:**

```
┌─────────────────────────────────────────────────────────┐
│ Leader                                                   │
│ > Forming team. Creating task list...                   │
│ > Launched backend, frontend, qa                        │
└─────────────────────────────────────────────────────────┘
     │
     ├── backend launches
     │   "Implementing Open-Meteo API client...
     │    Creating src/services/weather-api.ts"
     │
     ├── frontend launches
     │   "Implementing weather forecast card...
     │    Creating src/components/WeatherCard.tsx"
     │
     └── qa launches
         "Considering test strategy...
          Inventorying test cases"
```

#### 3. Team Members Communicate

```
backend → Leader:
  "API integration and caching complete.
   Weather data type: WeatherForecast { ... }"

Leader → frontend:
  "Backend API is ready.
   Refer to the WeatherForecast type and finish the UI"

frontend → Leader:
  "Weather card implementation complete.
   Weather icons and responsive design included"

Leader → qa:
  "Backend and frontend implementation complete. Write tests."

qa → Leader:
  "All tests created. 12/12 passing.
   API error fallback covered"
```

#### 4. Leader Integrates and Commits

Once all members complete, leader integrates and commits:

```
Leader:
  "All members complete.
   - API integration + caching ✓
   - Weather card UI ✓
   - Tests 12/12 pass ✓
   Committing now."
```

#### 5. Terminal View

Use `Shift + ↓` to switch between team members and see **in real-time what each is doing**.

```
┌─ Leader ──────────────────────────────────────────┐
│ Task progress:                                    │
│ ✓ backend: API integration complete              │
│ ● frontend: UI implementation... (80%)            │
│ ✓ qa: test creation complete                     │
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
  - backend: Spot CRUD + weather API integration + recommendation logic
  - frontend-spots: Spot management UI
  - frontend-weather: Weather card + weekly graph
  - frontend-recommend: Recommended spots UI
  - qa: tests for each feature (sequential as members complete)

  Once backend finishes, share with frontend members.
  Once all done, qa tests everything, then commit together.
```

**What takes a human team days happens in tens of minutes before your eyes** — this is the impact of agent teams.

### Cautions

| Item | Details |
|------|---------|
| **Token consumption** | Uses context per member. 3-person team ≈ 3 session costs |
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
