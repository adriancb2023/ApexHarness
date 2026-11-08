---
name: harness-core
description: Core of the Engineering Harness — task classification tables, skill and agent routing, Engram memory rules, state machine, handoffs, verification, and Definition of Done. Load it at the start of any task and apply its tables without re-deciding.
---

# Harness Core

Source of truth for the pipeline. If a decision is here, apply it as written and
note only the why in one line. Full metadata for each skill (triggers,
requires, produces, verification, when NOT to load it): `references/registry.md`,
only when you are unsure about a specific skill.

Token rules: this document is the whole orientation budget (~2k
tokens); do not print it again in the chat; cite sections by §.

## 1. Task classification (deterministic)

Scan the task text with the table; the first match wins.

| Triggers | Agent / pipeline |
| --- | --- |
| The user names an agent (`apex-dev`, `apex-bug`, `apex-verifier`, `apex-api-auditor`, `apex-frontend-auditor`, `apex-sql-auditor`, `apex-worker-auditor`, `apex-memory-fixer`, `apex-injection-auditor`, `apex-auth-auditor`, `apex-sec-api-auditor`, `apex-secrets-auditor`, `apex-hacker`, `apex-security-fixer`, or the equivalent `Apex_*` id) | **That agent, directly.** Do not classify, do not query Engram, do not write `.harness/state.md`, do not run the skill router, do not verify. The user's message is the assignment. `/harness` or "run the harness" / "haz el harness" does not match this row: follow the pipeline |
| `bug`, `error`, `crash`, `exception`, `fails`, `broken`, `regression`, "no funciona", "falla", "se queda", "no carga", "rompe", "petazo", "stack trace", "se cuelga", "doesn't work", "hangs", "won't load" | **BUG** (subagent Apex_Bug) |
| `implement`, `add`, `create`, `build`, `feature`, `develop`, `refactor`, `migrate`, "añade", "agrega", "implementa", "crea", "nueva versión de", "soporte para" | **DEV** (subagent Apex_Dev) |
| Analysis, explanation, exploration, questions, plans, review of one specific point | **Direct answer** from the Orchestrator, no spawn |

Ambiguous → reason the why in one line and choose; still unsure → standard pipeline
(§2). If the table did not settle it and you used the model to decide, note it in state.md.

Non-code tasks (docs, harness config, meta-tasks of this repo) are
treated as DEV or Answer according to their shape. If the task touches the harness itself, remember:
the Orchestrator may edit only `.harness/**`; changes to every other file
are executed by Apex_Dev (the agent with real edit permission).

## 2. Complexity → pipeline variant

| Level | Signal | Pipeline |
| --- | --- | --- |
| Trivial | ≤1 file, ≤~30 LOC, no new interface and no new domain | memory (gate) → Apex_Dev → light verify (implementer's output) → memory-write → DONE |
| Standard | 2–4 files or tests affected | classify → memory → route → Apex_Dev (+`tdd`) → `code-review` → Apex_Verifier → memory-write → DONE |
| Complex | new domain, new interface, multi-system, large uncertainty | research (if there is factual uncertainty) → grill-with-docs → to-spec → to-tickets → implement-spec per ticket → tdd → code-review → Apex_Verifier → retro (optional) → memory-write → DONE |

Each optional step (research, grill, spec, tickets, retro) is included only when it
adds value: when you skip it, one line says why. The typical count is 2–4 skills
per task; a higher number needs an explicit justification.

## 3. Memory Router (Engram)

**Gate (before searching, cost 0):** could the task repeat prior work,
inherit a decision, or touch a bug or convention already known? No → zero searches;
note "memory skip: gate does not apply". Yes → chain:

1. `mem_context` — cheap, once.
2. `mem_search` — topic/file keywords (max 2 searches; project scope
   by default: other projects are excluded automatically).
3. `mem_get_observation` — only for the 1–2 results you will inject.

**Cap:** ≤5 relevant observations in context. Drop observations that are
trivial, from another area, or unrelated to the task.

| Memory type | Rule |
| --- | --- |
| decision / architecture | Applies to the task → inject. If it contradicts the code: investigate; git/code wins; do not change it silently |
| bugfix | Similar area → inject cause+fix. Otherwise → drop |
| pattern / config | Inject if it touches the area |
| Progress | A starting point; git/code wins if they differ |
| `learning` titled `[HYPOTHESIS]` | Never as fact; use it only to mark uncertainty |

**Contradictions:** tests/evidence > current code > Engram > the agent's
assumptions. If Engram differs from the code: investigate and resolve, then record the
verdict (§9). Never adopt a memory without checking it against the current code.

## 4. Minimum context

Never the whole repo. Order: relevant memory → files/symbols involved
(directed read / grep) → nearby tests → implementation. If 3 files
answer it, do not read 10. Skills and context outside the task are not loaded.

## 5. Skill Router

Rule: `does this skill add value to THIS task?` no → do not load it (note it).
Per-skill details: `references/registry.md`.

| Need | Skill | Load if | Skip if |
| --- | --- | --- | --- |
| Bug | `diagnosing-bugs` | ALWAYS on the BUG pipeline | — |
| Implement | `tdd` | a testable slice is possible | there is no runtime/tests, or it is docs/config |
| Handoff with spec/ticket | `implement-spec` | the pipeline comes from to-spec/to-tickets | the spec is informal |
| Large change | `code-review` | >1 file or a complete feature | a ≤30 LOC change already covered by verify |
| Interface/architecture | `codebase-design` | it changes a module's shape or interface | a touch-up only |
| Domain concepts | `domain-modeling` | new or ambiguous concepts | the domain is known and stable |
| Factual uncertainty | `research` | an unknown technology/dependency/API BLOCKS the task | the fact is in local code or docs |
| Complex and ambiguous | `grill-with-docs` | the pipeline is complex | trivial/standard |
| Complex multi-step | `to-spec` → `to-tickets` | it will be implemented as several tickets | tickets do not fit |
| Close of a complex task | `retro` | a relevant process lesson | standard/trivial |

Note: `implement`, `to-spec`, `to-tickets`, `retro`, `triage`, `wayfinder`,
`grill-with-docs` are user-invoked (`disable-model-invocation: true`): they are NOT
advertised; call them by exact ID with the `skill` tool when routing selects
them. The model-invoked ones (`tdd`, `code-review`, `diagnosing-bugs`, `research`,
`codebase-design`, `domain-modeling`, `prototype`, `pr`) advertise themselves, but the
decision to load them is just as explicit.

## 6. State machine and artifacts

States: `RECEIVED CLASSIFYING MEMORY_LOOKUP PLANNING RESEARCHING IMPLEMENTING
DIAGNOSING VERIFYING REVIEWING REPAIRING COMPLETED FAILED BLOCKED UNVERIFIED`.

`.harness/state.md` (≤40 lines; the Orchestrator updates it on every transition):

```markdown
# Harness state — 2026-10-25 hh:mm
task: <1 line>
pipeline: dev | bug | answer
state: VERIFYING (prev: IMPLEMENTING)
selected: agent=Apex_Dev skills=[tdd, code-review] dropped=[research (local fact), grill (standard)]
memory: gate=hit ids=[12, 34] injected=2 est_tokens=~600
transitions:
| hh:mm | IMPLEMENTING → VERIFYING | implementation finished | evidence goes to Apex_Verifier |
...
```

Every transition has from → to, reason, evidence, and (if available) tokens.
Subagents do not write state.md; the Orchestrator is the only writer.

## 7. Verification and cache

1. Evidence: for each check, the command that was run + output (summary). Never an assertion.
2. Non-trivial verification is independent: the Apex_Verifier subagent does it
   (read-only by permissions). Trivial: the implementer's output with commands
   attached, reviewed by the Orchestrator.
3. Typical checks: area tests, full suite, typecheck, lint, build,
   bug reproduction, `git diff`/`git log` (if git exists; if not: UNVERIFIED for
   that specific check, not for the task).
4. Cache (`.harness/cache.md`): `| check | command | inputs (files+hash/mtime) |
   result | ts |`. A test that already passed with no code changes → do not repeat it.
   Any edit of the inputs → the check is invalidated.

FAIL → REPAIRING (max 2 cycles; handoff with evidence of what is wrong) → re-verify ONLY
what was invalidated. Past the limit: UNVERIFIED or BLOCKED with what was learned recorded.

## 8. Handoff between agents (compact; never the whole conversation)

```markdown
from: Apex_Harness | to: Apex_Dev | type: implement-request | 2026-10-25
goal: <1–2 lines>
context: <files, symbols, criteria; no dumps>
memory: [#12 decision X, #34 bug Y with its fix]  (required lines)
criteria: <what Apex_Verifier must demonstrate>
relevantMemoryIds: [12, 34]
```

Variants: `repair-request` (with rootCause/evidence for Apex_Dev) and `verify-request`
(for Apex_Verifier, with the check list). If a result comes back insufficient, the
next handoff includes only the delta that is needed.

## 9. Memory Writer (only on close; only writer: Orchestrator)

```
Is there reusable knowledge? NO → do not save (silence is valid)
YES → does similar memory on the topic exist? YES → mem_save with the same topic_key (upsert) / mem_update with id
                                          NO → new mem_save
```

**Save:** decisions and their why; established architecture; root cause of bugs
(what it was, the fix, the test, how to reproduce in one line); conventions; config/environment;
a progress milestone (1 observation per row); a reference to key files.

**Do not save:** logs, full diffs, full code, conversations, trivial
steps, internal thoughts, every command that was run.

Native format: a short searchable `title`; topical `type` (decision / architecture /
bugfix / pattern / config / discovery / learning); `content` with
**What / Why / Where / Learned**; a stable `topic_key` (if unsure:
`mem_suggest_topic_key`). A pending hypothesis → title prefixed with `[HYPOTHESIS]`.

Post-save: if the response brings `judgment_required`, iterate `candidates[]` and call
`mem_judge` with the `judgment_id` of EACH candidate. `supersedes`/`conflicts_with`
on decision/architecture/policy → ask the user first; the rest is
resolved silently. Never duplicate memory: before creating, search the topic; the
default criterion is upsert.

Session close: `mem_session_summary` (Goal / Instructions / Discoveries /
Accomplished / Next Steps / Relevant Files — the Engram plugin format).

## 10. Metrics (`.harness/metrics.jsonl`)

One JSON line per task on close:

```json
{"ts":"2026-10-25T10:34:31","task":"...","pipeline":"dev","agents":["Apex_Dev","Apex_Verifier"],
 "skillsUsed":["tdd","code-review"],"skillsSkipped":["research (local fact)"],
 "memoryQueries":1,"memoryResults":2,"contextFiles":3,"verification":{"checks":3,"pass":3},
 "retryCount":0,"finalState":"COMPLETED","tokensTui":null}
```

`tokensTui`: the real number from the TUI token panel (the Orchestrator notes it
if it is at hand; `null` if not). To answer "does Engram save tokens?":
run the same task twice (once with a memory lookup, once marking
"memory skip") in clean sessions and compare tokens/steps/retries of both lines
in the JSONL. Full protocol: `docs/METRICS.md`.

## 11. Anti-patterns (abort if you catch yourself)

1. Giant prompt: every skill + the whole repo + all of Engram at once.
2. Rigid pipeline: running research/grill/spec/tickets when the task is trivial.
3. `mem_search` "just in case" with no gate.
4. PASS from the implementer's assertion with no command executed.
5. Rewriting or re-checking work that was already verified when nothing changed.
6. One agent that does everything (plans, codes, diagnoses, reviews) — use the roles.

## 12. Isolation and install: only one harness is in charge

In any repo with this harness installed, the only active pipeline is
`Apex_*`. Install in **two steps**:

### Step 1 — harness (config-only; copy by hand or clone)

| Piece | Destination (default: project) | Conflict with a previous harness/agents |
| --- | --- | --- |
| `Apex_*.md` files | `<repo>/.opencode/agents/` | `Apex_*` IDs do not clash with foreign agents: they coexist and do not invoke each other. If the repo already had `harness.md`/`dev.md`/`bug.md`/`verifier.md` with NO prefix (another harness), disable them: delete/rename those files or add `disable: true` for each in `opencode.json` (`"agent": {"harness": {"disable": true}, ...}`) |
| `harness-core` | `<repo>/.opencode/skills/harness-core/` | Skill IDs must be unique across locations: if `harness-core` already exists in `~/.config/opencode/skills/` (an old version), delete the global one |
| `/harness` command | `<repo>/.opencode/commands/harness.md` | If another command with that ID existed, this replaces it (same path) |
| `opencode.json` | `<repo>/opencode.json` — MERGE, do not replace | Add `default_agent: "Apex_Harness"`, hard-deny `policies[]`, and ask on `git clean -d*`; keep the rest of the repo |
| rules | If the repo already has `AGENTS.md`: append a `## Harness (Apex_)` block at the end (do not replace it). Alternative without touching AGENTS.md: in `opencode.json`, `instructions: [".opencode/skills/harness-core/SKILL.md"]` |
| Cursor | `<repo>/.cursor/` (rules `apex-*`, commands/harness, skills/harness-core shim, mcp.json) | One always-apply pair for the harness; delete rules from a previous harness. Detail: `docs/CURSOR.md` |

### Step 2 — Skills for Real Engineers (required; they do NOT live in this repo)

```bash
npx skills@latest add mattpocock/skills -a opencode -a cursor -y --copy
# without git (copy from ~/.config/opencode/skills):
pwsh ./scripts/bootstrap-matt-skills.ps1 -FromOpenCodeGlobal
```

Installs the ~27 skills (`tdd`, `code-review`, `diagnosing-bugs`, …) into the
**project**: `<repo>/.opencode/skills/` and `<repo>/.cursor/skills/` (a global
copy may also remain in `~/.config/opencode/skills/`). Without this step the §5
router points at IDs that do not exist. Requires `git` for the official installer. Do not
version Matt skills in git (see `.gitignore`; only `harness-core` is versioned).


Hard guarantees (enforced by the HOST, not by prompts):

1. Hard-deny `policies[]` apply at every layer; no config or agent
   ranking can bypass them (docs: OpenCode 2).
2. Apex_Harness `subagent`: deny `*` → allow `Apex_Dev` / `Apex_Bug` /
   `Apex_Verifier`, the memory squad (`Apex_ApiAuditor`, `Apex_FrontendAuditor`,
   `Apex_SqlAuditor`, `Apex_WorkerAuditor`, `Apex_MemoryFixer`), and the security
   squad (`Apex_InjectionAuditor`, `Apex_AuthAuditor`, `Apex_SecApiAuditor`,
   `Apex_SecretsAuditor`, `Apex_Hacker`, `Apex_SecurityFixer`). With `deny`, other agents
   (for example a global `apex`, `build`, `general`) **disappear from the Orchestrator's
   spawn catalog**: there is no escape hatch for another harness to enter the pipeline.
3. A project-level `default_agent` overrides the global → the session ALWAYS opens as
   Apex_Harness even if the global says otherwise; and if the global does not exist, the
   project sets it.
4. Namespaced names (`Apex_*`, `harness-core`, `/harness`) → no accidental
   collision with Matt Pocock skills or third-party agents.

Global install (every repo): the same content in `~/.config/opencode/`
(agents/skills/commands) and `default_agent` + `policies[]` in the global config.
A project that defines its own `default_agent` overrides the global (a conscious
decision; our config is still respected on the other keys). The 27 Matt skills are
the shared FLOOR (step 2; they are not duplicated inside the namespaced
harness). Cursor: `docs/CURSOR.md`.
