# Reverse / cargo

## Paso 1

Obtenemos un binario, lo analizamos con radare2 y vemos que fue escrito en Go, esto se comprueba al buscar cadenas como 'GOARCH' o 'GOOS' y obtener algo asi:

``` asm
izz~GOARCH
9641  0x000970f0 0x004970f0 218  219  .rodata            ascii   path\tcommand-line-arguments\nbuild\t-buildmode=exe\nbuild\t-compiler=gc\nbuild\tCGO_ENABLED=1\nbuild\tCGO_CFLAGS=\nbuild\tCGO_CPPFLAGS=\nbuild\tCGO_CXXFLAGS=\nbuild\tCGO_LDFLAGS=\nbuild\tGOARCH=amd64\nbuild\tGOOS=linux\nbuild\tGOAMD64=v1\n
13131 0x000ec03b 0x004ec03b 218  219  .go.buildinfo      ascii   path\tcommand-line-arguments\nbuild\t-buildmode=exe\nbuild\t-compiler=gc\nbuild\tCGO_ENABLED=1\nbuild\tCGO_CFLAGS=\nbuild\tCGO_CPPFLAGS=\nbuild\tCGO_CXXFLAGS=\nbuild\tCGO_LDFLAGS=\nbuild\tGOARCH=amd64\nbuild\tGOOS=linux\nbuild\tGOAMD64=v1\n
```

Los binarios en go estan estaticamente enlazados, lo que significa que no acceden a librerias externas, por lo que contienen todo lo necesario para funcionar por sí solos, por ende encontramos facilmente mas de 1000 funciones hasta en un simple HolaMundo.

``` asm
[0x00465760]> afl|wc -l
1330
```  

Nos centramos en estas tres funciones:
``` asm
0x00465760    8    172 sym.main.map.init.0
0x00465820   11    151 sym.main.main
0x004658c0    5     76 sym.main.main.func1
```

La primera 'sym.main.map.init.0' describe la inicializacion de un objeto Map en Go. Se reservan 39 bytes:

``` asm
|      |:   0x00465779      bb27000000     mov ebx, 0x27               ; '\'' ; 39
|      |:   0x0046577e      31c9           xor ecx, ecx                ; int64_t arg_18h
|      |:   0x00465780      e81b75faff     call sym.runtime.makemap
```


Tambien vemos una llamada a sym.runtime.mapassign_fast32, que se usa para crear un mapa de runas o caracteres UINT32:
``` asm
| ; CODE XREF from sym.main.map.init.0 @ 0x4657d5(x)
| 0x0046578e      48894c2420     mov qword [var_20h], rcx
| 0x00465793      488d15ea17..   lea rdx, [0x00496f84]                 ; U"w5xgoe{4b8p7uqdsk6r9132f0_lamcn" ; int64_t arg_10h
| 0x0046579a      8b348a         mov esi, dword [rdx + rcx*4]          ; int64_t arg_8h
| 0x0046579d      8974241c       mov dword [var_1ch], esi
| 0x004657a1      488d3d4017..   lea rdi, str.vjtyzihncmal_0f2319r6ksdqu7p8b4eogx5ww5xgoe4b8p7uqdsk6r9132f0_lamcnhizytjv ; 0x496ee8 ; "v" ; int64_t arg4
| 0x004657a8      448b048f       mov r8d, dword [rdi + rcx*4]
| 0x004657ac      4889c3         mov rbx, rax
| 0x004657af      488d05ea88..   lea rax, [0x0046e0a0]
| 0x004657b6      4489c1         mov ecx, r8d                          ; int64_t arg_18h
| 0x004657b9      e8a28cfaff     call sym.runtime.mapassign_fast32
```

La funcion para crear mapas varia, por ejemplo, aqui hay un map con cadenas como indices y valores y este es el ensamblador equivalente:

``` go
  var constantes = map[string]float32{
    "PI":3.141516, "E": .71828, 
 }
```

``` asm
/ 177: sym.main.init ();
| afv: vars(1:sp[0x10..0x10])
|       .-> 0x0045d180      493b6610       cmp rsp, qword [r14 + 0x10]
|      ,==< 0x0045d184      0f869d000000   jbe 0x45d227
|      |:   0x0045d18a      55             push rbp
|      |:   0x0045d18b      4889e5         mov rbp, rsp
|      |:   0x0045d18e      4883ec28       sub rsp, 0x28
|      |:   0x0045d192      e849f8faff     call sym.runtime.makemap_small
|      |:   0x0045d197      4889442420     mov qword [var_20h], rax
|      |:   0x0045d19c      4889c3         mov rbx, rax
|      |:   0x0045d19f      488d0dc20b..   lea rcx, [0x0046dd68]       ; "PIM ,  [(\"\")) )\n @s -> Pn=][}\n]\n: i)> \n \t  +\"\nfinnilobjgc %: gp  *(in  n= - NaN  P m=  MPC=],  < end > ...]:\n???pc=  Gadxaessha" ; int64_t arg_10h
|      |:   0x0045d1a6      bf02000000     mov edi, 2                  ; int64_t arg1
|      |:   0x0045d1ab      488d054e7b..   lea rax, [0x00464d00]
|      |:   0x0045d1b2      e8691bfbff     call sym.runtime.mapassign_faststr
|      |:   0x0045d1b7      f30f10057d..   movss xmm0, dword [obj._f32.40490e99] ; [0x48843c:4]=0x40490e99
|      |:   0x0045d1bf      f30f1100       movss dword [rax], xmm0
|      |:   0x0045d1c3      488d05367b..   lea rax, [0x00464d00]
|      |:   0x0045d1ca      488b5c2420     mov rbx, qword [var_20h]
|      |:   0x0045d1cf      488d0d820b..   lea rcx, obj.go:string.     ; 0x46dd58 ; "E]+ :).?/=-[<{}_PIM ,  [(\"\")) )\n @s -> Pn=][}\n]\n: i)> \n \t  +\"\nfinnilobjgc %: gp  *(in  n= - NaN  P m=  MPC=],  < end > ...]:\n???pc=  Gadxaesshaavxfmaallgallprootitabsbrkidledead is LEAFbase of ) =  <==GOGC] = s + ,r2= pc=true+Inf-Inf: p=cas1cas2cas3cas4cas5cas6 at \n\tm= sp= sp: lr: fp= gp= mp=) m=ermssse3avx2bmi1bmi2defersweeptestRtestWexecWexecRschedhchansudoggscanmheaptracepanicsleep cnt=gcing MB,  got= ...\n max=scav  ptr ] = (" ; int64_t arg_10h
|      |:   0x0045d1d6      bf01000000     mov edi, 1                  ; int64_t arg1
|      |:   0x0045d1db      0f1f440000     nop dword [rax + rax]
|      |:   0x0045d1e0      e83b1bfbff     call sym.runtime.mapassign_faststr
```

Centrandonos en el Map de nuestro binario vemos una string con las runas:
``` asm
[0x004649c0]> s str.vjtyzihncmal_0f2319r6ksdqu7p8b4eogx5ww5xgoe4b8p7uqdsk6r9132f0_lamcnhizytjv
[0x004958d0]> pd 1
            ;-- str.vjtyzihncmal_0f2319r6ksdqu7p8b4eogx5ww5xgoe4b8p7uqdsk6r9132f0_lamcnhizytjv:
            ; DATA XREF from sym.main.map.init.0 @ 0x464a01(r)
            0x004958d0     .string "vjt}yzihncmal_0f2319r6ksdqu7p8b4{eogx5ww5xgoe{4b8p7uqdsk6r9132f0_lamcnhizy}tjv" ; len=316
```

La forma en la que se representan en este caso no tengo claro por que se ve así, pero teniendo en cuenta que se reservan 39 bytes (todas las runas son ASCII), es decir, 39 indices y esta cadena tiene 78 caracteres entonces asumimos que los primeros 39 son las claves y el resto los valores

`vjt}yzihncmal_0f2319r6ksdqu7p8b4{eogx5w => w5xgoe{4b8p7uqdsk6r9132f0_lamcnhizy}tjv`

En ghidra se puede observar mejor la diferencia y resulta que es asi:
```
 Valores:
        00465793 48 8d 15        LEA        param_3,[DAT_00496f84]                           = 00000077h
                 ea 17 03 00
 Claves:
        004657a1 48 8d 3d        LEA        param_1,[DAT_00496ee8]                           = 00000076h
                 40 17 03 00
```

Como dato adicional vemos el nombre de la variable:
```
 0x00464a4a      488b0d8fe3..   mov rcx, qword [obj.runtime.bss] ; obj.main.lookupTable
```



Entonces por ahora tenemos esto
``` go
 var lookupTable = map[rune]rune{
    'v': 'w', 'j': '5', 't': 'x', '}': 'g', 'y': 'o', 'z': 'e', 'i': '{', 'h': '4', 'n': 'b', 'c': '8',
    'm': 'p', 'a': '7', 'l': 'u', '_': 'q', '0': 'd', 'f': 's', '2': 'k', '3': '6', '1': 'r', '9': '9',
    'r': '1', '6': '3', 'k': '2', 's': 'f', 'd': '0', 'q': '_', 'u': 'l', '7': 'a', 'p': 'm', '8': 'c',
    'b': 'n', '4': 'h', '{': 'i', 'e': 'z', 'o': 'y', 'g': '}', 'x': 't', '5': 'j', 'w': 'v',
 }
```

## Paso 2

Desensamblamos 'sym.main.main'. Esta vez con ghidra porque muestra el proceso mas claro:
``` asm
                             **************************************************************
                             * DWARF original prototype: void main.main(void)             *
                             **************************************************************
                             undefined __stdcall main.main(undefined * * param_1, fun
             undefined         AL:1           <RETURN>
             undefined * *     RDI:8          param_1
             func() * *        RSI:8          param_2
             undefined8        RDX:8          param_3
             int               RCX:8          param_4
             undefined * *     R8:8           param_5
             undefined * *     R9:8           param_6
                             main.main                                       XREF[5]:     Entry Point(*), 
                                                                                          runtime.main:004330bb(c), 
                                                                                          004658b2(j), 00481038(*), 
                                                                                          .debug_frame::0000f39c(*)  
        00465820 49 3b 66 10     CMP        RSP,qword ptr [R14 + 0x10]
        00465824 0f 86 83        JBE        LAB_004658ad
                 00 00 00
        0046582a 55              PUSH       RBP
        0046582b 48 89 e5        MOV        RBP,RSP
        0046582e 48 83 ec 18     SUB        RSP,0x18
        00465832 48 83 3d        CMP        qword ptr [os.Args.len],0x2
                 2e be 08 
                 00 02
        0046583a 74 0a           JZ         LAB_00465846
        0046583c b8 01 00        MOV        EAX,0x1
                 00 00
        00465841 e8 7a f3        CALL       os.Exit                                          undefined os.Exit(undefined8 par
                 ff ff
                             LAB_00465846                                    XREF[1]:     0046583a(j)  
        00465846 48 8b 0d        MOV        param_4,qword ptr [os.Args.len]
                 1b be 08 00
        0046584d 48 83 f9 01     CMP        param_4,0x1
        00465851 76 4f           JBE        LAB_004658a2
        00465853 48 8b 15        MOV        param_3,qword ptr [os.Args]
                 06 be 08 00
        0046585a 48 8b 5a 10     MOV        RBX,qword ptr [param_3 + 0x10]
        0046585e 48 8b 4a 18     MOV        param_4,qword ptr [param_3 + 0x18]
        00465862 48 8d 05        LEA        RAX,[PTR_main.main.func1_00480f70]               = 004658c0
                 07 b7 01 00
        00465869 e8 12 fa        CALL       strings.Map                                      undefined * * strings.Map(undefi
                 ff ff
        0046586e 48 83 fb 32     CMP        RBX,0x32
        00465872 75 15           JNZ        LAB_00465889
        00465874 48 8d 1d        LEA        RBX,[s_p8xsi8dlba61rb9q0obhpr8qhbhuojrj_0047d0   = "p8xsi8dlba61rb9q0obhpr8qhbhuo
                 a1 a9 01 00
        0046587b b9 32 00        MOV        param_4,0x32
                 00 00
        00465880 e8 fb cf        CALL       runtime.memequal                                 bool runtime.memequal(void)
                 f9 ff
        00465885 84 c0           TEST       AL,AL
        00465887 75 0c           JNZ        LAB_00465895
                             LAB_00465889                                    XREF[1]:     00465872(j)  
        00465889 b8 01 00        MOV        EAX,0x1
                 00 00
        0046588e e8 2d f3        CALL       os.Exit                                          undefined os.Exit(undefined8 par
                 ff ff
        00465893 eb 07           JMP        LAB_0046589c
                             LAB_00465895                                    XREF[1]:     00465887(j)  
        00465895 31 c0           XOR        EAX,EAX
        00465897 e8 24 f3        CALL       os.Exit                                          undefined os.Exit(undefined8 par
                 ff ff
                             LAB_0046589c                                    XREF[1]:     00465893(j)  
        0046589c 48 83 c4 18     ADD        RSP,0x18
        004658a0 5d              POP        RBP
        004658a1 c3              RET
                             LAB_004658a2                                    XREF[1]:     00465851(j)  
        004658a2 b8 01 00        MOV        EAX,0x1
                 00 00
        004658a7 e8 14 94        CALL       runtime.panicIndex                               undefined runtime.panicIndex(voi
                 ff ff
        004658ac 90              NOP
                             LAB_004658ad                                    XREF[1]:     00465824(j)  
        004658ad e8 4e 73        CALL       runtime.morestack_noctxt                         undefined runtime.morestack_noct
                 ff ff
        004658b2 e9 69 ff        JMP        main.main
                 ff ff
        004658b7 cc cc cc        align      align(9)
                 cc cc cc 
                 cc cc cc

```

+ El programa debe tener un unico argumento, sino entonces se cierra con os.Exit(1)
+ Almacena el primer argumento (os.Args[1]) y llama a strings.Map, que aplica una funcion específica a cada caracter del string os.Args[1] y lo guarda en un nuevo string. En este caso es main.main.func1
+ Verifica que el argumento tenga una extension de 0x32 (50) caracteres, sino entonces se cierra con os.Exit(1)
+ Carga la cadena `p8xsi8dlba61rb9q0obhpr8qhbhuojrjqrjqshr1uoqjrpmu6g`
+ Realiza la comparacion entre la cadena anterior y el resultado de strings.Map(function,os.Args[1])

Aclaracion: La cadena es extremadamente larga por la forma en que Go trata las cadenas. A diferencia de los lenguajes tipo C, donde las cadenas son secuencias de caracteres terminadas en un carácter nulo, las cadenas en Go son secuencias de bytes con una longitud fija. Las cadenas son estructuras específicas de Go, formadas por un puntero a la ubicación de la cadena y un número entero, que es la longitud de la cadena.

Va quedando asi:
``` go 
package main

import (
	"os"
	"strings"
)

var lookupTable = map[rune]rune{
    'v': 'w', 'j': '5', 't': 'x', '}': 'g', 'y': 'o', 'z': 'e', 'i': '{', 'h': '4', 'n': 'b', 'c': '8',
    'm': 'p', 'a': '7', 'l': 'u', '_': 'q', '0': 'd', 'f': 's', '2': 'k', '3': '6', '1': 'r', '9': '9',
    'r': '1', '6': '3', 'k': '2', 's': 'f', 'd': '0', 'q': '_', 'u': 'l', '7': 'a', 'p': 'm', '8': 'c',
    'b': 'n', '4': 'h', '{': 'i', 'e': 'z', 'o': 'y', 'g': '}', 'x': 't', '5': 'j', 'w': 'v',
 }
 var firstString = "p8xsi8dlba61rb9q0obhpr8qhbhuojrjqrjqshr1uoqjrpmu6"

func main() {
 if len(os.Args) != 2 {
   os.Exit(1)
 }

 // flag
 secondString := strings.Map(decode,os.Args[1])

 if secondString != firstString {
   os.Exit(1)
 }

 os.Exit(0)
}

func decode(r rune) rune {
 // falta implementar 
 return r
}
```

## Paso 3

La funcion main.main.func analiza si el caracter es una clave de lookupTable, si es así devuelve el valor de esa clave, en caso contrario devuelve el mismo caracter.
``` asm
                             **************************************************************
                             * DWARF original prototype: void main.main.func1(int32 r,... *
                             **************************************************************
                             int __stdcall main.main.func1(undefined8 param_1, void *
             int               EAX:4          <RETURN>
             undefined8        RDI:8          param_1
             void *            RSI:8          param_2
             undefined8        RDX:8          param_3
             int32             Stack[0x8]:4   r_spill                                 XREF[4]:     004658ce(W), 
                                                                                                   004658f3(R), 
                                                                                                   004658fd(W), 
                                                                                                   00465906(R)  
                             main.main.func1                                 XREF[4]:     Entry Point(*), 0046590a(j), 
                                                                                          00480f70(*), 
                                                                                          .debug_frame::0000f3cc(*)  
        004658c0 49 3b 66 10     CMP        RSP,qword ptr [R14 + 0x10]
        004658c4 76 37           JBE        LAB_004658fd
        004658c6 55              PUSH       RBP
        004658c7 48 89 e5        MOV        RBP,RSP
        004658ca 48 83 ec 18     SUB        RSP,0x18
        004658ce 89 44 24 28     MOV        dword ptr [RSP + r_spill],EAX
        004658d2 48 8b 1d        MOV        RBX,qword ptr [main.lookupTable]                 = NaP
                 27 bb 08 00
        004658d9 89 c1           MOV        ECX,EAX
        004658db 48 8d 05        LEA        RAX,[DAT_0046e0a0]                               = 08h
                 be 87 00 00
        004658e2 e8 f9 89        CALL       runtime.mapaccess2_fast32                        uint8 * runtime.mapaccess2_fast3
                 fa ff
        004658e7 84 db           TEST       BL,BL
        004658e9 74 08           JZ         LAB_004658f3
        004658eb 8b 00           MOV        EAX,dword ptr [RAX]
        004658ed 48 83 c4 18     ADD        RSP,0x18
        004658f1 5d              POP        RBP
        004658f2 c3              RET
                             LAB_004658f3                                    XREF[1]:     004658e9(j)  
        004658f3 8b 44 24 28     MOV        EAX,dword ptr [RSP + r_spill]
        004658f7 48 83 c4 18     ADD        RSP,0x18
        004658fb 5d              POP        RBP
        004658fc c3              RET
                             LAB_004658fd                                    XREF[1]:     004658c4(j)  
        004658fd 89 44 24 08     MOV        dword ptr [RSP + r_spill],EAX
        00465901 e8 fa 72        CALL       runtime.morestack_noctxt                         undefined runtime.morestack_noct
                 ff ff
        00465906 8b 44 24 08     MOV        EAX,dword ptr [RSP + r_spill]
        0046590a eb b4           JMP        main.main.func1
```

Este es el programa final

``` go
package main

import (
	"os"
	"strings"
)

var lookupTable = map[rune]rune{
    'v': 'w', 'j': '5', 't': 'x', '}': 'g', 'y': 'o', 'z': 'e', 'i': '{', 'h': '4', 'n': 'b', 'c': '8',
    'm': 'p', 'a': '7', 'l': 'u', '_': 'q', '0': 'd', 'f': 's', '2': 'k', '3': '6', '1': 'r', '9': '9',
    'r': '1', '6': '3', 'k': '2', 's': 'f', 'd': '0', 'q': '_', 'u': 'l', '7': 'a', 'p': 'm', '8': 'c',
    'b': 'n', '4': 'h', '{': 'i', 'e': 'z', 'o': 'y', 'g': '}', 'x': 't', '5': 'j', 'w': 'v',
 }
 var firstString = "p8xsi8dlba61rb9q0obhpr8qhbhuojrjqrjqshr1uoqjrpmu6"

func main() {
 if len(os.Args) != 2 {
   os.Exit(1)
 }
 // flag
 secondString := strings.Map(transform,os.Args[1])

 // lookupTable es bidireccional, transform(transform(str)) == str
 // aqui obtenemos la flag pasando cualquier argumento
 flag := strings.Map(transform,firstString)
 print(flag)

 if secondString != firstString {
   os.Exit(1)
 }
 os.Exit(0)
}

func transform(r rune) rune {
 mapped, ok := lookupTable[r]
 if ok {
  return mapped
 }
 return r
}
```

Obtenemos la flag
``` bash
 go run cargo.go argumento1
  mctf{c0un73r1n9_dyn4m1c_4n4ly515_15_f41rly_51mpl3}exit status 1
 ./cargo mctf{c0un73r1n9_dyn4m1c_4n4ly515_15_f41rly_51mpl3} && echo "Exito!"
  Exito!
```

`mctf{c0un73r1n9_dyn4m1c_4n4ly515_15_f41rly_51mpl3}`





