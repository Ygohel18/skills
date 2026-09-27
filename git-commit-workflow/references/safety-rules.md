# Git Safety Rules & Destructive Command Guardrails

> Companion reference for `git-commit-workflow`.
> Contains the strict policy on prohibited commands, safe alternatives, and emergency reflog recovery.

---

## 1. High-Risk / Prohibited Commands

The following commands can destroy uncommitted work or corrupt shared team history. **An AI agent must NEVER execute these commands without explicit, unambiguous user confirmation for that specific invocation:**

| Command | Primary Danger | Safe Alternative |
|---|---|---|
| `git push --force` / `git push -f` | Overwrites remote commits, potentially erasing colleagues' pushed work | Use `--force-with-lease`, and only on private feature branches after user approval |
| `git reset --hard [ref]` | Instantly destroys all uncommitted working directory and staged changes | `git stash push -m "backup"` or create a temporary branch before resetting |
| `git clean -fdx` | Permanently deletes all untracked files, build outputs, and unversioned assets | Run dry-run `git clean -ndx` first so the user can inspect what would be deleted |
| `git rebase -i [shared-upstream]` | Rewrites history already published to teammates or CI | Add a new corrective commit (`git revert` or forward fix) |
| `git branch -D <branch>` | Force-deletes a branch even if it contains unmerged commits | Use `git branch -d` (safe delete); verify merge status before force-deleting |
| `git commit --no-verify` | Bypasses pre-commit linter, security scanners, and test hooks | Fix the underlying lint/format error; never bypass unless user explicitly demands it |
| `git filter-branch` / `git-filter-repo` | Rewrites the entire repository history and alters every commit SHA | Confine changes to current feature commits; consult team before running repo-wide filters |

---

## 2. Push Discipline & Remote Branches

### Protected Branch Policy
- **Never push directly to protected branches** (`main`, `master`, `release/*`, `production`).
- Always create a descriptive topic/feature branch:
  ```bash
  git checkout -b feat/add-payment-webhook
  ```

### Safe Force-Pushing
If rebasing or amending a private, un-merged feature branch, **never use bare `git push --force`**.
Always use `--force-with-lease`:
```bash
git push origin <branch-name> --force-with-lease
```
*Why?* `--force-with-lease` checks if anyone else has pushed commits to the remote branch since your last fetch. If new commits exist, Git refuses the push instead of silently destroying their work.

---

## 3. Hook Verification Policy

Many modern repositories configure pre-commit hooks via **Husky**, **lint-staged**, or `.pre-commit-config.yaml`.
- If a pre-commit hook fails during `git commit`, **do not rerun with `--no-verify` or `-n`**.
- Read the hook output carefully to diagnose the root cause:
  - If a linter failed $\rightarrow$ fix the linting error in the offending file and re-stage.
  - If a formatter modified files $\rightarrow$ stage the formatted diff and retry.
  - If a test failed $\rightarrow$ investigate and repair the broken test case.
- *Only exception:* If the user explicitly instructs: *"bypass the hook with --no-verify"*, confirm the request and log what was skipped.

---

## 4. Emergency Recovery Procedures

If a mistake happens, Git's content-addressable storage usually allows recovery:

### Recovering Lost Commits via Reflog
If a rebase, hard reset, or bad commit dropped changes:
```bash
# 1. View local HEAD change history
git reflog

# 2. Identify the commit hash right before the mistake (e.g., HEAD@{2})
# 3. Create a rescue branch at that point
git branch rescue-branch HEAD@{2}

# 4. Compare rescue branch with current branch
git diff HEAD rescue-branch
```

### Undoing the Most Recent Local Commit (Keeping Changes)
If you made a commit with a typo or missing file, but have NOT pushed:
```bash
# Soft reset: keeps your working directory and staging area intact
git reset --soft HEAD~1
```

### Recovering Accidentally Stashed Changes
```bash
# List all stashes
git stash list

# Inspect what is in the top stash without applying
git stash show -p stash@{0}

# Restore the stash safely
git stash apply stash@{0}
```
