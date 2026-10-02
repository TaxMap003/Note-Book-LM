# Cheapest Truly Pay-Per-Use Online Fax Services (US, API-capable preferred) — as of Oct 2026

Research date: 2026-10-02. Prices are from official pages where possible, fetched on that date. Third-party sources are flagged with their date. Method note: the Firecrawl tool had no credits left, so pages were read with WebFetch/WebSearch. Some numbers come from search-result summaries of official pages rather than a full page read; those are flagged.

## Q1. Ranked shortlist: price per page, minimum top-up, credit expiry, whether a number is needed, API, cost for 1x3 pages and 10x3 pages/month

### Takeaway
For a firm that faxes now and then and wants to send from code, **Notifyre** fits best. It charges $0.03/page to send, has no monthly fee, needs a **$10 minimum top-up**, credits never expire, it can send without renting a number, and it offers both a REST API and email-to-fax. **Telnyx** is cheapest per page ($0.007), but its own docs say you need a fax-enabled Telnyx number, which costs $1.00/month. So Telnyx is not truly free of monthly fees. It also requires a $10 minimum payment. No API-capable option has a $0 minimum. The lowest real minimums found are FaxSalad at $5 and SignalWire at $5 (which also comes with $5 of free trial credit).

### Cost table (US domestic sending; "1 fax" = 3 pages; "10 faxes" = 30 pages/month)

| Rank | Service | Send price | Min top-up / deposit | Monthly fee | Number needed to send? | API | 1 fax x 3 pp | 10 faxes x 3 pp / mo | Cash needed upfront |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **Notifyre** (PAYG) | $0.03/page | **$10** | $0 | No (send-only works with no number) | REST API + email-to-fax + web | $0.09 | $0.90 | $10 |
| 2 | **Telnyx Programmable Fax** | $0.007/page (send and receive) | **$10** minimum payment | **$1.00/mo for the number** (required) | **Yes**, per Telnyx docs | REST API + email-to-fax | $0.021 + $1.00 number = ~$1.02 | $0.21 + $1.00 = ~$1.21 | $10 |
| 3 | **SignalWire Fax** | $0.0095 **per minute** (48 states). Roughly $0.01-0.03 for 3 pages, estimated | **$5** manual top-up to leave trial. Auto top-up defaults to a $10 minimum | Number likely needed. Rental price not verified | Likely yes (not verified) | REST/LaML API | ~$0.03 + number | ~$0.30 + number | $5 (plus $5 free trial credit) |
| 4 | **FaxSalad** (PAYG) | $0.08/page (receive $0.03/page) | **$5** | $0 on PAYG | Not verified | Not verified | $0.24 | $2.40 | $5 (10 free pages first) |
| 5 | **Sinch Fax** (ex-Phaxio) | **$0.045/page** (Sinch official page); third party (Jul 2026) says $0.07/page | Not published | Number $2/mo (third party) | Third party says No | REST API | $0.135-$0.21 | $1.35-$2.10 | Unknown |
| 6 | **Fax.Plus** (Free plan + credits) | $0.20/page US/CA | **$10** | $0 | No (Free plan sends) | Web/mobile. API access on the Free plan not verified | $0.60 | $6.00 | $10 |
| 7 | **FaxZero** (free tier) | Free: max 3 pages + cover, 5 free faxes/day, FaxZero branding on cover | $0 | $0 | No | **No API** (web form) | $0.00 | $0.00 (within limits) | $0 |
| 8 | **FaxZero** (paid) | **$3.29 per fax** (PayPal), up to 25 pages, no branding | $0 (pay each fax) | $0 | No | No API | $3.29 | $32.90 | $3.29 |
| 9 | **GotFreeFax** (free tier) | Free: max 3 pages, 2 free faxes/day, ad-free cover | $0 | $0 | No | No API | $0.00 | Only 2/day, so 10/month works if spread out | $0 |
| 10 | **iFax** pay-per-fax | "As low as $1.99 per page" | Not stated | $0 claimed, but pushes a 1-year subscription | No | iFax API is on subscription plans | ~$5.97 | ~$59.70 | ~$6 |

Excluded by the hard filters (monthly fee, discontinued, or no fax API): Faxage, Documo/mFax, Dropbox Fax (HelloFax), ClickSend (fax retired), Twilio (dead), Vonage API (no fax), Bandwidth/Plivo (SIP/T.38 only, no PAYG fax REST API found). Details are in Q2.

### Cited Findings

**Notifyre**
- Send is "$0.03 per fax page", pay as you go, no subscription or contracts. Minimum top-up is $10. Credits never expire. No free trial; you must fund $10 to start. — [Notifyre Online Fax](https://notifyre.com/us/online-fax)
- Web, email-to-fax gateway and Fax API are all offered. HIPAA compliant with a free BAA. ISO 27001. AES-256 in transit and at rest. — [Notifyre Online Fax](https://notifyre.com/us/online-fax)
- Receiving needs a plan, starting at $4.90/month for one fax number and 200 incoming pages. — [Notifyre Online Fax](https://notifyre.com/us/online-fax)
- A third-party comparison lists Notifyre as $0.03/page, $10 deposit, number not required to send. (mfax.to is a competing fax vendor's blog, dated Jul 10, 2026.) — [mfax.to Fax API Pricing 2026](https://mfax.to/blog/fax-api-pricing/)

**Telnyx**
- "$0.007 per page" for sending and receiving, no monthly fee for fax usage itself. Numbers are "$1.00 / NUMBER/MO". Committed-volume pricing starts at $500/mo, which is optional. — [Telnyx Fax pricing](https://telnyx.com/pricing/fax)
- Prerequisites: "create a Telnyx account, phone number, and Fax Application". The `from` field is "the phone number, in E.164 format, the fax will be sent from". You also need a connection/app ID. — [Telnyx Send a Fax via API](https://developers.telnyx.com/docs/programmable-fax/send-a-fax-api)
- Conflict: mfax.to (Jul 2026) says Telnyx does not need a number to send, adds "+ SIP fees", and lists numbers at $2-4/mo. Telnyx's official docs and pricing page contradict this. Trust the official sources. — [mfax.to](https://mfax.to/blog/fax-api-pricing/)
- Minimum payment is $10 USD for top-ups. New users can pay up to $100 on day one, and that limit rises $50/day. Bitcoin payments have a $100 minimum. "Freemium" accounts cannot top up and must upgrade to a full account first, which means account verification. (From a search summary of Telnyx support pages.) — [Telnyx Billing Setup](https://support.telnyx.com/en/articles/4280500-billing-setup-billing-groups); [Telnyx Freemium Accounts](https://support.telnyx.com/en/articles/14327893-telnyx-pretrial-accounts)
- Email-to-fax is documented. — [Telnyx email to fax docs](https://developers.telnyx.com/docs/programmable-fax/email-to-fax)

**SignalWire**
- US fax is billed per minute: inbound $0.0095/min, outbound to the 48 contiguous states $0.0095/min, Alaska $0.0950/min, Hawaii $0.0550/min. The fax pricing page does not show number rental. — [SignalWire Fax pricing](https://signalwire.com/pricing/fax)
- New accounts get $5.00 of free credit and start in trial mode. A manual top-up of $5.00 ends trial mode. When a card is added, auto top-up turns on with a $10 minimum. (From a search summary of SignalWire docs.) — [SignalWire Billing / trial mode](https://developer.signalwire.com/platform/dashboard/guides/trial-mode/); [SignalWire auto top-up](https://developer.signalwire.com/guides/how-to-set-auto-top-up-by-credit-card)

**Sinch Fax (formerly Phaxio)**
- Official page: "Flat rate of $0.045 per page, with transparent pricing and no hidden charges". Offers "Try for free" (terms not shown), local/toll-free numbers or bring your own, HIPAA support. — [Sinch Fax API](https://sinch.com/voice/fax-api/)
- Conflict: a third party (Jul 2026) lists Phaxio/Sinch at $0.07/page US, number $2/mo, $0 monthly minimum, number not required to send, BAA included at no extra charge. — [mfax.to](https://mfax.to/blog/fax-api-pricing/)
- The official pricing URL (sinch.com/pricing/fax/) redirected to a contact-form "thank you" page, so a full rate card could not be checked. — [Sinch pricing URL](https://www.sinch.com/pricing/fax/)

**FaxSalad**
- US send is $0.08/page, receive $0.03/page. 10 free pages to try. Optional monthly plans: $10 (150 pages) and $20 (450 pages). — [FaxSalad pricing](https://faxsalad.com/pricing) (via search summary)
- $5 minimum top-up on PAYG. — [onefaxnow FaxSalad alternative page](https://onefaxnow.com/alternatives/faxsalad); [comfax one-time fax review, Jul 24 2026](https://comfax.com/reviews/top-one-time-fax-options/)

**Fax.Plus (Alohi)**
- Free plan per-page cost is $0.20 for US/Canada. Smallest top-up is $10. "Credit never expires and carries over month to month". No subscription. — [Alohi Help Center](https://help.alohi.com/hc/en-us/articles/11177827425180-Can-I-buy-extra-fax-pages-or-credits-on-the-Free-plan-Pay-as-you-go)
- Some third-party sources list an $8.99 minimum. The official help center says $10. — [search summary of Fax.Plus third-party pages](https://emitrr.com/blog/faxplus-pricing/)

**FaxZero**
- Free: max 3 pages plus cover page, "Max 5 free faxes per day", FaxZero branding on the cover. Paid: "$3.29 per fax (PayPal)", max 25 pages plus optional cover, no branding. — [FaxZero](https://faxzero.com/)
- 2024-2026 change: the paid fax now costs $3.29. The user remembered about $2/fax, so the price has gone up. The exact date of the increase was not found.

**GotFreeFax**
- Free: "3 pages per fax maximum", "2 free faxes per day maximum". The cover page is free and ad-free. Paid pay-per-fax handles up to 30 pages with priority delivery. Prepaid page credits "never expire", no monthly fee. — [GotFreeFax](https://www.gotfreefax.com/)

**iFax**
- Pay-per-fax "as low as $1.99 per page", "no monthly subscriptions". — [iFax Pay Per Fax](https://www.ifaxapp.com/one-time-fax/)
- Caution: a review says "iFax will try to sign you up for a 1-year faxing subscription" when you use its one-time option. — [comfax, Jul 24 2026](https://comfax.com/reviews/top-one-time-fax-options/)
- iFax Pro is $25/mo with $0.01/page overage (third party). — [mfax.to](https://mfax.to/blog/fax-api-pricing/)

### Inferences
- **Real minimum cash outlay:** Notifyre $10, Telnyx $10, Fax.Plus $10, FaxSalad $5, SignalWire $5 (with $5 free credit). FaxZero/GotFreeFax free tiers need $0. No API-capable provider found has a $0 minimum. Notifyre's $10 at $0.03/page covers about 333 pages, which is roughly 11 months at 10 faxes x 3 pages per month. Credits do not expire, so the $10 is effectively spent on faxes, not lost.
- **Telnyx's "no monthly fee" claim does not hold for sending**, because its docs need an owned number at $1/mo. Over a year that is about $12 in number rent plus a few cents per fax. At 10 faxes/month Telnyx (~$14.50/yr) costs more than Notifyre (~$10.80/yr). Telnyx only wins at high volume, or if the firm already rents a Telnyx number for something else.
- SignalWire bills per minute, so cost depends on transmission time (often about 30-60 seconds per page). The 3-page estimate above is approximate.
- For tax PII, Notifyre (BAA, encryption, ISO 27001) and Sinch (HIPAA, BAA) are much easier to defend under the FTC Safeguards Rule than free consumer web forms.

### Gaps
- Whether SignalWire fax can send without a SignalWire-owned number, and its number rental price: not verified.
- Sinch's minimum deposit, trial credit size, and whether $0.045 or $0.07/page is the current US rate: the official pricing page could not be read.
- Whether FaxSalad has a public API: not verified.
- Whether the Fax.Plus Free plan plus credits includes REST API access: not verified (Fax.Plus API is usually on business/enterprise plans).
- GotFreeFax paid per-fax and prepaid credit prices: the pricing page returned 404.
- KYC friction: Telnyx needs a full (non-Freemium) account to top up. Other providers' identity checks were not documented in the sources found.
- No Reddit or HN reports of hidden minimums were gathered, because the tool-call budget ran out.

## Q2. Candidates that fail the filters, discontinued services, and 2024-2026 changes

### Takeaway
Several well-known names are out. **ClickSend has retired fax for new customers.** **Twilio Fax has been dead since Dec 17, 2021.** The **Vonage API has no fax.** Faxage, Documo/mFax and Dropbox Fax all charge monthly fees. **FaxZero's paid fax rose to $3.29.** HelloFax is now Dropbox Fax (rebranded 2024).

### Cited Findings
- **ClickSend**: "Fax has finally retired — it's no longer available to new customers". The page points people to Sinch's fax API instead. — [ClickSend US pricing](https://www.clicksend.com/us/pricing/us/)
- **Twilio**: Programmable Fax access was turned off for all accounts on December 17, 2021, and API calls fail after that date. — [Twilio changelog](https://www.twilio.com/en-us/changelog/programmable-fax-end-of-life-one-year-notice); [Twilio support](https://support.twilio.com/hc/en-us/articles/223136667-Fax-Support-on-Twilio)
- **Faxage**: cheapest plan is Lite at $3.49/month plus $5.00 setup, with $0.05/minute usage. No send-only option. API and email-to-fax included. Fails the no-monthly-fee filter. — [Faxage pricing](https://www.faxage.com/pricing.php)
- **Documo (mFax)**: Solo Cloud Fax is $25/month billed annually (300 pages, 1 number), with $0.15/page overage. API is an add-on. Fails the filter. — [Documo pricing](https://www.documo.com/pricing). Note: "mfax.to" is a different vendor (says about $9/mo, about $0.04/page) and is not Documo's mFax. — [mfax.to](https://mfax.to/blog/fax-api-pricing/)
- **Dropbox Fax (formerly HelloFax)**: rebranded in 2024. hellofax.com 301-redirects to fax.dropbox.com. Paid plans start at $9.99/month. — [search summary citing fax.plus / documo / fax-flow reviews](https://www.documo.com/blog/hellofax-vs-myfax-vs-documo-comparison/)
- **FaxBurner**: 5 free send pages (one-time) and 25 receive pages/month on the free tier. Current paid pricing not found. — [search summary, comfax free-fax review](https://comfax.com/reviews/free-fax/)
- **PamFax**: listed with 3 free pages one-time. No confirmed 2025/2026 status or pricing found. — [saasworthy PamFax alternatives](https://www.saasworthy.com/product-alternative/30236/pamfax)
- **Vonage**: "The Vonage API platform does not support Fax, including Fax over IP, or the T.38 codec." — [Vonage API support](https://api.support.vonage.com/hc/en-us/articles/360038592671-Can-I-send-fax-over-the-Vonage-Voice-API)
- **Plivo**: Zentrunk SIP trunking does not support T.38 fax. No Plivo PAYG fax REST product was found. — [Plivo support](https://support.plivo.com/hc/en-us/articles/360041479991-Does-Plivo-Zentrunk-SIP-trunking-support-T-38-fax-)
- **Bandwidth**: supports fax only as T.38 over its voice/SIP network. This needs your own fax server, not a simple per-page REST fax API. — [Bandwidth T.38 guide](https://support.bandwidth.com/hc/en-us/articles/204251956-Bandwidth-T-38-faxing-support-guide)

### Inferences
- With Twilio and ClickSend gone, the realistic developer-grade PAYG fax APIs in 2026 are Telnyx, Sinch (Phaxio), SignalWire and Notifyre.
- ClickSend now refers fax customers to Sinch, which suggests Sinch is consolidating the SMB fax API market.

### Gaps
- Exact date of FaxZero's increase to $3.29.
- Whether Plivo still sells any fax product at all. Plivo's marketing mentions "fax" in some third-party lists, but nothing official was found.

## Q3. Free options (FaxZero, GotFreeFax) for client tax PII, IRS Pub 4557 / FTC Safeguards Rule, and online Forms 2848/8821

### Takeaway
Free web-form fax services work for occasional non-sensitive documents. They are a poor fit for client tax PII: there is no BAA or contract, no API, retention and privacy terms are unclear (FaxZero's privacy page returned 404), and FaxZero puts its branding on the free cover page. Under IRS Pub 4557 and the FTC Safeguards Rule (which requires a written information security plan), a firm should use a vendor with encryption and contractual safeguards. More importantly, the IRS now accepts **Forms 2848 and 8821 online** (Submit Forms 2848/8821 Online, and Tax Pro Account). So the main reason a tax firm faxes the IRS can often be avoided.

### Cited Findings
- FaxZero free tier: 3 pages plus cover, 5/day, FaxZero branding on the cover. The visible page shows no specific retention or privacy statement. — [FaxZero](https://faxzero.com/)
- GotFreeFax free tier: 3 pages, 2/day, ad-free cover. Retention terms are deferred to its Privacy Policy and Terms. — [GotFreeFax](https://www.gotfreefax.com/)
- IRS Pub 4557 ("Safeguarding Taxpayer Data") sets baseline safeguards for tax professionals: the "Security Six", administrative and physical protections, a written information security plan (WISP), and incident response. — [Intuit Tax Pro Center on Pub 4557](https://accountants.intuit.com/taxprocenter/practice-management/how-to-update-your-tax-firms-data-safeguards-based-on-irs-pub-4557/); [IRS: data security plan](https://www.irs.gov/newsroom/heres-what-tax-preparers-need-to-know-about-a-data-security-plan)
- The IRS page on data security plans says tax preparers must have a written plan (this requirement comes from the FTC Safeguards Rule). — [IRS: data security plan](https://www.irs.gov/newsroom/heres-what-tax-preparers-need-to-know-about-a-data-security-plan)
- Forms 2848/8821 can be filed through **Tax Pro Account** (the client signs digitally in their IRS online account) or **Submit Forms 2848 and 8821 Online** (IRS.gov/Submit2848; needs a Secure Access account). Fax and mail are still accepted, but signatures on faxed or mailed forms must be handwritten. — [IRS: Serve your clients](https://www.irs.gov/tax-professionals/serve-your-clients); [IRS newsroom on Submit Forms 2848/8821 Online](https://irs.gov/zh-hant/newsroom/new-irs-submit-forms-2848-and-8821-online-offers-contact-free-signature-options-for-tax-pros-and-clients-sending-authorization-forms); [Thomson Reuters](https://tax.thomsonreuters.com/news/irs-rolls-out-online-power-of-attorney-and-tax-information-authorization-forms/)
- Notifyre and Sinch both advertise HIPAA compliance with BAAs, and Notifyre adds AES-256 encryption at rest and ISO 27001. These are the kind of vendor controls a WISP can point to. — [Notifyre](https://notifyre.com/us/online-fax); [Sinch Fax API](https://sinch.com/voice/fax-api/)

### Inferences
- Recommended setup for the firm: (1) file POAs/TIAs online through the IRS tools instead of faxing; (2) for the remaining faxes (state agencies, some IRS units, banks), use Notifyre PAYG ($10 once, $0.03/page, API plus email-to-fax). Telnyx is the alternative if extreme per-page cost matters and $1/mo for a number is acceptable. (3) Keep FaxZero/GotFreeFax for non-PII only, if at all.
- Free services give no contractual service-provider oversight, which the FTC Safeguards Rule expects for vendors handling customer information. That is the main compliance problem, beyond the ad cover page.

### Gaps
- Pub 4557 does not appear to contain fax-specific rules (the search found none). The guidance above applies its general vendor and encryption principles.
- FaxZero and GotFreeFax retention periods: their privacy pages were not readable (FaxZero's returned 404).
- The FTC Safeguards Rule text was not fetched directly. The WISP requirement is cited from the IRS page.
