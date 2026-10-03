# Claude vs OpenAI: unattended named agents (quick check, 2026-10-03)
All sources accessed 2026-10-03. "n/v" = not verified in the 6 lookups.

## Anthropic
**Claude Code routines (cloud)**: the closest fit
- Named: yes. Each routine is given a descriptive name. [code.claude.com/docs/en/routines]
- Triggers: schedule, API call, GitHub event. No file or folder trigger. [same]
- Computer off: yes, runs on Anthropic cloud. [code.claude.com/docs/en/desktop-scheduled-tasks]
- Approvals: none. Runs as a full autonomous cloud session. [routines doc]
- Reports: session log, PRs, and connector messages (e.g. Slack). [routines doc]
- Plan: Pro, Max, Team, Enterprise. Still a research preview, with hourly run caps. [routines doc]

**Claude Cowork scheduled tasks**
- Schedule: yes. Cloud tasks run while the computer is asleep or the app is closed. [support.claude.com/en/articles/13854387]
- Folder: you can point a task at a folder, but then it runs only while the computer is awake. No file-arrival trigger. [aiblewmymind.substack.com/p/claude-cowork-cloud-scheduled-tasks]
- Limitation: cloud tasks cannot see local files. [same]
- Named agent, approvals, reporting, price: n/v.

**Claude Managed Agents (API)**
- Price: API token rates plus $0.08 per active session-hour. Idle time is free. [truefoundry.com/blog/claude-managed-agents-pricing (2026); finout.io blog]
- Triggers: your own code starts runs. No native schedule or folder trigger found (n/v).
- Criticism: costs are billed in 3 dimensions at once (tokens, cache, runtime). [finout.io]

## OpenAI
**ChatGPT scheduled tasks (+ agent)**
- Named agent: no. These are tasks, not agents, and Custom GPTs cannot run in them. [help.openai.com/en/articles/10291617]
- Schedule: yes, hourly at most on paid plans. Event-triggered tasks also exist, with app events as the source. [help.openai.com; learn.chatgpt.com/docs/automations]
- Folder: no native folder trigger. Tasks inside a project cannot read that project's files. [help.openai.com]
- Approvals: in full-access sandbox mode, background tasks change files and run commands without asking. [learn.chatgpt.com]
- Active-task caps: Free/Go 3, Plus 5, Business/Edu 10, Pro/Enterprise 15. The page also says tasks are "not available on Free or Go", which contradicts the caps. [help.openai.com]
- Criticisms: tasks pause automatically when ignored and mostly just send notifications [usecarly.com/blog/chatgpt-scheduled-tasks]. A vendor blog headline (Jun 22, 2026) says "ChatGPT Agent Mode Is Gone" (n/v).

**Agent Builder / AgentKit**
- OpenAI is winding it down and it shuts off **Nov 30, 2026** (notice dated Jun 3, 2026). [openai.com/index/introducing-agentkit; developers.openai.com/api/docs/guides/agent-builder]
- Native schedule or folder trigger: none found. Do not build on it.

## Bottom line
- Only Claude Code cloud routines confirm all of these: named, scheduled, unattended, runs with the computer off, reports automatically.
- No product has a native file-arrival trigger. The workaround is a sync script that calls the routine's API trigger.
