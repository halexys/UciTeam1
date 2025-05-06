import dns.message, dns.query
import socket

# Crear consulta DNS TXT para flag.tiktok.com
query = dns.message.make_query("TIKTOK.com", dns.rdatatype.TXT)

# Enviar consulta al servicio
with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.connect(('challs.umdctf.io',32300))
    s.send(len(query.to_wire()).to_bytes(4) + query.to_wire())
    response = s.recv(1024)

# Extraer la flag de la respuesta DNS
print(response.decode())
