# Your First 30 Minutes: Hands-On Tutorial

[< Back to Guide](../README.en.md)

---

Once installation is complete, let's experience "writing code with AI" through this hands-on tutorial. **Action is better than reading** — jump right in!

## Preparation

```bash
# 1. Create a working directory
mkdir my-first-claude-project && cd my-first-claude-project

# 2. Initialize a git repository (Claude Code works smarter with git)
git init

# 3. Launch Claude Code
claude
```

When you launch, you'll see a prompt like this:

```
╭──────────────────────────────────────╮
│ ✻ Welcome to Claude Code!           │
│                                      │
│ /help for available commands         │
╰──────────────────────────────────────╯

>
```

You're all set.

---

## Step 1: Have a Conversation (1 minute)

Start by talking to Claude about anything.

```
> Please introduce yourself
```

Claude will respond. This shows you can interact with AI right in your terminal.

---

## Step 2: Create a File (3 minutes)

Next, have Claude write some code for you.

```
> Create a simple HTML file.
  It should be a counter app where clicking a button increases the count.
  Make the design modern.
```

Claude will create `index.html`. Claude Code starts in **auto mode** (you'll see `⏵⏵ auto mode on` at the bottom of the screen), so creating the file goes ahead without confirmation. A separate model watches for dangerous operations and blocks them.

> **If you'd rather confirm each step**, press `Shift+Tab` once to switch to manual mode (`⏸ manual mode on`). In manual mode, a confirmation like the following appears before the file is created.
>
> The confirmation lists options corresponding to "Yes (allow)", "don't ask again", and "No (deny)". Review the content and choose `Yes`, and the file will be created. If you choose "don't ask again" for file edits, it only applies for that session. For how to read confirmations, see [Permissions Modes and Approval](overview.md#permissions-modes-and-approval-important).

```bash
# Open it in your browser to verify (in a separate terminal without exiting Claude Code)
open index.html        # macOS
xdg-open index.html    # Linux
explorer.exe index.html # WSL
```

**If a counter app appears in your browser, you've succeeded!**
This is the experience of "code being created from natural language instructions."

---

## Step 3: Request Changes (3 minutes)

Next, ask Claude to modify what was created.

```
> Add the following features to the counter:
  - A reset button
  - Turn the number red if the count goes above 10
  - Support for dark mode
```

Claude will edit the file. Check the browser again. You'll experience "features expanding with just additional instructions."

---

## Step 4: Ask Questions (2 minutes)

Claude can explain code too.

```
> Explain the code in index.html in a way a beginner can understand
```

Even code you didn't write can be understood by asking Claude. This is useful when joining existing projects.

---

## Step 5: Try Something More Complex (10 minutes)

Now you have freedom. Try one of these options:

### Option A: Todo App

```
> Create a Todo app with HTML + CSS + JavaScript.
  Features:
  - Add, delete, and mark tasks as complete
  - Persist data with LocalStorage (tasks stay after reload)
  - Simple and elegant UI
```

### Option B: Rock-Paper-Scissors Game

```
> Create a rock-paper-scissors game you can play in a browser.
  - Select with Rock/Paper/Scissors buttons
  - Computer's choice is random
  - Display win/loss record
  - Add animations to make it fun
```

### Option C: Your Portfolio Page

```
> Create an engineer's portfolio page.
  Name: (your name)
  Skills: Java, Python, etc (your skills)
  Make it responsive and use modern design.
```

---

## Step 6: Try Plan Mode (5 minutes)

Before adding features to your app, use Plan Mode to plan it out.

```
# Send with /plan to enter Plan Mode (you'll see "⏸ plan mode on" at the bottom)

> /plan I want to add a category feature to this Todo app.
  I want to classify tasks by categories like "Work", "Personal", and "Shopping".
  Create an implementation plan.
```

Claude will read the code and present **a plan of what and how to change**. Once satisfied with the plan, approve it from the options shown. Plan Mode ends and implementation starts right away. If you want changes, tell Claude without approving and it will rework the plan.

---

## Step 7: Commit Your Work (2 minutes)

Finally, have Claude commit your changes to git.

```
> Commit the changes to git.
  Write a commit message in English that clearly describes what was created.
```

Claude will stage, create a commit message, and commit everything.

---

## Congratulations!

You've now experienced:

| Experience | What You Learned |
|------|-----------|
| **Conversation** | Claude Code is an AI partner that works in your terminal |
| **File Creation** | Code is born from natural language instructions alone |
| **Change Requests** | New features expand with just additional requests |
| **Code Explanation** | You can understand others' code (and Claude's code) by asking |
| **Plan Mode** | Planning before building improves quality |
| **Commit** | Claude Code handles git operations for you |

**Did you experience a moment of delight?**

Next steps:

- Build something more complex → [Daily Development Workflow - Phase B](workflow-daily.md)
- Switch models → [Model Differences](models.md)
- Set up a proper project foundation → [Setup Workflow - Phase A](workflow-setup.md)
