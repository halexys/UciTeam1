# Misc / Trust in my calculator

```
$ nc calculator.ctf.cert.unlp.edu.ar 35003
 _______  _______ _________ _______  _______  _______  ______  
(       )(  ____ \__   __/(  ___  )(  ____ )(  ____ \(  __  \ 
| () () || (    \/   ) (   | (   ) || (    )|| (    \/| (  \  )
| || || || (__       | |   | (___) || (____)|| (__    | |   ) |
| |(_)| ||  __)      | |   |  ___  ||     __)|  __)   | |   | |
| |   | || (         | |   | (   ) || (\ (   | (      | |   ) |
| )   ( || (____/\   | |   | )   ( || ) \ \__| (____/\| (__/  )
|/     \|(_______/   )_(   |/     \||/   \__/(_______/(______/ 
                                                               

Bienvenidos! Resuelvan estas sumas para obtener la flag!:
2941 * 320
Mmmm tardaste mucho amiguito
```

El programa pide que devuelvas el resultado de cada ecuacion que te solicite, este es el script que usé para automatizar el proceso:

``` python
from pwn import *

io = remote("calculator.ctf.cert.unlp.edu.ar",35003)

io.recvuntil(b"Bienvenidos! Resuelvan estas sumas para obtener la flag!:\n")

operacion = io.recvline().decode('utf-8').strip()
resultado = eval(operacion)
io.sendline(str(resultado))

line = io.recvline()
while "resolver" in str(line):
    operacion = io.recvline().decode('utf-8').strip()
    resultado = eval(operacion)
    io.sendline(str(resultado))
    line = io.recvline()

success(line)
```

`flag{warm0+0up_now_you_can_try_pwn!}`
