# Microsoft vs Google: named autonomous agents (quick check, 2026-10-03)

## 1. Microsoft
**Copilot Studio autonomous agents**
- Named agent: yes, you build a custom agent with event triggers. [MS Learn, accessed 2026-10-03](https://learn.microsoft.com/en-us/microsoft-copilot-studio/authoring-triggers-about)
- File trigger: yes. "When an item is created in SharePoint" and "When a file is created in OneDrive"; email trigger too. [same]; [Nachanblog 2025-02-27](https://nanddeepnachanblogs.com/posts/2025-02-27-autonomous-agents-copilot-studio/)
- Schedule trigger: not confirmed in the sources read.
- Price: $200 license, pre-purchase plan or pay-as-you-go. [MS pricing, accessed 2026-10-03](https://www.microsoft.com/en-us/copilot/pricing/copilot-studio)
- Limitation: users report trouble getting file-upload triggers to fire. [Reddit, 2026](https://www.reddit.com/r/copilotstudio/comments/1vi317b/how_to_trigger_a_copilot_studio_agent_when_a_new/)

**Copilot Cowork (GA 2026-06-16)**
- Runs unattended in the cloud: yes. "Tasks keep running even when your laptop is off." It runs work end to end and "returns a completed result." [MS blog 2026-06-16](https://www.microsoft.com/en-us/copilot/blog/2026/06/16/copilot-cowork-is-now-generally-available/)
- Schedule or folder trigger: not stated in the GA post.
- Approvals: admins switch it on (off by default) and set spending caps. Users ask for more credits when they run out. [same]
- Models: Anthropic Opus 4.8 and Sonnet 4.6. GPT 5.5 is in Frontier, and Microsoft's own "Cowork 1" model is coming. [same]
- Price: needs the M365 Copilot license ($30/user/mo, [HSO May 2026](https://www.hso.com/blog/microsoft-copilot-vs-studio/)). Usage is billed on top at $0.01 per Copilot Credit (PayGo). [MS blog]
- Limitation: cost is variable. Every run spends credits and none are included in the $30 license. DLP is "coming soon."
- **Agent 365** (May 1, 2026) is a governance control plane, not an agent runner. [HSO]

## 2. Google
**Workspace Studio (formerly Workspace Flows)**
- Named agent/flow: yes. Gemini 3 builds it from plain language. [Google, accessed 2026-10-03](https://workspace.google.com/studio/)
- Triggers: Gmail, Forms, Drive and schedule-based events. [Zenphi, undated](https://zenphi.com/document-workflows-in-google-drive-google-studio-test/)
- New Drive copy/move steps arrived in September 2026. [Workspace Updates 2026-09](https://workspaceupdates.googleblog.com/2026/09/automate-drive-gmail-and-google-chat-actions-with-new-steps-in-Workspace-Studio.html)
- Reports: Chat posts, emails, Sheets rows; you track activity inside Gmail, Chat and Drive. [Google]
- Price: included in Workspace Business and Enterprise plans. [Google]
- Limitation: it can only reach data the user who started it can access. DLP for third-party services is "not yet" planned. [Google]

**Gemini Enterprise (formerly Agentspace)**
- Price: Business edition from $21/seat/mo (up to 300 seats); Standard and Plus from $30. Usage beyond quota is billed extra. [cloud.google.com](https://cloud.google.com/gemini-enterprise); [Coworker.ai 2026](https://coworker.ai/blog/gemini-enterprise-pricing)
- Limitation: Business-edition users "can run shared no-code agents but cannot build them." [Sentra 2026](https://www.sentra.app/articles/gemini-enterprise)
- New feature quotas started 2026-08-17. [Google docs, ~2026-09-29](https://docs.cloud.google.com/gemini/enterprise/docs/quotas-and-overages)

**Not verified (6-call cap):** schedule triggers in Copilot Studio and Cowork; scheduling and human-in-loop settings in Gemini Enterprise; Microsoft's "Copilot Autopilot" (announced 2026-09-25), which should be checked.
