# Installation and Setup

[< Back to Guide](../README.en.md)

---

## Prerequisites

| Item | Requirement |
|------|------|
| **OS** | macOS 13.0+ / Windows 10 1809+ / Ubuntu 20.04+ |
| **Memory** | 4GB or more |
| **Network** | Internet connection required |
| **Account** | A paid plan that includes Claude Code, or a Claude Console account (Free plan not supported. See the [pricing page](https://claude.com/pricing) for eligible plans) |

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

### Windows

On Windows, you can use either **native** (PowerShell / CMD) or **WSL**.

| | Native Windows | WSL 2 |
|--|-----------|------------|
| **Good for** | Working with Windows projects and tools | Using Linux tools. Matching the procedure with macOS team members |
| **Requirements** | None (Git for Windows is optional) | Enable WSL 2 |
| **Shell** | Runs commands in Git Bash if Git for Windows is installed, otherwise PowerShell | Same Bash as macOS/Linux |
| **Sandbox Support** | Not supported | Supported |

The command examples in this guide are written for Bash, so WSL 2 is easier if you want the team to follow the same procedure.

**Native Windows (PowerShell):**

```powershell
irm https://claude.ai/install.ps1 | iex
```

For CMD, run `curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd`. You don't need to run it as administrator.

**WSL:**

```bash
# 1. Install WSL (run PowerShell as Administrator)
wsl --install -d Ubuntu-24.04

# 2. After restarting your PC, Ubuntu will set up automatically
#    Set username and password

# 3. Install Claude Code inside WSL (same command as macOS)
curl -fsSL https://claude.ai/install.sh | bash
```

In either case, once installation finishes, open a new terminal, verify with `claude --version`, then launch with `claude`.

> **About installation methods**: The native installer above is recommended. It updates automatically in the background. You can also install via Homebrew, WinGet, or npm, but Homebrew and WinGet don't auto-update, so you need to update them yourself.

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
