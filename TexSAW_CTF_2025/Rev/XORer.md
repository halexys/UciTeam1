# XORer

El programa pide una contraseña al usuario. `main` acepta la entrada de usuario y luego invoca a check_password:
```
[0x00001235]> pdf
            ; DATA XREF from entry0 @ 0x1098(r)
/ 109: int main (int argc, char **argv, char **envp);
| afv: vars(2:sp[0x10..0x38])
|           0x00001235      55             push rbp
|           0x00001236      4889e5         mov rbp, rsp
|           0x00001239      4883ec30       sub rsp, 0x30
|           0x0000123d      64488b0425..   mov rax, qword fs:[0x28]
|           0x00001246      488945f8       mov qword [canary], rax
|           0x0000124a      31c0           xor eax, eax
|           0x0000124c      488d05ec0d..   lea rax, str.Enter_password: ; 0x203f ; "Enter password: "
|           0x00001253      4889c7         mov rdi, rax                ; const char *format
|           0x00001256      b800000000     mov eax, 0
|           0x0000125b      e800feffff     call sym.imp.printf         ; int printf(const char *format)
|           0x00001260      488d45d0       lea rax, [var_30h]
|           0x00001264      4889c6         mov rsi, rax
|           0x00001267      488d05e20d..   lea rax, str._31s           ; 0x2050 ; "%31s"
|           0x0000126e      4889c7         mov rdi, rax                ; const char *format
|           0x00001271      b800000000     mov eax, 0
|           0x00001276      e8f5fdffff     call sym.imp.__isoc99_scanf ; int scanf(const char *format)
|           0x0000127b      488d45d0       lea rax, [var_30h]
|           0x0000127f      4889c7         mov rdi, rax                ; char *arg1
|           0x00001282      e8f2feffff     call sym.check_password
|           0x00001287      b800000000     mov eax, 0
|           0x0000128c      488b55f8       mov rdx, qword [canary]
|           0x00001290      64482b1425..   sub rdx, qword fs:[0x28]
|       ,=< 0x00001299      7405           je 0x12a0
|       |   0x0000129b      e8b0fdffff     call sym.imp.__stack_chk_fail ; void __stack_chk_fail(void)
|       |   ; CODE XREF from main @ 0x1299(x)
|       `-> 0x000012a0      c9             leave
\           0x000012a1      c3             ret
```

Analicemos `check_password`:
```
0x00001179]> pdf
            ; CALL XREF from main @ 0x1282(x)
/ 188: sym.check_password (char *arg1);
| `- args(rdi) vars(6:sp[0x10..0x30])
|           0x00001179      55             push rbp
|           0x0000117a      4889e5         mov rbp, rsp
|           0x0000117d      4883ec30       sub rsp, 0x30
|           0x00001181      48897dd8       mov qword [s], rdi          ; arg1
|           0x00001185      64488b0425..   mov rax, qword fs:[0x28]
|           0x0000118e      488945f8       mov qword [canary], rax
|           0x00001192      31c0           xor eax, eax
|           0x00001194      48b8cb95d1..   movabs rax, 0xfa96cdd1fad195cb
|           0x0000119e      488945ec       mov qword [var_14h], rax
|           0x000011a2      c745f4c3c9..   mov dword [var_ch], 0xc291c9c3
|           0x000011a9      488b45d8       mov rax, qword [s]
|           0x000011ad      4889c7         mov rdi, rax                ; const char *s
|           0x000011b0      e88bfeffff     call sym.imp.strlen         ; size_t strlen(const char *s)
|           0x000011b5      8945e8         mov dword [var_18h], eax
|           0x000011b8      c745e40000..   mov dword [var_1ch], 0
|       ,=< 0x000011bf      eb3d           jmp 0x11fe
|       |   ; CODE XREF from sym.check_password @ 0x1202(x)
|      .--> 0x000011c1      8b45e4         mov eax, dword [var_1ch]
|      :|   0x000011c4      4863d0         movsxd rdx, eax
|      :|   0x000011c7      488b45d8       mov rax, qword [s]
|      :|   0x000011cb      4801d0         add rax, rdx
|      :|   0x000011ce      0fb600         movzx eax, byte [rax]
|      :|   0x000011d1      0fbec0         movsx eax, al
|      :|   0x000011d4      34a5           xor al, 0xa5
|      :|   0x000011d6      89c2           mov edx, eax
|      :|   0x000011d8      8b45e4         mov eax, dword [var_1ch]
|      :|   0x000011db      4898           cdqe
|      :|   0x000011dd      0fb64405ec     movzx eax, byte [rbp + rax - 0x14]
|      :|   0x000011e2      0fb6c0         movzx eax, al
|      :|   0x000011e5      39c2           cmp edx, eax
|     ,===< 0x000011e7      7411           je 0x11fa
|     |:|   0x000011e9      488d05180e..   lea rax, str.Wrong_password_ ; 0x2008 ; "Wrong password!"
|     |:|   0x000011f0      4889c7         mov rdi, rax                ; const char *s
|     |:|   0x000011f3      e838feffff     call sym.imp.puts           ; int puts(const char *s)
|    ,====< 0x000011f8      eb25           jmp 0x121f
|    ||:|   ; CODE XREF from sym.check_password @ 0x11e7(x)
|    |`---> 0x000011fa      8345e401       add dword [var_1ch], 1
|    | :|   ; CODE XREF from sym.check_password @ 0x11bf(x)
|    | :`-> 0x000011fe      837de407       cmp dword [var_1ch], 7
|    | `==< 0x00001202      7ebd           jle 0x11c1
|    |      0x00001204      488b45d8       mov rax, qword [s]
|    |      0x00001208      4889c6         mov rsi, rax
|    |      0x0000120b      488d05060e..   lea rax, str.Correct__Heres_your_flag:_texsaw_s_n ; 0x2018 ; "Correct! Here's your flag: texsaw{%s}\n"
|    |      0x00001212      4889c7         mov rdi, rax                ; const char *format
|    |      0x00001215      b800000000     mov eax, 0
|    |      0x0000121a      e841feffff     call sym.imp.printf         ; int printf(const char *format)
|    |      ; CODE XREF from sym.check_password @ 0x11f8(x)
|    `----> 0x0000121f      488b45f8       mov rax, qword [canary]
|           0x00001223      64482b0425..   sub rax, qword fs:[0x28]
|       ,=< 0x0000122c      7405           je 0x1233
|       |   0x0000122e      e81dfeffff     call sym.imp.__stack_chk_fail ; void __stack_chk_fail(void)
|       |   ; CODE XREF from sym.check_password @ 0x122c(x)
|       `-> 0x00001233      c9             leave
\           0x00001234      c3             ret
```

Aqui almacenan unas cadenas de bytes sospechosas en dos variables
```
|           0x00001194      48b8cb95d1..   movabs rax, 0xfa96cdd1fad195cb
|           0x0000119e      488945ec       mov qword [var_14h], rax
|           0x000011a2      c745f4c3c9..   mov dword [var_ch], 0xc291c9c3
```

Aqui hay un bucle que:
- Carga un byte de var_14h y un byte de la entrada de usuario (s)
- Realiza un XOR con el byte de la entrada de usuario y 0xa5
- Compara ambos bytes
- Si son diferentes muestra el mensaje `Wrong password!`
- Si son iguales sigue comparando hasta comparar 8 caracteres
- Muestra el mensaje  `Correct! Here's your flag: texsaw{%s}`

```
|       ,=< 0x000011bf      eb3d           jmp 0x11fe
|       |   ; CODE XREF from sym.check_password @ 0x1202(x)
|      .--> 0x000011c1      8b45e4         mov eax, dword [var_1ch]
|      :|   0x000011c4      4863d0         movsxd rdx, eax
|      :|   0x000011c7      488b45d8       mov rax, qword [s]
|      :|   0x000011cb      4801d0         add rax, rdx
|      :|   0x000011ce      0fb600         movzx eax, byte [rax]
|      :|   0x000011d1      0fbec0         movsx eax, al
|      :|   0x000011d4      34a5           xor al, 0xa5
|      :|   0x000011d6      89c2           mov edx, eax
|      :|   0x000011d8      8b45e4         mov eax, dword [var_1ch]
|      :|   0x000011db      4898           cdqe
|      :|   0x000011dd      0fb64405ec     movzx eax, byte [rbp + rax - 0x14]
|      :|   0x000011e2      0fb6c0         movzx eax, al
|      :|   0x000011e5      39c2           cmp edx, eax
|     ,===< 0x000011e7      7411           je 0x11fa
|     |:|   0x000011e9      488d05180e..   lea rax, str.Wrong_password_ ; 0x2008 ; "Wrong password!"
|     |:|   0x000011f0      4889c7         mov rdi, rax                ; const char *s
|     |:|   0x000011f3      e838feffff     call sym.imp.puts           ; int puts(const char *s)
|    ,====< 0x000011f8      eb25           jmp 0x121f
|    ||:|   ; CODE XREF from sym.check_password @ 0x11e7(x)
|    |`---> 0x000011fa      8345e401       add dword [var_1ch], 1
|    | :|   ; CODE XREF from sym.check_password @ 0x11bf(x)
|    | :`-> 0x000011fe      837de407       cmp dword [var_1ch], 7
|    | `==< 0x00001202      7ebd           jle 0x11c1
|    |      0x00001204      488b45d8       mov rax, qword [s]
|    |      0x00001208      4889c6         mov rsi, rax
|    |      0x0000120b      488d05060e..   lea rax, str.Correct__Heres_your_flag:_texsaw_s_n ; 0x2018 ; "Correct! Here's your flag: texsaw{%s}\n"
|    |      0x00001212      4889c7         mov rdi, rax                ; const char *format
|    |      0x00001215      b800000000     mov eax, 0
|    |      0x0000121a      e841feffff     call sym.imp.printf         ; int printf(const char *format)
```

Podemos probar y hacer XOR con los bytes de var_14h:
``` python
checked_bytes = 0xfa96cdd1fad195cb.to_bytes(length=8,byteorder='little')
password = "".join(chr(b ^ 0xa5) for b in checked_bytes)
print(f"The password is: {password}")
```
```
 python3 XORer.py
The password is: n0t_th3_
./XORer
Enter password: n0t_th3_
Correct! Here's your flag: texsaw{n0t_th3_}
```

Sin embargo la flag esta incompleta, si agregamos los bytes de var_ch entonces sí obtenemos el mensaje completo:

``` python
checked_bytes = 0xfa96cdd1fad195cb.to_bytes(length=8,byteorder='little')
more_bytes = 0xc291c9c3.to_bytes(length=4,byteorder='little')
stored_bytes = checked_bytes + more_bytes
password = "".join(chr(b ^ 0xa5) for b in stored_bytes)
print(f"The password is: {password}")
```

```
python3 XORer.py
The password is: n0t_th3_fl4g
./XORer
Enter password: n0t_th3_fl4g
Correct! Here's your flag: texsaw{n0t_th3_fl4g}
```

`texsaw{n0t_th3_fl4g}`
