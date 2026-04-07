# Glossary

[< Back to Guide](../README.en.md)

---

Explanation of terms used in this guide.

## AI & LLM Terms

| Term | Pronunciation | Definition |
|------|--------|------|
| **LLM** | "L-L-M" | Large Language Model. The core technology behind ChatGPT and Claude. Learns from massive text data and generates human-like text |
| **Token** | — | The minimum unit of text that AI processes. Japanese: approximately 1-3 tokens per character; English: approximately 1 token per word. Used for calculating costs and usage |
| **Context Window** | — | The maximum amount of information an AI can remember at once. Conversation history, files read, and command output all accumulate here. Accuracy decreases as it approaches full capacity |
| **Hallucination** | — | When AI generates plausible-sounding content that contradicts facts. Often called "AI lying." Can be prevented by testing and verification |
| **Prompt** | — | Instructions or questions given to AI. "Good at prompting" = "good at giving accurate instructions to AI" |
| **Inference** | "in-fer-ens" | The process of AI receiving a prompt and generating a response. "Inference cost" = the money spent running AI |
| **Fine-tuning** | — | Additional training of an existing AI model for a specific use case. Not used in Claude Code (controlled via prompts) |

## Claude Code Terms

| Term | Pronunciation | Definition |
|------|--------|------|
| **Claude Code** | "Claude Code" | Anthropic's terminal-based AI coding agent. The main subject of this guide |
| **Agent** | — | AI that autonomously performs tasks. Claude Code can decide what to do itself: read files → think → edit → test |
| **Sub-agent** | — | Specialized AI assistants that run within Claude Code. Defined in Markdown in `.claude/agents/` |
| **Skill** | — | Templated instructions invoked with `/skill-name`. Defined in `.claude/skills/<name>/SKILL.md` |
| **CLAUDE.md** | — | Instructions file placed in project root. Claude Code automatically reads it every time. Write project rules, tech stack, and conventions |
| **Plan Mode** | "Plan Mode" | Read-only exploration and design mode. Investigates codebase and makes plans, but doesn't modify files. Toggle with `Shift+Tab` |
| **Auto-Accept** | "Auto-Accept" | Automating file edit approvals. Bash commands still require confirmation. Toggle with `Shift+Tab` |
| **MCP** | "M-C-P" | Model Context Protocol. How Claude Code connects to external tools. "Claude Code's USB-C port" |
| **Hooks** | "Hooks" | Automatically runs shell commands before and after Claude Code executes tools. Example: auto-format after file edit |
| **Context** | — | Accumulated conversation with Claude Code. "Context is full" = no more room for information |
| **/clear** | "Clear" | Command to completely reset context. Use when switching tasks |
| **/compact** | "Compact" | Command to summarize and compress context. Use to extend a session |
| **Checkpoint** | — | Auto-saved restore point created after each Claude Code operation. Can revert to any point with `Esc+Esc` |

## Model Terms

| Term | Pronunciation | Definition |
|------|--------|------|
| **Opus** | "O-pus" | Claude's top-tier model. Best reasoning ability, but higher cost |
| **Sonnet** | "Sahn-ay" | Claude's mid-tier model. With 4.6, achieved near-Opus coding performance. Best value |
| **Haiku** | "Hai-koo" | Claude's lightest model. Fastest and cheapest. Good for simple tasks |
| **SWE-bench** | "S-W-E bench" | Software Engineering benchmark. Measures how well AI can solve real GitHub issues. An indicator of coding ability |

## Development Terms

| Term | Pronunciation | Definition |
|------|--------|------|
| **TDD** | "T-D-D" | Test-Driven Development. Write tests first, then implement to pass them. Works well with Claude Code |
| **E2E Test** | "End-to-End" | End-to-End testing. Replicates real user actions by automating a browser. Uses Playwright, etc. |
| **Playwright** | "Play-right" | Browser automation tool developed by Microsoft. Used for E2E testing. Claude Code can write and run it |
| **CI/CD** | "C-I C-D" | Continuous Integration / Continuous Delivery. Automates code build, testing, and deployment |
| **MVP** | "M-V-P" | Minimum Viable Product. Release with minimal features first, get feedback, then iterate |
| **PoC** | "P-O-C" | Proof of Concept. A prototype to verify if an idea is technically feasible |
| **Conventional Commits** | — | A commit message convention. Uses prefixes like `feat:`, `fix:`, `refactor:` to indicate the type of change |
| **Clean Architecture** | — | A software design pattern. Keeps business logic independent from frameworks and databases |
| **ORM** | "O-R-M" | Object-Relational Mapping. Maps program objects to database tables. Examples: Prisma, TypeORM |
| **WSL** | "W-S-L" | Windows Subsystem for Linux. Runs Linux on Windows. Recommended for Claude Code on Windows |
