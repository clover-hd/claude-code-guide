#!/usr/bin/env python3
"""Custom Claude Code status line: repo/branch, rate limits, context remaining.

Data sources:
  - stdin JSON: branch, workspace, session tokens, context window
  - OAuth Usage API: 5h/7d utilization % and reset time
  - Credentials: macOS Keychain or ~/.claude/.credentials.json (WSL/Linux)
"""

import json
import platform
import select
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

CLAUDE_DIR = Path.home() / ".claude"
USAGE_CACHE = CLAUDE_DIR / "statusline-usage-cache.json"
USAGE_CACHE_TTL = 600  # seconds (10 min - API allows ~5 req before 429)


# ── Credential retrieval ──────────────────────────────────────────────


def get_oauth_token():
    try:
        if platform.system() == "Darwin":
            result = subprocess.run(
                ["security", "find-generic-password", "-s", "Claude Code-credentials", "-w"],
                capture_output=True, text=True, timeout=5,
            )
            if result.returncode != 0:
                return None
            creds = json.loads(result.stdout.strip())
        else:
            cred_file = CLAUDE_DIR / ".credentials.json"
            if not cred_file.exists():
                return None
            creds = json.loads(cred_file.read_text())
        return creds.get("claudeAiOauth", {}).get("accessToken")
    except Exception:
        return None


# ── OAuth Usage API ───────────────────────────────────────────────────


def load_cache():
    """Load cache regardless of age. Returns (data, is_fresh)."""
    try:
        if USAGE_CACHE.exists():
            data = json.loads(USAGE_CACHE.read_text())
            is_fresh = time.time() - data.get("_ts", 0) < USAGE_CACHE_TTL
            return data, is_fresh
    except Exception:
        pass
    return None, False


def get_usage_cached():
    cached, is_fresh = load_cache()
    if is_fresh:
        return cached

    # Fetch fresh
    token = get_oauth_token()
    if not token:
        return cached  # return stale cache over nothing

    try:
        req = urllib.request.Request(
            "https://api.anthropic.com/api/oauth/usage",
            headers={
                "Authorization": f"Bearer {token}",
                "anthropic-beta": "oauth-2025-04-20",
                "Accept": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            usage = json.loads(resp.read())
    except Exception:
        return cached  # API error (429 etc) -> use stale cache

    # Save cache
    try:
        usage["_ts"] = time.time()
        USAGE_CACHE.write_text(json.dumps(usage))
    except Exception:
        pass

    return usage


# ── Formatting ────────────────────────────────────────────────────────


# ── ANSI Colors ───────────────────────────────────────────────────────

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"


def color_by_pct(pct):
    """Green < 50%, Yellow 50-80%, Red > 80%."""
    if pct is None:
        return DIM
    if pct >= 80:
        return RED
    if pct >= 50:
        return YELLOW
    return GREEN


def color_by_remaining(pct):
    """Green > 50%, Yellow 20-50%, Red < 20%."""
    if pct is None:
        return DIM
    if pct < 20:
        return RED
    if pct < 50:
        return YELLOW
    return GREEN


def fmt_tokens(n):
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n / 1_000:.0f}K"
    return str(n)


def fmt_remaining(resets_at):
    if not resets_at:
        return ""
    try:
        dt = datetime.fromisoformat(resets_at)
        now = datetime.now(timezone.utc)
        diff = (dt - now).total_seconds()
        if diff <= 0:
            return "soon"
        d = int(diff // 86400)
        h = int((diff % 86400) // 3600)
        m = int((diff % 3600) // 60)
        if d > 0:
            return f"{d}d{h:02d}h"
        if h > 0:
            return f"{h}h{m:02d}m"
        return f"{m}m"
    except Exception:
        return ""


# ── Main ──────────────────────────────────────────────────────────────


def main():
    try:
        _main()
    except Exception as e:
        print(f"err:{e}", file=sys.stderr)
        print("5h:-- | long:-- | ctx:--")


def _main():
    # ── stdin JSON (non-blocking with timeout) ──
    stdin_data = {}
    try:
        if select.select([sys.stdin], [], [], 1.0)[0]:
            raw = sys.stdin.read()
            if raw:
                stdin_data = json.loads(raw)
    except Exception:
        pass

    parts = []

    # ── Repo:branch ──
    try:
        ws = stdin_data.get("workspace") or {}
        if isinstance(ws, dict):
            cwd = ws.get("project_dir") or ws.get("current_dir") or ""
        else:
            cwd = str(ws)
        repo_name = Path(cwd).name if cwd else ""

        # Get branch + ahead/behind via git (stdin doesn't include it)
        branch = ""
        git_status = ""
        ahead = behind = 0
        if cwd:
            result = subprocess.run(
                ["git", "-C", cwd, "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True, text=True, timeout=3,
            )
            if result.returncode == 0:
                branch = result.stdout.strip()

            # Check ahead/behind remote
            result = subprocess.run(
                ["git", "-C", cwd, "rev-list", "--left-right", "--count", f"{branch}...@{{u}}"],
                capture_output=True, text=True, timeout=3,
            )
            if result.returncode == 0:
                ahead, behind = result.stdout.strip().split()
                ahead, behind = int(ahead), int(behind)
                if ahead > 0 and behind > 0:
                    git_status = f"↑{ahead}↓{behind}"  # need push & pull
                elif ahead > 0:
                    git_status = f"↑{ahead}"  # need push
                elif behind > 0:
                    git_status = f"↓{behind}"  # need pull

        if repo_name or branch:
            git_part = repo_name
            if branch:
                git_part = f"{git_part}:{branch}" if git_part else branch
            if git_status:
                git_part = f"{git_part} {YELLOW}{git_status}{RESET}"
            if behind > 0:
                git_part = f"{git_part} {RED}●{RESET}"
            parts.append(f"{BOLD}{CYAN}{git_part}{RESET}")
    except Exception:
        pass

    # ── Model ──
    try:
        model = stdin_data.get("model") or {}
        if isinstance(model, dict):
            model_name = model.get("display_name") or model.get("id") or ""
        else:
            model_name = str(model)
        if model_name:
            parts.append(f"{MAGENTA}{model_name}{RESET}")
    except Exception:
        pass

    # ── OAuth Usage API (rate limits) ──
    def fmt_limit(label, data):
        if not data:
            return f"{label}:{DIM}--{RESET}"
        pct = data.get("utilization")
        if pct is None:
            return f"{label}:{DIM}--{RESET}"
        c = color_by_pct(pct)
        reset = fmt_remaining(data.get("resets_at"))
        reset_str = f" \033[37m{reset}{RESET}" if reset else ""
        return f"{label}:{c}{pct:.0f}%{RESET}{reset_str}"

    try:
        usage = get_usage_cached()
        if usage:
            parts.append(fmt_limit("5h", usage.get("five_hour")))
            # 7d group: only show items with data
            seven_d_items = [
                ("all", usage.get("seven_day")),
                ("opus", usage.get("seven_day_opus")),
                ("sonnet", usage.get("seven_day_sonnet")),
            ]
            seven_d_parts = []
            for label, data in seven_d_items:
                if data and data.get("utilization") is not None:
                    seven_d_parts.append(fmt_limit(label, data))
            if seven_d_parts:
                parts.append(f"7d {' / '.join(seven_d_parts)}")
        else:
            parts.append(f"5h:{DIM}--{RESET}")
            parts.append(f"7d all:{DIM}--{RESET} / opus:{DIM}--{RESET} / sonnet:{DIM}--{RESET}")
    except Exception:
        parts.append(f"5h:{DIM}--{RESET}")
        parts.append(f"7d all:{DIM}--{RESET} / opus:{DIM}--{RESET} / sonnet:{DIM}--{RESET}")

    # ── Context remaining ──
    try:
        ctx = stdin_data.get("context_window") or {}
        remaining = ctx.get("remaining_percentage")
        used = ctx.get("used_percentage")
        if remaining is not None:
            ctx_remaining = remaining
        elif used is not None:
            ctx_remaining = 100.0 - used
        else:
            ctx_remaining = None

        if ctx_remaining is not None:
            c = color_by_remaining(ctx_remaining)
            parts.append(f"ctx:{c}{ctx_remaining:.0f}%{RESET}")
        else:
            parts.append(f"ctx:{DIM}--{RESET}")
    except Exception:
        parts.append(f"ctx:{DIM}--{RESET}")

    print(" | ".join(parts))


if __name__ == "__main__":
    main()
