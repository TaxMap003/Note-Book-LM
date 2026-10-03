# Phone approvals/notifications and teach-by-recording for local AI desktop agents (Claude Cowork vs. custom Claude Agent SDK app), as of 3 October 2026

Research date: 2026-10-03. Context: a small US accounting firm with unattended agents on a dedicated Windows PC (Chrome portal entry, desktop documents, email, research). The owner approves from an iPhone or Android phone. Every claim has an inline source. Anything anecdotal or from a third-party blog is labelled. Dates are given where known. Items that are likely to change soon are flagged **[VOLATILE]**.

---

## Q1. Claude Cowork / Claude apps: does the phone get a push when a desktop or scheduled task needs input or permission, and can the owner approve or reply from the phone?

### Takeaway
Yes, in part. Anthropic now sends phone pushes and lets you approve from the phone through three separate mechanisms:
- **Cowork (cloud/remote sessions and Dispatch):** a push when a task finishes or needs input. Dispatch forwards permission prompts to you and **auto-denies after 10 minutes**.
- **Claude Code Remote Control:** pushes for permission prompts and questions. These prompts stay open until you answer.
- **Claude Code Channels (Telegram/Discord):** can relay permission prompts into a chat app.

None of these is a general "send notification" API that a task can call with custom Approve/Reject buttons. There is also a hard product limit: **Claude in Chrome refuses purchases and financial transactions whatever the permission setting.** That collides directly with the "moves money" steps under the Cowork route.

### Cited Findings
**Cowork cloud/mobile (rolled out mid-2026) [VOLATILE]**
- Anthropic's Cowork article says: "When Claude finishes a task or needs your input, you'll get a notification on your phone." Cloud Cowork runs on web, iOS/Android, the Chrome side panel and the Windows/macOS desktop apps. — [support.claude.com: Use Claude Cowork on web, desktop, and mobile](https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile)
- The same article says: "On October 6, 2026, new Cowork tasks on Pro and Max plans run in the cloud. Your scheduled tasks move to the cloud too, including ones that use files on your computer." **This date is 3 days after the research date, so it is an announced change, not yet observed.** — [support.claude.com 15520349](https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile)
- A cloud session can read and write connected local folders "only while the desktop app is open on that computer and the session was started on desktop." Local file access, local connectors, browser use and computer use all need the desktop app running. — [support.claude.com 15520349](https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile)
- I found no explicit wording in that article about approving *permission requests* from the phone. It mentions only notifications for "needs your input". — [support.claude.com 15520349](https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile)
- Help Net Security reported the phone/mobile Cowork expansion on 2026-07-08. — [Help Net Security](https://www.helpnetsecurity.com/2026/07/08/claude-cowork-phone-mobile-web/)

**Dispatch (Cowork feature, beta)**
- Dispatch is a long-running Cowork agent. It splits your request into child tasks and runs each as a Cowork or Code session.
- It requires a Pro or Max plan and the latest Claude Desktop on macOS or Windows.
- Task states include "Awaiting input" and "Awaiting answer". — [claude.com docs: Dispatch](https://claude.com/docs/cowork/guide/dispatch)
- "When a child task needs permission to take an action … the prompt is forwarded to you. **If you don't respond within ten minutes, the request is automatically denied** and the task continues without that action." — [claude.com docs: Dispatch](https://claude.com/docs/cowork/guide/dispatch)
- Mobile use: Claude Desktop must be open with the computer awake and online. You start a Dispatch conversation from the mobile app and the work runs on the desktop. — [claude.com docs: Dispatch](https://claude.com/docs/cowork/guide/dispatch)
- The support article on assigning tasks from anywhere says:
  - "You'll get a push notification on your phone when a task is done or when Claude needs your go-ahead."
  - The feature is a limited beta for Pro and Max.
  - Windows x64 is supported.
  - It runs as a single continuous thread.
  - The desktop must be awake with the app open.
  - It warns that "a phishing link opened in your browser could cascade into actions that are difficult or impossible to undo."
  — [support.claude.com 13947068](https://support.claude.com/en/articles/13947068-assign-tasks-from-anywhere-in-claude-cowork)
- Anecdotal (XDA): "App permissions expire after 30 minutes," so long tasks need re-approval. I could not confirm this in official docs. — [XDA Developers](https://www.xda-developers.com/claudes-dispatch-feature-turned-my-phone-into-a-remote-control-for-my-entire-workflow/)
- Users have asked for remote approval of macOS system dialogs with mobile push, which suggests OS-level dialogs are not covered. — [GitHub issue #42693](https://github.com/anthropics/claude-code/issues/42693)

**Claude Code Remote Control (CLI/Desktop/VS Code sessions)**
- Remote Control connects claude.ai/code or the Claude iOS/Android app to a Claude Code session running locally. Requirements:
  - a Pro, Max, Team or Enterprise plan;
  - **API keys are not supported**;
  - on Team/Enterprise, an Owner must turn it on.
  — [code.claude.com: Remote Control](https://code.claude.com/docs/en/remote-control)
- How mobile push works:
  - Claude decides when to push, usually when a long task finishes or it needs a decision.
  - In `/config` you can turn on "Push when Claude decides" and/or "Push when actions required" (the latter covers permission prompts and questions).
  - There is "no per-event configuration".
  — [code.claude.com: Remote Control](https://code.claude.com/docs/en/remote-control)
- "Claude Code keeps permission prompts and `AskUserQuestion` questions open until you answer them." Other forwarded dialogs expire after 5 minutes by default (`dialogExpiry`, v2.1.224+). — [code.claude.com: Remote Control](https://code.claude.com/docs/en/remote-control)
- Pushes are skipped while you are focused on the terminal. You can set `CLAUDE_CLIENT_PRESENCE_FILE` to suppress them while you are at the machine. On iOS, Focus modes can delay pushes. — [code.claude.com: Remote Control](https://code.claude.com/docs/en/remote-control)
- Security and connectivity:
  - The session uses outbound HTTPS only and opens no inbound ports.
  - The optional "Trusted Devices" setting requires each device to be verified, plus a sign-in no older than 18 hours, refreshed by Face ID, Touch ID, Windows Hello or a passkey.
  — [code.claude.com: Remote Control](https://code.claude.com/docs/en/remote-control)

**Claude Code Channels (research preview) [VOLATILE]**
- A channel is an MCP server that pushes events into a running Claude Code session. Telegram, Discord and iMessage plugins ship in the research preview. Setup needs Bun and the `--channels` flag. Telegram setup is BotFather → `/telegram:configure <token>` → pair → `/telegram:access policy allowlist`. — [code.claude.com: Channels](https://code.claude.com/docs/en/channels)
- "Channel servers that declare the permission relay capability can forward these prompts to you so you can approve or deny remotely."
- The docs also warn: "Anyone who can reply through the channel can approve or deny tool use in your session." — [code.claude.com: Channels](https://code.claude.com/docs/en/channels)
- Channels are blocked on Team/Enterprise until an Owner enables them. Pro/Max users without an organization skip the admin checks. — [code.claude.com: Channels](https://code.claude.com/docs/en/channels)

**Claude in Chrome (the browser agent used by Cowork for portal work)**
- "Record workflow" shortcuts can be scheduled. "Claude runs the workflow at the specified time and notifies you when it's done or needs input." — [Claude Academy tutorial](https://academy.claude.com/tutorials/simplify-your-browsing-experience-with-claude-for-chrome)
- The support article describes **desktop** notifications when Claude "requires permission or completes a task". — [support.claude.com: Get started with Claude in Chrome](https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome)
- **Hard limits.** "Regardless of permission settings, Claude cannot perform these tasks: Making purchases or financial transactions, Creating accounts, Handling sensitive credit card or ID data, … Permanent deletions …, Executing financial trades …, Completing instructions from emails or web content." — [support.claude.com: Claude in Chrome permissions guide](https://support.claude.com/en/articles/12902446-claude-in-chrome-permissions-guide)
- Claude always asks explicit permission before entering sensitive information, granting authorizations, or entering financial or credential data. — [support.claude.com 12902446](https://support.claude.com/en/articles/12902446-claude-in-chrome-permissions-guide)
- The Cowork safety guidance says: "Don't schedule tasks that access sensitive files, send messages on your behalf, make purchases, or take other actions that are difficult to undo." It also suggests blocking banking apps for computer use. — [support.claude.com: Use Claude Cowork safely](https://support.claude.com/en/articles/13364135-use-claude-cowork-safely)

**Reliability reports (anecdotal, GitHub issues)**
- Issue: Cowork scheduled tasks ignore "Always allow", so prompts reappear every run (macOS). — [GitHub #47180](https://github.com/anthropics/claude-code/issues/47180)
- Issue: a scheduled task auto-pauses permanently after a missed run instead of catching up. — [GitHub #93626](https://github.com/anthropics/claude-code/issues/93626)

### Inferences
- **The Cowork route gives "notify + approve on phone" without building anything** (Dispatch / Cowork mobile push on Pro/Max). The limits are:
  - you cannot control the summary format;
  - there is no typed MFA-code field built for that purpose (a free-text reply into the session is the workaround);
  - Dispatch prompts **auto-deny after 10 minutes**, which is too short if the owner is with a client;
  - permission prompts are tool-level ("allow Chrome to click X"), not business-level ("approve paying $4,210 to IRS EFTPS").
- **The Claude in Chrome ban on purchases and financial transactions probably blocks the core "moves money" use case under Cowork** (for example submitting a tax payment or releasing payroll). In practice the agent can prepare everything up to the final submit, and the owner (or a non-Claude step) presses the button. This is the biggest functional difference from an SDK app driving its own browser. Even there, Anthropic's usage policies and model behavior still apply.
- Remote Control and Channels are Claude Code features that need a claude.ai subscription login (Remote Control rejects API keys). A custom Agent SDK app authenticated with an API key **cannot rely on Remote Control push**. It needs its own notification channel (see Q2).
- The 6 Oct 2026 move of Cowork scheduled tasks to the cloud matters here. Tasks that touch local files, Chrome or computer use still need the Windows PC on and the desktop app open. The "dedicated always-on PC" design is still required for portal work.

### Gaps
- No official documentation found saying whether a *cloud* Cowork scheduled task forwards tool permission prompts to the phone, or what timeout applies (other than Dispatch's 10 minutes).
- No official "send push notification" tool callable from a Cowork task or skill was found. The "PushNotification" capability seen in this Claude Code environment is not documented for Cowork.
- I could not confirm the XDA "permissions expire after 30 minutes" claim.
- Unknown whether Channels permission relay can be used from an Agent SDK process; the docs describe it for the CLI with `--channels`.
- Third-party products such as Pushary (pushary.com) claim Cowork phone approvals. They were not evaluated.

---

## Q2. Custom Agent SDK app: best two-way phone-approval channels (Telegram, Twilio SMS, Pushover, ntfy, Teams/Power Automate, Slack, signed web page) compared on reliability, cost, security and Windows setup

### Takeaway
For one owner on a Windows PC behind a normal office router, a **Telegram bot with inline Approve/Reject buttons over long polling** is the best fit:
- free;
- no public URL needed;
- the button press identifies the user;
- typed replies work for MFA codes.

Alternatives:
- **Pushover emergency priority** is a very reliable "wake me up" alert. It has no action buttons, so approval goes through a link or a separate page.
- **ntfy** has HTTP action buttons but needs a reachable endpoint.
- **Teams / Power Automate Approvals** suits a firm already on Microsoft 365, but is heavier.
- **Twilio SMS** works on any phone, but US A2P 10DLC registration adds cost and paperwork.

### Cited Findings
**Telegram Bot API**
- Bots are free to create and operate. — [Telegram bot features](https://core.telegram.org/bots/features)
- Inline keyboards show buttons under a message. Pressing a callback button "doesn't send messages to the chat". The bot receives a `callback_query` and should answer it with `answerCallbackQuery`. Editing the keyboard after a press is recommended. — [Telegram bot features](https://core.telegram.org/bots/features)
- `getUpdates` receives updates by long polling with no public URL. It is mutually exclusive with webhooks. — [Telegram Bot API](https://core.telegram.org/bots/api)
- `setWebhook` takes a `secret_token`, sent back as the `X-Telegram-Bot-Api-Secret-Token` header. A `CallbackQuery` carries a `from` User object, so the code can verify who pressed. — [Telegram Bot API](https://core.telegram.org/bots/api)
- Flood (rate) limits exist but are not fully published. — [Telegram bot features](https://core.telegram.org/bots/features)
- Anthropic's official Claude Code Telegram channel plugin uses pairing codes and a sender allowlist. — [code.claude.com: Channels](https://code.claude.com/docs/en/channels)

**Pushover**
- Price: $4.99 one-time per platform (iOS, Android, Desktop), with a 30-day trial. Teams cost $5 per user per month. — [Pushover pricing](https://pushover.net/pricing)
- 10,000 messages per month free for an individual (25,000 for Teams). — [Pushover API](https://pushover.net/api)
- Emergency priority (priority=2):
  - repeats every `retry` seconds (minimum 30) until acknowledged, up to `expire` (maximum 10,800 s = 3 h);
  - returns a receipt you can poll;
  - takes an optional `callback` URL that is called on acknowledgment.
  — [Pushover API](https://pushover.net/api)
- Supports a supplementary URL, HTML and one image attachment up to 5 MB. The API docs mention **no action or reply buttons**. — [Pushover API](https://pushover.net/api)

**ntfy**
- Up to **three** action buttons per notification (view, http, broadcast, copy). An `http` action "sends a HTTP request when the action button is tapped" (POST by default, with custom headers and body). — [ntfy docs: publish](https://docs.ntfy.sh/publish/)
- `broadcast` is Android-only. `copy` does not show in browser desktop notifications. — [ntfy docs: publish](https://docs.ntfy.sh/publish/)
- Topics can be protected with username/password or access tokens. It can be self-hosted or used via ntfy.sh. — [ntfy docs: publish](https://docs.ntfy.sh/publish/)

**Twilio SMS (US)**
- $0.0083 per segment outbound and inbound. A long-code number costs $1.15 per month, toll-free $2.15 per month. — [Twilio US SMS pricing](https://www.twilio.com/en-us/sms/pricing/us)
- Carrier pass-through fees per outbound SMS: AT&T $0.0035, T-Mobile $0.0045, Verizon $0.005. US A2P 10DLC is "subject to registration onboarding fees". — [Twilio US SMS pricing](https://www.twilio.com/en-us/sms/pricing/us)
- Third-party estimate: 10DLC costs $4–44 one-time for brand registration, $15 campaign vetting, and $1.50–10 per month per campaign. — [textbee.dev](https://textbee.dev/blog/twilio-pricing-real-cost-breakdown) (secondary source; check with Twilio)

**Microsoft Teams / Power Automate approvals**
- If no timeout is set, "Start and wait for an approval" waits up to 30 days, the maximum run time of a cloud flow. — [LinkedIn: Approval timeouts (practitioner)](https://www.linkedin.com/pulse/approval-timeouts-microsoft-power-automate-petter-skodvin-hvammen); [spguides](https://www.spguides.com/approval-timeout-in-power-automate/)
- Approvals is a **standard** (non-premium) connector. Approvers act through email, Outlook actionable messages or Teams. — [Microsoft Learn: Approvals connector](https://learn.microsoft.com/en-us/connectors/approvals/)
- Practitioner claims (secondary source): adaptive cards render natively in Teams mobile, and a flow using the HTTP trigger needs a **premium** license. — [Alphavima](https://alphavima.com/blog/power-automate-teams-adaptive-card-approval/)

**Slack**
- Socket Mode lets an app receive interactive payloads (button clicks, modals) over WebSocket "without exposing a public HTTP Request URL". It needs an app-level token with `connections:write`. Connections refresh every few hours, so the app must reconnect. — [Slack docs: Socket Mode](https://docs.slack.dev/apis/events-api/using-socket-mode)
- The Agent SDK docs show forwarding `Notification` hook events to a Slack incoming webhook. — [code.claude.com: Agent SDK hooks](https://code.claude.com/docs/en/agent-sdk/hooks)

### Inferences
**Comparison for this firm** (cost and setup effort are my estimates from the cited facts):

| Option | Two-way? | Typed MFA code? | Public URL needed on PC? | Cost | Setup on Windows | Security notes |
|---|---|---|---|---|---|---|
| Telegram bot (long polling) | Yes: inline buttons + replies | Yes: reply / ForceReply message | No | Free | Low: a Python/Node process plus a BotFather token | Allow only the owner's numeric user ID (from `callback_query.from`); put a random nonce in callback_data; edit the message after use so it cannot be replayed; Telegram cloud chats are not end-to-end encrypted, so keep sensitive data out of messages |
| Pushover (emergency) + approval web page | One-way push; acknowledge only | Only via a linked page | Yes, for the page (or a tunnel) | $4.99 per platform | Low for alerts; medium with the page | Strong "wake-up" alerting (repeats up to 3 h); approval security depends on the page |
| ntfy (self-hosted or ntfy.sh) | Yes, via http action buttons | Not natively (no reply text field found in docs) | The action URL must be reachable from the phone (public/tunnel/VPN) | Free if self-hosted | Medium | Use access tokens; sign action URLs; iOS action support needs checking |
| Twilio SMS | Yes: reply "YES 4821" / code | Yes | Yes for inbound webhooks (or poll the Twilio API) | About $1.15/mo + ~$0.012/msg + 10DLC fees | Medium-high (10DLC/toll-free verification paperwork) | SMS can be spoofed or SIM-swapped; require a one-time token in the reply |
| Teams / Power Automate Approvals | Yes: Approve/Reject card with comments | Comments field | No, if triggered via a standard connector (e.g., a SharePoint list row or email); the HTTP trigger is premium | Included with M365 (premium for HTTP) | Medium-high (flow design; cloud-to-local link) | Approver is tied to Entra ID identity, which suits audit; up to 30-day wait |
| Slack (Socket Mode) | Yes: buttons/modals | Yes: modal input | No | Free tier may suffice (not verified) | Medium | Workspace membership controls who can approve; restrict to the owner's user ID |
| Self-hosted approve-link web page | Yes | Yes (form) | Yes (or Cloudflare Tunnel / Tailscale) | Low | Medium-high | Must build HMAC-signed, single-use, short-expiry links behind login or passkey; risk of link prefetch by email scanners |

- **Suggested default:** Telegram for the decision and code entry, plus Pushover emergency priority as a fallback if no answer arrives within N minutes. Send a reminder, then fail closed (deny) after a set deadline.
- Avoid putting a full account number or SSN in any push or chat message; use the last 4 digits.

### Gaps
- Telegram `callback_data` size limit (commonly cited as 1–64 bytes) was not confirmed from the fetched page.
- Not confirmed: whether the ntfy iOS app supports `http` action buttons; ntfy.sh paid tier pricing.
- Not confirmed: Slack free-plan limits for bots; Microsoft's official current licensing for Teams adaptive-card approvals.
- No published reliability or latency statistics (delivery SLA) were found for any of these services.

---

## Q3. Human-in-the-loop approval-gate patterns (Claude Agent SDK hooks / permission callbacks; LangGraph interrupts) and what an approval summary should show before a payment

### Takeaway
The Claude Agent SDK provides the right hooks:
- **`canUseTool`** can wait for a phone answer **indefinitely**.
- A **`PreToolUse` hook** sees *every* tool call and can return allow, deny, ask or **defer**. Defer ends the turn so the process can exit and resume later from the saved session.
- The `PermissionRequest` and `Notification` hooks can push alerts.

LangGraph's `interrupt()` with a durable checkpointer is the equivalent pattern there.

Best practice is to gate **business actions** (a custom "submit_payment" tool with structured fields) rather than raw clicks. Show a short, verifiable summary and fail closed on timeout.

### Cited Findings
- `canUseTool` fires when Claude wants a tool that is not auto-approved, and when Claude calls `AskUserQuestion`. "The callback can stay pending indefinitely." For waits longer than the process can stay alive, register a `PreToolUse` hook returning `defer` "so the process can exit and resume later from the persisted session." — [code.claude.com: Handle approvals and user input](https://code.claude.com/docs/en/agent-sdk/user-input)
- "The callback never fires for auto-approved tools … For logic that must apply to every tool call, use a `PreToolUse` hook." — [code.claude.com: user input](https://code.claude.com/docs/en/agent-sdk/user-input)
- Responses can be: allow (optionally with modified `updatedInput`), deny with a message Claude sees, "approve and remember" via `updatedPermissions`, or a redirect via streaming input. — [code.claude.com: user input](https://code.claude.com/docs/en/agent-sdk/user-input)
- Custom tools can "integrate external approval systems". — [code.claude.com: user input](https://code.claude.com/docs/en/agent-sdk/user-input)
- `PreToolUse` hooks can return `permissionDecision` of "allow", "deny", "ask" or "defer". Precedence is deny > defer > ask > allow. Defer ends the turn with `stop_reason: "tool_deferred"`. — [code.claude.com: Agent SDK hooks](https://code.claude.com/docs/en/agent-sdk/hooks)
- **Hook timeout pitfall:** hook callbacks default to a **600-second** timeout. If a `PreToolUse` hook times out, "Claude Code doesn't run the tool call" and the turn continues. So a long phone wait should live in `canUseTool` (indefinite), use a raised `timeout`, or use `defer`. — [code.claude.com: Agent SDK hooks](https://code.claude.com/docs/en/agent-sdk/hooks)
- The `Notification` hook fires `permission_prompt` "once a permission request has waited about six seconds on your canUseTool callback" (TS SDK v0.3.233+, Python v0.2.139+). The docs include an example of forwarding to Slack. — [code.claude.com: Agent SDK hooks](https://code.claude.com/docs/en/agent-sdk/hooks)
- `AskUserQuestion` limits: 1–4 questions with 2–4 options each; not available in subagents. — [code.claude.com: user input](https://code.claude.com/docs/en/agent-sdk/user-input)
- LangGraph `interrupt()` needs a checkpointer (durable in production) and a `thread_id`. You resume with `Command(resume=value)`. State is saved and the graph "waits indefinitely". "Side effects called before interrupt must be idempotent," because the node re-runs on resume. — [LangChain docs: LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)
- OWASP LLM06 "Excessive Agency" recommends human approval for high-impact actions such as financial transactions. It also says not to rely on the LLM to decide authorization; downstream systems should enforce it. — [OWASP LLM06:2025 Excessive Agency](https://owasp.github.io/www-project-top-10-for-large-language-model-applications/2_0_vulns/LLM06_ExcessiveAgency.html)
- Anthropic guidance for Claude in Chrome: "for work with real consequences—money, messages sent as you, important files—stay close and review what Claude does." — [support.claude.com 12902446](https://support.claude.com/en/articles/12902446-claude-in-chrome-permissions-guide)

### Inferences
**Recommended gate design for the SDK app**
1. Give agents no raw "click the Submit button on bank site" freedom. Expose an MCP or custom tool such as `request_irreversible_action{type, payee, amount, source_account_last4, due_date, reference, evidence_screenshot}`.
2. Enforce it with a `PreToolUse` hook: deny any browser click on known "submit/pay/file" selectors unless an approval token for that exact payload exists.
3. The approval service sends the summary to Telegram (or another channel) and waits in `canUseTool` or the tool body. On timeout it returns deny with a reason.
4. Log every decision with a timestamp, approver ID and payload hash.

**Approval summary contents** (my synthesis, based on payment-control practice):
- agent name and playbook step;
- action type ("Submit EFTPS payment", "File 941");
- client name;
- payee or agency;
- **amount** and source account (last 4);
- settlement or effective date;
- reference or invoice number;
- what it was checked against (e.g., "matches the 941 liability of $X in the workbook");
- one cropped screenshot of the confirmation screen;
- an "irreversible" label;
- the approval expiry time.

Keep it under about 6 lines so it reads on a lock screen. Never auto-approve on timeout. Use one-tap Reject plus "Reject with note", so the note returns to Claude as a deny message.

**Other design notes**
- Approval fatigue is a risk. Only truly irreversible or money-moving steps should reach the phone; everything else is pre-approved by allow rules or by the playbook.
- The Dispatch-style 10-minute auto-deny is a sensible fail-closed default, but the firm should choose its own window (e.g., 2–4 hours, with a reminder).

### Gaps
- No Anthropic-published guidance was found specifically on payment-approval summary content. The list above is synthesis, not sourced best practice.
- No public benchmark was found on approval-fatigue rates for agent HITL.

---

## Q4. Relaying MFA / verification codes from the owner to the agent safely

### Takeaway
There are three options, safest first:
1. **Remove the human from the loop where the firm controls the account.** Store TOTP seeds in a password manager the agent's tooling can fill without the model seeing them. 1Password for Claude does this, but is **Mac-only today**.
2. **For codes sent to the owner's phone** (SMS or email OTP from portals), use a typed-reply channel (a Telegram reply, an SMS reply to Twilio, or a form) bound to that specific request. Inject the code with a tool that never echoes it into model context or logs.
3. **Never** put long-lived passwords in prompts or skills.

### Cited Findings
- 1Password for Claude (July 2026):
  - "zero-exposure architecture";
  - after biometric approval, 1Password injects the credential and one-time code into the page; "Claude never accesses the actual password or one-time code";
  - works with the Claude desktop app and Claude in Chrome;
  - currently **Mac only**;
  - built around per-task, user-initiated approval (unattended use is not addressed).
  — [1Password blog: 1Password for Claude](https://1password.com/blog/1password-for-claude); [1Password press release, July 2026](https://1password.com/press/2026/july/1password-for-claude)
- 1Password's Secure Agentic Autofill for Browserbase (early access, announced Oct 2025) delivers credentials to browser agents without exposing them. — [SiliconANGLE](https://siliconangle.com/2025/10/08/1password-tackles-ai-credential-risks-new-agentic-autofill-integration-browserbase/)
- Claude in Chrome always asks explicit permission before entering credential or financial data. — [support.claude.com 12902446](https://support.claude.com/en/articles/12902446-claude-in-chrome-permissions-guide)
- Agent SDK hooks can "inject credentials" by transforming tool inputs (`updatedInput`), and `PostToolUse` can replace tool output before Claude sees it (`updatedToolOutput`). — [code.claude.com: Agent SDK hooks](https://code.claude.com/docs/en/agent-sdk/hooks)
- Record-a-skill warning: "Don't type passwords or secrets … while recording." — [support.claude.com 12512198](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)

### Inferences
**Pattern for the SDK route**
1. The agent reaches an MFA screen and calls `request_mfa_code{portal, client, request_id}`.
2. The approval service sends a Telegram message: "IRS e-Services wants a code for Client X. Reply with the 6-digit code within 10 min."
3. The owner's reply is matched to `request_id` and the sender ID.
4. A dedicated `fill_secret_field` tool types the code through Playwright or CDP. A `PostToolUse` hook redacts it, so the code never enters the transcript.
5. The code is discarded and the request expires after one use.

**Pattern for the Cowork route**
- The owner types the code as a reply in the Dispatch or Cowork mobile session. The code then enters the model context and transcript. That is acceptable for short-lived OTPs, but less clean.

**Longer-term fixes**
- Move firm-controlled accounts to TOTP stored in a vault.
- Ask portals for "remember this device" on the dedicated PC.
- For IRS and state portals that require the owner's own identity verification, keep a human step.

### Gaps
- No Windows availability date for 1Password for Claude was found.
- No official Anthropic guidance was found on relaying SMS OTPs into Cowork sessions.
- Unknown whether 1Password's biometric approval can be done from the phone for a remote, unattended PC.

---

## Q5. Can current Claude models take video input directly? If not, what is the standard workaround and how accurate is it?

### Takeaway
No. As of Oct 2026 the Claude API and apps accept **images (JPEG/PNG/GIF/WebP) and text, not video or audio files**; animated GIFs use only the first frame. The standard workaround is:
- extract key frames with ffmpeg;
- transcribe the narration with Whisper;
- interleave timestamped frames and transcript and send them to Claude.

Inside Cowork, Anthropic's own "Record a skill" accepts a screen recording (see Q6), but that is a product feature, not API video input.

### Cited Findings
- Supported formats: "JPEG, PNG, GIF, and WebP … Animations are unsupported, and only the first frame is used." — [platform.claude.com: Vision](https://platform.claude.com/docs/en/build-with-claude/vision)
- Image limits:
  - up to 600 images per API request (100 for 200k-context models) and 20 per message on claude.ai;
  - 32 MB request-size limit;
  - more than 20 images in a request triggers a stricter per-image size limit (resize to ≤2000 px);
  - the Files API is recommended for many images.
  — [platform.claude.com: Vision](https://platform.claude.com/docs/en/build-with-claude/vision)
- Token cost:
  - visual tokens = ⌈w/28⌉×⌈h/28⌉;
  - Claude 4.7+ models use a high-resolution tier (2576 px long edge, 4784 visual tokens maximum);
  - a 1920×1080 frame is about 2,691 tokens on the high-res tier, or 1,560 tokens if downscaled on the standard tier;
  - example: Opus 5 at $5 per million input tokens costs about $6.48 per 1,000 1-megapixel images.
  — [platform.claude.com: Vision](https://platform.claude.com/docs/en/build-with-claude/vision)
- Anthropic does not use uploaded images for training. Images are not stored beyond the request (Files API aside). — [platform.claude.com: Vision FAQ](https://platform.claude.com/docs/en/build-with-claude/vision)
- Native video input "does not exist in Claude Code or the API" (as of 2026-05-07). Community plugins (late April 2026) instead use:
  - ffmpeg frame extraction (30–100 frames);
  - Whisper transcription (local, Groq or OpenAI);
  - timestamped transcripts.
  Stated limits: visual changes between sampled frames are invisible; quality depends on transcription; a 5-minute video costs about 50–80K input tokens. — [ClaudeCamp (blog)](https://claudecamp.ai/blog/claude-code-video-processing)
- The community plugin `claude-video-vision` uses ffmpeg plus Gemini, local Whisper or OpenAI for audio, with adaptive fps and resolution. — [GitHub: jordanrendric/claude-video-vision](https://github.com/jordanrendric/claude-video-vision)
- There are open feature requests for native video input in Claude Code. — [GitHub #12676](https://github.com/anthropics/claude-code/issues/12676); [GitHub #32130](https://github.com/anthropics/claude-code/issues/32130)
- Source-quality warning: one search aggregator attributed "Project Astra" to Anthropic. It is a Google project, so that source was discarded.

### Inferences
- **Accuracy:** frames plus transcript work well for "what screen, what field, what was said". They miss quick UI states (dropdown choices, tooltips, auto-filled values) unless frames are sampled at click events rather than at a fixed fps. Pairing frames with an event log (click coordinates, URL, DOM or UIA element names) fixes most of this (see Q8).
- **Cost:** a 10-minute demo sampled at about 60 event-driven frames (1080p, high-res tier) is about 160K visual tokens, roughly $0.80 of Opus 5 input before transcript and output. That is cheap compared with the owner's time.

### Gaps
- No published accuracy benchmark was found for the frames-plus-Whisper approach on UI procedure extraction.
- No Anthropic statement or roadmap date for native video input was found. The ClaudeCamp prediction ("within two release cycles") is speculation.

---

## Q6. Built-in Anthropic features that turn a demonstration into a reusable workflow or skill

### Takeaway
Two exist as of Oct 2026, and neither covers the firm's Windows setup cleanly:
1. **Cowork "Record a skill"** (launched 21 Jul 2026). You record your screen and voice for up to about 10 minutes and Claude proposes a skill (SKILL.md) for you to review. **Mac only**; not on Windows or the Enterprise plan.
2. **Claude in Chrome "Record workflow"** (classic side panel). Claude watches your screen and listens to your narration, then saves a *shortcut* (name, prompt, starting URL) that can be scheduled. It covers browser work only and produces a prompt, not a full skill.

**skill-creator**, or describing the job in chat, is the fallback for writing or editing SKILL.md files.

### Cited Findings
**Record a skill (Cowork)**
- "Recording is available on Pro, Max, and Team plans, in Cowork in Claude for Mac. It's not available in chat, on Windows, or on Free and Enterprise plans." — [support.claude.com: How to create custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
- Recording needs the macOS Accessibility and Screen Recording permissions and is limited to about 10 minutes.
- "After you send your recording to Claude, Claude reviews the recording to build the skill. What's saved afterward is a set of screenshots from the session." Video and audio are not kept.
- Claude proposes a new skill or updates to an existing one, which you can Save or Dismiss. The result appears in Customize > Skills.
— [support.claude.com 12512198](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
- Warning: "Don't type passwords or secrets, or display sensitive information or private conversations while recording. Everything on your screen is captured … along with anything you say." — [support.claude.com 12512198](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
- Launch: Anthropic's X account announced "teach Claude a skill … under Record a skill in the + menu of the Claude desktop app. Available on Pro, Max, and Team plans." — [Claude on X](https://x.com/claudeai/status/2079595988998554047)
- The-Decoder dates the launch to 21 July 2026 and notes OpenAI Codex has a similar record-and-replay-as-skill feature. — [The Decoder](https://the-decoder.com/claude-cowork-learns-new-skills-through-screen-recordings-and-voice-over-explanations/)
- Practitioner description: the output is "an editable Skill, not a macro … instructions Claude reasons from, not a click-for-click replay." — [search summary of cybersecuritynews / aqapro guides](https://cybersecuritynews.com/teach-skill-claude/) (secondary source)

**Record workflow (Claude in Chrome)**
- "Click the cursor icon in the menu bar or type / … select 'Record workflow'. Perform the task, clicking, typing, and narrating, while Claude watches your screen and listens to your voice."
- Claude generates "a name, a prompt describing what you did, and the starting URL". It can be scheduled with a chosen frequency and model.
— [Claude Academy](https://academy.claude.com/tutorials/simplify-your-browsing-experience-with-claude-for-chrome)
- The record feature is in the classic side panel and is "not available in Cowork sessions". Claude in Chrome is on Pro, Max, Team and Enterprise. — [support.claude.com 12012173](https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome)
- Third-party (unverified): a June 2026 explainer of "Record Workflow" and its limits exists. — [note.com (kazu)](https://note.com/kazu_t/n/n7a987aa922e7?hl=en)

**Skill files**
- Skills can also be written by hand as a `skill.md` (YAML metadata plus a markdown body, optional resources and scripts) and uploaded as a ZIP. — [support.claude.com 12512198](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)

### Inferences
- **Cowork route:** the owner could record on a **Mac** (if he has one) using Record a skill, then correct the skill in plain English in chat. Whether a Mac-recorded skill becomes available to Cowork on the Windows PC depends on account-level skill sync, which is unverified. On the Windows PC itself, the nearest built-in option is Chrome "Record workflow", for browser-only jobs. Its output (a prompt plus starting URL) can be pasted into a SKILL.md as a first draft.
- **SDK route:** there is no built-in recorder. Build the pipeline in Q8. The Agent SDK can load SKILL.md skills from the agent's folder, so the same artifact works in both routes.
- Both Anthropic features keep screenshots (Record a skill) or depend on narration. That is a confidentiality issue for client tax data (see Q8).

### Gaps
- No Anthropic statement on Windows availability timing for Record a skill.
- Not confirmed whether skills saved via Record a skill on Mac sync to the same account's Windows Cowork.
- No official documentation on how Chrome "Record workflow" handles sensitive fields, or on maximum recording length.

---

## Q7. Third-party tools that capture step-by-step procedures from screen activity (Scribe, Tango, Power Automate Desktop recorder, Windows Steps Recorder) and whether their output can feed playbook generation

### Takeaway
- **Scribe and Tango** auto-capture click-by-click guides with screenshots and can export **Markdown, HTML or PDF on paid plans**. That text plus image output is a good structured input for drafting a SKILL.md.
- **Power Automate Desktop's recorder** captures UI-element selectors and browser actions as automation steps. It is useful for exact field and selector names, but it produces flow actions, not prose.
- **Windows Steps Recorder (psr.exe)** is deprecated (Microsoft Learn lists it as announced Nov 2023), still present, and not recommended for new work.

### Cited Findings
**Scribe / Tango (secondary sources, pricing approximate) [VOLATILE]**
- Scribe exports PDF, Word, HTML and Markdown on Pro. Tango exports PDF, Markdown and HTML (Pro only). "Both require a paid plan to export a portable PDF/HTML/Markdown file." — [search summaries of guidejar / docsie / supered comparisons](https://www.guidejar.com/compare/scribehow-vs-tango) (secondary source)
- Pricing (2026, secondary): Tango Pro about $16/mo vs Scribe Pro about $23–25/mo personal. Team plans are about $13/seat/mo for Scribe (5-seat minimum) and about $15/user/mo for Tango (3-user minimum), billed annually. — [guidde comparison](https://www.guidde.com/tool-comparison/scribe-vs-tango-pricing-comparison); [docsie comparison](https://www.docsie.io/vs/scribe-vs-tango-pricing/) (secondary sources)

**Power Automate for desktop recorder (Microsoft Learn, updated 2026-08-31)**
- "The recorder keeps track of mouse and keyboard activity in relation to UI elements, and it records each action separately … can generate both UI and browser automation actions." When done, steps convert to desktop flow actions, and UI elements are added to the UI elements pane. — [Microsoft Learn: Record desktop flows](https://learn.microsoft.com/en-us/power-automate/desktop-flows/recording-flow)
- It supports UIA and MSAA selectors, can launch or detect Edge, **Chrome**, Firefox or IE, and has custom screens for dropdowns and date pickers. It offers image/OCR-based recording when accessibility APIs are missing. — [Microsoft Learn](https://learn.microsoft.com/en-us/power-automate/desktop-flows/recording-flow)
- Limits: "conditionals and loops can't be recorded"; recordings may contain redundant actions; image-based clicks can land in the wrong place. — [Microsoft Learn](https://learn.microsoft.com/en-us/power-automate/desktop-flows/recording-flow)

**Windows Steps Recorder**
- Microsoft Learn deprecated-features table (page updated Sept 2026): "Steps Recorder (psr.exe): Steps Recorder is no longer being updated and will be removed in a future release of Windows. For screen recording, we recommend the Snipping Tool, Xbox Game Bar, or Microsoft Clipchamp." Announced: **November 2023**. — [Microsoft Learn: Deprecated features](https://learn.microsoft.com/en-us/windows/whats-new/deprecated-features)
- Date conflict: several secondary sources say February 2024 (likely when it was widely reported). — [Neowin](https://www.neowin.net/news/microsoft-deprecates-even-more-windows-features-steps-recorder-gets-the-axe/); [usewhale](https://usewhale.io/blog/microsoft-steps-recorder/)
- As of 2026, psr.exe still opens on current Windows 11 builds with a removal banner, and no removal date is published. — [rottenwifi / vidocu summaries](https://vidocu.ai/blog/windows-steps-recorder-is-deprecated-what-replaces-it-in-2026) (secondary source)
- An open-source "BetterStepsRecorder" exists as a modern PSR replacement. — [GitHub: Bunbob41/BetterStepsRecorder](https://github.com/Bunbob41/BetterStepsRecorder)

### Inferences
- **Best feed for SKILL.md generation:** a Scribe or Tango Markdown export, since it already has numbered steps, URLs and field labels drawn from the DOM, plus screenshots. Combine it with the owner's narrated audio transcribed by Whisper. Claude then turns "what" (Scribe steps) and "why" (narration) into a playbook with decision rules.
- Power Automate Desktop output is most useful as a *reference* for exact selectors and field names, not as the playbook itself.
- **Data residency:** Scribe and Tango are cloud services, so client screenshots go to a third party. Use their redaction features or a dummy client.
- Steps Recorder: do not build on it.

### Gaps
- Scribe and Tango export details and prices come from comparison sites, not official pricing pages. Check them before purchase.
- Not checked: whether Scribe or Tango capture desktop (non-browser) apps on Windows on lower tiers, and their sensitive-data auto-redaction features.
- Not checked: whether Power Automate for desktop is free on Windows 11 for attended use (widely believed, not confirmed here).
- Claudia (claudiasop.com), a "browser workflow recorder for Claude Cowork", was not evaluated.

---

## Q8. Recommended teach-by-recording pipeline and pitfalls (URLs, field names and click targets vs. screenshots; sensitive data in recordings)

### Takeaway
Capture **structured events** (URL, page title, element label or selector, typed-value placeholder, click timestamp) alongside **event-triggered screenshots** and a **Whisper transcript of the narration**. Have Claude draft SKILL.md from that bundle. Then the owner corrects it in plain English and runs it in a supervised dry run.

Screenshots alone lose exact field names and transient states. Treat recordings of client data as sensitive. Use a dummy client or redact before anything leaves the PC.

### Cited Findings
- Anthropic's own recorder keeps "a set of screenshots" after processing, not the video, and warns that everything on screen and anything said is captured. — [support.claude.com 12512198](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
- Chrome Record workflow captures the starting URL as part of the generated shortcut. — [Claude Academy](https://academy.claude.com/tutorials/simplify-your-browsing-experience-with-claude-for-chrome)
- Power Automate Desktop records actions "in relation to UI elements" (UIA/MSAA selectors) and browser actions, showing that element-level capture is possible on Windows. — [Microsoft Learn](https://learn.microsoft.com/en-us/power-automate/desktop-flows/recording-flow)
- Frame sampling misses changes between frames; a 5-minute video costs about 50–80K tokens. — [ClaudeCamp](https://claudecamp.ai/blog/claude-code-video-processing)
- Claude may misread low-quality or small images; coordinates are approximate; JPEG compression can make text unreadable. — [platform.claude.com: Vision](https://platform.claude.com/docs/en/build-with-claude/vision)
- The Files API is recommended for many images to keep payloads small. — [platform.claude.com: Vision](https://platform.claude.com/docs/en/build-with-claude/vision)
- Anthropic does not train on uploaded images. — [platform.claude.com: Vision FAQ](https://platform.claude.com/docs/en/build-with-claude/vision)

### Inferences
**Pipeline for the SDK route on Windows** (cost and effort are my estimates)
1. **Capture**, using any one of:
   - (a) OBS or the Snipping Tool screen recording (video plus microphone), plus a small Chrome extension or CDP logger that writes `{t, url, title, action, element_label/aria/name, selector}` for each click and input; or
   - (b) Scribe/Tango in the browser, plus a phone or PC voice memo; or
   - (c) Claude in Chrome Record workflow for browser-only jobs.
2. **Extract:**
   - ffmpeg frames at each logged event timestamp (plus about 1 fps during idle periods), downscaled to ≤1568–2000 px;
   - Whisper (local faster-whisper on the PC, so audio stays on-prem) for the timestamped transcript.
3. **Redact:**
   - blur known PII regions (SSN, EIN, bank numbers) or use a test client;
   - replace typed values in the event log with placeholders such as `{client_EIN}`.
4. **Draft:** send Claude the event log, the transcript and labelled frames (Files API). Ask it for SKILL.md with:
   - purpose;
   - inputs;
   - step list (URL → field label → value source);
   - decision rules taken from the narration;
   - "STOP and request approval" markers before any irreversible step;
   - verification checks;
   - known failure modes.
5. **Correct:** the owner reviews in plain English ("step 7 is wrong, use the Q3 workbook tab") and Claude edits SKILL.md, using skill-creator or chat.
6. **Dry run:** run the skill in supervised mode with the approval gate on every step. Then narrow the gates to irreversible steps only.

**Pitfalls**
- **Narration matters most.** The screen shows *what*; the voice explains *why* and the exceptions. Ask the owner to say the decision rules aloud ("if the balance is under $500 we skip…").
- **Exact field names and URLs** should come from the DOM or UIA log, not OCR. Portals change layouts, so the skill should describe targets by label and purpose, not by coordinates.
- **One recording is one path.** Exceptions (e.g., a portal error) are never shown, so ask Claude to list the questions it still has after drafting.
- **Sensitive data:** an accounting recording will show SSNs, EINs, bank accounts and credentials. Use test data. Never type passwords on camera. Keep transcription local. Remember that Anthropic's Record a skill keeps screenshots in the Cowork task.
- **Under the Cowork route on Windows**, Record a skill is unavailable today (Mac only). The fallback is Chrome Record workflow (browser only), or a manual "describe the job in chat plus attach screenshots" flow.

### Gaps
- No published end-to-end accuracy results were found for demo-to-SKILL.md generation, from Anthropic or third parties.
- No firm-specific guidance was found on IRS Pub 4557 / FTC Safeguards Rule implications of sending screen recordings that contain taxpayer data to AI vendors. A compliance researcher should cover this.
