# FlagsFlagsFlags

Es un binario escrito en Go, esta empaquetado asi que hay que usar `upx -d` para descomprimirlo.

Si hacemos un `strings` al binario y filtramos por "flag{" encontramos un bloque de flags (en Go las cadenas forman estos bloques porque no terminan en null y se tratan de manera diferente)

Si limpiamos un poco y lo guardamos en un archivo, como "flags.txt" podemos observar que son 10000 posibles flags:

```
strings flags_patched| grep -Eo "flag{.*}" > flags.txt
sed -i 's/}/}\n/g' flags.txt
```

Podemos hacer fuerza bruta, acelerando el proceso usando varios hilos:
```python
import asyncio
import sys

CONCURRENCY = 100
found = False

async def try_flag(semaphore, flag, index):
    global found
    async with semaphore:
        if found:
            return
        try:
            proc = await asyncio.create_subprocess_exec(
                './flags_patched',
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.DEVNULL
            )

            try:
                stdout, _ = await asyncio.wait_for(
                    proc.communicate((flag + '\n').encode()), timeout=4.5
                )
            except asyncio.TimeoutError:
                try:
                    proc.kill()
                except ProcessLookupError:
                    pass
                return

            if found:
                return

            out = stdout.decode()
            print(f"[{index}] Trying: {flag}")
            if "Incorrect flag!" not in out:
                found = True
                print(f"\n[+] Found valid flag at line {index}: {flag}")
                print(f"[+] Output:\n{out}")
                sys.exit(0)
            print(out)

        except Exception as e:
            print(f"[{index}] Error: {e}")

async def main():
    with open("flags.txt", "r") as f:
        flags = f.readlines()

    semaphore = asyncio.Semaphore(CONCURRENCY)
    tasks = [
        asyncio.create_task(try_flag(semaphore, flag.strip(),i))
        for i, flag in enumerate(flags)
    ]

    await asyncio.gather(*tasks, return_exceptions=True)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user.")
```

