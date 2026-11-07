---
description: Run a task through the full Harness protocol (classify → memory → route → execute → verify → memory → DONE)
agent: Apex_Harness
---

Task: $ARGUMENTS

Follow the full Orchestrator protocol: load `harness-core`, classify the
task, apply the memory gate, select the agent and skills, execute via a subagent
with a compact handoff, verify with evidence, and issue a verdict with states
COMPLETED / FAILED / BLOCKED / UNVERIFIED. Record the pipeline in
`.harness/state.md` and close with metrics (`.harness/metrics.jsonl`) and
`mem_session_summary`.
