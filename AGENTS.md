# ApexHarness — project rules

**Owner:** Adrián Cruz Barranco

This repository **is** the Engineering Agent Harness: an orchestration layer
(Orchestrator, Skill Router, Memory Router/Writer, Verification, Policies) that lives
inside OpenCode and reuses its native mechanisms. There is no external runtime:
no Node, no CLI, no service. OpenCode still executes everything; the harness provides
the coordination.

## Map

| Path | Role |
| --- | --- |
| `.opencode/agents/Apex_Harness.md` | Orchestrator (primary agent). Classifies, routes, coordinates, verifies, updates memory. Does not code. |
| `.opencode/agents/Apex_Dev.md` | DEV agent (subagent). Implementation with TDD. |
| `.opencode/agents/Apex_Bug.md` | BUG agent (subagent). Diagnosis with a proved root cause. |
| `.opencode/agents/Apex_Verifier.md` | Independent verification (read-only subagent). |
| `.opencode/agents/Apex_InjectionAuditor.md` | Security squad: injection patterns (SEC-INJ); readonly. |
| `.opencode/agents/Apex_AuthAuditor.md` | Security squad: authn/authz (SEC-AUTH); readonly. |
| `.opencode/agents/Apex_SecApiAuditor.md` | Security squad: API AppSec (SEC-API); readonly. |
| `.opencode/agents/Apex_SecretsAuditor.md` | Security squad: secrets/crypto exposure (SEC-SEC); readonly. |
| `.opencode/agents/Apex_Hacker.md` | Security squad: defensive trust-boundary and agent-config review (SEC-HACK); readonly. |
| `.opencode/agents/Apex_SecurityFixer.md` | Security squad: applies one SEC-* secure patch. |
| `.agents/skills/security-audit-core/` | Security Audit Squad protocol (canonical); Cursor/OpenCode shims point here. |
| `.opencode/commands/harness.md` | `/harness <task>`: explicit entry to the full protocol. |
| `.opencode/skills/harness-core/` | Registry + routing, memory, state, verification, and DoD tables. The only source; load it at the start of any task. |
| `.cursor/` | Native Cursor port: rules, `/harness`, `harness-core` shim, Engram MCP. Matt skills are installed separately (gitignored). |
| `opencode.json` | Permission policies (reference in `/docs/CAPABILITIES.md` and `policies/SAFETY.md`). |
| `.harness/` | Per-task artifacts: `state.md`, `cache.md`, `metrics.jsonl`. |
| `docs/` | Capability findings, metrics, Cursor portability, methodologies. |

## Universal rules (every agent, in any project with this harness)

1. **Evidence > assertion.** Never declare COMPLETED/PASS without a command that was run and its output.
2. **Source priority:** tests/evidence > current code > Engram > assumptions.
   A memory that contradicts the code is investigated; it is not obeyed.
3. **Skills on demand:** load only what adds value to this task (2–4 typical);
   say in one line what you drop and why.
4. **Minimum context:** the files and symbols involved in the task, not the whole repo.
5. **Engram:** consult it only when a gate justifies it; write only
   reusable knowledge (rules in harness-core §3 and §9).
6. **Compact handoffs:** a contract travels between agents, never the whole conversation.
7. **Pipeline state** (`.harness/state.md`) and metrics (`.harness/metrics.jsonl`)
   stay current; the Orchestrator writes them.
8. Agents do not edit the user's global configuration (`~/.config/opencode/**`).
9. Reply in the user's language.
10. **One harness:** Apex_Harness is the only valid Orchestrator in a repo
    with this harness; do not route to foreign agents (global `apex`, `build`, `general`,
    `explore`) — Apex_Harness's `subagent` allowlist blocks them at the
    permission layer (see harness-core §12).

## Environment notes

- `git` is not installed on this machine: any `git diff/log` check is marked
  UNVERIFIED and replaced by tests or file evidence. Installing git unlocks it
  (and the `npx skills add mattpocock/skills` installer).
- Matt skills are **not versioned**: install step 2 (README / harness-core §12).
  They live in `.opencode/skills/*` and `.cursor/skills/*` (gitignored except `harness-core`).
  Bootstrap: `scripts/bootstrap-matt-skills.ps1`.
- The `git` history of this directory belongs to a different earlier project
  (an external runtime harness, discarded). Do not touch it.
