---
name: codex-review
description: >
  Reviews the current branch against its parent with codex exec review, then triages and
  fixes the findings, looping until the review is clean. Use when finishing a branch or
  before opening a pull request.
disable-model-invocation: true
arguments: [effort]
argument-hint: "[effort] [--model MODEL] [--branch BRANCH]"
metadata:
  author: salmundani
  version: "0.2.0"
---

# Codex Review

Arguments as typed: $ARGUMENTS

run

```sh
codex exec review --base "$PARENT_BRANCH" \
  -m $MODEL \
  -c model_reasoning_effort=$REASONING_EFFORT
```

Where:

- `$PARENT_BRANCH` is the branch on which this branch is based off, unless `--branch BRANCH` was passed, which replaces it.
- `$MODEL` is `gpt-5.6-sol`, unless `--model MODEL` was passed, which replaces it.
- `$REASONING_EFFORT` is `$effort` when that is non-empty and does not start with `--`, otherwise `high`.

For each of the codex findings, determine if it should be fixed or not and do so. Loop until the review comes back clean, or all review items were deferred/rejected. Commit before each iteration.
