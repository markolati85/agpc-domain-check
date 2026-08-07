"""A client small enough to read in one sitting.

Standard library only, so it drops into any project without a dependency
decision. The only thing it insists on is the distinction the API itself
insists on: an incomplete result is not a finding.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://guild.tradeuniquecapital.com"
TIMEOUT = 60


class CheckError(RuntimeError):
    """The check could not be run. Not a statement about the domain."""


def check(domain: str, *, ref: str = "", base: str = BASE,
          timeout: int = TIMEOUT) -> dict:
    """Check one domain's email authentication.

    `ref` attributes the call to your referral code.

    Raises CheckError when the request itself failed — a refusal, a rate
    limit, an unreachable host. That is deliberately a different outcome from
    a completed check with poor findings, because they call for different
    responses: one is retried, the other is fixed.
    """
    query = {"domain": domain}
    if ref:
        query["ref"] = ref
    url = f"{base}/api/check?{urllib.parse.urlencode(query)}"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        try:
            detail = json.loads(exc.read().decode("utf-8")).get("error", "")
        except Exception:
            detail = exc.reason
        raise CheckError(f"HTTP {exc.code}: {detail}") from None
    except (urllib.error.URLError, OSError, ValueError) as exc:
        raise CheckError(f"{type(exc).__name__}: {exc}") from None


def is_conclusive(result: dict) -> bool:
    """Did every check complete?

    Use this before acting on findings. A result with `complete` false means
    a lookup failed, and reporting that as "no SPF record" tells somebody
    they are unprotected when they may be fine.
    """
    return bool(result.get("complete"))


def summarise(result: dict) -> str:
    """One line a human can read, honest about incompleteness."""
    if not is_conclusive(result):
        return (f"{result.get('domain')}: INCOMPLETE — "
                f"{result.get('checks_completed')} of "
                f"{result.get('checks_total')} checks ran. Findings below are "
                f"partial; nothing here says the domain is misconfigured.")
    issues = result.get("findings", {}).get("issues") or []
    gaps = result.get("findings", {}).get("effectiveness_gaps") or []
    if not issues and not gaps:
        return f"{result.get('domain')}: grade {result.get('grade')} — no issues found."
    return (f"{result.get('domain')}: grade {result.get('grade')} — "
            f"{len(issues)} issue(s), {len(gaps)} effectiveness gap(s).")
