# DNS Ad Blocker

## Overview

This project is a small DNS resolver with ad and tracker blocking. It checks requested domains against a blocklist and returns `0.0.0.0` for blocked entries, while forwarding other DNS queries upstream. It also exposes the same resolver through DNS-over-HTTPS, so browsers can use the service without plain DNS configuration.

## Tech stack

- Python 3
- Scapy for DNS packet parsing and responses
- FastAPI and Uvicorn for the DoH endpoint
- Docker Compose for running DNS and DoH services together

## Project structure

- `dns_server.py` — UDP DNS resolver, blocklist lookup, cache, and upstream forwarding.
- `fastapi_doh.py` — FastAPI service that forwards DoH requests to the local DNS container.
- `adservers.txt` — domain blocklist used by the resolver.
- `stats.py` — reads the blocked-query log and prints domain/company statistics.
- `requirements.txt` — Python dependencies for the application.
- `Dockerfile` — application image definition.
- `docker-compose.yml` — starts the UDP DNS and DoH services.

## Running it

The Docker setup is intended for a Linux host or VPS because it binds ports 53/UDP and 443/TCP.

```bash
cd adblocker
docker compose up --build
```

Before starting, update the certificate paths and domain in `docker-compose.yml` if you do not use the configured Let's Encrypt certificate. Test UDP DNS with `dig @<server-ip> example.com`; the DoH endpoint is available at `/dns-query`.
