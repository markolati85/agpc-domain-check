# Domain authentication check — free API, no key

Check whether anyone can send email as a domain.

```bash
curl "https://guild.tradeuniquecapital.com/api/check?domain=example.com"
```

No signup, no API key, no account. 20 calls per caller per hour.

It runs the same engine as the paid audit over one domain and returns what it
actually found — not a teaser with the findings removed.

## What it checks

- **SPF**, including the RFC 7208 ten-lookup limit that silently breaks it
- **DKIM** selectors
- **DMARC** — and whether it *enforces* or only *monitors*, which is the
  difference between protection and a report nobody reads
- **Cross-domain DMARC reporting authorisation** (RFC 7489 §7.1) — the
  external `rua` authorisation record almost nobody publishes
- **MX** and **null-MX** (RFC 7505)

## The one rule it follows

**A failed lookup is never reported as a finding.**

If a DNS query times out, the response says the check was incomplete. It does
not say "no SPF record". Those mean different things, and only one of them is
a problem with the domain — telling somebody they are unprotected when they
may be fine is the worst thing a checker can do.

```jsonc
{
  "domain": "example.com",
  "grade": "B",
  "checks_completed": 3,
  "checks_total": 4,
  "complete": false,        // ← treat as unknown, not as a fault
  "findings": { "...": "..." }
}
```

## Install

```bash
pip install httpx     # or use urllib; the client has no hard dependency
```

Then copy `agpc_domain_check/client.py`, or:

```python
from agpc_domain_check import check

result = check("example.com")
print(result["grade"], result["findings"]["dmarc"])
```

JavaScript is in `examples/check.js` — it is twenty lines and has no
dependencies.

## Machine-readable

| | |
|---|---|
| OpenAPI 3.1 | `https://guild.tradeuniquecapital.com/openapi.json` |
| Agent card | `https://guild.tradeuniquecapital.com/.well-known/agent-card.json` |
| One-fetch summary | `https://guild.tradeuniquecapital.com/.well-known/agents.json` |
| For LLMs | `https://guild.tradeuniquecapital.com/llms.txt` |

Point any agent framework at the OpenAPI document and it can call this
unattended.

## Earn from it

If you send someone who buys the full audit, you take **25% of the settled
amount — EUR 37.25 per audit**.

```bash
curl -X POST https://guild.tradeuniquecapital.com/partners/terms \
  -H 'Content-Type: application/json' \
  -d '{"agent_id":"your-agent","code":"YOURCODE","rate":0.25}'
```

Then send people to `https://guild.tradeuniquecapital.com/order?ref=YOURCODE`.

- Up to **25%** is accepted immediately. Above that is **reviewed**, not
  refused. Above 40% is refused — past that the referral costs more than the
  work earns.
- Paid when the order **settles** — the money is in the account, not merely
  promised.
- **Reversed if the order is refunded.** You are not paid for our bad debt.

Not paid for: traffic or leads that never pay, refunded orders, and anything
obtained by deception, spam, unlawful scraping, or access to systems you are
not authorised to use.

## What the paid audit adds

Up to five domains in one order, DKIM probed across 34 known provider
selectors, prioritised remediation with the exact records to publish, and a
written report you can hand to whoever runs the DNS. **EUR 149, one-time.**

## Who runs this

Marko Latinović, a natural person resident in Serbia, in a personal capacity.
Not a company. There are no customer testimonials, because there are no
customers yet, and inventing them would be the first thing worth distrusting
about a security service.

Contact: markol@tradeuniquecapital.com

## Licence

MIT for the client code in this repository. The API is free to call within
the stated rate limit.
