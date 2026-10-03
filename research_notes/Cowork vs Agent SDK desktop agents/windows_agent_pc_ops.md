# Operating and Securing a Dedicated, Always-On Windows 11 Pro PC for Unattended AI Agents (Computer Use + Chrome), as of October 3, 2026

*Scope: a small US tax/accounting firm with an office mini PC where Claude-powered agents (Claude Desktop Cowork/computer use + Claude in Chrome, or a custom Claude Agent SDK app) wake on schedules, take screenshots, and click and type in Acrobat, Excel, Word and Chrome (payroll, tax, government and bank portals). The owner monitors from his phone. This file does not compare agent platforms. Research date: 2026-10-03. Sources are dated where possible. Community/forum material is labeled anecdotal.*

## 1. Unattended GUI automation on Windows: locked sessions, screen savers, RDP, headless displays, sleep and power

### Takeaway
Screenshot-and-click automation only works on an **interactive, unlocked desktop with a live display**. A locked workstation, a running secure desktop (lock screen or UAC prompt), a disconnected or minimized RDP session, or a headless box with no display attached each cause black screenshots, failed input, or wrong coordinates. The standard fix pattern from RPA vendors: auto-logon a dedicated account to the **console** session, never lock it, keep the display on (HDMI dummy plug or virtual display driver on a headless mini PC), disable sleep, and set the BIOS to power on after AC loss. If anyone uses RDP, they must hand the session back to the console (`tscon`) instead of just disconnecting. Claude's own computer use has the same requirement: Anthropic says "Your desktop must be active."

### Cited Findings
**What breaks (RPA vendor documentation and community)**
- Microsoft Power Automate (doc dated 2026-08-31) documents how its own unattended runs work: it "creates a remote desktop (RDP) session on the machine to run unattended desktop flows. Connecting to the machine's console session isn't available for unattended runs." It also "keep[s] the screen of the target machine locked." Windows 10/11 "can't run unattended desktop flows if any active Windows user sessions are present (even a locked one)." Unattended flows "can't run with elevated privileges." "Logging into a machine during an unattended flow execution isn't supported and might cause the flow to fail." — [Microsoft Learn: Run unattended desktop flows](https://learn.microsoft.com/en-us/power-automate/desktop-flows/run-unattended-desktop-flows)
- Same doc: "The default screen resolution of the remote desktop session might be different than the one used during flow authoring… This can result in errors if a target element isn't found, or even in interacting with the wrong element if keyboard or mouse actions are used." Microsoft's fix is to set the screen resolution explicitly for unattended mode. — [Microsoft Learn](https://learn.microsoft.com/en-us/power-automate/desktop-flows/run-unattended-desktop-flows)
- UiPath community (anecdotal but consistent across many threads): unattended robots "do not perform under locked screen / minimized RDP-Session"; the suggested fix is the robot setting "Login to Console". Screenshots fail when RDP disconnects because VMs "stop rendering the screen because there is no virtual screen". Take Screenshot and similar activities "require a default desktop with an interactive window station attached." — [UiPath Forum: locked screen/minimized RDP](https://forum.uipath.com/t/unattended-robot-does-not-perform-under-locked-screen-minimized-rdp-session/299469); [UiPath Forum: screenshot fails when RDP disconnects](https://forum.uipath.com/t/take-screenshot-fails-in-unattended-mode-when-rdp-disconnects/342665); [UiPath Forum: black screenshot](https://forum.uipath.com/t/robot-taking-black-screenshot-in-unattended-mode/290290)
- UiPath official docs (v2023.10, possibly dated): RDP clients cause problems by "disconnecting the remote display buffer when the RDP application is minimized." The fix is a DWORD `RemoteDesktop_SuppressWhenMinimized` = `2` under `HKCU\Software\Microsoft\Terminal Server Client` (and the HKLM/Wow6432Node equivalents), set **on the client machine that opens the RDP window**, not on the robot machine. — [UiPath Robot docs: Recording and Remote Control troubleshooting](https://docs.uipath.com/robot/standalone/2023.10/admin-guide/recording-and-remote-control-troubleshooting)
- SmartBear TestComplete docs: closing an RDP session "locks out the computer and displays the logon screen", which leaves "the user session without a GUI" and makes GUI tests fail. Fix: run `tscon %sessionname% /dest:console` (as administrator) instead of closing RDP. This "returns control to the original local session… allowing all programs… to continue running normally." Warning: this leaves the computer unlocked, so lock it afterwards with `Rundll32.exe user32.dll,LockWorkStation` if needed. — [SmartBear: Disconnecting From Remote Desktop While Running Automated Tests](https://support.smartbear.com/testcomplete/docs/testing-with/running/via-rdp/keeping-computer-unlocked.html)
- Locked workstation or secure desktop (LogonUI/UAC): input injection fails. Separately, Windows UIPI drops synthetic input from a medium-integrity process (the agent) to a high-integrity window (an elevated app or admin prompt). — [Microsoft Learn: UIPI issues with UI and browser automation](https://learn.microsoft.com/en-us/troubleshoot/power-platform/power-automate/desktop-flows/ui-automation/uipi-issues); [codenote.net: Windows admin elevation blocks computer use (UIPI)](https://codenote.net/en/posts/windows-admin-elevation-blocks-chatgpt-computer-use-uipi/) (secondary); [hermes-agent issue #49067](https://github.com/NousResearch/hermes-agent/issues/49067) (anecdotal)

**Auto-logon**
- Microsoft (doc dated 2026-02-12): enable via `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon` → `AutoAdminLogon`=1, `DefaultUserName`, `DefaultPassword`. Microsoft's warnings, quoted: "anyone who can physically obtain access to the computer can gain access to all the computer's contents, including any networks it is connected to"; "the password is stored in the registry in plain text"; that key "can be remotely read by the Authenticated Users group." It is "recommended only for cases in which the computer is physically secured." — [Microsoft Learn: Configure Windows to automate logon](https://learn.microsoft.com/en-us/troubleshoot/windows-server/user-profiles-and-logon/turn-on-automatic-logon)
- Same doc: the Sysinternals **Autologon** tool stores the password as an LSA secret instead of in the Winlogon key. Gotchas: hold Shift at boot to bypass auto-logon. A logon banner set by GPO or local policy breaks auto-logon. Exchange ActiveSync password policies break it (Windows 8.1+). A console logon by a different user overwrites `DefaultUserName`, so auto-logon may then fail. — [Microsoft Learn](https://learn.microsoft.com/en-us/troubleshoot/windows-server/user-profiles-and-logon/turn-on-automatic-logon)
- On Windows 11 the netplwiz "Users must enter a user name and password" checkbox is hidden when "For improved security, only allow Windows Hello sign-in for Microsoft accounts on this device" is on. Turn that off, or use Sysinternals Autologon. — [iTechGuides](https://www.itechguides.com/how-to-log-in-automatically-to-windows-11/) (secondary); [TheGeekPage](https://thegeekpage.com/auto-login-missing-from-netplwiz/) (secondary)
- The "Do not display the lock screen" Group Policy officially applies only to Enterprise, Education and Server SKUs, not Windows 11 Pro. A registry workaround exists. This policy only hides the lock-screen curtain. It does not stop the session from locking. — [NinjaOne](https://www.ninjaone.com/blog/enable-or-disable-lock-screen-in-windows-11/) (secondary); [Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/5653308/how-do-i-disable-the-lock-screen-on-windows-11-pro)

**Headless display**
- With no monitor attached, headless PCs commonly fall back to 1024x768 (or 800x600) in remote sessions, and some GPU-dependent apps and screen capture can fail. An HDMI dummy plug makes the GPU think a monitor is present. — [daily.dev summary](https://daily.dev/posts/an-hdmi-dummy-plug-might-be-the-smallest-cheap-gadget-that-s-actually-useful-n2ebmdoah) (secondary); [VCOM blog](https://www.vcom.com.hk/shows/169/673.html) (vendor)
- A software alternative: the open-source (MIT) **Virtual Display Driver**, built on Microsoft's Indirect Display Driver/IddCx, adds virtual monitors to Windows 10/11 with custom resolutions and EDIDs. Its stated use cases include headless systems. — [GitHub: VirtualDrivers/Virtual-Display-Driver](https://github.com/VirtualDrivers/Virtual-Display-Driver)

**Power and BIOS**
- "Most mini PCs ship with their BIOS set to remain off when mains power is restored." Set "Restore on AC Power Loss" / "AC Recovery" / "After Power Failure" to **Power On** ("Last State" is the alternative). UPS caveat: if the UPS keeps the standby rail powered, the board never sees AC drop and will not auto-restart. — [MiniLab HQ](https://minilabhq.com/posts/mini-pc-wont-auto-boot-after-power-loss/) (secondary); [ASUS FAQ: Restore AC Power Loss](https://www.asus.com/support/faq/1049855/)

**Claude-specific (Cowork computer use / Claude Desktop)**
- Anthropic support: "Your desktop must be active. Your computer needs to be awake and the Claude Desktop app needs to be open for computer use to work." Computer use is beta and limited to Pro and Max plans: "Team and Enterprise plans don't have access to computer use at this time." — [Claude Help: Let Claude use your computer in Cowork](https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork)
- Claude Code Desktop local scheduled tasks "only fire while the app is open and your computer is awake." "If your computer sleeps through a scheduled time, the run is skipped." Turn on **Keep computer awake** (Settings → Desktop app → General). On wake, the app runs only **one** catch-up for the most recently missed time in the last 7 days, so "A task scheduled for 9am might run at 11pm." — [Claude Code Docs: Desktop scheduled tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks)
- Anthropic (support page updated 2026-09-30): starting **October 6, 2026**, new Cowork tasks on Pro/Max run in the cloud and the "Only on your computer" option is removed. "Tasks that use files on your computer need the desktop app open." Claude reaches local folders "only while it's open." — [Claude Help: Use Claude Cowork on web, desktop, and mobile](https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile)
- Bug report (April 11, 2026, Claude Desktop 1.1617.0, closed as duplicate): on Windows, Claude Desktop holds an Electron `prevent-display-sleep` power request, so the monitor never turns off while the app runs. Visible with `powercfg /requests`. — [GitHub anthropics/claude-code #46483](https://github.com/anthropics/claude-code/issues/46483)
- Open bug (filed around September 23, 2026, Claude Desktop MSIX, Windows 11): with computer use enabled, the Windows session "locks repeatedly—7 times in 4 minutes." The only workaround given is to disable computer use. A Windows bug like this would stall an unattended agent PC. — [GitHub anthropics/claude-code #96412](https://github.com/anthropics/claude-code/issues/96412)

### Inferences
- **Recommended console-session baseline** (synthesized from the vendor docs above):
  - Create a dedicated local standard account (e.g., `agent01`).
  - Set up auto-logon with Sysinternals Autologon (LSA secret) rather than a plaintext registry value.
  - Make sure no logon banner policy is set.
  - Turn off the Windows Hello-only toggle.
  - Turn off the screen saver lock and Dynamic Lock, and do not set an inactivity lock for that account.
  - Set "Turn off display" and "Sleep" to Never and disable hibernate. The `powercfg` CLI can do this.
  - Fit an HDMI/DP dummy plug (or Virtual Display Driver), set a fixed resolution, and set display scaling to 100%.
  - Set the BIOS to power on after AC loss and add a BIOS password.
  - Put the PC on a UPS. If the UPS is configured to shut the PC down, it must also cut output afterwards so the BIOS sees AC drop and powers the PC back on.
- Wake timers are not needed if the PC never sleeps, and never sleeping is the safer design: Claude local tasks are **skipped** during sleep, and the single catch-up run arrives at the wrong time.
- Do not use Windows RDP to "check on" the agent unless the operator runs a `tscon … /dest:console` script before leaving. Prefer a viewer that attaches to the existing console session (Chrome Remote Desktop without curtain mode, RustDesk, etc.). See section 4 for the security trade-off.
- Anything that triggers UAC or runs elevated will block the agent. Install and patch software from a separate admin account, and keep the agent account non-admin.
- Because the open #96412 lock-loop bug exists, pilot the exact Claude Desktop build on the target PC for several days before relying on it, and alert on Windows lock events (Security log event 4800 "workstation locked"; event ID from general Windows knowledge, not verified in this research).

### Gaps
- Microsoft has no single first-party doc on "keep a Windows 11 Pro console session permanently unlocked for automation." The guidance is assembled from RPA vendors and community posts.
- I did not verify whether Windows 11 24H2/25H2 mini PCs that use Modern Standby (S0ix) can fully disable standby, or which registry overrides still work. Check this on the specific hardware.
- Exact behavior of Chrome Remote Desktop curtain mode and RustDesk privacy mode on the console session after disconnect was not confirmed from first-party docs. See section 4.

## 2. Windows Update restarts, active hours, Group Policy on Windows 11 Pro, auto-start, and Task Scheduler pitfalls

### Takeaway
On Windows 11, most of the classic "don't reboot me" policies are **legacy and do not apply**. "No auto-restart with logged on users" is unreliable, and Microsoft now steers admins away from it. For a user-less device the modern answer is either (a) **compliance deadlines** (forced restart once the deadline passes, regardless of active hours) or (b) the new **maintenance windows** policies (January 2026 non-security update, Windows 11 24H2+), which Microsoft explicitly targets at "user-less devices (such as kiosks)." Pick a weekly window, such as Sunday 2–5 a.m., when no agent jobs run, and make sure the agent session comes back by itself through auto-logon and auto-start. In Task Scheduler, "Run whether user is logged on or not" runs the task in non-interactive Session 0, which **cannot** take screenshots or drive the GUI.

### Cited Findings
- Active hours default to 8 AM–5 PM, with a maximum range of 18 hours on current versions. Configure them with GPO "Turn off auto-restart for updates during active hours." — [Microsoft Learn: Manage device restarts after updates (2025-09-26)](https://learn.microsoft.com/en-us/windows/deployment/update/waas-restart)
- On "No auto-restart with logged on users…", Microsoft says the policy "was never created as a CSP. In Group Policy this policy doesn't work exactly as per description. This policy can result in no quality update reboots period." The recommended replacement is "to leverage compliance deadline and then to configure no-auto reboot to prevent non-user aware reboots prior to the deadline being reached." — [Microsoft Learn: waas-restart](https://learn.microsoft.com/en-us/windows/deployment/update/waas-restart)
- Same page: "Always automatically restart at the scheduled time," "Specify deadline before auto-restart," the engaged-restart policies, and several notification policies are each labeled "a legacy policy and isn't applicable for Windows 11." Also: "When using RDP, only active RDP sessions are considered as signed-in users. Devices that don't have locally signed-in users, or active RDP sessions, are restarted." — [Microsoft Learn: waas-restart](https://learn.microsoft.com/en-us/windows/deployment/update/waas-restart)
- Compliance deadlines (Windows 11 22H2+): separate quality and feature deadline policies, each with a grace period and an option to opt out of auto-restart until the grace period ends. "Once the effective deadline is reached, the device is forced to restart regardless of active hours." Since the December 10, 2024 update, "Configure Automatic Updates" (e.g., install at 3:00 AM) is respected before the deadline and ignored after it. After a failed restart past the deadline, "If the device is plugged in, it will attempt to restart every 5 minutes." — [Microsoft Learn: Enforce compliance deadlines (2026-06-30, updated 2026-09-28)](https://learn.microsoft.com/en-us/windows/deployment/update/wufb-compliancedeadlines)
- **Maintenance windows** (new): "released with the January 2026 Windows non-security update for Windows 11, versions 24H2 and later," available "through Group Policy and mobile device management (MDM)." Microsoft's target examples include "User-less devices (such as kiosks)." They cover all Windows Update content (security, .NET, Defender, drivers/firmware, feature updates). Setting `MaintenanceWindowUpdateActions` to "Restart" only lets downloads and installs happen beforehand, with only the restart held for the window. The system "only attempts to restart the device before 5:30 AM" if the window ends at 6 AM. Microsoft recommends using "either maintenance windows or update deadlines, but not both," and notes that "Expired deadlines are the only case in which update settings force update actions to occur outside of the maintenance window." One-time windows can be set up to 90 days ahead. — [Microsoft Learn: wufb-compliancedeadlines](https://learn.microsoft.com/en-us/windows/deployment/update/wufb-compliancedeadlines)
- Anecdotal and unverified: a forum article claims recent Windows 11 servicing "enforces automatic restarts more aggressively" and that both "Turn off auto-restart during active hours" and "No auto-restart with logged on users" must be enabled. This partly conflicts with Microsoft's guidance above. — [WindowsForum](https://windowsforum.com/news/how-to-stop-or-manage-automatic-restarts-after-windows-updates.363897/)
- Task Scheduler: with "Run whether user is logged on or not," the task runs in Session 0, a non-interactive session, so "you will not see the GUI even if you are logged on as the running user account." For a visible UI, use "Run only when user is logged on." — [Microsoft Learn Q&A archive](https://learn.microsoft.com/en-us/archive/msdn-technet-forums/d0ed7784-3475-4218-95c4-477d84233cb3); [Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/5789906/scheduler-tasks-with-security-options-run-whether)
- UiPath forum: activities like Take Screenshot need "a default desktop with an interactive window station attached." The same constraint applies to any screenshot-driven agent run as a service or in Session 0. — [UiPath Forum](https://forum.uipath.com/t/robot-taking-black-screenshot-in-unattended-mode/290290)
- Claude Desktop local scheduled tasks: the app "checks the schedule every minute while the app is open." Each task has a deterministic delay of "a few minutes" to stagger API traffic. In Manual permission mode, a run that needs an unapproved tool "stalls until you approve it." MCP tools marked `requiresUserInteraction` "prompt on every call" and stall every run. The docs recommend running each task once with **Run now** and choosing "always allow." The task history shows skipped runs with the reason (asleep, previous run still in progress, other tasks running). — [Claude Code Docs: Desktop scheduled tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks)
- Cowork scheduled tasks move to the cloud on Oct 6, 2026 (Pro/Max). Ones that use local files need the desktop app open on the PC. — [Claude Help](https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile)

### Inferences
- **Recommended Windows Update posture for the agent PC (Windows 11 Pro 24H2/25H2):**
  - Configure a weekly maintenance window through Local Group Policy in an off-hours slot with no agent schedules. Allow updates to download and install beforehand and hold only the restart for the window.
  - Do not also configure deadlines.
  - Set active hours to the maximum 18-hour span covering business hours as a backstop.
  - Do not rely on "No auto-restart with logged on users."
  - Do not pause updates indefinitely. The WISP requires patching (section 6).
- **Auto-start chain after any reboot:**
  1. BIOS powers on.
  2. BitLocker TPM-only unlocks with no prompt (section 4).
  3. Auto-logon signs in the agent account.
  4. Startup triggers launch the agent: a Task Scheduler task with an "At log on" trigger for that user and "Run only when user is logged on," or a Startup-folder shortcut. It launches Claude Desktop and/or the Agent SDK runner.
  5. The runner posts a heartbeat (section 7).
- Never register a GUI-driving agent as a Windows service or as a "run whether logged on or not" task. It will run, but blind, in Session 0.
- Because local Claude Desktop tasks start a few minutes late and can stall on permission prompts, prompts should check the current time and skip stale work. All required tool approvals should be pre-granted during a supervised "Run now."
- Pin the Claude Desktop version, or at least re-test after auto-updates. Two Windows regressions affected unattended use in 2026 (#46483, #96412).

### Gaps
- I could not confirm whether Windows 11 Pro's Local Group Policy editor (not just MDM/Intune) exposes every maintenance-window setting in the ADMX templates shipped with 24H2/25H2. Microsoft says "Group Policy and MDM" but I did not inspect the ADMX.
- No first-party Anthropic statement on how Claude Desktop auto-updates on Windows or whether admins can defer or pin versions. One lead to check: [Deploy Claude Desktop for Windows](https://support.claude.com/en/articles/12622703-deploy-claude-desktop-for-windows), not fetched.

## 3. Hardware sizing for a mini PC running Chrome + Office/Acrobat + an agent runtime

### Takeaway
Anthropic's computer-use guidance favors **modest screen resolutions** (1280x800 or 1366x768 for web apps; 1024x768 or 1280x720 for general desktop; nothing above 1920x1080). So the mini PC needs RAM and a stable display, not a big GPU. Cowork on Windows runs a local Hyper-V-based VM, so the PC must be **Windows 11 Pro (not Home) with CPU virtualization enabled**. Third-party guides put RAM at 8 GB minimum and 16 GB recommended for Cowork alone. With Chrome, Excel, Word, Acrobat and an agent runtime open together, 32 GB is a sensible target (inference).

### Cited Findings
- Anthropic: "For general desktop tasks, use 1024x768 or 1280x720; for web applications, use 1280x800 or 1366x768. Avoid resolutions above 1920x1080 to prevent performance issues." — [Claude Platform Docs: Computer use tool](https://platform.claude.com/docs/en/docs/agents-and-tools/tool-use/computer-use-tool)
- Image limits: Claude Opus 4.7 and later (including all `computer_toolset_20260801` models) accept up to 2576 px on the long edge and about 3.75 MP. Earlier models accept 1568 px and about 1.15 MP. "The API does not downscale automatically, so oversized images are rejected." Keep the scale factor to map coordinates back to the screen. Screenshots cost "roughly 1,000–1,800 input tokens each," and once a request has more than 20 images "every image in it is held to a stricter per-side limit." — [Claude Platform Docs](https://platform.claude.com/docs/en/docs/agents-and-tools/tool-use/computer-use-tool)
- The current GA tool is `computer_toolset_20260801`, supporting Claude 5.5-generation and other listed models. On the Claude API, Claude 5.5+ models return an error for the older `computer_20251124` version. — [Claude Platform Docs](https://platform.claude.com/docs/en/docs/agents-and-tools/tool-use/computer-use-tool)
- Cowork on Windows needs the Virtual Machine Platform and the full Hyper-V stack (Virtual Machine Management Service). Windows Home is not supported. Firmware virtualization (VT-x/AMD-V) must be on. — [GitHub anthropics/claude-code #27906](https://github.com/anthropics/claude-code/issues/27906); [Microsoft Q&A: "Virtualization is not available" in Claude Desktop](https://learn.microsoft.com/en-my/answers/questions/5934959/virtualization-is-not-available-showing-in-claude); [BetterClaw guide](https://www.betterclaw.io/blog/claude-cowork-windows-setup) (secondary)
- RAM: "8 GB RAM minimum, 16 GB recommended"; "the Cowork VM uses about 1.8 GB." Third-party and unverified against an Anthropic spec sheet. — [Houtini: Claude Desktop and Cowork System Requirements](https://houtini.com/articles/claude-desktop-system-requirements/) (secondary)
- RDP/unattended sessions can come up at a different default resolution than the one used to design the automation, which causes misclicks. — [Microsoft Learn: Power Automate](https://learn.microsoft.com/en-us/power-automate/desktop-flows/run-unattended-desktop-flows)
- Headless PCs default to low resolutions without a display or dummy plug. — [daily.dev](https://daily.dev/posts/an-hdmi-dummy-plug-might-be-the-smallest-cheap-gadget-that-s-actually-useful-n2ebmdoah) (secondary)

### Inferences
- **Suggested spec (inference, not from an authoritative benchmark):**
  - Windows 11 Pro.
  - Recent 8-core-class x86 CPU with VT-x/AMD-V and a TPM 2.0.
  - **32 GB RAM** (16 GB floor).
  - 1 TB NVMe SSD (screen recordings and logs add up).
  - Wired gigabit Ethernet.
  - At least two video outputs (one for the dummy plug).
  - BIOS that supports "power on after AC loss" and a BIOS password.
  - Avoid ARM Windows for now: Acrobat, tax-software helpers and Cowork VM support on ARM were not verified.
- **Display:**
  - Run the physical or virtual display at 1280x800 or 1366x768 with 100% scaling, so screenshots need no rescaling and coordinates map 1:1.
  - If a larger desktop is needed for Excel, use 1920x1080 at most and let the agent downscale, per Anthropic's scale-factor guidance.
  - Keep the resolution fixed. Changing it between design time and run time is a documented source of misclicks.
- One agent "seat" per Windows session: only one console session exists on Windows 11 Pro, so concurrent GUI agents cannot share one desktop without stepping on each other's mouse and keyboard. Plan sequential schedules, or more PCs or VMs, for parallel "employees."

### Gaps
- No official Anthropic hardware spec for Claude Desktop/Cowork on Windows (CPU/RAM) was found. The RAM figures come from third parties.
- No published benchmarks for Chrome + Office + agent memory use on mini PCs. The 32 GB recommendation is judgment.

## 4. Security: dedicated account, least privilege, BitLocker, Chrome profile, password managers and TOTP, network segmentation, remote access

### Takeaway
The required always-unlocked console plus auto-logon **removes the OS login as a control**. Physical security, BitLocker, network isolation and narrow account privileges therefore carry the load. Anthropic's own guidance is blunt: use a dedicated, minimally privileged environment; keep sensitive accounts out of the agent's browser profile; "Do not give computer use permission access to sensitive apps (such as banking, healthcare, government)." The firm's intended use (payroll, tax, government and bank portals) runs **directly against** Anthropic's published recommendations. Mitigate with read-only portal roles, human approval gates, and an explicit risk acceptance in the WISP. For credentials, keep raw passwords and TOTP seeds out of the model's context, avoid a single vault holding both factors, and keep the owner's phone as the second factor where possible.

### Cited Findings
**Anthropic platform guidance**
- Computer use precautions: "Use a dedicated virtual machine or container with minimal privileges"; "Avoid giving the model access to sensitive data, such as account login information"; "Limit internet access to an allowlist of domains"; "Ask a human to confirm decisions that might result in meaningful real-world consequences… such as… completing financial transactions." Also: "Using computer use within applications that require login increases the risk of bad outcomes as a result of prompt injection." — [Claude Platform Docs: Computer use tool](https://platform.claude.com/docs/en/docs/agents-and-tools/tool-use/computer-use-tool)
- Cowork computer use: "Do not give computer use permission access to sensitive apps (such as banking, healthcare, government)." "We strongly advise against using computer use to manage or take actions on sensitive information including… Managing financial accounts… Interacting with apps containing personal information of others." "Computer use has no sandbox between Claude and your applications." It has per-app permission prompts and an **app blocklist**; trading/crypto apps are blocked by default. Clicking a link in one app can open Chrome "even if you haven't explicitly granted Claude permission to use Chrome." — [Claude Help: Let Claude use your computer in Cowork](https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork)
- Claude in Chrome (article dated Aug 12, 2026): "Use a separate browser profile without access to sensitive accounts (such as banking, healthcare, government)." Modes are "Automatically approve" (default, self-screening) and "Manually approve." Confirmations are required for downloads and sensitive data entry. Financial sites need permission before access. Adult and pirated-content sites are blocked. — [Claude Help: Use Claude in Chrome safely](https://support.claude.com/en/articles/12902428-use-claude-in-chrome-safely)

**Accounts, auto-logon, BitLocker**
- Auto-logon exposes the machine to anyone with physical access, and the registry method stores the password in plaintext readable by Authenticated Users. Use only where "physically secured." — [Microsoft Learn: Automatic logon](https://learn.microsoft.com/en-us/troubleshoot/windows-server/user-profiles-and-logon/turn-on-automatic-logon)
- BitLocker **TPM-only** "doesn't require any interaction with the user to unlock" and is "more convenient… but less secure." Pre-boot PIN "can also make it more difficult to update unattended or remotely administered devices because a PIN must be entered when a device reboots." Network Unlock (the unattended TPM+PIN option) requires a WDS server on wired Ethernet. For skilled attackers with lengthy physical access, Microsoft recommends TPM+PIN, disabled standby, and a BIOS password for defense in depth. — [Microsoft Learn: BitLocker countermeasures (2025-07-29)](https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/countermeasures)
- Elevated windows and UAC prompts cannot be driven by a medium-integrity automation process (UIPI). — [Microsoft Learn: UIPI issues](https://learn.microsoft.com/en-us/troubleshoot/power-platform/power-automate/desktop-flows/ui-automation/uipi-issues)

**IRS sample WISP and Pub 4557 controls that directly affect this machine**
- Pub 5708 (Rev. 8-2024) sample WISP language:
  - "Computers must be locked from access when employees are not at their desks."
  - "The Firm will not have any shared passwords or accounts to our computer systems."
  - If a password utility is used, confirm "Multi-factor authentication of the user is enabled to authenticate new devices."
  - "Remote Access will not be available unless the Office is staffed and systems are monitored. Nights and Weekends are high threat periods for Remote Access Takeover data theft."
  - "Remote access will only be allowed using multi-factor Authentication."
  - Guest Wi-Fi must be "on a different network and Wi-Fi node."
  - Firewall between internet and internal network, plus a software firewall on workstations.
  - "Event Logging will remain enabled on all systems containing PII. Review of event logs… at random intervals not to exceed 90 days."
  - "AutoRun" disabled.
  — [IRS Publication 5708](https://www.irs.gov/pub/irs-pdf/p5708.pdf)
- Pub 4557 (Rev. 6-2024): "Use password-activated screen savers to lock employee computers after a period of inactivity"; "multi-factor authentication and a secure Virtual Private Network (VPN) should be minimum standards for remote access to the firm's office network"; use drive encryption; keep encrypted backups. Warning signs of data theft include "Computer cursors moving or changing numbers without touching the keyboard" and "computers turning themselves on." — [IRS Publication 4557](https://www.irs.gov/pub/irs-pdf/p4557.pdf)

**Password managers and TOTP**
- 1Password Service Accounts (CLI `op read`, `op inject`, `op run`) have hourly and daily rate limits. The daily limit is shared account-wide (reported as 1,000/24h on individual/family plans and 5,000 on Teams). — [1Password Developer: Service account rate limits](https://www.1password.dev/service-accounts/rate-limits); [1Password Developer: Use service accounts with CLI](https://developer.1password.com/docs/service-accounts/use-with-1password-cli/); [compscidr/iac issue #542](https://github.com/compscidr/iac/issues/542) (for the specific numbers; anecdotal)
- 1Password **Secure Agentic Autofill** (announced Oct 8, 2025): "just-in-time" credential delivery to an agent's browser over an E2E-encrypted channel, with human-in-the-loop approval before sign-in; "raw credentials never enter the LLM context." At launch it was available **only in early access through Browserbase** (a cloud browser), not for a local Chrome on a Windows PC. Current status in October 2026 is unverified. — [1Password press release](https://1password.com/press/2025/oct/browserbase-ai-security-partnership); [1Password blog](https://1password.com/blog/closing-the-credential-risk-gap-for-browser-use-ai-agents)
- Bitwarden: unattended CLI use logs in with a personal API key (client_id/secret), unlocks to a `BW_SESSION` key, and should end with `bw lock`. Bitwarden Secrets Manager uses a separate `bws` CLI with machine-account access tokens. — [ComputingForGeeks](https://computingforgeeks.com/how-to-use-bitwarden-cli/) (secondary); [bigmike.help](https://bigmike.help/en/devops/bitwarden-cli-password-management-from-the-terminal-and-ci-cd-automation/) (secondary)
- TOTP in the same vault: critics say a single compromise yields both factors, so "the second factor stops being a second factor." 1Password's position is that storing TOTP in 1Password gives "the same level of protection" as an authenticator app on the same device. Bitwarden ships a separate Bitwarden Authenticator app (May 2024) for users who want separation. — [1Password blog](https://1password.com/blog/1password-2fa-passwords-codes-together); [Privacy Guides discussion](https://discuss.privacyguides.net/t/should-i-use-my-password-manager-for-storing-totp-codes/13379) (community); [AlternativeTo news](https://alternativeto.net/news/2024/5/bitwarden-launches-standalone-open-source-authenticator-app-for-two-factor-authentication)

**Remote access**
- CISA/NSA/MS-ISAC joint advisory AA23-025A (Jan 25, 2023; older but still relevant): criminals abused legitimate remote-access tools (AnyDesk, ScreenConnect), including **portable executables needing no admin rights**, to steal from bank accounts. — [CISA/NSA joint advisory (PDF)](https://media.defense.gov/2023/Jan/25/2003149873/-1/-1/0/JOINT_CSA_RMM.PDF); [CISA Guide to Securing Remote Access Software (June 2023)](https://www.cisa.gov/sites/default/files/2023-06/Guide%20to%20Securing%20Remote%20Access%20Software_clean%20Final_508c.pdf)
- Chrome Remote Desktop **curtain mode** (blanks the local screen during remote sessions) requires Windows Pro or higher and the policy `RemoteAccessHostRequireCurtain`=1. With curtain enabled, the host "will automatically show a locked screen" to anyone physically present. — [AirDroid guide](https://www.airdroid.com/remote-support/chrome-remote-desktop-curtain-mode/) (secondary); [AnyViewer](https://www.anyviewer.com/how-to/chrome-remote-desktop-lock-screen-2578.html) (secondary)
- Closing a Windows RDP session leaves the console locked and the GUI unavailable to automation unless `tscon` returns it to the console. — [SmartBear](https://support.smartbear.com/testcomplete/docs/testing-with/running/via-rdp/keeping-computer-unlocked.html)

### Inferences
- **Account model:**
  - Account 1, `agent01`: a standard (non-admin) local account, auto-logged on, the only account that runs agents.
  - Account 2: a separate local admin with a strong unique password, used only for installs and patching (never auto-logged on).
  - The owner's own Microsoft/Entra account should not be on this machine for daily use.
  - In agent01, use a **dedicated Chrome profile** containing only the allowlisted portals, with Chrome's own password saving off when a password manager handles fills. If the firm wants a URL allowlist, Chrome enterprise policies (URLAllowlist/URLBlocklist) can enforce it locally. These policy names come from general Chrome knowledge and were not verified here.
  - Use the Cowork **app blocklist** to deny everything except Acrobat, Excel, Word and Chrome.
- **Least privilege at the portals matters more than at the OS.** Where portals support sub-users, give the agent its **own** login (satisfying the WISP "no shared accounts" rule and portal ToS) with **view-only/read-only roles** at banks and payroll where possible. Keep anything that moves money or e-files behind the owner's approval. The existence of read-only sub-user roles varies by portal and was not verified.
- **BitLocker:** use TPM-only (needed for unattended reboots after updates or power loss) plus physical controls: a locked room or cage, BIOS password, Secure Boot, disabled boot from USB, and no exposed Thunderbolt/DMA if possible. With auto-logon, BitLocker mainly protects a **powered-off/stolen drive**. It does not protect a running, auto-logged-on PC. Document that limit in the WISP risk assessment.
- **Credentials:**
  - Best: the agent never sees raw passwords. Use the password manager's browser autofill or a human-approved fill, so the password never appears in the prompt or the screenshots the model reads.
  - Next best: inject secrets into the Agent SDK tool layer (e.g., `op run`/`op read` with a service account scoped to one "Agent" vault), never into the prompt.
  - Keep TOTP seeds for high-value portals (banks, IRS/ID.me, payroll) **off** the agent PC. Rely on "remember this device" plus codes relayed from the owner's phone, so a full compromise of the agent PC does not yield both factors.
  - Watch 1Password service-account rate limits if many runs fetch secrets.
- **Network:**
  - Put the agent PC on its own VLAN or a separate SSID/port group, firewalled from the firm's file server except for one read-only share holding client uploads, plus an outbound path to the internet.
  - Consider DNS filtering with an allowlist for the agent VLAN.
  - Disable inbound RDP from the internet entirely.
- **Remote access for the owner:**
  - (a) Claude's own phone surfaces (Dispatch/mobile Cowork) for approvals.
  - (b) A console-attaching viewer with MFA for visual checks, e.g., Chrome Remote Desktop tied to a Google account with 2-Step Verification, or RustDesk with a self-hosted relay. This does not lock the agent's session.
  - Avoid curtain mode and plain RDP, since both lock or detach the console that the agent needs.
  - The WISP sample discourages after-hours remote access, so the plan should document MFA, logging and alerting for remote sessions as compensating controls.
  - Never leave unattended-access passwords static and shared.

### Gaps
- No first-party documentation found on whether 1Password or Bitwarden **browser-extension autofill** keeps working unattended for days. Vault auto-lock timers, Windows Hello unlock prompts and extension re-auth would interrupt fills. This needs a pilot.
- RustDesk's and Chrome Remote Desktop's exact session behavior on disconnect (relocks or not) was not confirmed from first-party docs.
- Whether Anthropic's "do not use for banking/government" guidance is a contractual restriction or advisory only was not determined. It reads as advisory safety guidance. Other researchers covering platform terms should confirm.

## 5. AI-specific risks: prompt injection via client documents, email and web pages, and mitigations

### Takeaway
An agent that reads untrusted content (client uploads, inbound email, web pages) **and** can act (type into portals, send email, move files) is the exact pattern Anthropic and OWASP flag as most dangerous. Anthropic's built-in classifiers and training reduce but do not remove the risk: Claude in Chrome reports under 0.08% attack success in internal tests, "still non-zero." Standard mitigations:
- Separate the agents that read untrusted content from the agents that can act.
- Least privilege and allowlists of apps and sites.
- Human confirmation for irreversible or financial actions.
- Read-only portal roles.
- Close monitoring of scheduled, unattended runs.

### Cited Findings
- Anthropic: "In some circumstances, Claude will follow commands found in content even when they conflict with your instructions. For example, instructions on webpages or contained in images might override your instructions." Classifiers "automatically scan what the tools return, such as screenshots, to flag potential prompt injections" and steer the model to confirm with the user. "The precautions above remain important even with these classifiers in place." — [Claude Platform Docs: Computer use tool](https://platform.claude.com/docs/en/docs/agents-and-tools/tool-use/computer-use-tool)
- Anthropic (Use Cowork safely, updated 2026-09-16): "For prompt injection attacks to be successful, two things must be true at the same time: Claude can read information outside your trusted boundary, and can perform actions that could compromise the user." On scheduled tasks: "Don't schedule tasks that access sensitive files, send messages on your behalf, make purchases, or take other actions that are difficult to undo." Use "Manually approve" when "The task touches sensitive files, accounts, or sites." Computer use runs "without the permission checks that gate other Cowork tools." In "Skip all approvals," "nothing checks its actions." — [Claude Help: Use Cowork safely](https://support.claude.com/en/articles/13364135-use-cowork-safely)
- Anthropic: Claude "is trained to avoid risky operations—like transferring funds, modifying or deleting files, or handling sensitive data—and to flag signs of prompt injection. However, these safeguards aren't perfect." "Don't rely on them as a substitute for blocking access to sensitive apps." — [Claude Help: computer use in Cowork](https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork)
- Claude in Chrome: "Our current configuration reduces attack success rates to less than 0.08% against our internal testing… the chances of an attack are still non-zero." (Aug 12, 2026) — [Claude Help: Use Claude in Chrome safely](https://support.claude.com/en/articles/12902428-use-claude-in-chrome-safely)
- OWASP LLM01:2025 Prompt Injection: distinguishes direct from **indirect** injection (content from websites and files) and warns about multimodal attacks "hiding instructions in images that accompany benign text." Mitigations: constrain model behavior; define and validate output formats; input/output filtering; "privilege control and least privilege access"; "Require human approval for high-risk actions"; "Segregate and identify external content"; adversarial testing. It cross-references LLM06 Excessive Agency. — [OWASP GenAI: LLM01 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- OWASP Top 10 for Agentic Applications (2026): ASI01 Agent Goal Hijack (objective redirected "through content the agent reads"), ASI02 Tool Misuse & Exploitation, Identity & Privilege Abuse, Agentic Supply Chain, Unexpected Code Execution, Memory & Context Poisoning, Insecure Inter-Agent Communication, Cascading Failures, Human-Agent Trust Exploitation, Rogue Agents. — [Giskard summary](https://www.giskard.ai/knowledge/owasp-top-10-for-agentic-application-2026) (secondary); [Promptfoo: OWASP Agentic](https://www.promptfoo.dev/docs/red-team/owasp-agentic-ai/) (secondary)
- Cross-app spillover: actions in one app can affect others, e.g., an email link opening in Chrome. — [Claude Help](https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork)
- Plugins/MCPs "run on your computer with the same permissions as any other program." Stick to verified extensions. — [Claude Help: Use Cowork safely](https://support.claude.com/en/articles/13364135-use-cowork-safely)

### Inferences
- **Mitigation checklist for this firm:**
  1. **Split duties.** An "intake" agent reads client uploads and email but has no portal logins and can only write summaries or extracted fields to a staging folder. A "portal" agent works only from those structured fields and never opens raw client files or email.
  2. **Allowlists.** Use the Cowork app blocklist plus Chrome site permissions (or an enterprise URL allowlist) limited to named portals. Use a separate Chrome profile per role.
  3. **Confirmation gates.** Require phone approval for any submit, e-file, payment, payroll run, bank transfer, outbound email to a new address, or deletion. Use "Manually approve" for sensitive tasks, and never "Skip all approvals" on this PC. In an Agent SDK build, enforce gates in code before tool execution rather than relying on the prompt. That is a design inference; other researchers cover SDK specifics.
  4. **Read-only by default** at banks and payroll, with write access granted per task.
  5. **Treat every client upload as hostile:** a PDF can carry hidden text or instructions in images, and OWASP specifically calls out multimodal injection. Consider pre-converting uploads to text/OCR in a sandbox and stripping links.
  6. **Monitor scheduled runs:** review every run's transcript and recording, and alert on unexpected domains or apps.
  7. **Minimize on-screen data:** close unrelated windows, because screenshots capture everything visible.

### Gaps
- No public, independent measurements of prompt-injection success rates for desktop computer use (as opposed to Chrome/browser use) were found.
- No published real-world incident of an accounting firm compromised via agent prompt injection was found in this research.

## 6. Compliance for a US tax/accounting firm: FTC Safeguards Rule, IRS Pub 4557/5708 WISP, and what an AI agent changes

### Takeaway
Tax preparers are "financial institutions" under GLBA, so the FTC Safeguards Rule applies, and the IRS expects a **written information security plan (WISP)**. Pub 5708 is the IRS template. An agent PC with portal access to client data must be written into the WISP:
- in the asset inventory and risk assessment;
- in access controls, including how MFA applies to an unattended account;
- in logging and monitoring of "authorized users" (the agent is one);
- in service-provider oversight (Anthropic, the password-manager vendor, any remote-access vendor);
- in change management;
- in incident response.

Several sample-WISP rules (lock unattended computers, no shared accounts, no after-hours remote access) **conflict** with an unattended GUI agent. Each needs a documented exception and compensating controls approved by the Qualified Individual.

### Cited Findings
- The FTC lists "tax preparation firms" as covered financial institutions. Required elements:
  - a Qualified Individual;
  - a written risk assessment;
  - access controls reviewed periodically;
  - an inventory of data and "all systems, devices, platforms, and personnel";
  - encryption at rest and in transit;
  - "multi-factor authentication for anyone accessing customer information on your system";
  - evaluation of third-party apps;
  - disposal "no later than two years after your most recent use";
  - change management;
  - "procedures and controls to monitor when authorized users are accessing customer information on your system and to detect unauthorized access";
  - annual penetration testing and vulnerability scans every six months;
  - training;
  - service-provider contracts and oversight;
  - a written incident response plan;
  - an at-least-annual written report to the governing body.

  Firms with customer information on fewer than 5,000 consumers are exempt from "certain provisions." The FTC must be notified within 30 days of discovering unauthorized acquisition of unencrypted information of 500+ consumers. — [FTC: Safeguards Rule — What Your Business Needs to Know](https://www.ftc.gov/business-guidance/resources/ftc-safeguards-rule-what-your-business-needs-know)
- Pub 5708 (Rev. 8-2024) restates the FTC elements. It requires MFA "for any individual accessing any information system, unless your qualified individual has approved in writing the use of reasonably equivalent or more secure access controls," and FTC reporting for 500+ affected people within 30 days. Its sample policies (quoted in section 4) cover locking computers, no shared accounts, password utilities with MFA, MFA-only remote access limited to staffed hours, firewalls, event-log review at most every 90 days, and continuous patching with a security review "at least every 30 days." It advises cataloging "all devices used in your practice that come in contact with taxpayer data" and listing vendors such as "your IT Pro" authorized to handle PII. — [IRS Publication 5708](https://www.irs.gov/pub/irs-pdf/p5708.pdf)
- Pub 4557 (Rev. 6-2024) checklist: MFA for anyone accessing customer information; password-activated screen savers; encryption; encrypted backups; MFA plus VPN for remote access; staff awareness of remote-takeover signs (moving cursors, machines turning on). — [IRS Publication 4557](https://www.irs.gov/pub/irs-pdf/p4557.pdf)
- The IRS has repeatedly reminded tax pros (e.g., July 2025) of the WISP requirement. — [CPA Practice Advisor (2025-07-29)](https://www.cpapracticeadvisor.com/2025/07/29/irs-reminds-tax-pros-of-requirement-for-a-written-security-plan-wisp/165822/); [IRS: Tax professional tips for creating a data security plan](https://www.irs.gov/newsroom/tax-professional-tips-for-creating-a-data-security-plan)
- Anthropic: "You remain responsible for all actions taken by Claude performed on your behalf," including "Data accessed or modified," "Actions taken by scheduled tasks," and "Actions taken through computer use." Cowork activity is captured in the **Compliance API** and can stream to SIEMs via **OpenTelemetry**, but only for **Team and Enterprise** owners. — [Claude Help: Use Cowork safely](https://support.claude.com/en/articles/13364135-use-cowork-safely)
- Computer use in Cowork is "Available for Pro and Max plans only. Team and Enterprise plans don't have access to computer use at this time." — [Claude Help](https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork)

### Inferences
- **Audit-logging gap:** the plans that offer Cowork computer use (Pro/Max) appear not to be the plans with Compliance API/OpenTelemetry audit export (Team/Enterprise). A Cowork-based setup may lack the organization-level audit trail an FTC "monitor authorized users" control would want. That pushes toward local logging, such as screen recording, Windows event logs and saved transcripts, or toward an Agent SDK build where the firm logs every tool call itself. Other researchers comparing platforms should confirm.
- **WISP addendum items for the agent PC:**
  - **Inventory:** list the device, its accounts, apps, portals and data folders.
  - **Risk assessment:** cover prompt injection, credential theft, unattended unlocked console, remote-access takeover, and vendor (model provider) data handling.
  - **Access control:** the agent gets its own accounts per portal (no shared logins), least privilege, and read-only roles where possible.
  - **MFA:** the owner's phone remains the possession factor via relayed codes and remembered devices. Any case where TOTP seeds sit on the agent PC needs the Qualified Individual's *written* approval of "reasonably equivalent" controls.
  - **Exceptions:** document "console stays unlocked" as an exception to the screen-lock policy, with compensating controls (locked room, BitLocker, VLAN, camera, alerting on remote sessions and logons).
  - **Remote access:** owner-only, MFA, logged, alerting on connect.
  - **Logging:** keep Windows event logs on, keep agent transcripts and screen recordings, review at least every 90 days per the sample WISP, and dispose of recordings and screenshots containing PII within the FTC's two-year rule unless retention is otherwise required.
  - **Service providers:** review Anthropic's commercial or consumer terms and data retention, plus the password-manager and remote-tool vendors.
  - **Incident response:** add an agent-specific kill switch (pause tasks, revoke portal sessions, rotate credentials) and the FTC 30-day reporting step.
  - **Staff training:** tell staff the agent PC's cursor moves by itself, so they don't mistake it for an intrusion. Real remote-takeover signs from Pub 4557 must still be investigated, and alerting should tell agent activity apart from intrusions.

### Gaps
- **IRC §7216 / Treas. Reg. §301.7216** (taxpayer consent for use or disclosure of tax return information, including to cloud AI vendors) was not researched. It is likely material and should be checked by the report writer or counsel.
- State-law overlays (e.g., Massachusetts 201 CMR 17.00 WISP requirements, state breach-notification laws) were not researched.
- Whether newer revisions of Pub 4557/5708 exist after Rev. 6-2024 / Rev. 8-2024, or whether the IRS has issued AI-specific guidance for practitioners' own use of AI agents, was not confirmed. The IRS AI governance IRM (10.24.1) covers IRS internal use, not practitioners.
- Anthropic's data-retention and training terms by plan (Pro/Max vs Team/Enterprise vs API) were not researched here and matter for the vendor-oversight section.

## 7. Monitoring and recovery: health checks, heartbeats, run logs, recordings, backups

### Takeaway
Use an **external dead-man's-switch heartbeat**. The agent PC pings a monitoring URL on a schedule and after each job, and silence triggers a phone alert. This catches power loss, a crashed app, a stuck permission prompt, a sleeping PC, or a locked session. Combine it with:
- per-run transcripts and screen recordings stored encrypted and retained per the WISP;
- Windows event-log review;
- encrypted backups of client data and of the agent configuration;
- a written rebuild runbook.

### Cited Findings
- Healthchecks.io uses the "Dead man's switch technique: the monitored system must 'check in'… at regular, configurable time intervals. As soon as Healthchecks.io sees a missed check-in, it sends you an alert." A `/fail` suffix signals explicit failure. — [Healthchecks.io FAQ](https://healthchecks.io/docs/faq/); [Medium guide](https://medium.com/@nisheet110/healthchecks-io-the-ultimate-guide-to-application-and-cron-job-monitoring-fd1b6bf311fc) (secondary)
- Claude Desktop task history shows skipped runs and the reason (asleep, previous run in progress, other tasks running). Desktop notifications fire when tasks start and when catch-up runs start. Runs needing an unapproved tool stall and wait in the sidebar. — [Claude Code Docs: Desktop scheduled tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks)
- Anthropic recommends: "Review outputs after each run"; "Pause tasks you're not actively using"; "Monitor tasks, not just commands"; stop the task if Claude accesses unexpected files or sites. — [Claude Help: Use Cowork safely](https://support.claude.com/en/articles/13364135-use-cowork-safely)
- `powercfg /requests` shows which process holds the system or display awake (claude.exe was visible there). Useful for diagnosing sleep and display problems. — [GitHub #46483](https://github.com/anthropics/claude-code/issues/46483)
- Pub 4557: make full backups, encrypt them, back up monthly or more often during filing season, use external drives or cloud with encryption before upload. Encrypted backups are "your best protection against ransomware attacks." — [IRS Publication 4557](https://www.irs.gov/pub/irs-pdf/p4557.pdf)
- Sample WISP: event logging enabled, review at random intervals not exceeding 90 days. Patches and security updates reviewed and installed continuously, with a top-down security review at least every 30 days. — [IRS Publication 5708](https://www.irs.gov/pub/irs-pdf/p5708.pdf)
- FTC: monitor authorized users' access; dispose of customer information within two years of last use; written incident response plan. — [FTC Safeguards Rule guidance](https://www.ftc.gov/business-guidance/resources/ftc-safeguards-rule-what-your-business-needs-know)

### Inferences
- **Monitoring design:**
  1. **Machine heartbeat:** a Task Scheduler job in the agent session ("Run only when user is logged on") pings every 5–10 minutes. Silence means the PC is off, has rebooted without auto-logon, the network is down, or the session is gone.
  2. **Session-health heartbeat:** before pinging, the script checks that the session is unlocked (no LogonUI process / session state Active), Claude Desktop or the SDK runner is running, a test screenshot isn't black, and the resolution is as expected. If not, it pings `/fail` with a reason.
  3. **Per-job check-ins:** each scheduled agent job pings start/success/fail URLs, which catches "ran at 11 pm instead of 9 am" and stalled permission prompts.
  4. **Security alerts:** forward Windows events for logon, unlock, RDP/remote-tool connects, new local users and lock events to the owner's phone, through a small script or an RMM/EDR tool.
- **Run evidence:** save each run's transcript plus a screen recording (or periodic screenshots) to an encrypted folder. These contain client PII, so they fall under WISP retention and the FTC two-year disposal rule; set a retention period (e.g., through the filing-season close plus N months) and auto-delete.
- **Recovery:**
  - Keep a written runbook: BIOS settings, Windows policies, Autologon, display, Chrome profile, password-manager setup, Claude settings and approvals, and the scheduled-task definitions. Claude Desktop task prompts live under `~/.claude/scheduled-tasks/<task>/SKILL.md`, but schedule, model and folder do not; export or record them.
  - Keep a periodic full disk image of the configured PC so a failed SSD or a bad update can be restored quickly.
  - Back up client data separately and encrypted, per Pub 4557.
- **Kill switch:** keep a way for the owner to pause all agent tasks from the phone, and a documented credential-rotation procedure if compromise is suspected.

### Gaps
- No first-party Anthropic feature for external heartbeat/uptime alerts on the Desktop app was found. Monitoring has to be built around it.
- No authoritative retention period for AI-agent screen recordings at tax firms was found. The FTC two-year disposal rule and WISP log review are the nearest anchors.

## 8. Terms of service: automated/bot access to payroll, tax software, IRS e-Services, state portals and banks

### Takeaway
Many relevant vendors' terms **prohibit or restrict automated access, sometimes naming AI agents explicitly**. TaxAct's professional license (updated Sept 8, 2026) bars "artificial intelligence agents" and RPA without prior written authorization. ADP treats any third party using a client's credentials as an "Unauthorized Third Party" regardless of consent, and limits traffic to what "a human can reasonably produce." Anthropic itself places responsibility on the user for "Respecting third-party website terms of service, including any restrictions on automated access." Before automating any portal, review its current terms and ask the vendor for written permission or an API/integration route. Expect banks and government portals to be the most restrictive. Specific IRS e-Services and state-portal language was not located in this research.

### Cited Findings
- Anthropic: users remain responsible for "Respecting third-party website terms of service, including any restrictions on automated access." — [Claude Help: Use Cowork safely](https://support.claude.com/en/articles/13364135-use-cowork-safely)
- TaxAct Professional Software License Agreement (Last Updated: September 8, 2026): "Automated Means means scripts, bots, robotic process automation, artificial intelligence agents, scraping tools, or other automated technologies that interact with the Software." Users may not access or use the Software through Automated Means "without TaxAct's prior written authorization," and may not use the Software or outputs to train AI. — [TaxAct Professional legal notice](https://www.taxact.com/professional/legal-notice)
- ADP Terms (© 2026): an "Unauthorized Third Party" is "Any third party or business that seeks to access or accesses ADP sites or systems using the account credentials… of an ADP client or client employee, regardless of the their purposed consent." ADP prohibits data scrapers and aggregators and accessing the site "in a manner that sends more requests to ADP servers than a human can reasonably produce." Unauthorized access to password-protected areas "is prohibited and may lead to criminal prosecution." — [ADP Legal](https://www.adp.com/legal.aspx)
- ADP Marketplace terms: clients "may not use any robot, spider, or other automated process to scrape, crawl, or index" and must integrate "only through documented APIs." — [Law Insider: Use of the ADP APIs clause](https://www.lawinsider.com/clause/use-of-the-adp-apis) (secondary clause database)
- Banks: Wells Fargo, JPMorgan Chase and Bank of America have taken action against screen scraping by aggregators that log in with customers' credentials (article date not confirmed; likely years old). — [American Banker](https://www.americanbanker.com/news/the-truth-behind-the-hubbub-over-screen-scraping)
- IRS e-Services: sign-in now goes through ID.me, and users must accept the e-Services terms of agreement at sign-in. The current text on automation or credential sharing was not retrievable (the IRS "Preview updated e-Services user agreement" page returned 404 on 2026-10-03). — [IRS: e-Services](https://www.irs.gov/e-services); [IRS: Circular 230 practitioner e-Services access](https://www.irs.gov/e-file-providers/circular-230-practitioner-e-services-access)

### Inferences
- **How firms typically handle this** (inference; no survey data found):
  1. Prefer official integrations and APIs: payroll-provider APIs or accountant portals, bank data feeds through the firm's accounting software, and tax software's own import features. These sit outside the "no bots" clauses.
  2. Where only the web UI exists, ask the vendor for **written permission** (TaxAct's clause explicitly contemplates "prior written authorization").
  3. Give the agent its **own user** where the vendor allows multiple users, rather than having it reuse a client's or employee's credentials. ADP's language targets third parties using someone else's credentials.
  4. Keep automation at human pace and volume.
  5. Avoid automating ID.me/IRS e-Services and bank logins entirely, or limit agents to read-only, human-supervised sessions, given Anthropic's own "do not use for banking/government" guidance and the identity-proofing nature of ID.me.
- For the IRS, practitioner credentials are tied to an identity-proofed individual. Letting an AI agent operate an individual's e-Services session likely raises credential-sharing and accountability concerns even if no clause names "bots." This is unverified; check the current e-Services terms of agreement and ID.me's terms directly.
- ToS violations risk account suspension, which for a tax firm could mean losing access to EFIN/e-Services or payroll in peak season. That operational risk belongs in the WISP risk assessment and the business-continuity plan.

### Gaps
- Exact current text of the IRS e-Services terms of agreement and ID.me terms on automated access and credential use: not found.
- State tax portal terms (e.g., MassTaxConnect, other DOR portals): not found in this research. Search results returned only generic government ToS.
- Specific bank online-banking agreements, and the status of the CFPB §1033 open-banking rule (which affects screen scraping), were not researched.
- Payroll providers other than ADP (Gusto, Paychex, Patriot Software, QuickBooks Payroll) were not checked.
