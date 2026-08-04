---
name: resolving-merge-conflicts
description: "Use when you need to resolve an in-progress git merge/rebase conflict."
---

1. **See the current state** of the merge/rebase. Check git history, and the conflicting files.

2. **Find the primary sources** for each conflict. Understand deeply why each change was made, and what the original intent was. Read the commit messages, check the PRs, check original issues/tickets.

3. **Resolve each hunk.** Preserve both intents where possible. Where incompatible, pick the one matching the merge's
   stated goal and note the trade-off. Do **not** invent new behaviour. If intent cannot be established safely, stop
   and ask the user; do not abort, continue, stage, or commit without authorization.

4. Discover the project's **automated checks** and run them — typically typecheck, then tests, then format. Fix anything the merge broke.

5. **Finish only when requested.** Report the resolved files and verification results. Stage files, continue a rebase,
   or create a commit only when the user's request authorizes that action.
