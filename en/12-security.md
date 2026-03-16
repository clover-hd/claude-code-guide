# Security Basics

[< Back to Guide](README.en.md)

---

For company projects, you need at least a basic security awareness.

## Things That Should Never Be Committed

| File | Content | Mitigation |
|---------|------|------|
| `.env` | API keys, DB connection info, secrets | Add to `.gitignore` |
| `credentials.json` | Service account keys | Add to `.gitignore` |
| `*.pem`, `*.key` | SSL certificates, private keys | Add to `.gitignore` |
| `node_modules/` | Dependency packages | Add to `.gitignore` |

**Write rules in CLAUDE.md** and Claude automatically avoids them:

```markdown
# CLAUDE.md (excerpt)

## Security Rules
- Never commit .env files
- Never hardcode API keys or passwords in code
- Retrieve authentication info via environment variables
```

## Information Not to Pass to Claude

Claude Code communicates with AI in the cloud. Do not enter:

- Production database connection info
- Customer personal information (names, email addresses, etc.)
- Production API keys or secrets

> Development dummy data or test environment info is fine.

## .gitignore Template

When starting a new project, include at least this:

```gitignore
# Environment variables and secrets
.env
.env.local
.env.production

# Authentication info
credentials.json
*.pem
*.key
service-account.json

# Dependency packages
node_modules/

# Build artifacts
dist/
build/

# OS and editor
.DS_Store
.vscode/settings.json
```
