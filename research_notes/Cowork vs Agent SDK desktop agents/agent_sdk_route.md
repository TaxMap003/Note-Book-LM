# Custom local desktop-agent app on the Claude Agent SDK + computer-use + browser control (Windows, as of 2026-10-03)

Scope note: researched 2026-10-03. Primary sources are official Anthropic docs (code.claude.com, platform.claude.com, support.claude.com, anthropic.com), package registries (PyPI/npm, queried live on 2026-10-03) and the Microsoft/Google MCP READMEs. Third-party/practitioner material is labelled. Items I could not confirm are marked UNVERIFIED. Cowork's built-in scheduling and non-Anthropic LLMs are out of scope.

## 1. Claude Agent SDK: version, capabilities, skills, MCP, subagents, sessions, approval hooks, Windows

### Takeaway
The Agent SDK (Python 0.2.163 / TypeScript 0.3.288) is "Claude Code as a library". It runs a bundled Claude Code binary and gives you built-in file/shell/web tools, MCP, subagents, sessions/resume, hooks and permission callbacks. It loads the same `SKILL.md` playbooks from `.claude/skills` folders. It can block a tool call until an external (phone) approval arrives: the `canUseTool` callback can stay pending indefinitely, and a `PreToolUse` hook can `deny` (which works in every mode) or `defer` (the process exits and the session resumes later). Windows works natively with the TypeScript SDK. The latest Python releases have shipped without a Windows wheel (see Gaps).

### Cited Findings
**Versions and packaging (checked live 2026-10-03)**
- Python `claude-agent-sdk` latest is 0.2.163 (uploaded 2026-09-30), requires Python >=3.10. TypeScript `@anthropic-ai/claude-agent-sdk` latest is 0.3.288 (2026-10-02), Node >=18. Both release very often: 148 Python versions published so far. — [PyPI](https://pypi.org/project/claude-agent-sdk/); [npm](https://www.npmjs.com/package/@anthropic-ai/claude-agent-sdk)
- The TS package ships native binaries as optional dependencies, including `claude-agent-sdk-win32-x64` and `win32-arm64`. — [npm registry metadata](https://registry.npmjs.org/@anthropic-ai/claude-agent-sdk)
- Python 0.2.160–0.2.163 publish wheels only for macOS and Linux (no `win` wheel). Earlier versions (134 of 148, up to 0.2.159) did ship Windows wheels. The README says the release workflow builds "platform-specific wheels for macOS, Linux, and Windows". — [PyPI files](https://pypi.org/project/claude-agent-sdk/#files); [README](https://github.com/anthropics/claude-agent-sdk-python/blob/main/README.md)
- Official quickstart: "Both the TypeScript and Python SDKs bundle a native Claude Code binary... If pip installs the Python SDK's source distribution instead of a platform wheel, for example on ARM64 Windows, no binary is bundled. Install Claude Code natively... The Python SDK finds it on your PATH." The quickstart has explicit "On Windows" install steps. — [Agent SDK quickstart](https://code.claude.com/docs/en/agent-sdk/quickstart)
- Changelog index: "Claude Code on Windows runs without Git Bash" (Week 18, Apr 27–May 1 2026); "a PowerShell tool for Windows" (Week 13, Mar 23–27 2026). — [code.claude.com docs index](https://code.claude.com/docs/llms.txt)
- Hosting guidance: "1 GiB RAM, 5 GiB disk, and 1 CPU per agent is a reasonable starting point"; each session runs in its own subprocess. Transcripts can be persisted with a `SessionStore` adapter. — [Hosting the Agent SDK](https://code.claude.com/docs/en/agent-sdk/hosting)

**Capabilities**
- The SDK gives "the same tools, agent loop, and context management that power Claude Code, programmable in Python and TypeScript". Capabilities: built-in tools (read/write/edit files, run commands, search the web), hooks, subagents, MCP, permissions, sessions ("resume or fork later"), skills/commands/memory loaded "from your project's `.claude/` and from `~/.claude/`, same as Claude Code", and plugins. — [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)
- Licence: use is governed by Anthropic's Commercial Terms of Service. — [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)

**Skills (same SKILL.md playbooks)**
- Skills are `SKILL.md` files on disk, loaded from `~/.claude/skills/`, `<cwd>/.claude/skills/` and parent directories, `add_dirs`/`additionalDirectories`, or plugins. Discovery is governed by `setting_sources`/`settingSources` (needs `"user"`/`"project"`). The new `skills` option takes `"all"`, a list of names, or `[]`. "The SDK doesn't provide a programmatic API for registering them." Skills can be dispatched as `/<name>` in the prompt. Authoring guidance is shared with Claude Code ("Its guidance applies to SDK sessions"). — [Agent SDK skills](https://code.claude.com/docs/en/agent-sdk/skills)

**Permissions and approval gating (core to "block until owner approves from phone")**
- Evaluation order: hooks, then deny rules, then ask rules, then permission mode, then allow rules, then the `canUseTool` callback. "a hook deny applies even in `bypassPermissions` mode". "Auto-approved tools never reach `canUseTool`... permission checks you put there are silently bypassed for that tool." For checks that must run on every call, use a `PreToolUse` hook. — [Configure permissions](https://code.claude.com/docs/en/agent-sdk/permissions)
- Modes: `default`, `dontAsk` (deny instead of prompting; `canUseTool` never called), `acceptEdits`, `bypassPermissions`, `plan`, `auto` (model-classifier approvals). Since TS SDK v0.3.286, omitting `permissionMode` may start in auto mode, so "pass `default` explicitly" if you rely on it. — [Configure permissions](https://code.claude.com/docs/en/agent-sdk/permissions)
- MCP tools whose server sets `_meta["anthropic/requiresUserInteraction"]` "always fall through to the callback, even when an allow rule matches" (requires Claude Code v2.1.199+). This lets you mark custom "money" tools as always-ask. — [Configure permissions](https://code.claude.com/docs/en/agent-sdk/permissions)
- "The callback can stay pending indefinitely. Execution remains paused until your callback returns. If a user might take longer to respond than your process can reasonably stay running, register a `PreToolUse` hook that returns the `defer` decision instead of waiting in the callback, so the process can exit and resume later from the persisted session." A `PermissionRequest` hook can "send external notifications (Slack, email, push) when Claude is waiting for approval." — [Handle approvals and user input](https://code.claude.com/docs/en/agent-sdk/user-input)
- Callback returns: Python `PermissionResultAllow(updated_input=...)` / `PermissionResultDeny(message=...)`; TS `{behavior:"allow", updatedInput}` / `{behavior:"deny", message}`. You can also modify the input before allowing. The Python example needs a "dummy hook" workaround to keep the stream open for `can_use_tool`. — [Handle approvals and user input](https://code.claude.com/docs/en/agent-sdk/user-input)
- Hooks configured as commands have default timeouts of "600 for `command`, `http`, and `mcp_tool`; 30 for `prompt`; 60 for `agent`". Windows hook example uses `powershell.exe -NoProfile -ExecutionPolicy Bypass -File ...`. — [Hooks reference](https://code.claude.com/docs/en/hooks)
- `PreToolUse` `permissionDecision` values include "allow/deny/ask/defer". The fetched page was truncated before the defer details. — [Hooks reference](https://code.claude.com/docs/en/hooks)

### Inferences
- Hard money gate: put the check in a `PreToolUse` hook, not only in `canUseTool`, because allow rules and modes skip the callback. Better still, never give the agent a raw "submit/pay" capability. Expose irreversible steps only as dedicated custom tools whose own code checks for a signed approval token from the phone service, so the gate is enforced outside the model.
- For browser work a "submit payment" is just a click. A hook sees `left_click(ref/coords)` or `browser_click(target)`, not the meaning. A reliable gate therefore needs URL/selector allow/deny lists in the tool executor, plus a rule that the agent stops at a review screen while a human or approved tool does the final submit. This is a design inference, not documented guidance.
- Long approvals (hours): use the `defer` + resume pattern so the Windows service isn't holding open processes and browser contexts. Keep the transcript in a `SessionStore`.
- Prefer TypeScript on Windows right now, or pin Python <=0.2.159, or install native Claude Code and point the Python SDK at it via PATH/`cli_path`.

### Gaps
- Exact `defer` semantics (versions, how resume restores the pending tool call, interaction with browser state) were truncated in my fetch. Verify at https://code.claude.com/docs/en/hooks#defer-a-tool-call-for-later.
- Why Python 0.2.160+ lacks Windows wheels: no announcement found, possibly a temporary pipeline gap. UNVERIFIED cause.
- Whether in-process SDK hook callbacks (as opposed to settings-file command hooks) have a timeout was not documented in what I read.

## 2. Authentication and billing: API key vs Pro/Max/Team subscription

### Takeaway
Officially, a developer-built Agent SDK app should use an API key (pay per token): "Developers building products or services... including those using the Agent SDK, should use API key authentication." Separately, Anthropic's support article says Agent SDK usage by Pro/Max/Team/Enterprise subscribers currently draws from their subscription limits. A planned separate monthly "Agent SDK credit" ($20–$200 by plan) was announced for 2026-06-15 and then paused "for now". So running your own SDK app on your own subscription is a grey zone that Anthropic contemplates. But "advertised usage limits... assume ordinary, individual usage", and the policy can change without notice. For an always-on firm automation, budget on the API.

### Cited Findings
- "Unless previously approved, Anthropic does not allow third party developers to offer claude.ai login or rate limits for their products, including agents built on the Claude Agent SDK. Use the API key authentication methods described in the Quickstart instead." — [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)
- "OAuth authentication is intended exclusively for purchasers of Claude Free, Pro, Max, Team, and Enterprise subscription plans and is designed to support ordinary use of Claude Code and other native Anthropic applications... Developers building products or services that interact with Claude's capabilities, including those using the Agent SDK, should use API key authentication through Claude Console or a supported cloud provider. Anthropic does not permit third-party developers to offer Claude.ai login into their own applications, or to route requests through Free, Pro, or Max plan credentials on behalf of their users." Also: "Advertised usage limits for Pro and Max plans assume ordinary, individual usage of Claude Code and the Agent SDK." And "Anthropic reserves the right to take measures to enforce these restrictions and may do so without prior notice." — [Claude Code legal and compliance](https://code.claude.com/docs/en/legal-and-compliance)
- The same page explicitly allows "configuring an API key in a development environment, secrets manager, or machine image for use by the customer's own authorized users" when billed to the key owner. — [Claude Code legal and compliance](https://code.claude.com/docs/en/legal-and-compliance)
- Support article (current status): "Pausing the changes to Claude Agent SDK usage described below. For now, nothing has changed" (as of 2026-06-15). Agent SDK usage on Pro, Max, Team and Enterprise "presently draws from your subscription's standard usage limits". Planned (inactive) monthly credits: Pro $20, Max 5x $100, Max 20x $200, Team Standard $20, Team Premium $100, Enterprise usage-based $20, Enterprise Premium seats $200. Overflow would go to usage credits at API rates. — [Use the Claude Agent SDK with your Claude plan](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan)
- Third-party reporting: still paused as of 2026-08-28. — [aicatchup (secondary)](https://aicatchup.com/news/claude-agent-sdk-monthly-credit-paid-plans); [The New Stack (secondary)](https://thenewstack.io/anthropic-pauses-claude-agent-sdk-subscription-change/)
- Earlier 2026 enforcement against subscription OAuth in third-party tools (Feb–Apr 2026) is described in secondary reporting. — [WinBuzzer (secondary)](https://winbuzzer.com/2026/02/19/anthropic-bans-claude-subscription-oauth-in-third-party-apps-xcxwbn/)
- A VentureBeat headline says Anthropic "reinstates OpenClaw and third-party agent usage on Claude subscriptions — with a catch". Not read; UNVERIFIED details. — [VentureBeat](https://venturebeat.com/technology/anthropic-reinstates-openclaw-and-third-party-agent-usage-on-claude-subscriptions-with-a-catch)
- Subscription prices (claude.com/pricing as fetched): Pro $20/mo ($17 annual); Max 5x "from $100/mo"; Team Standard $25/mo ($20 annual), Team Premium $125/mo ($100 annual); Enterprise "$20/seat/month, billed annually" plus "usage at API rates". The fetch also listed Max 20x as "From $100 per month", which looks like an extraction error (historically $200). UNVERIFIED. Limits reset on rolling 5-hour windows with weekly caps. — [claude.com/pricing](https://claude.com/pricing)
- The Claude API's computer-use and browser-use tools (Section 3) are Claude API (Messages API) features, billed per token like any API request. — [Pricing](https://platform.claude.com/docs/en/about-claude/pricing)

### Inferences
- The firm is both "developer" and "end user" of its own internal app. The legal page restricts offering Claude.ai login to others and intermediating, and the support article treats subscriber SDK usage as drawing on plan limits. A firm signing its own SDK app into its own Max/Team account is therefore not clearly prohibited. But it relies on a paused, changeable policy, and 24/7 unattended agents strain the "ordinary, individual usage" assumption. Recommendation: API key (Console) as the base, optionally a subscription for prototyping only.
- A computer-use loop that calls the Messages API directly (e.g. `computer_toolset_20260801`) needs an API key in any case. Subscription OAuth is for the Claude Code binary, not raw API calls.

### Gaps
- No explicit Anthropic statement found on "a single firm's internal unattended agents on a Team plan via the Agent SDK". Ask Anthropic sales if the subscription route matters.
- Max 20x price not cleanly confirmed in this fetch.

## 3. Computer-use tool (Claude API): version, models, actions, Windows, resolution, benchmarks, safety

### Takeaway
Current tool: `computer_toolset_20260801` (GA on the Claude API and Google Cloud, no beta header). It has 17 member tools and is the only computer-use form Claude 5.5 models accept there. It is a client-side tool: you must build the screenshot/mouse/keyboard executor. The reference implementation is a Linux Docker/Xvfb/xdotool container, so on Windows you must write your own executor (e.g. mss/PIL screenshots plus pyautogui/SendInput). It must run in an interactive, unlocked user session, not inside a Windows service in Session 0. Claude Code's own built-in computer use is macOS-only in the CLI and not available non-interactively, so it does not help a Windows SDK service. Opus 5.5 scores 81.8% (partial credit) on OSWorld 2.1 per Anthropic.

### Cited Findings
**Version, models, platforms**
- `computer_toolset_20260801` is GA on the Claude API and Google Cloud. "Claude 5.5 and later models support computer use only through the `computer_toolset_20260801` toolset and return an error for the earlier `computer_20251124` tool version." Opus 4.8 also supports the toolset. Opus 4.7/4.6/Sonnet 4.6/Opus 4.5 use `computer_20251124` with a beta header. Bedrock/Foundry/Claude Platform on AWS offer only earlier beta versions (Bedrock accepts `computer_20251124` for Opus/Sonnet 5.5). — [Computer use tool docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)
- Request shape: one `tools` entry `{"type":"computer_toolset_20260801"}` with no `name` and no display dimensions, plus an optional `configs` map to disable members (e.g. `zoom`). Results must echo `"toolset_name":"computer"`. — [Computer use tool docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)
- Haiku 4.5 is not listed for the toolset (it historically used `computer_20250124`). It should be treated as unsuitable for current computer-use/browser-use toolsets. — [Computer use tool docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool); [Browser use tool docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool)

**Actions (17 members)**
- `screenshot`, `zoom` (region at full resolution), `left_click`, `right_click`, `middle_click`, `double_click`, `triple_click` (with optional modifier keys), `left_click_drag`, `mouse_move`, `left_mouse_down`, `left_mouse_up`, `cursor_position`, `scroll` (direction/amount), `type`, `key` (combos, repeat 1–100), `hold_key` (≤300 s), `wait` (≤300 s). Claude returns batches of actions. You run them in order and stop at the first failure; skipped actions return `"Not executed: an earlier computer action in this turn failed."`. Batches usually end with a screenshot. — [Computer use tool docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)

**What the developer must implement / Windows**
- The reference environment is Linux: Xvfb virtual display, Mutter/Tint2, xdotool input, Docker container, Python tool implementations and a web UI (anthropic-quickstarts/computer-use-demo). The developer provides screenshot capture, mouse/keyboard input, coordinate scaling, handlers for all 17 members, and the agent loop. — [Computer use tool docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)
- Claude Code's built-in computer use: "Computer use is a research preview on macOS that requires a Pro or Max plan. It is not available on Team or Enterprise plans. It requires an interactive session, so it is not available in non-interactive mode with the `-p` flag." "Computer use in the CLI is not available on Linux or Windows. On Windows, use computer use in Desktop instead." The Desktop app supports macOS and Windows, but that is the Desktop app, not the SDK. — [Claude Code computer use (CLI)](https://code.claude.com/docs/en/computer-use)
- Windows Session 0: background services run in Session 0, isolated from the interactive desktop, so "Win32 desktop duplication (DXGI) and SendInput event injection... fail". "A locked/disconnected session must not be treated as a usable interactive desktop." — [satelle issue #199 (practitioner)](https://github.com/Microck/satelle/issues/199); [FireDaemon on Session 0 isolation](https://www.firedaemon.com/post/microsoft-windows-interactive-services-and-session-0-isolation); [Microsoft Tech Community: Session 0 Isolation](https://techcommunity.microsoft.com/blog/askperf/application-compatibility---session-0-isolation/372361)
- PyAutoGUI is a cross-platform (Windows/macOS/Linux) mouse/keyboard automation module, commonly used as a minimal computer-use harness. — [pyautogui](https://github.com/asweigart/pyautogui)
- Community Windows ports exist: `sunkencity999/windows_claude_computer_use` (Windows-native port of the Anthropic demo, built for Claude 3.5 Sonnet, so its tool version is stale) and `showlab/computer_use_ootb` ("Windows and macOS, no Docker required"). Both seen in search snippets only; maintenance status UNVERIFIED. — [windows_claude_computer_use](https://github.com/sunkencity999/windows_claude_computer_use); [computer_use_ootb](https://github.com/showlab/computer_use_ootb)

**Resolution and image cost**
- Recommended: "General desktop tasks: 1024x768 or 1280x720", "Web applications: 1280x800 or 1366x768". Avoid going above 1920x1080. High-res tier (Claude 5.5, Opus 5, Sonnet 5, Opus 4.7+): long edge 2576 px, max 4784 visual tokens, computed as ⌈w/28⌉×⌈h/28⌉. Screenshots cost "roughly 1,000–1,800 input tokens each". Keep ≤20 images per request (above 20, stricter per-image limits apply). Prune old screenshots in batches (e.g. every 25 turns) to preserve caching. If you downscale, scale coordinates back up. — [Computer use tool docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)
- Computed from that formula: 1024x768 ≈ 1,036 tokens; 1280x720 ≈ 1,196; 1280x800 ≈ 1,334; 1366x768 ≈ 1,372; 1920x1080 ≈ 2,691. — derived from [Computer use tool docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)

**Benchmarks**
- Anthropic (released 2026-09-22): OSWorld 2.1 (partial) Opus 5.5 81.8%, Fable 5.1 80.7%, Opus 5 74.0%. Sonnet 5.5 and Haiku 5.5 "will follow in the coming weeks"; no Sonnet 5.5 OSWorld score was on that page. — [Introducing Claude Opus 5.5](https://www.anthropic.com/claude-opus-5-5)
- Third parties describe the same 81.8% as "OSWorld 2.0 (partial pass)" and stress it is partial credit, not a full-task completion rate. Version label conflicts with Anthropic's "2.1". — [Vellum (secondary)](https://www.vellum.ai/blog/claude-opus-5-5-benchmarks-explained)
- The docs give no OSWorld numbers. They note that among older models, Sonnet 4.6 clicked more precisely than Opus 4.6, and Opus 4.7 "narrows that gap". — [Computer use tool docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)

**Safety recommendations (official)**
- "1. Using a dedicated virtual machine or container with minimal privileges... 2. Avoiding giving the model access to sensitive data, such as account login information... 3. Limiting internet access to an allowlist of domains... 4. Asking a human to confirm decisions that might result in meaningful real-world consequences and any tasks requiring affirmative consent, such as accepting cookies, completing financial transactions, or agreeing to terms of service." — [Computer use tool docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)
- "If you use the computer use tools, classifiers will automatically scan what the tools return, such as screenshots, to flag potential prompt injections... they will automatically steer the model to check whether the instruction really came from you before acting on it." Opt-out via support. "Using computer use within applications that require login increases the risk of bad outcomes as a result of prompt injection." — [Computer use tool docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)
- Opus 5.5 "matches or beats Opus 5 in every setting we tested, including coding, tool use, computer use, and web browsing" on prompt injection. It "ties Fable 5.1 for the lowest prompt injection success rate of any model tested" (Gray Swan). — [Introducing Claude Opus 5.5](https://www.anthropic.com/claude-opus-5-5)

### Inferences
- Two ways to get desktop control inside an Agent SDK session on Windows:
  - (a) Write a custom MCP server (screenshot/click/type via mss + pyautogui/pywinauto) and expose it to the SDK agent.
  - (b) Write a custom SDK tool like `desktop_task(instruction)` that runs its own nested Messages API loop with `computer_toolset_20260801` (e.g. Sonnet 5.5 or Opus 5.5). Option (b) keeps Anthropic's trained action schema and the documented injection classifiers. Option (a) is simpler, but classifier coverage for custom screenshot tools is not documented.
- The "Windows service" in the candidate design should be only the scheduler/queue/approval broker. The agent worker that touches the GUI must run as a process in an auto-logged-on, never-locked interactive user session (e.g. a scheduled task "run only when user is logged on", or a startup app), with display scaling at 100% and a fixed resolution such as 1280x800. A dedicated VM (e.g. Hyper-V) gives the sandbox Anthropic recommends.
- Windows DPI scaling (125%/150%) will break coordinate mapping unless the executor is DPI-aware. This is standard pyautogui/Win32 behaviour, not from Anthropic docs. UNVERIFIED in this research.

### Gaps
- No official Anthropic Windows executor or reference implementation was found.
- No Sonnet 5.5 OSWorld score yet. No published success rates for long (30–60 min) real-world portal workflows.

## 4. Browser control options: Anthropic browser-use toolset, Playwright MCP, Chrome DevTools MCP, browser-use, Stagehand

### Takeaway
For web portals, DOM/accessibility-tree control is cheaper and more reliable than screenshots. Options:
- **Anthropic `browser_toolset_20260801`** (new, GA on Claude API/Google Cloud): 27 default members plus 4 optional, including `read_page` (accessibility tree), `find`, `form_input` and tabs. You must implement the executor (Playwright/CDP).
- **Microsoft Playwright MCP** (`@playwright/mcp` 0.0.83): persistent profiles by default, `--user-data-dir`, `--cdp-endpoint`, or attach to a running Chrome/Edge via an extension. The most direct drop-in for an Agent SDK agent.
- **Google Chrome DevTools MCP** (`chrome-devtools-mcp` 1.10.1): `--userDataDir`, `--browserUrl`/`--wsEndpoint`, or `--autoConnect` to a running Chrome 144+.

All three can use a dedicated persistent Chrome profile with saved logins. Anthropic's own guidance says a fresh profile without credentials is safer, which conflicts with saved-login convenience.

### Cited Findings
- Anthropic browser use: `browser_toolset_20260801`, "27 member tools by default... plus four more when you enable them". Supported on Fable 5.1/5, Mythos 5.1/5, Opus 5.5/5, Sonnet 5.5/5, Opus 4.8. GA on Claude API and Google Cloud; not on Bedrock/Foundry/Claude Platform on AWS. Members: navigate, screenshot, zoom, clicks, hover, drag, scroll/scroll_to, type, key, hold_key, wait, `read_page` (accessibility tree with refs), `find` (natural-language element search), `get_page_text`, `form_input`, tab management. Disabled by default: `file_upload`, `javascript_exec`, `read_console`, `read_network`. "Your application runs every call against its own browser automation; nothing runs on Anthropic's side." "a tree read of a typical page often costs fewer input tokens than a screenshot." Security: "a fresh profile that holds no credentials", domain allowlist enforced at the network layer, refuse non-http(s) schemes, human confirmation for "purchasing, modifying accounts, messaging, and accepting terms". Injection classifiers also scan browser results. — [Browser use tool docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool)
- Browser toolset overhead: "about 6,600 input tokens"; computer toolset "about 4,500 input tokens" (disabling zoom saves ~410). — [Pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- Computer-use docs: browser use is preferred for tasks "that stay inside webpages"; the two toolsets can be combined in one request (dispatch by `toolset_name`). — [Computer use tool docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)
- Playwright MCP: "structured accessibility snapshots, bypassing the need for screenshots or visually-tuned models". Persistent profile by default (Windows: `%USERPROFILE%\AppData\Local\ms-playwright\mcp-{channel}-{workspace-hash}`), overridable with `--user-data-dir`. Other flags: `--isolated` + `--storage-state`, `--cdp-endpoint`, and `--extension` ("Connect to a running browser instance (Edge/Chrome only). Requires the 'Playwright Extension'") with `--profile-dir-name`. "A persistent profile can only be used by one browser instance at a time." `--caps vision` adds coordinate-based interactions. The README also says coding agents increasingly favour Playwright CLI + Skills over MCP for token efficiency, while MCP suits "long-running autonomous workflows". — [Playwright MCP README](https://github.com/microsoft/playwright-mcp/blob/main/README.md); version from [npm](https://www.npmjs.com/package/@playwright/mcp) (0.0.83, 2026-09-28)
- Chrome DevTools MCP: officially supports Chrome and Chrome for Testing only. It uses Puppeteer and "automatically wait[s] for action results". `--autoConnect` "automatically connects to a browser (Chrome 144+) running locally from the user data directory... Requires the remote debugging server to be started... via chrome://inspect/#remote-debugging". Also `--browserUrl`, `--wsEndpoint`, `--userDataDir` (default `$HOME/.cache/chrome-devtools-mcp/chrome-profile`), `--isolated`, `--slim` mode, and screenshot max-width/format options to cut image tokens. Disclaimer: it "exposes content of the browser instance to the MCP clients". Performance tools may send trace URLs to Google CrUX unless `--no-performance-crux` is set. — [Chrome DevTools MCP README](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/README.md); [configuration guide](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/configuration.md); version 1.10.1 (2026-09-23) from [npm](https://www.npmjs.com/package/chrome-devtools-mcp)
- browser-use (Python) latest 0.13.10 (2026-09-04). Stagehand (`@browserbasehq/stagehand`) latest 4.1.0 (2026-09-09). Features and persistent-profile support not researched in detail (time limit). UNVERIFIED. — [PyPI browser-use](https://pypi.org/project/browser-use/); [npm stagehand](https://www.npmjs.com/package/@browserbasehq/stagehand)

### Inferences
- Simplest robust stack for an SDK agent: Playwright MCP with a dedicated `--user-data-dir` per agent (one profile per concurrent agent), DOM snapshots by default, and screenshots only when needed.
- Saved logins in that profile contradict Anthropic's "no credentials" advice. To compensate: a per-agent profile with only the needed portals, a domain allowlist (proxy/firewall), no password-manager autofill for payment sites, and MFA prompts routed to the owner.
- The Anthropic browser toolset brings trained schemas and classifiers, but you must write and maintain a Playwright/CDP executor. MCP servers are ready-made.

### Gaps
- No head-to-head reliability benchmark found comparing DOM-based MCP vs screenshot computer-use on real portals.
- browser-use/Stagehand profile-attach details not verified.

## 5. Cost: current prices, screenshot cost, caching, worked per-run estimate, vs subscriptions

### Takeaway
At list prices, a typical 45-minute mixed browser/desktop run (~120 model turns) costs about $4.70 on Sonnet 5.5 or $7.30 on Opus 5.5 with good prompt caching. Without caching it is about $22 and $44. Light DOM-only runs cost about $1.60–$2.60; heavy screenshot-driven runs about $10–$15. One agent running daily on workdays is roughly $100–$160 a month. Five such agents are roughly $500–$800 a month on the API. That compares with $100–$200/month Max plans or $25–$125/month Team seats, but those have usage caps and an uncertain policy for SDK automation.

### Cited Findings
- List prices per MTok (input / 5m cache write / 1h cache write / cache read / output):
  - Opus 5.5: $4 / $5 / $8 / $0.20 / $20
  - Sonnet 5.5: $2 / $2.50 / $4 / $0.20 / $10
  - Haiku 4.5: $1 / $1.25 / $2 / $0.10 / $5
  - Fable 5.1: $10 / $12.50 / $20 / $0.25 / $50
  - Opus 5 / 4.8: $5 / … / $0.50 / $25
  - Sonnet 5's $2/$10 "is now the standard price".
  - Batch API is 50% off.
  - Claude 4.7+ tokenizer "produces approximately 30% more tokens for the same text".
  - US-only inference costs 1.1x.
  - Web search is $10 per 1,000; web fetch has no extra charge.
  — [Pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- Cache multipliers: 5-min write 1.25x, 1-hour write 2x, read 0.1x (0.05x on Opus 5.5, 0.025x on Fable 5.1). — [Pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- Tool overheads: computer toolset ~4,500 input tokens; browser toolset ~6,600; tool-use system prompt 286 tokens on Opus 5.5/Sonnet 5.5. Screenshots are billed as image input, ~1,000–1,800 tokens each. — [Pricing](https://platform.claude.com/docs/en/about-claude/pricing); [Computer use tool docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)
- Opus 5.5 "costs 40% less" than Opus 5 on typical workloads. — [Introducing Claude Opus 5.5](https://www.anthropic.com/claude-opus-5-5)
- Subscription list prices: see Section 2 ([claude.com/pricing](https://claude.com/pricing)).

**Worked estimate (my model; assumptions stated, numbers computed from official prices)**

Assumptions:
- Fixed prefix (SDK/Claude Code system prompt + built-in and MCP tool schemas + computer toolset): 25–30K tokens. The Claude Code system-prompt size is an UNVERIFIED assumption.
- Each turn adds 2.5–3.5K new tokens: a pruned DOM snapshot, a ~1.3K-token 1280x800 screenshot, or tool text. These are written to the 5-minute cache.
- Whole context is re-read from cache each turn. History is capped at 60–120K by tool-result clearing, with 2–6 full cache rewrites per run after clearing.
- Output including adaptive thinking: 500–900 tokens per turn.

| Scenario | Sonnet 5.5 (cached) | Opus 5.5 (cached) | Haiku 4.5 (cached; not usable for computer/browser toolsets) | Sonnet 5.5 uncached | Opus 5.5 uncached |
|---|---|---|---|---|---|
| Light: 60 turns, mostly DOM (≈3.5M input, 30K output) | $1.64 | $2.62 | $0.82 | $7.27 | $14.55 |
| Typical: 120 turns, browser + ~30 screenshots, 30–60 min (≈10.5M input, 84K output) | $4.67 | $7.31 | $2.34 | $21.90 | $43.80 |
| Heavy: 200 turns, screenshot-heavy desktop (≈23.5M input, 180K output) | $9.91 | $15.26 | $4.95 | $48.80 | $97.59 |

### Inferences
- Caching is the main cost lever, roughly a 4.5–6x saving. Opus 5.5's cache-read price equals Sonnet 5.5's ($0.20), so the Opus premium mostly shows in output and cache writes: about 1.5x Sonnet per run, not 2x.
- Monthly illustration: Roy alone, one typical run per workday (22/mo), is about $103 on Sonnet 5.5 or $161 on Opus 5.5. A team of five similar agents is about $500–$800/mo. Email triage and research agents that make few or no screenshots cost far less.
- Use Haiku 4.5 or Sonnet 5.5 subagents for text-only subtasks (classification, extraction) to cut cost further. Batch API (50%) only fits non-interactive document processing.
- Versus subscriptions: Max 5x/20x ($100/$200) or Team Premium ($125) can be cheaper on paper, but they have 5-hour/weekly caps, the "ordinary, individual usage" clause and a paused policy (Section 2). Raw computer-use API calls need an API key regardless.

### Gaps
- No measured token logs for this specific workload; the estimate should be validated in a pilot using `usage` fields.
- Actual Claude Code harness prefix size on Windows is unmeasured.

## 6. Build effort: what must be built, rough time, starter projects

### Takeaway
The SDK provides the agent loop, file and web tools, skills, MCP, hooks and sessions. The firm must still build the Windows-specific and operational layer:
- scheduler, folder watcher and job queue
- worker launcher in an interactive session
- Windows computer-use executor
- browser profile management
- approval service plus a phone channel
- secrets handling, logging/audit with screenshots, a dashboard, retry/watchdog, and cost controls

My rough estimate for one experienced developer is 4–8 weeks to a reliable MVP for one agent (Roy), plus ongoing maintenance for portal UI changes and fast-moving SDK versions. This estimate is UNVERIFIED (no source). No off-the-shelf open-source "scheduled Claude agent with computer use on Windows" was found that matches current tool versions.

### Cited Findings
- Building blocks the SDK covers: built-in tools, hooks, subagents, MCP, permissions, sessions, skills, plugins. — [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)
- Building blocks the developer must build for computer use: screenshot capture, input, coordinate mapping, 17 action handlers, agent loop. — [Computer use tool docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)
- For browser use: an executor (Playwright/Puppeteer/CDP), tab state and element-ref mapping. — [Browser use tool docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool)
- Session persistence across restarts needs a `SessionStore` adapter. Memory files and working-directory artifacts need their own storage. `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` matters when isolating agents/tenants. — [Hosting the Agent SDK](https://code.claude.com/docs/en/agent-sdk/hosting)
- The `PermissionRequest` hook is the documented place to send push/Slack/email notifications when approval is pending. — [Handle approvals and user input](https://code.claude.com/docs/en/agent-sdk/user-input)
- Starter/reference material:
  - Anthropic computer-use demo (Linux Docker): [anthropic-quickstarts/computer-use-demo](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo)
  - Agent SDK demos: [claude-agent-sdk-demos](https://github.com/anthropics/claude-agent-sdk-demos) (linked from the [overview](https://code.claude.com/docs/en/agent-sdk/overview))
  - Community Windows ports (search snippets only, UNVERIFIED currency): [windows_claude_computer_use](https://github.com/sunkencity999/windows_claude_computer_use) (built for Claude 3.5 Sonnet-era tool), [computer_use_ootb](https://github.com/showlab/computer_use_ootb)
  - [OpenCoworkAI/open-cowork](https://github.com/OpenCoworkAI/open-cowork), an "open-source AI agent desktop app for Windows & macOS" bundling Claude Code, MCP and Skills (UNVERIFIED depth)

### Inferences
Rough component estimates for one experienced developer. All UNVERIFIED and judgement-based:
- Scheduler/queue/folder watcher (e.g. Node/Python service + SQLite queue + Task Scheduler/NSSM): 3–5 days.
- Interactive-session worker host, auto-logon, lock prevention, crash watchdog: 2–4 days.
- Windows computer-use executor (mss + pyautogui/pywinauto, DPI handling, scaling, batch semantics) or nested `computer_toolset` loop: 5–8 days.
- Browser layer (Playwright MCP config, per-agent profiles, domain allowlist): 2–3 days.
- Approval service: `PreToolUse` hook + custom "irreversible action" tools + phone push (Pushover/Twilio/Teams) with signed approve/deny, plus `defer`/resume: 4–7 days.
- Logging/audit (transcripts, screenshots, tool calls, costs) and a basic dashboard: 4–7 days.
- Playbooks/skills per job, plus end-to-end testing on real portals: 1–2 weeks per complex job.

Ongoing costs: SDK releases nearly daily (148 Python versions), so pin versions. Portal UI changes and MFA/CAPTCHA breakage need human attention.

### Gaps
- No published effort benchmarks or case studies for this architecture.
- No maintained open-source Windows reference app on the 2026 toolsets was confirmed.

## 7. Known failure modes and reliability tips for long unattended computer-use runs

### Takeaway
Expect these failures:
- misclicks on small or ambiguous targets
- trouble with dropdowns and scrollbars
- the agent assuming success without checking
- context and screenshot bloat
- drift, loops, and declaring victory early on long tasks
- prompt injection from page content
- environment problems: locked screen, Session 0, DPI scaling, MFA/CAPTCHA, session timeouts

Mitigations: short, explicit playbooks; verify each step with a screenshot or DOM check; prefer keyboard shortcuts and DOM tools; use `zoom`; manage screenshot history; use deterministic code for anything that doesn't need judgement; use a separate checker or human for final review.

### Cited Findings
- Official tips: give "simple, well-defined tasks with explicit step-by-step instructions". Prompt the agent: "After each step, take a screenshot and carefully evaluate if you have achieved the right outcome..." "Some UI elements (such as dropdowns and scrollbars) might be tricky for Claude to manipulate using mouse movements... try prompting the model to use keyboard shortcuts." Use `zoom` for small text. Put instruction text before the image. Add action delays for slow apps. Validate coordinates and return `is_error`. Prune screenshots in batches, keep ≤20 images per request, and use server-side tool-result clearing on 5.5 models. "For agents that span multiple sessions, run end-to-end verification at the start of each session." `disable_parallel_tool_use` gives one action per round-trip. — [Computer use tool docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)
- Accuracy diagnostics from the docs: small targets or detail lost when downscaling a 4K+ source (use `zoom`); clicking the wrong element (use positional prompts, break into smaller steps); poor overall accuracy (try a 1280x720 baseline). — [Computer use tool docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)
- Prompt-injection risk rises in logged-in apps; classifiers help but "the precautions above remain important". — [Computer use tool docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)
- OSWorld 2.0 paper (snippet only, not fully read): long-horizon agents "mainly fail along five recurring dimensions: information grounding and tracking, perception–action timing, domain knowledge and workflow learning, verification and reflection, and long-horizon state drift." — [OSWorld 2.0, arXiv 2606.29537](https://arxiv.org/pdf/2606.29537)
- Practitioner write-ups (anecdotal): agents "declare victory before the work is actually done", forget across context resets, loop on equivalent actions, and drift silently. Recommended fix: separate the evaluator from the generator. — [Addy Osmani, Long-running agents](https://addyosmani.com/blog/long-running-agents/); [Glen Rhodes (anecdotal)](https://glenrhodes.com/agent-orchestration-failure-modes-silent-drift-reconciliation-and-the-supervision-mindset-shift/)
- Session 0 / locked-session failures for GUI automation from Windows services (see Section 3). — [satelle issue #199](https://github.com/Microck/satelle/issues/199)
- The Opus 5.5 headline number is partial credit (81.8%) on OSWorld, so even the best model does not finish every multi-step desktop task. — [Introducing Claude Opus 5.5](https://www.anthropic.com/claude-opus-5-5); [Vellum (secondary)](https://www.vellum.ai/blog/claude-opus-5-5-benchmarks-explained)

### Inferences
- Reliability design for this firm:
  - Split each job into short runs (5–15 min) with checkpoints written to the job folder, rather than one 60-minute session.
  - Use DOM tools for portals and computer use only for native apps.
  - Code deterministic steps (file renames, Excel parsing via openpyxl, PDF text extraction) rather than doing them via GUI.
  - Add a watchdog that kills runs exceeding turn or cost budgets.
  - Record screenshots and transcripts for audit.
  - Route MFA, CAPTCHA and unexpected dialogs to the owner instead of letting the agent improvise.
  - Run a second-pass "checker" subagent or a human review before any submission.
- Account for unattended-PC hygiene: disable sleep, screen lock and Windows Update auto-restart during working windows; set display scaling to 100%; keep a fixed resolution; give each agent its own Chrome profile.

### Gaps
- No quantitative reliability data found for 30–60 minute unattended runs on real government, payroll or tax portals.
- Practitioner sources are anecdotal.
