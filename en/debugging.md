# How to Debug

[< Back to Guide](../README.en.md)

---

Claude Code can be a powerful debugging partner when you encounter bugs.

## Basic Pattern: Pass the Error and Let Claude Investigate

```
You: I'm getting this error. Find the cause and fix it.

        TypeError: Cannot read properties of undefined (reading 'map')
        at UserList (src/components/UserList.tsx:15:23)

Claude: Let me identify where the error is occurring...

        At src/components/UserList.tsx:15, we're calling users.map(),
        but there are cases where users is undefined.

        Root cause: Rendering happens before the API call in useEffect completes
        Fix: Set an initial value [] for users.

        (Applied fix → Ran tests → ✅ Passed)
```

## Pattern 1: Use Plan Mode to Investigate Root Cause

For complex bugs where the cause isn't immediately clear, it's safer to **investigate in Plan Mode before making fixes**.

```
# Enter Plan Mode with Shift+Tab

You: There's a bug where sessions aren't maintained after login.
     These files seem related:
     - src/auth/session.ts
     - src/middleware/auth.ts
     Find the cause. Don't fix it yet.

Claude: (Reading codebase in read-only mode)
        I've identified the cause. In session.ts, the token refresh logic...

# Once you understand the cause, exit Plan Mode with Shift+Tab to make fixes
```

## Pattern 2: Pass Logs

```bash
# Pipe error logs directly
cat error.log | claude "Analyze this error log and tell me the cause and solution"

# Logs from Docker environment
docker compose logs api-server --tail 50 | claude "Identify the error cause from this log"
```

## Pattern 3: Write a Reproduction Test First

The most reliable way to fix a bug is to **write a reproduction test first**.

```
You: There's a bug where a 500 error is returned when username is empty.
     First, write a test that reproduces this bug.
     Verify the test fails, then fix it.

Claude: Created a reproduction test.
        ❌ 1/1 failed (Bug reproduced)

        Applying fix...
        ✅ 1/1 passed (Fix complete)
```

## Tips for Giving Instructions When Debugging

```
❌ "It's not working"
✅ "Nothing appears on screen. The console shows this error: [error details]"

❌ "It's slow"
✅ "The /api/users response takes over 5 seconds. I think the DB query is the problem"

❌ "It worked before"
✅ "It worked up to commit abc123 last week. Check git log to see
    what changed"
```

Key: **Be specific about symptoms, location, and reproduction steps.**
