# DNS Ad Blocker cu DNS-over-HTTPS

Un resolver DNS scris în Python care blochează domenii cunoscute pentru reclame și tracking, păstrează un cache simplu și oferă aceeași rezolvare prin DNS-over-HTTPS (DoH).

## Ce conține

- `dns_server.py` ascultă pe UDP/53, blochează domeniile din `adservers.txt` cu răspunsul `0.0.0.0` și trimite restul interogărilor către 8.8.8.8.
- `fastapi_doh.py` expune endpoint-ul DoH compatibil cu `GET` și `POST` la `/dns-query`.
- `stats.py` produce statistici din jurnalul `blocked_queries.log`.
- `docker-compose.yml` pornește serviciul DNS și endpoint-ul HTTPS.

## Cerințe

- Docker și Docker Compose pe Linux/VPS pentru rularea pe porturile 53 și 443;
- un certificat Let's Encrypt valid pentru domeniul configurat în `docker-compose.yml`.

## Rulare

1. Schimbă calea și domeniul certificatului din `docker-compose.yml` dacă nu folosești `retele.me`.
2. Rulează `docker compose up --build` din acest director.
3. Testează DNS-ul UDP cu `dig @<ip-server> example.com` și DoH cu `https://<domeniu>/dns-query`.

Jurnalele, certificatele și variabilele de mediu sunt excluse din Git. Lista de blocare este păstrată pentru ca demonstrația să poată fi refăcută.
