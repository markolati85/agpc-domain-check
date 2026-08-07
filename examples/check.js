// No dependencies. Node 18+ (built-in fetch).
const BASE = "https://guild.tradeuniquecapital.com";

export async function check(domain, { ref = "" } = {}) {
  const q = new URLSearchParams({ domain, ...(ref ? { ref } : {}) });
  const res = await fetch(`${BASE}/api/check?${q}`);
  const body = await res.json();
  if (!res.ok) throw new Error(body.error || `HTTP ${res.status}`);
  return body;
}

// An incomplete result means a lookup failed. It is not a finding about the
// domain, and reporting it as one tells somebody they are unprotected when
// they may be fine.
export const isConclusive = (r) => Boolean(r.complete);

if (import.meta.url === `file://${process.argv[1]}`) {
  const domain = process.argv[2] || "example.com";
  const r = await check(domain);
  console.log(isConclusive(r)
    ? `${r.domain}: grade ${r.grade}`
    : `${r.domain}: INCOMPLETE (${r.checks_completed}/${r.checks_total})`);
}
