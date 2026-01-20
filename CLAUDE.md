# claudecode-sounds

Play sounds when Claude Code needs your attention.

## Shipping the Plugin

When releasing a new version, update both repos:

### 1. Plugin repo (this repo)

Update version in `.claude-plugin/plugin.json`:
```json
"version": "X.Y.Z"
```

Commit and push:
```bash
git add -A && git commit -m "Release vX.Y.Z" && git push
```

### 2. Marketplace repo

Located at `../codingagents`

Update version in `.claude-plugin/marketplace.json` under the `claudecode-sounds` plugin entry:
```json
"version": "X.Y.Z"
```

Commit and push:
```bash
cd ../codingagents
git add -A && git commit -m "Update claudecode-sounds to vX.Y.Z" && git push
```

### Version files to update

| File | Path |
|------|------|
| Plugin manifest | `.claude-plugin/plugin.json` |
| Marketplace | `../codingagents/.claude-plugin/marketplace.json` |
