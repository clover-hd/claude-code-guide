# Development Workflow Phase B: Daily Development Cycle

[< Back to Guide](../README.en.md) | [< Phase A: Project Initialization](workflow-setup.md)

---

Once the foundation is in place (CLAUDE.md, agents, skills), daily development follows this cycle:

## Overall Flow

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   1. Ideation    /consult to bounce ideas          │
│       ↓          Lock down "what to build"          │
│                                                     │
│   2. Planning    Plan Mode for implementation plan │
│       ↓          Design "how to build it"           │
│                                                     │
│  2.5. Persistence Save plan as spec document       │
│       ↓          Make it available next session     │
│                                                     │
│   3. Implementation Code per plan                  │
│       ↓          Build small and verify repeatedly  │
│                                                     │
│  3.5. Testing    Unit tests, E2E tests to verify   │
│       ↓          Claude auto-fixes failures        │
│                                                     │
│   4. Recording   /commit to save changes           │
│                  Record changes in logical units    │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## Step 1: Ideation — Lock down requirements with `/consult`

Don't jump straight into code. First, **bounce the idea with Claude** to lock down **what to build**.

```
You: /consult
Claude: I'm ready. What would you like to discuss?

You: I want to add a feature for users to upload profile pictures.

Claude: Let me clarify a few things:
        - Image size limits?
        - Need cropping functionality?
        - Save to S3 or local storage?
        - Add to existing profile page or new screen?
```

This is where you organize **feature scope, specifications, and priority**. Jumping into implementation with vague ideas causes mid-project direction changes that waste context.

> You don't need the `/consult` skill to brainstorm directly.
> With the skill, it "reads service specs before responding every time", improving accuracy.

---

## Step 2: Planning — Design with Plan Mode

Once requirements are locked, enter **Plan Mode** to create an implementation plan.

### What is Plan Mode?

Plan Mode is a **read-only exploration and design mode**. You can freely explore the codebase and devise an implementation strategy, but **make no file changes whatsoever**.

```
Can Do                              Can't Do
✅ Read files                        ❌ Create/edit/delete files
✅ Search codebase                   ❌ Run commands (npm, git, etc.)
✅ Get latest info via web search    ❌ Install packages
✅ Parallel investigation via sub-agents ❌ System-level changes
✅ Ask clarifying questions
```

### Plan Mode Operations

| Operation | How |
|-----------|-----|
| **Toggle ON/OFF** | Press `Shift + Tab` |
| **Start in Plan Mode** | `claude --permission-mode plan` |
| **Edit plan in editor** | `Ctrl + G` |

Each `Shift + Tab` toggles the mode:

```
Normal Mode → Auto-Accept Mode → Plan Mode → Normal Mode → ...
             ⏵⏵ accept edits on ⏸ plan mode on
```

### Using Plan Mode (Practical Example)

```
# 1. Press Shift+Tab to enter Plan Mode (screen shows "⏸ plan mode on")

You: I want to implement profile picture upload feature.
     Save to S3, max 5MB, JPEG/PNG support.
     Add to existing profile edit screen.

# 2. Claude explores codebase and creates a plan
Claude: Codebase examined. Implementation plan:

        ## Implementation Plan

        ### Affected Files
        - src/domain/entities/UserProfile.ts (add image URL field)
        - src/infrastructure/storage/S3Client.ts (new)
        - src/usecases/UploadProfileImageUseCase.ts (new)
        - src/interface/routes/profileRoutes.ts (add endpoint)
        - prisma/schema/user.prisma (add column)

        ### Steps
        1. Add profile_image_url column to Prisma schema
        2. Implement S3 upload infrastructure layer
        3. Implement use case (with validation)
        4. Add API endpoint
        5. Create and run tests

        Is this plan okay?

# 3. Review and adjust plan
You: Also add resize processing. Want to resize to 800x800 before upload.

Claude: I'll adjust the plan.
        Add Step 2.5: Image resize with sharp library...

# 4. Approve plan by pressing Shift+Tab to exit Plan Mode
# 5. Claude starts implementation following the plan
```

### Why Plan Mode Matters

| Without Plan | With Plan |
|-------------|-----------|
| Start coding immediately → discover design flaws → redo | Understand full scope first → implement correctly on first try |
| Context wasted | Planning phase is read-only, lightweight |
| "What will change?" unclear | Have file list in advance |
| Motivation drops with rework | Steady progress with plan visible |

---

## Step 2.5: Persistence — Save plan as specification document

The plan from Plan Mode lives only **within that session**. It disappears when you `/clear` or start a new session. That's why **permanently saving the plan as a spec document is critical**.

### Why persistence matters

```
Session A: Create plan → run out of context mid-implementation
                          ↓
Session B: /clear and restart → "What was that plan again?"

↓ With specs, you have ↓

Session B: Read docs/specs/profile-image.md → continue per plan
```

Plan Mode plans are session-bound, but **documents persist across sessions**. If referenced from CLAUDE.md or skills, Claude will always base decisions on those documents.

### Practical Flow

```
# After planning is solid in Plan Mode, give this instruction:

You: Save this plan to docs/specs/profile-image-upload.md as a spec.
     Include:
     - Feature overview
     - Technical specs (API, DB schema, storage design)
     - Affected file list
     - Implementation steps

Claude: docs/specs/profile-image-upload.md created.
```

> **Tip**: Plan Mode is read-only, but document creation happens after exiting Plan Mode. Workflow: confirm plan → Shift+Tab to exit Plan Mode → instruct "save plan to docs" → continue.

### What Documents to Keep

| Document | Example File | Why |
|----------|--------------|-----|
| **Feature Specification** | `docs/specs/feature-name.md` | Anchors "what to build". Capture refined requirements from consult |
| **API Design** | `docs/specs/api/endpoints.md` | Endpoints, request/response formats |
| **DB Schema Design** | `docs/specs/db/schema-changes.md` | Table definitions, migration plan |
| **Architecture Decision** | `docs/architecture-decisions/` | Record "why we chose this tech" |
| **Implementation Plan** | Inside `docs/specs/feature-name.md` | Steps, affected files, notes |

### Example Docs Directory Structure

```
docs/
├── service-overview.md              ← Service vision (Phase A1)
├── architecture.md                  ← Architecture (Phase A4)
├── specs/                           ← Feature specifications
│   ├── user-authentication.md
│   ├── profile-image-upload.md      ← ← Persist Plan Mode planning
│   ├── chat-messaging.md
│   └── api/
│       └── endpoints.md
└── architecture-decisions/          ← Record tech decisions
    ├── 001-why-prisma.md
    └── 002-why-clean-architecture.md
```

### Coordination with CLAUDE.md

If you note spec locations in CLAUDE.md, Claude automatically references them during implementation:

```markdown
# CLAUDE.md (excerpt)

## Reference Documents
- Feature specs: See docs/specs/
- Before implementing, always read the relevant spec
```

Reference specs from the consult skill too to improve brainstorming quality:

```markdown
# .claude/skills/consult/SKILL.md (excerpt)

## Prerequisites
1. docs/service-overview.md - Service overview
2. docs/specs/ - Existing feature specs (understand what's implemented or planned)
```

### Persist requirements discussed in /consult too

Consult discussions disappear if not saved. Once brainstorming solidifies:

```
You: Save this discussion to docs/specs/chat-messaging.md.
     Mark status as "Draft" since it's still being planned.

Claude: Created.

        # Chat Messaging
        **Status: Draft**

        ## Feature Overview
        One-to-one real-time chat between users...
```

Status flows: Draft → designed with Plan Mode → Approved → implemented.

---

## Step 3: Implementation — Code per plan

When you exit Plan Mode, Claude begins implementation following the established plan.

### Implementation Tips

**Progress in small steps, checking along the way**

```
You: Start with Step 1: Prisma schema changes

Claude: (modifies schema → runs migration)
        Done. Ready for next step?

You: Okay, now implement the S3 client

Claude: (creates S3Client.ts → runs tests)
        ...
```

**Stop immediately if heading the wrong direction**

```
You: (Press Escape to interrupt)
     No, I want to use multer instead of that approach
```

**Automatic delegation to sub-agents**

For large tasks, Claude may automatically delegate to sub-agents:
- Feature implementation → `developer` agent
- Test creation → `qa_engineer` agent
- Technical research needed → `tech_researcher` agent

---

## Step 3.5: Testing — Have Claude write and verify tests

After implementation, test before committing. Claude Code can **autonomously create, run, and fix failing tests** from unit tests to browser-driven E2E tests.

### Unit Testing

The most basic test type. Verify functions and modules work correctly.

```
You: Write unit tests for UploadProfileImageUseCase.
     Cover these cases:
     - Normal: JPEG upload succeeds
     - Error: File > 5MB → error
     - Error: Unsupported format (GIF) → error
     Run the tests and show results.

Claude: Tests created. Results:
        ✅ 3/3 passed
```

> **TDD (Test-Driven Development) Recommendation**: Have Claude write tests first without implementing, fail them, then implement to pass. This aligns perfectly with Claude Code—tests become the "correct answer", letting Claude generate accurate implementations while self-verifying.

```
# TDD Flow
You: Write just the tests first. Don't implement yet.
Claude: Tests created. Results: ❌ 3/3 failed (as expected)

You: Now implement to make these tests pass.
Claude: Implementation done. Results: ✅ 3/3 passed
```

### E2E Testing (Playwright)

Using Playwright, **Claude can operate a real browser** and write user-perspective tests:

```
You: Write an E2E test with Playwright for profile picture upload.
     1. Log in from login page
     2. Navigate to profile edit page
     3. Upload image file
     4. Confirm success message appears
     5. Confirm image displays on profile page
     Run the test and show results.

Claude: E2E test created.

        // tests/e2e/profile-image-upload.spec.ts
        import { test, expect } from '@playwright/test';

        test('Can upload profile image', async ({ page }) => {
          await page.goto('/login');
          await page.fill('[data-testid="email"]', 'test@example.com');
          await page.fill('[data-testid="password"]', 'password123');
          await page.click('[data-testid="login-button"]');

          await page.goto('/profile/edit');
          await page.setInputFiles('input[type="file"]', 'tests/fixtures/test-image.jpg');
          await expect(page.locator('.upload-success')).toBeVisible();
          ...
        });

        Results: ✅ 1/1 passed
```

### Claude's Automatic Test Repair Loop

Claude Code's true power is **automatic debugging when tests fail**:

```
Claude: Test results: ❌ 1/1 failed

        Error: Cannot find locator '.upload-success'

        (Checking screenshot...)
        The screen shows a toast notification for upload success,
        but the class is .toast-success. Fixing selector.

        After fix: ✅ 1/1 passed
```

Claude reads Playwright screenshots and accessibility trees, identifies failure causes, and fixes them. This is the concrete benefit of "giving Claude verification tools".

### Complete Testing Strategy

| Test Type | Tools | Coverage | Speed |
|-----------|-------|----------|-------|
| **Unit Tests** | Jest, Vitest | Individual functions/modules | Fast |
| **Integration Tests** | Jest + Supertest | API endpoints | Medium |
| **E2E Tests** | Playwright | Full browser workflows | Slow |

```
         Unit Tests (many, fast, cheap)
        ████████████████████████████████
        Integration Tests (moderate)
        ██████████████████
        E2E Tests (few, slow, expensive)
        ████████
```

You don't need E2E for everything. **Cover core logic with unit tests, save E2E for critical user flows** (login, payments, key features).

### Minimum E2E Coverage

- Login → Logout
- Core feature operations (create, edit, delete)
- Payments and orders (money-related)
- Search and filters (frequently used)

---

## Step 4: Recording — Commit with `/commit`

After implementation and testing are complete, use `/commit` to follow commit rules:

```
You: /commit

Claude: Checking changes...

        Breaking into 2 commits:

        1. feat: Add profile_image_url to Prisma schema
           → prisma/schema/user.prisma

        2. feat: Implement profile picture upload API
           → src/infrastructure/storage/S3Client.ts
           → src/usecases/UploadProfileImageUseCase.ts
           → src/interface/routes/profileRoutes.ts
           → tests/...

        Okay to commit?
```

---

## Workflow Application Patterns

### Pattern A: New Feature Development (Full Course)

```
/consult → Plan Mode → Implementation → /commit
```

The most thorough flow. For building brand-new features from scratch.

### Pattern B: Bug Fixes (From Planning)

```
Plan Mode (investigate) → Implementation (fix) → /commit
```

When you don't know the bug's cause. Use Plan Mode to investigate read-only first, then fix.

### Pattern C: Small Fixes (Direct Implementation)

```
Implementation → /commit
```

For small changes like text fixes or known bugs. No planning needed.

### Pattern D: Technical Research Only

```
Plan Mode (research, then stop)
```

For "Can we use this library?" or "Will this design work?" — investigate without code changes.

---

## Model Selection Per Workflow

How to pick which model for each phase is detailed in [Model Differences and Selection Guide](models.md#workflow-specific-selection-guide). The best practice: **default to Sonnet 4.6, switch to Opus only for deep design decisions like Plan Mode**.
