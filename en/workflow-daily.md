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
│  2.5. Persistence Save plan to docs/_wip/          │
│       ↓          Make it available next session     │
│                                                     │
│   3. Implementation Code per plan                  │
│       ↓          Build small and verify repeatedly  │
│                                                     │
│  3.5. Testing    Unit tests, E2E tests to verify   │
│       ↓          Claude auto-fixes failures        │
│                                                     │
│   4. Recording   Review, then /commit              │
│       ↓          Record changes in logical units    │
│                                                     │
│   5. Milestone   Overall review, clean up _wip/    │
│                  When a feature set is done         │
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

## Step 2.5: Persistence — Save plan as detailed design

The plan from Plan Mode lives only **within that session**. It disappears when you `/clear` or start a new session. That's why **saving the plan to a file as a detailed design once it's solid is critical**.

### Why persistence matters

```
Session A: Create plan → run out of context mid-implementation
                          ↓
Session B: /clear and restart → "What was that plan again?"

↓ With a detailed design, you have ↓

Session B: Read docs/_wip/profile-image.md → continue per plan
```

Plan Mode plans are session-bound, but **documents persist across sessions**.

### Practical Flow

```
# After planning is solid in Plan Mode, give this instruction:

You: Save this plan to docs/_wip/profile-image-upload.md as a detailed design.
     Include:
     - Feature overview
     - Technical design (API, DB schema, storage)
     - Affected file list
     - Implementation steps

Claude: docs/_wip/profile-image-upload.md created.
```

> **Tip**: Plan Mode is read-only, but document creation happens after exiting Plan Mode. Workflow: confirm plan → Shift+Tab to exit Plan Mode → instruct "save plan to docs" → continue.

### Treat detailed designs as temporary

A detailed design in `docs/_wip/` is **cleaned up once implementation is done** ([Step 5](#step-5-milestone--overall-review-and-cleanup)).

- Anything that counts as requirements, base spec, or the reason for a decision moves to the matching file in `docs/`
- Everything else (table definitions, API details, implementation steps) is deleted. The source code already holds it

> **Why not keep them?**
> If you keep detailed designs around, every code change opens a gap between docs and code. Claude reads the stale doc and implements on stale assumptions. **Treat the source as the source of truth for details, and keep only things that rarely change in docs** — that way docs and code never disagree.

### What to Keep Where

| What | Location | Lifetime |
|------|----------|----------|
| **Requirements & principles to keep** | `docs/requirements.md` | Permanent (update when requirements change) |
| **Base spec (skeleton)** | `docs/spec.md` | Permanent (update when the skeleton changes) |
| **How to lean when in doubt** | `docs/implementation-policy.md` | Permanent |
| **Why we decided** | `docs/decisions/NNNN-short-name.md` | Permanent (never rewrite; supersede with a new file) |
| **Detailed design & implementation plan** | `docs/_wip/<topic>.md` | Until implementation is done |

### Example Docs Directory Structure

```
docs/
├── README.md                        ← Documentation policy (Phase A0)
├── requirements.md                  ← Requirements & principles to keep (Phase A1)
├── spec.md                          ← Base spec (Phase A4)
├── implementation-policy.md         ← Implementation policy (Phase A4.5)
├── decisions/                       ← Why we decided
│   ├── 0001-orm-prisma.md
│   └── 0002-image-storage-s3.md
└── _wip/                            ← Detailed designs in progress
    └── profile-image-upload.md      ← Persisted Plan Mode plan
```

### Coordination with CLAUDE.md

If CLAUDE.md links to each file in docs/, Claude references them during implementation ([How to write CLAUDE.md](project-config.md)). If the developer agent definition also says "when starting implementation, write a detailed design in `docs/_wip/<topic>.md`, and clean it up when done," the same flow applies when implementing through the agent.

### Persist requirements discussed in /consult too

Consult discussions disappear if not saved. Once brainstorming solidifies:

```
You: Reflect the requirements we just settled in docs/requirements.md.
     Record why we decided "no read receipts in the MVP" in docs/decisions/.

Claude: Added chat to the MVP in docs/requirements.md.
        Created docs/decisions/0003-no-read-receipt-in-mvp.md.
        (What was decided, why, rejected options, when to revisit)
```

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
- Test creation → `qa-engineer` agent
- Decisions that touch policy → `advisor` agent (also callable via `/ask-advisor`)

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

### When the developer agent does it

When you implement through the developer agent, the agent itself goes all the way to the commit, following the "pre-commit flow" in its definition file ([Sub-agents](sub-agents.md#rules-for-working-as-a-team)).

```
developer: Pass type checks and tests
    → Ask qa-engineer to test (it runs the tests itself and reports results)
    → git add only the touched files, check with git diff --cached --stat
    → Ask code-reviewer to review the staged diff
    → Commit (the commit guard checks for secrets)
```

If the report just says "tests passed," ask it to **show the tail of the output**.

### When you commit yourself

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

## Step 5: Milestone — Overall review and cleanup

When a set of features is done (or at the end of the day), review the whole. The per-commit code-reviewer only sees diffs, so this is where you check **whether the overall direction has drifted**.

```
You: /ask-advisor milestone review. The previous milestone was abc1234

advisor: Must fix (most severe first)
         1. Image URLs can be fetched without auth (violates a principle to keep in requirements)
         To think about before the next milestone
         - When to delete images is still undecided
         What improved
         - ...
         Forgotten cleanup
         - docs/_wip/profile-image-upload.md
```

After the review, clean up `docs/_wip/`.

```
You: Clean up docs/_wip/profile-image-upload.md.
     Move anything that counts as requirements, base spec, or decision rationale into docs/, and delete the rest.
```

---

## Workflow Application Patterns

### Pattern A: New Feature Development (Full Course)

```
/consult → Plan Mode → save to docs/_wip/ → Implementation → tests & review → commit → milestone review & cleanup
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
