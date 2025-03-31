# Compiled Rome

Dentro de la funcion main esta la referencia a la flag en ROT13:
```
[0x000010c0]> s main
[0x000011ff]> pdf
            ; DATA XREF from entry0 @ 0x10d8(r)
/ 161: int main (int argc, char **argv, char **envp);
| afv: vars(3:sp[0x10..0x80])
|           0x000011ff      f30f1efa       endbr64
|           0x00001203      55             push rbp
|           0x00001204      4889e5         mov rbp, rsp
|           0x00001207      4883c480       add rsp, 0xffffffffffffff80
|           0x0000120b      64488b0425..   mov rax, qword fs:[0x28]
|           0x00001214      488945f8       mov qword [canary], rax
|           0x00001218      31c0           xor eax, eax
|           0x0000121a      488d05e70d..   lea rax, str.PbqrIvapvPGSI3av_ivQ1_P0zc1y1 ; 0x2008 ; "PbqrIvapvPGS{I3av_ivQ1_P0zc1y1}"
|           0x00001221      48894588       mov qword [var_78h], rax
|           0x00001225      488d05fc0d..   lea rax, str.Salve__peregrine__dic_mihi_nomen_tuum: ; 0x2028 ; "Salve, peregrine, dic mihi nomen tuum:"
|           0x0000122c      4889c7         mov rdi, rax                ; const char *s
```

```
echo "PbqrIvapvPGS{I3av_ivQ1_P0zc1y1}" | tr 'A-Za-z' 'N-ZA-Mn-za-m'
CodeVinciCTF{V3ni_viD1_C0mp1l1}
```

`CodeVinciCTF{V3ni_viD1_C0mp1l1}`
