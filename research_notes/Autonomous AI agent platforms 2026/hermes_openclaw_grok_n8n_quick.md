# Hermes / OpenClaw / Grok / n8n: quick check (accessed 2026-10-03)

Quick pass: 6 search calls, 2 of them failed (HTTP 429). "Not verified" means the search did not confirm it. It does not mean the feature is missing.

## 1. Nous Research Hermes Agent
- **What it is:** open-source, self-hosted agent framework. It works with many LLMs and runs on local or isolated backends. [github.com/nousresearch/hermes-agent](https://github.com/nousresearch/hermes-agent), [docs](https://hermes-agent.nousresearch.com/docs/)
- **Named agent:** yes, through "profiles" (multi-agent setup). [aibuilderclub, 2026](https://www.aibuilderclub.com/blog/hermes-nous-research-self-improving-agent)
- **Schedule:** yes. Built-in cron takes natural language or cron syntax and runs unattended. There is also a "no-agent" cron mode for watchdogs. [Automation Blueprints](https://hermes-agent.nousresearch.com/docs/guides/automation-blueprints), [buildfastwithai](https://blog.buildfastwithai.com/how-to-automate-tasks-with-hermes-agent)
- **Folder trigger:** not verified.
- **Reporting:** chat, a local file, or messaging platforms.
- **Security:** the docs cover command approval, DM pairing and container isolation. No 2026 CVE turned up in this pass. You are responsible for securing it yourself.
- **Cost:** free software, plus the server and LLM tokens.

## 2. OpenClaw (formerly Clawdbot/Moltbot)
- **What it is:** a self-hosted agent with a ClawHub skills marketplace. [Reddit r/selfhosted, 2026](https://www.reddit.com/r/selfhosted/comments/1r9yrw1/if_youre_selfhosting_openclaw_heres_every/)
- **Schedule, folder trigger, reporting, cost:** not verified in this pass.
- **Security (serious):**
  - CVE-2026-25253 (CVSS 8.8): one-click remote code execution, even against instances bound to localhost. Patched in v2026.1.29. [Conscia](https://conscia.com/blog/the-openclaw-security-crisis/)
  - Exposed instances: Censys counted about 1k growing to 21k+ between Jan 25 and 31, 2026. Maor Dayan found 42,665, of which 93.4% showed authentication bypass. [Conscia](https://conscia.com/blog/the-openclaw-security-crisis/)
  - SecurityScorecard (Feb 2026): 40,214 exposed instances. [Sangfor](https://www.sangfor.com/blog/cybersecurity/openclaw-ai-agent-security-risks-2026)
  - ClawHavoc malware: 824+ malicious skills by Feb 16, 2026. IBM counts 1,100+. [IBM X-Force](https://www.ibm.com/think/x-force/what-openclaw-reveals-about-agentic-ai-security-risks)
  - Evasive malicious skills were still on ClawHub in Feb–May 2026. [Unit 42](https://unit42.paloaltonetworks.com/openclaw-ai-supply-chain-risk/)

## 3. xAI Grok Automations / Tasks
- **What it is:** hosted inside the Grok app and runs only on Grok models. Launched July 16, 2026. [x.ai/news/grok-automations](https://x.ai/news/grok-automations), [AIToolHunt](https://aitoolhunt.co/blog/grok-automations-scheduled-email-tasks-2026)
- **Schedule and triggers:** runs on a schedule or on email/inbox triggers. Run history and controls are included. A folder trigger is not verified. [MindStudio](https://www.mindstudio.ai/blog/grok-automations-scheduled-tasks-email-triggers)
- **Named agent:** no. MindStudio describes it as "lightweight… simple recurring tasks."
- **Reporting:** in-app notifications. Grok Build added scheduled tasks around Sept 2026. [Changelog](https://x.ai/build/changelog)
- **Security and cost:** not verified.

## 4. n8n AI Agent
- **What it is:** a workflow platform, self-hosted or cloud. The AI Agent node works with OpenAI, Anthropic, Ollama and others, and is free on every plan. [CloudZero](https://www.cloudzero.com/blog/n8n-pricing/)
- **Triggers:** schedule and file triggers are standard workflow triggers. The Drive and OneDrive nodes were not re-verified in this pass.
- **Security:**
  - CVE-2026-21858 "Ni8mare" (CVSS 10.0, Jan 2026): unauthenticated takeover through webhooks and file upload, fixed in 1.121.0. [The Hacker News](https://thehackernews.com/2026/01/critical-n8n-vulnerability-cvss-100.html)
  - CVE-2026-25049: remote code execution, fixed in 1.123.17 and 2.5.2. [CSA SG](https://www.csa.gov.sg/alerts-and-advisories/alerts/al-2026-011/)
  - CVE-2026-33660: remote code execution, Mar 30, 2026. [Qualys](https://threatprotect.qualys.com/2026/03/30/n8n-patches-critical-remote-code-execution-vulnerability-cve-2026-33660/)
- **Cost:** Community Edition is free (pay for the server, about $3–7/mo, plus tokens). The self-hosted Business plan is €800/mo for 40k executions. [CloudZero](https://www.cloudzero.com/blog/n8n-pricing/)

## Verdict for a small US tax firm
- **OpenClaw:** avoid for taxpayer data because of its 2026 record.
- **Grok:** a consumer feature that is not built for a regulated workflow.
- **Hermes and n8n:** usable only if self-hosted, patched quickly, never exposed to the internet, and run with only the access each job needs. Keep the LLM provider's data terms in your written information security plan (WISP).
- **Gaps:** these were not checked against a primary source in this pass.
