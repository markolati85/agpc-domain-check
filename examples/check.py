"""Check a few domains and print an honest one-line summary each."""
import sys

sys.path.insert(0, "..")
from agpc_domain_check import check                       # noqa: E402
from agpc_domain_check.client import summarise            # noqa: E402

for domain in sys.argv[1:] or ["stripe.com", "github.com"]:
    try:
        print(summarise(check(domain)))
    except Exception as exc:
        print(f"{domain}: could not be checked — {exc}")
