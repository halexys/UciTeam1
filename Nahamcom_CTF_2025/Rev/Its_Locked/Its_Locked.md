# It's Locked

Podemos ver las ordenes ejecutadas en el script de bash con la opcion -x: `bash -x flag.sh`

De ahí podemos extraer un eval que hace varias operaciones con estas variables que contienen datos cifrados:
``` bash
BCL='\''aWQgLXUK'\''                                      # base64 de "id -u"
BCV='\''93iNKe0zcKfgfSwQoHYdJbWGu4Dfnw5ZZ5a3ld5UEqI='\''
echo $BCV
P=llLvO8+J6gmLlp964bcJG3I3mY27I9ACsJTvXYCZv2Q=
S='\''lRwuwaugBEhK488I'\''
C=3eOcpOICWx5iy2UuoJS9gQ==
```

La flag esta entre estos datos. A lo largo del programa hay varias llamadas a openssl para descifrar alguno de estos datos con `openss` y AES cbc mode:
```
Encriptado: $BCV
Clave: "B-${ID}-${UID}"
Resultado esperado: "TEST-VALUE-VERIFY"

Encriptado: $P
Clave: $_k (resultado de _bcl_get, puede ser "255" o "${valor_de_usuario-${UID}")
Resultado: $_P

Encriptado:$C
Clave: "C-${S}-${_P}"
Resultado $str (se intenta ejecutar luego)

Luego hay tres operaciones mas con openssl usando scripts de Perl dificiles de leer
```

Para comenzar la cadena de desencriptados debemos saber quienes son ID y UID.

Nos dicen que el `ID` es "hello", el script prueba como`ID` el resultado de cuatro comandos distintos:
``` bash
    command -v dmidecode > /dev/null && _bcl_verify "$(dmidecode -t 1 2> /dev/null | LANG=C perl -ne '\''/UUID/ && print && exit'\'')" && return;
    _bcl_verify "$({ ip l sh dev "$(LANG=C ip route show match 1.1.1.1 | perl -ne '\''s/.*dev ([^ ]*) .*/\1/ && print && exit'\'')" | LANG=C perl -ne '\''print if /ether / && s/.*ether ([^ ]*).*/\1/'\''; } 2> /dev/null)" && return;
    _bcl_verify "$({ blkid -o export | LANG=C perl -ne '\''/^UUID/ && s/[^[:alnum:]]//g && print && exit'\''; } 2> /dev/null)" && return;
    _bcl_verify "$({ fdisk -l | LANG=C perl -ne '\''/identifier/i && s/[^[:alnum:]]//g && print && exit'\''; } 2> /dev/null)" && return
```

El UID es el ID de usuario actual obtenido con `id -u`.

Podemos cambiar el contenido e `/etc/machine-id` con "hello" para obtener el `ID` correcto.

Para obtener el `UID` esperado hice este script para hallarlo por fuerza bruta:
``` python
import subprocess
CIPHERTEXT="93iNKe0zcKfgfSwQoHYdJbWGu4Dfnw5ZZ5a3ld5UEqI="
MAX_ID=10000
print("[*] Starting UID Bruteforce...\n")

for idnum in range(0,MAX_ID+1):
    KEY=f"B-hello-{idnum}"
    decrypted = subprocess.check_output(f"echo \"{CIPHERTEXT}\" | base64 -d | openssl enc -d -aes-256-cbc -md sha256 -nosalt -k \"{KEY}\" 2>/dev/null| tr -d '\\000'",
                                        shell=True,
                                        stderr= subprocess.DEVNULL)
    decrypted = decrypted.replace(b'\x00', b'').decode('utf-8', errors='ignore')
    if "TEST-VALUE-VERIFY" in decrypted:
        print(f"[*] UID found: {idnum}")
        exit(0)
    if idnum % 100 == 0:
        print(f"\rProgress: {idnum}/{MAX_ID}", end="", flush=True)
print("[*] Correct UID not found")

```
El `UID` correcto es 1338.

Ejecutamos el script con: `sudo UID=1338 ./flag.sh`

Pero no nos devuelve nada relevante. Con strace podemos observar que si se hace un syscall `write` pero al descriptor de archivo '3', no a stdout:
```
sudo UID=1338 strace ./flag.sh
...
rt_sigprocmask(SIG_SETMASK, [], NULL, 8) = 0
rt_sigaction(SIGCHLD, NULL, {sa_handler=SIG_DFL, sa_mask=[], sa_flags=0}, 8) = 0
rt_sigaction(SIGIO, NULL, {sa_handler=SIG_DFL, sa_mask=[], sa_flags=0}, 8) = 0
write(3, "echo \"flag{f2ea4caf879bde891f017"..., 70) = 70
close(3)                                = 0
exit_group(2)                           = ?
+++ exited with 2 +++
```

De hecho lo envia a /dev/null:
```
kalcast@debian:~/Descargas/Solve/Its_Locked$ sudo UID=1338 strace ./flag.sh 2>&1  | grep open
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "./flag.sh", O_RDONLY) = 3
read(3, "| openssl base64 -d -A 2> /dev/n"..., 128) = 128
read(3, "for x in openssl perl gunzip; do"..., 128) = 128
openat(AT_FDCWD, "/dev/null", O_WRONLY|O_CREAT|O_TRUNC, 0666) = 3
newfstatat(AT_FDCWD, "/usr/local/sbin/openssl", 0x7ffe419c1e80, 0) = -1 ENOENT (No existe el fichero o el directorio)
newfstatat(AT_FDCWD, "/usr/local/bin/openssl", 0x7ffe419c1e80, 0) = -1 ENOENT (No existe el fichero o el directorio)
newfstatat(AT_FDCWD, "/usr/sbin/openssl", 0x7ffe419c1e80, 0) = -1 ENOENT (No existe el fichero o el directorio)
newfstatat(AT_FDCWD, "/usr/bin/openssl", {st_mode=S_IFREG|0755, st_size=1099208, ...}, 0) = 0
write(1, "/usr/bin/openssl\n", 17)      = 17
openat(AT_FDCWD, "/dev/null", O_WRONLY|O_CREAT|O_TRUNC, 0666) = 3
openat(AT_FDCWD, "/dev/null", O_WRONLY|O_CREAT|O_TRUNC, 0666) = 3
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libm.so.6", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libcrypt.so.1", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/dev/urandom", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/dev/urandom", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/dev/null", O_RDONLY|O_CLOEXEC) = 3

kalcast@debian:~/Descargas/Solve/Its_Locked$ sudo UID=1338 strace ./flag.sh 2>&1  | grep write
write(1, "/usr/bin/openssl\n", 17)      = 17
write(1, "/usr/bin/perl\n", 14)         = 14
write(1, "/usr/bin/gunzip\n", 16)       = 16
write(3, "echo \"flag{f2ea4caf879bde891f017"..., 70) = 70
```

Con strace podemos filtrar por syscall y fd:
```
sudo UID=1338 strace -e trace=write -e write=3 ./flag.sh
--- SIGCHLD {si_signo=SIGCHLD, si_code=CLD_EXITED, si_pid=69072, si_uid=0, si_status=0, si_utime=0, si_stime=0} ---
--- SIGCHLD {si_signo=SIGCHLD, si_code=CLD_EXITED, si_pid=69073, si_uid=0, si_status=0, si_utime=0, si_stime=0} ---
--- SIGCHLD {si_signo=SIGCHLD, si_code=CLD_EXITED, si_pid=69074, si_uid=0, si_status=0, si_utime=0, si_stime=0} ---
--- SIGCHLD {si_signo=SIGCHLD, si_code=CLD_EXITED, si_pid=69090, si_uid=0, si_status=0, si_utime=0, si_stime=0} ---
write(1, "/usr/bin/openssl\n", 17)      = 17
write(1, "/usr/bin/perl\n", 14)         = 14
write(1, "/usr/bin/gunzip\n", 16)       = 16
--- SIGCHLD {si_signo=SIGCHLD, si_code=CLD_EXITED, si_pid=69091, si_uid=0, si_status=0, si_utime=0, si_stime=0} ---
--- SIGCHLD {si_signo=SIGCHLD, si_code=CLD_EXITED, si_pid=69096, si_uid=0, si_status=0, si_utime=0, si_stime=0} ---
--- SIGCHLD {si_signo=SIGCHLD, si_code=CLD_EXITED, si_pid=69099, si_uid=0, si_status=0, si_utime=0, si_stime=0} ---

gzip: stdin: decompression OK, trailing garbage ignored
--- SIGCHLD {si_signo=SIGCHLD, si_code=CLD_EXITED, si_pid=69102, si_uid=0, si_status=2, si_utime=0, si_stime=0} ---
write(3, "echo \"flag{f2ea4caf879bde891f017"..., 70) = 70
 | 00000  65 63 68 6f 20 22 66 6c  61 67 7b 66 32 65 61 34  echo "flag{f2ea4 |
 | 00010  63 61 66 38 37 39 62 64  65 38 39 31 66 30 31 37  caf879bde891f017 |
 | 00020  34 66 35 32 38 63 32 30  36 38 32 7d 22 0a 65 63  4f528c20682}".ec |
 | 00030  68 6f 20 22 43 6f 6e 67  72 61 75 6c 61 74 69 6f  ho "Congraulatio |
 | 00040  6e 73 21 22 0a 0a                                 ns!"..           |
+++ exited with 2 +++
```


