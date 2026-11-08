# Skill Registry — harness metadata

Real verification base: Matt skills installed **outside version control** by the
official installer
`npx skills@latest add mattpocock/skills -a opencode -a cursor -y --copy`
(`engineering/` set 20 + `productivity/` 7). Project destinations:
`<repo>/.opencode/skills/<id>/` and `<repo>/.cursor/skills/<id>/` (gitignored;
`harness-core` is versioned). Fallback: `scripts/bootstrap-matt-skills.ps1`.
Without that step 2, harness-core §5 routing has nothing to load.

Conventions:
- **user-invoked** (`disable-model-invocation: true`): the model does NOT see it advertised;
  it must be loaded by exact ID with the `skill` tool.
- **model-invoked**: it advertises itself; the decision to load it is still explicit.
- `requires/issues`: the skill assumes an issue tracker configured by
  `setup-matt-pocock-skills` (GitHub/GitLab/local). Without git, use the local variant.

## 1. Flow — implementation (user-invoked)

```yaml
implement:
  type: user-invoked
  agents: [Apex_Dev]
  purpose: implement the work of a spec or a set of tickets
  triggers: [handoff with spec, registered ticket, tracer bullet]
  requires: [spec or tickets, relevant-code-context]
  produces: [code-change, commit]
  verification: [typecheck, tests per module, suite at the end, code-review]
  notes: calls tdd on the agreed seams and code-review at the end
implement-spec:
  type: user-invoked
  agents: [Apex_Dev]
  purpose: implement the output of to-spec + to-tickets
  triggers: [new spec, ticket block ready]
  requires: [published spec, relevant-code-context]
  produces: [code-change]
  verification: [tests, code-review, diff]
```

## 2. Flow — planning (user-invoked)

```yaml
grill-with-docs:
  type: user-invoked
  agents: [Apex_Harness]
  purpose: an interview that sharpens a plan and leaves ADRs + a glossary as a side effect
  triggers: [complex/ambiguous task, new design, alignment with the domain]
  requires: [user available to answer]
  produces: [sharpened plan, ADRs, GLOSSARY.md]
  verification: [answers recorded, docs written]
grill-me:
  type: user-invoked
  agents: [Apex_Harness]
  purpose: a sharpening interview with no docs
  load-when: complex but the domain is already modeled
to-spec:
  type: user-invoked
  agents: [Apex_Harness]
  purpose: synthesize the current conversation into a published spec
  triggers: [approved complex pipeline, stable plan]
  produces: [published spec]
  verification: [spec reviewed by the user]
  requires/issues: tracker configured
to-tickets:
  type: user-invoked
  agents: [Apex_Harness]
  purpose: split a plan/spec into tracer-bullet tickets with blocking edges
  produces: [tickets with dependencies]
  verification: [blocking graph with no cycles]
  requires/issues: tracker configured (or the local variant)
retro:
  type: user-invoked
  agents: [Apex_Harness]
  purpose: retrospective of a coding session
  load-when: close of a complex pipeline or a user request
triage:
  type: user-invoked
  agents: [Apex_Harness]
  purpose: move external issues/PRs through a triage state machine with agent-ready briefs
  load-when: the user asks for triage/issues, not as an internal step of a task
  requires/issues: tracker configured
wayfinder:
  type: user-invoked
  agents: [Apex_Harness]
  purpose: a huge work plan as a map of decision tickets, resolved one at a time
  load-when: the work does not fit in one session
  requires/issues: tracker configured
improve-codebase-architecture:
  type: user-invoked
  agents: [Apex_Harness]
  purpose: scan deepening opportunities reported in HTML + grill the one that is chosen
  load-when: an explicit request for an architectural improvement
setup-matt-pocock-skills:
  type: user-invoked
  agents: [Apex_Harness]
  purpose: configure the tracker, labels, and docs layout of the repo; run once
  load-when: first use of the tracker skills in a new repo
```

## 3. Model-invoked — discipline

```yaml
tdd:
  type: model-invoked
  agents: [Apex_Dev, Apex_Bug]
  purpose: red-green-refactor by vertical slices on the seams
  triggers: [feature, fix, change with a testable slice]
  requires: [the repo's test framework, relevant-code-context]
  produces: [failing test → green, code-change]
  verification: [test suite, the test covers the new behavior]
diagnosing-bugs:
  type: model-invoked
  agents: [bug]
  purpose: diagnosis loop for hard bugs and performance regressions
  triggers: [bug, error, crash, regression, "no funciona", unexplained slowness]
  requires: [reproduction]
  produces: [root-cause with evidence, minimal fix]
  verification: [repro before, repro after, regression test]
  notes: ALWAYS on the BUG pipeline; no fix without a confirmed cause
code-review:
  type: model-invoked
  agents: [Apex_Dev, Apex_Bug, Apex_Harness]
  purpose: a 2-axis review — Standards (repo) and Spec (originating issue) in parallel subagents
  triggers: [before commit/PR, diff after implement]
  requires: [a fixed point (commit/branch/tag) or a diff]
  produces: [findings by severity with file:line]
  verification: [findings are closed before moving to COMPLETED]
  skip-when: a ≤30 LOC change already covered by direct verification
research:
  type: model-invoked
  agents: [Apex_Harness, Apex_Dev, Apex_Bug]
  purpose: investigate against trusted primary sources and write findings in the repo
  triggers: [unknown technology/dependency/API, a missing fact that BLOCKS]
  requires: [a bounded question]
  produces: [markdown findings]
  verification: [sources cited; no sources, no conclusion]
  skip-when: the fact is in code, local docs, or validated Engram
codebase-design:
  type: model-invoked
  agents: [Apex_Dev, Apex_Harness]
  purpose: deep-module vocabulary — small interfaces, seams, testability
  triggers: [a change that alters a module's shape or interface]
  produces: [module design, seam decisions]
domain-modeling:
  type: model-invoked
  agents: [Apex_Dev, Apex_Harness]
  purpose: build or sharpen the domain model — GLOSSARY.md and ADRs
  triggers: [new or ambiguous concepts, recording domain decisions]
  produces: [GLOSSARY.md, ADRs]
prototype:
  type: model-invoked
  agents: [Apex_Harness]
  purpose: a throwaway prototype to answer a design question
  load-when: a design doubt that throwaway code resolves faster than theorizing
pr:
  type: model-invoked
  agents: [Apex_Harness]
  purpose: the PR body
  requires: [git + remote; git is not available on this machine → skip]
wizard:
  type: model-invoked
  agents: [Apex_Harness]
  purpose: an interactive bash wizard for steps only a human can do
  load-when: provisioning/credentials/external dashboards/manual migrations
grilling:
  type: model-invoked
  agents: [Apex_Harness]
  purpose: grill the user on a plan/decision (model-invoked variant)
  load-when: the user explicitly asks for a stress test
```

## 4. Productivity (support)

```yaml
handoff:
  type: model-invoked
  purpose: compact the current conversation into a handoff document
  notes: aligns with §8 of the harness SKILL.md (compact contracts); the base
    format is this skill aligned with the harness contract
writing-for-agents:
  type: model-invoked
  purpose: write docs for agents (skills, AGENTS.md)
  load-when: you MAINTAIN the harness itself (editing the repo's skills/agents)
security-audit-core:
  type: model-invoked
  purpose: Security Audit Squad protocol (DEEP AppSec, SEC-* JSON, defensive fixes only)
  load-when: AppSec audit, SEC-* finding, Apex_Hacker review, or Apex_SecurityFixer patch
  agents: [Apex_InjectionAuditor, Apex_AuthAuditor, Apex_SecApiAuditor, Apex_SecretsAuditor, Apex_Hacker, Apex_SecurityFixer]
  notes: canonical at .agents/skills/security-audit-core/; Cursor/OpenCode shims point there; no exploits/PoCs
ask-matt:
  type: user-invoked
  purpose: meta router over the skills repository
  load-when: the request fits no other table
teach: {type: user-invoked, purpose: teach a concept in the workspace, load-when: a teaching request}
to-questionnaire: {type: user-invoked, purpose: turn an unanswerable decision into a questionnaire, load-when: third parties must answer}
wait-what: {type: user-invoked, purpose: re-pitch a message that did not land, load-when: a communication is repeated}
```

## 5. Canonical compositions (agents)

```yaml
auto: # = Apex_Harness (Orchestrator) + adaptive composition with Apex_Dev
  core: [implement-spec|implement, tdd, code-review]
  optional: [research, grill-with-docs, to-spec, to-tickets, retro,
             domain-modeling, codebase-design, wayfinder]
  flow-trivial: [memory(0-1) → Apex_Dev → verify] # no research/grill/spec/tickets/retro
Apex_Dev:
  core: [implement*, tdd, code-review, codebase-design, domain-modeling]
  optional: [research, implement-spec]
  avoids: full architecture when the task does not require it
Apex_Bug:
  core: [diagnosing-bugs, tdd, code-review]
  optional: [research, codebase-design, domain-modeling]
  never: code before a confirmed root cause
Apex_Verifier: # independent subagent, read-only
  core: [run the checks from the verify-request handoff]
  skill-loading: usually needs no repo skills
Apex_ApiAuditor:
  core: [memory-audit-core, diagnosing-bugs]
  use: diagnosing-bugs phases 1-4; close = JSON; no edit
  stack: [memory-audit-js, memory-audit-node, memory-audit-python, memory-audit-fastapi, memory-audit-java, memory-audit-dotnet]
Apex_FrontendAuditor:
  core: [memory-audit-core, diagnosing-bugs]
  use: diagnosing-bugs phases 1-4; close = JSON; no edit
  stack: [memory-audit-js, memory-audit-react, memory-audit-astro]
Apex_SqlAuditor:
  core: [memory-audit-core, diagnosing-bugs]
  use: diagnosing-bugs phases 1-4; close = JSON; no edit
  stack: [memory-audit-sql, memory-audit-postgresql]
Apex_WorkerAuditor:
  core: [memory-audit-core, diagnosing-bugs]
  use: diagnosing-bugs phases 1-4; close = JSON; no edit
  stack: [memory-audit-workers, memory-audit-js, memory-audit-node, memory-audit-python, memory-audit-java, memory-audit-dotnet]
Apex_MemoryFixer:
  core: [memory-audit-core, tdd]
  use: recommendation is the seam; red before the minimal patch
  avoids: [diagnosing-bugs, code-review]
  stack: the skills of the technology the finding names
Apex_InjectionAuditor:
  core: [security-audit-core]
  use: DEEP static AppSec; close = JSON; no edit; no exploits
  domain: [SEC-INJ]
Apex_AuthAuditor:
  core: [security-audit-core]
  use: DEEP static AppSec; close = JSON; no edit; no exploits
  domain: [SEC-AUTH]
Apex_SecApiAuditor:
  core: [security-audit-core]
  use: DEEP static AppSec; close = JSON; no edit; no exploits
  domain: [SEC-API]
Apex_SecretsAuditor:
  core: [security-audit-core]
  use: DEEP static AppSec; close = JSON; no edit; no exploits
  domain: [SEC-SEC]
Apex_Hacker:
  core: [security-audit-core]
  use: DEEP static trust-boundary and agent-config review; close = JSON; no edit; no exploits
  domain: [SEC-HACK]
Apex_SecurityFixer:
  core: [security-audit-core, tdd]
  use: recommendation is the seam; defensive test then minimal secure patch
  avoids: [diagnosing-bugs, code-review, exploits/PoCs]
```

## 6. OpenCode agents of the harness (`.opencode/agents/`)

| ID | mode | key permission | purpose |
| --- | --- | --- | --- |
| `Apex_Harness` | primary | edit only in `.harness/*` | classify/route/coordinate/memory/verification |
| `Apex_Dev` | subagent | subagent/question denied | implementation with its own verification |
| `Apex_Bug` | subagent | subagent/question denied | root-cause diagnosis with evidence |
| `Apex_Verifier` | subagent | edit DENIED | independent verification with a verdict |
| `Apex_ApiAuditor` | subagent | edit denied | memory on APIs and backends; JSON close |
| `Apex_FrontendAuditor` | subagent | edit denied | retained UI memory; JSON close |
| `Apex_SqlAuditor` | subagent | edit denied | SQL and ORM memory; JSON close |
| `Apex_WorkerAuditor` | subagent | edit denied | worker and queue memory; JSON close |
| `Apex_MemoryFixer` | subagent | writes the named patch | applies one MEM-* recommendation |
| `Apex_InjectionAuditor` | subagent | edit denied | AppSec injection patterns; SEC-INJ JSON close |
| `Apex_AuthAuditor` | subagent | edit denied | AppSec authn/authz; SEC-AUTH JSON close |
| `Apex_SecApiAuditor` | subagent | edit denied | API AppSec; SEC-API JSON close |
| `Apex_SecretsAuditor` | subagent | edit denied | secrets/crypto exposure; SEC-SEC JSON close |
| `Apex_Hacker` | subagent | edit denied | trust-boundary and agent-config gaps; SEC-HACK JSON close |
| `Apex_SecurityFixer` | subagent | writes the named patch | applies one SEC-* secure recommendation |

Keep this registry current when the skill set changes (reinstall,
add, or deprecate one). The source of truth is the files on disk, not the
documentation; if an ID does not exist on disk, do not route to it.
