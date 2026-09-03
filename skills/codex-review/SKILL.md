---
name: codex-review
description: >
  Reviews the current branch against its parent with codex exec review, then triages and
  fixes the findings, looping until the review is clean. Use when finishing a branch or
  before opening a pull request.
disable-model-invocation: true
metadata:
  author: salmundani
  version: "0.1.0"
---

# Codex Review

run

```sh
codex exec review --base "$PARENT_BRANCH" \
  -m gpt-5.6-sol \
  -c model_reasoning_effort=high
```

Where $PARENT_BRANCH is the branch on which this branch is based off.

For each of the codex findings, determine if it should be fixed or not and do so. Loop until the review comes back clean, or all review items were deferred/rejected. Commit before each iteration.
