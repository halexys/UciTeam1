# Winner

El binario no tiene PIE ni canario, por lo que sus direcciones de memoria no cambian y hay buffer overflow:
```
checksec --file=winner
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	FortifiableFILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   No Symbols	  No	0		3		winner
```

Revisando el binario con radare2 nos percatamos de que este primero toma de input un valor que cifra tras varias operaciones, luego compara esto con el segundo valor, si son iguales muestra el contenido de la flag:

El cifrado ocurre en la direccion 0x004012d0

La llamada a cat mediante system() ocurre en la direccion 0x004012b6

Un buffer overflow para poner el puntero de programa en la direccion 0x004012d0 no es posible porque el fallo termina con una llamada a exit():

![2025-03-30-221959_1080x202_scrot](https://github.com/user-attachments/assets/3372a45b-bed2-43f3-bb72-9ab2c411a2a3)

Sin embargo vemos que la direccion de memoria de la segunda entrada (s2) se encuentra a 32 bytes de donde se almacena la primera entrada transformada (s2):
```
[0x00401442]> afv
var char * s @ rbp-0x20
var char * s2 @ rbp-0x40
var char * s1 @ rbp-0x60
```

Podemos sobreescribir la salida cifrada por nuestra entrada y forzar una comparacion exitosa!

La primera entrada usa fgets, la segunda scanf:

```
|       :   0x00401483      be1f000000     mov esi, 0x1f               ; 31 ; int size
|       :   0x00401488      4889c7         mov rdi, rax                ; char *s
|       :   0x0040148b      e8e0fcffff     call sym.imp.fgets          ; char *fgets(char *s, int size, FILE *stream)
|       :   0x00401490      488d45c0       lea rax, [s2]
|       :   0x00401494      be1f000000     mov esi, 0x1f               ; 31 ; signed int64_t arg2
|       :   0x00401499      4889c7         mov rdi, rax                ; void *arg1
|       :   0x0040149c      e82ffeffff     call fcn.004012d0
|       :   0x004014a1      488d45e0       lea rax, [s]
|       :   0x004014a5      4889c6         mov rsi, rax
|       :   0x004014a8      488d05c90b..   lea rax, str.Hello__s       ; 0x402078 ; "Hello %s"
|       :   0x004014af      4889c7         mov rdi, rax                ; const char *format
|       :   0x004014b2      b800000000     mov eax, 0
|       :   0x004014b7      e874fcffff     call sym.imp.printf         ; int printf(const char *format)
|       :   0x004014bc      488d05c50b..   lea rax, str.Tell_me_your_favorite_Roblox_character__and_well_see_how_compatible_we_are: ; 0x402088 ; "Tell me your favorite Roblox character, and we'll see how compatible we are: "
|       :   0x004014c3      4889c7         mov rdi, rax                ; const char *s
|       :   0x004014c6      e835fcffff     call sym.imp.puts           ; int puts(const char *s)
|       :   0x004014cb      488d45a0       lea rax, [s1]
|       :   0x004014cf      4889c6         mov rsi, rax
|       :   0x004014d2      488d05fd0b..   lea rax, [0x004020d6]       ; "%s"
|       :   0x004014d9      4889c7         mov rdi, rax                ; const char *format
|       :   0x004014dc      b800000000     mov eax, 0
|       :   0x004014e1      e8cafcffff     call sym.imp.__isoc99_scanf ; int scanf(const char *format)
```

Hay que tener en cuenta que fgets solo esta leyendo 31 bytes de los 32 reservados

Nuestra carga util será 30 bytes de 'A', o cualquier otra cosa, luego 31 bytes nulos, para almacenar una cadena vacia en la primera cadena de la comparacion, y 1 byte nulo para almacenar una cadena vacia en la segunda cadena de la comparacion

La razon de usar bytes nulos es porque las cadenas en C y otros lenguajes similares son limitadas por el caracter nulo '\0', `no importa cuantos bytes vengan detras, la entrada solo consumira hasta el caracter nulo`

La comparacion se verá así: strcmp("","") lo cual es verdadero

`CodeVinciCTF{4r3_you_4_r3al_w1nn3?_4b2fc}`

 
