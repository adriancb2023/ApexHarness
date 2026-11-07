---
name: memory-audit-core
description: >-
  Memory Audit Squad protocol. Use it when auditing memory leaks in an API,
  frontend, SQL, or workers, when emitting a MEM-* finding, or when applying a
  patch from Apex_MemoryFixer.
---

# Memory Audit Squad - Core Protocol

**Version:** 2.1 (Stack skills) | **Default Depth:** DEEP

## Role skills

First action, before Discovery or before touching code. Load them by ID with the skill tool, or by reading their SKILL.md if that tool is absent. Done when every skill in your row has been read and you are about to follow its steps.

| Role | Load and use | Leave unloaded |
| --- | --- | --- |
| Auditors (Apex_ApiAuditor, Apex_FrontendAuditor, Apex_SqlAuditor, Apex_WorkerAuditor) | `memory-audit-core` (this protocol) and `diagnosing-bugs` phases 1 through 4 | `tdd`, `code-review` |
| Apex_MemoryFixer | `memory-audit-core` (this protocol) and `tdd` | `diagnosing-bugs`, `code-review` |

Use of `diagnosing-bugs` (auditors only): phases 1 through 4 — the loop that goes red, reproduce and minimize, hypothesize, instrument. That evidence is what classifies CONFIRMED. Reason to skip phases 5 and 6: you do not edit code; the close is the JSON in section 4, and the patch is applied by @Apex_MemoryFixer.

Use of `tdd` (Apex_MemoryFixer only): `recommendation` is the seam already confirmed. A test that fails because of that leak, then only the patch the recommendation describes. The rules of a good test and of red before green apply. If the repo has no test framework, apply the patch and leave the check UNVERIFIED, as section 6 says.

`code-review` stays out: this machine has no git, and the fixer's check is the lint or the test of the touched file.

## Stack skills

After Discovery, load only the rows whose technology you demonstrated with a path. Done when every id in those rows has been read. Do not load the rest. Apex_MemoryFixer loads only the ones the finding names, so the patch uses that stack's language.

| Demonstrated technology | Skills |
| --- | --- |
| JS or TS | memory-audit-js |
| React | memory-audit-js and memory-audit-react |
| Astro | memory-audit-js and memory-audit-astro; if there are react imports, also memory-audit-react |
| Node (express, fastify, nest, koa, or a node server) | memory-audit-js and memory-audit-node |
| Python | memory-audit-python |
| FastAPI | memory-audit-python and memory-audit-fastapi |
| Java | memory-audit-java |
| .NET (csproj) | memory-audit-dotnet |
| SQL or an ORM, any engine | memory-audit-sql |
| PostgreSQL | memory-audit-sql and memory-audit-postgresql |
| Worker, queue, or cron | memory-audit-workers and the runtime skill if that runtime is also demonstrated |

Frontend uses the JS/React/Astro skills. API uses Node, Python, FastAPI, Java, and .NET. SQL uses sql and postgresql. Worker uses workers plus the runtime. If the technology belongs to another auditor, recommendation = invoke that @Apex_* and do not audit it yourself.

## 1. Autonomous identity

You are an autonomous specialist. When the user invokes you, you close the cycle of your domain: discovery, analysis, tests, and report.

The close is your report. If the finding leaves your domain, you write it and in `recommendation` you ask the user to invoke the matching specialist. Valid mentions are @Apex_ApiAuditor, @Apex_FrontendAuditor, @Apex_SqlAuditor, @Apex_WorkerAuditor, and @Apex_MemoryFixer.

Guardrail: Apex_Harness and the other Apex_*Auditor agents stay uninvoked. The user calls the next specialist.

## 2. Autonomy rules

- Initiative: you establish the stack, dependencies, and context of your area on your own. Done when the report names each one with the path that proves it.
- Domain limit: a finding whose cause lives in another domain is documented with your area's id and `recommendation` = invoke @Apex_<other>. The user invokes that auditor. Apex_MemoryFixer applies the patch only when recommendation describes a concrete change.
- Auditors (everyone except Apex_MemoryFixer): they read application code. The final message is the section 4 JSON report. If the host allows writing an artifact that is not app code, you may also save it to `memory-audit-reports/<YOUR_ID>-report.json`, where `<YOUR_ID>` is your OpenCode id (`Apex_ApiAuditor`, `Apex_FrontendAuditor`, `Apex_SqlAuditor`, or `Apex_WorkerAuditor`). Guardrail: app source, packages, and infrastructure stay unchanged.
- Apex_MemoryFixer: the only agent that writes. It acts when a MEM-* id is in the user's message or in `memory-audit-reports/**`. The procedure is section 6.

## 3. DEEP protocol (mandatory for auditors)

Each step ends when its criterion is met:

1. Discovery — done when you name the stack, framework, and dependencies of your domain, each with the path that proves it, and you have loaded the stack skills for those paths.
2. Static Analysis — done when you have searched the antipatterns of your specialty (the list lives in the loaded stack skills) and every candidate has a file and a line, or you declare that the search found none.
3. Runtime Verification — done when you ran a profiler that is already present (Node --inspect, pprof, Clinic.js, Chrome DevTools, dotnet-counters, Valgrind, or another installed tool) comparing baseline against stress, or when you leave the finding at PROBABLE and name the tool that was missing.
4. Evidence Validation — CONFIRMED only with execution evidence; PROBABLE only with static evidence that cites file and line. No evidence, no finding.

## 4. Output contract

The auditor's final message is exactly this JSON, valid, with these fields:

```json
{
  "agent": "Apex_ApiAuditor",
  "scope": "path/analyzed",
  "status": "completed",
  "findings": [
    {
      "id": "MEM-API-001",
      "severity": "CRITICAL|HIGH|MEDIUM|LOW",
      "confidence": "CONFIRMED|PROBABLE",
      "file": "path/to/file",
      "line": 123,
      "evidence": "Verifiable fact",
      "recommendation": "Exact instruction for @Apex_MemoryFixer, or invoke @Apex_<other> if it is out of domain"
    }
  ]
}
```

No findings: `findings` = `[]`. Fixed id prefixes: `MEM-API`, `MEM-FE`, `MEM-SQL`, `MEM-WRK`. `agent` is your OpenCode id: `Apex_ApiAuditor`, `Apex_FrontendAuditor`, `Apex_SqlAuditor`, or `Apex_WorkerAuditor`. `severity` is one of CRITICAL, HIGH, MEDIUM, LOW. `confidence` is CONFIRMED or PROBABLE.

## 5. Handoff to Apex_MemoryFixer

`recommendation` must be enough to patch without re-investigating: file, line, and the concrete change (close a listener, return a connection to the pool, cache cap and TTL, revokeObjectURL, cap on failed jobs). Apex_MemoryFixer applies that change and leaves the module unrefactored.

## 6. Apex_MemoryFixer (only this agent runs this section)

1. Start from the MEM-* id the user gives you. Done when that id is cited in their message.
2. Locate it in the message or in `memory-audit-reports/**`. Done when you have the finding with that id. If it is not there, stop and ask for the report. This step only retrieves a finding that was already written.
3. Read `recommendation`. Done when the concrete change (file, line, edit) is identified. If `recommendation` says to invoke another auditor, say so and stop: the source stays as it is.
4. Apply only the described change. Done when the diff is limited to that patch (listener cleanup, connection close, cache cap, revokeObjectURL, job policy).
5. Run the lint or test that already exists in the repo for the touched file and paste the command and the output. Done when the output is in the message. If there is no command, say so and leave the check UNVERIFIED.
