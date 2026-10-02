# Fax MCP Servers and AI-Agent Fax Integrations (pay-per-fax focus, as of Oct 2026)

Research date: 2026-10-02. Method: live queries of the official MCP Registry API (registry.modelcontextprotocol.io/v0/servers?search=fax), npm and PyPI registry APIs, vendor landing pages scraped with curl, GitHub repo pages via WebFetch, and web search. GitHub's search/repo APIs were blocked in this environment, so star counts and last-commit dates come from rendered GitHub pages or npm publish dates and are incomplete. Firecrawl was out of credits; Glama's API returned nothing.

## 1. Official MCP servers from fax/telecom providers

### Takeaway
Only two big fax/telecom providers ship an official MCP that can send faxes. Fax.Plus has a hosted, fax-specific MCP, but it needs a paid subscription plan. Telnyx has a general SDK "code mode" MCP that can reach its pay-as-you-go Fax API ($0.007/page, no platform fee); it is not fax-specific. ClickSend has an MCP but stopped offering fax to new customers in April 2026. I found no official MCP from Sinch, SignalWire, Notifyre, Documo, iFax or eFax.

### Cited Findings
**Telnyx**
- The old Python `team-telnyx/telnyx-mcp-server` was archived on Sep 29, 2025, marked "DEPRECATED," and had 25 stars. Its tool list covered assistants, call control, messaging, numbers, connections, storage, embeddings and secrets, with **no fax tools**. Auth was the `TELNYX_API_KEY` env var. — [GitHub team-telnyx/telnyx-mcp-server](https://github.com/team-telnyx/telnyx-mcp-server)
- The successor is a Stainless-generated TypeScript MCP at `telnyx-node/packages/mcp-server`. You install it with `npx -y telnyx-mcp@latest` and authenticate with `TELNYX_API_KEY`. It supports `--transport=http` with a Bearer or `x-telnyx-api-key` header. It runs in "Code Mode" with just two tools: a docs-search tool and a code tool, where "agents will write code against the TypeScript SDK, which will then be executed in an isolated sandbox." Its README does not mention fax specifically. Telnyx also offers a remote hosted MCP. — [GitHub telnyx-node mcp-server](https://github.com/team-telnyx/telnyx-node/tree/master/packages/mcp-server)
- npm `telnyx-mcp` is at version 7.24.0, published 2026-09-25, so it is actively maintained. — [npm registry telnyx-mcp](https://registry.npmjs.org/telnyx-mcp)
- The Telnyx Node SDK that the code tool writes against includes `FaxApplications` resources and fax webhooks (`FaxQueued`, `FaxSendingStarted`, `FaxDelivered`, `FaxFailed`, `FaxMediaProcessed`). — [telnyx-node api.md](https://raw.githubusercontent.com/team-telnyx/telnyx-node/master/api.md)
- Telnyx Fax API pricing: "$0.007 a page. Send or receive... Per page, either direction, no monthly fee," "$0 platform fee," with "+ SIP Trunking usage for transmission." Telnyx's own comparison lists the eFax API at $0.10/page (competitor figures from Aug 2026). — [Telnyx Fax API pricing](https://telnyx.com/pricing/fax-api)

**Fax.Plus (Alohi)**
- It runs a hosted MCP at `https://mcp.fax.plus/mcp`. The tools send faxes, receive and search faxes (with page-level download), track delivery, manage contacts and groups, manage fax numbers, and manage the outbox (resend, update, delete). Auth is OAuth on Basic, Premium and Business plans; Personal Access Tokens with scopes are Enterprise-only. The Free plan is excluded, and so are accounts with Advanced Security Controls (HIPAA, PHIPA). Supported clients: Claude, ChatGPT, Perplexity, Gemini, Copilot, and custom agents. — [Fax.Plus MCP page](https://www.fax.plus/mcp)
- The Fax.Plus search snippet called the MCP "Available on Enterprise plans," which conflicts with the page body (Basic and up). — [Fax.Plus MCP search snippet](https://www.fax.plus/mcp)
- Zapier also exposes a Fax.Plus MCP with a send-fax action. — [Zapier Fax.Plus MCP](https://zapier.com/mcp/faxplus)

**ClickSend / Sinch**
- ClickSend offers an MCP server for sends, stats and contacts. However, "as of April 24, 2026, ClickSend is no longer offering fax to new customers." — [ClickSend Electronic Fax](https://www.clicksend.com/us/fax/) (via search summary)
- Sinch has a Fax REST API and an npm SDK `@sinch/fax` (v1.6.0, published 2026-09-23). I found no Sinch fax MCP. — [Sinch Fax API reference](https://developers.sinch.com/docs/fax/api-reference); [npm search](https://registry.npmjs.org/-/v1/search?text=fax%20mcp&size=40)
- SignalWire offers a programmable fax API but has no fax MCP that I could find. — [SignalWire Fax docs](https://developer.signalwire.com/fax/)

### Inferences
- Telnyx's code-mode MCP should be able to send a fax, because the agent writes SDK code (e.g., `client.faxes.create(...)`) and the SDK has fax resources. But it is a general tool with full-account power: it can buy numbers, place calls, and so on. Running it unattended for fax is riskier than using a narrow fax-only server.
- Fax.Plus fails the user's constraint: it requires a monthly paid plan.
- Telnyx outbound faxes need a Telnyx number and a Fax Application/connection. Number rental likely carries a small monthly fee, so Telnyx may not be strictly "no monthly fee." Confirm this with the provider-pricing research.

### Gaps
- I could not confirm that the hosted Telnyx remote MCP exposes fax. The README doesn't list per-endpoint tools.
- I found no sources at all on MCPs from Notifyre, Documo, iFax or eFax. Searches returned only their Zapier apps or nothing.
- I could not verify whether ClickSend's MCP ever had fax tools.

## 2. Community / third-party fax MCP servers (registries, GitHub, npm, PyPI)

### Takeaway
By late 2026 there are many **hosted, pay-per-fax MCP connectors** listed in the official MCP Registry. Several fit "no subscription, no minimum" exactly: PromptFax, SingleFax, OhFax, SendaFax, SendThisFax and GotFreeFax. The best open-source local option is `faxdrop-mcp` (MIT, actively released, strong safety features), but it depends on FaxDrop's own plans. PyPI has no fax MCP packages.

### Cited Findings
Results from the official MCP Registry (`registry.modelcontextprotocol.io/v0/servers?search=fax`, queried 2026-10-02). All are remote (hosted HTTP) servers unless noted. — [MCP Registry API query](https://registry.modelcontextprotocol.io/v0/servers?search=fax&limit=100)

| Registry name | Endpoint | Registry updated | Coverage / pricing (from vendor site) |
|---|---|---|---|
| app.promptfax/promptfax | https://promptfax.app/mcp | 2026-05-30 | "$2.00 for the first 5 pages, then $0.10 per page after that, capped at $4.50"; no account, "we don't do subscriptions"; charges only on delivery; PDF/JPG/PNG; Stripe — [promptfax.app](https://promptfax.app) |
| com.singlefax/mcp (v1.1.0) | https://singlefax.com/mcp | 2026-09-03 | "Send a One-Time Internet Fax. $0.99, No Subscription... for up to 10 pages. Pay only when" delivered; US/Canada/Puerto Rico; optional receive numbers ($4.99/30 days, $97 lifetime) and team plans from $9.99/mo — [singlefax.com](https://singlefax.com) |
| com.ohfax/ohfax | https://app.ohfax.com/mcp | 2026-09-20 | "$0.99 + $0.25 / page. Pay per fax. No subscription, no monthly minimum"; US/CA; PDF ≤10 MB / 30 pages; 1 page $1.24, 10 pages $3.49; full refund if undeliverable; docs deleted in 24h; registry says "pay via MPP, get delivery receipt" — [ohfax.com](https://www.ohfax.com) |
| ai.sendafax/sendafax (v1.0.1) | https://sendafax.ai/api/mcp | 2026-08-29 | Australia (+61) only; "USD $1 per page, or 11 pages for $10. Charged only after delivery"; last mile is Notifyre; tools include `get_coverage` (no login) and `send_fax` (destination, file or body, receipt_email) — [sendafax.ai](https://sendafax.ai) |
| com.sendthisfax/fax | https://www.sendthisfax.com/mcp | 2026-07-08 | EU institutions; pay per fax via one-time checkout link (no account/subscription) or a prepaid API key for autonomous mode; tools `get_price`, `send_fax`, `get_fax_status`, `check_balance`; auto refund on failure; `claude mcp add --transport http sendthisfax https://www.sendthisfax.com/mcp --header "Authorization: Bearer stf_live_..."` — [sendthisfax.com/en/mcp](https://www.sendthisfax.com/en/mcp) |
| com.gotfreefax/mcp (v1.0.1) | https://www.gotfreefax.com/mcp | 2026-06-07 | US/Canada; repo github.com/vannet/gotfreefax-mcp; free faxes (3 pages, email confirmation) or paid faxes (up to 300 pages), status checks, prepaid credits via PayPal; free tier needs no account — [search result / claudemarketplaces](https://claudemarketplaces.com/mcp/com.gotfreefax/mcp); [MCP Registry](https://registry.modelcontextprotocol.io/v0/servers?search=fax&limit=100) |
| com.edwyna/fax (v0.2.0) | https://edwyna.com/mcp | 2026-08-17 | "$4 per delivered fax," "Powered by FaxZero," prepaid accounts only, per-key sending and spending limits, failed faxes restore credit — [edwyna.com](https://edwyna.com) |
| com.noerrands/fax | https://api.noerrands.com/c/fax/mcp | 2026-09-24 | US/Canada fax from PDF, "quoted per page before sending"; fax "$1.49 first page"; prepaid credits with one API key shared across 8 "errands"; asks before every paid action — [noerrands.com](https://noerrands.com) |
| com.faxify/mcp | https://mcp.faxify.com/api/v1/mcp | 2026-09-19 | Send, receive and track faxes in US/Canada; OAuth 2.1; pricing not captured — [Faxify MCP](https://mcp.faxify.com/en); [Glama listing](https://glama.ai/mcp/connectors/com.faxify/mcp) |

Not fax senders, despite matching "fax" in the registry: `io.github.AKzar1el/nofax` (a human-in-the-loop approvals MCP), `com.faxlineindex`, `com.firmfax`, `com.housingfax`, `com.macfax`. — [MCP Registry API query](https://registry.modelcontextprotocol.io/v0/servers?search=fax&limit=100)

**Open-source / self-hosted**
- **faxdrop-mcp** (klodr/faxdrop-mcp): MIT license, npm `faxdrop-mcp` latest 0.10.1 published 2026-09-26, 5 stars, 210 commits, CI and CodeQL. Tools: `faxdrop_send_fax` (PDF/DOCX/JPEG/PNG ≤10 MB to E.164), `faxdrop_pair_number` (recipient allowlisting), `faxdrop_get_fax_status`. Provider is FaxDrop, which has a free tier of 2 faxes/month plus paid plans. — [GitHub klodr/faxdrop-mcp](https://github.com/klodr/faxdrop-mcp); [npm faxdrop-mcp](https://registry.npmjs.org/faxdrop-mcp); [mcp.so listing](https://mcp.so/server/faxdrop-mcp/klodr)
- **Faxbot** (DMontgomery40/Faxbot): MIT license, 10 stars, 231 commits. It is a self-hosted fax API with backends for Phaxio, Sinch, SignalWire, Documo, FreeSWITCH and SIP/Asterisk. It ships `faxbot-mcp` and `faxbot-mcp-sse` (stdio, HTTP and SSE transports), plus an admin console and HIPAA-aligned controls. Last-commit date was not visible. — [GitHub DMontgomery40/Faxbot](https://github.com/DMontgomery40/Faxbot)
- **ictfax-mcp** (npm 0.1.0, published 2026-09-01): an MCP for the ICTFax platform that lists and tracks faxes and, "with writes enabled," uploads documents and sends. Repo: github.com/ictinnovations/ictfax-mcp. — [npm search](https://registry.npmjs.org/-/v1/search?text=fax%20mcp&size=40)
- PyPI: `fax-mcp`, `mcp-fax`, `faxplus-mcp`, `sinch-mcp` and `telnyx-mcp-server` all return 404. No Python fax MCP packages were found under these names. — [PyPI JSON API checks](https://pypi.org/pypi/fax-mcp/json)
- `interfax` npm (InterFAX SDK) was last published 2024-02-16. It is an SDK, not an MCP. — [npm search](https://registry.npmjs.org/-/v1/search?text=fax%20mcp&size=40)

### Inferences
- **Lowest friction for Claude.ai or Claude Desktop with no account:** PromptFax ($2 to $4.50) or OhFax ($0.99 + $0.25/page) as remote connectors. Both charge only on delivery. The human pays at checkout, which doubles as a built-in confirmation step.
- **Cheapest per fax among hosted MCPs for US/CA:** SingleFax ($0.99 for up to 10 pages) and OhFax ($1.24 for 1 page). Even these cost about 100x more per page than raw Telnyx ($0.007/page), because you are paying for convenience and for having no account.
- **For autonomous sends with no checkout link:** SendThisFax (EU, prepaid key), Edwyna ($4, prepaid), NoErrands (prepaid credits) and GotFreeFax (prepaid PayPal credits). Prepaid credit is a deposit, so check whether each has a minimum top-up.
- Most of these hosted connectors were first registered between May and September 2026. They are new, small vendors with no track record, so check privacy and HIPAA terms before faxing sensitive documents. Only Faxbot and SingleFax mention HIPAA, and SingleFax only for its BAA team plans.

### Gaps
- I could not get GitHub stars or last-commit dates for vannet/gotfreefax-mcp, Faxbot or ictfax-mcp (GitHub API blocked).
- I could not retrieve listings from smithery.ai, pulsemcp.com or glama.ai search. Glama returned connector pages via search only, for Faxify, PromptFax, SingleFax and SendaFax.
- Pricing for Faxify, GotFreeFax paid tier, and FaxDrop paid plans was not captured.
- Minimum top-up amounts for the prepaid services (Edwyna, NoErrands, SendThisFax, GotFreeFax) are unknown.

## 3. Integration platforms exposing fax as agent tools

### Takeaway
Zapier MCP and Pipedream (Connect/MCP) expose fax actions from several providers. Both platforms carry their own pricing on top of the fax provider's, and many of the providers behind them are subscription-based (Fax.Plus, Documo, iFax). Composio has toolkits for Telnyx and ClickSend but none dedicated to fax.

### Cited Findings
- Zapier MCP pages exist (HTTP 200) for faxplus, documo, ifax, sinch and telnyx. Pages for notifyre, efax and clicksend-sms return 404. — [zapier.com/mcp/faxplus](https://zapier.com/mcp/faxplus); [zapier.com/mcp/documo](https://zapier.com/mcp/documo); [zapier.com/mcp/ifax](https://zapier.com/mcp/ifax)
- The Zapier Fax.Plus MCP's action is to send a fax from your FAX.PLUS account. — [Zapier Fax.Plus MCP](https://zapier.com/mcp/faxplus)
- Documo on Zapier has a "new fax received" trigger and supports sending faxes. — [Documo Zapier integrations](https://zapier.com/apps/documo/integrations); [Documo help](https://help.documo.com/hc/en-us/articles/26697865641755-Zapier-Integration)
- Zapier has a fax app category. — [Zapier fax apps](https://zapier.com/apps/categories/fax)
- Pipedream has a pre-built "Send Fax" action for Phaxio (now part of Sinch), usable "through the Pipedream Connect SDK, API, or MCP." Pipedream app pages also exist for sinch, signalwire, telnyx and clicksend. — [Pipedream Phaxio Send Fax](https://pipedream.com/apps/phaxio/actions/send-fax)
- Composio toolkit pages exist for telnyx and clicksend. Pages for faxplus, documo, sinch, signalwire, ifax, notifyre and phaxio return 404. — [composio.dev/toolkits/telnyx](https://composio.dev/toolkits/telnyx); [composio.dev/toolkits/clicksend](https://composio.dev/toolkits/clicksend)

### Inferences
- Whether Composio's Telnyx toolkit has a fax action is unverified. Even if it does, Composio and Zapier add platform-side metering (tasks or tool calls) on top of fax cost.
- For a strict pay-per-fax, no-subscription goal, these platforms add a second bill and a second vendor without lowering fax cost. A direct hosted fax MCP or a small custom MCP is simpler.

### Gaps
- I did not retrieve Zapier MCP and Pipedream Connect pricing (task or credit cost per tool call, free-tier limits). I also did not see the specific fax action lists inside Composio's Telnyx and ClickSend toolkits.
- n8n and Make: I found no fax-specific agent tooling in this pass. Both can call any fax REST API through an HTTP node, but this is unverified.

## 4. Writing a small custom MCP server for the cheapest pay-per-fax API

### Takeaway
A custom fax MCP is a small job: roughly 100 to 200 lines and half a day to a day, including safety controls. The provider REST API is a single "create fax" POST plus a "get fax" GET. Good existing templates are faxdrop-mcp (safety patterns) and Faxbot (multi-provider).

### Cited Findings
- Telnyx's fax lifecycle is exposed as webhooks (`FaxQueued` → `FaxSendingStarted` → `FaxDelivered` / `FaxFailed`) and as Fax Application resources in the official SDK. — [telnyx-node api.md](https://raw.githubusercontent.com/team-telnyx/telnyx-node/master/api.md)
- Telnyx bills $0.007 per page with no platform fee, plus SIP trunking usage. — [Telnyx Fax API pricing](https://telnyx.com/pricing/fax-api)
- Existing hosted servers converge on the same small tool surface: `get_price`/quote, `send_fax`, `get_fax_status` and `check_balance` (SendThisFax), and `get_coverage` and `send_fax` (SendaFax). — [SendThisFax MCP](https://www.sendthisfax.com/en/mcp); [sendafax.ai](https://sendafax.ai)
- faxdrop-mcp shows the full safety pattern in a small codebase: dry-run env flag, outbox directory jail, E.164 validation, 10 MB cap, recipient pairing/allowlist, and JSONL audit log. — [GitHub klodr/faxdrop-mcp](https://github.com/klodr/faxdrop-mcp)
- npm `@modelcontextprotocol/sdk` (v1.31.0, Sep 2026) and `fastmcp` (TypeScript) are current server frameworks. — [npm search](https://registry.npmjs.org/-/v1/search?text=fax%20mcp&size=40)

### Inferences (outline, not sourced from a single doc)
- **Stack:** Python FastMCP (`mcp` package) or the TypeScript MCP SDK. Run it locally over stdio for Claude Code or Claude Desktop. For a claude.ai custom connector it must be deployed as a remote HTTP server, e.g., on Cloud Run or a Worker, with auth.
- **Tools:**
  - `quote_fax(to, page_count)`: computes cost locally.
  - `send_fax(to, pdf_url | file_path, confirm_token)`: validates E.164 and the allowlist, uploads the file to a public or presigned URL if the provider needs a `media_url`, calls the provider's create-fax endpoint, and returns the fax ID.
  - `get_fax_status(fax_id)`: GET the fax by ID.
  - Optional: `list_recent_faxes`.
- **Telnyx specifics to verify against docs:** sending likely needs `connection_id` (Fax Application), `from` (a Telnyx number), `to`, and `media_url` or uploaded media. A Telnyx number is required, and its rental may be a monthly fee.
- **Effort:** core tools take 1 to 2 hours. Adding allowlist, dry-run, logging, a confirmation step and file handling brings it to about half a day. A hosted remote connector with OAuth adds roughly another day.

### Gaps
- I did not fetch Telnyx's "Send a fax" API reference, so I did not verify exact parameter names. I also did not verify the cost of the required Telnyx number.
- I did not compare custom-build options for other low-cost pay-as-you-go APIs (Sinch, SignalWire, Notifyre). That belongs to the provider-pricing research.

## 5. Safety for agent-sent faxes (confirmation, allowlist, logging)

### Takeaway
Faxes are irreversible and cost money, so agent setups should combine four things: a human confirmation step, a recipient allowlist, dry-run or quote-before-send, and audit logs. Several hosted connectors build these in through checkout links, spend limits, and "ask before acting" behavior.

### Cited Findings
- faxdrop-mcp offers number gating (open, pairing or closed modes) with country and number-type allowlists, `FAXDROP_MCP_DRY_RUN=true`, a JSONL audit log (file mode 0600) that redacts all but whitelisted fields, an outbox directory jail, and TOCTOU-safe file reads. — [GitHub klodr/faxdrop-mcp](https://github.com/klodr/faxdrop-mcp)
- SendThisFax's default mode returns a one-time payment link, so "you only click the payment link." That is human approval by design. Its prepaid API-key mode skips the link for autonomous sends. — [SendThisFax MCP](https://www.sendthisfax.com/en/mcp)
- PromptFax opens a Stripe payment panel before sending and charges only on delivery. — [promptfax.app](https://promptfax.app)
- Edwyna enforces "Per-key sending and spending limits" and requires an authorized API key for every fax. — [edwyna.com](https://edwyna.com)
- NoErrands lists actions that are always confirmed: "Muse cannot invent a recipient, a fax number, or your contact details. If your credits run out, it stops and gives you a top-up link instead of retrying." Every price is shown before approval. — [noerrands.com](https://noerrands.com)
- SendaFax tells agents: "There is no default number"; it is "Not a blast tool." — [sendafax.ai](https://sendafax.ai)
- The MCP Registry lists `nofax`, a local stdio MCP for human-in-the-loop approvals and notifications for AI coding agents, which could be paired with a fax tool. — [MCP Registry API query](https://registry.modelcontextprotocol.io/v0/servers?search=fax&limit=100)
- Fax.Plus excludes accounts with HIPAA/PHIPA Advanced Security Controls from MCP use. — [Fax.Plus MCP page](https://www.fax.plus/mcp)

### Inferences
- In Claude Code, keep the send tool out of auto-approve permissions so every `send_fax` call prompts the user. Allow only `quote` and `status` without prompting.
- Recommended controls for a custom server:
  - Allowlist recipient numbers in config.
  - Cap pages and daily spend.
  - Make `send_fax` require a confirmation token returned by a prior `quote_fax`, so it is a two-step call.
  - Log the number, page count, document hash and provider ID; do not log document content.
  - Delete uploaded media after the final status.
- For PHI or tax documents, avoid new hosted connectors that have no BAA. Prefer a provider that offers HIPAA terms (Telnyx states HIPAA on its pricing page) with a self-hosted MCP. — [Telnyx Fax API pricing](https://telnyx.com/pricing/fax-api)

### Gaps
- I found no independent security reviews or audits of any hosted fax MCP connector.
- I did not verify whether Claude.ai custom connectors offer per-tool confirmation settings for remote MCP tools.
