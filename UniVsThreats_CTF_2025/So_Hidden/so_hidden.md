# So Hidden

Descomprimir el APK y revisar la libreria nativa, contiene en las strings una IP y unas rutas:
```
r2 -A lib/x86_64/libnative-lib.so 2>/dev/null
 -- Use rabin2 to discover the real TRUTH
[0x00000ba0]> iz
[Strings]
nth paddr      vaddr      len size section type  string
-------------------------------------------------------
0   0x00000940 0x00000940 34  35   .rodata ascii /somebody-found-a-random-flag-path
1   0x00000963 0x00000963 51  52   .rodata ascii GET %s HTTP/1.1\r\nHost: %s:%d\r\nConnection: close\r\n\r\n
2   0x00000997 0x00000997 11  12   .rodata ascii 91.99.1.179
3   0x000009a3 0x000009a3 8   9    .rodata ascii /uvt-ctf
4   0x000009ac 0x000009ac 4   5    .rodata ascii \r\n\r\n
5   0x000009b1 0x000009b1 17  18   .rodata ascii DNS lookup failed
6   0x000009c3 0x000009c3 17  18   .rodata ascii Connection failed
7   0x000009d5 0x000009d5 6   7    .rodata ascii /jokes
```

Obtenemos el puerto haciendo una busqueda a la referencia de la IP:
```
[0x00000ba0]> iz
[Strings]
nth paddr      vaddr      len size section type  string
-------------------------------------------------------
0   0x00000940 0x00000940 34  35   .rodata ascii /somebody-found-a-random-flag-path
1   0x00000963 0x00000963 51  52   .rodata ascii GET %s HTTP/1.1\r\nHost: %s:%d\r\nConnection: close\r\n\r\n
2   0x00000997 0x00000997 11  12   .rodata ascii 91.99.1.179
3   0x000009a3 0x000009a3 8   9    .rodata ascii /uvt-ctf
4   0x000009ac 0x000009ac 4   5    .rodata ascii \r\n\r\n
5   0x000009b1 0x000009b1 17  18   .rodata ascii DNS lookup failed
6   0x000009c3 0x000009c3 17  18   .rodata ascii Connection failed
7   0x000009d5 0x000009d5 6   7    .rodata ascii /jokes
[0x00000ba0]> axt 0x00000997
sym.Java_com_example_uvt_1ctf_12025_Utils_getJoke 0xc20 [DATA:r--] lea rdi, str.91.99.1.179
sym.Java_com_example_uvt_1ctf_12025_Utils_getUVTCTF 0x1150 [DATA:r--] lea rdi, str.91.99.1.179
sym.Java_com_example_uvt_1ctf_12025_Utils_getHiddenFlag 0x11b0 [DATA:r--] lea rdi, str.91.99.1.179
[0x00000ba0]> s sym.Java_com_example_uvt_1ctf_12025_Utils_getJoke @ 0xc20
[0x00000c10]> pd 10
/ 91: sym.Java_com_example_uvt_1ctf_12025_Utils_getJoke (void *arg1, int64_t arg2);
| `- args(rdi, rsi) vars(4:sp[0x10..0x28])
|           0x00000c10      55             push rbp
|           0x00000c11      4889e5         mov rbp, rsp
|           0x00000c14      4883ec20       sub rsp, 0x20
|           0x00000c18      48897df8       mov qword [var_8h], rdi     ; arg1
|           0x00000c1c      488975f0       mov qword [var_10h], rsi    ; arg2
|           0x00000c20      488d3d70fd..   lea rdi, str.91.99.1.179    ; 0x997 ; "91.99.1.179" ; int64_t arg1
|           0x00000c27      befaa40000     mov esi, 0xa4fa             ; int64_t arg2   <==== PUERTO 
|           0x00000c2c      488d15a2fd..   lea rdx, str._jokes         ; 0x9d5 ; "/jokes" ; int64_t arg3
|           0x00000c33      e838000000     call fcn.00000c70        
|           0x00000c38      488945e8       mov qword [ptr], rax
[0x00000c10]> ?  0xa4fa
int32   42234   <====
uint32  42234
hex     0xa4fa
octal   0122372
unit    41.2K
segment 0000:a4fa
string  "\xfa\xa4"
fvalue  42234.0
float   0.000000000000000f
double  0.000000000000000
binary  0b1010010011111010
base36  0_wl6
ternary 0t2010221020
[0x00000c10]>
```

El puerto al que se conecta es al 0xa4fa(42234)

![2025-05-07-154939_1344x128_scrot](https://github.com/user-attachments/assets/ff42ce46-2634-4b30-8594-31c410b8d49d)

`UVT{m0b1l3_.s0_m4y_c0nt4in_s3ns1tiv3_1nf0}`
