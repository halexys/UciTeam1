from pwn import *
shares = []
for i in range(20):
    #io = process(["python3", "ASSS.py"])
    io = remote("asss.atreides.b01lersc.tf",8443,ssl=True,sni=True)
    io.recvuntil(b"Here is a ^_^: ")
    a = int(io.recvline().strip())
    io.recvuntil(b"Here is your share ^_^: (")
    line = io.recvline().strip().decode()
    x, y = line.split(", ")
    x = int(x)
    y = int(y[:-1])  # Eliminar el paréntesis final
    shares.append((x, y))
    io.close()

print(f"V = {shares}")
