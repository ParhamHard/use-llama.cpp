# AI Agent Reference Guide

## Git and GitHub Operations

### Removing Old Commits from GitHub

There are several methods to remove old commits from GitHub, depending on your specific needs:

#### Method 1: Interactive Rebase (Recommended for few commits)
- **Best for**: Few commits, clean history
- **Command**: `git rebase -i --root` (for all commits) or `git rebase -i HEAD~n` (for last n commits)
- **Use case**: When you want to pick, edit, squash, or drop specific commits
- **Example**: `git rebase -i --root` then edit the file to drop unwanted commits

#### Method 2: Reset and Force Push
```bash
# Reset to a specific commit
git reset --hard <commit-hash>

# Force push to overwrite GitHub history (use --force-with-lease for safety)
git push --force-with-lease origin master
```

#### Method 3: Filter Branch (For complex history rewriting)
```bash
git filter-branch --index-filter 'git rm --cached --ignore-unmatch <file>' --prune-empty --tag-name-filter cat -- --all
```

#### Method 4: BFG Repo Cleaner (For large repositories)
```bash
# Install BFG first
java -jar bfg.jar --delete-files <filename> <repo>
```

### Important Notes:
- **Force pushing rewrites history** - use with caution
- **--force-with-lease** is safer than --force as it prevents overwriting others' work
- **Interactive rebase** is the cleanest method for small repositories
- **Always backup** your repository before major history changes
- **Communicate with team members** if working on shared repositories

### Current Repository Status:
- Repository: use-llama.cpp
- Remotes: GitHub and Gitea
- Current branch: master
- Recent commits: 3 commits (including initial commit and project rename)

### Common Use Cases:
1. **Remove sensitive information** from commit history
2. **Clean up messy commit history** before sharing
3. **Remove large files** that were accidentally committed
4. **Squash multiple commits** into one clean commit
5. **Remove commits** that contain bugs or incorrect information

### Safety Commands:
```bash
# Check current status
git status

# View commit history
git log --oneline

# Check remote status
git remote -v

# Backup current state
git branch backup-before-cleanup
```
