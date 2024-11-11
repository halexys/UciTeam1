# Rev / Baby rev

Lo abrimos con un desensamblador como radare2: 

`r2 -A expectations`

En el decompilado de main observamos que si existe el fichero /tmp/superSecretDirectory/SuperDuperSecretFlag.txt entonces escribirá allí la flag:

```
 0x00001390      488d05840c..   lea rax, str._tmp_superSecretDirectory ; 0x201b ; "/tmp/superSecretDirectory"
|           0x00001397      4889c7         mov rdi, rax                ; int64_t arg1
|           0x0000139a      e835ffffff     call sym.directory_exists
|           0x0000139f      85c0           test eax, eax
|       ,=< 0x000013a1      0f84af000000   je 0x1456
|       |   0x000013a7      488d058a0c..   lea rax, str._tmp_superSecretDirectory_SuperDuperSecretFlag.txt ; 0x2038 ; "/tmp/superSecretDirectory/SuperDuperSecretFlag.txt"
|       |   0x000013ae      4889c7         mov rdi, rax                ; int64_t arg1
|       |   0x000013b1      e894ffffff     call sym.file_exists
|       |   0x000013b6      85c0           test eax, eax
|      ,==< 0x000013b8      0f8487000000   je 0x1445
|      ||   0x000013be      488d45b0       lea rax, [var_50h]
|      ||   0x000013c2      be40000000     mov esi, 0x40               ; elf_phdr ; int64_t arg2
|      ||   0x000013c7      4889c7         mov rdi, rax                ; int64_t arg1
|      ||   0x000013ca      e87afeffff     call sym.reveal_flag
|      ||   0x000013cf      488d05950c..   lea rax, [0x0000206b]       ; "w"
|      ||   0x000013d6      4889c6         mov rsi, rax                ; const char *mode
|      ||   0x000013d9      488d05580c..   lea rax, str._tmp_superSecretDirectory_SuperDuperSecretFlag.txt ; 0x2038 ; "/tmp/superSecretDirectory/SuperDuperSecretFlag.txt"
|      ||   0x000013e0      4889c7         mov rdi, rax                ; const char *filename
|      ||   0x000013e3      e848fdffff     call sym.imp.fopen          ; file*fopen(const char *filename, const char *mode)
|      ||   0x000013e8      488945a8       mov qword [stream], rax
|      ||   0x000013ec      48837da800     cmp qword [stream], 0
|     ,===< 0x000013f1      7516           jne 0x1409
|     |||   0x000013f3      488d05730c..   lea rax, str.I_cant_open_the_file. ; 0x206d ; "I can't open the file."
|     |||   0x000013fa      4889c7         mov rdi, rax                ; const char *s
|     |||   0x000013fd      e83efdffff     call sym.imp.perror         ; void perror(const char *s)
|     |||   0x00001402      b801000000     mov eax, 1
|    ,====< 0x00001407      eb61           jmp 0x146a
|    ||||   ; CODE XREF from main @ 0x13f1(x)
|    |`---> 0x00001409      488d55b0       lea rdx, [var_50h]          ;   ...
|    | ||   0x0000140d      488b45a8       mov rax, qword [stream]
|    | ||   0x00001411      488d0d6c0c..   lea rcx, [0x00002084]       ; "%s\n"
|    | ||   0x00001418      4889ce         mov rsi, rcx                ; const char *format
|    | ||   0x0000141b      4889c7         mov rdi, rax                ; FILE *stream
|    | ||   0x0000141e      b800000000     mov eax, 0
|    | ||   0x00001423      e8d8fcffff     call sym.imp.fprintf        ; int fprintf(FILE *stream, const char *format,   ...)
|    | ||   0x00001428      488b45a8       mov rax, qword [stream]
|    | ||   0x0000142c      4889c7         mov rdi, rax                ; FILE *stream
|    | ||   0x0000142f      e8acfcffff     call sym.imp.fclose         ; int fclose(FILE *stream)
|    | ||   0x00001434      488d054d0c..   lea rax, str.Flag_written_  ; 0x2088 ; "Flag written!"
|    | ||   0x0000143b      4889c7         mov rdi, rax                ; const char *s
```

Creamos el fichero, ejecutamos el programa y obtenemos la flag:

``` bash
mkdir /tmp/superSecretDirectory/
touch /tmp/superSecretDirectory/SuperDuperSecretFlag.txt
./expectations
Flag written!
cat /tmp/superSecretDirectory/SuperDuperSecretFlag.txt
flag{H3rE_15_Y0uR_R3ew4rd!!}
```

`flag{H3rE_15_Y0uR_R3ew4rd!!}`
