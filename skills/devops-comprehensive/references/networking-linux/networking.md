# Networking (الشبكات)

## 1. DNS

```
query → resolver → root → TLD → authoritative → A/AAAA/CNAME/TXT
```

- `dig +trace example.com` — see exactly where resolution stops.
- TTLs: lower (60–300s) before a migration so changes propagate fast; higher (3600s+) for stability.
- Common records: `A/AAAA` (host→IP), `CNAME` (alias — not allowed on apex), `TXT` (SPF/DKIM/verification), `MX` (mail).
- Debug order: is the record published? → resolver cache (old TTL)? → split-horizon/CDN routing? → local resolver?

## 2. TLS / HTTPS

```
ClientHello (cipher suites) → server cert (chain to CA) → verify hostname + expiry
→ key exchange → session keys → encrypted HTTP
```

- Cert expiry is a top-3 outage cause: automate (ACME/Let's Encrypt) + alert at 30 days.
- `openssl s_client -connect host:443 -servername host` — inspect chain, expiry, protocol.
- TLS 1.2 minimum; redirect 80 → 443; HSTS only after HTTPS works everywhere.
- Cert mismatch after a proxy/CDN: the edge must present a cert for the **public** hostname (SNI).

## 3. Ports & Firewalls

| Port | Service |
|------|---------|
| 22 | SSH |
| 53 | DNS (UDP+TCP) |
| 80/443 | HTTP/HTTPS |
| 3306/5432/6379 | MySQL/Postgres/Redis — **never public** |

- Default deny inbound; open only 22 (ideally from your IP), 80, 443. Databases reachable only over private networks/bastions.
- Debug: `curl -v` / `nc -zv host port` from the **client side**; then check host firewall (`ufw status`, `iptables -L -n`) and cloud security groups **in that order** — most "server down" is a security group.

## 4. HTTP Debugging

```bash
curl -sv https://example.com/api -o /dev/null     # headers, TLS, timing
curl -w '%{time_total}s %{http_code}\n' ...       # total time + status
```

- Read status classes: 4xx = client (fix request), 5xx = server (fix code), 429 = rate limit (backoff), 502/504 = upstream/gateway (proxy can't reach backend or it timed out).
- `X-Request-Id` end-to-end correlation across proxies; without it, a 502 is untraceable.

## 5. Load Balancing & Proxies

| Layer | Examples | Routes on |
|-------|----------|-----------|
| L4 (TCP) | NLB, HAProxy tcp | IP+port — fast, app-agnostic |
| L7 (HTTP) | ALB, nginx, Traefik | path/host/header — SSL termination, canary |

- Health checks must test **real readiness** (DB reachable), not just process alive.
- Timeouts chain: LB > backend, backend > downstream — misordered = LB gives up while backend still working (504s).
- Connection draining on deploy so in-flight requests finish.

## 6. Quick Diagnosis Ladder

```
1. DNS resolves?        dig / nslookup
2. TCP reachable?       nc -zv host port
3. TLS OK?              openssl s_client (expiry, chain)
4. HTTP responds?       curl -sv (status, headers)
5. App logic?           check app logs + trace id
```

Go top-down — 80% of "the site is down" stops at step 1–3.
