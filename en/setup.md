# Installation and Setup

[< Back to Guide](../README.en.md)

---

## Prerequisites

| Item | Requirement |
|------|------|
| **OS** | macOS 13.0+ / Windows 10 1809+ / Ubuntu 20.04+ |
| **Memory** | 4GB or more |
| **Network** | Internet connection required |
| **Account** | Claude Pro, Max, Teams, or Enterprise (Free plan not supported) |

> For this project, **your company covers the full cost of a Pro license**.

## Installation Steps

### macOS / Linux

```bash
# 1. Install Claude Code (recommended method)
curl -fsSL https://claude.ai/install.sh | bash

# 2. Verify installation
claude --version

# 3. First launch (browser login authentication will open)
claude
```

### Windows (WSL Recommended)

Claude Code internally executes commands via Bash, so **using WSL (Windows Subsystem for Linux) is strongly recommended**. While it works with PowerShell, WSL is significantly more comfortable for these reasons:

| | PowerShell | WSL (Recommended) |
|--|-----------|------------|
| **Command Compatibility** | Linux commands may not work | Same commands as macOS/Linux work natively |
| **Docker Integration** | Works indirectly via Docker Desktop | Natively with WSL 2 + Docker |
| **Team Environments** | Differs from macOS team members | Everyone uses the same Bash environment |
| **Claude Code Stability** | Requires additional config (uses Git Bash internally) | Works out of the box |
| **Sandbox Support** | Not supported | Supported on WSL 2 (improved security) |

```bash
# 1. Install WSL (run PowerShell as Administrator)
wsl --install -d Ubuntu-24.04

# 2. After restarting your PC, Ubuntu will set up automatically
#    Set username and password

# 3. Install Claude Code inside WSL (same command as macOS)
curl -fsSL https://claude.ai/install.sh | bash

# 4. Verify installation
claude --version

# 5. First launch
claude
```

> **npm installation is no longer recommended.** The native installer above is preferred. It also supports automatic updates.

> **Tip**: You can access Windows files from WSL via `/mnt/c/Users/...`, but for performance, it's best to work in the WSL filesystem (like `~/projects/`).

## After First Launch

```bash
# 1. Navigate to your project directory and launch
cd my-project && claude

# 2. Auto-generate CLAUDE.md (for existing projects)
> /init

# 3. Set up the status line (recommended)
#    Display usage rates and remaining context in real-time → See statusline.md for details
curl -fsSL https://raw.githubusercontent.com/clover-hd/claude-code-guide/main/tools/statusline.py -o ~/.claude/statusline.py

# 4. Diagnose installation (if you have issues)
claude doctor
```

## Updates

With native installation, **automatic updates** happen in the background. To manually update:

```bash
claude update
```
