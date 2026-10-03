# Claude Cowork as a platform for scheduled, unattended desktop agents on a dedicated Windows PC (state as of 3 Oct 2026)

Research date: 2026-10-03. Most official pages carry a "last updated" stamp, given in brackets after each claim. The platform is changing week to week. A large change is set for **6 Oct 2026**, three days after this research: new Cowork tasks on Pro and Max plans move to the cloud, and the "Only on your computer" option is removed. Re-check anything marked (VOLATILE) before deciding.

## 1. Scheduled tasks / Routines in Cowork: name, creation, where they run, machine state, missed runs, interval, triggers

### Takeaway
The Cowork feature is officially called **"Scheduled tasks"**. The Code tab of the desktop app calls its page **"Routines"**, and that page holds "local scheduled tasks" and cloud "routines". From 6 Oct 2026, Cowork scheduled tasks on Pro and Max run **in Anthropic's cloud**. They reach a Windows PC's folders, browser or screen only through the Claude Desktop app, and only while it is open and online. Cowork itself offers no file or email triggers: tasks run on a clock or by hand. The only documented setup where a task runs truly on one machine is the **Claude Code Desktop local scheduled task** (Code tab). It needs the app open and the PC awake. Missed runs are skipped, with a single catch-up run on wake.

### Cited Findings
**Name and creation**
- The feature is "Scheduled tasks". They are available on all paid plans (Pro, Max, Team, Enterprise), in Cowork and in the "new Claude experience" now reaching Pro and Max [updated 2026-09-29] — [Schedule recurring tasks in Claude Cowork](https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork)
- There are three ways to create one [2026-09-29] — [Schedule recurring tasks](https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork); you can also type `/schedule` in any Cowork task — [Get started with Claude Cowork](https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork) [2026-09-30]:
  - **New Claude experience:** describe the task and its cadence in any conversation, then click "Schedule".
  - **Create with Claude:** Scheduled → New task → "Create with Claude".
  - **Set up manually:** fill in task name, prompt, **approval mode**, frequency (hourly, daily, weekly, weekdays or manual), an optional model and an optional folder.
- Cadence presets are hourly, daily, weekdays, weekly and manual (on demand) [2026-09-29] — [Schedule recurring tasks](https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork). A July 2026 reviewer notes there is no monthly preset — [AI Blew My Mind, 9 Jul 2026](https://aiblewmymind.substack.com/p/claude-cowork-cloud-scheduled-tasks) (secondary).
- Custom cron expressions for local routines were added on 2026-06-25. A fix on 2026-08-25 made "1st of month and every Monday"-style schedules run on either day — [Claude Desktop changelog](https://claude.com/docs/cowork/changelog)

**Where they run (VOLATILE: 6 Oct 2026)**
- The help article currently says: "Scheduled tasks run remotely, so they run on their cadence even when your computer is asleep or the Claude Desktop app is closed." It also says: "They can't be tied to a folder on your computer." Yet the manual form still offers "Which folder Claude should work in (optional)", with the note "If a scheduled task requires local files or apps, it will only run locally." The article contradicts itself mid-transition [2026-09-29] — [Schedule recurring tasks](https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork)
- Official notice [2026-09-30] — [Use Claude Cowork on web, desktop, and mobile](https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile):
  - "On October 6, 2026, new Cowork tasks on Pro and Max plans run in the cloud. The Only on your computer option in Settings > General will be removed."
  - "Your scheduled tasks move to the cloud too, including ones that use files on your computer. Tasks that use files on your computer need the desktop app open."
- The same notice says that if you want tasks to run on your computer, "Claude Code in the desktop app runs on your computer and keeps your folders and history there… Your projects and scheduled tasks don't carry over to Claude Code." [2026-09-30] — [same article](https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile)
- Local file access, local connectors, browser use and computer use all need "the Claude Desktop app open on your machine, even when your session runs in the cloud." "If the app is closed, the session keeps running but can't reach your local files." [2026-09-30] — [same article](https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile)
- On Team and Enterprise, the "Cowork and chat are one Claude" merge is not happening yet: they "keep chat and Claude Cowork as they are today". Cowork sessions there can run in two places, "Sessions in the cloud (beta)" or "Local sessions". "Run Cowork in the cloud" is on by default for Team and off by default for Enterprise [2026-09-25] — [Use Claude Cowork on Team and Enterprise plans](https://support.claude.com/en/articles/13455879)
- The app has been automatically moving scheduled tasks to the cloud for some accounts. A 2026-09-11 change made it wait about a minute after the computer wakes before trying. A "Move to cloud" action exists on tasks (fix dated 2026-09-24) — [Claude Desktop changelog](https://claude.com/docs/cowork/changelog)

**Device-bound ("Require this computer") tasks**
- A task-form toggle called **"Require this computer (Claude Desktop (macOS))"** exists. Its help text reads: "Only runs while your computer is awake. Gives Claude access to the folders you've allowed on this computer and to Claude in Chrome." Such tasks show a grey "Requires this computer" or an orange "Only on this computer" badge. Agent-created tasks (made through the `create_trigger` tool) cannot be device-bound; they silently become cloud-only ("not bound: no_signed_approval — this task will run in the cloud only"), and the toggle cannot be turned on afterwards. (Bug report, opened 2026-09-05, still open, macOS) — [GitHub issue #92268](https://github.com/anthropics/claude-code/issues/92268)
- On Windows, device-bound scheduled tasks exist, but one user cannot save any change to them. The error is "Sign in again on this computer, then save your changes again", and it survives re-login and reboot. The report links other open issues (opened 2026-09-26, open, has repro): device sessions force-logged-out every 24–36 hours (#81512), a device key not persisting on Windows 11 (#77596), and a daily forced re-login with frozen task runs (#95963) — [GitHub issue #97341](https://github.com/anthropics/claude-code/issues/97341)
- A July 2026 reviewer found that picking a local folder in the form switches the task to "run only on your computer while it's awake and online". If the laptop is asleep, "the task won't start" — [AI Blew My Mind, 9 Jul 2026](https://aiblewmymind.substack.com/p/claude-cowork-cloud-scheduled-tasks) (secondary)

**Machine state, sleep and missed runs (Claude Code Desktop local scheduled tasks, the documented on-machine path after 6 Oct)**
- These tasks are created from Code tab → Routines → New routine → Local. "Local task runs on your machine… but only fires while the app is open and your computer is awake." — [Schedule recurring tasks in Claude Code Desktop](https://code.claude.com/docs/en/desktop-scheduled-tasks)
- "If your computer sleeps through a scheduled time, the run is skipped." A **Keep computer awake** setting prevents idle sleep. On wake or app start, the app "starts exactly one catch-up run for the most recently missed time" within the last 7 days and discards older ones. "A task scheduled for 9am might run at 11pm." — [same doc](https://code.claude.com/docs/en/desktop-scheduled-tasks)
- The app checks schedules every minute and adds a fixed delay of "a few minutes" to stagger traffic. Minimum interval: **1 minute for Desktop local tasks, 1 hour for cloud routines** — [same doc](https://code.claude.com/docs/en/desktop-scheduled-tasks)
- Local scheduled tasks reached the Code tab on 2026-09-02, "matching what Cowork already offered" — [Claude Desktop changelog](https://claude.com/docs/cowork/changelog)
- Sleep-related fixes in the changelog — [Claude Desktop changelog](https://claude.com/docs/cowork/changelog):
  - 2026-09-04: automatic re-runs after 5, 15 and 30 minutes when a task cannot reach the model, for example right after a wake behind a VPN.
  - 2026-08-27: tasks "that run on this computer occasionally being marked as skipped without running".
  - 2026-06-11: duplicate runs firing on wake.

**Triggers**
- None of the Cowork scheduled-task articles mention any trigger other than time or manual runs [2026-09-29] — [Schedule recurring tasks](https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork)
- Claude Code cloud **routines** "can also fire on API calls or GitHub events". Desktop local tasks run on a clock only — [Schedule recurring tasks in Claude Code Desktop](https://code.claude.com/docs/en/desktop-scheduled-tasks)

### Inferences
- The candidate design ("a scheduled task bound to that PC") is being retired for Pro and Max in Cowork on 6 Oct 2026. After that, a Cowork scheduled task runs in the cloud and reaches into the PC through the desktop app. It works only if the app stays open and signed in. Anthropic's own advice for "work [that] has to stay on one machine" is Claude Code Desktop rather than Cowork.
- No documented "file arrives" or "email arrives" trigger exists in Cowork. The workarounds are polling (an hourly task that checks a folder or inbox) or an external trigger calling a cloud routine through the API. A routine cannot directly drive the local screen.
- On a dedicated always-on PC, the sleep problems go away (set Windows to never sleep and turn on Keep awake). The re-login and device-key problems in #97341 and its linked issues are the bigger reliability risk for an unattended box.

### Gaps
- No official doc says whether a cloud-run Cowork scheduled task, after 6 Oct, can use **computer use** or **Claude in Chrome** on the PC with nobody present. The docs cover folders. The device-bound toggle text mentions folders and Claude in Chrome but not computer use.
- No doc says how Windows lock-screen or logged-out states affect runs.
- No official minimum interval is given for Cowork (as opposed to Code-tab) scheduled tasks.
- The "Require this computer (Claude Desktop (macOS))" label comes from a macOS report. It is unconfirmed whether Windows shows the same toggle after 6 Oct, or whether it survives the change at all.

## 2. Computer use in the desktop app on Windows: enabling it, per-app approvals, persistence, app tiers

### Takeaway
Computer use works on Windows. It is enabled through one toggle in Settings > General and is a beta for **Pro and Max only, not Team or Enterprise**. Per-app access is approved **per session**: "Allow for this session" or "Deny", with no documented "always allow". A new scheduled-task run is a new session. As documented, an unattended 9 a.m. run that needs a desktop app would therefore hit an approval prompt with nobody there to click it. The app tiers are fixed: browsers view-only, terminals and IDEs click-only, everything else full control.

### Cited Findings
- "Computer use is in beta for Pro and Max plans. It's available in Cowork and Claude Code in the Claude Desktop application for both macOS and Windows." "Team and Enterprise plans don't have access to computer use at this time." [2026-09-16] — [Let Claude use your computer in Cowork](https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork). Confirmed in the Claude Code docs: "not available on Team or Enterprise plans" — [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop)
- To enable: Settings > General (under Desktop app) → **Enable computer use** toggle. "On Windows, the toggle takes effect immediately and setup is complete." macOS also needs Accessibility and Screen Recording permissions — [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop); [Let Claude use your computer](https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork) [2026-09-16]
- Approval flow: "The first time Claude needs to use an app, a prompt appears in your session. Click **Allow for this session** or **Deny**. Approvals last for the current session, or 30 minutes in Dispatch-spawned sessions." — [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop)
- Tiers "are fixed by app category and can't be changed" — [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop):
  - **View only**: browsers and trading platforms.
  - **Click only**: terminals and IDEs.
  - **Full control**: everything else.
  - File Explorer and Settings show an extra warning.
  - A **Denied apps** list exists.
  - When not running in the background, Claude hides your other windows while it works.
- Background (non-takeover) mode is the default on **macOS 15+ only**. "Claude asks for your permission the first time a task needs the full screen in each session before taking over." [2026-09-16] — [Let Claude use your computer](https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork)
- Requirements: "Your computer needs to be awake and the Claude Desktop app needs to be open for computer use to work." [2026-09-16] — [same article](https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork)
- Investment, trading and crypto apps are blocked by default. Claude "is trained to avoid risky operations—like transferring funds, modifying or deleting files, or handling sensitive data", but "these safeguards aren't perfect". Anthropic recommends: "Do not give computer use permission access to sensitive apps (such as banking, healthcare, government)." It advises against "Managing financial accounts" and "Interacting with apps containing personal information of others" [2026-09-16] — [same article](https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork)
- "Computer use has no sandbox between Claude and your applications." [2026-09-16] — [same article](https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork)
- Windows availability was announced by Anthropic around early April 2026 ("Computer use in Claude Cowork and Claude Code Desktop is now available on Windows") — [Claude on X](https://x.com/claudeai/status/2039836891508261106); [Thurrott](https://www.thurrott.com/a-i/anthropic/334498/anthropic-brings-claude-computer-use-to-windows) (exact date not verified from the primary page)
- A "Computer Use teach mode" exists. A 2026-07-02 fix covers its Next and Exit buttons and screen-edge glow — [Claude Desktop changelog](https://claude.com/docs/cowork/changelog)
- Anecdotal, macOS: when computer use's `request_access` raises a native macOS dialog, you "must be physically at their Mac to approve within the 60-second timeout". The reporter said Windows was not affected (closed as duplicate, opened 2026-04-02) — [GitHub issue #42693](https://github.com/anthropics/claude-code/issues/42693)
- Fix dated 2026-09-15: "browser, computer use, and website access permission prompts in Dispatch sometimes being denied on their own before you could answer" — [Claude Desktop changelog](https://claude.com/docs/cowork/changelog)

### Inferences
- If the firm is on a **Team or Enterprise** plan, computer use is not available at all. It would have to run each agent under an individual Pro or Max seat. That may conflict with firm-wide admin control and data-handling expectations.
- Per-session app approvals are a hard blocker for a run that must click into a desktop app (QuickBooks Desktop, a tax-software client, Excel) with nobody present. Every scheduled run starts a fresh session, and nothing documents a persistent per-app grant for computer use. The one exception is Dispatch, whose approvals last 30 minutes, but Dispatch closed to new users from Sept 2026.
- On Windows, computer use takes over the whole screen. That suits a dedicated PC, but only one screen-driving task can work at a time (see section 6).
- Anthropic's own guidance tells users not to point computer use at banking or government apps. That covers much of the firm's planned portal work (IRS and state portals, payroll).

### Gaps
- Docs do not say whether "Automatically approve" or "Skip all approvals" mode skips the per-app computer-use prompt. The tiers are described as fixed, and the per-app prompt is described separately from the approval modes.
- Docs do not say whether computer use works while Windows is locked, at the lock screen, or in a disconnected RDP session.
- No official Windows launch date was confirmed from a primary page.

## 3. Claude in Chrome (and the built-in browser): unattended use, real profile and logins, password manager, per-site permissions, money and password policy, CAPTCHA and MFA

### Takeaway
Claude in Chrome drives the user's **real Chrome profile and shares its login state**. Per-site "always allow" grants persist in the extension settings. Several protections apply **regardless of permission mode**:
- Making purchases or financial transactions is **prohibited**.
- Entering sensitive information always needs explicit approval.
- Bypassing CAPTCHAs is prohibited.
- Claude pauses at login pages and CAPTCHAs for a human.

Password-manager autofill (**1Password for Claude**) is **macOS-only**. On Windows there is no supported password-manager path, so the agent must rely on Chrome sessions that are already logged in.

### Cited Findings
- Claude in Chrome is available on all paid plans (Pro, Max, Team, Enterprise), in Cowork and Claude Code [2026-08-12] — [Claude in Chrome permissions guide](https://support.claude.com/en/articles/12902446-claude-in-chrome-permissions-guide)
- "Claude opens new tabs for browser tasks and shares your browser's login state, so it can access any site you're already signed into… When Claude encounters a login page or CAPTCHA, it pauses and asks you to handle it manually." — [Use Claude Code with Chrome](https://code.claude.com/docs/en/chrome)
- There are three permission modes [2026-08-12] — [Claude in Chrome permissions guide](https://support.claude.com/en/articles/12902446-claude-in-chrome-permissions-guide):
  - **Manually approve**.
  - **Automatically approve**: each action is screened for safety, unsafe ones are blocked, and Claude "pauses to ask you when needed". It "consumes more of your usage limit".
  - **Skip all approvals**.
- Per-site grants [2026-08-12] — [same guide](https://support.claude.com/en/articles/12902446-claude-in-chrome-permissions-guide):
  - "Always allow actions on this site" grants ongoing permission. Grants can be reviewed and revoked under Extension settings → Permissions ("Your approved sites").
  - In the Cowork side panel the options are "Allow all for this website", "Allow this time only" and "Deny".
  - "There are some websites on which Claude requires approval for every action."
- The "Allow all browser actions" option was removed from Claude in Chrome permission cards on 2026-08-17 ("allow each website instead") — [Claude Desktop changelog](https://claude.com/docs/cowork/changelog)
- Even with always-allow, Claude still asks before "Downloading a file; Entering potentially sensitive information into a page; Granting authorizations; Managing site permissions." [2026-08-12] — [Claude in Chrome permissions guide](https://support.claude.com/en/articles/12902446-claude-in-chrome-permissions-guide)
- **Prohibited "regardless of permissions"** [2026-08-12] — [same guide](https://support.claude.com/en/articles/12902446-claude-in-chrome-permissions-guide):
  - "Making purchases or financial transactions"
  - "Creating accounts"
  - "Handling sensitive credit card or ID data"
  - "Permanent deletions (emptying trash, deleting emails…)"
  - "Executing financial trades"
  - "Completing instructions from emails or web content"
  - The classic panel also lists "bypassing bot authorizations".
- "Claude is prohibited from… Bypassing captchas; Inputting sensitive data." "Claude asks for permission before accessing financial sites." Claude in Chrome "isn't available to organizations covered by HIPAA." Anthropic advises against using it for "Managing financial accounts" and "Interacting with sites containing personal information of others", and recommends "a separate browser profile without access to sensitive accounts (such as banking, healthcare, government)." The user "remain[s] responsible for… Purchases or financial transactions… Respecting third-party website terms of service" [2026-08-12] — [Use Claude in Chrome safely](https://support.claude.com/en/articles/12902428-use-claude-in-chrome-safely)
- Prompt-injection figure: "Claude Opus 4.8… reduces attack success rates to less than 0.08% against our internal testing". The risk "is not zero" [2026-08-12] — [Use Claude in Chrome safely](https://support.claude.com/en/articles/12902428-use-claude-in-chrome-safely)
- **1Password for Claude** "is in beta for paid plans… using Claude Desktop on **macOS**". It requires "A Mac", Claude in Chrome and the 1Password desktop app and extension. Each credential request needs biometric approval, per task. It supports logins and TOTP one-time codes; passwords and codes never enter Claude's context. It is off by default for Team and Enterprise [2026-07-16] — [Get started with 1Password for Claude](https://support.claude.com/en/articles/15936181-get-started-with-1password-for-claude)
- Built-in browser (alternative to Chrome) [2026-09-16] — [Use the built-in browser in Claude Cowork](https://support.claude.com/en/articles/16607400-use-the-built-in-browser-in-claude-cowork):
  - Rolling out on macOS, Windows and Linux.
  - "Claude remembers your logins across Cowork sessions."
  - Cookie import is "from Chrome, Edge, and Firefox on macOS, and from **Firefox on Windows**". "Banking, email, and single sign-on sites stay unchecked by default."
  - Needs the desktop app open and online.
  - "Claude asks for your permission before acting on a site for the first time."
  - Anthropic "strongly advise[s] against" using it for financial accounts.
- Scheduling inside the extension: the Chrome side panel has its own scheduled "shortcuts" (daily, weekly, monthly or annually). A classic-panel "record a workflow" feature lets Claude learn a browser workflow, but "Recording isn't available when the side panel runs as a Cowork session." Notifications can alert "when Claude requires permission or completes a task" [2026-08-26] — [Get started with Claude in Chrome](https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome)
- If the preferred browser is Claude in Chrome, "tasks on web or mobile use the extension directly; your session needs to be connected to a desktop, but the app doesn't have to be open." [2026-09-16] — [Use the built-in browser](https://support.claude.com/en/articles/16607400-use-the-built-in-browser-in-claude-cowork)
- Team and Enterprise admins can set site allowlists and blocklists and an org-wide on/off for Claude in Chrome and the built-in browser [2026-09-25] — [Cowork on Team and Enterprise](https://support.claude.com/en/articles/13455879)

### Inferences
- **"Approve payroll" / "Submit payment" / e-file submit:** by policy Claude is prohibited from "purchases or financial transactions" in any mode. So the firm's "pause, phone approval, then Claude continues" pattern likely cannot end with Claude clicking the money-moving button. A human would have to do that final click. It is unconfirmed whether payroll approval or e-filing counts as a "financial transaction" under the classifier; behaviour may vary by site.
- **MFA:** Claude stops at login pages and CAPTCHAs, and on Windows no password manager is supported. An unattended run can work only while the Chrome profile's sessions are still logged in. Portals that time out sessions daily or demand MFA at each login (payroll, IRS e-Services and state tax portals usually do) will stall until a human logs in.
- **Typing data:** "Inputting potentially sensitive information" needs explicit permission in every mode. Tax IDs, SSNs and bank details are exactly the data the firm's agents would enter, so expect frequent approval stops, or refusals ("Handling sensitive… ID data" is prohibited).
- Per-site "always allow" grants persist, which helps unattended runs on low-risk sites. Financial and government sites may still need per-action approval.

### Gaps
- No official statement lists which specific sites (IRS, state DOR, ADP, Gusto and so on) are on Anthropic's "financial / requires approval for every action" lists.
- No documentation covers SMS or email OTP handling beyond 1Password TOTP on macOS.
- It is unconfirmed whether a cloud-run scheduled task can drive Claude in Chrome on a PC where nobody is logged into Windows.

## 4. Skills and plugins in Cowork: private playbooks, scripts, recording a skill

### Takeaway
Yes. A firm can write **private skills**: folders with a `SKILL.md` plus scripts and resources. They are enabled per Claude account, shared across chat, Cowork and Code, and available to scheduled tasks. Team and Enterprise owners can distribute them through plugin marketplaces. A built-in **"Record a skill"** feature (Pro, Max, Team) turns a narrated screen recording into a skill.

### Cited Findings
- "Skills are directories containing instructions, scripts, and resources that Claude dynamically loads". They "run in Claude's code sandbox, so **Code execution and file creation** must be on". The groups shown are "Created by you", "From your organization", "Shared with you", and Anthropic & Partners. Skills you upload "aren't reviewed by Anthropic" — [Skills overview](https://claude.com/docs/skills/overview); how to write SKILL.md, add scripts and package a skill: [Create custom skills](https://claude.com/docs/skills/how-to)
- "Scheduled tasks have access to the same capabilities as regular Cowork tasks, including connected tools, skills, and installed plugins." [2026-09-29] — [Schedule recurring tasks](https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork)
- Cowork "loads the ones enabled for your claude.ai account, synced at session start, and doesn't read the Claude Code CLI's `~/.claude` directory" — [Cowork overview](https://claude.com/docs/cowork/overview)
- Team and Enterprise owners can create plugin marketplaces and mark plugins "Installed by default / Available / Required / Not available" [2026-09-25] — [Cowork on Team and Enterprise](https://support.claude.com/en/articles/13455879); see also [Manage plugins for your organization](https://claude.com/docs/plugins/admin)
- **Record a skill**: "Record your screen while you do a task, talk through it as you go, and Claude turns it into a skill it can run again. Find it under Record a skill in the + menu of the Claude desktop app. Available on Pro, Max, and Team plans." (Anthropic, about July 2026) — [Claude on X](https://x.com/claudeai/status/2079595988998554047); coverage: [The Decoder](https://the-decoder.com/claude-cowork-learns-new-skills-through-screen-recordings-and-voice-over-explanations/), [Android Headlines, Jul 2026](https://www.androidheadlines.com/2026/07/claude-cowork-record-a-skill-screen-recording-feature.html)
- Windows support for Record a skill is implied by a 2026-09-04 fix: "Fixed Record a skill opening an unresponsive chooser window on Windows." — [Claude Desktop changelog](https://claude.com/docs/cowork/changelog)
- Code-tab local scheduled tasks store their prompt as `~/.claude/scheduled-tasks/<task-name>/SKILL.md`. A task can change its own schedule or prompt through the `update_scheduled_task` tool — [Schedule recurring tasks in Claude Code Desktop](https://code.claude.com/docs/en/desktop-scheduled-tasks)

### Inferences
- The "playbook as a skill" part of the design is well supported. Recording Roy's portal routine with Record a skill and then editing the resulting SKILL.md is a realistic way to draft playbooks.
- Skills run in Claude's code sandbox, which is cloud-side for cloud sessions. Scripts in a skill run there, not on the Windows PC, unless the session is local or Code-tab.

### Gaps
- No official help-center page for "Record a skill" was found (sources are the Anthropic X post and the press). Its limits (length, apps captured, Enterprise availability) are unverified.

## 5. Notifications and approvals from a phone

### Takeaway
Cloud Cowork sessions send a **push notification to the phone** when a task finishes or needs input. They can be opened and answered from Claude Mobile. **Dispatch**, the phone-to-desktop pairing, has push notifications and forwarded approvals, but it is **closed to new users** and Pro/Max-only. How long a task waits depends on the surface:
- Dispatch denies unanswered prompts after **10 minutes**.
- Code-tab local scheduled tasks in Manual mode **stall until answered**.
- The 2026-10-01 default for Claude-created scheduled tasks is "Automatically approve", which pauses only when something looks unsafe.

### Cited Findings
- "When Claude finishes a task or needs your input, you'll get a notification on your phone." You can "Open the same session from another surface to check progress, answer Claude's questions, or redirect the work." [2026-09-30] — [Use Claude Cowork on web, desktop, and mobile](https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile)
- "A task you start at your desk shows up in Claude Mobile too, so you can see how it's going, answer questions from Claude, and redirect the work from anywhere." [2026-09-16] — [Claude Cowork and chat are one Claude](https://support.claude.com/en/articles/16761823)
- Dispatch [2026-09-16] — [Dispatch help article](https://support.claude.com/en/articles/13947068):
  - "You'll get a push notification on your phone when a task is done or when Claude needs your go-ahead."
  - The computer must be awake with the desktop app open (macOS, Windows x64, Linux).
  - It runs as one continuous thread.
  - **"Dispatch isn't available to new users. If you already use Dispatch, you can keep using it for now."**
  - "Dispatch is only available for some Pro and Max plans."
- "When a child task needs permission… the prompt is forwarded to you. If you don't respond within ten minutes, the request is automatically denied and the task continues without that action." — [Run tasks in the background with Dispatch (docs)](https://claude.com/docs/cowork/guide/dispatch)
- Dispatch "requires a Pro or Max plan and is not available on Team or Enterprise plans." — [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop)
- Code-tab local scheduled tasks — [Schedule recurring tasks in Claude Code Desktop](https://code.claude.com/docs/en/desktop-scheduled-tasks):
  - In Manual mode, a tool without permission makes "the run stall… until you approve it. The session stays open in the sidebar so you can answer later."
  - "Run now" then "always allow" saves tool approvals for future runs.
  - MCP tools marked `requiresUserInteraction` "prompt on every call… Runs that call these tools stall each time."
  - A desktop (OS) notification fires when a task starts.
- Changelog — [Claude Desktop changelog](https://claude.com/docs/cowork/changelog):
  - 2026-10-01: "Changed scheduled tasks that Claude creates for you to use 'Automatically approve' by default where your organization allows it, so their runs use tools without asking first and pause only when something looks unsafe."
  - 2026-08-04: an "Allow for all scheduled runs" option on approval prompts.
  - 2026-09-15: a "Scheduled task failed" notification now appears when a task could not start.
- "Remote Control" (driving a desktop session from another device) asks for approval before terminal commands "only when the work was started or steered from another device" (2026-09-22) — [Claude Desktop changelog](https://claude.com/docs/cowork/changelog)
- Anecdotal (April 2026, macOS): a request for push-notified remote approval of computer-use access dialogs, closed as duplicate — [GitHub issue #42693](https://github.com/anthropics/claude-code/issues/42693)

### Inferences
- The owner's "pause → phone notification → approve → continue" flow works natively only for **Cowork-level prompts in cloud sessions** (connector or tool approvals, questions). Computer-use per-app prompts and Chrome "sensitive input" prompts likely surface the same way, but this is not documented. Money-moving clicks are prohibited outright, so "approve on phone, then Claude clicks Submit" is not a supported path.
- No custom approval policy can be defined (for example "pause only before steps tagged irreversible"). Only built-in modes exist (Manual / Auto / Skip), plus Claude's own safety classifier and whatever the skill's instructions tell Claude to ask.

### Gaps
- No documented maximum wait for a cloud Cowork task that "needs your input". Dispatch has a 10-minute auto-deny; Code-tab local tasks stall without limit.
- No documentation says whether phone notifications fire for **scheduled** runs specifically, as opposed to interactive tasks.
- No email notification option was found.

## 6. Concurrency: two scheduled tasks needing the screen at once

### Takeaway
Nothing documents queueing of screen-driving tasks. For Code-tab local scheduled tasks, overlapping runs are **skipped, not queued**: the history shows a run skipped because "the previous run was still in progress, or other scheduled tasks were already running". On Windows, computer use takes over the screen, so two screen-driving agents on one PC would collide.

### Cited Findings
- Skipped-run reasons in task history: "your computer was asleep, the previous run was still in progress, or other scheduled tasks were already running." — [Schedule recurring tasks in Claude Code Desktop](https://code.claude.com/docs/en/desktop-scheduled-tasks)
- Desktop "starts a fresh session when a task is due, independent of any manual sessions you have open." — [same doc](https://code.claude.com/docs/en/desktop-scheduled-tasks)
- Background (non-takeover) computer use is macOS 15+ only. Elsewhere, Claude "hides your other windows while it works so it interacts with only the approved app." — [Let Claude use your computer](https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork) [2026-09-16]; [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop)
- Users "can have several tasks running at the same time" in the new Claude experience (cloud) [2026-09-16] — [Claude Cowork and chat are one Claude](https://support.claude.com/en/articles/16761823)
- A 2026-07-21 fix covers "bash commands failing when several subtasks ran them at once" in the Cowork workspace — [Claude Desktop changelog](https://claude.com/docs/cowork/changelog)

### Inferences
- Several agents (Roy plus others) on one Windows PC would need staggered schedules. Otherwise later runs may be silently skipped (Code-tab tasks) or fight over mouse and keyboard (cloud tasks reaching into the PC). Cloud tasks that only use connectors can run in parallel without trouble.

### Gaps
- No official statement covers whether Cowork (as opposed to Code-tab) local or cloud scheduled tasks that both need computer use on the same PC are serialized, queued or allowed to collide.

## 7. Logs and audit: what each run leaves behind

### Takeaway
Each run is its own session with a full transcript (steps, tool calls, produced files), reviewable from the "Scheduled" page. Screenshots from computer use and connected browsers are saved to the task folder. Team and Enterprise get OpenTelemetry export and Compliance API coverage. Individual Pro and Max plans have no admin-grade audit trail.

### Cited Findings
- "Each scheduled task runs as its own Cowork session." You can "Review upcoming and past runs" from "Scheduled" in the sidebar [2026-09-29] — [Schedule recurring tasks](https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork)
- "Select any task to open its full transcript, the steps Claude took, and any files it produced." — [Dispatch docs](https://claude.com/docs/cowork/guide/dispatch)
- 2026-07-14 fix: "screenshots from connected browsers and computer use not being saved to the task folder." This implies screenshots are meant to be saved there — [Claude Desktop changelog](https://claude.com/docs/cowork/changelog)
- Code-tab tasks: "Review history: see every past run, including skipped runs" with skip reasons, plus a per-task "Always allowed" panel — [Schedule recurring tasks in Claude Code Desktop](https://code.claude.com/docs/en/desktop-scheduled-tasks)
- OpenTelemetry export (Team and Enterprise) [2026-09-25] — [Cowork on Team and Enterprise](https://support.claude.com/en/articles/13455879); [Monitoring](https://claude.com/docs/cowork/monitoring):
  - Events: `user_prompt`, `assistant_response`, `tool_result` (with `tool_input`, truncated about 4K) and `api_request`.
  - It covers "tool calls, file access, human approval decisions". It "doesn't replace audit logging for compliance purposes".
  - Content is captured only if enabled.
- Compliance API captures Cowork sessions. Local-session history is stored on the user's computer, "not subject to Anthropic's standard data retention policies", and admins cannot centrally delete it [2026-09-25] — [Cowork on Team and Enterprise](https://support.claude.com/en/articles/13455879)

### Inferences
- The per-run transcript plus screenshots is a reasonable working log. A firm that needs a tamper-evident audit trail of which client data an agent entered in which portal would need either Team/Enterprise OTel (which loses computer use) or its own logging.

### Gaps
- No documentation covers how long transcripts and screenshots are retained for individual-plan cloud sessions, or how to export them in bulk, beyond general deletion within 30 days after a user deletes a task.

## 8. Plans, usage limits and admin restrictions

### Takeaway
Feature availability splits along plan lines in a way that hurts this use case:

| Feature | Pro / Max | Team / Enterprise |
| --- | --- | --- |
| Cowork, scheduled tasks, skills, plugins, Claude in Chrome | Yes | Yes |
| Computer use | Yes | **No** |
| Dispatch | Yes (closed to new users) | No |
| Admin controls (OTel, browser allowlists, Auto-mode switch, plugin marketplaces) | No | Yes |

Long screen-driving runs draw on ordinary plan usage limits, and Auto mode costs more.

### Cited Findings
- Cowork is on all paid plans. The desktop app on Windows is "Available on all paid plans" [2026-09-25] — [Cowork on Team and Enterprise](https://support.claude.com/en/articles/13455879)
- Scheduled tasks: Pro, Max, Team and Enterprise [2026-09-29] — [Schedule recurring tasks](https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork)
- Computer use: Pro and Max only [2026-09-16] — [Let Claude use your computer](https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork)
- Claude in Chrome: all paid plans [2026-08-12] — [Chrome permissions guide](https://support.claude.com/en/articles/12902446-claude-in-chrome-permissions-guide)
- Dispatch: Pro and Max, closed to new users [2026-09-16] — [Dispatch help](https://support.claude.com/en/articles/13947068); [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop)
- Usage: "Everything you do with Claude counts toward your plan's usage limits. Longer agentic tasks… generally use more." [2026-09-16] — [One Claude](https://support.claude.com/en/articles/16761823). "Auto mode consumes more of your usage limit than the other modes." [2026-09-30] — [Get started with Claude Cowork](https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork)
- A 5-hour usage limit exists. Messages sent after reaching it are queued (2026-09-04) — [Claude Desktop changelog](https://claude.com/docs/cowork/changelog)
- Admin controls for Team and Enterprise owners [2026-09-25] — [Cowork on Team and Enterprise](https://support.claude.com/en/articles/13455879):
  - Enable or disable Cowork. Enterprise can enable it by group or custom role.
  - Turn "Run Cowork in the cloud" on or off.
  - Turn the built-in browser on or off.
  - Toggle Claude in Chrome, with allowlists and blocklists.
  - "Allow 'Automatically approve' mode" (on by default).
  - "Allow 'Always allow' for connector tools" (off by default).
  - Plugin marketplaces.
- Managed-config keys exist for **third-party (3P) Desktop deployments**: `scheduledTasksEnabled`, `keepAwakeEnabled` and `mcpScheduledTaskApprovalLifetimeDays` (Sept 2026) — [Claude Desktop changelog](https://claude.com/docs/cowork/changelog)
- "Shared logins aren't supported." [2026-09-30] — [Use Claude Cowork on web, desktop, and mobile](https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile)

### Inferences
- To get computer use, the firm would need a Pro or Max seat. Running one "employee" PC under one person's individual Max account blends personal and firm data. It also cannot use Team-level controls (OTel, browser allowlists, an org switch to forbid Skip mode).
- Several agents on one PC would most likely share one Claude account, since "shared logins aren't supported" and the desktop app signs in as one account. All agents would then draw on one usage pool.

### Gaps
- Exact current Pro and Max usage numbers, and how much a typical screenshot-heavy computer-use run consumes, were not found in official sources.
- Whether Anthropic plans to bring computer use to Team or Enterprise has no announced date.

## 9. Known limitations, bugs and community reports about unattended dedicated-machine use

### Takeaway
The official docs repeatedly frame scheduled and computer-use work as something to supervise, and explicitly warn against scheduling consequential or irreversible actions. The changelog and GitHub issues show active churn: cloud migration, device-binding bugs, forced re-logins on Windows, and a Windows update that broke local Cowork for a week. For this firm's requirements (unattended portal logins with MFA, entry of sensitive IDs, money-moving steps behind phone approval, several agents on one Windows PC), Cowork as of Oct 2026 is **not a reliable fit as the core runtime**. It is usable for the connector-based parts: email triage and drafting, research and reports, cloud-file work.

### Cited Findings
- Official safety guidance for scheduled tasks: "Because you can't monitor these tasks in real time… Don't schedule tasks that access sensitive files, send messages on your behalf, make purchases, or take other actions that are difficult to undo." [2026-09-16] — [Use Claude Cowork safely](https://support.claude.com/en/articles/13364135-use-cowork-safely)
- "Complex tasks sometimes need a second try… may struggle with complex multi-step workflows." "Screen interaction is slower than connectors." [2026-09-16] — [Let Claude use your computer](https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork)
- **Windows update breakage:** a Windows update released 8 Sep 2026 (including KB5124008) "stops Cowork from reaching your files when it runs on your Windows PC". This hit local Cowork sessions; cloud sessions and Claude Code were unaffected. It was resolved on 14 Sep 2026 by Microsoft's KB5129195 for Windows 11 24H2/25H2 — [Claude Desktop changelog](https://claude.com/docs/cowork/changelog)
- **Windows reliability fixes**, 2026-08 to 2026-10 — [Claude Desktop changelog](https://claude.com/docs/cowork/changelog):
  - "VM service not running" on Windows until restart (fixed 2026-08-13 and again 2026-09-24).
  - Sessions failing to start on Windows for accounts with many scheduled tasks or folders (several entries).
  - MSIX installs failing to save scheduled tasks (2026-08-11).
  - The app failing to start after updates (2026-09-24).
  - Terminal commands not running in the Terminal panel on Windows (2026-10-01).
- **Device-binding and sign-in bugs (open):**
  - Agent-created tasks cannot be device-bound; silent cloud fallback (opened 2026-09-05) — [#92268](https://github.com/anthropics/claude-code/issues/92268)
  - Windows scheduled-task settings cannot be saved ("Sign in again on this computer…") (opened 2026-09-26). It references device sessions force-logged-out every 24–36 hours (#81512), a device key not persisting on Windows 11 (#77596), and daily forced re-logins freezing task runs (#95963) — [#97341](https://github.com/anthropics/claude-code/issues/97341)
- A 2026-07-14 changelog entry mentions background sessions "blocked for session freshness, including while the desktop was idle" and requiring "Sign in again" — [Claude Desktop changelog](https://claude.com/docs/cowork/changelog)
- Anecdotal: the Windows app was reported using "prevent-display-sleep instead of prevent-app-suspension, preventing monitor from turning off" — [GitHub issue #46483](https://github.com/anthropics/claude-code/issues/46483) (title only seen; details not verified)
- A July 2026 hands-on review found the "local folder forces local run; asleep → won't start" behaviour "undocumented" at the time — [AI Blew My Mind, 9 Jul 2026](https://aiblewmymind.substack.com/p/claude-cowork-cloud-scheduled-tasks) (secondary)
- 1Password integration is Mac-only [2026-07-16] — [1Password for Claude](https://support.claude.com/en/articles/15936181-get-started-with-1password-for-claude). Built-in browser cookie import on Windows is Firefox-only [2026-09-16] — [Built-in browser](https://support.claude.com/en/articles/16607400-use-the-built-in-browser-in-claude-cowork)

### Inferences
- **What Cowork can do for this firm today:**
  - Connector-based scheduled jobs in the cloud: email triage and drafting through the Gmail or M365 connectors, research, reports, and summaries of files in connected cloud storage.
  - Private skills as playbooks, drafted with Record a skill.
  - Phone notifications and answers for cloud sessions.
  - Low-risk web reading through Claude in Chrome on an already-logged-in profile.
- **What it cannot reliably do unattended on a Windows PC:**
  1. Bind each agent to that PC after 6 Oct (Pro/Max), short of the Code tab's local tasks.
  2. Click into desktop apps without a per-session human "Allow".
  3. Log into MFA or CAPTCHA portals.
  4. Autofill passwords from a password manager on Windows.
  5. Enter SSNs, EINs or bank details without explicit approval (or at all).
  6. Click money-moving buttons even after approval (prohibited).
  7. Run two screen-driving agents at once.
  8. Run computer use on a Team or Enterprise plan.
  9. Trigger on file or email arrival.
- **Viability verdict for the report writer:** Cowork is a good fit for Roy's connector and research duties. It is not viable as the sole runtime for unattended portal and desktop-app automation with custom approval gates on Windows. That use case points to a custom app, or a hybrid in which Cowork handles cloud and connector jobs and a custom runner handles screen and portal work with its own approval and notification layer. Even a custom runner would face the same portal MFA problem, and Anthropic's usage policies on financial actions would still apply when it uses Claude models (the Agent SDK is out of scope for this note).

### Gaps
- No credible, detailed community write-up was found of someone running Cowork computer use unattended on a dedicated Windows box for weeks. Reports found were macOS-centred or about cloud tasks.
- Behaviour after the 6 Oct 2026 cutover cannot be verified yet. Treat everything about "local" Cowork scheduled tasks on Pro and Max as likely outdated within days.
