---
paths: "**/*.py"
---
# Dev Workflow

## Build + Test
Use uv for venv and dependency management.
Run pytest once per step. Never re-run to "confirm".
Always verify via pytest, not ad-hoc `python3 -c` scripts.

## Linting
Run `pyright` (full project, not just changed files) before committing. Fix all errors.
Subagents create dead code — verify after each task.

## Code Review
Suggest review before committing.
Before executing a plan, move completed/superseded plans to docs/plans/old_already_implemented/.
When a plan claims a module is "unchanged", grep its imports to verify no coupling to changed modules.

## Worktrees
Before starting work in a worktree:
1. `git fetch origin main`
2. Check divergence: `git log --oneline HEAD..origin/main | wc -l`
3. If >0 commits behind, `git merge origin/main` before any edits
4. If >5 commits behind, grep main for the planned change before implementing — another instance may have already done it

## Architecture
Don't propose subpackages or abstractions for codebases under ~2K LOC.
Before splitting a module, verify each resulting file has >50 lines of logic.
Prefer flat packages over nested. Don't build generic iteration for N=2.

## Testing
Tests must not hardcode seed values. Derive expected values from config imports or from the generated output.
