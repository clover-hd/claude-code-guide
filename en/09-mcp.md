# MCP Servers

[< Back to Guide](README.en.md)

---

## What is MCP?

**MCP (Model Context Protocol)** is a mechanism to connect external tools and services to Claude Code. It's like "Claude Code's USB-C port" where you can plug in various tools.

## How to Set Up

Define in `.mcp.json` in the project root or Claude Code's configuration file.

## Example: MCP Server Configuration

An example configuration using **3 MCP servers** in an actual project.

### 1. Sequential Thinking (Structured reasoning)

```
Purpose: Analyze and reason through complex problems step by step
Scenarios: Architecture design, impact analysis, decision-making
```

When complex design decisions are needed, Sequential Thinking is a thinking tool for Claude to "organize first, then think."

### 2. Serena (Code intelligence)

```
Purpose: Symbol-based code analysis and navigation
Features: Symbol search, pattern search, project memory
Scenarios: Understanding large codebase structure, tracing function definitions
```

By integrating with TypeScript's LSP (Language Server Protocol), Serena provides Claude Code with precise code analysis like an IDE.

### 3. Context7 (Library documentation)

```
Purpose: Retrieve latest documentation for npm libraries
Features: Library ID resolution, documentation retrieval
Scenarios: Questions like "What's the latest Prisma migration method?"
```

Context7 supplements library information not in Claude's training data.

## MCP Usage Examples

```
You: "I want to implement a Stripe payment flow"

Claude Code does:
  1. Context7 → Get latest Stripe SDK documentation
  2. Serena → Identify related files in the existing codebase
  3. Sequential Thinking → Organize implementation approach step by step
  4. Begin implementation
```

## Commonly used MCP servers

| MCP Server | Purpose |
|------------|------|
| **sequential-thinking** | Structured thinking for complex problems |
| **serena** | Deep analysis of codebase |
| **context7** | Retrieve library documentation |
| **filesystem** | File system operations |
| **github** | GitHub API integration |
| **postgres / mysql** | Direct database operations |
