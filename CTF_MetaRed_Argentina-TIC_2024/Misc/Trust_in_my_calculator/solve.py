from pwn import *

io = remote("calculator.ctf.cert.unlp.edu.ar",35003)

io.recvuntil(b"Bienvenidos! Resuelvan estas sumas para obtener la flag!:\n")

operacion = io.recvline().decode('utf-8').strip()
resultado = eval(operacion)
io.sendline(str(resultado))

line = io.recvline()
while "resolver" in str(line):
    operacion = io.recvline().decode('utf-8').strip()
    resultado = eval(operacion)
    io.sendline(str(resultado))
    line = io.recvline()

success(line)
