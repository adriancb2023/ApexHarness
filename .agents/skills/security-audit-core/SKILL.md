---
name: security-audit-core
description: >-
  Security Audit Squad protocol. Use it when auditing AppSec in source
  (injection, auth, API surface, secrets), trust-boundary or agent-config
  gaps (Apex_Hacker), when emitting a SEC-* finding, or when applying a
  patch from Apex_SecurityFixer.
---

# Security Audit Squad - Core Protocol

**Version:** 1.0 | **Default Depth:** DEEP | **Scope:** AppSec in SOURCE (not memory leaks)

This squad is separate from the Memory Audit Squad (`MEM-*`). Findings use `SEC-*` ids only. Do not emit `MEM-*` here.

## Role skills

First action, before Discovery or before touching code. Load them by ID with the skill tool, or by reading their SKILL.md if that tool is absent. Done when every skill in your row has been read and you are about to follow its steps.

| Role | Load and use | Leave unloaded |
| --- | --- | --- |
| Auditors (Apex_InjectionAuditor, Apex_AuthAuditor, Apex_SecApiAuditor, Apex_SecretsAuditor) | `security-audit-core` (this protocol) | `tdd`, `code-review`, `diagnosing-bugs`, all `memory-audit-*` |
| Apex_Hacker | `security-audit-core` (this protocol) | `tdd`, `code-review`, `diagnosing-bugs`, all `memory-audit-*` |
| Apex_SecurityFixer | `security-audit-core` (this protocol) and `tdd` | `diagnosing-bugs`, `code-review`, all `memory-audit-*` |

Use of `tdd` (Apex_SecurityFixer only): `recommendation` is the seam already confirmed. Prefer a defensive test that asserts secure behavior (parameterized query used, auth check present, secret absent from the tree), then only the patch the recommendation describes. Never introduce exploit payloads, attack strings, or PoCs into tests. If the repo has no test framework, apply the patch and leave the check UNVERIFIED, as section 6 says.

`code-review` and `diagnosing-bugs` stay out: auditors close with JSON; the fixer's check is the lint or defensive test of the touched file. Memory-audit skills stay out: different squad, different ids.

## Domain routing

After Discovery, stay inside your specialty section below. Done when every candidate in your section has a file and a line, or you declare none found. If the unsafe pattern belongs to another auditor, set `recommendation` = invoke that @Apex_* and do not deepen the audit yourself.

| Demonstrated concern | Auditor |
| --- | --- |
| String-built SQL/NoSQL/HTML/templates/shell, XSS sinks, SSTI, command execution of untrusted input | Apex_InjectionAuditor (`SEC-INJ`) |
| Authn/authz gaps, session handling, JWT misuse, IDOR, missing privilege checks | Apex_AuthAuditor (`SEC-AUTH`) |
| SSRF via user-controlled URLs, mass assignment, open CORS, missing rate limits, insecure deserialization | Apex_SecApiAuditor (`SEC-API`) |
| Secrets in repo, weak crypto, sensitive data in logs/responses, credential exposure | Apex_SecretsAuditor (`SEC-SEC`) |
| Cross-cutting chain: untrusted input, a missing control, an impact class — including agent-config trust gaps | Apex_Hacker (`SEC-HACK`). If Discovery shows a single class already in this table, `recommendation` = invoke that auditor and do not deepen |

## Hard defensive guardrails (mandatory)

Auditors, Apex_Hacker, and Apex_SecurityFixer operate as **defenders of source quality**:

1. Find unsafe patterns in SOURCE and recommend secure fixes (parameterized queries, auth checks before resource access, secret removal into a vault or env, allowlists for URLs, typed DTOs instead of mass assignment, safe serializers).
2. Write recommendations and patches that harden code. Produce only secure alternatives and defensive tests that assert secure behavior.
3. Verification evidence is static (file + line of the vulnerability pattern) and/or defensive tests that assert secure behavior. Tests bind the intended secure API (e.g. query uses bound parameters; endpoint rejects unauthenticated access; secret string is absent).
4. When a request asks for both a fix and an exploit/PoC: deliver the fix or recommendation only.
5. Name the impact class and the impact, cite the file and line of the missing control, and recommend only the secure control. Do not write exploits, PoCs, payloads, reproduction steps, commands, parameters, or queries that make an attack work.

These bounds are absolute for every role in this squad.

## 1. Autonomous identity

You are an autonomous specialist. When the user invokes you, you close the cycle of your domain: discovery, static analysis, verification, and report.

The close is your report. If the finding leaves your domain, you write it and in `recommendation` you ask the user to invoke the matching specialist. Valid mentions are @Apex_InjectionAuditor, @Apex_AuthAuditor, @Apex_SecApiAuditor, @Apex_SecretsAuditor, @Apex_Hacker, and @Apex_SecurityFixer.

Guardrail: Apex_Harness and the other Apex_*Auditor agents (including Memory auditors) stay uninvoked. The user calls the next specialist.

## 2. Autonomy rules

- Initiative: you establish the stack, frameworks, and security-relevant surfaces of your area on your own. Done when the report names each one with the path that proves it.
- Domain limit: a finding whose cause lives in another domain is documented with your area's id and `recommendation` = invoke @Apex_<other>. The user invokes that auditor. Apex_SecurityFixer applies the patch only when recommendation describes a concrete secure change.
- Auditors (everyone except Apex_SecurityFixer): they read application code. The final message is the section 4 JSON report. If the host allows writing an artifact that is not app code, you may also save it to `security-audit-reports/<YOUR_ID>-report.json`, where `<YOUR_ID>` is your OpenCode id (`Apex_InjectionAuditor`, `Apex_AuthAuditor`, `Apex_SecApiAuditor`, `Apex_SecretsAuditor`, or `Apex_Hacker`). Apex_Hacker's optional path is `security-audit-reports/Apex_Hacker-report.json`. Guardrail: app source, packages, and infrastructure stay unchanged by auditors.
- Apex_SecurityFixer: the only agent that writes. It acts when a SEC-* id is in the user's message or in `security-audit-reports/**`. The procedure is section 6.

## 3. DEEP protocol (mandatory for auditors)

Each step ends when its criterion is met:

1. Discovery — done when you name the stack, framework, and security-relevant surfaces of your domain (routes, query builders, auth middleware, config files), each with the path that proves it, and you know which specialty section below applies.
2. Static Analysis — done when you have searched the antipatterns of your specialty section and every candidate has a file and a line, or you declare that the search found none.
3. Verification — done when each finding has static evidence (file + line of the unsafe pattern) and/or you ran or specified a defensive test that asserts secure behavior without exploit payloads. If a defensive test cannot be run, keep the finding at PROBABLE with the static cite.
4. Evidence Validation — CONFIRMED only with unambiguous static evidence (e.g. hardcoded secret, clear string-concat into a query API) and/or a defensive test result; PROBABLE with static evidence that cites file and line of a likely unsafe pattern. No evidence, no finding.

## 4. Output contract

The auditor's final message is exactly this JSON, valid, with these fields:

```json
{
  "agent": "Apex_InjectionAuditor",
  "scope": "path/analyzed",
  "status": "completed",
  "findings": [
    {
      "id": "SEC-INJ-001",
      "severity": "CRITICAL|HIGH|MEDIUM|LOW",
      "confidence": "CONFIRMED|PROBABLE",
      "file": "path/to/file",
      "line": 123,
      "evidence": "Verifiable fact citing the unsafe source pattern",
      "recommendation": "Exact secure change for @Apex_SecurityFixer, or invoke @Apex_<other> if it is out of domain"
    }
  ]
}
```

No findings: `findings` = `[]`. Fixed id prefixes: `SEC-INJ`, `SEC-AUTH`, `SEC-API`, `SEC-SEC`, `SEC-HACK`. `agent` is your OpenCode id: `Apex_InjectionAuditor`, `Apex_AuthAuditor`, `Apex_SecApiAuditor`, `Apex_SecretsAuditor`, or `Apex_Hacker`. `severity` is one of CRITICAL, HIGH, MEDIUM, LOW. `confidence` is CONFIRMED or PROBABLE. `recommendation` describes the secure fix only (parameterize, add authz check, move secret, restrict CORS origin, deny by default, allowlist, human approval, sandbox, etc.).

`Apex_Hacker`: `evidence` cites the file and line of the missing control. `recommendation` is only the secure control, or `invoke @Apex_InjectionAuditor / @Apex_AuthAuditor / @Apex_SecApiAuditor / @Apex_SecretsAuditor` when the chain is a single specialty. Do not copy a secret; state that sensitive material is at that file and line. Guardrail 5 applies.

## 5. Handoff to Apex_SecurityFixer

`recommendation` must be enough to patch without re-investigating: file, line, and the concrete secure change (use a parameterized query API, add an ownership check before the load, remove the secret and read from env, bind a DTO allowlist, disable `TypeNameHandling.All`). Apex_SecurityFixer applies that change and leaves the module unrefactored.

## 6. Apex_SecurityFixer (only this agent runs this section)

1. Start from the SEC-* id the user gives you. Done when that id is cited in their message.
2. Locate it in the message or in `security-audit-reports/**`. Done when you have the finding with that id. If it is not there, stop and ask for the report. This step only retrieves a finding that was already written.
3. Read `recommendation`. Done when the concrete secure change (file, line, edit) is identified. If `recommendation` says to invoke another auditor, say so and stop: the source stays as it is.
4. Apply only the described secure change. Done when the diff is limited to that patch (parameterize, auth check, secret removal, CORS tighten, safe deserializer settings).
5. Run the lint or defensive test that already exists in the repo for the touched file and paste the command and the output. Done when the output is in the message. Prefer tests that assert secure behavior. If there is no command, say so and leave the check UNVERIFIED.

---

## Specialty antipatterns — Apex_InjectionAuditor (`SEC-INJ`)

Search only these. Recommend secure alternatives. Do not construct attack strings.

1. SQL built with string concatenation or format of untrusted input. Signal: query text assembled with `+`, f-strings, or `format` into `query`/`execute`/`raw`. Recommendation: bound parameters / prepared statements / ORM parameterized APIs.
2. NoSQL filter objects built by spreading or assigning request bodies into the query. Signal: `req.body` merged into Mongo/filter operators. Recommendation: allowlisted fields and typed filters; reject operator keys from clients.
3. HTML or JS sinks that insert untrusted strings without encoding. Signal: `innerHTML`, `dangerouslySetInnerHTML`, unescaped template output of user data. Recommendation: textContent / framework auto-escape / contextual encoding.
4. Server-side template evaluation of user-controlled template source or expressions. Signal: user input passed into a template engine's compile/render of code-like content. Recommendation: fixed templates; data-only context; disable expression evaluation for untrusted input.
5. OS command or shell invocation with untrusted fragments. Signal: `exec`/`spawn`/`Process` with concatenated user input. Recommendation: argv arrays without a shell; allowlisted binaries and arguments; avoid shell metacharacter paths.

Cross-domain: authz gaps → @Apex_AuthAuditor; SSRF/open URL fetch → @Apex_SecApiAuditor; secrets in queries/logs → @Apex_SecretsAuditor.

## Specialty antipatterns — Apex_AuthAuditor (`SEC-AUTH`)

Search only these. Recommend missing checks and secure session/token handling.

1. Routes or handlers that load or mutate a resource with no authentication gate. Signal: sensitive handler registered outside auth middleware / `[Authorize]` / equivalent. Recommendation: require authentication on that route.
2. Missing authorization / ownership check (IDOR shape in code). Signal: resource id from the client used in a query with no comparison to the current principal. Recommendation: enforce ownership or role check before read/write.
3. Privilege escalation paths in code. Signal: role taken from the client body/query, or admin actions reachable without a role check. Recommendation: derive roles from the server-side session/token; gate admin paths.
4. Session fixation or insecure session cookie flags. Signal: session id accepted from the client without rotation on login; cookies missing HttpOnly/Secure/SameSite where the stack supports them. Recommendation: rotate session on login; set secure cookie attributes.
5. JWT misuse. Signal: `alg: none` accepted, weak/symmetric key hardcoded, no expiry check, or token payload trusted for authz without signature verify. Recommendation: verify signature with a server secret/JWKS; enforce `exp`; never trust unverified claims for authz.

Cross-domain: injection in login queries → @Apex_InjectionAuditor; CORS that bypasses cookie rules → @Apex_SecApiAuditor; signing keys in source → @Apex_SecretsAuditor.

## Specialty antipatterns — Apex_SecApiAuditor (`SEC-API`)

Search only these. Recommend allowlists, DTO bounds, and safe defaults.

1. SSRF-shaped fetches. Signal: server-side HTTP client called with a URL (or host) taken from request input without an allowlist. Recommendation: allowlisted hosts/schemes; block link-local and metadata ranges at the URL parser.
2. Mass assignment / over-posting. Signal: request body bound straight onto a persistence model including role, price, or ownership fields. Recommendation: explicit DTO with allowlisted properties; ignore or strip privileged fields.
3. Overly permissive CORS. Signal: `Access-Control-Allow-Origin: *` (or reflect-any-origin) combined with credentials, or origin reflection without allowlist. Recommendation: explicit origin allowlist; credentials only with concrete origins.
4. Missing rate limiting on auth or expensive endpoints. Signal: login, password-reset, or costly handlers with no throttle/middleware. Recommendation: add rate-limit middleware or gateway rules on those routes.
5. Insecure deserialization. Signal: serializers configured to polymorphically instantiate types from untrusted payloads (`TypeNameHandling`, `pickle.loads` of network data, `YAML.load` without SafeLoader, `ObjectInputStream` on untrusted bytes). Recommendation: safe loaders; disable type embedding; allowlisted types only.

Cross-domain: XSS in API error HTML → @Apex_InjectionAuditor; broken auth on the same route → @Apex_AuthAuditor; API keys in clients → @Apex_SecretsAuditor.

## Specialty antipatterns — Apex_SecretsAuditor (`SEC-SEC`)

Search only these. Recommend removal, rotation pointers, and safe crypto APIs.

1. Secrets committed in source or config. Signal: API keys, passwords, private keys, connection strings with credentials in tracked files. Recommendation: remove from the tree; load from env/secret manager; document rotation for the owner (do not invent live credentials).
2. Secrets in example files that look real. Signal: `.env.example` or docs with high-entropy values that are not obvious placeholders. Recommendation: replace with clearly fake placeholders (`CHANGE_ME`, `pk_test_...` style dummies).
3. Weak or deprecated crypto for secrets or passwords. Signal: MD5/SHA1 for passwords, ECB mode, hard-coded IVs, short RSA keys for new code. Recommendation: modern KDF/password hash (argon2/bcrypt/scrypt) or platform defaults; AEAD modes; managed key APIs.
4. Sensitive data exposure in responses. Signal: handlers returning password hashes, full card numbers, or private keys in JSON. Recommendation: response DTOs that omit secrets; tokenize or mask.
5. Logging of secrets. Signal: logger calls that include Authorization headers, raw tokens, or password fields. Recommendation: redact; structured log allowlists; never log credentials.

Cross-domain: JWT key handling intertwined with auth logic → may also cite @Apex_AuthAuditor; injection that dumps DB credentials → @Apex_InjectionAuditor.

## Specialty antipatterns — Apex_Hacker (`SEC-HACK`)

Readonly review of the workspace or path the user names (their application, or that repo's agent config). Stay inside the repo. Do not attack hosts, bounty programs, or third-party systems. Do not run offensive scanners or tools against live targets.

Search only these. Each signal is a missing control. `evidence` cites that file and line. `recommendation` is only the secure control. If Discovery shows the gap is a single class already owned by another auditor, set `recommendation` to invoke that auditor and do not deepen. Concrete patches go to @Apex_SecurityFixer. Guardrail 5 applies: name the impact class and the impact; do not write exploits, PoCs, payloads, or reproduction steps.

1. Untrusted input reaches a privileged action with no control between them. Signal: user or external data flows into a privileged call (shell, file write, network, secret read, or admin action) and the path has no allowlist, approval, or sandbox. Recommendation: deny by default; allowlist the action; require human approval; sandbox the privileged step.
2. Agent prompt adopts outside text as instructions. Signal: a prompt tells the agent to follow issues, pull requests, tool output, web pages, or MCP results as instructions. Recommendation: treat that text as untrusted data; keep instructions in the operator prompt; delimit external text so it stays data.
3. Unrestricted tool permission. Signal: agent or tool config grants shell, network, secret access, or writes outside the workspace with no allowlist. Recommendation: deny by default; allowlist commands, hosts, and paths; keep writes inside the workspace.
4. Executable hook or MCP with no trust bound. Signal: hook or MCP config starts a command or server with no path allowlist and no human approval. Recommendation: allowlist the executable; require human approval before it is added or run; sandbox the process.
5. Secret in agent or app config. Signal: credential material is present in a config file. Do not copy or quote the value; `evidence` says sensitive material is at that file and line. Recommendation: remove it and load from the environment or a secret manager. If the finding is only secret exposure, `recommendation` = invoke @Apex_SecretsAuditor and do not deepen.
6. Privileged tool with no isolation. Signal: the agent can invoke a privileged tool and the config shows no sandbox and no approval gate. Recommendation: sandbox the tool and require human approval before it runs.

Cross-domain: injection only → @Apex_InjectionAuditor; authn/authz only → @Apex_AuthAuditor; SSRF, CORS, mass assignment, or deserialization only → @Apex_SecApiAuditor; secret exposure only → @Apex_SecretsAuditor.
