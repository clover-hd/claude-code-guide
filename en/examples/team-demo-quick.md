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
# Weather Forecast Display

## Overview
Fetch weather forecasts from Open-Meteo API for registered outing spots and display them as visually appealing cards.

## Input
- Latitude/longitude of registered spots (from SQLite)

## Output
- Weather cards with weather icon, temperature, and precipitation probability
- Current weather and 24-hour forecast per spot

## Technical constraints (Important)
- Use Open-Meteo API (https://api.open-meteo.com/) for weather data
- No API key required (uses Open-Meteo free tier)
- Cache API responses for ~30 minutes (prevent excessive requests)
- Spot data is retrieved from SQLite (implemented in cycle 1)

## API Endpoint
Backend calls:
  https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m,precipitation_probability

## Work Division
- Backend: Open-Meteo API integration + response cache
- Frontend: Weather card UI
- Testing: Unit tests using mocked API responses
```

Save this as `docs/specs/feature-weather.md`.

---

## Demo Time (10 minutes)

### Step 1: Say This First

> "I'm now going to **have Claude Code form a team**. A leader, backend developer, frontend developer, and test engineer AI will **work simultaneously on one PC, communicating with each other as they develop**. Watch as the same teamwork humans do unfolds."

### Step 2: Instruct the Team

```
> Based on the spec in docs/specs/feature-weather.md,
  develop it with the team in parallel. Must follow the spec's "technical constraints".

  Team:
  - backend: Open-Meteo API integration + response cache
  - frontend: Weather card UI (weather icon, temperature, precipitation)
  - qa: Unit tests with mocked API responses

  Once backend is done, share type definitions with frontend.
  When everyone's done, run tests and report results.
```

### Step 3: Explain as You Watch

As the team works, use `Shift + ↓` to switch between members and explain.

**What to highlight:**

```
① Team formation moment
  "Leader just created the task list and launched 3 members"

② Working in parallel
  "Shift+↓ to switch. See? Backend's writing the API integration while
   frontend's building the card UI. Simultaneous."

③ Member communication
  "Backend finished, leader shared type definitions with frontend.
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

Open browser, select a spot, and if the weather forecast card displays, perfect.

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
