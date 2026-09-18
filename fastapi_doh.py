from fastapi import FastAPI, Request, Response
import socket
import base64

app = FastAPI()

def trimite_catre_udp(cerere_dns_bytes):
    socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_udp.settimeout(2.0)
    socket_udp.sendto(cerere_dns_bytes, ('dns_udp', 53))
    raspuns, _ = socket_udp.recvfrom(65535)
    socket_udp.close()
    return raspuns

@app.get("/dns-query")
async def interogare_dns_get(dns: str):
    completare = '=' * (4 - len(dns) % 4)
    cerere_dns_bytes = base64.urlsafe_b64decode(dns + completare)
    raspuns_udp = trimite_catre_udp(cerere_dns_bytes)
    return Response(content=raspuns_udp, media_type="application/dns-message")

@app.post("/dns-query")
async def interogare_dns_post(cerere: Request):
    cerere_dns_bytes = await cerere.body()
    raspuns_udp = trimite_catre_udp(cerere_dns_bytes)
    return Response(content=raspuns_udp, media_type="application/dns-message")
