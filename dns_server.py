from scapy.all import DNS, DNSQR, DNSRR
import socket
import time

domenii_blocate = set()
fisier = open('adservers.txt', 'r')
for linie in fisier:
    if linie.startswith('0.0.0.0'):
        domenii_blocate.add(linie.split()[1].encode() + b'.')
fisier.close()

cache_dns = {}

socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
socket_server.bind(('0.0.0.0', 53))

while True:
    cerere, adresa_sursa = socket_server.recvfrom(65535)
    pachet = DNS(cerere)
    strat_dns = pachet.getlayer(DNS)

    if strat_dns is not None and strat_dns.opcode == 0:
        nume_domeniu = strat_dns.qd.qname
        nume_afisare = nume_domeniu.decode('utf-8')

        if nume_domeniu in domenii_blocate:
            print(f"[BLOCAT] {nume_afisare}")
            fisier_jurnal = open('blocked_queries.log', 'a')
            fisier_jurnal.write(nume_afisare + '\n')
            fisier_jurnal.close()

            raspuns_dns = DNSRR(rrname=nume_domeniu, ttl=330, type="A", rclass="IN", rdata='0.0.0.0')
            pachet_raspuns = DNS(id=pachet[DNS].id, qr=1, aa=0, rcode=0, qd=pachet.qd, an=raspuns_dns)
            socket_server.sendto(bytes(pachet_raspuns), adresa_sursa)
            continue

        if nume_domeniu in cache_dns and time.time() - cache_dns[nume_domeniu][1] < 300:
            print(f"[CACHE] {nume_afisare}")
            raspuns_dns = DNSRR(rrname=nume_domeniu, ttl=330, type="A", rclass="IN", rdata=cache_dns[nume_domeniu][0])
            pachet_raspuns = DNS(id=pachet[DNS].id, qr=1, aa=0, rcode=0, qd=pachet.qd, an=raspuns_dns)
            socket_server.sendto(bytes(pachet_raspuns), adresa_sursa)
            continue

        print(f"[FWD 8.8.8.8] {nume_afisare}")
        socket_redirectionare = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socket_redirectionare.settimeout(2.0)
        try:
            socket_redirectionare.sendto(cerere, ('8.8.8.8', 53))
            raspuns_google, _ = socket_redirectionare.recvfrom(65535)
            socket_server.sendto(raspuns_google, adresa_sursa)

            pachet_primit = DNS(raspuns_google)
            if pachet_primit.ancount > 0 and pachet_primit.an.type == 1:
                cache_dns[nume_domeniu] = (pachet_primit.an.rdata, time.time())
        except:
            print(f"[TIMEOUT] {nume_afisare}")
            pass
        socket_redirectionare.close()

socket_server.close()
